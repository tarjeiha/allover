#!/usr/bin/env python3
"""
Bygger lov- og forskriftstekst i repoet fra Lovdatas åpne datasett (NLOD 2.0).

Bruk:
    python3 verktoy/bygg.py                 # laster ned datasettene og bygger
    python3 verktoy/bygg.py --kilde <mappe> # bruker allerede utpakkede datasett

Hva som bygges styres av regelverk.json. For hver lov skrives:
    <mappe>/lov/par-<nr>.md                       én fil per paragraf
    <mappe>/forskrifter/<slug>/par-<nr>.md        én fil per forskriftsparagraf
    <mappe>/VEIVISER.md                           bare blokken mellom AUTO-markørene
og for hele repoet:
    indeks.tsv                                    alle paragrafer med sti
    CLAUDE.md                                     bare blokken mellom AUTO-markørene

Mappene merknader/, rundskriv/ og eu-eos/ under en lov bygges ikke, men listes
i veiviseren og i indeks.tsv. EU-rettsakter (eu.py) og tariffavtaler (avtale.py) bygges
i samme kjøring og listes i en egen blokk i CLAUDE.md.

Håndskrevet tekst utenfor AUTO-markørene røres ikke. Lovtekst skal aldri
redigeres for hånd, fordi den overskrives ved neste bygg.

Parseren (parse_lovdata.py) er hentet fra aid-skill-bygging og håndterer de
kjente fellene i Lovdata-formatet (h2/h3-overskrifter, innhold utenfor legalP,
nøstede kapitler, tabeller, fotnoter).
"""

import argparse
import copy
import json
import re
import shutil
import sys
import tarfile
import urllib.request
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import avtale as avtalemodul  # noqa: E402
import eu as eumodul  # noqa: E402
from parse_lovdata import (  # noqa: E402
    har_innhold_utenfor_paragrafer,
    parse_dokument,
    render_paragraf,
    slug_paragraf,
)

ROT = Path(__file__).resolve().parent.parent
API = "https://api.lovdata.no/v1/publicData/get/"
DATASETT = ["gjeldende-lover.tar.bz2", "gjeldende-sentrale-forskrifter.tar.bz2"]
AUTO_START = "<!-- AUTO-START: genereres av verktoy/bygg.py, ikke rediger for hånd -->"
AUTO_SLUTT = "<!-- AUTO-SLUTT -->"
MIN_DEKNING = 0.98


def last_ned(mappe: Path) -> None:
    mappe.mkdir(parents=True, exist_ok=True)
    for navn in DATASETT:
        fil = mappe / navn
        if not fil.exists():
            print(f"Laster ned {navn}")
            with urllib.request.urlopen(API + navn, timeout=300) as r, open(fil, "wb") as f:
                shutil.copyfileobj(r, f)
        with tarfile.open(fil, "r:bz2") as tar:
            tar.extractall(mappe, filter="data")


def filnavn_for(dokid: str) -> str:
    """LOV-2006-05-19-16 -> nl-20060519-016.xml, FOR-2013-01-11-33 -> sf-20130111-0033.xml"""
    m = re.match(r"(LOV|FOR)-(\d{4})-(\d{2})-(\d{2})(?:-(\d+))?$", dokid)
    if not m:
        return ""
    prefiks = "nl" if m.group(1) == "LOV" else "sf"
    bredde = 3 if prefiks == "nl" else 4
    return f"{prefiks}-{m.group(2)}{m.group(3)}{m.group(4)}-{int(m.group(5) or 0):0{bredde}d}.xml"


def lag_oppslag(kilde: Path) -> dict:
    """legacyID og filnavn -> filsti. legacyID leses med regex for å slippe å parse alt."""
    monster = re.compile(r'class="legacyID"[^>]*>\s*([^<\s]+)')
    oppslag = {}
    filer = [f for f in kilde.rglob("*") if f.is_file() and f.suffix in (".xml", ".html")]
    print(f"{len(filer)} dokumenter i datasettene, f.eks. {[f.relative_to(kilde).as_posix() for f in filer[:3]]}")
    for fil in filer:
        oppslag[fil.name] = fil
        m = monster.search(fil.read_text(encoding="utf-8", errors="ignore"))
        if m:
            oppslag[m.group(1).strip()] = fil
    return oppslag


