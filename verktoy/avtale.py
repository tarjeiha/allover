#!/usr/bin/env python3
"""
Tariffavtaler i basen (foreløpig hovedtariffavtalen i staten).

Avtalene ligger ikke på Lovdata. Kildefilen (Word eller PDF fra regjeringen.no)
legges i <mappe>/kilde/, enten via innboksen eller ved at bygget laster den ned.
Dette skriptet deler den opp:

    <mappe>/avtale/punkt-<n-m>.md             punkt i del 1, 2, 4 og 5
    <mappe>/avtale/fellesbestemmelsene/par-<n>.md   paragrafene i del 3
    <mappe>/avtale/del-<n>.md                 del 6–9 og annen tekst uten punkter
    <mappe>/avtale/vedlegg-<n>.md             vedleggene
    <mappe>/VEIVISER.md                       bare blokken mellom AUTO-markørene

Bruk alene:
    python3 verktoy/avtale.py      # bygger alle avtaler i regelverk.json
"""

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import sys
import urllib.request
from collections import Counter
from datetime import date
from pathlib import Path

ROT = Path(__file__).resolve().parent.parent
ORD = re.compile(r"\w+", re.UNICODE)
MIN_DEKNING = 0.99
NETTLESER = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/130.0 Safari/537.36"
}
AUTO_START = "<!-- AUTO-START: genereres av verktoy/bygg.py, ikke rediger for hånd -->"
AUTO_SLUTT = "<!-- AUTO-SLUTT -->"


def til_tekst(fil: Path) -> str:
    if fil.suffix.lower() == ".pdf":
        return subprocess.run(["pdftotext", str(fil), "-"], capture_output=True, text=True, check=True).stdout
    md = subprocess.run(
        ["pandoc", str(fil), "-t", "gfm", "--wrap=none"], capture_output=True, text=True, check=True
    ).stdout
    return rett_nummerering(md, word_som_tekst(fil))


def word_som_tekst(fil: Path) -> str:
    """Teksten slik LibreOffice viser den, med Word sin nummerering av lister («4.», «b.»)."""
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(
            ["soffice", "--headless", "--convert-to", "txt:Text (encoded):UTF8", "--outdir", tmp, str(fil)],
            capture_output=True, text=True, check=True, timeout=300,
        )
        return (Path(tmp) / f"{fil.stem}.txt").read_text(encoding="utf-8")


LISTEPUNKT_MD = re.compile(r"^(\s*)(\d+)\.(\s+)(.*)$")
LISTEPUNKT_LO = re.compile(r"^\s*((?:\d{1,2}|[a-zæøå]|[ivx]{1,4})[.)])\s+(.*)$")


def _bokstaver(s: str, n: int = 30) -> str:
    s = re.sub(r"\[\^[^\]]+\]", "", s)
    return "".join(c for c in s.lower() if c.isalpha())[:n]


def rett_nummerering(md: str, lo: str) -> str:
    """
    Pandoc nummererer lister i Word-filer feil når flere lister bygger på samme listemal: nummeret
    fortsetter fra forrige liste («20.» i stedet for «4.»), og bokstavlister blir tall. Nummeret
    hentes derfor fra LibreOffice-teksten, som følger Word. Punktene pares på teksten.
    """
    lo_punkter = [(m.group(1), _bokstaver(m.group(2))) for m in map(LISTEPUNKT_LO.match, lo.splitlines()) if m]
    ut, j, rettet = [], 0, 0
    for linje in md.splitlines():
        m = LISTEPUNKT_MD.match(linje)
        if m:
            nokkel = _bokstaver(m.group(4))
            for k in range(j, min(j + 40, len(lo_punkter))):
                etikett, tekst = lo_punkter[k]
                if nokkel and tekst and (tekst.startswith(nokkel) or nokkel.startswith(tekst)):
                    if etikett != f"{m.group(2)}.":
                        rettet += 1
                    linje = f"{m.group(1)}{etikett}{m.group(3)}{m.group(4)}"
                    j = k + 1
                    break
        ut.append(linje)
    return "\n".join(ut) + "\n"


def renset(linje: str) -> str:
    """Overskriftslinje uten markdown-pynt."""
    s = re.sub(r"^#+\s*", "", linje.strip())
    s = re.sub(r"^\*\*(.*)\*\*$", r"\1", s).strip()
    s = s.replace("\\", "")
    return re.sub(r"\s+", " ", s)


