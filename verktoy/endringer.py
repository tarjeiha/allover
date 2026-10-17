"""
Vedtatte endringer som ikke er i kraft, hentet fra Norsk Lovtidend avd. I.

Lovdatas åpne datasett har Lovtidend med alle kunngjorte endringslover og
endringsforskrifter. Hver endring er merket med hvilket dokument og hvilken
paragraf den gjelder (data-change-part o.l.), og med ny ordlyd.

En endring regnes som tatt inn når den gjeldende teksten viser til endringsakten
(lenke i «Endret ved» under paragrafen, eller i dokumenthodet når endringen ikke
gjelder en bestemt paragraf). Det som ikke er tatt inn, varsles i paragraffilen,
i veiviseren og i en egen fil per endringsakt under <mappe>/vedtatte-endringer/.

For å unngå støy fra gamle endringer som aldri ble lenket i gjeldende tekst, tas
en endringsakt med fast ikrafttredelsesdato bare med når datoen er i framtiden
eller mindre enn GRENSE_DAGER siden. «Kongen bestemmer» tas med til et
ikraftsettingsvedtak finnes, og da etter samme regel som faste datoer.
"""

import json
import re
import shutil
import tarfile
import urllib.request
import zlib
from datetime import date, timedelta
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString

from parse_lovdata import clean, render_blandet, render_list, render_tabell, slug_paragraf

LISTE = "https://api.lovdata.no/v1/publicData/list"
API = "https://api.lovdata.no/v1/publicData/get/"
GRENSE_DAGER = 90
MAPPE = "vedtatte-endringer"

DATO = re.compile(r"\d{4}-\d{2}-\d{2}")
ENDRER = re.compile(r'<dd class="changesToDocuments"[^>]*>(.*?)</dd>', re.S)
TITTEL = re.compile(r'<dd class="title"[^>]*>(.*?)</dd>', re.S)
LI = re.compile(r"<li[^>]*>\s*([^<\s]+)")
MAANED = {m: i + 1 for i, m in enumerate(
    ["januar", "februar", "mars", "april", "mai", "juni", "juli", "august",
     "september", "oktober", "november", "desember"])}
AKTNAVN = re.compile(r"\b(lov|forskrift)\s+(\d{1,2})\.\s*([a-zæøå]+)\s+(\d{4})\s+nr\.\s*(\d+)", re.I)


def last_ned(mappe: Path) -> list:
    """Laster ned alle Lovtidend avd. I-datasettene og returnerer filstiene."""
    mappe.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(LISTE, timeout=60) as r:
        navn = [d["filename"] for d in json.load(r) if d["filename"].startswith("lovtidend-avd1")]
    filer = []
    for n in sorted(navn):
        fil = mappe / n
        if not fil.exists():
            print(f"Laster ned {n}")
            with urllib.request.urlopen(API + n, timeout=600) as r, open(fil, "wb") as f:
                shutil.copyfileobj(r, f)
        filer.append(fil)
    return filer


def _dokumenter(filer: list):
    """(navn, rå tekst) for hvert dokument i tar-filene, uten å pakke ut på disk."""
    for fil in filer:
        with tarfile.open(fil, "r:bz2") as tar:
            for m in tar:
                if m.isfile() and m.name.endswith((".xml", ".html")):
                    yield m.name, tar.extractfile(m).read().decode("utf-8", "replace")


def _aktref(tekst: str) -> list:
    """«lov 22. desember 2025 nr. 115» -> ['lov/2025-12-22-115']"""
    ut = []
    for typ, dag, mnd, aar, nr in AKTNAVN.findall(tekst):
        if mnd.lower() in MAANED:
            ut.append(f"{typ.lower()}/{aar}-{MAANED[mnd.lower()]:02d}-{int(dag):02d}-{nr}")
    return ut


def _dd(soup, cls: str) -> str:
    dd = soup.find("dd", class_=cls)
    return clean(dd.get_text(" ", strip=True)) if dd else ""


