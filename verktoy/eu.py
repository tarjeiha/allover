#!/usr/bin/env python3
"""
EU-laget: henter EU-rettsakter fra EUR-Lex og finner hvor norsk lov- og
forskriftstekst viser til dem.

Brukes av bygg.py. Hva som hentes styres av "eu" i regelverk.json:

    {"mappe": "regelverk/eu/forordning-883-2004", "navn": "Trygdeforordningen",
     "celex": "32004R0883", "versjon": "02004R0883-20190731", "sprak": "EN",
     "eos": "Kontrollert mot folketrygdloven § 1-3 a ..."}

"versjon" er den konsoliderte CELEX-versjonen som skal brukes, eller CELEX for
originalteksten. Den låses med vilje: EUR-Lex viser EU-versjonen, og en nyere
EU-versjon kan inneholde endringer som ikke er tatt inn i EØS-avtalen. Bygget
sjekker om det finnes nyere konsoliderte versjoner og skriver det i veiviseren,
men bytter aldri versjon selv.

For hver rettsakt skrives:
    <mappe>/art-<nr>.md       én fil per artikkel
    <mappe>/vedlegg-<nr>.md   én fil per vedlegg
    <mappe>/VEIVISER.md       bare blokken mellom AUTO-markørene
"""

import copy
import re
import time
import warnings
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag, XMLParsedAsHTMLWarning

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

EURLEX = "https://eur-lex.europa.eu/legal-content/{sprak}/TXT/HTML/?uri=CELEX:{celex}"
SPARQL = "https://publications.europa.eu/webapi/rdf/sparql"
CELLAR = "https://publications.europa.eu/resource/celex/{celex}"
NETTLESER = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/130.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en;q=0.9,nb;q=0.8",
}
MIN_DEKNING = 0.98
ORD = re.compile(r"\w+", re.UNICODE)

# ---------------------------------------------------------------------------
# Henvisninger i norsk tekst
# ---------------------------------------------------------------------------

# Fanger «forordning (EF) nr. 883/2004», «rådsdirektiv 2003/88/EF»,
# «europaparlaments- og rådsforordning (EU) 2016/679» o.l.
HENVISNING = re.compile(
    r"(?<!EØS-komiteens )\b\w*?(forordning|direktiv)\w*\s+"
    r"(?:\((?:EU|EF|EØF|EU, Euratom)\)\s*)?(?:nr\.?\s*)?(\d{1,4})\s*/\s*(\d{2,4})",
    re.IGNORECASE,
)


def nokkel(type_: str, a: str, b: str) -> str:
    """Normaliserer et rettsaktnummer til «R-2004-883» / «L-2003-88»."""
    t = "L" if type_.lower().startswith("direktiv") else "R"
    x, y = int(a), int(b)
    if t == "L":
        aar, nr = x, y
    elif len(b) == 2 or 1958 <= y <= 2014:
        nr, aar = x, y
    else:
        aar, nr = x, y
    if aar < 100:
        aar += 1900 if aar >= 50 else 2000
    return f"{t}-{aar}-{nr}"


def nokkel_fra_celex(celex: str) -> str:
    m = re.match(r"[03](\d{4})([RL])(\d{4})", celex)
    return f"{m.group(2)}-{m.group(1)}-{int(m.group(3))}" if m else ""


def visningsnavn(n: str) -> str:
    t, aar, nr = n.split("-")
    aar, nr = int(aar), int(nr)
    if t == "L":
        return f"Direktiv {aar if aar >= 1999 else aar % 100}/{nr}"
    return f"Forordning {aar}/{nr}" if aar >= 2015 else f"Forordning nr. {nr}/{aar if aar >= 1999 else aar % 100}"


def finn_henvisninger(tekst: str) -> set:
    return {nokkel(m.group(1), m.group(2), m.group(3)) for m in HENVISNING.finditer(tekst)}