def er_innholdsfortegnelse(linje: str) -> bool:
    return bool(re.search(r"\.{4,}|_Toc|\]\(#|\t\d+\s*$|\s\d{1,3}\s*$", linje))


DEL = re.compile(r"^(?:Del\s+)?([1-9])\s*(?:[.:–-]\s*)?\s*([A-ZÆØÅ][^\d]{2,80})$")
PUNKT = re.compile(r"^([1-9])\.(\d{1,2})\.?\s+([A-ZÆØÅ(].{1,100})$")
PARAGRAF = re.compile(r"^§\s*(\d{1,2})\.?\s+([A-ZÆØÅ].{1,120})$")
VEDLEGG = re.compile(r"^Vedlegg\s+(\d{1,2})\s*[:.–-]?\s*(.*)$")


def del_opp(tekst: str) -> list:
    """Deler avtaleteksten i (nøkkel, tittel, linjer). Overskriftene må komme i stigende rekkefølge,
    så innholdsfortegnelsen og henvisninger i løpende tekst ikke blir tatt for overskrifter."""
    deler = [("innledning", "Innledning", [])]
    gjeldende_del, gjeldende_par = 0, 0
    sist_punkt = (0, 0)
    vedlegg = 0
    for linje in tekst.splitlines():
        r = renset(linje)
        if r and not er_innholdsfortegnelse(linje) and len(r) < 130:
            m = VEDLEGG.match(r)
            if m and int(m.group(1)) == vedlegg + 1 and gjeldende_del >= 7:
                vedlegg += 1
                deler.append((f"vedlegg-{vedlegg}", r, []))
                continue
            m = DEL.match(r)
            if m and int(m.group(1)) == gjeldende_del + 1 and vedlegg == 0:
                gjeldende_del += 1
                gjeldende_par = 0
                deler.append((f"del-{gjeldende_del}", f"Del {gjeldende_del} {m.group(2).strip(' –-')}", []))
                continue
            m = PUNKT.match(r)
            if m and vedlegg == 0 and int(m.group(1)) == gjeldende_del and gjeldende_del != 3:
                p = (int(m.group(1)), int(m.group(2)))
                if p[1] == sist_punkt[1] + 1 or (p[0] != sist_punkt[0] and p[1] == 1):
                    sist_punkt = p
                    deler.append((f"punkt-{p[0]}-{p[1]}", f"{p[0]}.{p[1]} {m.group(3)}", []))
                    continue
            m = PARAGRAF.match(r)
            if m and gjeldende_del == 3 and int(m.group(1)) == gjeldende_par + 1:
                gjeldende_par += 1
                deler.append((f"par-{gjeldende_par}", f"§ {gjeldende_par} {m.group(2)}", []))
                continue
        deler[-1][2].append(linje)
    return deler


TOC_LINJE = re.compile(r"^\[(.+?)\s*\[\d+\]\(#[^)]*\)\]\(#[^)]*\)\s*$")
TOC_NUMMER = re.compile(r"^(§\s*\d+|Vedlegg\s+\d+:?|\d+(?:\.\d+)*)\s+(.*)$")
FOTNOTE_DEF = re.compile(r"^\[\^([^\]]+)\]:")


def _norm(s: str) -> str:
    s = re.sub(r"\[\^[^\]]+\]", "", s)
    return re.sub(r"[^\w]+", " ", renset(s).lower()).strip()


