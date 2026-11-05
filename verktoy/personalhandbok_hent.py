#!/usr/bin/env python3
"""
Holder Statens personalhåndbok i basen oppdatert fra Lovdata (lovdata.no/dokument/SPH/sph).

Bruk:
    python3 verktoy/personalhandbok_hent.py           # hent og skriv punkter som er endret
    python3 verktoy/personalhandbok_hent.py --tving   # skriv alle punktene på nytt

1. Går gjennom håndboka side for side fra kapittel 1, med lenken «Neste side» nederst på
   hver side. Lovdata deler håndboka i om lag 100 sider.
2. Deler teksten i punkter på nivå to (f.eks. 10.1), med underpunktene som overskrifter i
   filen. Innledningen til hvert kapittel får egen fil (punkt-10.md).
3. Lovdata oppgir ikke når et punkt sist ble endret, så endringer finnes med sjekksum av
   teksten (regelverk/personalhandboka.tsv). Filer skrives bare når teksten er endret, og
   punkter som er borte fra håndboka, slettes.

Filene legges i regelverk/statsansatteloven/rundskriv/personalhandboka/ med oversikt.md.
Skriver personalhandbok-rapport.txt (commit-melding og sammendrag) når noe er endret.
Skriptet henter én side om gangen med pause.
"""

import argparse
import copy
import datetime
import hashlib
import re
import sys
import time
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString

ROT = Path(__file__).resolve().parent.parent
LOVDATA = "https://lovdata.no"
START = LOVDATA + "/dokument/SPH/sph/KAPITTEL_1"
MAPPE = ROT / "regelverk" / "statsansatteloven" / "rundskriv" / "personalhandboka"
STATUS = ROT / "regelverk" / "personalhandboka.tsv"
RAPPORT = ROT / "personalhandbok-rapport.txt"
UA = {"User-Agent": "regelverksbase/1.0 (+https://github.com/tarjeiha/allover)"}
PAUSE = 1.5
MAKS_SIDER = 400
KOLONNER = ["punkt", "tittel", "sjekksum", "lagt_inn"]
NAVN = "Statens personalhåndbok"


def hent(url: str) -> str:
    for forsok in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
                return r.read().decode("utf-8", "replace")
        except Exception:
            if forsok == 2:
                raise
            time.sleep(5 * (forsok + 1))
        finally:
            time.sleep(PAUSE)


# --- HTML til Markdown --------------------------------------------------------------------

def tekst(el) -> str:
    """Innebygd tekst med lenker."""
    deler = []
    for barn in el.children:
        if isinstance(barn, NavigableString):
            deler.append(str(barn))
        elif barn.name == "a":
            href = barn.get("href", "")
            innhold = barn.get_text(" ", strip=True)
            if not href or href.startswith("#") or not innhold:
                deler.append(tekst(barn))
            else:
                href = LOVDATA + href if href.startswith("/") else href
                deler.append(f"[{innhold}]({href})")
        elif barn.name in ("strong", "b"):
            t = tekst(barn).strip()
            deler.append(f"**{t}**" if t else "")
        elif barn.name in ("em", "i"):
            t = tekst(barn).strip()
            deler.append(f"*{t}*" if t else "")
        elif barn.name == "sup":
            deler.append(f"^{barn.get_text('', strip=True)}")
        elif barn.name == "br":
            deler.append("\x00")
        elif barn.name in ("script", "style", "button"):
            continue
        else:
            deler.append(tekst(barn))
    return re.sub(r"[ \t\r\n ]+", " ", "".join(deler)).replace("\x00", "  \n").strip()


def tabell(el) -> str:
    rader = [[tekst(c).replace("|", "\\|") for c in tr.find_all(["th", "td"], recursive=False)]
             for tr in el.find_all("tr")]
    rader = [r for r in rader if any(r)]
    if not rader:
        return ""
    bredde = max(len(r) for r in rader)
    rader = [r + [""] * (bredde - len(r)) for r in rader]
    linjer = ["| " + " | ".join(rader[0]) + " |", "|" + "---|" * bredde]
    return "\n".join(linjer + ["| " + " | ".join(r) + " |" for r in rader[1:]])


def listepunkt(el) -> str:
    """Lovdata skriver listepunkter som en tabell med nummer og tekst."""
    celler = el.find("tr").find_all("td", recursive=False) if el.find("tr") else []
    nivå = int(el.get("data-level", "1") or 1)
    innrykk = "   " * (nivå - 1)
    if len(celler) >= 2:
        merke = celler[0].get_text(" ", strip=True)
        innhold = " ".join(tekst(c) for c in celler[1:])
        merke = "-" if merke in ("", "–", "-", "•", "·") else merke
        if re.fullmatch(r"\d+\.", merke) or merke == "-":
            return f"{innrykk}{merke} {innhold}"
        return f"{innrykk}- {merke} {innhold}"
    return f"{innrykk}- {tekst(el)}"


