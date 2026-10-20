#!/usr/bin/env python3
"""
Søk på tvers av fire datatyper fra Stortinget (sesjon 2013-2014 t.o.m. sist oppdaterte sesjon):
anmodningsvedtak, spørsmål (skriftlig/interpellasjon/spørretime), og representantforslag.

Bruk:
  python3 sok_stortinget.py --query "uføretrygd"                                    # søker i alle typer
  python3 sok_stortinget.py --datatype anmodningsvedtak --komite "Arbeids- og sosialkomiteen" --sesjon forrige
  python3 sok_stortinget.py --datatype sporsmal --sporsmalstype skriftlig_sporsmal --query "dagpenger"
  python3 sok_stortinget.py --datatype sporsmal --minister "arbeids- og inkluderingsministeren"
  python3 sok_stortinget.py --datatype representantforslag --utfall avvist --parti SV
  python3 sok_stortinget.py --id 40018174 --datatype anmodningsvedtak

Felles filtre: --query (fritekst), --sesjon (eksakt eller "inneværende"/"forrige"), --emne, --limit, --format, --sorter
Type-spesifikke filtre: --komite (anmodningsvedtak+representantforslag), --minister (sporsmal),
--sporsmalstype (sporsmal), --parti (representantforslag), --utfall (representantforslag)

--sesjon aksepterer eksakt sesjon-id (f.eks. 2024-2025) ELLER "inneværende"/"forrige", regnet ut fra
dagens dato (Stortingets sesjon løper 1. oktober-30. september).

Sortering: ved --query rangeres treff etter relevans (tittel > stikkord[kun anmodningsvedtak, korte
lister] > tekst), med nyeste dato som sekundærnøkkel. Uten --query sorteres på dato, nyeste først.

Visning tilpasses antall treff automatisk (full detalj ved få treff, kompakt liste ved mange).
"""
import argparse
import json
import sys
import os
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from felles import (  # noqa: E402
    MINISTER_TITTEL, SPORSMAL_TYPE_NAVN, SPORSMAL_URL_MONSTER,
    STIKKORD_PÅLITELIG_GRENSE, resolve_sesjon,
)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # mappen stortinget/
DATA_MAPPER = {
    'anmodningsvedtak': os.path.join(BASE, 'data', 'anmodningsvedtak'),
    'sporsmal': os.path.join(BASE, 'data', 'sporsmal'),
    'representantforslag': os.path.join(BASE, 'data', 'representantforslag'),
    'saker': os.path.join(BASE, 'data', 'saker'),
    'forslag': os.path.join(BASE, 'data', 'forslag'),
}
ALLE_DATATYPER = list(DATA_MAPPER)

FULL_DETALJ_GRENSE = 5
MEDIUM_DETALJ_GRENSE = 20
# MINISTER_TITTEL, SPORSMAL_TYPE_NAVN, SPORSMAL_URL_MONSTER, STIKKORD_PÅLITELIG_GRENSE:
# se scripts/felles.py — delt med oppdater_inkrementell.py og backfill_sesjon.py, ikke
# duplisert her (se endringslogg 2026-09-16).


_cache = {}


def last(datatype, sesjon=None):
    """Leser data for en datatype fra data/<datatype>/<sesjon>.json (én fil per sesjon).
    Med `sesjon` leses bare den ene filen."""
    nokkel = (datatype, sesjon)
    if nokkel not in _cache:
        mappe = DATA_MAPPER[datatype]
        if not os.path.isdir(mappe):
            print(f"Feil: finner ikke {mappe}. Hent mappen stortinget/ fra repoet tarjeiha/allover "
                  f"(git clone --depth 1 --filter=blob:none --sparse, deretter git sparse-checkout set stortinget).",
                  file=sys.stderr)
            sys.exit(1)
        filer = [f'{sesjon}.json'] if sesjon else sorted(f for f in os.listdir(mappe) if f.endswith('.json'))
        data = []
        for navn in filer:
            sti = os.path.join(mappe, navn)
            if os.path.exists(sti):
                with open(sti, encoding='utf-8') as f:
                    data.extend(json.load(f))
        for v in data:
            v['_datatype'] = datatype
        _cache[nokkel] = data
    return _cache[nokkel]


