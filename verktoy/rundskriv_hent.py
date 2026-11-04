#!/usr/bin/env python3
"""
Holder Navs rundskriv i basen oppdatert fra Lovdata (Nav rettskilder, lovdata.no/nav).

Bruk:
    python3 verktoy/rundskriv_hent.py            # hent nye og endrede rundskriv
    python3 verktoy/rundskriv_hent.py r08-00     # hent bestemte rundskriv uansett dato
    python3 verktoy/rundskriv_hent.py --tving    # hent alle på nytt

1. Finner rundskrivene: lenkene til /nav/rundskriv/<kode> på kapittelsidene til folketrygdloven,
   sidene under «andre rettskilder» og endringsloggen.
2. Tar med rundskriv med hovednummer som hører til en lov i basen (HOVEDNR under). R45 har
   egen jobb (r45.py). Rundskriv til lover som ikke er i basen, hoppes over.
3. Leser «Sist endret» på hver side og sammenligner med regelverk/nav-rundskriv.tsv.
   Er rundskrivet nytt eller endret, legges det inn med innboksens kode (rundskriv.py), i
   regelverk/<lov>/rundskriv/rundskriv-<kode>/ eller under forskriftskommentarene.
4. Erstatter et rundskriv en eldre, håndhentet mappe (GAMLE_MAPPER), slettes den gamle mappen
   når det nye er lagt inn. Feiler innleggingen, beholdes den gamle.

Skriver nav-rundskriv-rapport.txt (commit-melding og sammendrag) når noe er endret.
Lovdata publiserer Navs rundskriv åpent. Skriptet henter én side om gangen med pause.
"""

import datetime
import json
import re
import shutil
import sys
import tempfile
import time
import urllib.parse
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).parent))
import rundskriv as innboks  # noqa: E402

ROT = Path(__file__).resolve().parent.parent
STATUS = ROT / "regelverk" / "nav-rundskriv.tsv"
RAPPORT = ROT / "nav-rundskriv-rapport.txt"
LOVDATA = "https://lovdata.no"
URL = LOVDATA + "/nav/rundskriv/{}"
PAUSE = 1.5

# Navs hovednummer -> lovmappe i basen. Hovednummer 1-26 følger folketrygdlovens kapitler.
HOVEDNR = {**{n: "regelverk/folketrygdloven" for n in range(1, 27)},
           30: "regelverk/nav-loven", 36: "regelverk/forvaltningsloven",
           37: "regelverk/permitteringslonnsloven", 62: "regelverk/afp-loven",
           67: "regelverk/lonnsgarantiloven", 76: "regelverk/arbeidsmarkedsloven",
           80: "regelverk/samordningsloven", 83: "regelverk/personopplysningsloven"}
EGEN_JOBB = {"r45-00"}

# Filer og mapper som ble hentet for hånd før denne jobben fantes (mønstre relativt til roten).
# De slettes når rundskrivet er lagt inn på nytt. Feiler innleggingen, legges de tilbake.
_F = "regelverk/folketrygdloven/rundskriv/"
_K = _F + "ftrl/"
GAMLE_MAPPER = {
    "r04-00": [_K + "kap-4"], "r08-00": [_K + "kap-8"], "r09-00": [_K + "kap-9"],
    "r11-00": [_K + "kap-11"], "r11a-00": [_K + "kap-11a"], "r12-00": [_K + "kap-12"],
    "r06-00": [_K + "kap-6/*.md"], "r06-04-for": [_K + "kap-6/retningslinjer-diagnoser"],
    "r10-00": [_K + "kap-10/*.md"],
    "r10-07": [_K + "kap-10/paragraf-10-7/generelt-reiseutgifter"],
    "r10-07-4-5-ledd": [_K + "kap-10/paragraf-10-7/fjerde-femte-ledd"],
    "r10-07acd": [_K + "kap-10/paragraf-10-7/hjelpemidler-arbeid-dagligliv-acd"],
    "r10-07a": [_F + "forskrifter/aktivitetshjelpemidler-over-26"],
    "r10-07b": [_F + "forskrifter/horeapparat-tinnitusmaskerer"],
    "r10-07e": [_F + "forskrifter/lese-sekretarhjelp-blinde-svaksynte"],
    "r10-07f": [_F + "forskrifter/tolkehjelp-horselshemmede"],
    "r10-07g": [_F + "forskrifter/tolke-ledsagerhjelp-dovblinde"],
    "r10-07h": [_F + "forskrifter/anskaffelse-motorkjoretoy"],
    "r10-07i": [_F + "forskrifter/ortopediske-hjelpemidler-proteser-parykk"],
    "r10-07-for": [_F + "forskrifter/servicehund"],
    "r11a-00-for": [_F + "forskrifter/tilleggsstonadsforskriften"],
    "r12-00-for": [_F + "forskrifter/omregning-uforepensjon-til-uforetrygd"],
    "r12-13-for": [_F + "forskrifter/okt-beregningsgrunnlag-gift-samboende"],
    "r12-14-for": [_F + "forskrifter/uforetrygdforskriften-kap7"],
    "r12-15-for": [_F + "forskrifter/overgangsregler-barnetillegg-uforetrygd-2015"],
    "r12-19-for-1375": [_F + "forskrifter/uredusert-ytelse-institusjon"],
    "r12-19-for-1376": [_F + "forskrifter/beregning-uforetrygd-institusjon"],
}


