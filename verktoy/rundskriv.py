#!/usr/bin/env python3
"""
Legger rundskriv fra innboks/ inn i basen.

Bruk:
    python3 verktoy/rundskriv.py

For hver fil i innboks/ (PDF, Word, ODT, HTML, Markdown eller tekst):
  1. Teksten hentes ut (pdftotext for PDF, pandoc for resten).
  2. Loven finnes ut fra teksten: navnene og kortformene i regelverk.json telles,
     og NAV-rundskriv med nummer som R08-00 hører til folketrygdloven.
     Starter filnavnet med en lovmappe (f.eks. arbeidsmiljoloven-...), gjelder den.
  3. Har rundskrivet overskrifter som «Til § 8-4», «§ 8-4. Tittel» eller «Forskrift om X § 3 skal
     forstås slik», deles det i én fil per paragraf. Innholdsfortegnelsen tas bort.
  4. Alt legges i regelverk/<lov>/rundskriv/<navn>/, originalen i original/ under samme mappe.
     Står navnet på en forskrift under loven (fra regelverk.json) i tittelen, er det et rundskriv
     til forskriften, og det legges i regelverk/<lov>/rundskriv/forskrifter/<forskrift>/.
     Tittelen hentes fra «Sammendrag» i hodet på Lovdata-utskrifter.

Er loven uklar, mangler teksten (f.eks. skannet PDF) eller blir noe av teksten borte
ved oppdelingen, legges ingenting inn. Filen blir liggende i innboksen, og en fil
<filnavn>.FEIL.txt ved siden av forklarer hvorfor.

Skriptet skriver en oppsummering til rundskriv-rapport.txt (brukes som commit-melding).
"""

import datetime
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from bygg import dekning  # noqa: E402
from parse_lovdata import slug_paragraf  # noqa: E402

ROT = Path(__file__).resolve().parent.parent
INNBOKS = ROT / "innboks"
IGNORER = {"README.md", ".gitkeep"}
STØTTET = {".pdf", ".docx", ".odt", ".doc", ".html", ".htm", ".md", ".txt", ".rtf"}
MIN_TEGN = 500
MIN_TREFF = 3
MIN_DEKNING = 0.99

# Linjer som «Til § 8-4», «§ 11-5. Nedsatt arbeidsevne», «## Kommentar til § 3»
PARAGRAFLINJE = re.compile(
    r"^\s*(?:#+\s*)?(?:\d+(?:\.\d+)*\.?\s+)?(?:til\s+|kommentar(?:er)?\s+til\s+)?"
    r"(?:[a-zæøå]+loven\s+)?§\s*(\d+(?:\s?[a-z])?(?:\s?[A-Z])?(?:\s?-\s?\d+(?:\s?[a-z])?)?)\b",
    re.IGNORECASE,
)
# Navs rundskriv til en forskrift: «## 4. Forskrift om tilskudd til ekspertbistand § 3 skal forstås slik».
# Bare med «skal forstås slik», ellers ville forskriftsavsnitt inne i rundskriv til loven blitt egne deler.
FORSKRIFT_FORSTÅS = re.compile(
    r"^\s*(?:#+\s*)?(?:\d+(?:\.\d+)*\.?\s+)?forskrift(?:en)?\s+om\s+[^§\n]{1,150}?\s"
    r"§\s*(\d+(?:\s?[a-z])?)\s+skal\s+forstås\s+slik\b",
    re.IGNORECASE,
)
# R08-00, R03-01 og rundskriv til forskrifter som R08-07A-FOR og R10-07-FOR
NAV_NUMMER = re.compile(r"\bR\s?(\d{2})\s?[A-Z]?-\s?(?:00\b|\d{2}[A-Z]?-FOR\b)")


def slug(tekst: str) -> str:
    t = unicodedata.normalize("NFKD", tekst.lower())
    t = t.replace("ø", "o").replace("æ", "ae").replace("å", "a")
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:80] or "rundskriv"


def hent_tekst(fil: Path) -> str:
    if fil.suffix.lower() in (".md", ".txt"):
        return fil.read_text(encoding="utf-8", errors="replace")
    if fil.suffix.lower() == ".pdf":
        ut = subprocess.run(["pdftotext", "-enc", "UTF-8", str(fil), "-"],
                            capture_output=True, text=True, check=True)
        return ut.stdout
    if fil.suffix.lower() in (".html", ".htm"):
        # Lagrede nettsider har menyer, topp- og bunntekst som ikke hører til rundskrivet
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(fil.read_text(encoding="utf-8", errors="replace"), "lxml")
        for el in soup.find_all(["nav", "header", "footer", "script", "style", "noscript", "form", "aside"]):
            el.decompose()
        hoved = soup.find("main") or soup.find("article") or soup.body or soup
        ut = subprocess.run(["pandoc", "-f", "html", "-t", "gfm", "--wrap=none"],
                            input=str(hoved), capture_output=True, text=True, check=True)
        return ut.stdout
    ut = subprocess.run(["pandoc", str(fil), "-t", "gfm", "--wrap=none"],
                        capture_output=True, text=True, check=True)
    return ut.stdout


