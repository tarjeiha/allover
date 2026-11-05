#!/usr/bin/env python3
"""
Holder veiledere og rundskriv fra direktoratenes nettsider oppdatert i basen.

Bruk:
    python3 verktoy/nettsider_hent.py                 # alle kildene
    python3 verktoy/nettsider_hent.py udir imdi       # bare disse kildene
    python3 verktoy/nettsider_hent.py --tving         # skriv alt på nytt

Kildene står i KILDER under: hvilket nettsted, hvilke dokumenter og hvilken lov de hører til.
Et dokument er en side med undersider, f.eks. et rundskriv med ett kapittel per side.

1. Leser sitemap.xml på nettstedet og finner sidene til hvert dokument.
2. Har sitemap dato for siste endring (lastmod), hentes bare dokumenter med ny dato. Ellers
   hentes alle sidene hver gang. Teksten sammenlignes med sjekksum (regelverk/nettsider.tsv),
   og et dokument skrives bare når teksten faktisk er endret.
3. Hvert dokument legges i regelverk/<lov>/rundskriv/<kilde>/<dokument>/ med én fil per
   underside og oversikt.md. Dokumenter som er borte fra nettstedet, slettes.

Skriver nettsider-rapport.txt (commit-melding og sammendrag) når noe er endret. Feiler én
kilde, fortsetter skriptet med de andre og avslutter med feilkode til slutt.
Nettstedene tillater automatisk henting av disse sidene (robots.txt). Skriptet bruker en
åpen User-Agent og henter én side om gangen med pause.
"""

import argparse
import datetime
import hashlib
import json
import re
import shutil
import sys
import time
import traceback
import urllib.error
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup, Comment, NavigableString

ROT = Path(__file__).resolve().parent.parent
STATUS = ROT / "regelverk" / "nettsider.tsv"
RAPPORT = ROT / "nettsider-rapport.txt"
UA = {"User-Agent": "regelverksbase/1.0 (+https://github.com/tarjeiha/allover)"}
PAUSE = 1.0
KOLONNER = ["kilde", "dokument", "mappe", "tittel", "lastmod", "sider", "sjekksum", "lagt_inn"]
STØY = re.compile(r"breadcrumb|share|social|related|feedback|cookie|skip|toc|menu|tilbakemelding"
                  r"|print|footer|header|navigation|byline|tags|cardlist", re.I)

# Hver kilde: nettsted, utgiver, mappenavn under rundskriv/, og dokumentene.
# "under": hver underside av stien er et eget dokument. "dokument": stien er ett dokument.
KILDER = {
    "udir": {
        "base": "https://www.udir.no",
        "utgiver": "Utdanningsdirektoratet",
        "navn": "Udirs rundskriv og veiledere",
        "innhold": ["main article", "article", "main"],
        "dokumenter": [{"under": "/regelverk-og-tilsyn/skole-og-opplaring/", "lov": "opplaeringslova"}],
    },
    "imdi": {
        "base": "https://www.imdi.no",
        "utgiver": "IMDi",
        "navn": "IMDis veiledere",
        "innhold": ["div.report-read-content", "main article", "article", "main"],
        "dokumenter": [
            {"dokument": "/regelverk/integreringsloven/veileder-til-integreringsloven/", "lov": "integreringsloven"},
            {"dokument": "/regelverk/integreringsloven/juridisk-veileder-til-integreringslovens-midlertidige-kapittel-6a2/",
             "lov": "integreringsloven"},
            {"dokument": "/regelverk/regler-for-planlegging-og-gjennomforing-av-introduksjonsprogrammet/",
             "lov": "integreringsloven"},
            {"dokument": "/regelverk/regelverk-kvalifisering/", "lov": "integreringsloven"},
            {"dokument": "/regelverk/tolkeloven/", "lov": "tolkeloven"},
        ],
        "utelat": r"lenker-til-lovdata",
    },
    "spk": {
        "base": "https://www.spk.no",
        "utgiver": "Statens pensjonskasse",
        "navn": "Informasjon fra Statens pensjonskasse",
        "innhold": ["main article", "article", "main"],
        "dokumenter": [
            {"dokument": "/alderspensjon/", "lov": "spk-loven"},
            {"dokument": "/uforepensjon/", "lov": "spk-loven"},
            {"dokument": "/etterlattepensjon/", "lov": "spk-loven"},
            {"dokument": "/medlemskap-i-spk/", "lov": "spk-loven"},
            {"dokument": "/tidligere-medlem/", "lov": "spk-loven"},
            {"dokument": "/yrkesskadeforsikring/", "lov": "spk-loven"},
            {"dokument": "/avtalefestet-pensjon-afp/", "lov": "afp-loven"},
        ],
        "utelat": r"pensjonskalkulator|/nyheter/|/aktuelt",
    },
}

# Knappetekst og ikonnavn som står igjen som egne linjer etter konverteringen.
RESTER = re.compile(r"Til toppen|Skriv ut|Del|Lukk|east|west|north|south|close|menu"
                    r"|(?:arrow|expand|chevron|keyboard_arrow)_\w+", re.I)

