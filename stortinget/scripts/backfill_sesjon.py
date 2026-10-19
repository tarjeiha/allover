#!/usr/bin/env python3
"""
Engangs-backfill av historiske, AVSLUTTEDE sesjoner for sporsmal.json.

Bakgrunn (se endringslogg 2026-09-16): de tre sporsmal-endepunktene
(skriftligesporsmal, interpellasjoner, sporretimesporsmal) returnerer uten
`status=alle` KUN poster med status 'besvart' — stille, uten feilmelding.
Dette ble oppdaget og rettet for inneværende sesjon (2025-2026) 2026-09-16,
men sesjonene 2021-2022 t.o.m. 2024-2025 er fortsatt bygget med det gamle,
ufullstendige kallet og mangler etter alt å dømme sine trukket/bortfalt-
poster (til_behandling er ikke aktuelt for lukkede sesjoner).

Dette er en ENGANGSJOBB, ikke noe som skal kjøre på schedule — avsluttede
sesjoner endrer seg ikke. Kjør denne når backfillen faktisk skal gjøres,
ikke periodisk (se designdiskusjon 2026-09-16).

Bruk:
  python3 backfill_sesjon.py --dry-run              # vis hva som ville blitt lagt til
  python3 backfill_sesjon.py                        # kjør for alle 4 historiske sesjoner
  python3 backfill_sesjon.py --sesjon 2023-2024      # kjør for én bestemt sesjon
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from felles import upsert_sporsmal_for_sesjon  # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # mappen stortinget/
DATA = os.path.join(BASE, 'data')

HISTORISKE_SESJONER = ['2021-2022', '2022-2023', '2023-2024', '2024-2025']


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--dry-run', action='store_true')
    p.add_argument('--sesjon', action='append', help='Kan gjentas. Default: alle fire historiske sesjoner.')
    args = p.parse_args()

    sesjoner = args.sesjon or HISTORISKE_SESJONER
    sti = os.path.join(DATA, 'sporsmal')

    resultat = {}
    for sesjon in sesjoner:
        print(f"Backfiller sesjon {sesjon}{' (dry-run)' if args.dry_run else ''}...", file=sys.stderr)
        resultat[sesjon] = upsert_sporsmal_for_sesjon(sesjon, sti, args.dry_run)
        print(f"  +{resultat[sesjon]['nye']} nye, {resultat[sesjon]['oppdatert']} oppdatert", file=sys.stderr)

    print(json.dumps(resultat, ensure_ascii=False, indent=2))
    totalt_nye = sum(r['nye'] for r in resultat.values())
    print(f"\nTotalt {totalt_nye} nye poster på tvers av {len(sesjoner)} sesjon(er).", file=sys.stderr)


if __name__ == '__main__':
    main()