def egen_sesjon(v):
    """Feltnavnet for sesjon varierer per datatype."""
    return v.get('sesjon') or v.get('sesjon_fremmet')


# Synonymer og skrivemåter for AIDs fagord, inkludert nynorsk. Står ett av uttrykkene i
# søket, holder det at ett av uttrykkene i samme gruppe finnes i posten. Hold gruppene
# smale: et uttrykk skal kunne erstatte et annet uten å endre hva søket handler om.
SYNONYMER = [
    ['aap', 'arbeidsavklaringspenger', 'arbeidsavklaringspengar'],
    ['nav', 'arbeids- og velferdsetaten', 'arbeids- og velferdsforvaltningen'],
    ['sykepenger', 'sjukepengar', 'sykelønn', 'sjukeløn'],
    ['sykmelding', 'sykemelding', 'sjukmelding', 'sykmeldt', 'sykemeldt', 'sjukmeld'],
    ['sykefravær', 'sjukefråvær'],
    ['dagpenger', 'dagpengar'],
    ['foreldrepenger', 'foreldrepengar'],
    ['fedrekvote', 'pappaperm', 'fedrekvoten'],
    ['uføretrygd', 'uførepensjon', 'uføreytelse'],
    ['omstillingsstønad', 'etterlattepensjon', 'gjenlevendepensjon', 'etterlatteytelse'],
    ['yrkesskade', 'arbeidsskade', 'yrkessjukdom', 'yrkessykdom'],
    ['afp', 'avtalefestet pensjon', 'avtalefesta pensjon'],
    ['tjenestepensjon', 'tenestepensjon'],
    ['arbeidsledighet', 'arbeidsløshet', 'arbeidsløyse', 'ledighet'],
    ['arbeidsledig', 'arbeidsløs', 'ledige'],
    ['sosialhjelp', 'økonomisk stønad', 'økonomisk sosialhjelp'],
    ['arbeidslivskriminalitet', 'a-krim'],
    ['ia-avtalen', 'inkluderende arbeidsliv', 'ia-avtale'],
    ['innleie', 'bemanningsbyrå', 'bemanningsforetak', 'bemanningsbransjen'],
    ['introduksjonsprogram', 'introduksjonsprogrammet', 'introprogram'],
    ['statsborgerskap', 'statsborgarskap'],
    ['fordrevne fra ukraina', 'ukrainske flyktninger', 'flyktninger fra ukraina'],
    ['arbeidsmiljøloven', 'aml'],
]
_SYNONYM_OPPSLAG = {uttrykk: gruppe for gruppe in SYNONYMER for uttrykk in gruppe}
_MIN_LEDD = 4  # korteste ledd når et sammensatt søkeord deles opp


def del_sammensatte(krav, tekster):
    """Et søkeord som ikke finnes i noen post, deles i to ledd (pårørendestøtte -> pårørende
    + støtte), med eller uten fugebokstav (s/e). Blant delingene der begge leddene står i
    samme post, velges den jevneste. Returnerer nye krav og en liste over delingene som ble gjort."""
    nye, delt = [], []
    for krav_ in krav:
        ord_ = krav_[0][0] if len(krav_) == 1 and len(krav_[0]) == 1 else None
        if not ord_ or any(ord_ in t for t in tekster):
            nye.append(krav_)
            continue
        beste = None
        for i in range(_MIN_LEDD, len(ord_) - _MIN_LEDD + 1):
            etterledd = ord_[i:]
            kandidater = [ord_[:i]] + ([ord_[:i - 1]] if ord_[i - 1] in 'se' and i - 1 >= _MIN_LEDD else [])
            for forledd in kandidater:
                if any(forledd in t and etterledd in t for t in tekster):
                    jevnhet = min(len(forledd), len(etterledd))
                    if not beste or jevnhet > beste[0]:
                        beste = (jevnhet, forledd, etterledd)
        if beste:
            nye.append([[beste[1], beste[2]]])
            delt.append(f'«{ord_}» som «{beste[1]}» + «{beste[2]}»')
        else:
            nye.append(krav_)
    return nye, delt


