#!/usr/bin/env python3
"""Kontrollerer håndskrevet tekst i basen: merknader og den håndskrevne delen av veiviserne.

Sjekker at
- stier i `backticks` finnes (relativt til roten, regelverksmappen eller filens mappe),
- ingen tekst sier at et regelverk som er i regelverk.json, «ikke er i basen» eller «ikke er dekket»,
- ingen veiviser sier at en tolkningskilde (IMDi, Udir, SPK, Sivilombudet, Arbeidstilsynet, Statens
  personalhåndbok, Navs rundskriv) ikke er i basen når regelverket har en mappe for den under rundskriv/.
  Nevner setningen selv stien til mappen, godtas den («… ligger under `rundskriv/spk/`, men praksis er ikke i basen»),
- ingen håndskrevet tekst har departementsnavnet som avsender: «AID», «ASD», skillnavn med «aid-»
  eller uttrykk som «tekst fra departementet» og «departementets vurdering». Repoet er åpent og skal ikke
  se ut som noe et departement har publisert. Når lovteksten selv sier «departementet», er det greit,
  og det samme gjelder dokumentnavnet «Prop. 1 S for AID».

Lov- og forskriftstekst, rundskriv og AUTO-blokkene kontrolleres ikke, de bygges automatisk.
Skriver funnene og avslutter med kode 1 hvis det er feil.

Bruk: python3 verktoy/sjekk_tekst.py
      python3 verktoy/sjekk_tekst.py --fritekst FIL [FIL ...]
        sjekker bare avsendernavn i fritekst, f.eks. PR-tittel, PR-tekst og commit-meldinger.
        Linjer i HTML-kommentarer hoppes over.
"""
import json
import re
import sys
from pathlib import Path

ROT = Path(__file__).resolve().parent.parent
STI = re.compile(r"`([^`\s]+)`")
AVSENDER = re.compile(
    r"(?<!Prop\. 1 S for )\bAIDs?\b|\bASD\b|(?<![-\w])aid-[a-z]"
    r"|\b(?:fra|i|for|hos)\s+departementet\b(?!\s+(?:kan|skal|gir|har\s+hjemmel))"
    r"|\bdepartementets\s+(?:vurdering|føring|skriveregler|interne|egne|mål|budsjett)"
    r"|\bdepartementet\s+(?:har\s+valgt|mener|vil)\b")
IKKE_I_BASEN = r"(?:er\s+)?(?:\*\*)?ikke(?:\*\*)?\s+(?:i\s+basen|dekket|med\s+i\s+basen|lagt\s+inn)"


# Tolkningskilde -> test på mappene under regelverk/<lov>/rundskriv/ og rettspraksis/. Navnene som vises i veiviseren,
# står i TOLKNINGSKILDER i verktoy/bygg.py. Legg til begge steder når en ny kilde kommer inn.
KILDER = [
    (re.compile(r"\bIMDis?\b|Integrerings- og mangfoldsdirektorat"), lambda d: d.name == "imdi"),
    (re.compile(r"\bUdirs?\b|Utdanningsdirektorat"), lambda d: d.name == "udir"),
    (re.compile(r"\bSPKs?\b|Statens pensjonskasses?\b"), lambda d: d.name == "spk"),
    (re.compile(r"Sivilombud"), lambda d: d.name == "sivilombudet"),
    (re.compile(r"\bHøyesteretts?\b|\brettspraksis\b", re.I), lambda d: d.name == "hoyesterett"),
    (re.compile(r"Arbeidstilsynet"), lambda d: d.name == "arbeidstilsynet"),
    (re.compile(r"personalhåndbok", re.I), lambda d: d.name == "personalhandboka"),
    (re.compile(r"(?:\bNAVs?|\bNavs?|Arbeids- og velferdsdirektoratets?)\b[^.]*\brundskriv"),
     lambda d: d.name.startswith("rundskriv-r")),
]
MANGLER = re.compile(r"ikke\s+(?:med\s+)?i\s+basen|ikke\s+dekket", re.I)


