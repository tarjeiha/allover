#!/usr/bin/env python3
"""
Saker fra arbeids- og sosialkomiteen og forslagene som ble votert over i dem.

To datatyper:
- saker:   alle saker komiteen har hatt (proposisjoner, meldinger, representantforslag,
           budsjett m.m.), med vedtaksteksten fra Stortingets vedtaksliste der den finnes.
- forslag: mindretallsforslag og løse forslag fra voteringene i de samme sakene, med parti
           og om forslaget ble vedtatt. Komiteens tilråding tas ikke med (den er vedtaket).
           Voteringer finnes hos Stortinget fra sesjon 2011-2012.

Eldre enkeltsaker (f.eks. uførereformen) legges inn ved å føre sak-id-en i
stortinget/enkeltsaker.txt. Sak-id-en er tallet etter ?p= i adressen til saken på stortinget.no.

Bruk:
  python3 komitesaker.py                          # inneværende sesjon + enkeltsaker
  python3 komitesaker.py --sesjon forrige
  python3 komitesaker.py --fra 2013-2014          # alle sesjoner fra og med 2013-2014 (engangsjobb)
  python3 komitesaker.py --dry-run

Forslag hentes bare for saker som er ferdigbehandlet, og bare én gang per sak
(feltet forslag_hentet). Output: ett JSON-objekt på stdout som oppsummerer endringene.
"""
import argparse
import html
import json
import os
import re
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from felles import (  # noqa: E402
    NS, t, hent_xml, hent_sesjon_xml, parse_saker_liste, parse_stortingsvedtak_liste,
    vedtak_tekst, resolve_sesjon, sesjon_for_dato, last_json, skriv_json,
)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # mappen stortinget/
DATA = os.path.join(BASE, 'data')
ENKELTSAKER = os.path.join(BASE, 'enkeltsaker.txt')

KOMITEER = {'ARBSOS'}
MAKS_TEKST = 3000      # tegn per vedtaks- eller forslagstekst; budsjettvedtak kan være svært lange
MAKS_VEDTAK = 5        # vedtak per sak
SAK_URL = "https://www.stortinget.no/no/Saker-og-publikasjoner/Saker/Sak/?p={}"


def ren_tekst(raa):
    tekst = ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', raa or '')).split())
    return tekst if len(tekst) <= MAKS_TEKST else tekst[:MAKS_TEKST].rsplit(' ', 1)[0] + ' […]'


def emner_av(el):
    liste = el.find(f"{NS}emne_liste")
    return [t(e, 'navn') for e in liste if t(e, 'navn')] if liste is not None else []


def vedtak_per_sak(vedtak_root):
    ut = {}
    for v in parse_stortingsvedtak_liste(vedtak_root):
        sak_id = t(v, 'sak_id')
        tekst = vedtak_tekst(v)
        if sak_id and tekst:
            liste = ut.setdefault(sak_id, [])
            if len(liste) < MAKS_VEDTAK:
                liste.append(tekst if len(tekst) <= MAKS_TEKST else tekst[:MAKS_TEKST].rsplit(' ', 1)[0] + ' […]')
    return ut


def sak_record(sak, sesjon, vedtak):
    idv = t(sak, 'id')
    komite_el = sak.find(f"{NS}komite")
    return {
        'id': idv,
        'sesjon': t(sak, 'behandlet_sesjon_id') or t(sak, 'sak_sesjon') or sesjon or 'ukjent',
        'dokumentgruppe': t(sak, 'dokumentgruppe'),
        'type': t(sak, 'type'),
        'tittel': t(sak, 'tittel'),
        'korttittel': t(sak, 'korttittel'),
        'henvisning': t(sak, 'henvisning'),
        'komite': t(komite_el, 'navn') if komite_el is not None else None,
        'emne': emner_av(sak),
        'status': t(sak, 'status'),
        'vedtak': vedtak.get(idv, []),
        'sak_url': SAK_URL.format(idv),
    }


def hent_forslag(sak_rec):
    """Mindretallsforslag og løse forslag fra voteringene i én sak."""
    try:
        root = hent_xml(f"https://data.stortinget.no/eksport/voteringer?sakid={sak_rec['id']}")
    except RuntimeError:
        return None
    liste = root.find(f"{NS}sak_votering_liste")
    ut = []
    for vo in (liste if liste is not None else []):
        vid = t(vo, 'votering_id')
        try:
            froot = hent_xml(f"https://data.stortinget.no/eksport/voteringsforslag?voteringid={vid}")
        except RuntimeError:
            return None
        fliste = froot.find(f"{NS}voteringsforslag_liste")
        for f in (fliste if fliste is not None else []):
            if (t(f, 'forslag_type') or '') == 'tilraading':
                continue
            pliste = f.find(f"{NS}forslag_levert_av_parti_liste")
            antall_for, antall_mot = t(vo, 'antall_for'), t(vo, 'antall_mot')
            ut.append({
                'id': t(f, 'forslag_id'),
                'sak_id': sak_rec['id'],
                'sesjon': sak_rec['sesjon'],
                'dato': (t(vo, 'votering_tid') or '')[:10],
                'sak_tittel': sak_rec['korttittel'] or sak_rec['tittel'],
                'henvisning': sak_rec['henvisning'],
                'forslag_type': t(f, 'forslag_type'),
                'betegnelse': ' '.join((t(f, 'forslag_betegnelse') or '').split()),
                'partier': sorted(t(p, 'id') for p in pliste if t(p, 'id')) if pliste is not None else [],
                'tekst': ren_tekst(t(f, 'forslag_tekst')),
                'vedtatt': t(vo, 'vedtatt') == 'true',
                'resultat': t(vo, 'votering_resultat_type_tekst'),
                'antall_for': int(antall_for) if antall_for and int(antall_for) >= 0 else None,
                'antall_mot': int(antall_mot) if antall_mot and int(antall_mot) >= 0 else None,
                'sak_url': sak_rec['sak_url'],
            })
    return ut


