#!/usr/bin/env python3
"""
Lager ordlisten med offisielle engelske navn som oversettelsesrutinen bruker
(sprak/oversetting-navn.tsv).

Bruk:
    python3 verktoy/oversetting_navn_hent.py

Kilder:
- Nav: alle sider i sitemap.xml på nav.no som har en engelsk utgave (adresse som slutter
  på /en). Overskriften på den norske og den engelske siden blir ett par, for eksempel
  «Arbeidsavklaringspenger (AAP)» og «Work assessment allowance (AAP)».
- Lovdata: listen over oversatte lover (lovdata.no/register/loverEngelsk). Bare lovene som
  er i regelverksbasen (regelverk.json), tas med, med navnet derfra.

regjeringen.no stenger automatisk henting (Cloudflare), også fra GitHub Actions, så navn på
departementer og titler kommer ikke herfra. Skriptet bruker en åpen User-Agent og henter én
side om gangen med pause.

Skriver oversetting-navn-rapport.txt (commit-melding) når listen er endret. Feiler én kilde,
beholdes radene fra forrige kjøring for den kilden, og skriptet avslutter med feilkode.
"""

import csv
import html
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

ROT = Path(__file__).resolve().parent.parent
UT = ROT / "sprak" / "oversetting-navn.tsv"
RAPPORT = ROT / "oversetting-navn-rapport.txt"
UA = {"User-Agent": "regelverksbase/1.0 (+https://github.com/tarjeiha/allover)"}
PAUSE = 0.5
KOLONNER = ["norsk", "engelsk", "kilde", "adresse"]

# Sider på nav.no som ikke er ytelser, ordninger eller tjenester: skjemaer, lokale sider, tester.
NAV_HOPP = re.compile(r"/start/|skjemadetaljer|/lokalt/|/test/|-copy/|/samarbeidspartner/|/no/")
# Sider om selve nettstedet (innlogging, informasjonskapsler, kontakt, søk), ikke fagbegreper.
NAV_STØY = re.compile(r"/(utlogging|informasjonskapsler|soketips|skriv-til-oss|kontakt|kontaktinformasjon"
                      r"|kontonummer|personvern[^/]*|tilgjengelighet|svindel|velg-[^/]+|tilbakemeldinger"
                      r"|sporsmal|soknader|tjenester|endringer|ettersende|ettersending)/en$")


def hent(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def rens(tekst):
    tekst = html.unescape(tekst).replace("\xad", "").replace(" ", " ")
    tekst = re.sub(r"<[^>]+>", "", tekst)
    return re.sub(r"\s+", " ", tekst).strip()


def overskrift(side):
    m = re.search(r"<h1[^>]*>(.*?)</h1>", side, re.S)
    if m and rens(m.group(1)):
        return rens(m.group(1))
    m = re.search(r'<meta property="og:title" content="([^"]*)"', side)
    return rens(m.group(1)).removesuffix(" - nav.no") if m else ""


def nav():
    sitemap = hent("https://www.nav.no/sitemap.xml")
    adresser = sorted({u for u in re.findall(r"<loc>([^<]+)</loc>", sitemap)
                       if u.endswith("/en") and not NAV_HOPP.search(u + "/") and not NAV_STØY.search(u)})
    print(f"Nav: {len(adresser)} sider med engelsk utgave")
    rader = []
    for en in adresser:
        no = en[: -len("/en")]
        try:
            e = overskrift(hent(en))
            time.sleep(PAUSE)
            n = overskrift(hent(no))
            time.sleep(PAUSE)
        except Exception as feil:  # én side som feiler, skal ikke stoppe resten
            print(f"  hoppet over {en}: {feil}")
            continue
        if not e or not n or "Fant ikke siden" in n or e == n:
            print(f"  hoppet over {en}: «{n}» / «{e}»")
            continue
        rader.append({"norsk": n, "engelsk": e, "kilde": "Nav", "adresse": en})
    return rader


def lovdata():
    lover = json.loads((ROT / "regelverk.json").read_text(encoding="utf-8"))["lover"]
    navn = {l["lov"].removeprefix("LOV-"): l["navn"] for l in lover if l.get("lov")}
    treff, side_nr = [], 1
    while True:
        side = hent(f"https://lovdata.no/register/loverEngelsk?offset={(side_nr - 1) * 20}")
        nye = re.findall(r'<a[^>]+href="(/dokument/NLE/lov/(\d{4}-\d{2}-\d{2}-\d+)[^"]*)"[^>]*>(.*?)</a>', side, re.S)
        nye = [t for t in nye if t not in treff]
        if side_nr == 1:
            print("  sidelenker:", sorted(set(re.findall(r'href="([^"]*loverEngelsk[^"]*)"', side)))[:20])
        if not nye or side_nr > 50:
            break
        treff += nye
        side_nr += 1
        time.sleep(PAUSE)
    print(f"Lovdata: {len(treff)} oversatte lover i listen")
    if not treff:
        raise RuntimeError("fant ingen lover i listen hos Lovdata, oppbygningen er kanskje endret")
    rader, sett = [], set()
    for sti, lovid, tittel in treff:
        if lovid in navn and lovid not in sett:
            sett.add(lovid)
            rader.append({"norsk": navn[lovid], "engelsk": rens(tittel), "kilde": "Lovdata (ikke autoritativ oversettelse)",
                          "adresse": "https://lovdata.no" + sti})
    print(f"Lovdata: {len(rader)} av lovene i basen har engelsk oversettelse")
    return rader


def les_gamle():
    if not UT.exists():
        return []
    with UT.open(encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def main():
    gamle = les_gamle()
    rader, feilet = [], []
    for navn, fn, kilde in [("Nav", nav, "Nav"), ("Lovdata", lovdata, "Lovdata")]:
        try:
            rader += fn()
        except Exception as feil:
            print(f"{navn} feilet: {feil}")
            feilet.append(navn)
            rader += [r for r in gamle if r["kilde"].startswith(kilde)]
    unike = {}
    for r in rader:
        unike.setdefault((r["kilde"], r["norsk"], r["engelsk"]), r)
    rader = sorted(unike.values(), key=lambda r: (r["kilde"], r["norsk"].lower()))
    nye = [[r[k] for k in KOLONNER] for r in rader]
    if nye != [[r[k] for k in KOLONNER] for r in gamle]:
        with UT.open("w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter="\t", lineterminator="\n")
            w.writerow(KOLONNER)
            w.writerows(nye)
        RAPPORT.write_text(f"Ordliste for oversetting: {len(nye)} navn\n", encoding="utf-8")
        print(f"Skrev {len(nye)} navn til {UT.relative_to(ROT)}")
    else:
        print("Ingen endringer i ordlisten")
    if feilet:
        sys.exit(1)


if __name__ == "__main__":
    main()
