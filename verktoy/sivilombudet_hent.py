#!/usr/bin/env python3
"""
Holder Sivilombudets uttalelser om lovene i basen oppdatert fra sivilombudet.no.

Bruk:
    python3 verktoy/sivilombudet_hent.py           # hent nye og endrede uttalelser
    python3 verktoy/sivilombudet_hent.py --tving   # hent alle på nytt
    python3 verktoy/sivilombudet_hent.py --maks 300  # stans etter 300 hentinger, resten tas neste gang

1. Leser uttalelsene i sitemap på sivilombudet.no (uttalelser-sitemap*.xml), med dato for
   siste endring (lastmod).
2. Henter uttalelser som er nye eller har ny dato siden forrige gang (regelverk/sivilombudet.tsv).
   Uttalelser fra før FRA_ÅR tas ikke med.
3. Uttalelsen kobles til lovene i basen som nevnes med paragraf («forvaltningsloven § 25»).
   Den legges under loven som nevnes oftest, i regelverk/<lov>/rundskriv/sivilombudet/<navn>.md,
   og de andre lovene står i `lover:` øverst i filen. Uttalelser uten lov fra basen hoppes over.

4. Skriver regelverk/<lov>/rundskriv/sivilombudet/oversikt.md med alle uttalelsene under loven:
   dato, saksnummer, tittel og hvilke paragrafer i loven som nevnes. Veiviseren viser dit.

Skriver sivilombudet-rapport.txt (commit-melding og sammendrag) når noe er endret.
Sivilombudet tillater automatisk henting (robots.txt). Skriptet henter én side om gangen med pause.
"""

import argparse
import datetime
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).parent))
import nettsider_hent as nett  # noqa: E402

ROT = Path(__file__).resolve().parent.parent
BASE = "https://www.sivilombudet.no"
STATUS = ROT / "regelverk" / "sivilombudet.tsv"
RAPPORT = ROT / "sivilombudet-rapport.txt"
FRA_ÅR = 2010
KOLONNER = ["side", "lastmod", "dato", "saksnummer", "fil", "lover", "sjekksum", "lagt_inn"]
# Andre navn lovene omtales med, i tillegg til navnet i regelverk.json.
ALIAS = {
    "regelverk/spk-loven": ["pensjonskasseloven", "lov om statens pensjonskasse"],
    "regelverk/nav-loven": ["nav-loven", "arbeids- og velferdsforvaltningsloven"],
    "regelverk/likestillings-og-diskrimineringsloven": ["likestillings- og diskrimineringsloven"],
    "regelverk/universitets-og-hoyskoleloven": ["universitets- og høyskoleloven", "uhl."],
    "regelverk/folketrygdloven": ["folketrygdloven", "ftrl."],
    "regelverk/forvaltningsloven": ["forvaltningsloven", "fvl."],
    "regelverk/offentleglova": ["offentleglova", "offl."],
    "regelverk/opplaeringslova": ["opplæringslova", "opplæringsloven"],
    "regelverk/utlendingsloven": ["utlendingsloven", "utl."],
    "regelverk/statsansatteloven": ["statsansatteloven"],
    "regelverk/arbeidsmiljoloven": ["arbeidsmiljøloven", "aml."],
}


def lovmønstre() -> dict:
    """Lovmappe -> (lov fra regelverk.json, regex som finner «<navn> §»)."""
    cfg = json.loads((ROT / "regelverk.json").read_text(encoding="utf-8"))
    ut = {}
    for lov in cfg["lover"]:
        if "ikke i kraft" in lov["navn"].lower():
            continue
        navn = [re.split(r"\s*\(", lov["navn"])[0].lower()] + ALIAS.get(lov["mappe"], [])
        navn = sorted({n.rstrip(".") for n in navn if len(n) > 3}, key=len, reverse=True)
        alt = "|".join(re.escape(n) + r"s?\.?" for n in navn)
        ut[lov["mappe"]] = (lov, re.compile(rf"(?<![\w-])(?:{alt})\s+(?:§|kapittel|kap\.)", re.I))
    return ut


