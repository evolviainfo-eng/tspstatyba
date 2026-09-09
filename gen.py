#!/usr/bin/env python3
"""Generuoja paslaugų puslapius į paslaugos/<slug>/index.html."""
import os

TEL = "+370 639 94290"
TELR = "+37063994290"

SERVICES = [
    {
        "slug": "vidaus-apdaila",
        "name": "Vidaus apdaila",
        "title": "Vidaus apdaila Šiauliuose · TSP Statyba",
        "desc": "Glaistymas, dažymas, plytelių klijavimas, grindų ir lubų įrengimas iki rakto. "
                "MB „TSP Statyba“, Šiauliai ir regionas.",
        "hero": ("w3-a", "1600", [("w3-a-900.webp", "900w"), ("w3-a-1600.webp", "1600w")],
                 "Svetainė su medinių lentelių siena, sofa ir dideliu langu po vidaus apdailos darbų"),
        "lead": [
            "Įrengiame patalpas nuo pilkų sienų iki paruošto gyventi namo. Dirbame ir atskirais "
            "etapais, ir visą vidų iš vienų rankų, tad jums nereikia derinti kelių brigadų tarpusavyje.",
            "Prieš pradedant apžiūrime objektą vietoje, apmatuojame ir pateikiame sąmatą su darbais "
            "ir medžiagomis. Baigę patys apsižiūrime ir sutvarkome trūkumus."
        ],
        "list": [
            "Sienų ir lubų glaistymas",
            "Dažymas ir dekoratyvinės sienų dangos",
            "Plytelių klijavimas, vonios ir sanitariniai mazgai",
            "Grindų dangų klojimas",
            "Pakabinamos lubos ir apšvietimo paruošimas",
            "Medinių lentelių ir kita dekoratyvinė apdaila",
        ],
        "ar": "45",
        "gal": [
            ("w2-a-900.webp", "Svetainė su medinių lentelių siena ir koridorius po vidaus apdailos darbų"),
            ("w2-b-900.webp", "Vonios kambarys su marmuro imitacijos plytelėmis ir laisvai stovinčia vonia"),
            ("w2-c-900.webp", "Lubos su linijiniais šviestuvais ir akmens plokštės sienos apdaila"),
        ],
    },
    {
        "slug": "fasadai-ir-klinkeris",
        "name": "Fasadai ir klinkeris",
        "title": "Fasadai ir klinkerio klijavimas Šiauliuose · TSP Statyba",
        "desc": "Klinkerio ir betono plytelių fasadai, siūlių formavimas, cokolio ir angokraščių apdaila. "
                "MB „TSP Statyba“, Šiauliai ir regionas.",
        "hero": ("w1-a", "1800", [("w1-a-900.webp", "900w"), ("w1-a-1600.webp", "1600w"), ("w1-a-1800.webp", "1800w")],
                 "Dviaukštis tamsaus klinkerio namas vakare su apšviesta terasa"),
        "lead": [
            "Klijuojame klinkerio ir betono plyteles, formuojame siūles ir darome fasado apdailos "
            "darbus. Fasadas yra tas darbas, kuriame matosi kiekvienas milimetras, todėl kampus, "
            "angokraščius ir siūlių plotį deriname vietoje pagal objektą.",
            "Dirbame su šviesiu ir tamsiu klinkeriu, betono plytelėmis ir medžio apdailos akcentais. "
            "Objektą perduodame užbaigtą, be paliktų nesutvarkytų detalių."
        ],
        "list": [
            "Klinkerio plytelių klijavimas",
            "Betono plytelių fasadai",
            "Siūlių formavimas ir valymas",
            "Cokolio apdaila",
            "Kampų, angokraščių ir detalių apdaila",
            "Medžio apdailos akcentai",
        ],
        "ar": "32",
        "gal": [
            ("w5-1400.webp", "Vienaukštis namas su mūro ir tinko fasadu ir trinkelių taku"),
            ("w4-1600.webp", "Vienaukštis namas su klinkerio cokoliu ir tinkuotu fasadu"),
            ("o3-1600.webp", "Tamsaus klinkerio namas su medžio apdailos akcentu ir terasa"),
        ],
    },
    {
        "slug": "siltinimas",
        "name": "Šiltinimas",
        "title": "Fasadų šiltinimas ir dekoratyvinis tinkavimas Šiauliuose · TSP Statyba",
        "desc": "Fasadų šiltinimas, armavimas ir dekoratyvinis tinkavimas. "
                "MB „TSP Statyba“, Šiauliai ir regionas.",
        "hero": ("w5", "1400", [("w5-900.webp", "900w"), ("w5-1400.webp", "1400w"), ("w5-2048.webp", "2048w")],
                 "Apšiltintas ir užbaigtas vienaukščio namo fasadas su mūro ir tinko apdaila"),
        "lead": [
            "Šiltiname fasadus ir tuo pačiu darbu užbaigiame juos dekoratyviniu tinku, tad objekto "
            "nereikia palikti su plikomis plokštėmis ir laukti kitos brigados.",
            "Faktūrą ir atspalvį pasirenkate patys, mes parodome pavyzdžius ant objekto. Šiltinimą "
            "deriname su cokolio ir angokraščių apdaila, kad fasadas atrodytų kaip vienas darbas."
        ],
        "list": [
            "Fasado šiltinimas polistirenu arba akmens vata",
            "Armavimas ir tinklelio klijavimas",
            "Gruntavimas",
            "Dekoratyvinis tinkas, faktūros pasirinkimas",
            "Cokolio šiltinimas ir apdaila",
            "Angokraščių apdaila",
        ],
        "ar": "45",
        "gal": [
            ("sv-siltinimas-1400.webp", "Dekoratyvinio tinko faktūra iš arti ant apšiltinto fasado"),
            ("w1-b-1000.webp", "Šviesaus mūro fasadas su tamsia plytelių apdaila"),
            ("intro-1400.webp", "Tinkuotas fasadas su tamsaus klinkerio cokoliu ir medžio apdaila"),
        ],
    },
    {
        "slug": "renovacija-ir-statyba",
        "name": "Renovacija ir statyba",
        "title": "Renovacija ir bendrieji statybos darbai Šiauliuose · TSP Statyba",
        "desc": "Patalpų atnaujinimas, mūro ir stogo konstrukcijų darbai, objekto vedimas etapais. "
                "MB „TSP Statyba“, Šiauliai ir regionas.",
        "hero": ("sv-renovacija-1400", None, [("sv-renovacija-1000.webp", "1000w"), ("sv-renovacija-1400.webp", "1400w")],
                 "Mūro darbai statomame name: blokelių sienos ir angos"),
        "lead": [
            "Atnaujiname patalpas ir dirbame bendruosius statybos darbus. Imamės ir atskiro etapo, "
            "ir viso objekto: nuo mūro bei stogo konstrukcijų iki užbaigtos vidaus apdailos.",
            "Dirbame sutartu grafiku ir eigą deriname su jumis. Objektą perduodame užbaigtą ir "
            "liekame pasiekiami klausimams."
        ],
        "list": [
            "Mūro darbai",
            "Pertvarų įrengimas ir griovimas",
            "Stogo konstrukcijų montavimas",
            "Senų patalpų atnaujinimas",
            "Darbų organizavimas etapais",
            "Užbaigto objekto perdavimas",
        ],
        "ar": "45",
        "gal": [
            ("proc-1400.webp", "Medinės stogo konstrukcijos montavimas ant mūrinių sienų"),
            ("w3-b-1000.webp", "Erdvi patalpa su mediniais laiptais ir naujomis grindimis"),
            ("w2-c-900.webp", "Lubos su linijiniais šviestuvais ir akmens plokštės sienos apdaila"),
        ],
    },
]