EU_RETTSAKT = re.compile(
    r"(europaparlaments- og rådsforordning|europaparlaments- og rådsdirektiv|kommisjonsforordning|"
    r"kommisjonens gjennomføringsforordning|rådsforordning|regulation \((eu|ec)\)|directive \d+/\d+/(eu|ec)|"
    r"(forordning|direktiv) \((eu|ef|eøf)\) nr\.?|the european parliament and of the council)",
    re.IGNORECASE,
)


def ser_ut_som_eu_rettsakt(tekst: str) -> bool:
    """Ser bare på starten, der tittelen står. Et rundskriv som omtaler en forordning, stoppes ikke."""
    return bool(EU_RETTSAKT.search(tekst[:1500]))


def finn_lov(fil: Path, tekst: str, lover: list) -> tuple:
    """Returnerer (lov, begrunnelse) eller (None, begrunnelse)."""
    for lov in lover:
        navn = Path(lov["mappe"]).name
        if fil.name.lower().startswith(navn + "-"):
            return lov, f"filnavnet starter med «{navn}»"
    liten = tekst.lower()
    treff = Counter()
    for lov in lover:
        for alias in {a.lower() for a in lov.get("alias", [])} | {lov["navn"].lower()}:
            treff[lov["mappe"]] += len(re.findall(r"(?<![\wæøå])" + re.escape(alias.lower()) + r"(?![\wæøå])", liten))
    if NAV_NUMMER.search(tekst[:3000]):
        ftrl = next((l["mappe"] for l in lover if Path(l["mappe"]).name == "folketrygdloven"), "folketrygdloven")
        treff[ftrl] += MIN_TREFF
    rangert = treff.most_common()
    oversikt = ", ".join(f"{m}: {n}" for m, n in rangert if n) or "ingen"
    if not rangert or rangert[0][1] < MIN_TREFF:
        return None, f"fant ingen lov i basen som teksten viser tydelig til (treff: {oversikt})"
    if len(rangert) > 1 and rangert[1][1] * 2 > rangert[0][1]:
        return None, (f"teksten viser til flere lover omtrent like mye (treff: {oversikt}). "
                      "Start filnavnet med lovmappen, f.eks. «folketrygdloven-...», for å velge")
    lov = next(l for l in lover if l["mappe"] == rangert[0][0])
    return lov, f"flest henvisninger til {lov['navn']} (treff: {oversikt})"


SAMMENDRAG = re.compile(r"^\|\s*Sammendrag\s*\|\s*(.+?)\s*\|\s*$", re.M | re.IGNORECASE)
DOKNR = re.compile(r"^\|\s*Doknr(?:/publisert)?\s*\|\s*(\S+)\s*\|\s*$", re.M | re.IGNORECASE)


def ren_lenketekst(s: str) -> str:
    """«[<u>ftrl § 8-7a</u>](https://…)» -> «ftrl § 8-7a»."""
    s = re.sub(r"</?u>", "", s)
    return re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s).strip()


def tittel_fra(tekst: str, fil: Path) -> str:
    # Lovdata-utskrifter har en tabell øverst der «Sammendrag» er den egentlige tittelen
    m = SAMMENDRAG.search(tekst[:5000])
    if m:
        tittel = ren_lenketekst(m.group(1))
        nr = DOKNR.search(tekst[:5000])
        if nr and nr.group(1) not in tittel:
            tittel += f" ({nr.group(1)})"
        return tittel[:200]
    for linje in tekst.splitlines():
        if linje.startswith("# ") and len(linje) > 7:
            return linje[2:].strip()[:150]
    for linje in tekst.splitlines():
        linje = linje.strip().lstrip("#").strip()
        if len(linje) > 5:
            return linje[:150]
    return fil.stem


LEDD = re.compile(r"(første|andre|annet|tredje|fjerde|femte|sjette|sjuende|syvende|åttende|niende|tiende)\s+ledd",
                  re.IGNORECASE)


