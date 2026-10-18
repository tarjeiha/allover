#!/usr/bin/env python3
"""
Henter Navs webtabeller (HTML-tabeller under /tabeller/) og lagrer dem som TSV i data/nav/.

Bruk:
    python3 verktoy/nav_webtabell.py [--tor]

Mange av Navs tidsserier finnes bare som webtabeller, ikke som xlsx. Arkivsidene for uføretrygd
har for eksempel 29 webtabeller per 31. desember 2016–2025. Sidene står i data/nav/webtabeller.json.

For hver side i webtabeller.json:
  1. Siden leses, og alle lenker til /tabeller/ plukkes ut.
  2. Hver webtabell leses. Innholdet (overskrifter og tabeller) lagres som original i
     data/nav/<prefiks>-<navn>/original/<navn>.html, og tabellene skrives som TSV.
  3. Hvert tall i TSV-en kontrolleres mot originalen. Avvik gir feil, og tabellen legges ikke inn.
Tabeller som ikke har endret seg siden sist, skrives ikke på nytt.
Med --tor skrives ingenting; skriptet viser bare hva som ville blitt lagt inn.

Rapporten skrives til nav-webtabell-rapport.txt.
"""
import datetime
import hashlib
import html
import json
import re
import shutil
import sys
import urllib.parse
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from data_innboks import NAV, bygg_indeks  # noqa: E402
from nav_hent import hent  # noqa: E402

ROT = Path(__file__).resolve().parent.parent
LENKE = re.compile(r'href="([^"]*?/tabeller/[^"#]+)"', re.I)
TALL = re.compile(r"^-?\d{1,3}(?: \d{3})*(?:,\d+)?$|^-?\d+(?:,\d+)?$")


