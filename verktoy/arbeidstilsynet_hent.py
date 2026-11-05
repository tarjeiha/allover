#!/usr/bin/env python3
"""
Holder Arbeidstilsynets kommentarer til forskriftene i basen oppdatert fra arbeidstilsynet.no.

Bruk:
    python3 verktoy/arbeidstilsynet_hent.py           # hent nye og endrede kommentarer
    python3 verktoy/arbeidstilsynet_hent.py --tving   # hent alle på nytt

1. Leser sitemap.xml på arbeidstilsynet.no. Hver forskrift har en side under
   /regelverk/forskrifter/<navn>/, og alle sidene har dato for siste endring (lastmod).
2. Henter forskrifter som er nye eller har ny dato siden forrige gang
   (regelverk/arbeidstilsynet-kommentarer.tsv). Forskriften kobles til basen gjennom
   Lovdata-lenkene på siden: den forskriften i regelverk.json som det lenkes oftest til.
3. Tar bare med «Arbeidstilsynets kommentar» under hver paragraf, ikke forskriftsteksten,
   som kommer fra Lovdata. Kommentarene legges i
   regelverk/<lov>/rundskriv/arbeidstilsynet/<forskrift>/par-<nr>.md med oversikt.md.
   Filene skrives bare når teksten faktisk er endret.

Skriver arbeidstilsynet-rapport.txt (commit-melding og sammendrag) når noe er endret.
Arbeidstilsynet tillater automatisk henting (robots.txt). Skriptet henter én side om gangen med pause.
"""

import argparse
import datetime
import hashlib
import json
import re
import shutil
import sys
import time
import urllib.request
from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString

ROT = Path(__file__).resolve().parent.parent
BASE = "https://www.arbeidstilsynet.no"
STATUS = ROT / "regelverk" / "arbeidstilsynet-kommentarer.tsv"
RAPPORT = ROT / "arbeidstilsynet-rapport.txt"
UNDERMAPPE = "rundskriv/arbeidstilsynet"
UA = {"User-Agent": "regelverksbase/1.0 (+https://github.com/tarjeiha/allover)"}
PAUSE = 1.0
KOLONNER = ["side", "forskrift_id", "mappe", "lastmod", "kommentarer", "sjekksum", "lagt_inn"]


def hent(url: str) -> str:
    for forsok in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return r.read().decode("utf-8", "replace")
        except Exception:
            if forsok == 2:
                raise
            time.sleep(5 * (forsok + 1))


def forskrifter_i_basen() -> dict:
    """Lovdata-id (uten FOR-) -> (lov, forskrift) fra regelverk.json."""
    cfg = json.loads((ROT / "regelverk.json").read_text(encoding="utf-8"))
    ut = {}
    for lov in cfg["lover"]:
        for f in lov.get("forskrifter", []):
            ut[f["id"].removeprefix("FOR-")] = (lov, f)
    return ut


def sider_fra_sitemap() -> dict:
    """Forskriftsside -> nyeste lastmod blant sidene under den."""
    xml = hent(BASE + "/sitemap.xml")
    nyeste = {}
    for url, mod in re.findall(r"<url>\s*<loc>(.*?)</loc>\s*<lastmod>(.*?)</lastmod>", xml):
        m = re.match(re.escape(BASE) + r"/regelverk/forskrifter/([^/]+)/", url)
        if m:
            nyeste[m.group(1)] = max(nyeste.get(m.group(1), ""), mod)
    if not nyeste:
        raise RuntimeError("fant ingen forskrifter i sitemap.xml – har nettstedet endret oppbygning?")
    return nyeste


def les_status() -> dict:
    if not STATUS.exists():
        return {}
    linjer = STATUS.read_text(encoding="utf-8").splitlines()
    return {r["side"]: r for r in (dict(zip(KOLONNER, l.split("\t"))) for l in linjer[1:] if l)}


def skriv_status(status: dict) -> None:
    linjer = ["\t".join(KOLONNER)] + ["\t".join(status[s].get(k, "") for k in KOLONNER) for s in sorted(status)]
    STATUS.write_text("\n".join(linjer) + "\n", encoding="utf-8")


# --- HTML til Markdown --------------------------------------------------------------------