def finn(oppslag: dict, dokid: str):
    return oppslag.get(dokid) or oppslag.get(filnavn_for(dokid))


ORD = re.compile(r"\w+", re.UNICODE)


def dekning(kilde_tekst: str, md: str) -> float:
    """Andel av ordene i kilden som finnes i den genererte filen."""
    kilde = Counter(ORD.findall(kilde_tekst.lower()))
    ut = Counter(ORD.findall(md.lower()))
    totalt = sum(kilde.values())
    if not totalt:
        return 1.0
    funnet = sum(min(n, ut[o]) for o, n in kilde.items())
    return funnet / totalt


def bygg_dokument(sti: Path, utmappe: Path, ref: str, feil: list) -> tuple:
    """Som _bygg_dokument, men en feil i ett dokument stopper ikke resten av bygget."""
    try:
        return _bygg_dokument(sti, utmappe, ref, feil)
    except Exception as e:  # noqa: BLE001
        feil.append(f"{ref} ({sti.name}): {type(e).__name__}: {e}")
        return None, None


def _bygg_dokument(sti: Path, utmappe: Path, ref: str, feil: list) -> tuple:
    """Skriver én fil per paragraf og returnerer (metadata, kapitler med oppføringer)."""
    if utmappe.exists():
        shutil.rmtree(utmappe)
    utmappe.mkdir(parents=True)
    meta, kapitler = parse_dokument(sti)
    resultat = []
    brukte = Counter()
    for kap in kapitler:
        oppforinger = []
        for art in kap["paragrafer"]:
            kildetekst = copy.copy(art).get_text(" ")
            md = render_paragraf(art, ref)
            slug = slug_paragraf(art.get("data-name"))
            brukte[slug] += 1
            if brukte[slug] > 1:
                slug = f"{slug}-{brukte[slug]}"
            fil = utmappe / f"par-{slug}.md"
            fil.write_text(md, encoding="utf-8")
            d = dekning(kildetekst, md)
            if d < MIN_DEKNING:
                feil.append(f"{fil.relative_to(ROT)}: bare {d:.1%} av ordene i kilden er med")
            tittel = md.splitlines()[0].lstrip("# ").strip()
            oppforinger.append((tittel, fil))
        resultat.append((kap["tittel"], oppforinger))
    if not any(oppf for _, oppf in resultat):
        # Løpende inndelte dokumenter (vedtak, delegeringer o.l.) har ingen paragrafer
        tegn, rest = har_innhold_utenfor_paragrafer(sti, terskel=1)
        if not tegn:
            feil.append(f"{ref} ({sti.name}): fant verken paragrafer eller annen tekst")
            return meta, resultat
        fil = utmappe / "tekst.md"
        fil.write_text(f"# {meta['tittel'] or ref}\n\n{rest}", encoding="utf-8")
        return meta, [("", [("Hele teksten (dokumentet har ikke paragrafer)", fil)])]
    tegn, rest = har_innhold_utenfor_paragrafer(sti)
    if tegn:
        fil = utmappe / "utenfor-paragrafene.md"
        fil.write_text(f"# {ref}: innhold utenfor paragrafene\n\n{rest}", encoding="utf-8")
        resultat.append(("Innhold utenfor paragrafene", [("Vedlegg, tabeller o.l.", fil)]))
    return meta, resultat


def erstatt_auto(fil: Path, innhold: str, skjelett: str) -> None:
    tekst = fil.read_text(encoding="utf-8") if fil.exists() else skjelett
    blokk = f"{AUTO_START}\n{innhold.rstrip()}\n{AUTO_SLUTT}"
    if AUTO_START in tekst and AUTO_SLUTT in tekst:
        før = tekst.split(AUTO_START)[0]
        etter = tekst.split(AUTO_SLUTT, 1)[1]
        tekst = før + blokk + etter
    else:
        tekst = tekst.rstrip() + "\n\n" + blokk + "\n"
    fil.write_text(tekst, encoding="utf-8")