def kjente_tolkningskilder() -> set:
    """Mappenavnene i TOLKNINGSKILDER i bygg.py, lest som tekst så sjekken ikke trenger byggets avhengigheter."""
    tekst = (ROT / "verktoy" / "bygg.py").read_text(encoding="utf-8")
    m = re.search(r"^TOLKNINGSKILDER = \{(.*?)^\}", tekst, re.S | re.M)
    return set(re.findall(r'^\s*"([\w-]+)":', m.group(1), re.M)) if m else set()


def tolkningskilder(mappe: Path) -> list:
    return [d for r in (mappe / "rundskriv", mappe / "rettspraksis") if r.is_dir() for d in r.rglob("*") if d.is_dir()]


def handskrevet(fil: Path) -> str:
    tekst = fil.read_text(encoding="utf-8")
    return tekst.split("<!-- AUTO-START")[0] if fil.name == "VEIVISER.md" else tekst


def filer() -> list:
    ut = sorted((ROT / "regelverk").rglob("VEIVISER.md"))
    ut += sorted(f for f in (ROT / "regelverk").rglob("merknader/*.md"))
    return ut


def avsenderfiler() -> list:
    """Håndskrevne filer utenfor regelverk/ som leses av alle: inngangsfiler, skills, veivisere og README."""
    ut = [ROT / n for n in ("README.md", "OM-BASENE.md", "CLAUDE.md", "SKILLVERSJONER.md")]
    ut += sorted((ROT / "skills").rglob("*.md")) + sorted((ROT / "sprak").glob("*.md"))
    ut += sorted((ROT / "data").glob("*.md")) + sorted((ROT / "stortinget").glob("*.md"))
    ut += [ROT / d / "VEIVISER.md" for d in ("budsjett", "politikk", "veiledere")]
    ut += sorted(ROT.glob("innboks*/README.md")) + sorted((ROT / "verktoy").glob("*.md"))
    return [f for f in ut if f.exists()]


def regelverksmappe(fil: Path) -> Path:
    deler = fil.relative_to(ROT).parts
    n = 3 if deler[1] == "eu" else 2
    return ROT.joinpath(*deler[:n])


def ser_ut_som_sti(s: str) -> bool:
    if any(t in s for t in "<>*…{}") or s.startswith(("http", "#")) or "://" in s:
        return False
    if "NN" in s or re.search(r"(?<![a-z])[NXY](?![a-z])", s):  # mønstre som `kap-N/` og `par-X-Y.md`
        return False
    return s.endswith((".md", ".tsv", ".json", "/")) and not s.startswith("-")


def finnes(s: str, fil: Path, forrige: Path | None = None) -> bool:
    """Stier står ofte relativt til en mappe nevnt like før (f.eks. i en tabell under `forskrifter/`).
    Godta derfor også treff i undermappene til regelverket, og et rent filnavn hvor som helst i regelverket."""
    s = s.rstrip("/")
    mappe = regelverksmappe(fil)
    baser = [ROT, mappe, fil.parent] + ([forrige] if forrige else []) + [d for d in mappe.iterdir() if d.is_dir()]
    baser += [d for under in ("forskrifter", "rundskriv") if (mappe / under).is_dir()
              for d in (mappe / under).iterdir() if d.is_dir()]
    if any((base / s).exists() for base in baser) or (mappe / "rundskriv" / f"rundskriv-{s}").exists():
        return True
    return "/" not in s and next(mappe.rglob(s), None) is not None


def navn_i_basen() -> list:
    cfg = json.loads((ROT / "regelverk.json").read_text(encoding="utf-8"))
    navn = []
    for gruppe in ("lover", "avtaler", "eu"):
        for r in cfg.get(gruppe, []):
            for n in [r.get("navn"), r.get("kortnavn"), *r.get("alias", [])]:
                if n and len(n) > 4 and not n.endswith("."):
                    navn.append(n)
    return sorted(set(navn), key=len, reverse=True)


