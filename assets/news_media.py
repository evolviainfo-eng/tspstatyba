#!/usr/bin/env python3
"""Parsisiunčia kiekvieno assets/news.json įrašo peržiūros nuotrauką tiesiai iš Facebook
og:image. Nereikia nei prisijungimo, nei kliento leidimų. Paleisti prieš gen.py."""
import html as ihtml
import json
import os
import re
import subprocess

UA = "facebookexternalhit/1.1"
OUT = "assets/news_src"
os.makedirs(OUT, exist_ok=True)

posts = json.load(open("assets/news.json", encoding="utf-8"))
for i, p in enumerate(posts):
    page = subprocess.run(
        ["curl", "-s", "-L", "--max-time", "30", "-A", UA, p["url"]],
        capture_output=True, text=True).stdout
    m = re.search(r'og:image"\s+content="([^"]+)"', page)
    if not m:
        print("no og:image for", p["url"])
        continue
    url = ihtml.unescape(m.group(1))
    dst = "%s/news-%d.jpg" % (OUT, i + 1)
    subprocess.run(["curl", "-s", "-L", "--max-time", "40", "-o", dst, url])
    print(dst, os.path.getsize(dst), "bytes")
