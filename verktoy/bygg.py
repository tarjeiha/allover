#!/usr/bin/env python3
"""
Bygger lov- og forskriftstekst i repoet fra Lovdatas åpne datasett (NLOD 2.0).

Bruk:
    python3 verktoy/bygg.py                 # laster ned datasettene og bygger
    python3 verktoy/bygg.py --kilde <mappe> # bruker allerede utpakkede datasett

Hva som bygges styres av regelverk.json. For hver lov skrives:
    <mappe>/lov/par-<nr>.md                       én fil per paragraf
    <mappe>/forskrifter/<slug>/par-<nr>.md        én fil per forskriftsparagraf
    <mappe>/VEIVISER.md                           bare blokken mellom AUTO-markørene
og for hele repoet:
    indeks.tsv                                    alle paragrafer med sti
    CLAUDE.md                                     bare blokken mellom AUTO-markørene

Håndskrevet tekst utenfor AUTO-markørene røres ikke. Lovtekst skal aldri
redigeres for hånd, fordi den overskrives ved neste bygg.

Parseren (parse_lovdata.py) er hentet fra aid-skill-bygging og håndterer de
kjente fellene i Lovdata-formatet (h2/h3-overskrifter, innhold utenfor legalP,
nøstede kapitler, tabeller, fotnoter).
"""

import argparse
import copy
import json
import re
import shutil
import sys
import tarfile
import urllib.request
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from parse_lovdata import (  # noqa: E402
    har_innhold_utenfor_paragrafer,
    parse_dokument,
    render_paragraf,
    slug_paragraf,
)

ROT = Path(__file__).resolve().parent.parent
API = "https://api.lovdata.no/v1/publicData/get/"
DATASETT = ["gjeldende-lover.tar.bz2", "gjeldende-sentrale-forskrifter.tar.bz2"]
AUTO_START = "<!-- AUTO-START: genereres av verktoy/bygg.py, ikke rediger for hånd -->"
AUTO_SLUTT = "<!-- AUTO-SLUTT -->"
MIN_DEKNING = 0.98


def last_ned(mappe: Path) -> None:
    mappe.mkdir(parents=True, exist_ok=True)
    for navn in DATASETT:
        fil = mappe / navn
        if not fil.exists():
            print(f"Laster ned {navn}")
            with urllib.request.urlopen(API + navn, timeout=300) as r, open(fil, "wb") as f:
                shutil.copyfileobj(r, f)
        with tarfile.open(fil, "r:bz2") as tar:
            tar.extractall(mappe, filter="data")


def filnavn_for(dokid: str) -> str:
    """LOV-2006-05-19-16 -> nl-20060519-016.xml, FOR-2008-10-17-1119 -> sf-20081017-1119.xml"""
    m = re.match(r"(LOV|FOR)-(\d{4})-(\d{2})-(\d{2})-(\d+)$", dokid)
    if not m:
        return ""
    prefiks = "nl" if m.group(1) == "LOV" else "sf"
    return f"{prefiks}-{m.group(2)}{m.group(3)}{m.group(4)}-{int(m.group(5)):03d}.xml"


def lag_oppslag(kilde: Path) -> dict:
    """legacyID og filnavn -> filsti. legacyID leses med regex for å slippe å parse alt."""
    monster = re.compile(r'class="legacyID"[^>]*>\s*([^<\s]+)')
    oppslag = {}
    filer = [f for f in kilde.rglob("*") if f.is_file() and f.suffix in (".xml", ".html")]
    print(f"{len(filer)} dokumenter i datasettene, f.eks. {[f.relative_to(kilde).as_posix() for f in filer[:3]]}")
    for fil in filer:
        oppslag[fil.name] = fil
        m = monster.search(fil.read_text(encoding="utf-8", errors="ignore"))
        if m:
            oppslag[m.group(1).strip()] = fil
    return oppslag


def finn(oppslag: dict, dokid: str):
    return oppslag.get(dokid) or oppslag.get(filnavn_for(dokid))


ORD = re.compile(r"\w+", re.UNICODE)


def dekning(kilde_tekst: str, md: str) -> float:
    """Andel av ordene i kilden som finnes i den genererte filen."""
    kilde = Counter(ORD.findall(kilde_tekst.lower()))
    ut = Counter(ORD.findall(md.lower()))
    totalt = sum(kilde.values())
    if not totalt:
        return 1.0
    funnet = sum(min(n, ut[o]) for o, n in kilde.items())
    return funnet / totalt