def hent(url: str):
    req = urllib.request.Request(urllib.parse.quote(url, safe=":/?=&%#"),
                                 headers={"User-Agent": "Mozilla/5.0 (regelverksbasen; tarjeiha/allover)"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:  # noqa: BLE001
        print(f"{url}: feil {e}")
        return None
    finally:
        time.sleep(PAUSE)


def er_rundskriv(html: str) -> bool:
    m = re.search(r"<title>([^<]*)", html)
    return bool(m) and bool(re.search(r"rundskriv|kommentar", m.group(1), re.I))


def rens(html: str) -> str:
    """Beholder bare selve rundskrivet: fjerner meny, skript og kapitteloversikt, og pakker ut div-ene
    slik at overskriftene blir overskrifter også etter konvertering til Markdown."""
    s = BeautifulSoup(html, "lxml")
    tittel = s.title.get_text(strip=True) if s.title else "Rundskriv"
    tittel = re.sub(r"\s*-\s*Lovdata$", "", tittel)
    innhold = s.find(id="ToContent")
    if innhold is None:
        raise ValueError("fant ikke innholdet på siden")
    for t in innhold.find_all(["script", "style", "nav", "header", "footer", "form", "button", "noscript"]):
        t.decompose()
    # Kapitteloversikten er en lenkeliste rett etter overskriften «Kapitteloversikt»
    for h in innhold.find_all(re.compile("^h[1-6]$")):
        if h.get_text(strip=True) == "Kapitteloversikt":
            nxt = h.find_next_sibling()
            if nxt is not None and nxt.name == "ul":
                nxt.decompose()
            h.decompose()
    # Metatabellen øverst (myndighet, dato, dokumentnummer, sist endret) blir vanlige linjer
    for tabell in innhold.find_all("table"):
        etiketter = tabell.find_all("th", class_="metafieldLabel")
        if not etiketter:
            continue
        ny = s.new_tag("p")
        for rad in tabell.find_all("tr"):
            th, td = rad.find("th"), rad.find("td")
            if th and td and td.get_text(strip=True):
                ny.append(f"{th.get_text(strip=True)}: {td.get_text(' ', strip=True)}")
                ny.append(s.new_tag("br"))
        tabell.replace_with(ny)
    # Lenker og uthevinger i overskrifter fjernes, så «§ 7-2» står først i overskriften
    for h in innhold.find_all(re.compile("^h[1-6]$")):
        for t in h.find_all(["a", "em", "i", "strong", "b", "span"]):
            t.unwrap()
    for t in innhold.find_all(True):
        if t.name == "a":
            href = t.get("href", "")
            if not href or href.startswith("#"):
                t.unwrap()
                continue
        t.attrs = {k: v for k, v in t.attrs.items() if k == "href" and t.name == "a"}
        if t.name == "a" and t.get("href", "").startswith("/"):
            t["href"] = "https://lovdata.no" + t["href"]
    for t in innhold.find_all(["div", "span", "section", "article"]):
        t.unwrap()
    return (
        "<!DOCTYPE html><html><head><meta charset=\"utf-8\"><title>"
        + tittel
        + "</title></head><body>"
        + innhold.decode_contents()
        + "</body></html>"
    )


def hovednr(kode: str):
    m = re.match(r"r(\d{2})(?:[a-z]\b|[a-z]?-)", kode)
    return int(m.group(1)) if m else None


def lovmappe(kode: str):
    if kode in EGEN_JOBB or not kode.startswith("r"):
        return None
    return HOVEDNR.get(hovednr(kode))


def finn_koder() -> set:
    """Alle rundskrivkoder som Lovdata lenker til fra Nav rettskilder."""
    forside = hent(LOVDATA + "/nav") or ""
    andre = sorted(set(re.findall(r'href="(/nav/andre-rettskilder/[^"#]+)"', forside)))
    sider = [f"/nav/folketrygdloven/kap{n}" for n in [*range(1, 27), "11a"]] + andre + ["/nav/endringer"]
    koder = set()
    for s in sider:
        html = hent(LOVDATA + s) or ""
        koder |= {k.lower() for k in re.findall(r"/nav/rundskriv/([A-Za-z0-9\-]+)", html)}
    if len(koder) < 50:
        raise SystemExit(f"Fant bare {len(koder)} rundskriv hos Lovdata. Har sidene endret seg?")
    return koder


def sist_endret(html: str) -> str:
    s = BeautifulSoup(html, "lxml")
    for rad in s.find_all("tr"):
        th, td = rad.find("th"), rad.find("td")
        if th and td and th.get_text(strip=True).lower() == "sist endret":
            m = re.search(r"\d{4}-\d{2}-\d{2}", td.get_text(" ", strip=True))
            if m:
                return m.group(0)
    return ""


def les_status() -> dict:
    if not STATUS.exists():
        return {}
    rader = [l.split("\t") for l in STATUS.read_text(encoding="utf-8").splitlines()[1:] if l.strip()]
    return {r[0]: {"lov": r[1], "sist_endret": r[2], "hentet": r[3], "mappe": r[4] if len(r) > 4 else ""} for r in rader}


def skriv_status(status: dict) -> None:
    linjer = ["kode\tlov\tsist_endret\thentet\tmappe"]
    linjer += [f"{k}\t{v['lov']}\t{v['sist_endret']}\t{v['hentet']}\t{v['mappe']}" for k, v in sorted(status.items())]
    STATUS.write_text("\n".join(linjer) + "\n", encoding="utf-8")


def legg_inn(kode: str, mappe: str, html: str, lover: list, dato: str) -> str:
    """Legger inn ett rundskriv med innboksens kode. Returnerer stien til mappen det havnet i."""
    lov = Path(mappe).name
    gamle = [g for m in GAMLE_MAPPER.get(kode, []) for g in sorted(ROT.glob(m))]
    with tempfile.TemporaryDirectory() as tmp:
        fil = Path(tmp) / f"{lov}-rundskriv-{kode}.html"
        fil.write_text(rens(html), encoding="utf-8")
        sikkerhet = Path(tmp) / "gammel"
        for g in gamle:
            mål = sikkerhet / g.relative_to(ROT)
            mål.parent.mkdir(parents=True, exist_ok=True)
            (shutil.copytree if g.is_dir() else shutil.copy2)(g, mål)
            shutil.rmtree(g) if g.is_dir() else g.unlink()
        try:
            svar = innboks.legg_inn(fil, lover, dato)
        except Exception:
            for g in gamle:
                kilde = sikkerhet / g.relative_to(ROT)
                g.parent.mkdir(parents=True, exist_ok=True)
                (shutil.copytree if kilde.is_dir() else shutil.copy2)(kilde, g)
            raise
    m = re.search(r"-> (\S+)/ ", svar)
    return m.group(1) if m else ""


def main() -> int:
    args = [a.lower() for a in sys.argv[1:]]
    tving = "--tving" in args
    valgte = {a for a in args if not a.startswith("--")}
    config = json.loads((ROT / "regelverk.json").read_text(encoding="utf-8"))
    lover = config["lover"]
    i_basen = {l["mappe"] for l in lover}
    dato = datetime.date.today().isoformat()
    status = les_status()
    koder = valgte or finn_koder()
    aktuelle = sorted(k for k in koder if lovmappe(k) in i_basen)
    print(f"{len(koder)} koder hos Lovdata, {len(aktuelle)} rundskriv til lover i basen")
    nye, endret, stoppet = [], [], []
    for kode in aktuelle:
        html = hent(URL.format(kode))
        if not html or not er_rundskriv(html):
            stoppet.append(f"{kode}: fant ikke rundskrivet hos Lovdata")
            continue
        dato_lovdata = sist_endret(html)
        før = status.get(kode)
        if før and før["sist_endret"] == dato_lovdata and not tving and kode not in valgte:
            continue
        try:
            mappe = legg_inn(kode, lovmappe(kode), html, lover, dato)
        except Exception as e:  # noqa: BLE001 – ett rundskriv som feiler skal ikke stoppe de andre
            stoppet.append(f"{kode}: {e}")
            continue
        status[kode] = {"lov": Path(lovmappe(kode)).name, "sist_endret": dato_lovdata, "hentet": dato, "mappe": mappe}
        tittel = re.sub(r"\s*-\s*Lovdata$", "", re.search(r"<title>([^<]*)", html).group(1).strip())
        (endret if før else nye).append(f"{kode.upper()} – {tittel} (sist endret {dato_lovdata or 'ukjent'}) -> {mappe}/")
        print(f"{kode}: lagt inn i {mappe}/")
        skriv_status(status)
    skriv_status(status)
    if nye or endret or stoppet:
        linjer = [f"Navs rundskriv fra Lovdata: {len(nye)} nye, {len(endret)} oppdatert, {len(stoppet)} stoppet", ""]
        for navn, liste in (("Nye", nye), ("Oppdatert", endret), ("Stoppet", stoppet)):
            if liste:
                linjer += [f"{navn}:", *[f"- {x}" for x in liste], ""]
        RAPPORT.write_text("\n".join(linjer), encoding="utf-8")
        print("\n".join(linjer))
    else:
        print("Ingen endringer.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