def ser_ut_som_overskrift(rest: str, markdown_overskrift: bool = False) -> bool:
    """«§ 8-10. Sykepengegrunnlag» og «§ 8-10 første ledd» er overskrifter, «§ 8-46 for vernepliktige,» er ikke.
    I en Markdown-overskrift («### § 16-5 Krav til pleieforholdet») er også tittel med stor forbokstav en overskrift."""
    rest = rest.strip()
    if markdown_overskrift and rest[:1].isupper():
        return True
    return not rest or rest[0] in ".–-:" or bool(LEDD.match(rest))


def uten_innholdsfortegnelse(tekst: str) -> str:
    """Word-filer har ofte en innholdsfortegnelse med alle overskriftene som lenker. Den tas bort,
    ellers deles teksten opp på innholdsfortegnelsen. Den varer til neste overskrift med tekst."""
    linjer = tekst.splitlines()
    start = next((i for i, l in enumerate(linjer) if re.match(r"^#+\s*innholds(fortegnelse|oversikt)\s*$", l, re.I)), None)
    if start is None:
        return tekst
    slutt = next((i for i in range(start + 1, len(linjer)) if re.match(r"^#+\s*\S", linjer[i])), len(linjer))
    return "\n".join(linjer[:start] + linjer[slutt:])


def finn_forskrift(tittel: str, fil: Path, lov: dict):
    """Forskriften rundskrivet gjelder, når navnet på en forskrift under loven står i tittelen
    eller filnavnet. Ved flere treff vinner det lengste navnet. Bare tittelen telles, siden
    rundskriv til en lov ofte omtaler mange forskrifter."""
    hvor = re.sub(r"\s+", " ", tittel.lower())
    filnavn = fil.stem.lower()
    treff = [f for f in lov.get("forskrifter", [])
             if re.sub(r"\s+", " ", f["navn"].lower()) in hvor or (len(f["slug"]) > 6 and f["slug"] in filnavn)]
    return max(treff, key=lambda f: len(f["navn"])) if treff else None


def del_opp(tekst: str) -> list:
    """Returnerer [(paragraf eller None, tekst)]. Én del hvis det ikke finnes paragrafoverskrifter."""
    linjer = tekst.splitlines()
    # Har teksten overskrifter (Word og Markdown), regnes bare overskrifter. Fra PDF finnes
    # ingen overskrifter, og da regnes korte linjer.
    bare_overskrifter = sum(1 for l in linjer if l.startswith("#")) >= 2
    starter = []
    for i, linje in enumerate(linjer):
        if len(linje) > 160 or (bare_overskrifter and not linje.startswith("#")):
            continue
        m = PARAGRAFLINJE.match(linje)
        if m and ser_ut_som_overskrift(linje[m.end():], linje.startswith("#")):
            starter.append((i, "§ " + re.sub(r"\s+", " ", m.group(1)).strip()))
            continue
        m = FORSKRIFT_FORSTÅS.match(linje)
        if m:
            starter.append((i, "§ " + re.sub(r"\s+", " ", m.group(1)).strip()))
    if len(starter) < 2:
        return [(None, tekst)]
    deler = []
    if starter[0][0] > 0:
        deler.append((None, "\n".join(linjer[: starter[0][0]])))
    for n, (i, par) in enumerate(starter):
        slutt = starter[n + 1][0] if n + 1 < len(starter) else len(linjer)
        bit = "\n".join(linjer[i:slutt])
        if deler and deler[-1][0] == par:
            # Underoverskrifter for samme paragraf hører til samme del
            deler[-1] = (par, deler[-1][1] + "\n" + bit)
        else:
            deler.append((par, bit))
    return deler


def gjelder_forskrift(tittel: str, fil: Path) -> bool:
    return "forskrift" in (tittel + " " + fil.stem).lower()


FORSKRIFTSDEL = re.compile(r"^(\[FOR-\d{4}-\d{2}-\d{2}-\d+-§|Bestemmelsen utfyller \S*loven\b)")


def del_gjelder_forskrift(del_tekst: str) -> bool:
    """NAVs rundskriv kommenterer ofte både loven og forskrifter til den. En del om en forskriftsparagraf
    begynner med lenke til forskriften («[FOR-2009-12-22-1810-§2-1](…)») eller med «Bestemmelsen utfyller …loven»."""
    linjer = [l.strip() for l in del_tekst.splitlines() if l.strip() and not l.startswith("#")]
    return bool(linjer) and bool(FORSKRIFTSDEL.match(linjer[0]))


