#!/usr/bin/env python3
"""
Holder Utdanningsdirektoratets rundskriv og veiledere til opplæringslova oppdatert fra udir.no.

Bruk:
    python3 verktoy/udir_hent.py           # hent nye og endrede rundskriv og veiledere
    python3 verktoy/udir_hent.py --tving   # hent alle på nytt

1. Leser sitemap.xml på udir.no. Hvert rundskriv og hver veileder har en side under
   /regelverk-og-tilsyn/skole-og-opplaring/<navn>/, ofte med undersider, og alle sidene har
   dato for siste endring (lastmod).
2. Henter dokumenter der en av sidene er ny eller har ny dato siden forrige gang
   (regelverk/udir-rundskriv.tsv), og skriver dem bare når teksten faktisk er endret.
3. Hvert dokument legges i regelverk/opplaeringslova/rundskriv/udir/<navn>/ med én fil per
   underside og oversikt.md. Dokumenter som er borte fra udir.no, slettes.

Skriver udir-rapport.txt (commit-melding og sammendrag) når noe er endret.
Udir tillater automatisk henting av disse sidene (robots.txt). Skriptet henter én side om
gangen med pause.
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
from pathlib import Path

from bs4 import BeautifulSoup, Comment, NavigableString

ROT = Path(__file__).resolve().parent.parent
BASE = "https://www.udir.no"
PREFIKS = "/regelverk-og-tilsyn/skole-og-opplaring/"
MAPPE = ROT / "regelverk" / "opplaeringslova" / "rundskriv" / "udir"
STATUS = ROT / "regelverk" / "udir-rundskriv.tsv"
RAPPORT = ROT / "udir-rapport.txt"
UA = {"User-Agent": "regelverksbase/1.0 (+https://github.com/tarjeiha/allover)"}
PAUSE = 1.0
KOLONNER = ["dokument", "tittel", "lastmod", "sider", "sjekksum", "lagt_inn"]
STØY = re.compile(r"breadcrumb|share|social|related|feedback|cookie|skip|toc|menu|tilbakemelding"
                  r"|print|footer|header|navigation|byline|tags", re.I)


def hent(url: str) -> str:
    for forsok in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return r.read().decode("utf-8", "replace")
        except Exception:
            if forsok == 2:
                raise
            time.sleep(5 * (forsok + 1))
        finally:
            time.sleep(PAUSE)


def dokumenter_fra_sitemap() -> dict:
    """Dokumentnavn -> {underside-sti: lastmod}. Undersiden "" er dokumentets forside."""
    xml = hent(BASE + "/sitemap.xml")
    ut = {}
    for url, mod in re.findall(r"<url>\s*<loc>\s*(.*?)\s*</loc>\s*<lastmod>\s*(.*?)\s*</lastmod>", xml):
        sti = url.removeprefix(BASE)
        if not sti.startswith(PREFIKS):
            continue
        deler = [d for d in sti[len(PREFIKS):].split("/") if d]
        if not deler:
            continue
        ut.setdefault(deler[0].lower(), {})["/".join(deler[1:]).lower()] = mod[:10]
    if not ut:
        raise RuntimeError("fant ingen sider under skole-og-opplaring i sitemap.xml – har udir.no endret oppbygning?")
    return ut


def les_status() -> dict:
    if not STATUS.exists():
        return {}
    linjer = STATUS.read_text(encoding="utf-8").splitlines()
    return {r["dokument"]: r for r in (dict(zip(KOLONNER, l.split("\t"))) for l in linjer[1:] if l)}


def skriv_status(status: dict) -> None:
    linjer = ["\t".join(KOLONNER)] + ["\t".join(status[d].get(k, "") for k in KOLONNER) for d in sorted(status)]
    STATUS.write_text("\n".join(linjer) + "\n", encoding="utf-8")


# --- HTML til Markdown --------------------------------------------------------------------

def tekst(el) -> str:
    deler = []
    for barn in el.children:
        if isinstance(barn, Comment):
            continue
        if isinstance(barn, NavigableString):
            deler.append(str(barn))
        elif barn.name == "a":
            href, innhold = barn.get("href", ""), barn.get_text(" ", strip=True)
            if not href or href.startswith("#") or href.startswith("javascript") or not innhold:
                deler.append(tekst(barn))
            else:
                href = BASE + href if href.startswith("/") else href
                deler.append(f"[{innhold}]({href})")
        elif barn.name in ("strong", "b"):
            t = tekst(barn).strip()
            deler.append(f"**{t}**" if t else "")
        elif barn.name in ("em", "i"):
            t = tekst(barn).strip()
            deler.append(f"*{t}*" if t else "")
        elif barn.name == "br":
            deler.append("\x00")
        elif barn.name in ("script", "style", "button", "svg"):
            continue
        else:
            deler.append(tekst(barn))
    return re.sub(r"[ \t\r\n ]+", " ", "".join(deler)).replace("\x00", "  \n").strip()


def markdown(el) -> str:
    blokker = []

    def liste(node, innrykk: str) -> list:
        linjer = []
        for i, li in enumerate(node.find_all("li", recursive=False), 1):
            merke = f"{i}." if node.name == "ol" else "-"
            under = li.find_all(["ul", "ol"], recursive=False)
            for u in under:
                u.extract()
            linjer.append(f"{innrykk}{merke} {tekst(li)}")
            for u in under:
                linjer += liste(u, innrykk + "   ")
        return linjer

    def gå(node):
        for barn in node.children:
            if isinstance(barn, Comment):
                continue
            if isinstance(barn, NavigableString):
                if barn.strip():
                    blokker.append(barn.strip())
                continue
            navn = barn.name
            if navn in ("h2", "h3", "h4", "h5", "h6"):
                t = barn.get_text(" ", strip=True)
                if t:
                    blokker.append("#" * int(navn[1]) + " " + t)
            elif navn == "h1":
                continue
            elif navn == "p":
                t = tekst(barn)
                if t:
                    blokker.append(t)
            elif navn in ("ul", "ol"):
                blokker.append("\n".join(liste(barn, "")))
            elif navn == "blockquote":
                t = tekst(barn)
                if t:
                    blokker.append("> " + t)
            elif navn == "table":
                rader = [[tekst(c).replace("|", "\\|") for c in tr.find_all(["th", "td"])]
                         for tr in barn.find_all("tr")]
                rader = [r for r in rader if any(r)]
                if rader:
                    bredde = max(len(r) for r in rader)
                    rader = [r + [""] * (bredde - len(r)) for r in rader]
                    linjer = ["| " + " | ".join(rader[0]) + " |", "|" + "---|" * bredde]
                    blokker.append("\n".join(linjer + ["| " + " | ".join(r) + " |" for r in rader[1:]]))
            elif navn in ("script", "style", "button", "figure", "svg", "img", "form", "noscript",
                          "nav", "aside", "header", "footer", "iframe"):
                continue
            else:
                gå(barn)

    gå(el)
    return "\n\n".join(b for b in blokker if b.strip()).strip()


def les_side(url: str) -> tuple:
    """(tittel, markdown) for én side."""
    soup = BeautifulSoup(hent(url), "lxml")
    h1 = soup.find("h1")
    tittel = re.sub(r"\s+", " ", h1.get_text(" ", strip=True)) if h1 else url.rstrip("/").rsplit("/", 1)[-1]
    innhold = (soup.select_one("main article") or soup.select_one("article")
               or soup.select_one("main") or soup.select_one("[role=main]") or soup.body)
    for t in innhold.find_all(["nav", "aside", "header", "footer", "form", "script", "style", "noscript"]):
        t.decompose()
    for t in innhold.find_all(True):
        if t.attrs is None:
            continue
        merker = " ".join(t.get("class", [])) + " " + (t.get("id") or "")
        if STØY.search(merker) and t.name not in ("main", "article", "body"):
            t.decompose()
    return tittel, markdown(innhold)


def filnavn(under: str) -> str:
    return re.sub(r"[^0-9a-z]+", "-", under.lower().replace("/", "--")).strip("-") + ".md"


def sorter(under: str) -> list:
    return [int(d) if d.isdigit() else d for d in re.split(r"(\d+)", under)]


def les_dokument(dok: str, sider: dict) -> tuple:
    """(tittel, forsidetekst, [(underside, tittel, markdown)])"""
    tittel, forside = les_side(f"{BASE}{PREFIKS}{dok}/")
    undersider = []
    for under in sorted((s for s in sider if s), key=sorter):
        t, md = les_side(f"{BASE}{PREFIKS}{dok}/{under}/")
        undersider.append((under, t, md))
    return tittel, forside, undersider


def skriv_dokument(dok: str, tittel: str, forside: str, undersider: list, dato: str) -> None:
    mappe = MAPPE / dok
    if mappe.exists():
        shutil.rmtree(mappe)
    mappe.mkdir(parents=True)
    url = f"{BASE}{PREFIKS}{dok}/"
    innhold = []
    for under, t, md in undersider:
        fil = mappe / filnavn(under)
        hode = "\n".join([
            "---",
            f'rundskriv: "{tittel}"',
            'utgiver: "Utdanningsdirektoratet"',
            'lov: "Opplæringslova"',
            f'kilde: "{url}{under}/"',
            f'lagt_inn: "{dato}"',
            "---",
        ])
        fil.write_text(f"{hode}\n\n# {tittel}: {t}\n\n{md}\n", encoding="utf-8")
        innhold.append(f"- {t} – `{fil.name}`")
    (mappe / "oversikt.md").write_text(
        "\n".join(["---", f'rundskriv: "{tittel}"', 'utgiver: "Utdanningsdirektoratet"',
                   'lov: "Opplæringslova"', f'kilde: "{url}"', f'lagt_inn: "{dato}"', "---", ""])
        + f"\n# {tittel}\n\n"
        f"Utdanningsdirektoratets tekst, hentet fra [udir.no]({url}) {dato}. Den er veiledning og "
        "tolkning, ikke lov- eller forskriftstekst.\n\n"
        + (forside + "\n\n" if forside else "")
        + ("## Innhold\n\n" + "\n".join(innhold) + "\n" if innhold else ""), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tving", action="store_true", help="hent alle på nytt")
    args = ap.parse_args()

    dato = datetime.date.today().isoformat()
    dokumenter = dokumenter_fra_sitemap()
    status = les_status()
    nye, endret, borte, uendret = [], [], [], 0

    for dok, sider in sorted(dokumenter.items()):
        lastmod = max(sider.values()) + f"/{len(sider)}"
        gammel = status.get(dok)
        if gammel and gammel.get("lastmod") == lastmod and (MAPPE / dok).exists() and not args.tving:
            continue
        tittel, forside, undersider = les_dokument(dok, sider)
        sjekksum = hashlib.sha256(json.dumps([tittel, forside, undersider], ensure_ascii=False)
                                  .encode()).hexdigest()[:16]
        rad = {"dokument": dok, "tittel": tittel.replace("\t", " "), "lastmod": lastmod,
               "sider": str(len(sider)), "sjekksum": sjekksum}
        if gammel and gammel.get("sjekksum") == sjekksum and (MAPPE / dok).exists() and not args.tving:
            status[dok] = {**gammel, **rad}
            uendret += 1
            continue
        skriv_dokument(dok, tittel, forside, undersider, dato)
        status[dok] = {**rad, "lagt_inn": dato}
        (endret if gammel else nye).append(f"{tittel} ({len(sider)} sider)")

    for dok in [d for d in status if d not in dokumenter]:
        shutil.rmtree(MAPPE / dok, ignore_errors=True)
        borte.append(status.pop(dok)["tittel"])

    skriv_status(status)
    print(f"Nye: {len(nye)}, endret: {len(endret)}, borte: {len(borte)}, uendret tekst: {uendret}")
    for linje in nye + endret + borte:
        print("  ", linje)
    if nye or endret or borte:
        melding = [f"Udirs rundskriv og veiledere: {len(nye)} nye, {len(endret)} endret, {len(borte)} borte", ""]
        melding += [f"- Ny: {l}" for l in nye] + [f"- Endret: {l}" for l in endret] + [f"- Borte: {l}" for l in borte]
        RAPPORT.write_text("\n".join(melding) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