def del_opp_etter_overskrifter(tekst: str):
    """
    Deler en Word-fil konvertert med pandoc etter overskriftene, med nummereringen fra
    innholdsfortegnelsen. Word sin automatiske nummerering («2.5.1», «Del 3») blir ikke med i
    overskriftene ved konvertering, men står i innholdsfortegnelsen. Returnerer (deler, tekst uten
    innholdsfortegnelse), eller None når dokumentet ikke har en innholdsfortegnelse å bygge på.
    """
    linjer = tekst.splitlines()
    # Innholdsfortegnelsen: lenkelinjer, noen ganger brutt over to linjer
    toc, i, slutt = [], 0, 0
    buffer = ""
    for n, l in enumerate(linjer):
        if l.startswith("[") or buffer:
            buffer = (buffer + " " + l.strip()).strip()
            m = TOC_LINJE.match(buffer)
            if m:
                tm = TOC_NUMMER.match(renset(m.group(1)))
                if tm:
                    toc.append((re.sub(r"\s+", " ", tm.group(1)).rstrip(":"), tm.group(2).strip()))
                buffer, slutt = "", n + 1
            elif len(buffer) > 400:
                buffer = ""
        elif l.strip() and toc and not l.startswith("#"):
            break
    if len(toc) < 20:
        return None
    kropp = linjer[slutt:]

    # Fotnoter samles og legges til delen som viser til dem
    fotnoter, rest, aktiv = {}, [], None
    for l in kropp:
        m = FOTNOTE_DEF.match(l)
        if m:
            aktiv = m.group(1)
            fotnoter[aktiv] = [l]
        elif aktiv and (l.startswith("    ") or not l.strip()):
            fotnoter[aktiv].append(l)
        else:
            aktiv = None
            rest.append(l)

    deler = [("innledning", "Innledning", [])]
    refs_i_overskrift: dict = {}
    neste = 0
    for l in rest:
        if l.startswith("#"):
            tittel = _norm(l)
            treff = next((k for k in range(neste, min(neste + 4, len(toc))) if _norm(toc[k][1]) == tittel
                          or _norm(f"{toc[k][0]} {toc[k][1]}") == tittel), None)
            if treff is not None:
                neste = treff + 1
                nr, tit = toc[treff]
                hrefs = re.findall(r"\[\^([^\]]+)\]", l)
                tit = re.sub(r"\[\^[^\]]+\]", "", renset(tit))
                deler_nr = nr.split(".")
                if nr.startswith("§"):
                    n = re.sub(r"\D", "", nr)
                    deler.append((f"par-{n}", f"§ {n} {tit}", []))
                    refs_i_overskrift[deler[-1][0]] = hrefs
                    continue
                if nr.startswith("Vedlegg"):
                    n = re.sub(r"\D", "", nr)
                    deler.append((f"vedlegg-{n}", f"Vedlegg {n}: {tit}", []))
                    refs_i_overskrift[deler[-1][0]] = hrefs
                    continue
                if len(deler_nr) == 1:
                    deler.append((f"del-{nr}", f"Del {nr} {tit}", []))
                    refs_i_overskrift[deler[-1][0]] = hrefs
                    continue
                if len(deler_nr) == 2:
                    deler.append((f"punkt-{deler_nr[0]}-{deler_nr[1]}", f"{nr} {tit}", []))
                    refs_i_overskrift[deler[-1][0]] = hrefs
                    continue
                # Underpunkter (2.5.1) blir overskrifter i punktfilen, med nummeret tilbake
                deler[-1][2].append(f"### {nr} {tit}" + "".join(f"[^{h}]" for h in hrefs))
                continue
        deler[-1][2].append(l)

    for nokkel, _, innhold in deler:
        brukt = list(dict.fromkeys(refs_i_overskrift.get(nokkel, [])
                                   + re.findall(r"\[\^([^\]]+)\]", "\n".join(l for l in innhold if not FOTNOTE_DEF.match(l)))))
        if brukt:
            innhold.append("")
            for f in brukt:
                innhold.extend(fotnoter.get(f, []))
    return deler, "\n".join(kropp)


def dekning(kilde: str, md: str) -> float:
    k = Counter(ORD.findall(kilde.lower()))
    u = Counter(ORD.findall(md.lower()))
    tot = sum(k.values())
    return 1.0 if not tot else sum(min(n, u[o]) for o, n in k.items()) / tot


def gjeldende_kilde(mappe: Path):
    filer = sorted(f for f in (mappe / "kilde").glob("*") if f.suffix.lower() in (".docx", ".pdf") and f.is_file())
    return filer[-1] if filer else None