def oppdater_indeks(rel: str, lovnavn: str, rader: list) -> None:
    """Rundskrivet skal kunne finnes med en gang. Veiviseren oppdateres ved neste bygg."""
    sti = ROT / "indeks.tsv"
    linjer = sti.read_text(encoding="utf-8").splitlines() if sti.exists() else ["lov\tdokument\tparagraf\tsti"]
    linjer = [l for l in linjer if not l.split("\t")[-1].startswith(rel + "/")]
    linjer += [f"{lovnavn}\tRundskriv\t{t}\t{s}" for t, s in rader]
    sti.write_text("\n".join(linjer) + "\n", encoding="utf-8")


def legg_inn(fil: Path, lover: list, dato: str) -> str:
    tekst = hent_tekst(fil)
    if len(re.sub(r"\s+", "", tekst)) < MIN_TEGN:
        raise ValueError("fant nesten ingen tekst i filen. Er det en skannet PDF? Den må ha tekstlag")
    if ser_ut_som_eu_rettsakt(tekst):
        raise ValueError("teksten ser ut som en EU-rettsakt (forordning, direktiv eller beslutning), "
                         "ikke et rundskriv. Innboksen tar foreløpig bare rundskriv")
    lov, grunn = finn_lov(fil, tekst, lover)
    if lov is None:
        raise ValueError(grunn)
    tittel = tittel_fra(tekst, fil)
    tekst = uten_innholdsfortegnelse(tekst)
    # Bilder fra Word (logoer o.l.) blir lenker til filer som ikke finnes
    tekst = re.sub(r"^<img src=\"media/[^>]*>\s*$\n?", "", tekst, flags=re.M)
    til_forskrift = finn_forskrift(tittel, fil, lov)
    if til_forskrift:
        mappe = ROT / lov["mappe"] / "rundskriv" / "forskrifter" / til_forskrift["slug"]
        grunn += f"; gjelder {til_forskrift['navn']}"
    else:
        navn = slug(re.sub(rf"^{re.escape(Path(lov['mappe']).name)}-", "", fil.stem))
        mappe = ROT / lov["mappe"] / "rundskriv" / navn
    deler = del_opp(tekst)
    samlet = "\n".join(d for _, d in deler)
    d = dekning(tekst, samlet)
    if d < MIN_DEKNING:
        raise ValueError(f"bare {d:.1%} av teksten kom med ved oppdelingen")

    ny = not mappe.exists()
    if mappe.exists():
        for gammel in mappe.glob("*.md"):
            gammel.unlink()
    (mappe / "original").mkdir(parents=True, exist_ok=True)
    forskrift = bool(til_forskrift) or gjelder_forskrift(tittel, fil)
    hode = {
        "rundskriv": tittel,
        "lov": lov["navn"],
        **({"forskrift": til_forskrift["navn"], "forskrift_id": til_forskrift["id"]} if til_forskrift else {}),
        "kilde": f"original/{fil.name}",
        "lagt_inn": dato,
    }
    filer, brukte = [], Counter()
    for par, del_tekst in deler:
        if par is None:
            s = "innledning" if len(deler) > 1 else "tekst"
        else:
            s = "par-" + slug_paragraf(par)
        brukte[s] += 1
        if brukte[s] > 1:
            s = f"{s}-{brukte[s]}"
        meta = dict(hode)
        if par:
            meta["paragraf"] = par
            meta["gjelder"] = "forskrift" if forskrift or del_gjelder_forskrift(del_tekst) else "lov"
        fm = "\n".join(f'{k}: "{v}"' for k, v in meta.items())
        overskrift = f"{tittel} – {par}" if par else tittel
        (mappe / f"{s}.md").write_text(
            f"---\n{fm}\n---\n\n# {overskrift}\n\n{del_tekst.strip()}\n", encoding="utf-8")
        filer.append((par, f"{s}.md"))
    liste = "\n".join(f"- {par or 'Innledning og tekst uten paragraf'} – `{f}`" for par, f in filer)
    (mappe / "oversikt.md").write_text(
        f"# {tittel}\n\n"
        + (f"Rundskriv til {til_forskrift['navn']} ({til_forskrift['id']}), med hjemmel i {lov['navn'].lower()}. "
           if til_forskrift else f"Rundskriv til {lov['navn']}. ")
        + f"Lagt inn {dato} fra `original/{fil.name}`. "
        "Dette er ikke lov- eller forskriftstekst.\n\n"
        + (f"Paragrafhenvisningene gjelder forskriften rundskrivet kommenterer, ikke loven.\n\n" if forskrift and len(filer) > 1 else "")
        + f"## Innhold\n\n{liste}\n", encoding="utf-8")
    shutil.move(str(fil), mappe / "original" / fil.name)
    rel = mappe.relative_to(ROT).as_posix()
    oppdater_indeks(rel, lov["navn"], [(f"{tittel} – {par}" if par else tittel, f"{rel}/{f}") for par, f in filer])
    return f"{'Nytt' if ny else 'Oppdatert'}: {fil.name} -> {rel}/ ({len(filer)} filer; {grunn})"


