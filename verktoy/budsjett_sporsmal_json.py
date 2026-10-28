"""Legger svar på budsjettspørsmål inn fra regjeringen.no (JSON) og departementets interne liste.

Bruk: python3 verktoy/budsjett_sporsmal_json.py ÅR RUNDE LISTE.xml SIDE.json [SIDE.json ...]

SIDE.json er sidene fra regjeringen.no-API-et for runden (BudsjettSporsmalApi, én fil per side,
eller flere sider etter hverandre i samme fil). LISTE.xml er utdraget fra den interne SharePoint-
listen (SvarTilStortinget, Atom-XML) med kolonnene SfsParti, SfsSpmNummer, SfsBudsjettar,
SfsSpmRunde, SfsSpmKategori, SfsKapittelOgPost og SfsDepartement.

Bare svar som står i begge legges inn: listen sier hvilke svar som er departementets, og JSON
sier at svaret er publisert. Svar som bare står i listen, er ikke publisert og legges ikke inn.
Teksten og tabellene kommer fra JSON. Publiseringsdato, antall versjoner og lenke skrives i
felt.tsv (andre felt i felt.tsv beholdes). Lenken bygges fra svarsiden for runden i
budsjett/sporsmal-sider.tsv.

Listen inneholder upubliserte spørsmål og skal ikke legges i repoet.
"""
import csv
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parent))
from budsjett import rens, slug  # noqa: E402
from budsjett_sporsmal import BUDSJETT, TILLEGG, oppdater_indeks, ukjente_familier, utelatt  # noqa: E402

SIDER = BUDSJETT / "sporsmal-sider.tsv"
NS = {"a": "http://www.w3.org/2005/Atom",
      "d": "http://schemas.microsoft.com/ado/2007/08/dataservices",
      "m": "http://schemas.microsoft.com/ado/2007/08/dataservices/metadata"}
RUNDER = {"statsbudsjettet": "stb", "stb": "stb", "rnb": "rnb"}


def les_json(sti):
    """Gir alle svar i én eller flere API-sider som ligger etter hverandre i filen."""
    tekst = Path(sti).read_text(encoding="utf-8-sig").strip()
    dekoder, i, svar = json.JSONDecoder(), 0, []
    while i < len(tekst):
        obj, i = dekoder.raw_decode(tekst, i)
        svar += obj["Result"]["List"] if "Result" in obj else obj
        while i < len(tekst) and tekst[i] in " \r\n\t,":
            i += 1
    return svar


def les_liste(sti):
    """Gir radene i SharePoint-utdraget (én eller flere Atom-sider etter hverandre)."""
    rader = []
    for del_ in re.split(r"(?=<\?xml)", Path(sti).read_text(encoding="utf-8-sig")):
        if not del_.strip():
            continue
        for e in ET.fromstring(del_.encode("utf-8")).findall("a:entry", NS):
            p = e.find("a:content/m:properties", NS)
            rader.append({c.tag.split("}")[1]: (c.text or "") for c in p})
    return rader


def nummer(verdi):
    return int(float(verdi)) if verdi else None


def dato(navn):
    m = re.search(r"av (\d{1,2})\.(\d{1,2})\.(\d{4})", navn)
    return f"{int(m.group(1)):02d}.{int(m.group(2)):02d}.{m.group(3)}" if m else ""


FELTKODE = re.compile(r"\s*SEQ \w+ \\\* ARABIC\s*")


def tekst(node):
    """Teksten i et HTML-element, uten Word-feltkoder som «SEQ Tabell \\* ARABIC»."""
    return rens(FELTKODE.sub(" ", node.get_text(" ") if hasattr(node, "get_text") else str(node)))


def celle(c):
    return tekst(c).replace("|", "/")


def spenn(c, navn):
    return int(re.sub(r"\D", "", c.get(navn, "1")) or 1)


def tabell_md(tabell):
    # rowspan gjentas nedover, slik Word-innleggingen gjør; colspan gir tomme celler etter teksten
    rader, venter = [], {}
    for tr in tabell.find_all("tr"):
        rad, celler, i = [], list(tr.find_all(["td", "th"])), 0
        while celler or i in venter:
            if i in venter:
                tekst_, igjen = venter.pop(i)
                rad.append(tekst_)
                if igjen > 1:
                    venter[i] = (tekst_, igjen - 1)
                i += 1
                continue
            c = celler.pop(0)
            if spenn(c, "rowspan") > 1:
                venter[i] = (celle(c), spenn(c, "rowspan") - 1)
            rad += [celle(c)] + [""] * (spenn(c, "colspan") - 1)
            i += spenn(c, "colspan")
        rader.append(rad)
    rader = [r for r in rader if any(r)]
    if not rader:
        return ""
    # colspan i HTML-en fra regjeringen.no er ofte for stor; tomme kolonner til slutt fjernes
    bredde = max(max((i + 1 for i, c in enumerate(r) if c), default=1) for r in rader)
    rader = [r[:bredde] for r in rader]
    rader = [r + [""] * (bredde - len(r)) for r in rader]
    linjer = ["| " + " | ".join(rader[0]) + " |", "|" + "---|" * bredde]
    linjer += ["| " + " | ".join(r) + " |" for r in rader[1:]]
    return "\n".join(linjer)