def sokekrav(q):
    """Deler søket i krav. Hvert krav er en liste av alternativer, og hvert alternativ en
    liste av ord som alle må finnes. Kjente uttrykk fra SYNONYMER blir ett krav med hele
    gruppen som alternativer, de øvrige ordene ett krav hver."""
    rest = f' {q} '
    krav = []
    for uttrykk in sorted(_SYNONYM_OPPSLAG, key=len, reverse=True):
        if f' {uttrykk} ' in rest:
            rest = rest.replace(f' {uttrykk} ', ' ')
            krav.append([alt.split() for alt in _SYNONYM_OPPSLAG[uttrykk]])
    krav += [[[ord_]] for ord_ in rest.split()]
    return krav


def sokbar_tekst(v):
    dt = v['_datatype']
    if dt == 'anmodningsvedtak':
        felter = [v['tittel'], v['tekst']]
        if len(v['stikkord']) <= STIKKORD_PÅLITELIG_GRENSE:
            felter += v['stikkord']
    elif dt == 'sporsmal':
        felter = [v['tittel']] + v.get('emne', [])
    elif dt == 'saker':
        felter = [v['tittel'], v.get('korttittel'), v.get('henvisning')] + v.get('emne', []) + v.get('vedtak', [])
    elif dt == 'forslag':
        felter = [v['tekst'], v.get('sak_tittel'), v.get('betegnelse')]
    else:  # representantforslag
        felter = [v['tittel'], v.get('utfall_tekst') or '']
    return ' '.join((felt or '').lower() for felt in felter)


def matcher_tekstfelt(v, krav):
    # Ordbasert AND fremfor fraseoverensstemmelse: alle ord i søket må finnes et sted i
    # feltene (uansett rekkefølge/felt), ikke som sammenhengende substring i ett felt.
    # Kjente fagord utvides med synonymer (SYNONYMER), og sammensatte ord uten treff deles
    # opp (del_sammensatte). Begge deler utvider treffmengden, aldri innskrenker den.
    samlet = v.get('_tekst') or sokbar_tekst(v)
    return all(any(all(ord_ in samlet for ord_ in alternativ) for alternativ in krav_) for krav_ in krav)


def treffer(v, args):
    dt = v['_datatype']
    if args.id and v['id'] != args.id:
        return False
    if args.sesjon and egen_sesjon(v) != args.sesjon:
        return False
    if args.emne:
        if not any(args.emne.lower() in e.lower() for e in v.get('emne', [])):
            return False
    if args.komite:
        if dt not in ('anmodningsvedtak', 'representantforslag', 'saker'):
            return False
        if not v.get('komite') or args.komite.lower() not in v['komite'].lower():
            return False
    if args.minister:
        if dt != 'sporsmal':
            return False
        mid = v.get('til_minister_id') or ''
        tittel = MINISTER_TITTEL.get(mid, '')
        if args.minister.lower() not in (tittel + mid).lower():
            return False
    if args.sporsmalstype:
        kode = {'skriftlig_sporsmal': 's', 'interpellasjon': 'i', 'sporretime_sporsmal': 'm'}.get(args.sporsmalstype)
        if dt != 'sporsmal' or v.get('type') != kode:
            return False
    if args.status:
        if dt != 'sporsmal' or (v.get('status') or 'besvart') != args.status:
            return False
    if args.parti:
        if dt == 'forslag':
            partier = v.get('partier', [])
        elif dt == 'representantforslag':
            partier = [p.get('parti') or '' for p in v.get('forslagstillere', [])]
        else:
            return False
        if not any(args.parti.lower() == p.lower() for p in partier):
            return False
    if args.utfall:
        if dt != 'representantforslag' or v.get('utfall') != args.utfall:
            return False
    if args.sak_id and v.get('sak_id', v['id']) != args.sak_id:
        return False
    if args.query:
        if not matcher_tekstfelt(v, args.krav):
            return False
    return True


