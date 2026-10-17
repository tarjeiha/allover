#!/usr/bin/env python3
"""
Parser for Lovdata API sine datapakker (gjeldende-lover / gjeldende-sentrale-forskrifter).

Kildeformatet er XML-kompatibel HTML med eksplisitt struktur:
  section.section          -> kapittel (h2 = kapitteltittel)
  article.legalArticle     -> paragraf (data-name="§4a", h3.legalArticleHeader = tittel)
  article.legalP           -> ledd, med leddnummer i id-attributtet (...-ledd-3)
  ol.defaultList > li      -> bokstav-/nummerliste, li[data-name]="a."
  article.changesToParent  -> endringshistorikk (holdes adskilt fra selve lovteksten)

MERK om leddnummerering: i motsetning til Lovdatas .docx-eksport (der leddnummer måtte
hardkodes, jf. domener/regelverk.md) er leddnummer her eksplisitt i id-attributtet og
kan leses direkte. Vi leser id, men verifiserer også mot rekkefølge.
"""

import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup, Comment, NavigableString


def clean(text):
    """Normaliser whitespace uten å miste innhold."""
    return re.sub(r"\s+", " ", text).strip()


def merk_fotnoter(node):
    """
    Erstatt fotnotereferanser (sup.footnotereference) med en lesbar markør.

    Uten dette blir referansetallet limt inn i løpende tekst som et nakent siffer:
    "Loven trer i kraft fra den tid Kongen bestemmer. 1 Fra samme tid oppheves..."
    Det leses som en del av setningen, ikke som en note.
    """
    for sup in node.find_all("sup", class_="footnotereference"):
        sup.string = f" [note {clean(sup.get_text())}]"
    return node


def hent_fotnoter(node):
    """
    Hent ut fotnotetekst og fjern noteapparatet fra noden.

    Fotnoter ligger i <footer class="footnotes"> med én article.footnote per note.
    footer er ikke en av taggene render_paragraf itererer over, så uten dette
    forsvinner notene helt. Notene bærer ofte ikrafttredelsesdatoer og
    avgrensninger som ikke står noe annet sted i paragrafen.
    """
    noter = []
    for footer in node.find_all("footer", class_="footnotes"):
        for fn in footer.find_all("article", class_="footnote"):
            t = clean(fn.get_text(" ", strip=True))
            if t and t not in noter:
                noter.append(t)
        footer.extract()
    return noter


def render_inline(node):
    """Tekst fra en node, med lenker beholdt som ren tekst."""
    return clean(node.get_text(" ", strip=True))


def ledd_nummer(article):
    """Hent leddnummer fra id-attributt, f.eks. '...-ledd-3' -> 3."""
    nid = article.get("id", "") or ""
    m = re.search(r"-ledd-(\d+)$", nid)
    return int(m.group(1)) if m else None


def render_blandet(node, indent=0):
    """
    Tekst, lister og tabeller i dokumentrekkefølge, som avsnitt.

    Tekst som står ETTER en liste i samme ledd (f.eks. et siste punktum etter
    bokstavlisten) må komme etter listen. Å trekke ut listene først og lese
    resten som én tekst flyttet slik tekst foran listen.
    """
    avsnitt = []
    buffer = []

    def tøm():
        s = clean(" ".join(buffer))
        if s:
            avsnitt.append([s])
        buffer.clear()

    for c in node.children:
        if isinstance(c, NavigableString):
            if not isinstance(c, Comment):
                buffer.append(str(c))
        elif c.name in ("ol", "ul"):
            tøm()
            avsnitt.append(render_list(c, indent))
        elif c.name == "table":
            tøm()
            avsnitt.append(render_tabell(c))
        elif c.find(["ol", "ul", "table"]):
            tøm()
            avsnitt.extend(render_blandet(c, indent))
        else:
            buffer.append(c.get_text(" "))
    tøm()
    return avsnitt


def render_list(ol, indent=0):
    """Render ol/ul med bokstav- eller tallmarkører."""
    lines = []
    pad = "  " * indent
    for li in ol.find_all("li", recursive=False):
        marker = (li.get("data-name") or "").strip()
        if not marker:
            marker = "-"
        # Innholdet i li ligger typisk i article.listArticle > article.legalP.
        # Nestede lister og tekst etter dem beholdes i rekkefølge.
        deler = render_blandet(li, indent + 1)
        if deler and len(deler[0]) == 1 and not deler[0][0].startswith(("|", "  ")):
            lines.append(f"{pad}{marker} {deler[0][0]}".rstrip())
            deler = deler[1:]
        else:
            lines.append(f"{pad}{marker}")
        for d in deler:
            if len(d) == 1 and not d[0].startswith(("|", " ")):
                lines.append(f"{pad}  {d[0]}")
            else:
                lines.extend(d)
    return lines