def html_md(html):
    """Gjør svarteksten om til avsnitt og Markdown-tabeller, slik Word-innleggingen gjør."""
    blokker = []

    def gaa(node):
        for barn in node.children:
            navn = getattr(barn, "name", None)
            if navn is None:
                if tekst(barn):
                    blokker.append(tekst(barn))
            elif navn == "table":
                md = tabell_md(barn)
                if md:
                    blokker.append(md)
            elif navn in ("ul", "ol"):
                for li in barn.find_all("li", recursive=False):
                    if tekst(li):
                        blokker.append("- " + tekst(li))
            elif barn.find(["table", "p", "ul", "ol", "div"]):
                gaa(barn)
            elif tekst(barn):
                blokker.append(tekst(barn))

    gaa(BeautifulSoup(html or "", "lxml").body or BeautifulSoup("", "lxml"))
    return blokker


def markdown(aar, runde, intern, svar):
    parti, nr = intern["SfsParti"], nummer(intern["SfsSpmNummer"])
    linjer = [f"# Spørsmål nr. {nr} fra {parti} til {runde.upper()} {aar}", ""]
    for navn, verdi in [("Parti", parti), ("Spørsmålsnr", str(nr)), ("Dato på spørsmålet", dato(svar["Name"])),
                        ("Kategori", intern.get("SfsSpmKategori", "")),
                        ("Kapittel og post", intern.get("SfsKapittelOgPost", "")),
                        ("Departement", intern.get("SfsDepartement", "")), ("Tittel", rens(svar["Name"]))]:
        if verdi:
            linjer.append(f"- **{navn}:** {rens(verdi)}")
    linjer += ["", f"## {rens(svar['Subtitle']) or 'Spørsmål'}", ""]
    linjer += ["\n\n".join(html_md(svar["Question"])), "", "## Svar", ""]
    for b in html_md(svar["Response"]):
        linjer += [b, ""]
    return "\n".join(linjer).rstrip() + "\n"


def svarside(aar, runde):
    with open(SIDER, encoding="utf-8", newline="") as inn:
        for r in csv.DictReader(inn, delimiter="\t"):
            if r["aar"] == str(aar) and r["runde"] == runde:
                return r["side"]
    return ""


def skriv_felt(mappe, nye):
    """Fyller publisert, versjoner og lenke i felt.tsv og beholder de håndførte feltene."""
    f = mappe / "felt.tsv"
    rader = {}
    if f.exists():
        with open(f, encoding="utf-8", newline="") as inn:
            rader = {r["fil"]: r for r in csv.DictReader(inn, delimiter="\t")}
    for fil, verdier in nye.items():
        rader.setdefault(fil, {"fil": fil}).update(verdier)
    with open(f, "w", encoding="utf-8", newline="") as ut:
        w = csv.DictWriter(ut, fieldnames=["fil"] + TILLEGG, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for fil in sorted(rader, key=lambda s: (s.split("-")[0], int(re.sub(r"\D", "", s) or 0))):
            w.writerow({k: rader[fil].get(k, "") for k in ["fil"] + TILLEGG})


def legg_inn(aar, runde, liste, sider, budsjett=BUDSJETT):
    runde = runde.lower()
    publisert = {}
    for side in sider:
        for s in les_json(side):
            publisert.setdefault((s["Party"].upper(), int(s["QuestionNumber"])), []).append(s)
    interne = [r for r in les_liste(liste) if r.get("SfsBudsjettar") == str(aar)
               and RUNDER.get(r.get("SfsSpmRunde", "").lower()) == runde]
    if not interne:
        raise ValueError(f"fant ingen svar for {runde.upper()} {aar} i listen")
    mappe = budsjett / str(aar) / "sporsmal" / runde
    mappe.mkdir(parents=True, exist_ok=True)
    utenfor = utelatt(mappe)
    side_url = svarside(aar, runde)
    felt, ikke_publisert, per_parti = {}, [], Counter()
    for r in interne:
        nr = nummer(r["SfsSpmNummer"])
        navn = f"{slug(r['SfsParti'])}-{nr}"
        versjoner = publisert.get((r["SfsParti"].upper(), nr))
        if not versjoner or navn in utenfor:
            ikke_publisert.append(navn)
            continue
        svar = max(versjoner, key=lambda s: s["SortByPublished"])
        (mappe / f"{navn}.md").write_text(markdown(aar, runde, r, svar), encoding="utf-8")
        per_parti[r["SfsParti"]] += 1
        id_ = svar["ID"].removeprefix("ID")
        felt[f"{navn}.md"] = {"publisert": svar["Published"], "versjoner": str(len({s["ID"] for s in versjoner})),
                              "lenke": f"{side_url}?bq={id_}&page=1" if side_url else ""}
    skriv_felt(mappe, felt)
    rader = oppdater_indeks(mappe)
    ukjente = ukjente_familier(rader, budsjett)
    return (f"{runde.upper()} {aar}: {len(felt)} lagt inn, {len(ikke_publisert)} ikke publisert "
            f"({', '.join(sorted(ikke_publisert)) or 'ingen'}), {len(rader)} i alt ("
            + ", ".join(f"{p} {n}" for p, n in sorted(per_parti.items())) + ")"
            + (f". Ukjente familier: {', '.join(ukjente)}" if ukjente else ""))


if __name__ == "__main__":
    print(legg_inn(int(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4:]))