EKSTRA = [("merknader", "Merknader"), ("rundskriv", "Rundskriv"), ("eu-eos", "EU/EØS-regelverk")]


def tittel_for(fil: Path) -> str:
    """Første overskrift, eller paragraf og tittel fra frontmatter."""
    tekst = fil.read_text(encoding="utf-8")
    fm = {}
    if tekst.startswith("---\n"):
        hode, _, tekst = tekst[4:].partition("\n---")
        for linje in hode.splitlines():
            k, _, v = linje.partition(":")
            fm[k.strip()] = v.strip().strip('"')
    for linje in tekst.splitlines():
        if linje.startswith("# "):
            return linje[2:].strip()
    if fm.get("tittel"):
        return " ".join(x for x in (fm.get("paragraf", ""), fm["tittel"]) if x)
    return fil.stem


def ekstra_kilder(mappe: Path, lovnavn: str, indeks: list) -> list:
    """Håndskrevne og kopierte kilder ved siden av lovteksten. De bygges ikke, bare listes."""
    ut = []
    for undermappe, navn in EKSTRA:
        rot = mappe / undermappe
        filer = sorted(f for f in rot.rglob("*.md") if "original" not in f.relative_to(rot).parts) if rot.is_dir() else []
        if not filer:
            continue
        ut += [f"### {navn}", ""]
        if undermappe == "merknader":
            ut += [f"- {tittel_for(f)} – `{f.relative_to(mappe).as_posix()}`" for f in filer]
        else:
            grupper = {}
            for f in filer:
                grupper.setdefault(f.parent, []).append(f)
            for gruppe, gfiler in grupper.items():
                rel = gruppe.relative_to(mappe).as_posix()
                oversikt = [f for f in gfiler if f.name == "oversikt.md"]
                hint = f", start med `{oversikt[0].relative_to(mappe).as_posix()}`" if oversikt else ""
                ut.append(f"- `{rel}/` – {len(gfiler)} filer{hint}")
        for f in filer:
            indeks.append(f"{lovnavn}\t{navn}\t{tittel_for(f)}\t{f.relative_to(ROT).as_posix()}")
        ut.append("")
    return ut


def rundskriv_per_paragraf(mappe: Path) -> dict:
    """Paragraf-slug -> rundskrivfiler som kommenterer den paragrafen i loven (fra innboksen)."""
    kart = {}
    for f in sorted((mappe / "rundskriv").rglob("par-*.md")) if (mappe / "rundskriv").is_dir() else []:
        if "original" in f.parts:
            continue
        hode = f.read_text(encoding="utf-8").split("\n---", 1)[0]
        par = re.search(r'^paragraf: "([^"]+)"', hode, re.M)
        if par and re.search(r'^gjelder: "lov"', hode, re.M):
            kart.setdefault(slug_paragraf(par.group(1)), []).append(f.relative_to(mappe).as_posix())
    return kart


def i_kraft(meta: dict) -> bool:
    return bool(re.match(r"\d{4}-\d{2}-\d{2}", meta.get("ikraft") or ""))


def status(meta: dict) -> str:
    """Dato for siste endring i kraft, eller at dokumentet ikke er i kraft ennå."""
    if not i_kraft(meta):
        return f"Ikke i kraft ({meta.get('ikraft') or 'ukjent dato'})"
    return meta["sist_endret"] or meta["ikraft"]


def kilde_linje(meta: dict) -> str:
    deler = [meta["tittel"]]
    if meta["legacyID"]:
        deler.append(meta["legacyID"])
    linje = " – ".join(deler)
    if meta["sist_endret"]:
        linje += f". Sist endret i kraft: {meta['sist_endret']}"
    if not i_kraft(meta):
        linje += f". **Ikke i kraft:** {meta.get('ikraft') or 'ukjent dato'}"
    if meta["departement"]:
        linje += f". Forvaltes av: {meta['departement']}"
    return linje + "."