NAV = '''<header class="nav" id="nav">
  <div class="nav__in wrap">
    <a class="nav__logo" href="/" aria-label="TSP Statyba, į puslapio pradžią">
      <img src="/img/logo-nav-dark.png" alt="TSP Statyba" width="148" height="102">
    </a>
    <button class="nav__burger" id="burger" type="button" aria-expanded="false" aria-controls="navlinks" aria-label="Atidaryti meniu"><span></span></button>
    <nav class="nav__links" id="navlinks" aria-label="Pagrindinis meniu">
      <a href="/#darbai" class="nav__d">Darbai</a>
      <a href="/#paslaugos" class="nav__d is-active">Paslaugos</a>
      <a href="/#procesas" class="nav__d">Kaip dirbame</a>
      <a href="/#naujienos" class="nav__d">Naujienos</a>
      <a href="/#kontaktai" class="nav__d">Kontaktai</a>
      <a href="tel:{telr}" class="nav__tel tnum">{tel}</a>
      <a href="/#kontaktai" class="nav__cta btn btn--sm">Gauti pasiūlymą</a>
    </nav>
  </div>
</header>'''.replace('{telr}', TELR).replace('{tel}', TEL)

FOOT = '''<footer class="foot">
  <div class="wrap foot__in">
    <img class="foot__logo" src="/img/logo-full-light.png" alt="TSP Statyba, Tavo statybų partneris" width="220" height="168" loading="lazy" decoding="async">
    <div class="foot__cols">
      <p class="foot__txt">
        MB „TSP Statyba“ · Įm. k. 306822009 · PVM kodas LT100017734711<br>
        Šatrijos g. 20-1, LT-76230 Šiauliai ·
        <a class="tnum" href="tel:{telr}">{tel}</a> ·
        <a href="mailto:tavostatybupartneris@gmail.com">tavostatybupartneris@gmail.com</a>
      </p>
      <p class="foot__b">
        <a href="https://www.facebook.com/TSPstatyba" target="_blank" rel="noopener">Facebook</a>
        <a href="https://www.instagram.com/tavo_statybu_partneris/" target="_blank" rel="noopener">Instagram</a>
        <span>© 2026</span>
      </p>
    </div>
  </div>
</footer>

<div class="callbar" id="callbar">
  <a href="tel:{telr}">Skambinti</a>
  <a href="/#kontaktai">Gauti pasiūlymą</a>
</div>'''.replace('{telr}', TELR).replace('{tel}', TEL)