def er_tariffavtale(fil: Path, avtale: dict) -> bool:
    """Hovedtariffavtalen kjennes igjen på filnavnet. Den går ikke gjennom rundskrivløpet."""
    return fil.suffix.lower() in (".docx", ".pdf") and fil.name.lower().startswith(
        avtale.get("filprefiks", Path(avtale["mappe"]).name)
    )


def legg_inn_avtale(fil: Path, avtale: dict, config: dict) -> str:
    """Deler opp avtalen rett fra innboksen og sletter Word-filen når det har gått bra.
    Filen finnes da bare i Git-historikken; nattbygget rører ikke avtalen."""
    import avtale as avtalemodul

    feil, merknader, indeks = [], [], []
    periode = avtalemodul.bygg_avtale(avtale, fil, feil, merknader, indeks)
    if periode is None or feil:
        # Rull tilbake: forrige oppdeling og veiviser tilbake på plass; filen blir liggende i innboksen
        mappe = str(ROT / avtale["mappe"])
        subprocess.run(["git", "checkout", "--", mappe], cwd=ROT, capture_output=True)
        subprocess.run(["git", "clean", "-fdq", "--", mappe], cwd=ROT, capture_output=True)
        raise ValueError("; ".join(feil + merknader) or "oppdelingen feilet")
    lagre_periode(avtale["mappe"], periode, config)
    avtalemodul.oppdater_indeks(avtale["navn"], indeks)
    avtalemodul.oppdater_claude(config)
    fil.unlink()
    return f"Lagt inn: {fil.name} -> {avtale['mappe']}/ ({len(indeks)} filer, periode {periode or 'ukjent'}). Word-filen er slettet."


def lagre_periode(mappe: str, periode: str, config: dict) -> None:
    """Skriver perioden fra forsiden av avtalen inn i regelverk.json. Varslene i nattbygget bygger på den."""
    if not periode:
        return
    fil = ROT / "regelverk.json"
    tekst = fil.read_text(encoding="utf-8")
    data = json.loads(tekst)
    for a in data.get("avtaler", []):
        if a["mappe"] == mappe and a.get("periode") != periode:
            a["periode"] = periode
            fil.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for a in config.get("avtaler", []):
        if a["mappe"] == mappe:
            a["periode"] = periode


def main() -> int:
    if not INNBOKS.is_dir():
        print("Ingen innboks.")
        return 0
    config = json.loads((ROT / "regelverk.json").read_text(encoding="utf-8"))
    lover = config["lover"]
    dato = datetime.date.today().isoformat()
    rapport, feil = [], []
    for fil in sorted(INNBOKS.iterdir()):
        if not fil.is_file() or fil.name in IGNORER or fil.name.endswith(".FEIL.txt"):
            continue
        feilfil = fil.with_name(fil.name + ".FEIL.txt")
        if fil.suffix.lower() not in STØTTET:
            melding = f"filtypen {fil.suffix} støttes ikke. Bruk PDF, Word, ODT, HTML, Markdown eller tekst"
        else:
            try:
                avtale = next((a for a in config.get("avtaler", []) if er_tariffavtale(fil, a)), None)
                if avtale:
                    rapport.append(legg_inn_avtale(fil, avtale, config))
                    feilfil.unlink(missing_ok=True)
                    continue
                rapport.append(legg_inn(fil, lover, dato))
                feilfil.unlink(missing_ok=True)
                continue
            except (ValueError, subprocess.CalledProcessError) as e:
                melding = str(e)
        feilfil.write_text(f"Ikke lagt inn ({dato}): {melding}\n", encoding="utf-8")
        feil.append(f"Ikke lagt inn: {fil.name}: {melding}")
    linjer = rapport + feil
    if linjer:
        tittel = f"Rundskriv fra innboksen: {len(rapport)} lagt inn, {len(feil)} stoppet"
        (ROT / "rundskriv-rapport.txt").write_text(tittel + "\n\n" + "\n".join(linjer) + "\n", encoding="utf-8")
        print(tittel)
        print("\n".join(linjer))
    else:
        print("Innboksen er tom.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
