#!/usr/bin/env python3
"""
Henter Navs rundskriv til EØS-avtalens bestemmelser om trygd (R45-00) fra Lovdata og deler det opp.

Bruk:
    python3 verktoy/r45.py              # hent fra Lovdata, bygg bare hvis «Sist endret» er ny
    python3 verktoy/r45.py --tving      # hent og bygg uansett
    python3 verktoy/r45.py --fil x.html # bygg fra en lagret side (når Lovdata ikke kan nås)

R45 er ett stort dokument (over 2 MB HTML) med kapitler som følger folketrygdlovens kapitler, pluss
barnetrygd (33), kontantstøtte (34) og bidragsforskudd (54). Det kommenterer trygdeforordningen
(EF) nr. 883/2004 og gjennomføringsforordningen (EF) nr. 987/2009, og legges derfor under
trygdeforordningen: regelverk/eu/forordning-883-2004/rundskriv/r45-00/.

Oppdelingen følger Lovdatas egen inndeling (div med data-level). Hvert kapittel får en mappe, og et
punkt blir én fil sammen med underpunktene sine når det samlet er under GRENSE tegn. Lengre punkter
deles videre. Fotnotene flyttes til filen som viser til dem. Er under 99 % av ordene med etter
oppdelingen, skrives ingenting.

Innboksen (verktoy/rundskriv.py) brukes ikke: den deler etter §-overskrifter og legger rundskriv
under én lov, og passer ikke for R45.
"""

import argparse
import re
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).parent))
from bygg import dekning  # noqa: E402
from rundskriv import slug  # noqa: E402

ROT = Path(__file__).resolve().parent.parent
URL = "https://lovdata.no/nav/rundskriv/r45-00"
UT = ROT / "regelverk" / "eu" / "forordning-883-2004" / "rundskriv" / "r45-00"
NAVN = "Navs rundskriv til EØS-avtalens bestemmelser om trygd (R45-00)"
LOVNAVN = "Trygdeforordningen"
GRENSE = 25000
MIN_DEKNING = 0.99
NIVÅ = re.compile(r'<div data-level="(\d)"[^>]*\bid="([^"]+)"[^>]*>')


def hent(url: str = URL, forsok: int = 3) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (regelverksbasen; tarjeiha/allover)"})
    for i in range(forsok):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read().decode("utf-8", errors="replace")
        except Exception as e:  # noqa: BLE001
            if i == forsok - 1:
                raise
            print(f"Henting feilet ({e}), prøver igjen")
            time.sleep(5 * (i + 1))
    raise RuntimeError("uventet")


def sist_endret(html: str) -> str:
    meta = BeautifulSoup(html[: html.find('id="documentBody"') + 1000], "lxml").find(id="documentMeta")
    if meta is None:
        raise ValueError("fant ikke metadata (Myndighet, Dato, Sist endret) på siden")
    felt = [t.get_text(" ", strip=True) for t in meta.find_all(["th", "td"])]
    for k, v in zip(felt, felt[1:]):
        if k == "Sist endret":
            return v
    raise ValueError("fant ikke «Sist endret» i metadata")


def lagret_sist_endret() -> str:
    oversikt = UT / "oversikt.md"
    if not oversikt.exists():
        return ""
    m = re.search(r"^Sist endret hos Nav: (\S+)", oversikt.read_text(encoding="utf-8"), re.M)
    return m.group(1) if m else ""


def tekst(html: str) -> str:
    return BeautifulSoup(html, "lxml").get_text(" ", strip=True)