class Webtabell(HTMLParser):
    """Leser overskrifter (h2/h3) og tabeller i rekkefølge fra innholdsdelen av siden."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.deler = []  # ("overskrift", tekst) eller ("tabell", {"hode": [...], "kropp": [...]})
        self._tekst = None
        self._tabell = None
        self._rad = None
        self._celle = None
        self._span = 1
        self._del = None

    def handle_starttag(self, tag, attrs):
        if tag in ("h2", "h3") and self._tabell is None:
            self._tekst = []
        elif tag == "table":
            self._tabell = {"hode": [], "kropp": []}
            self._del = "kropp"
        elif self._tabell is not None:
            if tag == "thead":
                self._del = "hode"
            elif tag == "tbody":
                self._del = "kropp"
            elif tag == "tr":
                self._rad = []
            elif tag in ("td", "th") and self._rad is not None:
                self._celle = []
                span = dict(attrs).get("colspan") or "1"
                self._span = int(span) if span.isdigit() else 1

    def handle_endtag(self, tag):
        if tag in ("h2", "h3") and self._tekst is not None:
            t = rens("".join(self._tekst))
            if t:
                self.deler.append(("overskrift", t))
            self._tekst = None
        elif tag == "table" and self._tabell is not None:
            self.deler.append(("tabell", self._tabell))
            self._tabell = None
        elif self._tabell is not None:
            if tag in ("td", "th") and self._celle is not None:
                self._rad += [rens("".join(self._celle))] + [""] * (self._span - 1)
                self._celle = None
            elif tag == "tr" and self._rad is not None:
                if any(self._rad):
                    self._tabell[self._del].append(self._rad)
                self._rad = None
            elif tag == "thead":
                self._del = "kropp"

    def handle_data(self, data):
        if self._celle is not None:
            self._celle.append(data)
        elif self._tekst is not None:
            self._tekst.append(data)


def rens(t):
    return re.sub(r"\s+", " ", t.replace("\xa0", " ")).strip()


def tall(t):
    """«318 244» -> «318244», «10,6» -> «10.6». Annen tekst («-», «:», «.») beholdes."""
    if TALL.match(t):
        return t.replace(" ", "").replace(",", ".")
    return t


def innhold(side_html):
    """Klipper ut innholdsdelen (statPage) av siden, eller hele <main> om den mangler."""
    m = re.search(r'<div class="statPage">.*?</article>', side_html, re.S)
    if not m:
        m = re.search(r'<main.*?</main>', side_html, re.S) or re.search(r'id="maincontent".*', side_html, re.S)
    return m.group(0) if m else ""


def les(original):
    p = Webtabell()
    p.feed(original)
    return p.deler


def til_tsv(deler):
    """Én TSV-blokk per tabell. Kolonnen «gruppe» er overskriften over tabellen."""
    linjer, overskrift = [], ""
    for type_, d in deler:
        if type_ == "overskrift":
            overskrift = d
            continue
        for rad in d["hode"]:
            linjer.append("\t".join(["gruppe", "rad"] + rad[1:]))
        for rad in d["kropp"]:
            linjer.append("\t".join([overskrift, rad[0]] + [tall(c) for c in rad[1:]]))
    return linjer


def kontroller(deler, tsvlinjer):
    """Sammenligner hvert tall i originalen med TSV-en. Returnerer antall tall og antall avvik."""
    kilde = []
    for type_, d in deler:
        if type_ == "tabell":
            for rad in d["kropp"]:
                kilde += [c for c in rad[1:] if TALL.match(c)]
    tsv = []
    for linje in tsvlinjer:
        if linje.startswith("#") or linje.startswith("gruppe\t"):
            continue
        tsv += [c for c in linje.split("\t")[2:] if re.match(r"^-?\d+(?:\.\d+)?$", c)]
    avvik = sum(1 for a, b in zip(kilde, tsv) if float(a.replace(" ", "").replace(",", ".")) != float(b))
    avvik += abs(len(kilde) - len(tsv))
    return len(kilde), avvik


KORTFORMER = [
    ("mottakere-av-uforetrygd-", ""), ("av-uforetrygd-", ""),
    ("tabellen-viser-landene-hvor-flest-kommer-fra", ""),
    ("som-andel-av-befolkningen", "andel"), ("per-1000-ikke-ufor-i-befolkningen", "per-1000"),
    ("gjennomsnittlig-arlig-pensjon", "gjennomsnitt"), ("aldersstandardiserte-tall", "aldersstandardisert"),
    ("hvor-uforegrad-er-forskjellig-fra-utbetalingsgrad", "uforegrad-ulik-utbetalingsgrad"),
    ("med-beregnet-ytelse-som-ung-ufor", "ung-ufor"), ("-belop-i-kroner", "-kroner"), ("-per-tusen", ""), ("-per-1000-", "-"),
]


def navn_fra_url(url):
    """mottakere-av-uforetrygd-etter-kjonn-og-alder.pr.31.12.2016-2025.antall -> kjonn-alder-antall"""
    s = urllib.parse.unquote(url.rstrip("/").rsplit("/", 1)[-1]).lower()
    s = re.sub(r"\.pr\.[\d.\-]+", ".", s)
    s = re.sub(r"\.\d\.kvartal-\d\.kvartal-[\d\-]+", ".", s)
    s = re.sub(r"\.\d{4}(?:-\d{4})?(?=[.-]|$)", ".", s)
    s = re.sub(r"[^a-z0-9]+", "-", s.replace(".", "-")).strip("-")
    for gammel, ny in KORTFORMER:
        s = s.replace(gammel, ny)
    s = re.sub(r"(^|-)etter-", r"\1", s).replace("-og-", "-")
    return re.sub(r"-+", "-", s).strip("-")


def lenker(side):
    tekst = hent(side).decode("utf-8", "replace")
    ut = []
    for m in LENKE.finditer(tekst):
        url = urllib.parse.urljoin("https://www.nav.no", html.unescape(m.group(1)))
        if url not in ut:
            ut.append(url)
    return ut


def legg_inn(url, prefiks, arkivside, beskrivelse, tor):
    navn = navn_fra_url(url)
    mappe = NAV / f"{prefiks}-{navn}"
    original = innhold(hent(url).decode("utf-8", "replace"))
    deler = les(original)
    if not any(t == "tabell" for t, _ in deler):
        raise ValueError("fant ingen tabell på siden")
    gammel = mappe / "original" / f"{navn}.html"
    if gammel.exists() and hashlib.sha256(gammel.read_bytes()).digest() == hashlib.sha256(original.encode()).digest():
        return None
    tittel = next((d for t, d in deler if t == "overskrift"), navn)
    iday = datetime.date.today().isoformat()
    hode = [
        "# Kilde: Nav",
        f"# Tabell: {tittel}",
        f"# Kildeside: {url}",
        f"# Arkivside: {arkivside}",
        f"# Lagt inn: {iday}",
        "# Webtabell hos Nav (ikke xlsx). Kolonnen «gruppe» er overskriften over hver deltabell.",
    ]
    linjer = hode + til_tsv(deler)
    antall, avvik = kontroller(deler, linjer)
    if avvik:
        raise ValueError(f"{avvik} av {antall} tall ble ikke like i TSV-en")
    if tor:
        return f"{mappe.relative_to(ROT).as_posix()} ({antall} tall)"
    ny = Path(str(mappe) + ".ny")
    shutil.rmtree(ny, ignore_errors=True)
    (ny / "original").mkdir(parents=True)
    (ny / "original" / f"{navn}.html").write_text(original, encoding="utf-8")
    (ny / f"{navn}.tsv").write_text("\n".join(linjer) + "\n", encoding="utf-8")
    (ny / "om.md").write_text(
        f"# {tittel}\n\nKilde: Nav, {url}\nArkivside: {arkivside}\n{beskrivelse}\nLagt inn: {iday}\n",
        encoding="utf-8",
    )
    if mappe.exists():
        shutil.rmtree(mappe)
    ny.rename(mappe)
    return f"{mappe.relative_to(ROT).as_posix()} ({antall} tall)"


def main(tor=False):
    sider = json.loads((NAV / "webtabeller.json").read_text(encoding="utf-8"))["sider"]
    lagt, uendret, feil = [], 0, []
    for s in sider:
        try:
            urler = lenker(s["side"])
        except Exception as e:  # noqa: BLE001
            feil.append(f"{s['side']}: kunne ikke leses ({e})")
            continue
        if not urler:
            feil.append(f"{s['side']}: fant ingen webtabeller (har Nav endret siden?)")
        for url in urler:
            try:
                r = legg_inn(url, s["prefiks"], s["side"], s.get("beskrivelse", ""), tor)
            except Exception as e:  # noqa: BLE001
                feil.append(f"{url}: {e}")
                continue
            if r:
                lagt.append(r)
            else:
                uendret += 1
    if lagt and not tor:
        bygg_indeks()
    linjer = [f"Nav-webtabeller: {len(lagt)} lagt inn eller endret, {uendret} uendret, {len(feil)} feil", ""]
    if lagt:
        linjer += ["Lagt inn:"] + [f"- {x}" for x in lagt] + [""]
    if feil:
        linjer += ["Feil:"] + [f"- {f}" for f in feil]
    (ROT / "nav-webtabell-rapport.txt").write_text("\n".join(linjer) + "\n", encoding="utf-8")
    print("\n".join(linjer))
    return 1 if feil else 0


if __name__ == "__main__":
    sys.exit(main("--tor" in sys.argv))
