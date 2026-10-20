#!/usr/bin/env python3
"""Skriver oversikten over hva basen inneholder i OM-BASENE.md.

Bare blokken mellom AUTO-markørene skrives om. Tallene telles fra filene i repoet:
regelverk.json og rundskrivmappene, mappene under budsjett/, data/nav/indeks.tsv,
pakke.json for Eurostat og OECD, og stortinget/siste-oppdatering.json.

Bruk: python3 verktoy/om_basene.py
"""
import csv
import json
from datetime import date
from pathlib import Path

ROT = Path(__file__).resolve().parent.parent
FIL = ROT / "OM-BASENE.md"
AUTO_START = "<!-- AUTO-START: genereres av verktoy/om_basene.py, ikke rediger for hånd -->"
AUTO_SLUTT = "<!-- AUTO-SLUTT -->"

BUDSJETTDOK = [
    ("prop-1-s-aid", "Prop. 1 S for AID"),
    ("prop-1-s-tillegg-1", "Prop. 1 S Tillegg 1"),
    ("gul-bok", "Gul bok"),
    ("gul-bok-bevilgninger.tsv", "bevilgninger fra Gul bok (tabell)"),
    ("nasjonalbudsjettet", "Nasjonalbudsjettet"),
    ("stortinget", "Stortingets vedtak"),
    ("sporsmal", "svar på budsjettspørsmål fra Stortinget"),
]


def liste(navn: list) -> str:
    return navn[0] if len(navn) == 1 else ", ".join(navn[:-1]) + " og " + navn[-1]


def regelverk() -> list:
    d = json.loads((ROT / "regelverk.json").read_text(encoding="utf-8"))
    lover = d["lover"]
    forskrifter = sum(len(lov.get("forskrifter", [])) for lov in lover)
    rundskriv = sum(1 for _ in (ROT / "regelverk").rglob("rundskriv/*/oversikt.md"))
    ut = [
        "### Regelverk",
        "",
        f"- **{len(lover)} lover og instrukser** med {forskrifter} forskrifter: {liste([lov['navn'] for lov in lover])}.",
    ]
    for avtale in d["avtaler"]:
        ut.append(f"- **{avtale['navn']}**, {avtale['periode']}.")
    ut.append(f"- **{len(d['eu'])} EU-rettsakter** (forordninger og direktiver fra EUR-Lex).")
    if rundskriv:
        ut.append(f"- **{rundskriv} rundskriv** og veiledninger til lovene, blant dem Navs rundskriv til folketrygdloven.")
    ut += [
        "- **Stortinget:** se eget avsnitt under.",
        "",
        "Lov- og forskriftsteksten hentes fra Lovdata hver natt.",
    ]
    return ut


def budsjett() -> list:
    ut = ["### Statsbudsjettet", ""]
    for mappe in sorted((ROT / "budsjett").glob("[0-9][0-9][0-9][0-9]")):
        dok = [tekst for navn, tekst in BUDSJETTDOK if (mappe / navn).exists()]
        if dok:
            ut.append(f"- **{mappe.name}:** {liste(dok)}.")
    satser = sorted(f.stem.replace("stonad", "stønad") for f in (ROT / "budsjett" / "satser").glob("*.tsv"))
    if satser:
        ut.append(f"- **Satstabeller over flere år:** {liste(satser)}.")
    ut += ["", "Budsjettdokumentene lastes opp for hånd. Stortingets vedtak hentes hver uke."]
    return ut


def statistikk() -> list:
    with open(ROT / "data" / "nav" / "indeks.tsv", encoding="utf-8") as f:
        nav = sum(1 for _ in csv.DictReader(f, delimiter="\t"))
    eurostat = len(json.loads((ROT / "data" / "eurostat" / "pakke.json").read_text(encoding="utf-8"))["tabeller"])
    oecd = len(json.loads((ROT / "data" / "oecd" / "pakke.json").read_text(encoding="utf-8"))["tabeller"])
    tekster = len(list((ROT / "data" / "nav" / "tekster").rglob("*.md"))) if (ROT / "data" / "nav" / "tekster").is_dir() else 0
    ut = [
        "### Statistikk",
        "",
        f"- **Nav:** {nav} tabeller (sykefravær, arbeidsledighet, AAP, uføretrygd, pensjon, familieytelser m.m.), hentet hver uke.",
    ]
    if tekster:
        ut.append(f"- **Navs pressemeldinger:** {tekster} fra januar 2024 og framover.")
    ut += [
        f"- **Eurostat:** {eurostat} tabeller for sammenligning med Norden og EU.",
        f"- **OECD:** {oecd} tabeller for sammenligning med andre OECD-land.",
        "- **SSB:** tallene ligger ikke i basen, men katalogen viser hvilke SSB-tabeller som svarer på hva. Claude henter dem med SSB-tilkoblingen.",
    ]
    return ut


def stortinget() -> list:
    if not (ROT / "stortinget" / "siste-oppdatering.json").exists():
        return []
    d = json.loads((ROT / "stortinget" / "siste-oppdatering.json").read_text(encoding="utf-8"))
    sesjoner = sorted(f.stem for f in (ROT / "stortinget" / "data" / "anmodningsvedtak").glob("*.json"))
    tall = lambda n: f"{n:,}".replace(",", " ")
    return [
        "### Stortinget",
        "",
        f"Fra sesjon {sesjoner[0]} til {sesjoner[-1]}, oppdatert {d['dato']}:",
        "",
        f"- **{tall(d['anmodningsvedtak']['total'])} anmodningsvedtak**",
        f"- **{tall(d['sporsmal']['total'])} spørsmål** (skriftlige spørsmål, spørretime og interpellasjoner)",
        f"- **{tall(d['representantforslag']['total'])} representantforslag** med utfall",
    ]


def lag() -> str:
    ut = [f"Oversikten ble sist laget {date.today().isoformat()}.", ""]
    for del_ in (regelverk(), budsjett(), statistikk(), stortinget()):
        if del_:
            ut += del_ + [""]
    return "\n".join(ut)


def main() -> None:
    tekst = FIL.read_text(encoding="utf-8")
    før, _, rest = tekst.partition(AUTO_START)
    _, _, etter = rest.partition(AUTO_SLUTT)
    ny = f"{før}{AUTO_START}\n{lag().rstrip()}\n{AUTO_SLUTT}{etter}"
    # Datoen alene er ingen endring
    gammel = [l for l in tekst.splitlines() if not l.startswith("Oversikten ble sist laget")]
    nye = [l for l in ny.splitlines() if not l.startswith("Oversikten ble sist laget")]
    if gammel != nye:
        FIL.write_text(ny, encoding="utf-8")
        print("skrev OM-BASENE.md")
    else:
        print("uendret")


if __name__ == "__main__":
    main()
