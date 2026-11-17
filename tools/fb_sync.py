#!/usr/bin/env python3
"""Naujienų skilties sinchronizacija su facebook.com/TSPstatyba.

Viešas puslapis be prisijungimo atiduoda naujausią įrašą (tekstą, datą, nuorodą,
nuotrauką arba reel'o mp4). Jei jo dar nėra assets/news.json, skriptas:
  1. paruošia mediją: nuotrauka -> img/news-<id>-{700,1000,1400}.webp (3:2),
     video -> paskutinės 10 s, 720x480 H.264 video/news-<id>.mp4 + poster;
  2. įdeda įrašą į news.json viršų ir palieka 3 naujausius;
  3. ištrina iškritusių įrašų failus;
  4. perrašo index.html naujienų bloką (gen.build_news).

Paleidžia GitHub Actions (.github/workflows/fb-sync.yml) kas 3 val.
Išėjimo kodai: 0 = viskas gerai (su nauju įrašu arba be), 1 = FB nieko neatidavė.
Reikia: python3, Pillow, ffmpeg (tik video įrašams).
"""
import datetime as dt
import glob
import html as ihtml
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = "https://www.facebook.com/TSPstatyba"
NEWS = os.path.join(ROOT, "assets", "news.json")
KEEP = 3
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36")
HEADERS = {
    "User-Agent": UA,
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "lt-LT,lt;q=0.9,en;q=0.8",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Site": "none",
}
MONTHS = ("Sausio", "Vasario", "Kovo", "Balandžio", "Gegužės", "Birželio", "Liepos",
          "Rugpjūčio", "Rugsėjo", "Spalio", "Lapkričio", "Gruodžio")
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿⌀-⏿⬀-⯿"
                   "︎️‍⃣]")


def get(url, binary=False):
    last = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            return data if binary else data.decode("utf-8", "replace")
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(3 + attempt * 5)
    raise last


def jstr(s):
    """FB JSON eilutė (su \\/ ir \\uXXXX) -> python str."""
    return json.loads('"%s"' % s)


def field(seg, pattern):
    m = re.search(pattern, seg)
    return jstr(m.group(1)) if m else None


def parse_stories(page):
    """Visi puslapio įrašai: post_id, laikas, tekstas, nuoroda, media."""
    anchors = list(re.finditer(r'"post_id":"(\d+)","creation_time":(\d+)', page))
    out, seen = [], set()
    for i, a in enumerate(anchors):
        pid, ts = a.group(1), int(a.group(2))
        if pid in seen:
            continue
        seen.add(pid)
        end = anchors[i + 1].start() if i + 1 < len(anchors) else a.start() + 80000
        seg = page[a.start():end]
        story = {"id": pid, "ts": ts,
                 "text": field(seg, r'"message":\{"text":"((?:[^"\\]|\\.)*)"') or "",
                 "url": field(seg, r'"permalink_url":"((?:[^"\\]|\\.)*)"')
                 or "https://www.facebook.com/100063790592393/posts/%s" % pid,
                 "video": None, "photo": None, "photo_uri": None}
        kind = re.match(r'[^\]]{0,200}?"attachments":\[\{"media":\{"__typename":"(\w+)"(?:,"__isNode":"\w+")?,"id":"(\d+)"',
                        seg[len(a.group(0)):])
        if kind and kind.group(1) == "Video":
            story["video"] = (field(seg, r'"browser_native_hd_url":"((?:[^"\\]|\\.)*)"')
                              or field(seg, r'"browser_native_sd_url":"((?:[^"\\]|\\.)*)"'))
            story["photo_uri"] = field(seg, r'"preferred_thumbnail":\{"image":\{"uri":"((?:[^"\\]|\\.)*)"')
        elif kind and kind.group(1) == "Photo":
            story["photo"] = kind.group(2)
            story["photo_uri"] = field(seg, r'"image":\{"uri":"((?:[^"\\]|\\.)*)"')
        out.append(story)
    return out