def tekst(el) -> str:
    """Innebygd tekst med lenker."""
    deler = []
    for barn in el.children:
        if isinstance(barn, NavigableString):
            deler.append(str(barn))
        elif barn.name == "a" and barn.get("href"):
            href = barn["href"]
            href = BASE + href if href.startswith("/") else href
            deler.append(f"[{barn.get_text(' ', strip=True)}]({href})")
        elif barn.name in ("strong", "b"):
            deler.append(f"**{tekst(barn).strip()}**")
        elif barn.name in ("em", "i"):
            deler.append(f"*{tekst(barn).strip()}*")
        elif barn.name == "br":
            deler.append("  \n")
        else:
            deler.append(tekst(barn))
    return re.sub(r"[ \t\r\n]+", " ", "".join(deler).replace("  \n", "\x00")).replace("\x00", "  \n")


def markdown(el) -> str:
    blokker = []

    def gå(node, innrykk=""):
        for barn in node.children:
            if isinstance(barn, NavigableString):
                if barn.strip():
                    blokker.append(barn.strip())
                continue
            navn = barn.name
            if navn in ("h2", "h3", "h4", "h5"):
                blokker.append("### " + barn.get_text(" ", strip=True))
            elif navn == "p":
                t = tekst(barn).strip()
                if t:
                    blokker.append(t)
            elif navn in ("ul", "ol"):
                linjer = []
                for i, li in enumerate(barn.find_all("li", recursive=False), 1):
                    merke = f"{i}." if navn == "ol" else "-"
                    linjer.append(f"{innrykk}{merke} {tekst(li).strip()}")
                blokker.append("\n".join(linjer))
            elif navn == "table":
                rader = [[tekst(c).strip().replace("|", "\\|") for c in tr.find_all(["th", "td"])]
                         for tr in barn.find_all("tr")]
                rader = [r for r in rader if r]
                if rader:
                    bredde = max(len(r) for r in rader)
                    rader = [r + [""] * (bredde - len(r)) for r in rader]
                    linjer = ["| " + " | ".join(rader[0]) + " |", "|" + "---|" * bredde]
                    linjer += ["| " + " | ".join(r) + " |" for r in rader[1:]]
                    blokker.append("\n".join(linjer))
            elif navn in ("script", "style", "button", "figure", "svg"):
                continue
            else:
                gå(barn, innrykk)

    gå(el)
    return "\n\n".join(b for b in blokker if b).strip()


# --- Lesing av forskriftssiden ------------------------------------------------------------

def les_side(side: str, i_basen: dict):
    """Returnerer (lov, forskrift, [(paragraf, overskrift, markdown)]) eller (None, None, []) ."""
    html = hent(f"{BASE}/regelverk/forskrifter/{side}/")
    ider = Counter(re.findall(r"lovdata\.no/forskrift/(\d{4}-\d{2}-\d{2}-\d+)", html))
    treff = [(n, i) for i, n in ider.items() if i in i_basen]
    if not treff:
        return None, None, []
    lov, forskrift = i_basen[max(treff)[1]]
    soup = BeautifulSoup(html, "lxml")
    kommentarer = []
    for blokk in soup.select("div.lawsandregulationslistpage__comments"):
        innhold = blokk.select_one("div.accordion-item__content")
        if innhold is None:
            continue
        paragraf = blokk.find_parent("div", class_="accordion__sub-chapter")
        knapp = paragraf.find("button") if paragraf else None
        overskrift = re.sub(r"\s+", " ", knapp.get_text(" ", strip=True)) if knapp else ""
        m = re.match(r"(§\s*[\d]+(?:-\d+)*\s*[a-z]?)\.?\s*(.*)", overskrift)
        if not m:
            continue
        nr = re.sub(r"\s+", " ", m.group(1)).strip()
        kommentarer.append((nr, m.group(2).strip().rstrip("."), markdown(innhold)))
    return lov, forskrift, kommentarer


def slug(nr: str) -> str:
    return "par-" + re.sub(r"[^0-9a-z]+", "-", nr.lower().replace("§", "")).strip("-")