# ---------------------------------------------------------------------------
# Henting
# ---------------------------------------------------------------------------


def hent(url: str, forsok: int = 3, ekstra: dict | None = None) -> bytes:
    hoder = {**NETTLESER, **(ekstra or {})}
    if ekstra:
        hoder["Accept"] = "application/xhtml+xml, text/html"
    for i in range(forsok):
        try:
            req = urllib.request.Request(url, headers=hoder)
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except Exception:  # noqa: BLE001
            if i == forsok - 1:
                raise
            time.sleep(5 * (i + 1))
    return b""


def konsoliderte_versjoner(celex: str) -> list:
    """Alle konsoliderte versjoner EUR-Lex kjenner for rettsakten, nyeste først."""
    m = re.match(r"[03](\d{4}[RL]\d{4})", celex)
    if not m:
        return []
    q = (
        "PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>\n"
        "SELECT DISTINCT ?celex WHERE { ?w cdm:resource_legal_id_celex ?celex . "
        f'FILTER(STRSTARTS(STR(?celex), "0{m.group(1)}-")) }} ORDER BY DESC(?celex)'
    )
    url = SPARQL + "?" + urllib.parse.urlencode({"query": q, "format": "text/csv"})
    linjer = hent(url).decode("utf-8").splitlines()[1:]
    return [linje.strip().strip('"') for linje in linjer if linje.strip()]


# ---------------------------------------------------------------------------
# Tolking av EUR-Lex-HTML
# ---------------------------------------------------------------------------

BLOKK = {"p", "div", "table", "ul", "ol", "li", "tr", "td", "th", "tbody", "thead", "hr"}
TITTELKLASSER = {"title-article-norm", "oj-ti-art", "stitle-article-norm", "oj-sti-art"}


def renske(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("\xa0", " ")).strip()


def tekst(el) -> str:
    if isinstance(el, NavigableString):
        return renske(str(el))
    deler = []
    for d in el.descendants:
        if isinstance(d, NavigableString):
            deler.append(str(d))
    return renske(" ".join(deler))


def har_blokkbarn(el: Tag) -> bool:
    return any(isinstance(c, Tag) and c.name in BLOKK for c in el.children)


def tabell(el: Tag) -> list:
    rader = []
    for tr in el.find_all("tr"):
        celler = [tekst(td).replace("|", "\\|") for td in tr.find_all(["td", "th"], recursive=False)]
        if any(celler):
            rader.append(celler)
    if not rader:
        return []
    # Tabeller som bare er oppsett for nummererte punkter: «(a) tekst»
    if all(len(r) == 2 and len(r[0]) <= 8 for r in rader):
        return [f"{r[0]} {r[1]}".strip() for r in rader]
    bredde = max(len(r) for r in rader)
    ut = []
    for i, r in enumerate(rader):
        r = r + [""] * (bredde - len(r))
        ut.append("| " + " | ".join(r) + " |")
        if i == 0:
            ut.append("|" + "---|" * bredde)
    return ["\n".join(ut)]


def blokker(el: Tag) -> list:
    """Gjør et HTML-element om til en liste med avsnitt (markdown)."""
    if isinstance(el, NavigableString):
        s = renske(str(el))
        return [s] if s else []
    if not isinstance(el, Tag) or el.name in ("script", "style"):
        return []
    klasser = set(el.get("class") or [])
    if klasser & TITTELKLASSER or "eli-title" in klasser:
        return []
    if "modref" in klasser or "arrow" in klasser:
        merke = tekst(el)
        return [f"[{merke}]"] if merke else []
    if el.name == "hr":
        return []
    if el.name == "table":
        return tabell(el)
    if "grid-container" in klasser:
        kol1 = el.find(class_="grid-list-column-1")
        kol2 = el.find(class_="grid-list-column-2")
        merke = tekst(kol1) if kol1 else ""
        innhold = []
        for c in (kol2.children if kol2 else []):
            innhold += blokker(c)
        if not innhold:
            return [merke] if merke else []
        return [f"{merke} {innhold[0]}".strip()] + innhold[1:]
    if el.name in ("div", "li", "td", "ul", "ol", "tbody", "section") or (
        el.name == "p" and har_blokkbarn(el)
    ):
        ut = []
        nummer = ""
        for c in el.children:
            if isinstance(c, Tag) and "no-parag" in (c.get("class") or []):
                nummer = tekst(c)
                continue
            b = blokker(c)
            if nummer and b:
                b[0] = f"{nummer} {b[0]}"
                nummer = ""
            ut += b
        if nummer:
            ut.insert(0, nummer)
        # Løs tekst og inline-elementer i en div slås sammen til ett avsnitt
        if not har_blokkbarn(el):
            s = tekst(el)
            return [s] if s else []
        return ut
    s = tekst(el)
    return [s] if s else []