def relevans_niva(v, query):
    q = query.lower()
    if q in (v.get('tittel') or v.get('tekst') or '').lower():
        return 0
    if v['_datatype'] == 'anmodningsvedtak' and len(v['stikkord']) <= STIKKORD_PÅLITELIG_GRENSE:
        if any(q in s.lower() for s in v['stikkord']):
            return 1
    if v['_datatype'] == 'sporsmal' and any(q in e.lower() for e in v.get('emne', [])):
        return 1
    return 2


def dato_for_sortering(v):
    dt = v['_datatype']
    if dt == 'anmodningsvedtak':
        return v['dato']
    if dt in ('sporsmal', 'forslag'):
        return v.get('dato') or ''
    if dt == 'saker':
        return v.get('sesjon') or ''
    return v.get('behandlet_sesjon') or v.get('sesjon_fremmet') or ''


def sorter(treff, args):
    if args.sorter == 'dato_stigende':
        return sorted(treff, key=dato_for_sortering)
    if args.sorter == 'dato_synkende':
        return sorted(treff, key=dato_for_sortering, reverse=True)
    if args.query and args.sorter in ('auto', 'relevans'):
        return sorted(treff, key=lambda v: (relevans_niva(v, args.query), tuple(-ord(c) for c in dato_for_sortering(v) or '')))
    return sorted(treff, key=dato_for_sortering, reverse=True)


def fmt_anmodningsvedtak(v, full):
    hode = f"[{v['sesjon']}] vedtak nr. {v['vedtak_nummer']} ({v['dato'][:10]}) — {v['komite'] or 'komité ukjent'}"
    if full == 'full':
        return f"{hode}\n  Sak: {v['tittel']}\n  {v['tekst']}\n  Lenke: {v['vedtak_url']}"
    if full == 'medium':
        tekst = v['tekst'] if len(v['tekst']) <= 200 else v['tekst'][:200].rsplit(' ', 1)[0] + ' […]'
        return f"{hode} — {v['tittel']}\n  {tekst}\n  {v['vedtak_url']}"
    tekst = v['tekst'] if len(v['tekst']) <= 90 else v['tekst'][:90].rsplit(' ', 1)[0] + '…'
    return f"{v['dato'][:10]} [{v['komite'] or 'ukjent'}] {tekst} — {v['vedtak_url']}"


def fmt_sporsmal(v, full):
    typenavn = SPORSMAL_TYPE_NAVN[v['type']]
    fra = f"{v.get('fra_navn') or 'ukjent'} ({v.get('fra_parti') or '?'})"
    til = MINISTER_TITTEL.get(v.get('til_minister_id') or '', v.get('til_minister_id') or 'ukjent statsråd')
    dato = (v.get('dato') or '')[:10]
    url = SPORSMAL_URL_MONSTER[v['type']].format(v['legacy_id']) if v.get('legacy_id') else '(lenke mangler — bruk id ved oppslag)'
    status = v.get('status') or 'besvart'
    status_merke = '' if status == 'besvart' else f" [{status.upper().replace('_', ' ')}]"
    tittel_merke = ' (tittel ikke fastsatt av Stortinget ennå)' if v.get('tittel_midlertidig') else ''
    if full == 'full':
        return (f"[{v['sesjon']}] {typenavn} nr. {v['sporsmal_nummer']} ({dato}) — fra {fra} til {til}{status_merke}\n"
                f"  {v['tittel']}{tittel_merke}\n  Status: {status}\n  Lenke: {url}")
    if full == 'medium':
        tekst = v['tittel'] if len(v['tittel']) <= 200 else v['tittel'][:200].rsplit(' ', 1)[0] + ' […]'
        return f"[{v['sesjon']}] {typenavn}{status_merke} — {dato} — fra {fra} til {til}\n  {tekst}{tittel_merke}\n  {url}"
    tekst = v['tittel'] if len(v['tittel']) <= 90 else v['tittel'][:90].rsplit(' ', 1)[0] + '…'
    return f"{dato} [{typenavn}, {til}]{status_merke} {tekst} — {url}"


