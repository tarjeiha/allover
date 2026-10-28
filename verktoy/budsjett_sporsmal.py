"""Legger svar på budsjettspørsmål fra Stortinget inn i budsjettbasen.

Bruk: python3 verktoy/budsjett_sporsmal.py <samledokument.docx> [...]

Leser samledokumentet som Finansdepartementets system lager (Word, opptil 100 svar per fil).
Hvert svar begynner med «Finansdepartementet: Vårt saksnr:» og har feltene Parti, Spørsmålsnr,
Dato på spørsmålet, Kategori, Tittel, Undertittel, Spørsmål, Kapittel og post, Departement og
Finansdepartementets svar. Tomme maler (feltet Parti er «[Parti]») hoppes over.

Svarene legges i budsjett/ÅR/sporsmal/RUNDE/, én Markdown-fil per svar (PARTI-NR.md), og
sporsmal.tsv lages på nytt av alle filene i mappen. Flere samledokumenter for samme runde kan
derfor lastes opp etter hverandre. Et svar med samme parti og nummer erstattes.
Svar som står i utelatt.txt i mappen (én linje per svar, som filnavnet uten .md, f.eks. «v-143»),
legges ikke inn. Det brukes for svar som ikke er publisert på regjeringen.no.
felt.tsv i mappen holdes for hånd og har én rad per svar (kolonnen fil) med type, tema, år,
forutsetninger, grunnlag, familie, se_ogsa, publisert, versjoner og lenke til regjeringen.no.
Feltene kobles inn i sporsmal.tsv ved hvert bygg, så de overlever ny innlegging.
Runden leses fra linjen «Spørsmål fra Stortingets finanskomite til STB 2026»:
STB = statsbudsjettet (Prop. 1 S), RNB = revidert nasjonalbudsjett. Andre koder brukes som mappenavn.
"""
import csv
import re
from collections import Counter
import sys
from pathlib import Path

import docx
from docx.table import Table

sys.path.insert(0, str(Path(__file__).resolve().parent))
from budsjett import blokker, rens, slug, tabell_md  # noqa: E402

ROT = Path(__file__).resolve().parent.parent
BUDSJETT = ROT / "budsjett"
START = "Finansdepartementet: Vårt saksnr:"
FELT = ["Parti", "Spørsmålsnr", "Dato på spørsmålet", "Kategori", "Tittel", "Undertittel",
        "Spørsmål", "Kapittel og post", "Departement"]
SVAR = "Finansdepartementets svar"
RUNDE = re.compile(r"Spørsmål fra Stortingets (\S+) til (\S+) (\d{4})")
KOLONNER = ["runde", "parti", "nr", "dato", "kategori", "departement", "kap_post", "kapitler",
            "undertittel", "tabeller", "fil"]
TILLEGG = ["type", "tema", "aar", "forutsetninger", "grunnlag", "familie", "se_ogsa",
           "publisert", "versjoner", "lenke"]


def etikett(tekst):
    """Gir feltnavnet hvis avsnittet er en feltetikett («Parti:», «Kapittel og post»)."""
    t = tekst.rstrip(":").strip()
    return t if t in FELT or t == SVAR else None


def svarblokker(sti):
    """Gir én liste med («p», tekst) og («t», markdown) per svar i dokumentet."""
    blokk = None
    for b in blokker(docx.Document(sti)):
        if isinstance(b, Table):
            if blokk is not None:
                md = tabell_md(b)
                if md:
                    blokk.append(("t", md))
            continue
        tekst = rens(b.text)
        if tekst.startswith(START):
            if blokk is not None:
                yield blokk
            blokk = []
        elif blokk is not None and tekst:
            blokk.append(("p", tekst))
    if blokk is not None:
        yield blokk


def les_svar(blokk):
    """Gir en ordbok med feltene, eller None for en tom mal."""
    d = {"komite": "", "runde": "", "aar": None}
    felt, svar = None, []
    for type_, tekst in blokk:
        if type_ == "p" and not d["runde"] and (m := RUNDE.match(tekst)):
            d["komite"], d["runde"], d["aar"] = m.group(1), m.group(2), int(m.group(3))
            continue
        e = etikett(tekst) if type_ == "p" else None
        if e:
            felt = e
            d.setdefault(e, [])
            continue
        if felt == SVAR:
            svar.append((type_, tekst))
        elif felt:
            d[felt].append(tekst)
    for f in FELT:
        verdi = "\n\n".join(d.get(f) or [])
        d[f] = "" if re.fullmatch(r"\[[^\]]*\]", verdi) else verdi
    if not d["Parti"] or not d["runde"]:
        return None
    if not d["Spørsmålsnr"]:
        raise ValueError(f"svar fra {d['Parti']} uten spørsmålsnummer")
    d["svar"] = svar
    return d


def kapitler(kap_post):
    """Henter kapittelnumre (tre eller fire sifre) fra feltet Kapittel og post."""
    return ";".join(dict.fromkeys(re.findall(r"(?<![\d.,])(\d{3,4})(?!\d|,\d)", kap_post)))