def seksjoner(html: str) -> tuple:
    """Deler dokumentet ved hver <div data-level=...>. Lovdatas div-er nestes ikke alltid riktig,
    så oppdelingen gjøres på teksten, ikke på treet. Returnerer (innledning, [seksjon], fotnoter)."""
    start = html.find('id="documentBody"')
    if start < 0:
        raise ValueError("fant ikke dokumentteksten (documentBody) på siden")
    start = html.find(">", start) + 1
    slutt = html.find("<footer", start)
    kropp = html[start: slutt if slutt > 0 else len(html)]
    # Fotnotene står i tabeller i slutten av kapitlene. De tas ut og legges i filen som viser til dem.
    fotnoter = {}
    def ta_ut(m):
        tabell = BeautifulSoup(m.group(0), "lxml")
        for rad in tabell.find_all("tr"):
            nr, innhold = rad.find("td", class_="fotnoteNummer"), rad.find("td", class_="fotnote")
            if nr is None or innhold is None or nr.a is None:
                continue
            fotnoter[nr.a.get("id")] = (nr.get_text(strip=True), innhold.decode_contents())
        return ""
    kropp = re.sub(r'<table class="[^"]*\bfotnote\b[^"]*"[^>]*>.*?</table>', ta_ut, kropp, flags=re.S)
    treff = list(NIVÅ.finditer(kropp))
    if not treff:
        raise ValueError("fant ingen kapitler (div med data-level) på siden")
    innledning = kropp[: treff[0].start()]
    ut = []
    for i, m in enumerate(treff):
        bit = kropp[m.end(): treff[i + 1].start() if i + 1 < len(treff) else len(kropp)]
        hm = re.search(r"<h[1-7][^>]*>(.*?)</h[1-7]>", bit, re.S)
        tittel = re.sub(r"\s+", " ", BeautifulSoup(hm.group(1), "lxml").get_text(" ")).strip() if hm else ""
        if hm:
            bit = bit[: hm.start()] + bit[hm.end():]
        ut.append({"nivå": int(m.group(1)), "id": m.group(2), "tittel": tittel, "html": bit, "barn": []})
    return innledning, ut, fotnoter


def tre(seksjoner_: list) -> list:
    røtter, stakk = [], []
    for s in seksjoner_:
        while stakk and stakk[-1]["nivå"] >= s["nivå"]:
            stakk.pop()
        (stakk[-1]["barn"] if stakk else røtter).append(s)
        stakk.append(s)
    return røtter


def størrelse(s: dict) -> int:
    return len(tekst(s["html"])) + sum(størrelse(b) for b in s["barn"])


def samlet_html(s: dict, dybde: int = 0) -> str:
    """Seksjonen med alle underpunkter. Underpunktene får overskrift h2, h3 ... etter dybde."""
    h = min(1 + dybde, 6)
    ut = f"<h{h}>{s['tittel']}</h{h}>{s['html']}" if dybde else s["html"]
    return ut + "".join(samlet_html(b, dybde + 1) for b in s["barn"])