def eu_henvisninger(mappe: Path, lovnavn: str, eu_mapper: dict, norske: dict, nevnt: dict) -> list:
    """Finner EU-rettsakter som lov- og forskriftsteksten viser til med nummer."""
    treff: dict = {}
    for fil in sorted(list((mappe / "lov").glob("*.md")) + list((mappe / "forskrifter").rglob("*.md"))):
        for n in eumodul.finn_henvisninger(fil.read_text(encoding="utf-8")):
            treff.setdefault(n, []).append(fil)
    if not treff:
        return []
    ut = ["## EU-rettsakter som teksten viser til", "",
          "Funnet automatisk ved søk etter rettsaktnummer. Stier til `eu/` er fra roten av basen.", ""]
    for n in sorted(treff, key=lambda k: (k not in eu_mapper, k)):
        filer = treff[n]
        vis = ", ".join(f"`{f.relative_to(mappe).as_posix()}`" for f in filer[:8])
        if len(filer) > 8:
            vis += f" og {len(filer) - 8} til"
        if n in eu_mapper:
            a = eu_mapper[n]
            ut.append(f"- **{eumodul.visningsnavn(n)}** ({a['navn']}) – i basen: `{a['mappe']}/VEIVISER.md`. Nevnt i {vis}")
            norske.setdefault(n, {}).setdefault(lovnavn, []).extend(f.relative_to(ROT).as_posix() for f in filer)
        else:
            ut.append(f"- {eumodul.visningsnavn(n)} – ikke i basen. Nevnt i {vis}")
            nevnt.setdefault(n, {})[lovnavn] = len(filer)
    return ut + [""]