def clean_text(t):
    t = EMOJI.sub("", t)
    t = re.sub(r"#\w+", "", t)
    t = re.sub(r"\s+[–—]\s+", ", ", t)
    t = re.sub(r"\s+-\s+", ", ", t)
    t = re.sub(r"\s*\n\s*", " ", t)
    t = re.sub(r"\s{2,}", " ", t).strip(" ,")
    t = re.sub(r"\s+([,.!?])", r"\1", t)
    if len(t) > 360:
        cut = t[:360]
        stop = max(cut.rfind(". "), cut.rfind("! "), cut.rfind("? "))
        t = cut[:stop + 1] if stop > 160 else cut.rsplit(" ", 1)[0].rstrip(",;:") + "…"
    return t


def lt_label(ts):
    try:
        from zoneinfo import ZoneInfo
        d = dt.datetime.fromtimestamp(ts, ZoneInfo("Europe/Vilnius"))
    except Exception:  # noqa: BLE001
        d = dt.datetime.utcfromtimestamp(ts + 2 * 3600)
    return d.strftime("%Y-%m-%d"), "%s %d d." % (MONTHS[d.month - 1], d.day)


def largest_photo(fbid, fallback):
    """Pilna nuotraukos raiška iš facebook.com/photo/?fbid= (be prisijungimo)."""
    try:
        h = get("https://www.facebook.com/photo/?fbid=%s" % fbid)
        best = None
        for m in re.finditer(r'"image":\{"uri":"((?:[^"\\]|\\.)*)","width":(\d+),"height":(\d+)', h):
            w = int(m.group(2))
            if not best or w > best[0]:
                best = (w, jstr(m.group(1)))
        if best and best[0] >= 900:
            return best[1]
    except Exception as e:  # noqa: BLE001
        print("photo page failed:", e)
    return fallback


def save_webp(src, base, widths):
    from PIL import Image, ImageOps
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    w, h = im.size
    tw, th = (w, round(w * 2 / 3)) if h >= w * 2 / 3 else (round(h * 3 / 2), h)
    x = (w - tw) // 2
    y = int((h - th) * 0.4)
    im = im.crop((x, y, x + tw, y + th))
    made = []
    for W in widths:
        if W > tw * 1.15 and made:
            break
        out = os.path.join(ROOT, "img", "%s-%d.webp" % (base, W))
        im.resize((W, round(W * 2 / 3)), Image.LANCZOS).save(out, "WEBP", quality=80, method=6)
        made.append(out)
    return made


CROP = "scale=720:480:force_original_aspect_ratio=increase,crop=720:480"


def frame_scores(raw, tmp):
    """Kiekvieno 0,5 s kadro „turtingumas“ kortelės kirpime (tuščia siena mažai, kambarys daug)."""
    from PIL import Image, ImageFilter, ImageStat
    d = os.path.join(tmp, "frames")
    os.makedirs(d, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-vf", "fps=2," + CROP + ",scale=288:192",
                    os.path.join(d, "%04d.png")], check=True)
    scores = []
    for f in sorted(glob.glob(os.path.join(d, "*.png"))):
        im = Image.open(f).convert("L")
        # entropija: daug tonų = kambarys su baldais; siena ar balta+TV = mažai
        scores.append(im.entropy() + 0.05 * ImageStat.Stat(im.filter(ImageFilter.FIND_EDGES)).mean[0])
    return scores