def _del(change) -> str:
    for k, v in change.attrs.items():
        if k.startswith("data-") and k.endswith("-part"):
            return v.split(";;")[0]
    return ""


def _paragraf(delsti: str) -> str:
    """'lov/1999-07-02-64/§21/ledd/1' -> '21'. Tom streng når endringen ikke gjelder en paragraf."""
    m = re.search(r"/(§[^/]+)", delsti)
    return slug_paragraf(m.group(1)) if m else ""


def _render(node) -> list:
    """Endringen som Markdown-linjer: instruks («§ 21 skal lyde:») og ny tekst."""
    ut = []
    for c in node.children:
        if isinstance(c, NavigableString):
            if clean(str(c)):
                ut += [clean(str(c)), ""]
            continue
        cls = c.get("class") or []
        if "futuretitle" in cls:
            ut += [f"**{clean(c.get_text(' '))}**", ""]
        elif "futureLegalArticle" in cls or "legalArticle" in cls:
            hode = c.find(class_=re.compile("LegalArticleHeader|legalArticleHeader"), recursive=False)
            if hode:
                ut += [f"**{re.sub(r'\s+([.,])', r'\1', clean(hode.get_text(' ')))}**", ""]
                hode.extract()
            ut += _render(c)
        elif c.name in ("ol", "ul"):
            ut += render_list(c) + [""]
        elif c.name == "table":
            ut += render_tabell(c)
        else:
            for avsnitt in render_blandet(c):
                ut += avsnitt + [""]
    return ut


def _henvisninger(sti: Path) -> tuple:
    """Lenker til endringsakter i gjeldende tekst: (per paragraf-slug, hele dokumentet)."""
    soup = BeautifulSoup(sti.read_text(encoding="utf-8"), "lxml")

    def hrefs(node):
        return {a["href"].split("#")[0] for a in node.find_all("a", href=True)}

    per_par = {}
    for art in soup.find_all("article", class_="legalArticle"):
        s = slug_paragraf(art.get("data-name"))
        sett = per_par.setdefault(s, set())
        for c in art.find_all("article", class_="changesToParent", recursive=False):
            sett |= hrefs(c)
    alle = set()
    for c in soup.find_all("article", class_="changesToParent"):
        alle |= hrefs(c)
    hode = soup.find("header")
    if hode:
        alle |= hrefs(hode)
    return per_par, alle


def _status(akt: dict, vedtak: list, idag: date) -> str | None:
    """Tekst om ikrafttredelse, eller None når akten er for gammel til å tas med."""
    grense = idag - timedelta(days=GRENSE_DAGER)
    datoer = [date.fromisoformat(d) for d in DATO.findall(akt["ikraft"])]
    kongen = "Kongen bestemmer" in akt["ikraft"] or not datoer
    if not kongen:
        if max(datoer) < grense:
            return None
        return _datotekst(datoer, idag)
    if not vedtak:
        return "Ikrafttredelse: Kongen bestemmer, og tidspunktet er ikke fastsatt i Lovtidend ennå."
    vdatoer = [date.fromisoformat(d) for v in vedtak for d in DATO.findall(v["ikraft"])]
    delt = any("delt" in v["tittel"].lower() for v in vedtak)
    if vdatoer and max(vdatoer) < grense and not delt:
        return None
    linjer = ["Ikrafttredelse: Kongen bestemmer."]
    for v in vedtak:
        linjer.append(f"Satt i kraft ved {v['id']} ({v['tittel']}): {v['ikraft'] or 'dato ikke oppgitt'}.")
    if delt:
        linjer.append("Bare deler av endringene er satt i kraft. Sjekk vedtaket for hvilke deler som gjelder.")
    return " ".join(linjer)