def les_enkeltsaker():
    if not os.path.exists(ENKELTSAKER):
        return []
    ider = []
    with open(ENKELTSAKER, encoding='utf-8') as f:
        for linje in f:
            linje = linje.split('#', 1)[0].strip()
            if linje.isdigit():
                ider.append(linje)
    return ider


def hent_enkeltsak(sak_id, vedtak_cache):
    try:
        root = hent_xml(f"https://data.stortinget.no/eksport/sak?sakid={sak_id}")
    except RuntimeError:
        return None
    sesjon = t(root, 'sak_sesjon')
    if sesjon and sesjon not in vedtak_cache:
        try:
            vedtak_cache[sesjon] = vedtak_per_sak(hent_sesjon_xml('stortingsvedtak', sesjon))
        except RuntimeError:
            vedtak_cache[sesjon] = {}
    rec = sak_record(root, sesjon, vedtak_cache.get(sesjon, {}))
    rec['enkeltsak'] = True
    return rec


def oppdater(sesjoner, dry_run=False):
    saker_sti, forslag_sti = os.path.join(DATA, 'saker'), os.path.join(DATA, 'forslag')
    saker = {x['id']: x for x in last_json(saker_sti)}
    forslag = {x['id']: x for x in last_json(forslag_sti)}
    nye_saker = endrede_saker = nye_forslag = 0
    vedtak_cache = {}

    kandidater = []
    for sesjon in sesjoner:
        vedtak_cache[sesjon] = vedtak_per_sak(hent_sesjon_xml('stortingsvedtak', sesjon))
        for sak in parse_saker_liste(hent_sesjon_xml('saker', sesjon)):
            komite_el = sak.find(f"{NS}komite")
            if komite_el is not None and t(komite_el, 'id') in KOMITEER:
                kandidater.append(sak_record(sak, sesjon, vedtak_cache[sesjon]))
    for sak_id in les_enkeltsaker():
        if sak_id not in saker:
            rec = hent_enkeltsak(sak_id, vedtak_cache)
            if rec:
                kandidater.append(rec)

    for rec in kandidater:
        gammel = saker.get(rec['id'])
        if gammel is None:
            nye_saker += 1
        else:
            rec['forslag_hentet'] = gammel.get('forslag_hentet', False)
            rec['enkeltsak'] = gammel.get('enkeltsak', rec.get('enkeltsak', False))
            if not rec['vedtak']:
                rec['vedtak'] = gammel.get('vedtak', [])
            if rec == gammel:
                continue
            endrede_saker += 1
        rec.setdefault('forslag_hentet', False)
        rec.setdefault('enkeltsak', False)
        if rec['status'] == 'behandlet' and not rec['forslag_hentet']:
            funnet = hent_forslag(rec)
            if funnet is not None:
                for f in funnet:
                    if f['id'] and f['id'] not in forslag:
                        nye_forslag += 1
                    forslag[f['id']] = f
                rec['forslag_hentet'] = True
        saker[rec['id']] = rec

    if not dry_run and (nye_saker or endrede_saker or nye_forslag):
        skriv_json(saker_sti, list(saker.values()))
        skriv_json(forslag_sti, list(forslag.values()))
    return {'saker': {'nye': nye_saker, 'endret': endrede_saker, 'total': len(saker)},
            'forslag': {'nye': nye_forslag, 'total': len(forslag)}}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--sesjon', default='inneværende')
    p.add_argument('--fra', help='Første sesjon i en engangsjobb, f.eks. 2013-2014. Kjører til og med inneværende.')
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args()
    if args.fra:
        start, slutt = int(args.fra[:4]), int(sesjon_for_dato(date.today())[:4])
        sesjoner = [f'{a}-{a + 1}' for a in range(start, slutt + 1)]
    else:
        sesjoner = [resolve_sesjon(args.sesjon)]
    print(f"Komitésaker for {', '.join(sesjoner)}{' (dry-run)' if args.dry_run else ''}...", file=sys.stderr)
    print(json.dumps(oppdater(sesjoner, args.dry_run), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
