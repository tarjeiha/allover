#!/usr/bin/env python3
"""
Kartlegger Navs rundskriv hos Lovdata: hvilke som finnes, når de sist ble endret, og hvilken lov de gjelder.

Bruk:
    python3 verktoy/rundskriv_kartlegg.py > kartlegging.tsv

Leser oversiktssidene på lovdata.no/nav/, finner alle lenker til /nav/rundskriv/<kode>, og henter
hver side med pause mellom. Skriver én linje per rundskriv: kode, tittel, dato, sist endret, sammendrag.
Endrer ingenting i basen.
"""

import re
import sys
import time
import urllib.request

from bs4 import BeautifulSoup

UA = {"User-Agent": "Mozilla/5.0 (regelverksbasen; tarjeiha/allover)"}
OVERSIKTER = [
    "https://lovdata.no/nav/rundskriv",
    "https://lovdata.no/nav/rundskriv/",
    "https://lovdata.no/nav",
    "https://lovdata.no/nav/",
    "https://lovdata.no/register/navRundskriv",
]
KODE = re.compile(r"/nav/rundskriv/([a-z0-9][a-z0-9\-]*)", re.I)
PAUSE = 1.5


def hent(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
            return r.status, r.read().decode("utf-8", errors="replace")
    except Exception as e:  # noqa: BLE001
        return getattr(e, "code", 0), ""


def lenker(html, base):
    s = BeautifulSoup(html, "lxml")
    koder, sider = {}, set()
    for a in s.find_all("a", href=True):
        h = a["href"]
        m = KODE.search(h)
        if m:
            koder.setdefault(m.group(1).lower(), a.get_text(" ", strip=True))
        elif h.startswith("/nav/") or h.startswith("/register/") or "offset=" in h or "page=" in h:
            sider.add(h if h.startswith("http") else "https://lovdata.no" + h)
    return koder, sider


def main():
    koder, besøkt, kø = {}, set(), list(OVERSIKTER)
    while kø and len(besøkt) < 60:
        url = kø.pop(0)
        if url in besøkt:
            continue
        besøkt.add(url)
        status, html = hent(url)
        time.sleep(PAUSE)
        nye, sider = lenker(html, url) if html else ({}, set())
        print(f"# oversikt {url}: status {status}, {len(nye)} rundskrivlenker, {len(sider)} andre lenker", file=sys.stderr)
        if html and not nye and url in OVERSIKTER:
            print("# utdrag: " + re.sub(r"\s+", " ", BeautifulSoup(html, "lxml").get_text(" "))[:1500], file=sys.stderr)
            print("# lenker: " + " ".join(sorted(sider))[:3000], file=sys.stderr)
        for k, t in nye.items():
            koder.setdefault(k, t)
        # Følg bare lenker som ser ut som lister over rundskriv
        for s in sorted(sider):
            if re.search(r"rundskriv|navRundskriv|offset=|page=", s, re.I) and s not in besøkt:
                kø.append(s)
    print(f"# fant {len(koder)} rundskriv", file=sys.stderr)
    print("kode\tlenketekst\ttittel\tdato\tsist_endret\tsammendrag\tstatus")
    for k in sorted(koder):
        status, html = hent(f"https://lovdata.no/nav/rundskriv/{k}")
        time.sleep(PAUSE)
        meta, tittel = {}, ""
        if html:
            s = BeautifulSoup(html, "lxml")
            tittel = re.sub(r"\s*-\s*Lovdata$", "", s.title.get_text(strip=True)) if s.title else ""
            for rad in s.find_all("tr"):
                th, td = rad.find("th"), rad.find("td")
                if th and td:
                    meta[th.get_text(strip=True).lower()] = td.get_text(" ", strip=True)
        rens = lambda x: re.sub(r"\s+", " ", x or "").replace("\t", " ")[:250]
        print("\t".join([k, rens(koder[k]), rens(tittel), rens(meta.get("dato")),
                         rens(meta.get("sist endret")), rens(meta.get("sammendrag")), str(status)]), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