def blokker(div, nivå_fil: int) -> list:
    """Markdown-blokker for ett kapittel-div. Under-div-er blir overskrifter i samme fil."""
    ut = []
    for barn in div.children:
        if isinstance(barn, NavigableString):
            if barn.strip():
                ut.append(barn.strip())
            continue
        klasser = barn.get("class", [])
        if barn.name == "div" and "kapittel" in klasser:
            nivå = int(barn.get("data-level", "3"))
            h = barn.find(re.compile("^h[1-6]$"), recursive=False)
            if h:
                ut.append("#" * min(6, nivå - nivå_fil + 1) + " " + h.get_text(" ", strip=True))
            ut += blokker(barn, nivå_fil)
        elif barn.name == "div" and "documentButtonsBar" in klasser:
            continue
        elif re.fullmatch(r"h[1-6]", barn.name or ""):
            continue  # kapitteloverskriften skrives av kalleren
        elif barn.name == "table" and "listeItem" in klasser:
            linje = listepunkt(barn)
            if ut and ut[-1].endswith("\x01"):
                ut[-1] = ut[-1] + "\n" + linje + "\x01"
            else:
                ut.append(linje + "\x01")
        elif barn.name == "table":
            t = tabell(barn)
            if t:
                ut.append(t)
        elif barn.name in ("ul", "ol"):
            linjer = [f"{f'{i}.' if barn.name == 'ol' else '-'} {tekst(li)}"
                      for i, li in enumerate(barn.find_all("li", recursive=False), 1)]
            ut.append("\n".join(linjer))
        elif barn.name in ("p", "blockquote"):
            t = tekst(barn)
            if t:
                ut.append(("> " if barn.name == "blockquote" else "") + t)
        elif barn.name in ("a", "script", "style", "button"):
            continue
        else:
            ut += blokker(barn, nivå_fil)
    return ut


def ferdig(blokkliste: list) -> str:
    return "\n\n".join(b.replace("\x01", "") for b in blokkliste if b.replace("\x01", "").strip()).strip()


# --- Lesing av håndboka -------------------------------------------------------------------

def punkt_for(data_id: str) -> str:
    """KAPITTEL_10-1 -> 10.1"""
    return data_id.removeprefix("KAPITTEL_").replace("-", ".")


def les_handboka() -> tuple:
    """Returnerer (tittel, {punkt: (overskrift, markdown, url)}) i rekkefølge."""
    punkter = {}
    url, sett, tittel = START, set(), NAVN
    for _ in range(MAKS_SIDER):
        if url in sett:
            break
        sett.add(url)
        soup = BeautifulSoup(hent(url), "lxml")
        if soup.title and tittel == NAVN:
            t = re.sub(r"\s*-\s*Lovdata\s*$", "", soup.title.get_text(" ", strip=True))
            tittel = t or NAVN
        kropp = soup.find(id="documentBody")
        if kropp is None:
            raise RuntimeError(f"fant ikke teksten på {url} – har Lovdata endret oppbygning?")
        for div in kropp.find_all("div", class_="kapittel"):
            nivå = int(div.get("data-level", "0") or 0)
            if nivå not in (1, 2):
                continue
            h = div.find(re.compile("^h[1-6]$"), recursive=False)
            overskrift = h.get_text(" ", strip=True) if h else punkt_for(div["data-id"])
            if nivå == 1:
                # Bare innledningen: teksten før første underpunkt.
                kopi = copy.copy(div)
                for under in kopi.find_all("div", class_="kapittel"):
                    under.decompose()
                md = ferdig(blokker(kopi, 1))
            else:
                md = ferdig(blokker(div, 2))
            punkt = punkt_for(div["data-id"])
            lenke = f"{LOVDATA}/dokument/SPH/sph/{div['data-id']}"
            if punkt not in punkter or len(md) > len(punkter[punkt][1]):
                punkter[punkt] = (overskrift, md, lenke)
        neste = soup.select_one("ul.pager li.next a[href]")
        if neste is None or "disabled" in (neste.find_parent("li").get("class") or []):
            break
        url = LOVDATA + neste["href"] if neste["href"].startswith("/") else neste["href"]
    else:
        raise RuntimeError(f"stanset etter {MAKS_SIDER} sider – går «Neste side» i ring?")
    if len(punkter) < 100:
        raise RuntimeError(f"fant bare {len(punkter)} punkter – har Lovdata endret oppbygning?")
    return tittel, punkter


