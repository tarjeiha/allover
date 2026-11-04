#!/usr/bin/env python3
"""
Kartlegger Navs rundskriv hos Lovdata (Nav rettskilder, lovdata.no/nav). Endrer ingenting i basen.

Leser kapittelsidene til folketrygdloven og sidene under «andre rettskilder», samler alle
lenker til /nav/rundskriv/<kode>, og henter hvert rundskriv for tittel og «sist endret».
Skriver også et utdrag av endringsloggen (/nav/endringer).
"""

import re
import sys
import time
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup

UA = {"User-Agent": "Mozilla/5.0 (regelverksbasen; tarjeiha/allover)"}
ROT = "https://lovdata.no"
PAUSE = 1.2


def hent(url):
    try:
        req = urllib.request.Request(urllib.parse.quote(url, safe=":/?=&%#"), headers=UA)
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:  # noqa: BLE001
        print(f"# feil {url}: {e}", file=sys.stderr)
        return ""
    finally:
        time.sleep(PAUSE)


def koder_i(html):
    return {m.lower() for m in re.findall(r"/nav/rundskriv/([A-Za-z0-9\-]+)", html)}


def main():
    forside = hent(ROT + "/nav")
    andre = sorted({h for h in re.findall(r'href="(/nav/andre-rettskilder/[^"#]+)"', forside)})
    sider = [f"/nav/folketrygdloven/kap{n}" for n in list(range(1, 27)) + ["11a"]] + andre
    funn = {}
    for s in sider:
        html = hent(ROT + s)
        k = koder_i(html)
        print(f"SIDE\t{s}\t{len(k)}\t{' '.join(sorted(k))}")
        for x in k:
            funn.setdefault(x, s)
    endr = hent(ROT + "/nav/endringer")
    tekst = re.sub(r"\s+", " ", BeautifulSoup(endr, "lxml").get_text(" "))
    i = tekst.find("Endringslogg")
    print("ENDRINGER", tekst[i: i + 3000])
    for x in sorted(koder_i(endr)):
        funn.setdefault(x, "/nav/endringer")
    print(f"# fant {len(funn)} rundskriv")
    print("RS\tkode\tfunnet_paa\ttittel\tdato\tsist_endret\tsammendrag")
    for k in sorted(funn):
        html = hent(f"{ROT}/nav/rundskriv/{k}")
        s = BeautifulSoup(html, "lxml")
        tittel = re.sub(r"\s*-\s*Lovdata$", "", s.title.get_text(strip=True)) if s.title else ""
        meta = {}
        for rad in s.find_all("tr"):
            th, td = rad.find("th"), rad.find("td")
            if th and td:
                meta[th.get_text(strip=True).lower()] = re.sub(r"\s+", " ", td.get_text(" ", strip=True))
        r = lambda v: (v or "").replace("\t", " ")[:200]
        print("\t".join(["RS", k, funn[k], r(tittel), r(meta.get("dato")), r(meta.get("sist endret")),
                         r(meta.get("sammendrag"))]), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