def les_status() -> dict:
    if not STATUS.exists():
        return {}
    linjer = STATUS.read_text(encoding="utf-8").splitlines()
    return {r["side"]: r for r in (dict(zip(KOLONNER, l.split("\t"))) for l in linjer[1:] if l)}


def skriv_status(status: dict) -> None:
    linjer = ["\t".join(KOLONNER)] + ["\t".join(status[s].get(k, "") for k in KOLONNER) for s in sorted(status)]
    STATUS.write_text("\n".join(linjer) + "\n", encoding="utf-8")


def uttalelser() -> dict:
    """Side (slug) -> lastmod, for uttalelsene på norsk."""
    ut = {}
    for url, mod in nett.sitemap(BASE + "/uttalelser-sitemap.xml") + \
            nett.sitemap(BASE + "/uttalelser-sitemap2.xml"):
        m = re.fullmatch(re.escape(BASE) + r"/uttalelser/([^/]+)/?", url)
        if m:
            ut[m.group(1)] = mod
    if len(ut) < 500:
        raise RuntimeError(f"fant bare {len(ut)} uttalelser i sitemap – har nettstedet endret oppbygning?")
    return ut


def les_uttalelse(side: str) -> dict | None:
    try:
        html = nett.hent(f"{BASE}/uttalelser/{side}/")
    except urllib.error.HTTPError as e:
        if e.code in (404, 410):
            return None
        raise
    soup = BeautifulSoup(html, "lxml")
    artikkel = soup.select_one("article") or soup.select_one("main")
    h1 = soup.find("h1")
    meta = artikkel.select_one("div.post-meta")
    m = re.search(r"(\d{1,2}\.\d{1,2}\.\d{4})\s*\(([^)]+)\)", meta.get_text(" ", strip=True) if meta else "")
    dato, saksnr = (m.group(1), m.group(2)) if m else ("", "")
    kropp = artikkel.select_one("div.article-body") or artikkel
    for t in kropp.select("section.table-of-contents, .toc, nav, button, form, script, style"):
        t.decompose()
    nett.BASE = BASE
    return {"tittel": re.sub(r"\s+", " ", h1.get_text(" ", strip=True)) if h1 else side,
            "dato": dato, "saksnummer": saksnr, "tekst": nett.markdown(kropp)}


def paragrafmønstre() -> dict:
    """Lovmappe -> regex som fanger paragrafnummeret i «<navn> § 25» og «<navn> §§ 24 og 25»."""
    ut = {}
    for mappe, (lov, _) in lovmønstre().items():
        navn = [re.split(r"\s*\(", lov["navn"])[0].lower()] + ALIAS.get(mappe, [])
        navn = sorted({n.rstrip(".") for n in navn if len(n) > 3}, key=len, reverse=True)
        alt = "|".join(re.escape(n) + r"s?\.?" for n in navn)
        nr = r"\d+(?:\s?-\s?\d+)?(?:[a-z]|\s[a-h])?(?![\w-])"
        ut[mappe] = re.compile(rf"(?<![\w-])(?:{alt})\s+§§?\s*({nr}(?:\s*(?:,|og|og/eller|jf\.)\s*{nr})*)", re.I)
    return ut


def paragrafnøkkel(nr: str) -> tuple:
    deler = re.findall(r"\d+|[a-z]", nr)
    return tuple((0, int(d)) if d.isdigit() else (1, d) for d in deler)


def les_hode(tekst: str) -> dict:
    hode = {}
    if tekst.startswith("---"):
        for linje in tekst.split("---", 2)[1].splitlines():
            if ":" in linje:
                k, v = linje.split(":", 1)
                hode[k.strip()] = v.strip().strip('"')
    m = re.search(r"^# (.+)$", tekst, re.M)
    hode["tittel"] = m.group(1).strip() if m else ""
    return hode