def srcset(items):
    return ", ".join("/img/%s %s" % (f, w) for f, w in items)


def gallery(gal, ar):
    out = []
    for i, (fn, alt) in enumerate(gal):
        out.append(
            '        <div class="ph ar%s" data-reveal%s>\n'
            '          <img src="/img/%s" sizes="(min-width:760px) 31vw, 100vw" '
            'loading="lazy" decoding="async" alt="%s">\n'
            '        </div>' % (ar, ' data-delay="%d"' % (i * 70) if i else '', fn, alt))
    return "\n".join(out)


def others(slug):
    cards = []
    for s in SERVICES:
        if s["slug"] == slug:
            continue
        cards.append(
            '        <a href="/paslaugos/%s/" data-reveal>\n'
            '          <h3>%s</h3>\n'
            '          <p>%s</p>\n'
            '        </a>' % (s["slug"], s["name"], s["list"][0] + ", " + s["list"][1].lower() + "."))
    return "\n".join(cards)


PAGE = '''<!doctype html>
<html lang="lt">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#ffffff">
<link rel="canonical" href="https://tspstatyba.lt/paslaugos/{slug}/">
<link rel="icon" href="/img/favicon.png" sizes="48x48">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">

<meta property="og:type" content="website">
<meta property="og:locale" content="lt_LT">
<meta property="og:site_name" content="TSP Statyba">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://tspstatyba.lt/paslaugos/{slug}/">
<meta property="og:image" content="https://tspstatyba.lt/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="preload" as="image" href="/img/{heroimg}" imagesrcset="{herosrcset}" imagesizes="100vw" fetchpriority="high">
<link rel="stylesheet" href="/css/main.css?v=20260909">

<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Service","name":"{name}",
"serviceType":"{name}","areaServed":"Šiauliai",
"provider":{{"@type":"HomeAndConstructionBusiness","name":"MB „TSP Statyba“",
"url":"https://tspstatyba.lt/","telephone":"{telr}",
"address":{{"@type":"PostalAddress","streetAddress":"Šatrijos g. 20-1","addressLocality":"Šiauliai","postalCode":"LT-76230","addressCountry":"LT"}}}},
"url":"https://tspstatyba.lt/paslaugos/{slug}/"}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
{{"@type":"ListItem","position":1,"name":"Pradžia","item":"https://tspstatyba.lt/"}},
{{"@type":"ListItem","position":2,"name":"Paslaugos","item":"https://tspstatyba.lt/#paslaugos"}},
{{"@type":"ListItem","position":3,"name":"{name}","item":"https://tspstatyba.lt/paslaugos/{slug}/"}}]}}
</script>
</head>
<body>
<a class="skip" href="#main">Pereiti prie turinio</a>

{nav}

<main id="main">

  <section class="phero">
    <div class="phero__media">
      <img src="/img/{heroimg}" srcset="{herosrcset}" sizes="100vw" fetchpriority="high" decoding="async" alt="{heroalt}">
    </div>
    <div class="phero__scrim" aria-hidden="true"></div>
    <div class="phero__in">
      <p class="crumb"><a href="/">Pradžia</a> · <a href="/#paslaugos">Paslaugos</a></p>
      <h1>{name}</h1>
    </div>
  </section>

  <section class="sect">
    <div class="wrap lead__grid">
      <div>
        <p class="lede" data-reveal>{lead1}</p>
        <p class="lede" data-reveal data-delay="70">{lead2}</p>
        <div class="lead__cta" data-reveal data-delay="130">
          <a class="btn" href="/#kontaktai">Gauti pasiūlymą</a>
          <a class="tel tnum" href="tel:{telr}">{tel}</a>
        </div>
      </div>
      <div class="lead__side">
        <h2 data-reveal>Ką apima</h2>
        <ul class="wlist">
{items}
        </ul>
      </div>
    </div>
  </section>

  <section class="sect alt">
    <div class="wrap">
      <div class="sect__head">
        <h2 data-reveal>Darbų pavyzdžiai</h2>
        <div class="rule" data-reveal data-delay="60"></div>
      </div>
      <div class="gal">
{gallery}
      </div>
    </div>
  </section>

  <section class="sect">
    <div class="wrap">
      <div class="sect__head">
        <h2 data-reveal>Kitos paslaugos</h2>
        <div class="rule" data-reveal data-delay="60"></div>
      </div>
      <div class="more">
{others}
      </div>
    </div>
  </section>

  <section class="band">
    <div class="wrap band__in">
      <div>
        <h2 data-reveal>Aptarkime jūsų objektą</h2>
        <p data-reveal data-delay="70">Atsiųskite nuotrauką ar aprašymą, atvyksime apžiūrėti ir pateiksime sąmatą.</p>
        <a class="tel tnum" href="tel:{telr}" data-reveal data-delay="110">{tel}</a>
      </div>
      <a class="btn" href="/#kontaktai" data-reveal data-delay="140">Užpildyti užklausą</a>
    </div>
  </section>
</main>

{foot}

<div id="fb-root"></div>
<script src="/js/lenis.min.js?v=20260909" defer></script>\n<script src="/js/main.js?v=20260909" defer></script>
</body>
</html>
'''


