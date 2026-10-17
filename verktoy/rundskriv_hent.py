#!/usr/bin/env python3
"""
Henter NAVs rundskriv til folketrygdloven fra Lovdata og legger HTML-filene i innboks/.

Bruk:
    python3 verktoy/rundskriv_hent.py [r13-00 r14-00 ...]

Uten argumenter hentes rundskrivene R01-00 til R25-00 som ikke allerede ligger i basen
(kapittel 4, 6, 8, 9, 10, 11 og 12 ligger inne fra før), pluss tilleggsdeler (R03-01, R03-02 ...).
Selve innlegginga gjør verktoy/rundskriv.py.

Lovdata publiserer Navs rundskriv åpent på lovdata.no/nav/rundskriv/. Skriptet henter én side
om gangen med pause mellom hver, og er ment å kjøres manuelt, ikke etter tidsplan.
"""

import re
import sys
import time
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup

ROT = Path(__file__).resolve().parent.parent
INNBOKS = ROT / "innboks"
URL = "https://lovdata.no/nav/rundskriv/{}"
FINNES_FRA_FØR = {4, 6, 8, 9, 10, 11, 12}
PAUSE = 2.0


def hent(kode: str):
    req = urllib.request.Request(URL.format(kode), headers={"User-Agent": "Mozilla/5.0 (regelverksbasen; tarjeiha/allover)"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:  # noqa: BLE001
        print(f"{kode}: feil {e}")
        return None


def er_rundskriv(html: str) -> bool:
    m = re.search(r"<title>([^<]*)", html)
    return bool(m) and m.group(1).strip().lower().startswith("rundskriv")


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


def lagre(kode: str, html: str) -> None:
    INNBOKS.mkdir(exist_ok=True)
    html = rens(html)
    (INNBOKS / f"folketrygdloven-rundskriv-{kode}.html").write_text(html, encoding="utf-8")


def main() -> int:
    koder = [a.lower() for a in sys.argv[1:]]
    if not koder:
        for kap in range(1, 26):
            if kap in FINNES_FRA_FØR:
                continue
            koder.append(f"r{kap:02d}-00")
    antall = 0
    for kode in koder:
        deler = [kode]
        # tilleggsdeler (-01, -02 ...) hentes når grunnrundskrivet er hentet
        if kode.endswith("-00"):
            deler += [f"{kode[:-3]}-{n:02d}" for n in range(1, 10)]
        for d in deler:
            html = hent(d)
            time.sleep(PAUSE)
            if html is None or not er_rundskriv(html):
                if d.endswith("-00"):
                    print(f"{d}: ikke funnet")
                else:
                    break
                continue
            lagre(d, html)
            antall += 1
            print(f"{d}: lagret {re.search(r'<title>([^<]*)', html).group(1).strip()}")
    print(f"{antall} rundskriv lagt i innboks/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