def skriv_oversikter() -> int:
    """Skriver oversikt.md i hver mappe med uttalelser. Returnerer antall mapper."""
    mønstre = paragrafmønstre()
    mapper = sorted({f.parent for f in (ROT / "regelverk").glob("*/rundskriv/sivilombudet/*.md")})
    for mappe in mapper:
        lovmappe = mappe.parent.parent.relative_to(ROT).as_posix()
        mønster = mønstre.get(lovmappe)
        rader = []
        for f in sorted(mappe.glob("*.md")):
            if f.name == "oversikt.md":
                continue
            tekst = f.read_text(encoding="utf-8")
            h = les_hode(tekst)
            paragrafer = set()
            for m in mønster.finditer(tekst) if mønster else []:
                for nr in re.findall(r"\d+(?:\s?-\s?\d+)?(?:[a-z]|\s[a-h])?(?![\w-])", m.group(1)):
                    paragrafer.add(re.sub(r"\s", "", nr))
            par = ", ".join(f"§ {p}" for p in sorted(paragrafer, key=paragrafnøkkel))
            rader.append((h.get("dato", ""), h.get("saksnummer", ""), h["tittel"].replace("|", "/"),
                          par, h.get("lover", "").replace(";", ","), f.name))
        rader.sort(key=lambda r: r[0], reverse=True)
        lov = rader and les_hode((mappe / rader[0][5]).read_text(encoding="utf-8")).get("lov", "") or lovmappe
        linjer = [
            f"# Sivilombudets uttalelser om {lov[0].lower() + lov[1:] if ' ' not in lov and lov[1:2].islower() else lov}",
            "",
            f"{len(rader)} uttalelser fra {FRA_ÅR} og senere der loven nevnes med paragraf, nyeste først. "
            "Kolonnen «Paragrafer» viser paragrafene i loven som nevnes i uttalelsen. Uttalelser som nevner "
            "denne loven oftere enn andre lover i basen, ligger her. Andre lover som nevnes, står i kolonnen "
            "«Også». Uttalelsene er ikke bindende, men tillegges stor vekt i forvaltningen.",
            "",
            "Søk i tabellen etter paragraf eller stikkord i tittelen, og åpne filen før du bruker uttalelsen.",
            "",
            "| Dato | Sak | Tittel | Paragrafer | Også | Fil |",
            "|---|---|---|---|---|---|",
        ] + [f"| {d} | {s} | {t} | {p} | {o} | `{fil}` |" for d, s, t, p, o, fil in rader]
        (mappe / "oversikt.md").write_text("\n".join(linjer) + "\n", encoding="utf-8")
    return len(mapper)


