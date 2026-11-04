#!/usr/bin/env python3
"""
Kartlegger Navs rundskriv hos Lovdata. Midlertidig utforsking: skriver lenkestrukturen på
lovdata.no/nav til loggen. Endrer ingenting i basen.
"""

import re
import sys
import time
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup

UA = {"User-Agent": "Mozilla/5.0 (regelverksbasen; tarjeiha/allover)"}
PAUSE = 1.5


def hent(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(urllib.parse.quote(url, safe=":/?=&%#"), headers=UA), timeout=60) as r:
            return r.status, r.read().decode("utf-8", errors="replace")
    except Exception as e:  # noqa: BLE001
        return getattr(e, "code", 0), ""


def vis(url, alle_lenker=False):
    status, html = hent(url)
    time.sleep(PAUSE)
    s = BeautifulSoup(html, "lxml")
    hrefs = [a["href"] for a in s.find_all("a", href=True)]
    rund = sorted(set(re.findall(r"""[^"'\s<>]*rundskriv[^"'\s<>]*""", html, re.I)))
    print(f"\n=== {url} status {status}, {len(hrefs)} lenker, {len(rund)} rundskriv-treff")
    for r in rund[:400]:
        print("RUND", r)
    if alle_lenker:
        for h in sorted(set(hrefs)):
            print("LENKE", h)
    tekst = re.sub(r"\s+", " ", s.get_text(" "))
    i = tekst.lower().find("rundskriv")
    print("TEKST", tekst[max(0, i - 300): i + 700] if i >= 0 else tekst[-800:])
    return hrefs, html


def main():
    hrefs, _ = vis("https://lovdata.no/nav", alle_lenker=True)
    kapitler = [h for h in hrefs if re.search(r"/nav/folketrygdloven/kap", h)][:2]
    for h in kapitler:
        vis(h if h.startswith("http") else "https://lovdata.no" + h, alle_lenker=True)
    for h in ["https://lovdata.no/nav/andre-rettskilder/Sosialtjenesteloven",
              "https://lovdata.no/nav/andre-rettskilder/",
              "https://lovdata.no/nav/rundskriv/r08-00",
              "https://lovdata.no/nav/rundskriv/r08-07a-for"]:
        vis(h, alle_lenker=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
