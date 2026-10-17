"""Deler en Prop. 1 S (Word-fil fra regjeringen.no) opp i Markdown-filer.

Bruk: python3 verktoy/budsjett.py <prop.docx> <utmappe>

Oppdelingen følger stilene i Word-filen fra regjeringen.no:
- Del I og delen med særlige temaer: én fil per overskrift på nivå 1.
- Budsjettforslaget: én fil per programkategori og én fil per budsjettkapittel
  (stil «b-budkaptit»), med postene som underoverskrifter.
- Forslag til vedtak: én fil.
Tabeller gjengis som Markdown-tabeller. Skriptet skriver også poster.tsv
med kapittel, post og posttittel.
"""
import re
import sys
import unicodedata
from pathlib import Path

import docx
from docx.table import Table
from docx.text.paragraph import Paragraph

OVERSKRIFT = {
    "Heading 1": "##", "Heading 2": "###", "Heading 3": "####",
    "b-progkat": "##", "b-budkaptit": "#", "b-post": "##", "b-underpost": "###",
    "avsnitt-tittel": "###", "avsnitt-undertittel": "####",
    "avsnitt-under-undertittel": "#####", "Fullmakttit": "##",
    "a-vedtak-del": "###", "Subtitle": "##", "a-vedtak-tekst": "####", "Formaltit": "##",
}
LISTE = {"List", "List 2", "List Number", "opplisting", "alfaliste", "alfaliste 2",
         "romertall liste 2", "friliste"}


def slug(tekst):
    t = unicodedata.normalize("NFKD", tekst.lower())
    t = t.replace("æ", "ae").replace("ø", "o").replace("å", "a")
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:60]


def rens(tekst):
    return re.sub(r"\s+", " ", tekst.replace("\xa0", " ")).strip()


def tabell_md(tabell):
    rader = []
    for rad in tabell.rows:
        celler, sett = [], set()
        for celle in rad.cells:
            if id(celle._tc) in sett:
                continue
            sett.add(id(celle._tc))
            celler.append(rens(celle.text).replace("|", "\\|"))
        if celler and celler[0] == "KPAL":
            celler[0] = ""
        if any(celler):
            rader.append(celler)
    if not rader:
        return ""
    bredde = max(len(r) for r in rader)
    rader = [r + [""] * (bredde - len(r)) for r in rader]
    ut = ["| " + " | ".join(rader[0]) + " |", "|" + "---|" * bredde]
    ut += ["| " + " | ".join(r) + " |" for r in rader[1:]]
    return "\n".join(ut)


def blokker(dok):
    for el in dok.element.body.iterchildren():
        if el.tag.endswith("}p"):
            yield Paragraph(el, dok)
        elif el.tag.endswith("}tbl"):
            yield Table(el, dok)


def del_opp(sti, utmappe, kilde):
    dok = docx.Document(sti)
    utmappe = Path(utmappe)
    filer = {}          # filnavn -> liste med linjer
    rekkefolge = []
    poster = []
    gjeldende = None
    seksjon = "forside"
    teller = {"del-1": 0, "tema": 0}
    kap = None

    def ny(navn, tittel):
        nonlocal gjeldende
        gjeldende = navn
        if navn not in filer:
            filer[navn] = [f"<!-- Kilde: {kilde}. Generert av verktoy/budsjett.py, skal ikke redigeres for hånd. -->", ""]
            rekkefolge.append((navn, tittel))

    for b in blokker(dok):
        if isinstance(b, Table):
            if gjeldende and seksjon != "forside":
                md = tabell_md(b)
                if md:
                    filer[gjeldende] += [md, ""]
            continue
        stil, tekst = b.style.name, rens(b.text)
        if not tekst:
            continue
        if stil == "del-tittel":
            t = tekst.lower()
            seksjon = "budsjett" if "budsjettforslag" in t else "tema" if "tema" in t else "del-1"
            continue
        if stil in ("del-nr",) or stil.startswith("i-") or stil == "is-dep":
            continue
        if stil.startswith("a-tilraar") or stil == "a-vedtak-tit":
            seksjon = "vedtak"
            ny("forslag-til-vedtak.md", "Forslag til vedtak")
        if seksjon == "forside":
            continue
        if stil == "Heading 1" and seksjon in ("del-1", "tema"):
            teller[seksjon] += 1
            ny(f"{seksjon}-{teller[seksjon]:02d}-{slug(tekst)}.md", tekst)
            filer[gjeldende].append(f"# {tekst}\n")
            continue
        if seksjon == "budsjett":
            if stil == "Heading 1":
                ny("budsjettforslag-innleiing.md", tekst)
                filer[gjeldende].append(f"# {tekst}\n")
                continue
            if stil == "b-progkat":
                m = re.match(r"Programkategori (\d+)\.(\d+)", tekst)
                ny(f"programkategori-{m.group(1)}-{m.group(2)}.md" if m else f"programkategori-{slug(tekst)}.md", tekst)
                filer[gjeldende].append(f"# {tekst}\n")
                continue
            if stil == "b-budkaptit":
                m = re.match(r"Kap\. (\d+)", tekst)
                kap = m.group(1) if m else slug(tekst)
                ny(f"kap-{int(kap):04d}.md" if m else f"kap-{kap}.md", tekst)
                filer[gjeldende].append(f"# {tekst}\n")
                continue
            if stil == "b-post" and kap:
                m = re.match(r"Post (\d+)\s*(.*)", tekst)
                if m:
                    poster.append((kap, m.group(1), m.group(2), gjeldende))
        if gjeldende is None:
            continue
        if stil in OVERSKRIFT:
            filer[gjeldende].append(f"{OVERSKRIFT[stil]} {tekst}\n")
        elif stil in LISTE:
            filer[gjeldende].append(f"- {tekst}")
        elif stil == "Tabellnavn" and re.fullmatch(r"\d+N\d+\w*", tekst):
            continue
        elif stil in ("Tabellnavn", "figur-tittel"):
            filer[gjeldende].append(f"\n**{tekst}**\n")
        elif stil in ("blokksit",):
            filer[gjeldende].append(f"> {tekst}\n")
        else:
            filer[gjeldende].append(f"{tekst}\n")

    utmappe.mkdir(parents=True, exist_ok=True)
    for navn, linjer in filer.items():
        (utmappe / navn).write_text("\n".join(linjer).rstrip() + "\n", encoding="utf-8")
    with open(utmappe / "poster.tsv", "w", encoding="utf-8") as f:
        f.write("kap\tpost\tposttittel\tfil\n")
        for kap_, post, tittel, fil in poster:
            f.write(f"{kap_}\t{post}\t{tittel}\t{fil}\n")
    return rekkefolge, poster


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    kilde = sys.argv[3] if len(sys.argv) > 3 else Path(sys.argv[1]).name
    filer, poster = del_opp(sys.argv[1], sys.argv[2], kilde)
    print(f"{len(filer)} filer, {len(poster)} poster")