def fmt_representantforslag(v, full):
    forslagstillere = ', '.join(f"{p['navn']} ({p['parti']})" for p in v.get('forslagstillere', [])[:3])
    if full == 'full':
        return (f"[{v['sesjon_fremmet']}] {v['tittel']}\n  Fremmet av: {forslagstillere}\n  Komité: {v.get('komite') or 'ukjent'} | "
                f"Utfall: {v['utfall']}\n  {v.get('utfall_tekst') or '(ingen vedtakstekst funnet)'}\n  Lenke: {v['sak_url']}")
    if full == 'medium':
        return f"[{v['sesjon_fremmet']}] {v['tittel']} — Utfall: {v['utfall']}\n  Fremmet av: {forslagstillere}\n  {v['sak_url']}"
    return f"{v['sesjon_fremmet']} [{v['utfall']}] {v['tittel'][:80]} — {v['sak_url']}"


def kort(tekst, n):
    return tekst if len(tekst) <= n else tekst[:n].rsplit(' ', 1)[0] + ' […]'


def fmt_saker(v, full):
    hode = f"[{v['sesjon']}] {v.get('henvisning') or v.get('dokumentgruppe') or ''} — {v['status']}"
    if full == 'full':
        vedtak = '\n  '.join(kort(x, 600) for x in v.get('vedtak', [])) or '(ingen vedtakstekst i Stortingets vedtaksliste, se saken)'
        return f"{hode}\n  {v['tittel']}\n  Emne: {', '.join(v.get('emne', [])) or '–'}\n  Vedtak: {vedtak}\n  Lenke: {v['sak_url']}"
    if full == 'medium':
        return f"{hode}\n  {v.get('korttittel') or v['tittel']}\n  {v['sak_url']}"
    return f"{v['sesjon']} {kort(v.get('korttittel') or v['tittel'], 90)} — {v['sak_url']}"


def fmt_forslag(v, full):
    utfall = 'vedtatt' if v.get('vedtatt') else 'ikke vedtatt'
    stemmer = f", {v['antall_for']} mot {v['antall_mot']}" if v.get('antall_for') is not None else ''
    hode = f"[{v['sesjon']}] {v['dato']} — {v.get('betegnelse') or v.get('forslag_type')} — {utfall}{stemmer}"
    if full == 'full':
        return f"{hode}\n  Sak: {v.get('sak_tittel')} ({v.get('henvisning') or ''})\n  {v['tekst']}\n  Lenke: {v['sak_url']}"
    if full == 'medium':
        return f"{hode}\n  {kort(v['tekst'], 200)}\n  {v['sak_url']}"
    return f"{v['dato']} [{'/'.join(v.get('partier', [])) or '?'}, {utfall}] {kort(v['tekst'], 90)} — {v['sak_url']}"


FORMATTERE = {'anmodningsvedtak': fmt_anmodningsvedtak, 'sporsmal': fmt_sporsmal, 'representantforslag': fmt_representantforslag,
              'saker': fmt_saker, 'forslag': fmt_forslag}