FB_SVG = ('<svg width="15" height="15" viewBox="0 0 24 24" aria-hidden="true">'
          '<path d="M24 12.07C24 5.4 18.63 0 12 0S0 5.4 0 12.07C0 18.1 4.39 23.1 10.13 24v-8.44H7.08'
          'v-3.49h3.05V9.41c0-3.02 1.79-4.69 4.53-4.69 1.31 0 2.68.24 2.68.24v2.96h-1.51c-1.49 0-1.96.93'
          '-1.96 1.89v2.26h3.33l-.53 3.49h-2.8V24C19.61 23.1 24 18.1 24 12.07z"/></svg>')


def _plural(n, one, few, many):
    if n % 10 == 1 and n % 100 != 11:
        return "%d %s" % (n, one)
    if 2 <= n % 10 <= 9 and not 11 <= n % 100 <= 19:
        return "%d %s" % (n, few)
    return "%d %s" % (n, many)


def _views(n):
    if n >= 1000:
        return "%d tūkst. peržiūrų" % round(n / 1000.0)
    return _plural(n, "peržiūra", "peržiūros", "peržiūrų")


RX_LIKE = ('<span class="rx rx--like"><svg width="10" height="10" viewBox="0 0 24 24">'
           '<path d="M2 21h4V9H2v12zm20-11a2 2 0 0 0-2-2h-6.3l.95-4.57.03-.32a1.5 1.5 0 0 0-.44-1.06'
           'L13.17 1 6.6 7.59A2 2 0 0 0 6 9v10a2 2 0 0 0 2 2h9a2 2 0 0 0 1.84-1.22l3.02-7.05'
           'c.09-.23.14-.47.14-.73v-2z"/></svg></span>')
RX_LOVE = ('<span class="rx rx--love"><svg width="10" height="10" viewBox="0 0 24 24">'
           '<path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3'
           'c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5'
           'c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg></span>')