def make_video(url, base, tmp):
    raw = os.path.join(tmp, "raw.mp4")
    with open(raw, "wb") as f:
        f.write(get(url, binary=True))
    dur = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", raw],
        capture_output=True, text=True, check=True).stdout.strip())
    scores = frame_scores(raw, tmp)
    length = min(10.0, dur)
    # reel'ai dažniausiai „prieš -> po“: pradžios (~30 %) nenaudoti, iš likusio imti
    # 10 s langą su daugiausiai detalių (ne tuščias sienas), lygiosiose vėlesnį
    lo = min(dur * 0.3, max(0.0, dur - length))
    hi = max(lo, dur - length - 0.2)
    best, start, t = None, lo, lo
    while t <= hi + 1e-6:
        win = scores[int(t * 2):int((t + length) * 2)] or [0]
        val = sum(win) / len(win)
        if best is None or val >= best - 0.01:
            best, start = val, t
        t += 0.5
    out = os.path.join(ROOT, "video", "%s.mp4" % base)
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-ss", "%.2f" % start, "-i", raw, "-t", "%.2f" % length,
         "-vf", CROP, "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "30",
         "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], check=True)
    # poster = detaliausias lango kadras (rodomas iki paleidimo ir prie reduced-motion)
    win = scores[int(start * 2):int((start + length) * 2)]
    pt = start + (win.index(max(win)) / 2 if win else 0)
    poster = os.path.join(tmp, "poster.jpg")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "%.2f" % pt, "-i", raw, "-frames:v", "1",
                    "-vf", CROP, "-q:v", "2", poster], check=True)
    save_webp(poster, base, (700,))
    print("video %.1f s, langas %.1f-%.1f s, poster %.1f s" % (dur, start, start + length, pt))
    return out


def drop_files(entry, keep_bases):
    for key, pattern in (("img", "img/%s-*.webp"), ("video", "video/%s.mp4")):
        base = entry.get(key)
        if base and base not in keep_bases:
            for f in glob.glob(os.path.join(ROOT, pattern % base)):
                os.remove(f)
                print("removed", os.path.relpath(f, ROOT))


def known(posts, pid):
    return any(p.get("id") == pid or p["url"].rstrip("/").endswith(pid) for p in posts)


def main():
    page = get(PAGE)
    stories = parse_stories(page)
    if not stories:
        print("FB neatidavė nė vieno įrašo (login siena ar pasikeitęs HTML).")
        return 1
    with open(NEWS, encoding="utf-8") as f:
        posts = json.load(f)

    new = [s for s in sorted(stories, key=lambda s: -s["ts"]) if not known(posts, s["id"])]
    newest_known = max((p["date"] for p in posts), default="")
    new = [s for s in new if lt_label(s["ts"])[0] >= newest_known]
    if not new:
        print("naujų įrašų nėra; naujausias FB:", stories[0]["id"], lt_label(stories[0]["ts"])[0])
        return 0

    with tempfile.TemporaryDirectory() as tmp:
        for s in reversed(new):
            base = "news-%s" % s["id"]
            date, label = lt_label(s["ts"])
            entry = {"id": s["id"], "date": date, "label": label, "text": clean_text(s["text"]),
                     "url": s["url"], "img": None, "video": None, "alt": ""}
            if s["video"]:
                make_video(s["video"], base, tmp)
                entry.update(img=base, video=base,
                             alt="Vaizdo įrašas iš TSP Statyba Facebook puslapio")
            elif s["photo"] or s["photo_uri"]:
                uri = largest_photo(s["photo"], s["photo_uri"]) if s["photo"] else s["photo_uri"]
                src = os.path.join(tmp, "photo.jpg")
                with open(src, "wb") as f:
                    f.write(get(uri, binary=True))
                if save_webp(src, base, (700, 1000, 1400)):
                    entry.update(img=base, alt="Nuotrauka iš TSP Statyba Facebook įrašo")
            if not entry["text"] and not entry["img"]:
                print("praleistas tuščias įrašas", s["id"])
                continue
            posts.insert(0, entry)
            print("pridėtas", s["id"], date, entry["text"][:60])

    posts.sort(key=lambda p: p["date"], reverse=True)
    keep, gone = posts[:KEEP], posts[KEEP:]
    keep_bases = {p.get(k) for p in keep for k in ("img", "video")}
    for p in gone:
        drop_files(p, keep_bases)
    with open(NEWS, "w", encoding="utf-8") as f:
        json.dump(keep, f, ensure_ascii=False, indent=2)
        f.write("\n")

    os.chdir(ROOT)
    sys.path.insert(0, ROOT)
    import gen
    gen.build_news()
    return 0


if __name__ == "__main__":
    sys.exit(main())
