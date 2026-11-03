#!/usr/bin/env python3
"""Påminnelser om nye utgaver av dokumentene i politikk/ og veiledere/.

Dokumentene lastes ned og legges inn for hånd, fordi regjeringen.no ikke slipper til automatisk
henting. Dette skriptet åpner bare en sak i GitHub når en ny utgave ventes: for dokumenter som
revideres årlig, fra den 1. i måneden `ventes_i` året etter utgivelsen. Datoene står i
politikk/dokumenter.json og veiledere/dokumenter.json og oppdateres når en ny utgave legges inn.

Bruk:
    python3 verktoy/politikk.py            # viser hvilke saker som ville blitt åpnet i dag
    python3 verktoy/politikk.py --varsle   # åpner sakene i GitHub (én gang per sak)
"""
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

ROT = Path(__file__).resolve().parent.parent
FILER = [ROT / "politikk" / "dokumenter.json", ROT / "veiledere" / "dokumenter.json"]


def varsler(config: dict, idag: date, del_: str = "politikk") -> list:
    """Saker som skal åpnes: (tittel, tekst)."""
    ut = []
    for d in config.get("dokumenter", []):
        if d.get("revideres") != "årlig":
            continue
        utgitt = date.fromisoformat(d["utgitt"])
        ventet = date(utgitt.year + 1, d.get("ventes_i", utgitt.month), 1)
        if idag < ventet:
            continue
        if del_ == "veiledere":
            ut.append((
                f"Se etter ny utgave av {d['navn']} ({ventet.year})",
                f"Utgaven i basen er {d['navn']}, {d['utgave']}, fra {d['utgiver']}. Retningslinjene oppdateres "
                f"løpende på regjeringen.no ({d.get('nettside', 'regjeringen.no')}). Det er nå over et år siden utgaven i basen.\n\n"
                "Sjekk datoen for siste oppdatering på regjeringen.no. Er det kommet en ny utgave: last ned PDF-en, del den opp i "
                f"`{d['mappe']}/` på samme måte som i dag (én fil per kapittel, vedleggene hver for seg), og oppdater `utgitt` og "
                "`utgave` i `veiledere/dokumenter.json` og utgaven i `veiledere/VEIVISER.md`. Lukk saken når det er gjort. "
                "Er utgaven den samme, sett `utgitt` ett år fram og lukk saken."
            ))
            continue
        ut.append((
            f"Se etter ny utgave av {d['navn']} ({ventet.year})",
            f"Utgaven i basen er {d['navn']} {d['utgave']}, utgitt av {d['utgiver']} {utgitt.strftime('%d.%m.%Y')}. "
            f"Dokumentet revideres årlig, og en ny utgave ventes rundt {ventet.strftime('%m.%Y')}. "
            "Har det vært regjeringsskifte, kan det være erstattet av en ny regjeringsplattform.\n\n"
            "Når den nye utgaven er lagt ut på regjeringen.no: last ned PDF-en, del den opp i "
            f"`{d['mappe']}/` på samme måte som i dag (én fil per kapittel), og oppdater `utgitt` og `utgave` i "
            "`politikk/dokumenter.json` og datoen i `politikk/VEIVISER.md`. Lukk saken når det er gjort. "
            "Er det ingen ny utgave ennå, la saken stå åpen."
        ))
    return ut


def main() -> int:
    saker = []
    for fil in FILER:
        if fil.exists():
            saker += varsler(json.loads(fil.read_text(encoding="utf-8")), date.today(), fil.parent.name)
    if sys.argv[1:] != ["--varsle"]:
        for tittel, _ in saker:
            print(tittel)
        return 0
    for tittel, tekst in saker:
        finnes = subprocess.run(
            ["gh", "issue", "list", "--state", "all", "--search", f"\"{tittel}\" in:title", "--json", "title", "--jq", ".[].title"],
            capture_output=True, text=True, check=True, cwd=ROT,
        ).stdout.splitlines()
        if tittel in finnes:
            print(f"Finnes allerede: {tittel}")
            continue
        subprocess.run(["gh", "label", "create", "driftsvarsel", "--color", "FBCA04", "--force",
                        "--description", "Varsel fra en fast jobb. Claude går gjennom disse."], check=False, cwd=ROT)
        subprocess.run(["gh", "issue", "create", "--title", tittel, "--assignee", "tarjeiha", "--label", "driftsvarsel", "--body", tekst], check=True, cwd=ROT)
        print(f"Åpnet sak: {tittel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