def _datotekst(datoer: list, idag: date) -> str:
    vis = ", ".join(d.isoformat() for d in sorted(set(datoer)))
    if min(datoer) > idag:
        return f"Trer i kraft {vis}."
    if max(datoer) <= idag:
        return f"Trådte i kraft {vis}, men er ikke tatt inn i teksten i basen ennå."
    return f"I kraft fra {vis} (ulike deler til ulik tid). Deler som er i kraft, er ikke tatt inn i teksten i basen ennå."


def finn_ventende(filer: list, maal: dict, idag: date) -> dict:
    """
    maal: refid ('lov/1988-04-29-21') -> sti til gjeldende dokument.
    Returnerer refid -> liste av akter med endringer som ikke er tatt inn.
    """
    print(f"Lovtidend: ser etter endringer i {len(maal)} dokumenter")
    if not maal:
        raise ValueError("fant ikke DokumentID i noen av dokumentene i basen")
    kandidater = []
    vedtak_for: dict = {}
    for navn, raa in _dokumenter(filer):
        tittel = TITTEL.search(raa)
        tittel = clean(re.sub(r"<[^>]+>", " ", tittel.group(1))) if tittel else ""
        if re.search(r"ikraftsetting|ikrafttredelse|i kraft", tittel, re.I):
            soup = BeautifulSoup(raa.split("</header>")[0], "lxml")
            v = {"id": _dd(soup, "legacyID"), "tittel": tittel, "ikraft": _dd(soup, "dateInForce")}
            for ref in _aktref(tittel + " " + _dd(soup, "miscInformation")):
                vedtak_for.setdefault(ref, []).append(v)
        endrer = ENDRER.search(raa)
        if endrer and any(r in maal for r in LI.findall(endrer.group(1))):
            kandidater.append(zlib.compress(raa.encode("utf-8")))
    print(f"Lovtidend: {len(kandidater)} endringsakter berører regelverk i basen")
    sjekket = 0

    henv = {}
    ut: dict = {}
    for pakket in kandidater:
        raa = zlib.decompress(pakket).decode("utf-8")
        # Hodet først: de fleste aktene er i kraft for lenge siden og trenger ikke parses helt
        soup = BeautifulSoup(raa.split("</header>", 1)[0], "lxml")
        akt = {
            "ref": _dd(soup, "refid"), "id": _dd(soup, "legacyID"), "tittel": _dd(soup, "title"),
            "korttittel": _dd(soup, "titleShort"), "ikraft": _dd(soup, "dateInForce"),
            "kunngjort": _dd(soup, "dateOfPublication")[:10], "annet": _dd(soup, "miscInformation"),
            "dokid": _dd(soup, "dokid"),
        }
        status = _status(akt, vedtak_for.get(akt["ref"], []), idag)
        if status is None:
            continue
        sjekket += 1
        soup = BeautifulSoup(raa, "lxml")
        for dc in soup.find_all("article", class_="document-change"):
            mref = dc.get("data-document", "")
            if mref not in maal:
                continue
            if mref not in henv:
                henv[mref] = _henvisninger(maal[mref])
            per_par, alle = henv[mref]
            endringer = []
            for ch in dc.find_all("article", class_="change"):
                par = _paragraf(_del(ch))
                if par and par in per_par:
                    tatt_inn = akt["ref"] in per_par[par]
                else:
                    tatt_inn = akt["ref"] in alle
                if not tatt_inn:
                    endringer.append({"paragraf": par, "linjer": _render(ch)})
            if not dc.find("article", class_="change") and akt["ref"] not in alle:
                endringer.append({"paragraf": "", "linjer": _render(dc)})
            if endringer:
                ut.setdefault(mref, []).append(dict(akt, status=status, endringer=endringer))
    print(f"Lovtidend: {sjekket} kan være ikke i kraft, {sum(len(v) for v in ut.values())} med endringer som ikke er tatt inn")
    return ut


def filnavn(akt: dict) -> str:
    return re.sub(r"[^\w-]+", "-", akt["id"].lower()) + ".md"