def skriv_mappe(side: str, lov: dict, forskrift: dict, kommentarer: list, dato: str) -> Path:
    mappe = ROT / lov["mappe"] / UNDERMAPPE / forskrift["slug"]
    if mappe.exists():
        shutil.rmtree(mappe)
    mappe.mkdir(parents=True)
    url = f"{BASE}/regelverk/forskrifter/{side}/"
    tittel = f"Arbeidstilsynets kommentarer til {forskrift['navn'][0].lower()}{forskrift['navn'][1:]}"
    innhold = []
    for nr, overskrift, tekst_ in kommentarer:
        fil = mappe / f"{slug(nr)}.md"
        hode = "\n".join([
            "---",
            f'rundskriv: "{tittel}"',
            f'utgiver: "Arbeidstilsynet"',
            f'lov: "{lov["navn"]}"',
            f'forskrift: "{forskrift["navn"]}"',
            f'forskrift_id: "{forskrift["id"]}"',
            f'kilde: "{url}"',
            f'lagt_inn: "{dato}"',
            f'paragraf: "{nr}"',
            'gjelder: "forskrift"',
            "---",
        ])
        navn = f"{nr} {overskrift}".strip()
        fil.write_text(f"{hode}\n\n# Arbeidstilsynets kommentar til {forskrift['navn'][0].lower()}"
                       f"{forskrift['navn'][1:]} {navn}\n\n{tekst_}\n", encoding="utf-8")
        innhold.append(f"- {navn} – `{fil.name}`")
    (mappe / "oversikt.md").write_text(
        f"# {tittel}\n\n"
        f"Arbeidstilsynets kommentarer til {forskrift['navn']} ({forskrift['id']}), hentet fra "
        f"[arbeidstilsynet.no]({url}) {dato}. Kommentarene er Arbeidstilsynets veiledning, ikke "
        "forskriftstekst. Forskriftsteksten ligger under `forskrifter/` og kommer fra Lovdata.\n\n"
        "## Innhold\n\n" + "\n".join(innhold) + "\n", encoding="utf-8")
    return mappe


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tving", action="store_true", help="hent alle forskriftene på nytt")
    args = ap.parse_args()

    dato = datetime.date.today().isoformat()
    i_basen = forskrifter_i_basen()
    sider = sider_fra_sitemap()
    status = les_status()
    nye, endret, uendret = [], [], 0

    for side, lastmod in sorted(sider.items()):
        gammel = status.get(side)
        if gammel and gammel.get("lastmod") == lastmod and not args.tving:
            continue
        time.sleep(PAUSE)
        lov, forskrift, kommentarer = les_side(side, i_basen)
        rad = {"side": side, "lastmod": lastmod, "kommentarer": str(len(kommentarer))}
        if lov is None or not kommentarer:
            # Ikke i basen, eller uten kommentarer: noter datoen så siden ikke hentes hver uke.
            status[side] = {**rad, "forskrift_id": forskrift["id"] if forskrift else "",
                            "mappe": "", "sjekksum": "", "lagt_inn": ""}
            continue
        sjekksum = hashlib.sha256(json.dumps(kommentarer, ensure_ascii=False).encode()).hexdigest()[:16]
        mappe = f"{lov['mappe']}/{UNDERMAPPE}/{forskrift['slug']}"
        if gammel and gammel.get("sjekksum") == sjekksum and (ROT / mappe).exists() and not args.tving:
            status[side] = {**gammel, **rad}
            uendret += 1
            continue
        skriv_mappe(side, lov, forskrift, kommentarer, dato)
        status[side] = {**rad, "forskrift_id": forskrift["id"], "mappe": mappe,
                        "sjekksum": sjekksum, "lagt_inn": dato}
        (endret if gammel and gammel.get("mappe") else nye).append(
            f"{forskrift['navn']} ({len(kommentarer)} paragrafer med kommentar)")

    skriv_status(status)
    print(f"Nye: {len(nye)}, endret: {len(endret)}, uendret tekst: {uendret}")
    for linje in nye:
        print("  ny:", linje)
    for linje in endret:
        print("  endret:", linje)
    if nye or endret:
        melding = [f"Arbeidstilsynets kommentarer: {len(nye)} nye, {len(endret)} oppdatert", ""]
        melding += [f"- Ny: {l}" for l in nye] + [f"- Oppdatert: {l}" for l in endret]
        RAPPORT.write_text("\n".join(melding) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