def sjekk() -> list:
    navn = navn_i_basen()
    # «Statsansatteloven er ikke i basen», også sist i en liste. «Veiledning om tolkeloven er ikke i basen» er riktig.
    dekket = re.compile(r"(?<!om )(?<!til )(?<!etter )\b(" + "|".join(re.escape(n) for n in navn)
                        + r")\b(?:\s*\([^)]*\))?\s+" + IKKE_I_BASEN, re.IGNORECASE)
    funn = []
    for fil in filer():
        rel = fil.relative_to(ROT).as_posix()
        forrige = None  # sist nevnte mappe, som stier i en tabell under den er relative til
        for nr, linje in enumerate(handskrevet(fil).splitlines(), 1):
            for s in STI.findall(linje):
                if not ser_ut_som_sti(s):
                    continue
                if not finnes(s, fil, forrige):
                    funn.append(f"{rel}:{nr}: stien `{s}` finnes ikke")
                elif s.endswith("/") and (ROT / s).is_dir():
                    forrige = ROT / s
            m = dekket.search(linje)
            if m:
                funn.append(f"{rel}:{nr}: «{m.group(0).strip()}», men {m.group(1)} er i basen")
            if a := AVSENDER.search(linje):
                funn.append(f"{rel}:{nr}: «{a.group(0)}» viser et departement som avsender")
            if fil.name == "VEIVISER.md":
                mapper = tolkningskilder(regelverksmappe(fil))
                for setning in re.split(r"(?<=[.!?])\s+", linje):
                    if not MANGLER.search(setning) or "rundskriv/" in setning:
                        continue
                    for kilde, test in KILDER:
                        k = kilde.search(setning)
                        if k and any(test(d) for d in mapper):
                            funn.append(f"{rel}:{nr}: sier at «{k.group(0)}» ikke er i basen, "
                                        "men regelverket har en mappe for den under rundskriv/")
    kjente = kjente_tolkningskilder()
    for d in sorted((ROT / "regelverk").glob("*/rundskriv/*/")):
        if d.is_dir() and not d.name.startswith("rundskriv-") and d.name not in kjente | {"forskrifter"}:
            funn.append(f"{d.relative_to(ROT).as_posix()}/: ny tolkningskilde uten navn i TOLKNINGSKILDER i "
                        "verktoy/bygg.py og KILDER i verktoy/sjekk_tekst.py")
    for fil in avsenderfiler():
        rel = fil.relative_to(ROT).as_posix()
        for nr, linje in enumerate(handskrevet(fil).splitlines(), 1):
            if a := AVSENDER.search(linje):
                funn.append(f"{rel}:{nr}: «{a.group(0)}» viser et departement som avsender")
    return funn


def sjekk_fritekst(stier) -> list:
    """PR-tekster og commit-meldinger er like åpne som filene."""
    funn = []
    for sti in stier:
        tekst = re.sub(r"<!--.*?-->", "", Path(sti).read_text(encoding="utf-8"), flags=re.S)
        for nr, linje in enumerate(tekst.splitlines(), 1):
            if a := AVSENDER.search(linje):
                funn.append(f"{Path(sti).name}:{nr}: «{a.group(0)}» viser et departement som avsender")
    return funn


def main() -> int:
    if sys.argv[1:2] == ["--fritekst"]:
        funn = sjekk_fritekst(sys.argv[2:])
        for f in funn:
            print(f)
        print(f"{len(funn)} funn i fritekst" if funn else "Ingen funn i fritekst")
        return 1 if funn else 0
    funn = sjekk()
    for f in funn:
        print(f)
    print(f"{len(funn)} funn i håndskrevet tekst" if funn else "Ingen funn i håndskrevet tekst")
    return 1 if funn else 0


if __name__ == "__main__":
    sys.exit(main())