def markdown(d):
    linjer = [f"# Spørsmål nr. {d['Spørsmålsnr']} fra {d['Parti']} til {d['runde']} {d['aar']}", ""]
    for navn, verdi in [("Parti", d["Parti"]), ("Spørsmålsnr", d["Spørsmålsnr"]),
                        ("Dato på spørsmålet", d["Dato på spørsmålet"]), ("Kategori", d["Kategori"]),
                        ("Kapittel og post", d["Kapittel og post"]), ("Departement", d["Departement"]),
                        ("Tittel", d["Tittel"])]:
        if verdi:
            linjer.append(f"- **{navn}:** {verdi}")
    linjer += ["", f"## {d['Undertittel'] or 'Spørsmål'}", "", d["Spørsmål"], "", "## Svar", ""]
    for type_, tekst in d["svar"]:
        linjer += [tekst, ""]
    return "\n".join(linjer).rstrip() + "\n"


def tillegg(mappe):
    """Gir de håndførte feltene fra felt.tsv i mappen, med filnavnet som nøkkel."""
    f = mappe / "felt.tsv"
    if not f.exists():
        return {}
    with open(f, encoding="utf-8", newline="") as inn:
        return {r["fil"]: r for r in csv.DictReader(inn, delimiter="\t")}


def oppdater_indeks(mappe):
    ekstra = tillegg(mappe)
    rader = []
    for f in sorted(mappe.glob("*.md")):
        tekst = f.read_text(encoding="utf-8")
        felt = dict(re.findall(r"^- \*\*(.+?):\*\* (.*)$", tekst, re.M))
        overskrift = re.search(r"^## (.+)$", tekst, re.M)
        rader.append({
            "runde": mappe.name, "parti": felt.get("Parti", ""), "nr": felt.get("Spørsmålsnr", ""),
            "dato": felt.get("Dato på spørsmålet", ""), "kategori": felt.get("Kategori", ""),
            "departement": felt.get("Departement", ""), "kap_post": felt.get("Kapittel og post", ""),
            "kapitler": kapitler(felt.get("Kapittel og post", "")),
            "undertittel": overskrift.group(1) if overskrift else "",
            "tabeller": tekst.count("\n|---"), "fil": f.name,
            **{k: ekstra.get(f.name, {}).get(k) or "" for k in TILLEGG},
        })
    rader.sort(key=lambda r: (r["parti"], int(r["nr"]) if r["nr"].isdigit() else 0, r["nr"]))
    with open(mappe / "sporsmal.tsv", "w", encoding="utf-8", newline="") as ut:
        w = csv.DictWriter(ut, fieldnames=KOLONNER + TILLEGG, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for r in rader:
            w.writerow({k: str(v).replace("\t", " ").replace("\n", " ") for k, v in r.items()})
    return rader


def ukjente_familier(rader, budsjett=BUDSJETT):
    """Gir familier i felt.tsv som ikke står i budsjett/sporsmal-familier.tsv."""
    f = budsjett / "sporsmal-familier.tsv"
    if not f.exists():
        return []
    with open(f, encoding="utf-8", newline="") as inn:
        kjente = {r["familie"] for r in csv.DictReader(inn, delimiter="\t")}
    return sorted({r["familie"] for r in rader if r.get("familie")} - kjente)


def utelatt(mappe):
    """Gir filnavnene (uten .md) som ikke skal legges inn, fra utelatt.txt i mappen."""
    f = mappe / "utelatt.txt"
    if not f.exists():
        return set()
    return {l.split("#")[0].strip() for l in f.read_text(encoding="utf-8").splitlines()} - {""}


def legg_inn(sti, budsjett=BUDSJETT):
    """Legger inn alle svar i ett samledokument. Gir en kort rapport."""
    svar = [d for b in svarblokker(sti) if (d := les_svar(b))]
    if not svar:
        raise ValueError("fant ingen svar. Dokumentet ser ikke ut som et samledokument med budsjettspørsmål")
    runder = {(d["aar"], d["runde"]) for d in svar}
    if len(runder) > 1:
        raise ValueError("dokumentet har svar fra flere runder: " + ", ".join(f"{r} {a}" for a, r in sorted(runder)))
    aar, runde = runder.pop()
    mappe = budsjett / str(aar) / "sporsmal" / slug(runde)
    mappe.mkdir(parents=True, exist_ok=True)
    nye = hoppet = 0
    utenfor = utelatt(mappe)
    for d in svar:
        navn = f"{slug(d['Parti'])}-{slug(d['Spørsmålsnr'])}"
        if navn in utenfor:
            hoppet += 1
            continue
        f = mappe / f"{navn}.md"
        nye += not f.exists()
        f.write_text(markdown(d), encoding="utf-8")
    rader = oppdater_indeks(mappe)
    utelatt_tekst = f", {hoppet} utelatt etter utelatt.txt" if hoppet else ""
    per_parti = Counter(r["parti"] for r in rader)
    uten_felt = sum(not r["type"] for r in rader)
    felt_tekst = f". {uten_felt} uten rad i felt.tsv" if uten_felt else ""
    if ukjente := ukjente_familier(rader, budsjett):
        felt_tekst += ". Ukjente familier: " + ", ".join(ukjente)
    return (f"{len(svar)} svar til {runde} {aar} ({nye} nye{utelatt_tekst}), "
            f"{len(rader)} i alt i `budsjett/{aar}/sporsmal/{mappe.name}/` ("
            + ", ".join(f"{p} {n}" for p, n in sorted(per_parti.items())) + f"){felt_tekst}")


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        print(legg_inn(Path(arg)))