def build_news():
    """Įrašo naujausius Facebook įrašus iš assets/news.json į index.html.
    Atnaujinimas: apify/facebook-posts-scraper -> assets/news.json -> python3 gen.py"""
    import json
    with open("assets/news.json", encoding="utf-8") as f:
        posts = json.load(f)
    cards = []
    for i, p in enumerate(posts):
        total = p["like"] + p["love"]
        rx = RX_LIKE + (RX_LOVE if p["love"] else "")
        right = []
        if p.get("views"):
            right.append(_views(p["views"]))
        if p.get("comments"):
            right.append(_plural(p["comments"], "komentaras", "komentarai", "komentarų"))
        if p.get("shares"):
            right.append(_plural(p["shares"], "bendrinimas", "bendrinimai", "bendrinimų"))

        widths = [w for w in (700, 1000, 1400)
                  if os.path.exists("img/%s-%d.webp" % (p["img"], w))]
        srcset = ", ".join("img/%s-%d.webp %dw" % (p["img"], w, w) for w in widths)

        if p.get("video"):
            media = ('          <div class="post__media post__media--video is-paused" data-video>\n'
                     '            <video src="video/%s.mp4" poster="img/%s-700.webp" muted loop '
                     'playsinline preload="none" width="720" height="480" aria-label="%s"></video>\n'
                     '            <span class="post__play" aria-hidden="true">'
                     '<svg width="20" height="20" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span>\n'
                     '            <a class="post__cover" href="%s" target="_blank" rel="noopener">'
                     '<span class="vh">Žiūrėti šį įrašą Facebook</span></a>\n'
                     '          </div>\n' % (p["video"], p["img"], p["alt"], p["url"]))
        else:
            media = ('          <a class="post__media" href="%s" target="_blank" rel="noopener" '
                     'tabindex="-1" aria-hidden="true">\n'
                     '            <img src="img/%s-%d.webp" srcset="%s" '
                     'sizes="(min-width:960px) 36vw, 100vw" width="1000" height="667" '
                     'loading="lazy" decoding="async" alt="%s">\n'
                     '          </a>\n' % (p["url"], p["img"], widths[-1], srcset, p["alt"]))

        cards.append(
            '        <article class="post" data-reveal%s>\n'
            '          <header class="post__head">\n'
            '            <img class="post__avatar" src="img/fb-avatar.webp" width="48" height="48" alt="" loading="lazy" decoding="async">\n'
            '            <span>\n'
            '              <b class="post__name">TSP Statyba</b>\n'
            '              <span class="post__meta"><time datetime="%s">%s</time></span>\n'
            '            </span>\n'
            '          </header>\n'
            '          <p class="post__text">%s</p>\n'
            '%s'
            '          <p class="post__stats">\n'
            '            <span class="post__rx">%s<span class="tnum">%d</span></span>\n'
            '            <span class="tnum">%s</span>\n'
            '          </p>\n'
            '          <p class="post__actions">\n'
            '            <a href="%s" target="_blank" rel="noopener">%s Žiūrėti Facebook</a>\n'
            '          </p>\n'
            '        </article>' % (
                ' data-delay="%d"' % (i * 70) if i else '',
                p["date"], p["label"], p["text"], media,
                rx, total, " · ".join(right),
                p["url"], FB_SVG))
    block = "<!-- NEWS:START -->\n" + "\n".join(cards) + "\n<!-- NEWS:END -->"
    with open("index.html", encoding="utf-8") as f:
        html = f.read()
    x = html.index("<!-- NEWS:START -->")
    y = html.index("<!-- NEWS:END -->") + len("<!-- NEWS:END -->")
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html[:x] + block + html[y:])
    print("wrote", len(posts), "news cards into index.html")


def build():
    for s in SERVICES:
        base, big, ss_items, alt = s["hero"]
        heroimg = "%s-%s.webp" % (base, big) if big else "%s.webp" % base
        items = "\n".join(
            '          <li><span>%02d</span>%s</li>' % (i + 1, t)
            for i, t in enumerate(s["list"]))
        html = PAGE.format(
            title=s["title"], desc=s["desc"], slug=s["slug"], name=s["name"],
            nav=NAV, foot=FOOT, tel=TEL, telr=TELR,
            heroimg=heroimg, herosrcset=srcset(ss_items), heroalt=alt,
            lead1=s["lead"][0], lead2=s["lead"][1],
            items=items, gallery=gallery(s["gal"], s["ar"]), others=others(s["slug"]))
        d = os.path.join("paslaugos", s["slug"])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote", os.path.join(d, "index.html"))

    urls = ["https://tspstatyba.lt/"] + \
           ["https://tspstatyba.lt/paslaugos/%s/" % s["slug"] for s in SERVICES]
    body = "\n".join(
        '  <url>\n    <loc>%s</loc>\n    <lastmod>2026-09-09</lastmod>\n'
        '    <changefreq>monthly</changefreq>\n    <priority>%s</priority>\n  </url>'
        % (u, "1.0" if i == 0 else "0.8") for i, u in enumerate(urls))
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                + body + "\n</urlset>\n")
    print("wrote sitemap.xml with", len(urls), "urls")


if __name__ == "__main__":
    build()
    build_news()