def filnavn(punkt: str) -> str:
    return "punkt-" + re.sub(r"[^0-9a-z]+", "-", punkt.lower()).strip("-") + ".md"


def sorter(punkt: str) -> list:
    return [(0, int(d), "") if d.isdigit() else (1, 0, d) for d in punkt.split(".")]


def les_status() -> dict:
    if not STATUS.exists():
        return {}
    linjer = STATUS.read_text(encoding="utf-8").splitlines()
    return {r["punkt"]: r for r in (dict(zip(KOLONNER, l.split("\t"))) for l in linjer[1:] if l)}


def skriv_status(status: dict) -> None:
    linjer = ["\t".join(KOLONNER)]
    linjer += ["\t".join(status[p].get(k, "") for k in KOLONNER) for p in sorted(status, key=sorter)]
    STATUS.write_text("\n".join(linjer) + "\n", encoding="utf-8")


def filtekst(tittel: str, punkt: str, overskrift: str, md: str, url: str, dato: str) -> str:
    hode = "\n".join([
        "---",
        f'rundskriv: "{NAVN}"',
        f'utgave: "{tittel}"',
        f'kilde: "{url}"',
        f'lagt_inn: "{dato}"',
        f'punkt: "{punkt}"',
        "---",
    ])
    navn = overskrift if overskrift.startswith(punkt) else f"{punkt} {overskrift}"
    ledd = "punkt" if "." in punkt else "kapittel"
    return f"{hode}\n\n# {NAVN} {ledd} {navn}\n\n{md}\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tving", action="store_true", help="skriv alle punktene på nytt")
    args = ap.parse_args()

    dato = datetime.date.today().isoformat()
    tittel, punkter = les_handboka()
    status = les_status()
    MAPPE.mkdir(parents=True, exist_ok=True)
    nye, endret, borte = [], [], []

    for punkt, (overskrift, md, url) in punkter.items():
        sjekksum = hashlib.sha256((overskrift + "\n" + md).encode()).hexdigest()[:16]
        gammel = status.get(punkt)
        fil = MAPPE / filnavn(punkt)
        if gammel and gammel["sjekksum"] == sjekksum and fil.exists() and not args.tving:
            continue
        lagt_inn = gammel["lagt_inn"] if gammel and gammel["sjekksum"] == sjekksum else dato
        fil.write_text(filtekst(tittel, punkt, overskrift, md, url, lagt_inn), encoding="utf-8")
        if gammel and gammel["sjekksum"] != sjekksum:
            endret.append(overskrift)
        elif not gammel:
            nye.append(overskrift)
        status[punkt] = {"punkt": punkt, "tittel": overskrift.replace("\t", " "),
                         "sjekksum": sjekksum, "lagt_inn": lagt_inn}

    for punkt in [p for p in status if p not in punkter]:
        (MAPPE / filnavn(punkt)).unlink(missing_ok=True)
        borte.append(status.pop(punkt)["tittel"])

    rekke = sorted(punkter, key=sorter)
    innhold = [f"{'  ' if '.' in p else ''}- {punkter[p][0]} – `{filnavn(p)}`" for p in rekke]
    (MAPPE / "oversikt.md").write_text(
        f"# {NAVN}\n\n"
        f"{tittel}, hentet fra [Lovdata]({LOVDATA}/dokument/SPH/sph). Håndboka er veiledning og "
        "tolkning av regelverket for statsansatte, og gjengir også bestemmelser fra "
        "hovedtariffavtalene og særavtalene i staten. Den er ikke lov- eller forskriftstekst. "
        "Oppgi den som «Statens personalhåndbok punkt x.y».\n\n"
        "Hvert punkt på nivå to har egen fil, og innledningen til hvert kapittel ligger i "
        "kapittelfilen (f.eks. `punkt-10.md`). Underpunktene står som overskrifter i filene.\n\n"
        "## Innhold\n\n" + "\n".join(innhold) + "\n", encoding="utf-8")
    skriv_status(status)

    print(f"{tittel}: {len(punkter)} punkter. Nye: {len(nye)}, endret: {len(endret)}, borte: {len(borte)}")
    if nye or endret or borte:
        melding = [f"Statens personalhåndbok: {len(nye)} nye, {len(endret)} endret, {len(borte)} borte", ""]
        vis = lambda liste, ord_: [f"- {ord_}: {l}" for l in liste[:40]] + (
            [f"- … og {len(liste) - 40} til"] if len(liste) > 40 else [])
        melding += vis(nye, "Ny") + vis(endret, "Endret") + vis(borte, "Borte")
        RAPPORT.write_text("\n".join(melding) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
