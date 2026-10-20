#!/usr/bin/env python3
"""
Lett, idempotent oppdatering av inneværende sesjon for stortinget.

Gjør TO ting i én kjøring:
1. TILLEGG: henter fersk XML for inneværende sesjon (alle fem endepunkter,
   status=alle) og legger til poster som mangler lokalt.
2. RECONCILIATION (kun inneværende sesjon — se designdiskusjon 2026-09-16):
   - sporsmal: alle poster fra fersk inneværende-sesjon-XML skrives inn på
     nytt (upsert), slik at status som har gått fra til_behandling -> besvart
     (el.l.) blir oppdatert, ikke stående fast på gammel status.
   - representantforslag: samme upsert-logikk for status/komite/emne.
   - representantforslag UTFALL: ALLE lokale poster (uansett hvilken sesjon
     de ble fremmet i) med utfall == 'ukjent' sjekkes på nytt mot et
     vedtak-oppslag bygget fra inneværende sesjons fulle stortingsvedtak-XML
     (ikke bare ANMOD-filtrert) — dette er gratis siden vi uansett bygger
     oppslaget for å finne utfall på NYE forslag.
   - anmodningsvedtak: ren tillegg (et vedtak endrer seg ikke etter at det
     er fattet) — ingen reconciliation.

Historisk backfill av eldre, avsluttede sesjoner dekkes IKKE her — se
scripts/backfill_sesjon.py, som er en sjeldnere engangsjobb.

Bruk:
  python3 oppdater_inkrementell.py               # oppdater inneværende sesjon
  python3 oppdater_inkrementell.py --dry-run      # vis hva som ville blitt gjort, ikke skriv

Output: ett JSON-objekt på stdout som oppsummerer endringene (brukes av
Claude til å bygge sesongens korte oppsummering), pluss en menneskelesbar
oppsummering på stderr.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from felles import (  # noqa: E402
    resolve_sesjon, hent_sesjon_xml, upsert_sporsmal_for_sesjon,
    parse_stortingsvedtak_liste, parse_anmodningsvedtak_record,
    parse_saker_liste, parse_representantforslag_grunnrecord, beriket_representantforslag,
    bygg_vedtak_oppslag, klassifiser_utfall, t, last_json, skriv_json,
)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # mappen stortinget/
DATA = os.path.join(BASE, 'data')


def oppdater_sporsmal(sesjon, dry_run):
    return upsert_sporsmal_for_sesjon(sesjon, os.path.join(DATA, 'sporsmal'), dry_run)


def oppdater_anmodningsvedtak(sesjon, dry_run, vedtak_root):
    sti = os.path.join(DATA, 'anmodningsvedtak')
    eksisterende = last_json(sti)
    eksisterende_ider = {x['id'] for x in eksisterende}

    sak_cache = {}
    nye_poster = []
    for v in parse_stortingsvedtak_liste(vedtak_root):
        idv = t(v, 'id')
        if idv in eksisterende_ider:
            continue
        type_el = v.find('{http://data.stortinget.no}stortingsvedtak_type')
        type_id = t(type_el, 'id') if type_el is not None else None
        if type_id != 'ANMOD':
            continue
        rec = parse_anmodningsvedtak_record(v, sesjon, sak_cache)
        nye_poster.append(rec)

    if not dry_run and nye_poster:
        eksisterende.extend(nye_poster)
        skriv_json(sti, eksisterende)
    return {'nye': len(nye_poster), 'total': len(eksisterende_ider) + len(nye_poster)}


def oppdater_representantforslag(sesjon, dry_run, vedtak_oppslag, saker_root):
    sti = os.path.join(DATA, 'representantforslag')
    eksisterende = last_json(sti)
    per_id = {x['id']: x for x in eksisterende}

    sak_cache = {}
    nye = 0
    status_oppdatert = 0
    for sak in parse_saker_liste(saker_root):
        dokumentgruppe = t(sak, 'dokumentgruppe')
        if dokumentgruppe != 'representantforslag':
            continue
        idv = t(sak, 'id')
        # Billig grunnrecord fra bulk-XML (ingen nettverkskall) — status og
        # utfall kommer herfra + det ferdigbygde vedtak-oppslaget.
        rec = parse_representantforslag_grunnrecord(sak, sesjon, vedtak_oppslag)
        if idv not in per_id:
            # Ny post: ETT per-sak-kall for å hente forslagstillere/komite/emne.
            rec = beriket_representantforslag(rec, sak_cache)
            per_id[idv] = rec
            nye += 1
        else:
            gammel = per_id[idv]
            if gammel.get('status') != rec['status'] or gammel.get('utfall') != rec['utfall']:
                gammel['status'] = rec['status']
                gammel['utfall'] = rec['utfall']
                gammel['utfall_tekst'] = rec['utfall_tekst']
                gammel['behandlet_sesjon'] = rec['behandlet_sesjon']
                status_oppdatert += 1

    # Reconciliation: sjekk ALLE lokale 'ukjent'-poster, og 'annet' uten vedtakstekst
    # (uansett sesjon fremmet), på nytt mot dette vedtak-oppslaget — gratis, oppslaget er
    # allerede bygget. 'annet' uten tekst skyldtes at vedtaksteksten ble lest fra feil felt.
    utfall_lost = 0
    for idv, rec in per_id.items():
        if not (rec.get('utfall') == 'ukjent' or (rec.get('utfall') == 'annet' and not rec.get('utfall_tekst'))):
            continue
        nytt_utfall, ny_tekst = klassifiser_utfall(idv, vedtak_oppslag)
        if nytt_utfall != 'ukjent' and (nytt_utfall, ny_tekst) != (rec['utfall'], rec.get('utfall_tekst')):
            rec['utfall'] = nytt_utfall
            rec['utfall_tekst'] = ny_tekst
            utfall_lost += 1

    if not dry_run and (nye or status_oppdatert or utfall_lost):
        skriv_json(sti, list(per_id.values()))
    return {'nye': nye, 'status_oppdatert': status_oppdatert, 'utfall_lost_opp': utfall_lost,
            'total': len(per_id)}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--dry-run', action='store_true', help='Vis hva som ville blitt gjort, ikke skriv til disk')
    p.add_argument('--sesjon', default='inneværende', help='Default: inneværende (løses dynamisk fra dagens dato)')
    args = p.parse_args()

    sesjon = resolve_sesjon(args.sesjon)
    print(f"Oppdaterer sesjon {sesjon}{' (dry-run)' if args.dry_run else ''}...", file=sys.stderr)

    resultat = {'sesjon': sesjon, 'dry_run': args.dry_run}

    print("  henter og oppdaterer sporsmal...", file=sys.stderr)
    resultat['sporsmal'] = oppdater_sporsmal(sesjon, args.dry_run)

    print("  henter stortingsvedtak (for anmodningsvedtak + representantforslag-utfall)...", file=sys.stderr)
    vedtak_root = hent_sesjon_xml('stortingsvedtak', sesjon)

    print("  oppdaterer anmodningsvedtak...", file=sys.stderr)
    resultat['anmodningsvedtak'] = oppdater_anmodningsvedtak(sesjon, args.dry_run, vedtak_root)

    print("  bygger vedtak-oppslag og oppdaterer representantforslag...", file=sys.stderr)
    vedtak_oppslag = bygg_vedtak_oppslag([vedtak_root])
    print("  henter saker (representantforslag)...", file=sys.stderr)
    saker_root = hent_sesjon_xml('saker', sesjon)
    resultat['representantforslag'] = oppdater_representantforslag(sesjon, args.dry_run, vedtak_oppslag, saker_root)

    print(json.dumps(resultat, ensure_ascii=False, indent=2))

    s = resultat['sporsmal']
    a = resultat['anmodningsvedtak']
    r = resultat['representantforslag']
    print(
        f"\nOppsummering: sporsmal +{s['nye']} nye, {s['oppdatert']} oppdatert (status endret). "
        f"anmodningsvedtak +{a['nye']} nye. "
        f"representantforslag +{r['nye']} nye, {r['status_oppdatert']} statusendret, "
        f"{r['utfall_lost_opp']} fikk avklart utfall (på tvers av sesjoner).",
        file=sys.stderr,
    )


if __name__ == '__main__':
    main()