BASE = ""  # nettstedet som hentes nå, brukes når relative lenker gjøres fullstendige


def hent(url: str) -> str:
    for forsok in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (403, 404, 410) or forsok == 2:
                raise
            time.sleep(5 * (forsok + 1))
        except Exception:
            if forsok == 2:
                raise
            time.sleep(5 * (forsok + 1))
        finally:
            time.sleep(PAUSE)


def sitemap(url: str) -> list:
    """[(url, lastmod eller "")], også fra sitemap-indekser."""
    xml = hent(url)
    if "<sitemapindex" in xml:
        ut = []
        for u in re.findall(r"<loc>\s*(.*?)\s*</loc>", xml):
            ut += sitemap(u)
        return ut
    ut = []
    for blokk in re.findall(r"<url>(.*?)</url>", xml, re.S):
        loc = re.search(r"<loc>\s*(.*?)\s*</loc>", blokk)
        mod = re.search(r"<lastmod>\s*(.*?)\s*</lastmod>", blokk)
        if loc:
            ut.append((loc.group(1).replace("&amp;", "&"), mod.group(1)[:10] if mod else ""))
    return ut


def dokumenter(kilde: dict) -> dict:
    """(dokumentsti, lov) -> {underside: lastmod}. Undersiden "" er dokumentets forside."""
    base, utelat = kilde["base"], kilde.get("utelat")
    ut = {}
    for url, mod in sitemap(base + "/sitemap.xml"):
        sti = url.removeprefix(base).removeprefix(base.replace("://www.", "://"))
        sti = sti if sti.endswith("/") else sti + "/"
        if utelat and re.search(utelat, sti):
            continue
        for d in kilde["dokumenter"]:
            if "under" in d and sti.startswith(d["under"]) and len(sti) > len(d["under"]):
                deler = sti[len(d["under"]):].strip("/").split("/")
                nøkkel = (d["under"] + deler[0] + "/", d["lov"])
                ut.setdefault(nøkkel, {})["/".join(deler[1:])] = mod
            elif "dokument" in d and sti.lower().startswith(d["dokument"]):
                ut.setdefault((d["dokument"], d["lov"]), {})[sti[len(d["dokument"]):].strip("/")] = mod
    return ut


def les_status() -> dict:
    if not STATUS.exists():
        return {}
    linjer = STATUS.read_text(encoding="utf-8").splitlines()
    rader = (dict(zip(KOLONNER, l.split("\t"))) for l in linjer[1:] if l)
    return {(r["kilde"], r["dokument"]): r for r in rader}


def skriv_status(status: dict) -> None:
    linjer = ["\t".join(KOLONNER)] + ["\t".join(status[n].get(k, "") for k in KOLONNER) for n in sorted(status)]
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
    t = re.sub(r"[ \t\r\n\u00a0]+", " ", "".join(deler))
    t = re.sub(r"\s*\x00\s*", "\x00", t.strip())
    return re.sub(r"\x00+", "  \n", t).strip()


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
    return "\n\n".join(b for b in blokker if b.strip() and not RESTER.fullmatch(b.strip())).strip()


def les_side(url: str, velgere: list) -> tuple:
    """(tittel, markdown) for én side, eller (None, None) når siden ikke finnes."""
    try:
        html = hent(url)
    except urllib.error.HTTPError as e:
        if e.code in (404, 410):
            print(f"  finnes ikke: {url}")
            return None, None
        raise
    soup = BeautifulSoup(html, "lxml")
    h1 = soup.find("h1")
    tittel = re.sub(r"\s+", " ", h1.get_text(" ", strip=True)) if h1 else url.rstrip("/").rsplit("/", 1)[-1]
    innhold = next((e for v in velgere if (e := soup.select_one(v))), None) or soup.body
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


def mappenavn(dok: str) -> str:
    return re.sub(r"[^0-9a-z]+", "-", dok.strip("/").rsplit("/", 1)[-1].lower()).strip("-")


def sorter(under: str) -> list:
    return [(0, int(d), "") if d.isdigit() else (1, 0, d) for d in re.split(r"(\d+)", under)]


def les_dokument(kilde: dict, dok: str, sider: dict) -> tuple:
    """(tittel, forsidetekst, [(underside, tittel, markdown)])"""
    url = kilde["base"] + dok
    tittel, forside = les_side(url, kilde["innhold"]) if "" in sider else (None, None)
    undersider = []
    for under in sorted((s for s in sider if s), key=sorter):
        t, md = les_side(f"{url}{under}/", kilde["innhold"])
        if t is not None and md:
            undersider.append((under, t, md))
    if tittel is None:
        tittel = undersider[0][1] if undersider else mappenavn(dok)
    return tittel, forside or "", undersider