def tekst_uten_titler(el: Tag) -> str:
    """Kildeteksten til dekningskontrollen: artikkeltitlene skrives på norsk og telles ikke."""
    kopi = copy.copy(el)
    for t in kopi.find_all(class_=list(TITTELKLASSER)):
        t.decompose()
    return tekst(kopi)


def tittel_i(el: Tag, klasser: tuple) -> str:
    t = el.find(class_=list(klasser))
    return tekst(t) if t else ""


def kapittel_for(art: Tag) -> str:
    """Nærmeste kapittel-/avsnittsoverskrift over artikkelen."""
    for forelder in art.parents:
        if not isinstance(forelder, Tag):
            continue
        titler = [
            tekst(c)
            for c in forelder.find_all(
                class_=["title-division-1", "title-division-2", "oj-ti-section-1", "oj-ti-section-2"],
                recursive=False,
            )
        ]
        if not titler:
            # oj-format: titlene ligger i en eli-title-div
            for c in forelder.find_all(class_="eli-title", recursive=False):
                titler.append(tekst(c))
            for c in forelder.find_all("p", class_=["oj-ti-section-1"], recursive=False):
                titler.insert(0, tekst(c))
        if titler:
            return " – ".join(t for t in titler if t)
    return ""


def endringsliste(soup) -> list:
    """M- og C-merkene i en konsolidert tekst med navnet på endringsrettsakten."""
    ut, sett = [], set()
    for a in soup.find_all("a"):
        t = tekst(a)
        if re.fullmatch(r"►[MCA]\d+", t) and t not in sett:
            rad = a.find_parent("tr")
            celler = rad.find_all("td") if rad else []
            # Bare oversikten øverst: merket står alene i første celle
            if len(celler) >= 2 and tekst(celler[0]) == t:
                navn = re.sub(r"^(Amended by|Corrected by):\s*", "", tekst(celler[1]))
                if navn:
                    sett.add(t)
                    ut.append((t[1:], navn))
    return ut


