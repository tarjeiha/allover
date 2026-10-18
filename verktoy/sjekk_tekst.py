#!/usr/bin/env python3
"""Kontrollerer håndskrevet tekst i basen: merknader og den håndskrevne delen av veiviserne.

Sjekker at
- stier i `backticks` finnes (relativt til roten, regelverksmappen eller filens mappe),
- ingen tekst sier at et regelverk som er i regelverk.json, «ikke er i basen» eller «ikke er dekket».

Lov- og forskriftstekst, rundskriv og AUTO-blokkene kontrolleres ikke, de bygges automatisk.
Skriver funnene og avslutter med kode 1 hvis det er feil.

Bruk: python3 verktoy/sjekk_tekst.py
"""
import json
import re
import sys
from pathlib import Path

ROT = Path(__file__).resolve().parent.parent
STI = re.compile(r"`([^`\s]+)`")
IKKE_I_BASEN = r"(?:er\s+)?(?:\*\*)?ikke(?:\*\*)?\s+(?:i\s+basen|dekket|med\s+i\s+basen|lagt\s+inn)"


def handskrevet(fil: Path) -> str:
    tekst = fil.read_text(encoding="utf-8")
    return tekst.split("<!-- AUTO-START")[0] if fil.name == "VEIVISER.md" else tekst


def filer() -> list:
    ut = sorted((ROT / "regelverk").rglob("VEIVISER.md"))
    ut += sorted(f for f in (ROT / "regelverk").rglob("merknader/*.md"))
    return ut


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
    return funn


def main() -> int:
    funn = sjekk()
    for f in funn:
        print(f)
    print(f"{len(funn)} funn i håndskrevet tekst" if funn else "Ingen funn i håndskrevet tekst")
    return 1 if funn else 0


if __name__ == "__main__":
    sys.exit(main())