def skriv_nevnte(nevnt: dict) -> None:
    linjer = [
        "# EU-rettsakter som norsk tekst i basen viser til, men som ikke ligger i basen",
        "",
        "Genereres av `verktoy/bygg.py` ved hvert bygg. Bruk listen til å velge hvilke rettsakter som skal legges inn.",
        "",
        "| Rettsakt | Antall filer | Regelverk |",
        "|---|---|---|",
    ]
    for n, lover in sorted(nevnt.items(), key=lambda kv: -sum(kv[1].values())):
        linjer.append(f"| {eumodul.visningsnavn(n)} | {sum(lover.values())} | {', '.join(sorted(lover))} |")
    (ROT / "eu").mkdir(exist_ok=True)
    (ROT / "eu" / "nevnte-rettsakter.md").write_text("\n".join(linjer) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kilde", type=Path, help="mappe med utpakkede datasett")
    args = ap.parse_args()

    kilde = args.kilde or ROT / ".lovdata"
    if not args.kilde:
        last_ned(kilde)
    oppslag = lag_oppslag(kilde)
    config = json.loads((ROT / "regelverk.json").read_text(encoding="utf-8"))

    feil: list = []
    merknader: list = []
    indeks = ["lov\tdokument\tparagraf\tsti"]
    lovliste = []
    eu_mapper = {eumodul.nokkel_fra_celex(a["celex"]): a for a in config.get("eu", [])}
    norske_henvisninger: dict = {}
    nevnt_ikke_i_basen: dict = {}

    for lov in config["lover"]:
        mappe = ROT / lov["mappe"]
        lovfil = finn(oppslag, lov["lov"])
        if not lovfil:
            feil.append(f"Fant ikke {lov['lov']} ({filnavn_for(lov['lov'])}) i datasettene")
            continue
        meta, kapitler = bygg_dokument(lovfil, mappe / "lov", lov["navn"], feil)
        if meta is None:
            continue
        etikett = "Lov" if lov["lov"].startswith("LOV") else "Forskrift/instruks"
        linjer = ["## Kilder", "", f"- **{etikett}:** {kilde_linje(meta)}"]
        forskriftsblokker = []
        for fs in lov.get("forskrifter", []):
            fsfil = finn(oppslag, fs["id"])
            if not fsfil:
                feil.append(f"Fant ikke {fs['id']} ({filnavn_for(fs['id'])}) i datasettene")
                continue
            fmeta, fkap = bygg_dokument(
                fsfil, mappe / "forskrifter" / fs["slug"], fs["navn"], feil
            )
            if fmeta is None:
                continue
            linjer.append(f"- **Forskrift:** {kilde_linje(fmeta)}")
            forskriftsblokker.append((fs["navn"], fkap))

        rundskriv = rundskriv_per_paragraf(mappe)
        eu_avsnitt = eu_henvisninger(mappe, lov["navn"], eu_mapper, norske_henvisninger, nevnt_ikke_i_basen)

        def liste(navn, kap, er_loven=False):
            ut = [f"### {navn}", ""]
            for kaptittel, oppf in kap:
                if kaptittel:
                    ut += [f"**{kaptittel}**", ""]
                for tittel, fil in oppf:
                    rel = fil.relative_to(mappe).as_posix()
                    linje = f"- {tittel} – `{rel}`"
                    if er_loven and fil.stem.startswith("par-") and fil.stem[4:] in rundskriv:
                        linje += " (rundskriv: " + ", ".join(f"`{r}`" for r in rundskriv[fil.stem[4:]]) + ")"
                    ut.append(linje)
                    indeks.append(f"{lov['navn']}\t{navn}\t{tittel}\t{fil.relative_to(ROT).as_posix()}")
                ut.append("")
            return ut

        linjer += ["", "## Innhold", ""]
        linjer += liste(lov["navn"], kapitler, er_loven=True)
        for navn, fkap in forskriftsblokker:
            linjer += liste(navn, fkap)
        linjer += eu_avsnitt
        ekstra = ekstra_kilder(mappe, lov["navn"], indeks)
        if ekstra:
            linjer += ["## Andre kilder", "", "Dette er ikke lov- eller forskriftstekst.", ""] + ekstra

        skjelett = f"# {lov['navn']}: veiviser\n\n_Håndskrevet veiledning mangler ennå._\n"
        erstatt_auto(mappe / "VEIVISER.md", "\n".join(linjer), skjelett)
        lovliste.append(f"| {lov['navn']} | `{lov['mappe']}/VEIVISER.md` | {status(meta)} |")

    # Tariffavtaler
    for a in config.get("avtaler", []):
        avtalemodul.prov_nedlasting(a, merknader)
        avtalemodul.bygg_avtale(a, feil, merknader, indeks)

    # EU-rettsakter
    for a in config.get("eu", []):
        info = eumodul.bygg_rettsakt(ROT, a, feil, merknader)
        if not info:
            continue
        if not info.get("beholdt"):
            skjelett = f"# {a['navn']}: veiviser\n\n_Håndskrevet veiledning mangler ennå._\n"
            erstatt_auto(ROT / a["mappe"] / "VEIVISER.md", eumodul.veiviser_blokk(ROT, info, norske_henvisninger), skjelett)
        for _, tittel, fil in info["oppforinger"]:
            indeks.append(f"{a['navn']}\tEU-rettsakt\t{tittel}\t{fil.relative_to(ROT).as_posix()}")
        for fil in sorted((ROT / a["mappe"] / "merknader").glob("*.md")):
            indeks.append(f"{a['navn']}\tMerknader\t{tittel_for(fil)}\t{fil.relative_to(ROT).as_posix()}")
    skriv_nevnte(nevnt_ikke_i_basen)

    (ROT / "indeks.tsv").write_text("\n".join(indeks) + "\n", encoding="utf-8")
    tabell = ["| Regelverk | Veiviser | Sist endret i kraft |", "|---|---|---|"] + lovliste
    erstatt_auto(ROT / "CLAUDE.md", "\n".join(tabell), "# Regelverksbasen\n")
    avtalemodul.oppdater_claude(config)

    for m in merknader:
        print(f"MERK: {m}")

    if feil:
        print("FEIL:")
        for f in feil:
            print(f"  {f}")
        return 1
    print(f"Ferdig: {len(indeks) - 1} paragrafer i indeksen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