def lovdata_url(akt: dict) -> str:
    return f"https://lovdata.no/dokument/{akt['dokid']}" if akt["dokid"] else "https://lovdata.no"


def skriv(rot: Path, mappe: Path, dokumenter: list, ventende: dict, indeks: list, lovnavn: str) -> list:
    """
    dokumenter: [(refid, navn, mappe for paragraffilene)] for loven og forskriftene i mappen.
    Skriver filene under <mappe>/vedtatte-endringer/, setter varsel i paragraffilene og
    returnerer avsnittet til veiviseren.
    """
    utmappe = mappe / MAPPE
    if utmappe.exists():
        shutil.rmtree(utmappe)
    akter: dict = {}
    for ref, navn, parmappe in dokumenter:
        for akt in ventende.get(ref, []):
            akter.setdefault(akt["ref"], (akt, []))[1].append((navn, parmappe, akt["endringer"]))

    ut = ["## Vedtatte endringer som ikke er i kraft", ""]
    if not akter:
        return ut + ["Ingen funnet i Norsk Lovtidend for regelverket i denne mappen.", ""]
    ut += ["Fra Norsk Lovtidend. Teksten i paragraffilene er gjeldende tekst; ny ordlyd står i filene under.", ""]
    utmappe.mkdir(parents=True)
    for akt, deler in akter.values():
        fil = utmappe / filnavn(akt)
        rel = fil.relative_to(rot).as_posix()
        linjer = [
            f"# {akt['tittel']}", "",
            f"**Kilde:** Norsk Lovtidend avd. I, {akt['id']}, kunngjort {akt['kunngjort']}. {lovdata_url(akt)}", "",
            f"**{akt['status']}**", "",
        ]
        if akt["annet"]:
            linjer += [f"**Om vedtaket:** {akt['annet']}", ""]
        linjer += ["Dette er vedtatt tekst som ikke er tatt inn i gjeldende tekst i basen. "
                   "Bare endringer i regelverk i denne mappen er tatt med.", ""]
        berort = []
        for navn, parmappe, endringer in deler:
            linjer += [f"## Endringer i {navn}", ""]
            for e in endringer:
                linjer += e["linjer"]
                pf = parmappe / f"par-{e['paragraf']}.md" if e["paragraf"] else None
                if pf and pf.exists():
                    _varsle(pf, akt, rel)
                    berort.append(f"§ {e['paragraf']}")
                elif e["paragraf"]:
                    berort.append(f"§ {e['paragraf']} (ny)")
            if not any(e["paragraf"] for e in endringer):
                berort.append(navn)
        fil.write_text("\n".join(linjer).rstrip() + "\n", encoding="utf-8")
        unike = list(dict.fromkeys(berort))
        vis = ", ".join(unike[:15]) + (f" og {len(unike) - 15} til" if len(unike) > 15 else "")
        ut.append(f"- **{akt['korttittel'] or akt['tittel']}** ({akt['id']}). {akt['status']} "
                  f"Endrer: {vis}. Ny tekst: `{fil.relative_to(mappe).as_posix()}`")
        indeks.append(f"{lovnavn}\tVedtatt endring, ikke i kraft\t{akt['tittel']}\t{rel}")
    return ut + [""]


def _varsle(pf: Path, akt: dict, rel: str) -> None:
    """Varsel rett under kildelinjen i paragraffilen. Filen bygges på nytt hver gang."""
    tekst = pf.read_text(encoding="utf-8")
    varsel = (f"> **Vedtatt endring, ikke i kraft:** {akt['korttittel'] or akt['tittel']} ({akt['id']}). "
              f"{akt['status']} Ny ordlyd: `{rel}`")
    if varsel in tekst:
        return
    linjer = tekst.split("\n")
    i = next((n for n, l in enumerate(linjer) if l.startswith("**Kilde:**")), 0)
    linjer[i + 1:i + 1] = ["", varsel]
    pf.write_text("\n".join(linjer), encoding="utf-8")