def les_rettsakt(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")
    artikler = []
    for div in soup.find_all("div", id=re.compile(r"^art_\d+[a-z]*$")):
        nr = div["id"][4:]
        artikler.append(
            {
                "nr": nr,
                "tittel": tittel_i(div, ("title-article-norm", "oj-ti-art")) or f"Article {nr}",
                "undertittel": tittel_i(div, ("stitle-article-norm", "oj-sti-art")),
                "kapittel": kapittel_for(div),
                "avsnitt": blokker(div),
                "kilde": tekst_uten_titler(div),
            }
        )
    vedlegg = []
    if not artikler:
        artikler, vedlegg = les_eldre_format(soup)
    sett = set()
    for div in soup.find_all("div", id=re.compile(r"^anx_[IVXLC\d]+$")):
        nr = div["id"][4:]
        if nr in sett:
            continue
        sett.add(nr)
        titler = [tekst(p) for p in div.find_all("p", class_=["title-annex-1", "title-annex-2"])]
        vedlegg.append(
            {"nr": nr, "tittel": " – ".join(titler[:2]) or f"Annex {nr}", "avsnitt": blokker(div), "kilde": tekst(div)}
        )
    dok = soup.find(class_=["title-doc-first", "oj-doc-ti", "eli-main-title"])
    deler = []
    for p in soup.find_all("p", class_="title-doc-first"):
        s = tekst(p)
        if s in deler:
            break
        deler.append(s)
    tittel = " ".join(deler) or (tekst(dok) if dok else "")
    return {"tittel": tittel, "artikler": artikler, "vedlegg": vedlegg, "endringer": endringsliste(soup)}


def les_eldre_format(soup) -> list:
    """Eldre tekster på EUR-Lex er bare <p>-er: «Artikel 1», tittel, avsnitt."""
    avsnitt = [tekst(p) for p in soup.find_all("p")]
    artikler, vedlegg, gjeldende = [], [], None
    for i, s in enumerate(avsnitt):
        m = re.fullmatch(r"(?:Article|Artikel|Artikkel)\s+(\d+[a-z]*)", s)
        if m and not vedlegg:
            gjeldende = {"nr": m.group(1), "tittel": s, "undertittel": "", "kapittel": "", "avsnitt": [], "kilde": ""}
            nesten = avsnitt[i + 1] if i + 1 < len(avsnitt) else ""
            if nesten and len(nesten) < 120 and not re.match(r"^\d+\.", nesten):
                gjeldende["undertittel"] = nesten
            artikler.append(gjeldende)
            continue
        if re.fullmatch(r"(?:ANNEX|BILAG|VEDLEGG)(?:\s+[IVXLC\d]+)?", s) and artikler:
            nr = s.split()[1] if len(s.split()) > 1 else str(len(vedlegg) + 1)
            gjeldende = {"nr": nr, "tittel": s, "avsnitt": [], "kilde": ""}
            vedlegg.append(gjeldende)
            continue
        if re.match(r"(?:Done at|Udfærdiget i|Utferdiget i)\b", s) and not vedlegg:
            gjeldende = None
            continue
        if gjeldende is not None and s:
            if s == gjeldende.get("undertittel") and not gjeldende["avsnitt"]:
                continue
            gjeldende["avsnitt"].append(s)
    for a in artikler + vedlegg:
        a["kilde"] = " ".join(a["avsnitt"])
    return artikler, vedlegg


def dekning(kilde: str, md: str) -> float:
    k = Counter(ORD.findall(kilde.lower()))
    u = Counter(ORD.findall(md.lower()))
    tot = sum(k.values())
    return 1.0 if not tot else sum(min(n, u[o]) for o, n in k.items()) / tot


def filnavn(nr: str) -> str:
    return re.sub(r"[^\w-]+", "-", nr.lower()).strip("-")


# ---------------------------------------------------------------------------
# Bygging
# ---------------------------------------------------------------------------


def bygg_rettsakt(rot: Path, akt: dict, feil: list, merknader: list) -> dict | None:
    """Henter og skriver én rettsakt. Returnerer metadata til veiviseren."""
    mappe = rot / akt["mappe"]
    sprak = akt.get("sprak", "EN")
    url = EURLEX.format(sprak=sprak, celex=akt["versjon"])
    # EUR-Lex svarer av og til med en ventside (AWS WAF) til automatiske oppslag. Da prøves
    # Publikasjonskontorets CELLAR-tjeneste, som er laget for maskinell henting av samme tekst.
    kilder = [url, CELLAR.format(celex=akt["versjon"])]
    data, problemer = {"artikler": []}, []
    for kilde in kilder:
        try:
            html = hent(kilde, ekstra={"Accept-Language": "eng" if sprak == "EN" else sprak.lower()}
                        if kilde.startswith(CELLAR[:30]) else None).decode("utf-8", errors="replace")
        except Exception as e:  # noqa: BLE001
            problemer.append(f"{kilde}: {e}")
            continue
        data = les_rettsakt(html)
        if data["artikler"]:
            url = kilde
            break
        problemer.append(f"{kilde}: ingen artikler ({len(html)} tegn)")
        time.sleep(5)
    time.sleep(3)
    if not data["artikler"]:
        tidligere = list(mappe.glob("art-*.md"))
        melding = f"{akt['navn']}: fikk ikke hentet teksten ({'; '.join(problemer)[:400]})"
        if tidligere:
            merknader.append(melding + ". Beholder teksten fra forrige bygg.")
            return {"akt": akt, "tittel": "", "oppforinger": eksisterende(mappe), "endringer": [], "nyere": [],
                    "url": url, "beholdt": True}
        feil.append(melding)
        return None

    for gammel in list(mappe.glob("art-*.md")) + list(mappe.glob("vedlegg-*.md")):
        gammel.unlink()
    mappe.mkdir(parents=True, exist_ok=True)
    kort = akt.get("kortnavn", akt["navn"])
    kildelinje = (
        f"**Kilde:** {akt['navn']} ({visningsnavn(nokkel_fra_celex(akt['celex']))}), "
        f"EUR-Lex {akt['versjon']}, språk {sprak}."
    )
    merknad = (
        "Dette er EU-tekst, ikke norsk lov- eller forskriftstekst. Hvilken versjon som gjelder i Norge, "
        f"avgjøres av EØS-avtalen og norsk gjennomføring: se `{akt['mappe']}/VEIVISER.md`."
    )
    oppforinger = []
    for a in data["artikler"]:
        fil = mappe / f"art-{filnavn(a['nr'])}.md"
        deler = [f"# {kort} artikkel {a['nr']}", ""]
        if a["undertittel"]:
            deler += [f"**{a['undertittel']}**", ""]
        deler += [kildelinje, "", merknad, "", "---", ""]
        deler += [s + "\n" for s in a["avsnitt"]]
        md = "\n".join(deler).rstrip() + "\n"
        fil.write_text(md, encoding="utf-8")
        d = dekning(a["kilde"], md)
        if d < MIN_DEKNING:
            feil.append(f"{fil.relative_to(rot)}: bare {d:.1%} av ordene i kilden er med")
        tittel = f"Artikkel {a['nr']}" + (f". {a['undertittel']}" if a["undertittel"] else "")
        oppforinger.append((a["kapittel"], tittel, fil))
    for v in data["vedlegg"]:
        fil = mappe / f"vedlegg-{filnavn(v['nr'])}.md"
        md = "\n".join([f"# {kort} vedlegg {v['nr']}", "", f"**{v['tittel']}**", "", kildelinje, "", merknad, "", "---", ""]
                       + [s + "\n" for s in v["avsnitt"]]).rstrip() + "\n"
        fil.write_text(md, encoding="utf-8")
        d = dekning(v["kilde"], md)
        if d < MIN_DEKNING:
            feil.append(f"{fil.relative_to(rot)}: bare {d:.1%} av ordene i kilden er med")
        oppforinger.append(("Vedlegg", f"Vedlegg {v['nr']}. {v['tittel']}", fil))

    nyere = []
    try:
        versjoner = konsoliderte_versjoner(akt["celex"])
        if akt["versjon"].startswith("0"):
            nyere = [v for v in versjoner if v > akt["versjon"]]
        else:
            nyere = versjoner
    except Exception as e:  # noqa: BLE001
        merknader.append(f"{akt['navn']}: kunne ikke sjekke nyere versjoner: {e}")
    return {"akt": akt, "tittel": data["tittel"], "oppforinger": oppforinger, "endringer": data["endringer"],
            "nyere": nyere, "url": url}


def eksisterende(mappe: Path) -> list:
    """Oppføringer for artikkelfiler fra et tidligere bygg, når teksten ikke kunne hentes på nytt."""
    ut = []
    for fil in sorted(mappe.glob("art-*.md"), key=lambda f: [int(x) if x.isdigit() else x for x in re.split(r"(\d+)", f.stem)]) + \
            sorted(mappe.glob("vedlegg-*.md")):
        linjer = fil.read_text(encoding="utf-8").splitlines()
        tittel = linjer[0].lstrip("# ") if linjer else fil.stem
        under = next((l.strip("*") for l in linjer[1:4] if l.startswith("**") and not l.startswith("**Kilde")), "")
        ut.append(("", f"{tittel}" + (f". {under}" if under else ""), fil))
    return ut


def veiviser_blokk(rot: Path, info: dict, norske: dict) -> str:
    akt = info["akt"]
    mappe = rot / akt["mappe"]
    linjer = ["## Kilder", ""]
    linjer.append(f"- **Rettsakt:** {info['tittel'] or akt['navn']}")
    linjer.append(f"- **Versjon i basen:** EUR-Lex {akt['versjon']}, språk {akt.get('sprak', 'EN')}")
    linjer.append(f"- **EØS:** {akt.get('eos') or 'Ikke kontrollert mot EØS-avtalen. Sjekk hvilken versjon som er tatt inn før teksten legges til grunn.'}")
    if info["nyere"]:
        vis = ", ".join(info["nyere"][:5]) + (" m.fl." if len(info["nyere"]) > 5 else "")
        if akt["versjon"].startswith("0"):
            linjer.append(f"- **Nyere EU-versjoner finnes:** {vis}. De kan inneholde endringer som ikke gjelder i Norge. "
                          "Versjonen i basen byttes bare når det er kontrollert hva som er tatt inn i EØS-avtalen.")
        else:
            linjer.append(f"- **Konsoliderte EU-versjoner finnes:** {vis}. Basen har originalteksten uten senere endringer.")
    if info["endringer"]:
        linjer += ["", "**Endringsmerker i teksten** (▼ foran et ledd viser hvilken rettsakt teksten kommer fra):", ""]
        linjer += [f"- {m}: {navn}" for m, navn in info["endringer"]]
    linjer += ["", "## Norske regler som viser til rettsakten", ""]
    treff = norske.get(nokkel_fra_celex(akt["celex"]), {})
    if treff:
        linjer.append("Stiene er fra roten av basen.")
        linjer.append("")
        for lovnavn, filer in sorted(treff.items()):
            vis = ", ".join(f"`{f}`" for f in filer[:12])
            if len(filer) > 12:
                vis += f" og {len(filer) - 12} til"
            linjer.append(f"- **{lovnavn}:** {vis}")
    else:
        linjer.append("Ingen lov- eller forskriftstekst i basen nevner rettsakten med nummer.")
    merknadsfiler = sorted((mappe / "merknader").glob("*.md")) if (mappe / "merknader").is_dir() else []
    if merknadsfiler:
        linjer += ["", "## Merknader", "", "Dette er ikke rettsaktstekst.", ""]
        linjer += [f"- `{f.relative_to(mappe).as_posix()}`" for f in merknadsfiler]
    rundskriv = sorted((mappe / "rundskriv").glob("*/oversikt.md")) if (mappe / "rundskriv").is_dir() else []
    if rundskriv:
        linjer += ["", "## Rundskriv", "", "Dette er ikke rettsaktstekst.", ""]
        for f in rundskriv:
            tittel = f.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
            linjer.append(f"- {tittel} – start med `{f.relative_to(mappe).as_posix()}`")
    linjer += ["", "## Innhold", ""]
    forrige = None
    for kap, tittel, fil in info["oppforinger"]:
        if kap != forrige:
            if kap:
                linjer += ["", f"**{kap}**", ""]
            forrige = kap
        linjer.append(f"- {tittel} – `{fil.relative_to(mappe).as_posix()}`")
    return "\n".join(linjer)