def bygg_dokument(sti: Path, utmappe: Path, ref: str, feil: list) -> tuple:
    """Skriver én fil per paragraf og returnerer (metadata, kapitler med oppføringer)."""
    if utmappe.exists():
        shutil.rmtree(utmappe)
    utmappe.mkdir(parents=True)
    meta, kapitler = parse_dokument(sti)
    resultat = []
    brukte = Counter()
    for kap in kapitler:
        oppforinger = []
        for art in kap["paragrafer"]:
            kildetekst = copy.copy(art).get_text(" ")
            md = render_paragraf(art, ref)
            slug = slug_paragraf(art.get("data-name"))
            brukte[slug] += 1
            if brukte[slug] > 1:
                slug = f"{slug}-{brukte[slug]}"
            fil = utmappe / f"par-{slug}.md"
            fil.write_text(md, encoding="utf-8")
            d = dekning(kildetekst, md)
            if d < MIN_DEKNING:
                feil.append(f"{fil.relative_to(ROT)}: bare {d:.1%} av ordene i kilden er med")
            tittel = md.splitlines()[0].lstrip("# ").strip()
            oppforinger.append((tittel, fil))
        resultat.append((kap["tittel"], oppforinger))
    tegn, rest = har_innhold_utenfor_paragrafer(sti)
    if tegn:
        fil = utmappe / "utenfor-paragrafene.md"
        fil.write_text(f"# {ref}: innhold utenfor paragrafene\n\n{rest}", encoding="utf-8")
        resultat.append(("Innhold utenfor paragrafene", [("Vedlegg, tabeller o.l.", fil)]))
    return meta, resultat


def erstatt_auto(fil: Path, innhold: str, skjelett: str) -> None:
    tekst = fil.read_text(encoding="utf-8") if fil.exists() else skjelett
    blokk = f"{AUTO_START}\n{innhold.rstrip()}\n{AUTO_SLUTT}"
    if AUTO_START in tekst and AUTO_SLUTT in tekst:
        før = tekst.split(AUTO_START)[0]
        etter = tekst.split(AUTO_SLUTT, 1)[1]
        tekst = før + blokk + etter
    else:
        tekst = tekst.rstrip() + "\n\n" + blokk + "\n"
    fil.write_text(tekst, encoding="utf-8")


def kilde_linje(meta: dict) -> str:
    deler = [meta["tittel"]]
    if meta["legacyID"]:
        deler.append(meta["legacyID"])
    linje = " – ".join(deler)
    if meta["sist_endret"]:
        linje += f". Sist endret i kraft: {meta['sist_endret']}"
    if meta["departement"]:
        linje += f". Forvaltes av: {meta['departement']}"
    return linje + "."


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kilde", type=Path, help="mappe med utpakkede datasett")
    args = ap.parse_args()

    kilde = args.kilde or ROT / ".lovdata"
    if not args.kilde:
        last_ned(kilde)
    oppslag = lag_oppslag(kilde)
    config = json.loads((ROT / "regelverk.json").read_text(encoding="utf-8"))

    feil: list = []
    indeks = ["lov\tdokument\tparagraf\tsti"]
    lovliste = []

    for lov in config["lover"]:
        mappe = ROT / lov["mappe"]
        lovfil = finn(oppslag, lov["lov"])
        if not lovfil:
            feil.append(f"Fant ikke {lov['lov']} ({filnavn_for(lov['lov'])}) i datasettene")
            continue
        meta, kapitler = bygg_dokument(lovfil, mappe / "lov", lov["navn"], feil)
        linjer = ["## Kilder", "", f"- **Lov:** {kilde_linje(meta)}"]
        forskriftsblokker = []
        for fs in lov.get("forskrifter", []):
            fsfil = finn(oppslag, fs["id"])
            if not fsfil:
                feil.append(f"Fant ikke {fs['id']} ({filnavn_for(fs['id'])}) i datasettene")
                continue
            fmeta, fkap = bygg_dokument(
                fsfil, mappe / "forskrifter" / fs["slug"], fs["navn"], feil
            )
            linjer.append(f"- **Forskrift:** {kilde_linje(fmeta)}")
            forskriftsblokker.append((fs["navn"], fkap))

        def liste(navn, kap):
            ut = [f"### {navn}", ""]
            for kaptittel, oppf in kap:
                if kaptittel:
                    ut += [f"**{kaptittel}**", ""]
                for tittel, fil in oppf:
                    rel = fil.relative_to(mappe).as_posix()
                    ut.append(f"- {tittel} – `{rel}`")
                    indeks.append(f"{lov['navn']}\t{navn}\t{tittel}\t{fil.relative_to(ROT).as_posix()}")
                ut.append("")
            return ut

        linjer += ["", "## Innhold", ""]
        linjer += liste(lov["navn"], kapitler)
        for navn, fkap in forskriftsblokker:
            linjer += liste(navn, fkap)

        skjelett = f"# {lov['navn']}: veiviser\n\n_Håndskrevet veiledning mangler ennå._\n"
        erstatt_auto(mappe / "VEIVISER.md", "\n".join(linjer), skjelett)
        lovliste.append(
            f"| {lov['navn']} | `{lov['mappe']}/VEIVISER.md` | {meta['sist_endret'] or 'ukjent'} |"
        )

    (ROT / "indeks.tsv").write_text("\n".join(indeks) + "\n", encoding="utf-8")
    tabell = ["| Regelverk | Veiviser | Sist endret i kraft |", "|---|---|---|"] + lovliste
    erstatt_auto(ROT / "CLAUDE.md", "\n".join(tabell), "# Regelverksbasen\n")

    if feil:
        print("FEIL:")
        for f in feil:
            print(f"  {f}")
        return 1
    print(f"Ferdig: {len(indeks) - 1} paragrafer i indeksen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
