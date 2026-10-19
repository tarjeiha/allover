#!/usr/bin/env python3
"""
Henter Navs pressemeldinger om statistikk og lagrer teksten i data/nav/tekster/.

Bruk:
    python3 verktoy/nav_tekster.py [--tor] [--wayback]

Nav legger pressemeldinger om statistikk under .../statistikk/<område>/nyheter/<navn>. De står i
nav.no/sitemap.xml så lenge de ligger ute. Eldre pressemeldinger tas ned etter en tid.

  1. Kandidater: alle /statistikk/*/nyheter/-adresser i sitemap.xml og alle som allerede er lagret.
     Med --wayback tas også adresser Internet Archive har sett siden 2024 med (brukes for å hente
     eldre pressemeldinger én gang). Er en side borte fra nav.no, hentes Internet Archives kopi.
  2. Siden leses fra __NEXT_DATA__ (Navs egen sidedata): tittel, publiseringsdato, sist endret,
     ingress og brødtekst. Bare innhold med contentType «pressRelease» publisert fra og med FRA lagres.
  3. Teksten skrives som markdown til data/nav/tekster/<område>/<dato>-<navn>.md. Hvert tall i Navs
     tekst kontrolleres mot markdown-filen. Avvik gir feil, og filen skrives ikke.
  4. En lagret side skrives på nytt bare når Nav har endret den (sist endret).
data/nav/tekster/indeks.tsv lister alle lagrede tekster. Filer slettes aldri.
Med --tor skrives ingenting; skriptet viser bare hva som ville blitt lagt inn.

Rapporten skrives til nav-tekster-rapport.txt.
"""
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from nav_hent import UA  # noqa: E402

ROT = Path(__file__).resolve().parent.parent
TEKSTER = ROT / "data" / "nav" / "tekster"
FRA = "2024-01-01"
NAVNO = "https://www.nav.no"
SITEMAP = NAVNO + "/sitemap.xml"
NYHET = re.compile(r"^https://www\.nav\.no/no/nav-og-samfunn/statistikk/([a-z0-9-]+)/nyheter/([a-z0-9.\-]+)$")
TALL = re.compile(r"\d{1,3}(?:[ \u00a0]\d{3})+(?:,\d+)?|\d+(?:,\d+)?")


def hent(url, forsok=3):
    for i in range(forsok):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if i == forsok - 1:
                raise
        except Exception:  # noqa: BLE001
            if i == forsok - 1:
                raise
        time.sleep(3 * (i + 1))
    return None


def rens_url(url):
    url = urllib.parse.unquote(url.strip()).split("?")[0].split("#")[0].rstrip("/")
    url = url.replace("http://", "https://").replace(":80/", "/").replace("://nav.no/", "://www.nav.no/")
    return url if NYHET.match(url) else None


def fra_sitemap():
    tekst = hent(SITEMAP) or ""
    return {u for u in map(rens_url, re.findall(r"<loc>([^<]+)</loc>", tekst)) if u}


def fra_wayback():
    cdx = ("https://web.archive.org/cdx/search/cdx?url=www.nav.no/no/nav-og-samfunn/statistikk/"
           "&matchType=prefix&filter=original:.*/nyheter/.*&collapse=urlkey&fl=original&from=2024&limit=20000")
    tekst = hent(cdx) or ""
    return {u for u in map(rens_url, tekst.split()) if u}


def wayback_kopi(url):
    """Returnerer (html, kopiadresse) for nyeste kopi i Internet Archive, eller (None, None)."""
    try:
        svar = json.loads(hent("https://archive.org/wayback/available?url=" + urllib.parse.quote(url, safe="")) or "{}")
    except Exception:  # noqa: BLE001
        return None, None
    kopi = svar.get("archived_snapshots", {}).get("closest", {})
    if not kopi.get("available") or kopi.get("status") != "200":
        return None, None
    ts = kopi["timestamp"]
    rå = f"https://web.archive.org/web/{ts}id_/{url}"
    return hent(rå), f"https://web.archive.org/web/{ts}/{url}"


def sidedata(tekst):
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', tekst or "", re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))["props"]["pageProps"]["content"]
    except (KeyError, ValueError, TypeError):
        return None


