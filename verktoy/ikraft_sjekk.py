#!/usr/bin/env python3
"""Finner lover som står som «ikke i kraft» i regelverk.json, men som Lovdata nå oppgir en dato for.

Bruk:
    python3 verktoy/ikraft_sjekk.py --ut fil.md   # skriver funnene til fila, exit 0

Kjøres etter bygget. Er det funn, lager nattbygget et driftsvarsel. Da må den nye loven
tas i bruk: endre navnet i regelverk.json, temalisten i CLAUDE.md og veiviserne, og flytte
eller merke kilder som gjelder den gamle loven (for forvaltningsloven: Sivilombudets
uttalelser, se paragrafnøkkelen i regelverk/forvaltningsloven-2025/merknader/).
"""
import argparse
import json
import re
from pathlib import Path

ROT = Path(__file__).resolve().parent.parent


def funn() -> list[str]:
    cfg = json.loads((ROT / "regelverk.json").read_text(encoding="utf-8"))
    ut = []
    for lov in cfg["lover"]:
        if "ikke i kraft" not in lov["navn"].lower():
            continue
        veiviser = ROT / lov["mappe"] / "VEIVISER.md"
        linje = next((l for l in veiviser.read_text(encoding="utf-8").splitlines()
                      if l.startswith("- **Lov:**")), "") if veiviser.exists() else ""
        status = re.search(r"\*\*Ikke i kraft:\*\* ([^.]+)", linje)
        if status and not re.search(r"\d{4}-\d{2}-\d{2}", status.group(1)):
            continue  # fortsatt «Kongen bestemmer» eller ukjent dato
        når = status.group(1) if status else (re.search(r"Sist endret i kraft: ([\d-]+)", linje) or [None, "i kraft"])[1]
        ut.append(f"- {lov['navn']} ({lov['lov']}): Lovdata oppgir nå {når}. Kilde: `{lov['mappe']}/VEIVISER.md`.")
    return ut


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ut", required=True)
    args = ap.parse_args()
    f = funn()
    Path(args.ut).write_text("\n".join(f) + ("\n" if f else ""), encoding="utf-8")
    print("\n".join(f) if f else "Ingen lover merket «ikke i kraft» har fått dato.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
