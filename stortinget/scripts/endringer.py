#!/usr/bin/env python3
"""
Lister hva nattoppdateringen har brakt inn: nye spørsmål, anmodningsvedtak,
representantforslag, saker i arbeids- og sosialkomiteen og forslag fra voteringene
i dem, og spørsmål som har fått svar. Sammenligner datafilene i arbeidskopien med siste commit (HEAD), så det må kjøres etter
oppdater_inkrementell.py og før endringene committes.

Statusendringer ellers (trukket, bortfalt, utfall o.l.) tas ikke med.
Resultatet skrives til stortinget/siste-endringer.json og leses av varselet
om nye stortingssaker.

Bruk:
  python3 endringer.py                # skriv stortinget/siste-endringer.json
  python3 endringer.py --ut -         # skriv til stdout
"""
import argparse
import json
import os
import subprocess
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from felles import MINISTER_TITTEL, SPORSMAL_TYPE_NAVN, SPORSMAL_URL_MONSTER  # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # mappen stortinget/
ROT = os.path.dirname(BASE)
DATATYPER = ['sporsmal', 'anmodningsvedtak', 'representantforslag', 'saker', 'forslag']


def git(*args):
    return subprocess.run(['git', *args], cwd=ROT, capture_output=True, text=True, check=True).stdout


def endrede_filer(datatype):
    """Datafiler (relative til repoet) som er endret eller nye siden HEAD."""
    sti = f'stortinget/data/{datatype}'
    endret = git('diff', '--name-only', 'HEAD', '--', sti).split()
    nye = git('ls-files', '--others', '--exclude-standard', '--', sti).split()
    return [f for f in endret + nye if f.endswith('.json')]


def les_for_og_etter(fil):
    try:
        for_ = json.loads(git('show', f'HEAD:{fil}'))
    except subprocess.CalledProcessError:
        for_ = []  # ny sesjonsfil
    with open(os.path.join(ROT, fil), encoding='utf-8') as f:
        etter = json.load(f)
    return {x['id']: x for x in for_}, etter


def sporsmal_post(v):
    return {
        'id': v['id'],
        'type': SPORSMAL_TYPE_NAVN.get(v.get('type'), v.get('type')),
        'dato': (v.get('dato') or '')[:10],
        'tittel': (v.get('tittel') or '').strip(),
        'fra': f"{v.get('fra_navn')} ({v.get('fra_parti')})",
        'til_minister_id': v.get('til_minister_id'),
        'til': MINISTER_TITTEL.get(v.get('til_minister_id'), v.get('til_minister_id')),
        'besvart_av': v.get('besvart_av_navn'),
        'status': v.get('status'),
        'emne': v.get('emne') or [],
        'lenke': SPORSMAL_URL_MONSTER[v['type']].format(v['legacy_id'])
        if v.get('legacy_id') and v.get('type') in SPORSMAL_URL_MONSTER else None,
    }


def finn_endringer():
    ut = {'dato': date.today().isoformat(),
          'nye': {d: [] for d in DATATYPER},
          'besvart': []}
    for datatype in DATATYPER:
        for fil in endrede_filer(datatype):
            for_, etter = les_for_og_etter(fil)
            for v in etter:
                gammel = for_.get(v['id'])
                if datatype == 'sporsmal':
                    if gammel is None:
                        ut['nye'][datatype].append(sporsmal_post(v))
                    elif v.get('status') == 'besvart' and gammel.get('status') != 'besvart':
                        ut['besvart'].append(sporsmal_post(v))
                elif gammel is None:
                    ut['nye'][datatype].append(v)
    ut['antall'] = {**{d: len(ut['nye'][d]) for d in DATATYPER}, 'besvart': len(ut['besvart'])}
    return ut


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--ut', default=os.path.join(BASE, 'siste-endringer.json'))
    args = ap.parse_args()
    ut = finn_endringer()
    tekst = json.dumps(ut, ensure_ascii=False, indent=1)
    if args.ut == '-':
        print(tekst)
    else:
        with open(args.ut, 'w', encoding='utf-8') as f:
            f.write(tekst + '\n')
    print(f"Endringer: {ut['antall']}", file=sys.stderr)


if __name__ == '__main__':
    main()