def iso(dato: str) -> str:
    d, m, å = dato.split(".")
    return f"{å}-{int(m):02d}-{int(d):02d}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tving", action="store_true", help="hent alle på nytt")
    ap.add_argument("--maks", type=int, default=0, help="stans etter så mange hentinger (0 = ingen grense)")
    ap.add_argument("--bare-oversikt", action="store_true", help="skriv bare oversikt.md, uten å hente")
    args = ap.parse_args()
    if args.bare_oversikt:
        print(f"Skrev oversikt for {skriv_oversikter()} lover")
        return 0

    idag = datetime.date.today().isoformat()
    lover = lovmønstre()
    sider = uttalelser()
    status = les_status()
    nye, endret, borte, hentet = [], [], [], 0

    for side, lastmod in sorted(sider.items(), key=lambda x: x[1], reverse=True):
        rå, lastmod = lastmod, f"{lastmod}|v{nett.FORMAT}"
        gammel = status.get(side)
        if gammel and not gammel.get("fil") and gammel.get("lastmod", "").split("|")[0] == rå and not args.tving:
            # Uttalelser som ble hoppet over (for gamle eller uten lov fra basen) hentes ikke på nytt
            # bare fordi formatet er endret.
            gammel["lastmod"] = lastmod
            continue
        if gammel and gammel.get("lastmod") == lastmod and not args.tving:
            continue
        if args.maks and hentet >= args.maks:
            break
        hentet += 1
        u = les_uttalelse(side)
        rad = {"side": side, "lastmod": lastmod}
        if u is None or not u["dato"] or int(u["dato"][-4:]) < FRA_ÅR:
            status[side] = {**rad, "dato": u["dato"] if u else ""}
            continue
        treff = Counter({m: len(p.findall(u["tekst"])) for m, (_, p) in lover.items()})
        treff = Counter({m: n for m, n in treff.items() if n})
        gammel_fil = ROT / gammel["fil"] if gammel and gammel.get("fil") else None
        if not treff:
            if gammel_fil and gammel_fil.exists():
                gammel_fil.unlink()
            status[side] = {**rad, "dato": u["dato"], "saksnummer": u["saksnummer"]}
            continue
        hoved = treff.most_common(1)[0][0]
        lov = lover[hoved][0]
        andre = [lover[m][0]["navn"] for m, _ in treff.most_common()[1:]]
        sjekksum = hashlib.sha256(json.dumps(u, ensure_ascii=False).encode()).hexdigest()[:16]
        fil = f"{hoved}/rundskriv/sivilombudet/{side[:120]}.md"
        if gammel and gammel.get("sjekksum") == sjekksum and gammel.get("fil") == fil and (ROT / fil).exists() \
                and not args.tving:
            status[side] = {**gammel, **rad}
            continue
        if gammel_fil and gammel_fil.exists() and gammel["fil"] != fil:
            gammel_fil.unlink()
        hode = "\n".join([
            "---",
            f'rundskriv: "Sivilombudets uttalelse {u["dato"]} ({u["saksnummer"]})"',
            'utgiver: "Sivilombudet"',
            f'lov: "{lov["navn"]}"',
            *([f'lover: "{"; ".join(andre)}"'] if andre else []),
            f'dato: "{iso(u["dato"])}"',
            f'saksnummer: "{u["saksnummer"]}"',
            f'kilde: "{BASE}/uttalelser/{side}/"',
            f'lagt_inn: "{idag}"',
            "---",
        ])
        (ROT / fil).parent.mkdir(parents=True, exist_ok=True)
        (ROT / fil).write_text(f"{hode}\n\n# {u['tittel']}\n\nSivilombudets uttalelse {u['dato']} "
                               f"(sak {u['saksnummer']}).\n\n{u['tekst']}\n", encoding="utf-8")
        status[side] = {**rad, "dato": u["dato"], "saksnummer": u["saksnummer"], "fil": fil,
                        "lover": "; ".join([hoved.removeprefix("regelverk/")] +
                                           [m.removeprefix("regelverk/") for m, _ in treff.most_common()[1:]]),
                        "sjekksum": sjekksum, "lagt_inn": idag}
        (endret if gammel and gammel.get("fil") else nye).append(f"{u['tittel']} ({u['dato']}, {lov['navn']})")

    for side in [s for s in status if s not in sider]:
        rad = status.pop(side)
        if rad.get("fil") and (ROT / rad["fil"]).exists():
            (ROT / rad["fil"]).unlink()
            borte.append(rad["fil"])

    skriv_status(status)
    skriv_oversikter()
    gjenstår = sum(1 for s, l in sider.items() if status.get(s, {}).get("lastmod") != f"{l}|v{nett.FORMAT}")
    print(f"Hentet {hentet}. Nye: {len(nye)}, endret: {len(endret)}, borte: {len(borte)}, gjenstår: {gjenstår}")
    if nye or endret or borte:
        melding = [f"Sivilombudets uttalelser: {len(nye)} nye, {len(endret)} endret, {len(borte)} borte", ""]
        vis = lambda liste, ord_: [f"- {ord_}: {l}" for l in liste[:40]] + (
            [f"- … og {len(liste) - 40} til"] if len(liste) > 40 else [])
        melding += vis(nye, "Ny") + vis(endret, "Endret") + vis(borte, "Borte")
        RAPPORT.write_text("\n".join(melding) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