def prov_nedlasting(avtale: dict, merknader: list) -> None:
    """Laster ned kildefilen hvis den er tilgjengelig og har endret seg. Regjeringen.no stenger ofte
    for GitHub sine servere; da brukes filen som ligger i repoet."""
    url = avtale.get("kilde_url")
    if not url:
        return
    mappe = ROT / avtale["mappe"]
    try:
        req = urllib.request.Request(url, headers=NETTLESER)
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
    except Exception as e:  # noqa: BLE001
        merknader.append(f"{avtale['navn']}: fikk ikke lastet ned {url} ({e}). Bruker filen i {avtale['mappe']}/kilde/.")
        return
    navn = Path(url.split("?")[0]).name
    gammel = gjeldende_kilde(mappe)
    if gammel and hashlib.sha256(gammel.read_bytes()).hexdigest() == hashlib.sha256(data).hexdigest():
        return
    (mappe / "kilde").mkdir(parents=True, exist_ok=True)
    if gammel and gammel.name != navn:
        arkiv = mappe / "kilde" / "tidligere"
        arkiv.mkdir(exist_ok=True)
        shutil.move(str(gammel), arkiv / gammel.name)
    (mappe / "kilde" / navn).write_bytes(data)
    merknader.append(f"{avtale['navn']}: ny kildefil lastet ned fra {url}")


def bygg_avtale(avtale: dict, feil: list, merknader: list, indeks: list) -> str | None:
    """Bygger én avtale. Returnerer raden til tabellen i CLAUDE.md, eller None hvis kilden mangler."""
    mappe = ROT / avtale["mappe"]
    kilde = gjeldende_kilde(mappe)
    if not kilde:
        merknader.append(f"{avtale['navn']}: ingen kildefil i {avtale['mappe']}/kilde/ ennå. Last den opp i innboksen.")
        return None
    try:
        tekst = til_tekst(kilde)
    except Exception as e:  # noqa: BLE001
        feil.append(f"{avtale['navn']}: kunne ikke lese {kilde.name}: {e}")
        return None
    oppdelt = del_opp_etter_overskrifter(tekst) if kilde.suffix.lower() == ".docx" else None
    if oppdelt:
        deler, tekst = oppdelt
    else:
        deler = del_opp(tekst)
    antall_par = sum(1 for k, _, _ in deler if k.startswith("par-"))
    antall_del = sum(1 for k, _, _ in deler if k.startswith("del-"))
    if antall_del < 5 or antall_par < 10:
        feil.append(
            f"{avtale['navn']}: fant bare {antall_del} deler og {antall_par} paragrafer i {kilde.name}. "
            "Oppdelingen stemmer trolig ikke med dokumentet, så ingenting er skrevet."
        )
        return None

    ut = mappe / "avtale"
    if ut.exists():
        shutil.rmtree(ut)
    (ut / "fellesbestemmelsene").mkdir(parents=True)
    kildelinje = (
        f"**Kilde:** {avtale['navn']} {avtale.get('periode', '')}, fil `{kilde.name}` "
        f"({avtale.get('utgiver', 'regjeringen.no')})."
    ).replace("  ", " ")
    merknad = "Dette er tariffavtaletekst, ikke lov eller forskrift."
    skrevet, alt_md = [], []
    gjeldende_del_tittel = ""
    for nokkel, tittel, linjer in deler:
        innhold = "\n".join(linjer).strip()
        if nokkel.startswith("del-"):
            gjeldende_del_tittel = tittel
            if not innhold:
                continue
        if not innhold and nokkel == "innledning":
            continue
        if nokkel.startswith("par-"):
            fil = ut / "fellesbestemmelsene" / f"{nokkel}.md"
            overskrift = f"Hovedtariffavtalen i staten, fellesbestemmelsene {tittel}"
        else:
            fil = ut / f"{nokkel}.md"
            overskrift = f"Hovedtariffavtalen i staten {'punkt ' if nokkel.startswith('punkt-') else ''}{tittel}"
        md = f"# {overskrift}\n\n{kildelinje} {merknad}\n\n---\n\n{innhold}\n"
        fil.write_text(md, encoding="utf-8")
        alt_md.append(md)
        skrevet.append((gjeldende_del_tittel if not nokkel.startswith(("vedlegg", "innledning")) else "", tittel, fil))
    d = dekning(tekst, "\n".join(alt_md))
    if d < MIN_DEKNING:
        feil.append(f"{avtale['navn']}: bare {d:.1%} av ordene i kildefilen kom med i oppdelingen")

    linjer = [
        "## Kilder",
        "",
        f"- **Avtale:** {avtale['navn']} {avtale.get('periode', '')}".rstrip(),
        f"- **Kildefil:** `kilde/{kilde.name}` ({avtale.get('utgiver', 'regjeringen.no')})",
        f"- **Sjekksum for kildefilen:** {hashlib.sha256(kilde.read_bytes()).hexdigest()[:12]}",
        "",
        "Dette er tariffavtaletekst, ikke lov- eller forskriftstekst.",
        "",
        "## Innhold",
        "",
    ]
    forrige = None
    for deltittel, tittel, fil in skrevet:
        if deltittel != forrige and deltittel:
            linjer += ["", f"**{deltittel}**", ""]
            forrige = deltittel
        linjer.append(f"- {tittel} – `{fil.relative_to(mappe).as_posix()}`")
        indeks.append(f"{avtale['navn']}\tTariffavtale\t{tittel}\t{fil.relative_to(ROT).as_posix()}")
    erstatt_auto(mappe / "VEIVISER.md", "\n".join(linjer), f"# {avtale['navn']}: veiviser\n")
    return f"| {avtale['navn']} | `{avtale['mappe']}/VEIVISER.md` | {avtale.get('periode', 'ukjent')} |"