class TilMarkdown(HTMLParser):
    """Gjør Navs brødtekst om til enkel markdown: avsnitt, overskrifter, lister, lenker, figurer og tabeller."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blokker = []
        self.buf = []
        self.rad = None
        self.tabell = None

    def tom(self, prefiks=""):
        t = re.sub(r"\s+", " ", "".join(self.buf)).strip()
        self.buf = []
        if t:
            self.blokker.append(prefiks + t)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("p", "h2", "h3", "h4", "li", "figcaption"):
            self.tom()
        elif tag == "br":
            self.buf.append(" ")
        elif tag == "img" and a.get("src"):
            self.tom()
            self.blokker.append(f"![{a.get('alt') or 'Figur'}]({urllib.parse.urljoin(NAVNO, a['src'])})")
        elif tag == "table":
            self.tom()
            self.tabell = []
        elif tag == "tr":
            self.rad = []
        elif tag in ("td", "th"):
            self.buf = []

    def handle_endtag(self, tag):
        if tag in ("p", "figcaption"):
            self.tom()
        elif tag in ("h2", "h3", "h4"):
            self.tom("### " if tag != "h2" else "## ")
        elif tag == "li":
            self.tom("- ")
        elif tag in ("td", "th") and self.rad is not None:
            self.rad.append(re.sub(r"\s+", " ", "".join(self.buf)).strip().replace("|", "/"))
            self.buf = []
        elif tag == "tr" and self.tabell is not None and self.rad is not None:
            self.tabell.append(self.rad)
            self.rad = None
        elif tag == "table" and self.tabell is not None:
            if self.tabell:
                bredde = max(len(r) for r in self.tabell)
                rader = [r + [""] * (bredde - len(r)) for r in self.tabell]
                linjer = ["| " + " | ".join(rader[0]) + " |", "|" + "---|" * bredde]
                linjer += ["| " + " | ".join(r) + " |" for r in rader[1:]]
                self.blokker.append("\n".join(linjer))
            self.tabell = None

    def handle_data(self, data):
        self.buf.append(data)


def markdown(html_tekst):
    p = TilMarkdown()
    # Lenker skrives som [tekst](adresse).
    html_tekst = re.sub(
        r'<a\b[^>]*href="([^"]*)"[^>]*>(.*?)</a>',
        lambda m: f"[{re.sub(r'<[^>]+>', '', m.group(2)).strip()}]({urllib.parse.urljoin(NAVNO, html.unescape(m.group(1)))})",
        html_tekst, flags=re.S)
    p.feed(html_tekst)
    p.tom()
    return "\n\n".join(p.blokker)


def tall_i(tekst):
    return sorted(re.sub(r"\s", "", t) for t in TALL.findall(re.sub(r"\s+", " ", tekst)))


def bygg_fil(url, c, kopi):
    omrade, navn = NYHET.match(url).groups()
    omrade = omrade.removesuffix("-statistikk")
    data = c.get("data") or {}
    publisert = (c.get("publish") or {}).get("first") or c.get("createdTime") or ""
    tittel = c.get("displayName", "").strip()
    ingress = re.sub(r"\s+", " ", data.get("ingress") or "").strip()
    brod = (data.get("text") or {}).get("processedHtml") or ""
    md = markdown(brod)
    hode = [
        f"# {tittel}",
        "",
        "- Kilde: Nav, pressemelding om statistikk",
        f"- Område: {omrade}",
        f"- Publisert: {publisert[:10]}",
        f"- Sist endret hos Nav: {(c.get('modifiedTime') or '')[:10]}",
        f"- Adresse: {url}",
    ]
    if kopi:
        hode.append(f"- Hentet fra kopi i Internet Archive (siden er tatt ned hos Nav): {kopi}")
    hode += ["", "Teksten er Navs egen, gjengitt uten endringer i innhold. Figurer er lenket, ikke lagret.", ""]
    tekst = "\n".join(hode) + "\n" + (f"**{ingress}**\n\n" if ingress else "") + md + "\n"
    # Kontroll: alle tall i Navs ingress og brødtekst skal finnes i filen.
    kilde = html.unescape(re.sub(r"<[^>]+>", " ", ingress + " " + re.sub(r'(src|href)="[^"]*"', "", brod)))
    mangler = [t for t in set(tall_i(kilde)) if tall_i(kilde).count(t) > tall_i(tekst).count(t)]
    sti = TEKSTER / omrade / f"{publisert[:10]}-{navn}.md"
    return sti, tekst, mangler, {"publisert": publisert[:10], "omrade": omrade, "tittel": tittel, "url": url,
                                 "endret": (c.get("modifiedTime") or "")[:10], "kopi": kopi or ""}


def les_indeks():
    fil = TEKSTER / "indeks.tsv"
    if not fil.exists():
        return {}
    rader = fil.read_text(encoding="utf-8").splitlines()
    felt = rader[0].split("\t")
    return {r["url"]: r for r in (dict(zip(felt, linje.split("\t"))) for linje in rader[1:] if linje)}


def skriv_indeks(indeks):
    felt = ["publisert", "omrade", "tittel", "fil", "url", "endret", "kopi"]
    rader = sorted(indeks.values(), key=lambda r: (r["publisert"], r["url"]), reverse=True)
    linjer = ["\t".join(felt)] + ["\t".join(r.get(f, "") for f in felt) for r in rader]
    (TEKSTER / "indeks.tsv").write_text("\n".join(linjer) + "\n", encoding="utf-8")


def main(tor=False, wayback=False):
    indeks = les_indeks()
    feil, nye, endret, uendret, utenfor = [], [], [], 0, 0
    try:
        kandidater = fra_sitemap()
    except Exception as e:  # noqa: BLE001
        kandidater = set()
        feil.append(f"sitemap.xml kunne ikke leses ({e})")
    if not kandidater and not feil:
        feil.append("fant ingen pressemeldinger i sitemap.xml (har Nav endret oppbygningen?)")
    if wayback:
        try:
            kandidater |= fra_wayback()
        except Exception as e:  # noqa: BLE001
            feil.append(f"Internet Archive kunne ikke leses ({e})")
    kandidater |= set(indeks)
    for url in sorted(kandidater):
        lagret = indeks.get(url)
        if lagret and lagret.get("kopi"):
            continue  # Hentet fra kopi: siden er borte hos Nav og endres ikke.
        try:
            tekst = hent(url)
        except Exception as e:  # noqa: BLE001
            feil.append(f"{url}: kunne ikke leses ({e})")
            continue
        kopi = None
        if tekst is None:
            if lagret or not wayback:
                continue  # Tatt ned hos Nav. Det vi har, beholdes.
            tekst, kopi = wayback_kopi(url)
            time.sleep(1)
        c = sidedata(tekst)
        if not c or (c.get("data") or {}).get("contentType") != "pressRelease":
            utenfor += 1
            continue
        publisert = ((c.get("publish") or {}).get("first") or c.get("createdTime") or "")[:10]
        if publisert < FRA:
            utenfor += 1
            continue
        if lagret and lagret.get("endret") == (c.get("modifiedTime") or "")[:10]:
            uendret += 1
            continue
        sti, md, mangler, rad = bygg_fil(url, c, kopi)
        if mangler:
            feil.append(f"{url}: tall i Navs tekst mangler i filen: {', '.join(sorted(mangler)[:10])}")
            continue
        rad["fil"] = sti.relative_to(ROT).as_posix()
        (endret if lagret else nye).append(f"{rad['publisert']} {rad['tittel']} ({rad['omrade']})" + (" [kopi]" if kopi else ""))
        if not tor:
            if lagret and lagret.get("fil") and lagret["fil"] != rad["fil"]:
                (ROT / lagret["fil"]).unlink(missing_ok=True)
            sti.parent.mkdir(parents=True, exist_ok=True)
            sti.write_text(md, encoding="utf-8")
            indeks[url] = rad
    if not tor and indeks:
        skriv_indeks(indeks)
    linjer = [f"Nav-tekster: {len(nye)} ny(e), {len(endret)} endret, {uendret} uendret, {utenfor} utenfor, {len(feil)} feil", ""]
    if nye:
        linjer += ["Nye pressemeldinger:"] + [f"- {n}" for n in sorted(nye, reverse=True)] + [""]
    if endret:
        linjer += ["Endret hos Nav:"] + [f"- {n}" for n in sorted(endret, reverse=True)] + [""]
    if feil:
        linjer += ["Feil:"] + [f"- {f}" for f in feil]
    (ROT / "nav-tekster-rapport.txt").write_text("\n".join(linjer) + "\n", encoding="utf-8")
    print("\n".join(linjer))
    return 1 if feil else 0


if __name__ == "__main__":
    sys.exit(main("--tor" in sys.argv, "--wayback" in sys.argv))
