#!/usr/bin/env python3
"""
Lister forskrifter i Lovdatas datasett som har hjemmel i en lov, ut fra hjemmelsfeltet
(dd.basedOn), slik BYGGING.md sier at forskrifter skal velges.

Bruk:
    python3 verktoy/finn_forskrifter.py --kilde .lovdata LOV-2023-06-09-30 ...
    python3 verktoy/finn_forskrifter.py --kilde .lovdata --alle  # alle lovene i regelverk.json,
                                                                 # bare forskrifter som ikke er med

For hver lov skrives forskriftene med ID, tittel, departement og om de allerede er
med i regelverk.json. Skriptet endrer ingenting i repoet.
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROT = Path(__file__).resolve().parent.parent


def felt(tekst: str, cls: str) -> str:
    m = re.search(rf'<dd class="{cls}"[^>]*>(.*?)</dd>', tekst, re.S)
    if not m:
        return ""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(1))).strip()


def hjemmelslenker(tekst: str) -> set:
    """Lov-ID-er som hjemmelsfeltet lenker til, f.eks. lov/2023-06-09-30 -> LOV-2023-06-09-30."""
    m = re.search(r'<dd class="basedOn"[^>]*>(.*?)</dd>', tekst, re.S)
    if not m:
        return set()
    ider = set()
    for dato, nr in re.findall(r"lov/(\d{4}-\d{2}-\d{2})-(\d+)", m.group(1)):
        ider.add(f"LOV-{dato}-{int(nr)}")
    return ider


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kilde", type=Path, default=ROT / ".lovdata")
    ap.add_argument("--alle", action="store_true", help="alle lovene i regelverk.json, bare de som mangler")
    ap.add_argument("lover", nargs="*")
    args = ap.parse_args()

    config = json.loads((ROT / "regelverk.json").read_text(encoding="utf-8"))
    med = {fs["id"] for lov in config["lover"] for fs in lov.get("forskrifter", [])}
    lover = list(args.lover)
    if args.alle:
        lover += [l["lov"] for l in config["lover"] if l["lov"].startswith("LOV")]
    if not lover:
        print("Ingen lover å sjekke.")
        return 0

    treff = {lov: [] for lov in lover}
    filer = sorted(args.kilde.rglob("sf-*.xml"))
    print(f"{len(filer)} forskrifter i datasettene")
    for fil in filer:
        tekst = fil.read_text(encoding="utf-8", errors="ignore")
        hjemler = hjemmelslenker(tekst)
        if fil == filer[0]:
            print(f"Eksempel på hjemmelsfelt ({fil.name}): {sorted(hjemler)}")
        for lov in lover:
            if lov in hjemler:
                treff[lov].append((
                    felt(tekst, "legacyID"),
                    felt(tekst, "title"),
                    felt(tekst, "ministry"),
                    len(hjemler),
                ))

    for lov, liste in treff.items():
        mangler = [t for t in liste if t[0] not in med]
        print(f"\n=== {lov}: {len(liste)} forskrifter med hjemmel i loven, {len(mangler)} ikke med")
        for fid, tittel, dep, antall in sorted(mangler if args.alle else liste):
            merke = "MED " if fid in med else "    "
            andre = f" (hjemmel i {antall} lover)" if antall > 1 else ""
            print(f"{merke}{fid}\t{tittel}\t[{dep}]{andre}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
