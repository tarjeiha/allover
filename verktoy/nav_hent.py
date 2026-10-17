#!/usr/bin/env python3
"""
Henter nye xlsx-filer fra Navs statistikksider og legger dem i innboks-data/.

Bruk:
    python3 verktoy/nav_hent.py [--tor]

For hver kildeside i data/nav/kilder.json:
  1. Siden leses, og alle xlsx-lenker (/_/attachment/...) plukkes ut.
  2. Filnavnet kobles til en kjent tabell med samme mønster som innboksen bruker.
     Filer uten treff lastes ikke ned, men står i rapporten.
  3. Filen lastes ned og sammenlignes (sha256) med originalene som allerede ligger i
     data/nav/<mappe>/ (også kvartalsmappene). Er den ny, legges den i innboks-data/,
     og data_innboks.py leser den inn med de samme kontrollene som ved manuell opplasting.
Med --tor lastes ingenting ned til innboks-data/; skriptet viser bare hva som ville blitt hentet.

Rapporten skrives til nav-hent-rapport.txt. Selve innlegging og feilvarsling skjer i
data_innboks.py og arbeidsflyten nav-hent.yml.
"""
import hashlib
import html
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from data_innboks import INNBOKS, NAV, finn_tabell  # noqa: E402

ROT = Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
LENKE = re.compile(r'href="([^"]*?/_/attachment/(?:download|inline)/[^"]+?)"', re.I)


def hent(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def xlsx_lenker(side):
    tekst = hent(side).decode("utf-8", "replace")
    ut = {}
    for m in LENKE.finditer(tekst):
        url = urllib.parse.urljoin("https://www.nav.no", html.unescape(m.group(1)))
        url = url.replace("/attachment/inline/", "/attachment/download/")
        navn = urllib.parse.unquote(url.rsplit("/", 1)[-1])
        if navn.lower().endswith(".xlsx"):
            ut[url] = navn
    return ut


def kjente_hasher():
    ut = set()
    for f in NAV.rglob("original/*.xlsx"):
        ut.add(hashlib.sha256(f.read_bytes()).hexdigest())
    for f in INNBOKS.glob("*.xlsx"):
        ut.add(hashlib.sha256(f.read_bytes()).hexdigest())
    return ut


def main(tor=False):
    tabeller = json.loads((NAV / "kilder.json").read_text(encoding="utf-8"))["tabeller"]
    sider = sorted({t["kildeside"] for t in tabeller if t["kildeside"].startswith("http")})
    kjente = kjente_hasher()
    nye, uendret, ukjente, feil = [], 0, [], []
    sett = set()
    for side in sider:
        try:
            lenker = xlsx_lenker(side)
        except Exception as e:  # noqa: BLE001
            feil.append(f"{side}: kunne ikke leses ({e})")
            continue
        if not lenker:
            feil.append(f"{side}: fant ingen xlsx-lenker (har Nav endret siden?)")
        for url, navn in lenker.items():
            if url in sett:
                continue
            sett.add(url)
            fil = Path(navn)
            t = finn_tabell(fil, tabeller)
            if t["kildeside"].startswith("ukjent"):
                ukjente.append(f"{navn} (på {side})")
                continue
            try:
                data = hent(url)
            except Exception as e:  # noqa: BLE001
                feil.append(f"{navn}: nedlasting feilet ({e})")
                continue
            if hashlib.sha256(data).hexdigest() in kjente:
                uendret += 1
                continue
            nye.append(navn)
            if not tor:
                INNBOKS.mkdir(exist_ok=True)
                (INNBOKS / navn).write_bytes(data)
    linjer = [f"Nav-henting: {len(nye)} ny(e) fil(er), {uendret} uendret, {len(ukjente)} uten treff i kilder.json, {len(feil)} feil", ""]
    if nye:
        linjer += ["Nye filer:"] + [f"- {n}" for n in nye] + [""]
    if ukjente:
        linjer += ["Filer på Navs sider som ikke står i kilder.json (ikke hentet):"] + [f"- {n}" for n in ukjente] + [""]
    if feil:
        linjer += ["Feil:"] + [f"- {f}" for f in feil]
    (ROT / "nav-hent-rapport.txt").write_text("\n".join(linjer) + "\n", encoding="utf-8")
    print("\n".join(linjer))
    return 1 if feil else 0


if __name__ == "__main__":
    sys.exit(main("--tor" in sys.argv))