def finn_header(art):
    """Paragrafoverskrift ligger på h2 i noen forskrifter, h3 i lover. Godta begge."""
    for tag in ("h2", "h3", "h4"):
        h = art.find(tag, class_="legalArticleHeader", recursive=False)
        if h:
            return h
    return art.find(class_="legalArticleHeader", recursive=False)


def render_paragraf(art, lovref):
    """
    Render én paragraf (article.legalArticle) til markdown.

    Går gjennom ALLE direkte barn i dokumentrekkefølge, ikke bare legalP:
    i flere forskrifter ligger innholdet som <ol> rett under paragrafen uten
    legalP-wrapper. Kun-legalP-iterasjon droppet dette stille (tomme filer).
    """
    name = (art.get("data-name") or "").strip()
    header = finn_header(art)
    if header:
        val = header.find("span", class_="legalArticleValue")
        tit = header.find("span", class_="legalArticleTitle")
        pnum = clean(val.get_text()) if val else name
        ptitle = clean(tit.get_text()) if tit else ""
    else:
        pnum, ptitle = name, ""

    out = []
    out.append(f"# {pnum}." + (f" {ptitle}" if ptitle else ""))
    out.append("")
    out.append(f"**Kilde:** {lovref} {pnum}")
    out.append("")

    # Noteapparatet hentes og fjernes før innholdet renderes, slik at
    # notetekst ikke blandes inn i selve lovteksten.
    noter = hent_fotnoter(art)
    merk_fotnoter(art)

    changes = []
    seq = 0
    for child in art.find_all(
        ["article", "ol", "ul", "p", "table"], recursive=False
    ):
        cls = child.get("class") or []
        if "changesToParent" in cls:
            changes.append(child)
            continue
        if "legalP" in cls:
            seq += 1
            n = ledd_nummer(child) or seq
            out.append(f"**{n}. ledd**")
            out.append("")
            for avsnitt in render_blandet(child):
                out.extend(avsnitt)
                out.append("")
        elif child.name in ("ol", "ul"):
            # Liste direkte under paragrafen, uten legalP-wrapper
            out.extend(render_list(child))
            out.append("")
        elif child.name == "table":
            # Tabell direkte under paragrafen, uten ledd-wrapper
            out.extend(render_tabell(child))
        else:
            # Generisk blokk (bl.a. article.defaultP). Kan inneholde både
            # lister og tabeller, i den rekkefølgen de står.
            for avsnitt in render_blandet(child):
                out.extend(avsnitt)
                out.append("")

    if noter:
        out.append("**Noter:**")
        out.append("")
        for n in noter:
            out.append(f"- {n}")
        out.append("")

    if changes:
        out.append("---")
        out.append("")
        out.append("**Endringshistorikk:**")
        out.append("")
        for c in changes:
            out.append(f"- {render_inline(c)}")
        out.append("")

    return "\n".join(out).rstrip() + "\n"


KAPITTELMONSTER = re.compile(r"^kap\d+[A-Za-z]*$")


def parse_dokument(path):
    """
    Les et Lovdata-dokument og returner metadata + kapittel/paragraf-struktur.

    To fallgruver håndteres her:

    1. Noen lover (folketrygdloven) har et nivå OVER kapitlene ("Del I", "Del II").
       Kapitlene ligger nestet inne i delene.
    2. Noen kapitler har undersekjoner (ftrl kap. 3, 8, 9 og 14 har romertall-
       inndeling som "I. Svangerskapspenger"). Paragrafene ligger da IKKE som
       direkte barn av kapittelet.

    Derfor: kapitler identifiseres på data-name-mønsteret kapN / kapNA, og
    paragrafer hentes REKURSIVT innenfor hvert kapittel. Et ikke-rekursivt søk
    droppet 29 av 30 paragrafer i ftrl kap. 3 uten å feile.
    """
    html = Path(path).read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "lxml")

    def keyinfo(cls):
        dd = soup.find("dd", class_=cls)
        return clean(dd.get_text(" ", strip=True)) if dd else ""

    meta = {
        "tittel": keyinfo("title"),
        "korttittel": keyinfo("titleShort"),
        "legacyID": keyinfo("legacyID"),
        "dokid": keyinfo("dokid"),
        "departement": keyinfo("ministry"),
        "ikraft": keyinfo("dateInForce"),
        "sist_endret": keyinfo("lastChangeInForce"),
    }

    body = soup.find("main", class_="documentBody") or soup
    alle_seksjoner = body.find_all("section", class_="section")

    kapittelseksjoner = [
        s for s in alle_seksjoner if KAPITTELMONSTER.match((s.get("data-name") or "").strip())
    ]
    if not kapittelseksjoner:
        # Forskrifter og lover uten kapN-navngiving: bruk seksjoner som faktisk
        # inneholder paragrafer, og hopp over rene container-seksjoner.
        kapittelseksjoner = [
            s
            for s in alle_seksjoner
            if s.find("article", class_="legalArticle")
            and not s.find("section", class_="section")
        ]

    kapitler = []
    for sec in kapittelseksjoner:
        h = sec.find(["h2", "h3", "h4"])
        kaptittel = clean(h.get_text()) if h else ""
        kapnavn = (sec.get("data-name") or "").strip()
        paragrafer = sec.find_all("article", class_="legalArticle")
        kapitler.append({"navn": kapnavn, "tittel": kaptittel, "paragrafer": paragrafer})

    if not kapitler:
        paragrafer = body.find_all("article", class_="legalArticle")
        kapitler.append({"navn": "", "tittel": "", "paragrafer": paragrafer})

    # Paragrafer som ligger utenfor alle seksjoner (forekommer i noen forskrifter
    # der f.eks. ikrafttredelsesbestemmelsen står etter siste kapittel).
    fordelt = {id(a) for k in kapitler for a in k["paragrafer"]}
    foreldrelose = [
        a for a in body.find_all("article", class_="legalArticle") if id(a) not in fordelt
    ]
    if foreldrelose:
        kapitler.append(
            {"navn": "utenfor-kapittel", "tittel": "", "paragrafer": foreldrelose}
        )

    # Kontroll: fanger opp at paragrafer forsvinner i nesting.
    i_dok = len(body.find_all("article", class_="legalArticle"))
    i_kap = sum(len(k["paragrafer"]) for k in kapitler)
    if i_kap != i_dok:
        print(
            f"  ADVARSEL {Path(path).name}: {i_dok} paragrafer i dokumentet, "
            f"{i_kap} fordelt på kapitler (differanse {i_dok - i_kap})"
        )

    return meta, kapitler