ANDRE_START = "<!-- AUTO-START andre kilder: genereres av verktoy/bygg.py, ikke rediger for hånd -->"
ANDRE_SLUTT = "<!-- AUTO-SLUTT andre kilder -->"


def andre_kilder(config: dict) -> str:
    """Tabellene over tariffavtaler og EU-rettsakter i CLAUDE.md, ut fra det som ligger i repoet."""
    ut = []
    avtaler = [a for a in config.get("avtaler", []) if (ROT / a["mappe"] / "avtale").is_dir()]
    if avtaler:
        ut += ["**Tariffavtaler** (ikke lov eller forskrift)", "", "| Avtale | Veiviser | Periode |", "|---|---|---|"]
        ut += [f"| {a['navn']} | `{a['mappe']}/VEIVISER.md` | {a.get('periode', 'ukjent')} |" for a in avtaler]
        ut.append("")
    rettsakter = [a for a in config.get("eu", []) if (ROT / a["mappe"] / "VEIVISER.md").exists()]
    if rettsakter:
        ut += ["**EU-rettsakter** (EU-tekst fra EUR-Lex, ikke norsk lov; se veiviseren om hvilken versjon som gjelder i EØS)", "",
               "| Rettsakt | Nummer | Veiviser | EØS-versjon |", "|---|---|---|---|"]
        for a in rettsakter:
            ut.append(f"| {a['navn']} | {a.get('nummer', '')} | `{a['mappe']}/VEIVISER.md` | "
                      f"{'kontrollert' if a.get('eos') else 'ikke kontrollert'} |")
    return "\n".join(ut) or "_Ingen ennå._"


def oppdater_claude(config: dict) -> None:
    erstatt_auto(ROT / "CLAUDE.md", andre_kilder(config), "", ANDRE_START, ANDRE_SLUTT)


def oppdater_indeks(navn: str, rader: list) -> None:
    """Bytter ut radene for én avtale i indeks.tsv (brukes når innboksen bygger avtalen)."""
    fil = ROT / "indeks.tsv"
    linjer = fil.read_text(encoding="utf-8").splitlines() if fil.exists() else ["lov\tdokument\tparagraf\tsti"]
    linjer = [linje for linje in linjer if not linje.startswith(f"{navn}\t")] + rader
    fil.write_text("\n".join(linjer) + "\n", encoding="utf-8")


def erstatt_auto(fil: Path, innhold: str, skjelett: str, start: str = AUTO_START, slutt: str = AUTO_SLUTT) -> None:
    tekst = fil.read_text(encoding="utf-8") if fil.exists() else skjelett
    blokk = f"{start}\n{innhold.rstrip()}\n{slutt}"
    if start in tekst and slutt in tekst.split(start, 1)[1]:
        før, rest = tekst.split(start, 1)
        tekst = før + blokk + rest.split(slutt, 1)[1]
    else:
        tekst = tekst.rstrip() + "\n\n" + blokk + "\n"
    fil.write_text(tekst, encoding="utf-8")


def main() -> int:
    config = json.loads((ROT / "regelverk.json").read_text(encoding="utf-8"))
    feil, merknader, indeks = [], [], []
    for a in config.get("avtaler", []):
        print(bygg_avtale(a, feil, merknader, indeks))
    for m in merknader:
        print("MERK:", m)
    for f in feil:
        print("FEIL:", f)
    return 1 if feil else 0


if __name__ == "__main__":
    sys.exit(main())