def main():
    p = argparse.ArgumentParser(description='Søk på tvers av Stortingets anmodningsvedtak, spørsmål, representantforslag, '
                                            'saker i arbeids- og sosialkomiteen og forslag fra voteringene i dem')
    p.add_argument('--query')
    p.add_argument('--sesjon')
    p.add_argument('--emne')
    p.add_argument('--komite', help='Anmodningsvedtak, representantforslag og saker')
    p.add_argument('--minister', help='Spørsmål — substring i statsrådens tittel/id')
    p.add_argument('--sporsmalstype', choices=['skriftlig_sporsmal', 'interpellasjon', 'sporretime_sporsmal'])
    p.add_argument('--status', choices=['besvart', 'til_behandling', 'trukket', 'bortfalt'],
                    help='Spørsmål — filtrer på status. Default: alle statuser vises (bruk denne for kun ubesvarte, f.eks. --status til_behandling).')
    p.add_argument('--parti', help='Representantforslag og forslag — eksakt partikode, f.eks. SV, A, H')
    p.add_argument('--sak-id', dest='sak_id', help='Saker og forslag — alt som hører til én sak (tallet etter ?p= på stortinget.no)')
    p.add_argument('--utfall', choices=['vedtatt (anmodning)', 'avvist', 'annet', 'ukjent'], help='Representantforslag')
    p.add_argument('--id')
    p.add_argument('--datatype', choices=ALLE_DATATYPER, action='append',
                    help='Kan gjentas for flere typer. Default: søk i alle.')
    p.add_argument('--limit', type=int, default=50)
    p.add_argument('--format', choices=['json', 'kort'], default='kort')
    p.add_argument('--sorter', choices=['auto', 'dato_stigende', 'dato_synkende', 'relevans'], default='auto')
    args = p.parse_args()

    if args.sesjon:
        args.sesjon = resolve_sesjon(args.sesjon)

    datatyper = args.datatype or ALLE_DATATYPER
    datatyper = [dt for dt in datatyper if os.path.isdir(DATA_MAPPER[dt]) or args.datatype]

    if not any([args.query, args.sesjon, args.komite, args.emne, args.id, args.minister, args.parti, args.utfall, args.sporsmalstype, args.sak_id]):
        print("Feil: minst ett søkekriterium må angis", file=sys.stderr)
        sys.exit(1)

    alle_data = []
    for dt in datatyper:
        alle_data.extend(last(dt, args.sesjon) if args.sesjon else last(dt))

    kjente_sesjoner = sorted({f[:-5] for dt in datatyper for f in os.listdir(DATA_MAPPER[dt]) if f.endswith('.json')})
    if args.sesjon and args.sesjon not in kjente_sesjoner:
        print(f"MERK: Indeksen har ingen poster for sesjon {args.sesjon}. Dekker {kjente_sesjoner[0]} t.o.m. {kjente_sesjoner[-1]}. "
              f"Er sesjonen nyere, er dataene ikke oppdatert ennå (se oppdatering.md).\n", file=sys.stderr)

    if args.query:
        for v in alle_data:
            v['_tekst'] = sokbar_tekst(v)
        args.krav, delt = del_sammensatte(sokekrav(args.query.lower()), [v['_tekst'] for v in alle_data])
        if delt:
            print(f"MERK: ingen poster har {', '.join(delt)}. Søkte på leddene hver for seg.\n", file=sys.stderr)
    treff = [v for v in alle_data if treffer(v, args)]
    for v in alle_data:
        v.pop('_tekst', None)
    treff = sorter(treff, args)
    total = len(treff)
    vist = treff[:args.limit]

    if args.format == 'kort':
        print(f"Antall treff: {total} (viser {len(vist)})")
        if total > len(vist):
            print(f"MERK: {total - len(vist)} treff til er ikke vist. Snevre inn eller øk --limit.")
        if args.emne:
            print("MERK: emne-feltet har varierende dekning (ikke alle poster har emne registrert).")
        if 'representantforslag' in datatyper and any(v['_datatype'] == 'representantforslag' for v in vist):
            print("MERK: representantforslag-utfall er ~83% dekket (vedtatt/avvist); resten er 'annet' (vis rå vedtakstekst) eller 'ukjent'.")
        if 'sporsmal' in datatyper and any(v['_datatype'] == 'sporsmal' and v.get('status') != 'besvart' for v in vist):
            print("MERK: treffene inkluderer spørsmål/interpellasjoner som ikke er besvart ennå (til_behandling/trukket/bortfalt) — se statusmerke i [ ]. Filtrer med --status ved behov.")
        print()
        if total <= FULL_DETALJ_GRENSE:
            niva = 'full'
        elif total <= MEDIUM_DETALJ_GRENSE:
            niva = 'medium'
        else:
            niva = 'kompakt'
        for v in vist:
            print(FORMATTERE[v['_datatype']](v, niva))
            print()
    else:
        for v in vist:
            v.pop('_datatype', None)
        print(json.dumps({'total_treff': total, 'vist': len(vist), 'sesjon_oppslatt_til': args.sesjon, 'vedtak': vist}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