def slug_paragraf(name):
    """'§4a' -> '4a', '§ 12' -> '12'"""
    s = (name or "").replace("§", "").strip()
    s = re.sub(r"\s+", "", s).lower()
    # Noen dokumenter har interne navn som "utll1/a1"; de må bli gyldige filnavn
    return re.sub(r"[^\w.-]+", "-", s).strip("-") or "ukjent"


if __name__ == "__main__":
    meta, kapitler = parse_dokument(sys.argv[1])
    print(meta)
    for k in kapitler:
        print(k["navn"], "|", k["tittel"], "|", len(k["paragrafer"]), "paragrafer")


def render_tabell(table):
    """Render en HTML-tabell til markdown. Tabeller bærer ofte selve substansen
    (f.eks. invaliditetstabellen i menerstatningsforskriften)."""
    linjer = []
    rader = table.find_all("tr")
    if not rader:
        return linjer
    for i, tr in enumerate(rader):
        celler = [clean(td.get_text(" ", strip=True)) for td in tr.find_all(["td", "th"])]
        if not celler:
            continue
        celler = [c.replace("|", "\\|") for c in celler]
        linjer.append("| " + " | ".join(celler) + " |")
        if i == 0:
            linjer.append("|" + "---|" * len(celler))
    linjer.append("")
    return linjer


def render_blokk(node, nivaa=2):
    """
    Generisk renderer for innhold som IKKE ligger inne i en legalArticle.

    Flere forskrifter har vesentlig innhold utenfor paragrafstrukturen:
    invaliditetstabeller, kommentarer til forskriften, eller hele forskrifter
    som bare er løpende tekst uten paragrafer. Et rent paragrafsøk dropper
    dette stille - i menerstatningsforskriften utgjorde det 92 % av teksten.
    """
    out = []
    for child in node.find_all(
        ["section", "h1", "h2", "h3", "h4", "h5", "article", "ol", "ul", "p", "table", "div"],
        recursive=False,
    ):
        cls = child.get("class") or []
        if child.name == "article" and "legalArticle" in cls:
            continue
        if child.name == "article" and "changesToParent" in cls:
            continue
        if child.name == "section":
            out.extend(render_blokk(child, nivaa + 1))
        elif child.name in ("h1", "h2", "h3", "h4", "h5"):
            out.append("#" * min(nivaa, 6) + " " + clean(child.get_text()))
            out.append("")
        elif child.name == "table":
            out.extend(render_tabell(child))
        elif child.name in ("ol", "ul"):
            out.extend(render_list(child))
            out.append("")
        else:
            for avsnitt in render_blandet(child):
                out.extend(avsnitt)
                out.append("")
    return out


def har_innhold_utenfor_paragrafer(path, terskel=400):
    """Returnerer (antall_tegn, markdown) for innhold utenfor legalArticle."""
    soup = BeautifulSoup(Path(path).read_text(encoding="utf-8"), "lxml")
    body = soup.find("main", class_="documentBody") or soup
    for a in body.find_all("article", class_="legalArticle"):
        a.extract()
    for c in body.find_all("article", class_="changesToParent"):
        c.extract()
    rest = len(re.sub(r"\s+", "", body.get_text(" ")))
    if rest < terskel:
        return 0, ""
    md = "\n".join(render_blokk(body, 1)).rstrip() + "\n"
    return rest, md