def til_markdown(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    for a in soup.find_all("a"):
        href = a.get("href")
        if not href:
            a.unwrap() if a.get_text(strip=True) else a.decompose()
            continue
        if href.startswith("#fotnote_"):
            continue
        if href.startswith("#"):
            a["href"] = URL + href
        elif href.startswith("/"):
            a["href"] = "https://lovdata.no" + href
    # <colgroup><col span="4"> leser pandoc som én kolonne, og resten av tabellen forsvinner
    for t in soup.find_all(["span", "colgroup"]):
        if t.name == "colgroup" or "namedAnchor" in (t.get("class") or []):
            t.decompose()
    # Lovdata har avsnitt rett i listen (<ul><li>…</li><p>…</p></ul>). Pandoc dropper dem, så de flyttes
    # inn i punktet foran.
    for liste in soup.find_all(["ul", "ol"]):
        for barn in list(liste.children):
            if getattr(barn, "name", None) in ("li", None):
                continue
            forrige = barn.find_previous_sibling("li")
            if forrige is None:
                forrige = soup.new_tag("li")
                barn.insert_before(forrige)
            forrige.append(barn.extract())
    for t in soup.find_all(True):
        for attr in ("class", "style", "data-uid", "data-id", "data-level", "data-refid", "id", "name"):
            t.attrs.pop(attr, None)
    ut = subprocess.run(["pandoc", "-f", "html", "-t", "gfm", "--wrap=none"],
                        input=str(soup.body or soup), capture_output=True, text=True, check=True).stdout
    ut = ut.replace("​", "")
    # Fotnotehenvisningene blir [^N]
    ut = re.sub(r"<sup>\s*\[\s*(\d+)\s*\]\(#fotnote_(\d+)\)\s*</sup>", r"[^\2]", ut)
    ut = re.sub(r"\[\s*(\d+)\s*\]\(#fotnote_(\d+)\)", r"[^\2]", ut)
    return re.sub(r"\n{3,}", "\n\n", ut).strip() + "\n"


def fotnotetekst(md: str, fotnoter: dict) -> tuple:
    """Legger til fotnotene filen viser til, nummerert som i rundskrivet. Returnerer (md, kildetekst)."""
    brukte = []
    for n in re.findall(r"\[\^(\d+)\]", md):
        if n not in brukte:
            brukte.append(n)
    if not brukte:
        return md, ""
    linjer, kilde = [], []
    for n in brukte:
        vis, innhold = fotnoter.get(f"fotnote_{n}", (n, ""))
        md = md.replace(f"[^{n}]", f"<sup>{vis}</sup>")
        fn = til_markdown(innhold).strip().replace("\n\n", " ")
        linjer.append(f"{vis}. {fn}")
        kilde.append(tekst(innhold))
    return md + "\n## Fotnoter\n\n" + "\n".join(linjer) + "\n", " ".join(kilde)


def filnavn(tittel: str, brukte: set) -> str:
    m = re.match(r"^\s*(\d+(?:\s?\.\s?\d+)*)\.?\s*[–-]?\s*(.*)$", tittel)
    nummer, rest = (re.sub(r"\s", "", m.group(1)).replace(".", "-"), m.group(2)) if m else ("", tittel)
    kort = slug(rest)
    if len(kort) > 50:
        kort = kort[:51].rsplit("-", 1)[0]
    navn = (f"{nummer}-" if nummer else "") + kort
    navn = navn.strip("-") or "punkt"
    kandidat, i = navn, 2
    while kandidat in brukte:
        kandidat, i = f"{navn}-{i}", i + 1
    brukte.add(kandidat)
    return kandidat + ".md"


def kapittelmappe(tittel: str, brukte: set) -> str:
    m = re.match(r"^Kapittel\s+(\d+(?:\s*–\s*\d+)?)\s*–", tittel)
    navn = "kap-" + (re.sub(r"\D+", "-", m.group(1)).strip("-") if m else slug(tittel)[:30])
    kandidat, i = navn, 2
    while kandidat in brukte:
        kandidat, i = f"{navn}-{i}", i + 1
    brukte.add(kandidat)
    return kandidat


def skriv(html: str, ut: Path = UT) -> list:
    endret = sist_endret(html)
    innledning, alle, fotnoter = seksjoner(html)
    kapitler = tre(alle)
    filer = []  # (mappe, filnavn, tittel, anker, md, kildetekst, kapittel)

    def legg_til(mappe, navn, tittel, anker, kropp_html, kapittel):
        md = til_markdown(kropp_html)
        md, fn_kilde = fotnotetekst(md, fotnoter)
        filer.append((mappe, navn, tittel, anker, md, tekst(kropp_html) + " " + fn_kilde, kapittel))

    def del_opp(s, mappe, brukte, kapittel):
        if størrelse(s) <= GRENSE or not s["barn"]:
            legg_til(mappe, filnavn(s["tittel"], brukte), s["tittel"], s["id"], samlet_html(s), kapittel)
            return
        if tekst(s["html"]):
            legg_til(mappe, filnavn(s["tittel"], brukte), s["tittel"], s["id"], s["html"], kapittel)
        for b in s["barn"]:
            del_opp(b, mappe, brukte, kapittel)

    mapper = set()
    for kap in kapitler:
        mappe = kapittelmappe(kap["tittel"], mapper)
        brukte = set()
        if størrelse(kap) <= GRENSE:
            legg_til(mappe, "00-kapittel.md", kap["tittel"], kap["id"], samlet_html(kap), kap["tittel"])
            continue
        if tekst(kap["html"]):
            legg_til(mappe, "00-innledning.md", kap["tittel"] + " (innledning)", kap["id"], kap["html"], kap["tittel"])
        for b in kap["barn"]:
            del_opp(b, mappe, brukte, kap["tittel"])

    # Kontroll: alle ord i kilden skal være med
    kilde = tekst(innledning) + " " + " ".join(tekst(s["html"]) + " " + s["tittel"] for s in alle)
    kilde += " " + " ".join(tekst(v) for _, v in fotnoter.values())
    samlet = tekst(innledning) + " " + " ".join(f[2] + " " + f[4] for f in filer)
    d = dekning(kilde, samlet)
    if d < MIN_DEKNING:
        raise ValueError(f"bare {d:.1%} av ordene i rundskrivet kom med ved oppdelingen")

    if ut.exists():
        shutil.rmtree(ut)
    ut.mkdir(parents=True)
    rader = []
    per_kapittel, artikkelpunkter = {}, []
    for mappe, navn, tittel, anker, md, _, kapittel in filer:
        (ut / mappe).mkdir(exist_ok=True)
        rel = f"{mappe}/{navn}"
        hode = (f'---\nrundskriv: "{NAVN}"\nkapittel: "{kapittel}"\npunkt: "{tittel}"\n'
                f'kilde: "{URL}#{anker}"\nsist_endret: "{endret}"\n---\n\n')
        (ut / rel).write_text(
            hode + f"# {tittel}\n\n{NAVN}. {kapittel}. Dette er ikke lov-, forskrifts- eller rettsaktstekst.\n\n"
            + md, encoding="utf-8")
        rader.append((f"R45 {tittel}" if tittel.startswith(kapittel) else f"R45 {kapittel} – {tittel}", rel))
        per_kapittel.setdefault((mappe, kapittel), []).append(f"- {tittel} – `{navn}`")
        if re.search(r"\bartikk?(el|lene)\b", tittel, re.I):
            artikkelpunkter.append(f"- {tittel} – `{rel}`")
    kap_liste = []
    for (mappe, kapittel), linjer in per_kapittel.items():
        (ut / mappe / "oversikt.md").write_text(
            f"# R45 {kapittel}\n\n{NAVN}. Kilde: {URL}. Sist endret hos Nav: {endret}.\n\n"
            "## Innhold\n\n" + "\n".join(linjer) + "\n", encoding="utf-8")
        kap_liste.append(f"- {kapittel} – `{mappe}/` ({len(linjer)} filer, start med `{mappe}/oversikt.md`)")

    intro = til_markdown(innledning).strip()
    oversikt = (
        f"# {NAVN}\n\n"
        f"Rundskriv fra Arbeids- og velferdsdirektoratet (Nav) til trygdeforordningen (EF) nr. 883/2004 og "
        f"gjennomføringsforordningen (EF) nr. 987/2009, slik de gjelder etter EØS-avtalen. "
        f"Dette er ikke lov-, forskrifts- eller rettsaktstekst.\n\n"
        f"Kilde: {URL}\n\n"
        f"Sist endret hos Nav: {endret}\n\n"
        + (f"{intro}\n\n" if intro else "")
        + "Kapitlene følger folketrygdlovens kapitler (kapittel 8 gjelder sykepenger osv.). Kapittel 1 er en "
        "generell del om EØS-avtalen og forordningene, kapittel 2 gjelder medlemskap og lovvalg. Kapittel 33, 34 "
        "og 54 gjelder barnetrygd, kontantstøtte og bidragsforskudd.\n\n"
        "## Kapitler\n\n" + "\n".join(kap_liste) + "\n\n"
        "## Punkter med artikkel i overskriften\n\n" + "\n".join(artikkelpunkter) + "\n"
    )
    (ut / "oversikt.md").write_text(oversikt, encoding="utf-8")
    oppdater_indeks(ut.relative_to(ROT).as_posix(), [(t, f"{ut.relative_to(ROT).as_posix()}/{r}") for t, r in rader])
    print(f"R45 (sist endret {endret}): {len(filer)} filer i {len(mapper)} kapitler, dekning {d:.2%}")
    return filer


def oppdater_indeks(rel: str, rader: list) -> None:
    """Rundskrivet skal kunne finnes med en gang. Nattbygget lager de samme radene."""
    sti = ROT / "indeks.tsv"
    linjer = sti.read_text(encoding="utf-8").splitlines() if sti.exists() else ["lov\tdokument\tparagraf\tsti"]
    linjer = [l for l in linjer if not l.split("\t")[-1].startswith(rel + "/")]
    linjer += [f"{LOVNAVN}\tRundskriv\t{t}\t{s}" for t, s in rader]
    sti.write_text("\n".join(linjer) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--fil", help="lagret HTML-side i stedet for å hente fra Lovdata")
    p.add_argument("--tving", action="store_true", help="bygg selv om «Sist endret» er uendret")
    a = p.parse_args()
    html = Path(a.fil).read_text(encoding="utf-8") if a.fil else hent()
    endret = sist_endret(html)
    if not a.tving and not a.fil and endret == lagret_sist_endret():
        print(f"R45 er uendret (sist endret {endret}).")
        return 0
    skriv(html)
    rapport = ROT / "r45-rapport.txt"
    rapport.write_text(f"R45: EØS-rundskrivet fra Nav oppdatert (sist endret {endret})\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