def skriv_dokument(kilde: dict, mappe: Path, url: str, lov: dict, tittel: str, forside: str,
                   undersider: list, dato: str) -> None:
    if mappe.exists():
        shutil.rmtree(mappe)
    mappe.mkdir(parents=True)

    def hode(kilde_url: str) -> str:
        return "\n".join(["---", f'rundskriv: "{tittel}"', f'utgiver: "{kilde["utgiver"]}"',
                          f'lov: "{lov["navn"]}"', f'kilde: "{kilde_url}"', f'lagt_inn: "{dato}"', "---"])

    innhold = []
    for under, t, md in undersider:
        fil = mappe / filnavn(under)
        fil.write_text(f"{hode(url + under + '/')}\n\n# {tittel}: {t}\n\n{md}\n", encoding="utf-8")
        innhold.append(f"- {t} – `{fil.name}`")
    nettsted = kilde["base"].removeprefix("https://").removeprefix("www.")
    (mappe / "oversikt.md").write_text(
        f"{hode(url)}\n\n# {tittel}\n\n"
        f"Tekst fra {kilde['utgiver']}, hentet fra [{nettsted}]({url}) {dato}. Den er veiledning "
        "og tolkning, ikke lov- eller forskriftstekst.\n\n"
        + (forside + "\n\n" if forside else "")
        + ("## Innhold\n\n" + "\n".join(innhold) + "\n" if innhold else ""), encoding="utf-8")


def kjør_kilde(navn: str, kilde: dict, lover: dict, status: dict, dato: str, tving: bool, logg: dict) -> None:
    global BASE
    BASE = kilde["base"]
    funnet = dokumenter(kilde)
    if not funnet:
        raise RuntimeError(f"{navn}: fant ingen av dokumentene i sitemap.xml – har nettstedet endret oppbygning?")
    for (dok, lovmappe), sider in sorted(funnet.items()):
        lov = lover[f"regelverk/{lovmappe}"]
        mappe_rel = f"regelverk/{lovmappe}/rundskriv/{navn}/{mappenavn(dok)}"
        lastmod = (max(sider.values()) + f"/{len(sider)}") if all(sider.values()) else ""
        gammel = status.get((navn, dok))
        finnes = (ROT / mappe_rel).exists()
        if gammel and lastmod and gammel.get("lastmod") == lastmod and finnes and not tving:
            continue
        tittel, forside, undersider = les_dokument(kilde, dok, sider)
        if not forside and not undersider:
            continue
        sjekksum = hashlib.sha256(json.dumps([tittel, forside, undersider], ensure_ascii=False)
                                  .encode()).hexdigest()[:16]
        rad = {"kilde": navn, "dokument": dok, "mappe": mappe_rel, "tittel": tittel.replace("\t", " "),
               "lastmod": lastmod, "sider": str(len(undersider) + 1)}
        if gammel and gammel.get("sjekksum") == sjekksum and finnes and not tving:
            status[(navn, dok)] = {**gammel, **rad}
            continue
        skriv_dokument(kilde, ROT / mappe_rel, kilde["base"] + dok, lov, tittel, forside, undersider, dato)
        status[(navn, dok)] = {**rad, "sjekksum": sjekksum, "lagt_inn": dato}
        logg["Endret" if gammel else "Ny"].append(f"{kilde['utgiver']}: {tittel} ({len(undersider) + 1} sider)")
    for nøkkel in [n for n in status if n[0] == navn and n[1] not in {d for d, _ in funnet}]:
        rad = status.pop(nøkkel)
        shutil.rmtree(ROT / rad["mappe"], ignore_errors=True)
        logg["Borte"].append(f"{kilde['utgiver']}: {rad['tittel']}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("kilder", nargs="*", help=f"kildene som skal hentes (standard: {', '.join(KILDER)})")
    ap.add_argument("--tving", action="store_true", help="skriv alt på nytt")
    args = ap.parse_args()

    cfg = json.loads((ROT / "regelverk.json").read_text(encoding="utf-8"))
    lover = {l["mappe"]: l for l in cfg["lover"]}
    dato = datetime.date.today().isoformat()
    status = les_status()
    logg = {"Ny": [], "Endret": [], "Borte": []}
    feil = []
    for navn in args.kilder or list(KILDER):
        try:
            kjør_kilde(navn, KILDER[navn], lover, status, dato, args.tving, logg)
        except Exception:  # noqa: BLE001
            traceback.print_exc()
            feil.append(navn)
    skriv_status(status)

    print(f"Nye: {len(logg['Ny'])}, endret: {len(logg['Endret'])}, borte: {len(logg['Borte'])}")
    for typ, linjer in logg.items():
        for l in linjer:
            print(f"  {typ}: {l}")
    if any(logg.values()):
        melding = [f"Veiledere fra nettsider: {len(logg['Ny'])} nye, {len(logg['Endret'])} endret, "
                   f"{len(logg['Borte'])} borte", ""]
        melding += [f"- {typ}: {l}" for typ, linjer in logg.items() for l in linjer]
        RAPPORT.write_text("\n".join(melding) + "\n", encoding="utf-8")
    if feil:
        print("FEIL i kildene:", ", ".join(feil))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
