"""
Felles bibliotek for aid-stortinget-fra2021: XML-parsing, berikelse og
minister/URL-oppslag delt mellom søkeskriptet (sok_stortinget.py) og
vedlikeholdsskriptene (oppdater_inkrementell.py, backfill_sesjon.py).

All dupliserende logikk (minister-koder, URL-mønstre, sentinel-datohåndtering,
avvisningsformler, sak-berikelse) skal ligge HER — ikke kopieres inn i det
enkelte skriptet på nytt. Se endringslogg for begrunnelse (2026-09-16).
"""
import json
import os
import time
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import date

NS = "{http://data.stortinget.no}"

SPORSMAL_ENDEPUNKTER = ['skriftligesporsmal', 'interpellasjoner', 'sporretimesporsmal']


# ---------------------------------------------------------------------------
# Generisk JSON-IO, katalog per datatype (delt mellom oppdater_inkrementell.py og backfill_sesjon.py)
# ---------------------------------------------------------------------------

def _sesjon_av(post):
    return post.get('sesjon') or post.get('sesjon_fremmet')


def last_json(sti):
    """Leser en datatype. `sti` er en katalog med én fil per sesjon (data/<datatype>/<sesjon>.json)."""
    if not os.path.isdir(sti):
        return []
    ut = []
    for navn in sorted(os.listdir(sti)):
        if navn.endswith('.json'):
            with open(os.path.join(sti, navn), encoding='utf-8') as f:
                ut.extend(json.load(f))
    return ut


def skriv_json(sti, data):
    """Skriver en datatype tilbake som én fil per sesjon. Filer som ikke er endret røres ikke,
    slik at en oppdatering bare gir diff i sesjonene som faktisk er endret. Atomisk skriving."""
    os.makedirs(sti, exist_ok=True)
    per_sesjon = {}
    for post in data:
        per_sesjon.setdefault(_sesjon_av(post), []).append(post)
    for sesjon, poster in per_sesjon.items():
        tekst = json.dumps(poster, ensure_ascii=False, separators=(',', ':'))
        fil = os.path.join(sti, f'{sesjon}.json')
        if os.path.exists(fil):
            with open(fil, encoding='utf-8') as f:
                if f.read() == tekst:
                    continue
        tmp = fil + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as f:
            f.write(tekst)
        os.replace(tmp, fil)

# ---------------------------------------------------------------------------
# Minister-koder og URL-mønstre for spørsmål
# ---------------------------------------------------------------------------

SPORSMAL_TYPE_NAVN = {'s': 'Skriftlig spørsmål', 'i': 'Interpellasjon', 'm': 'Spørretimespørsmål'}
SPORSMAL_URL_MONSTER = {
    's': 'https://www.stortinget.no/no/Saker-og-publikasjoner/Sporsmal/Skriftlige-sporsmal-og-svar/Skriftlig-sporsmal/?qnid={}',
    'i': 'https://www.stortinget.no/no/Saker-og-publikasjoner/Sporsmal/Interpellasjoner/Interpellasjon/?qnid={}',
    'm': 'https://www.stortinget.no/no/Saker-og-publikasjoner/Sporsmal/Sporretimesporsmal/et-sporretimesporsmal/?qnid={}',
}
# XML-ens type-felt ('skriftlig_sporsmal'/'interpellasjon'/'sporretime_sporsmal') -> kort kode
SPORSMAL_XML_TYPE_TIL_KORTKODE = {
    'skriftlig_sporsmal': 's', 'interpellasjon': 'i', 'sporretime_sporsmal': 'm',
}

# NB: denne tabellen er kjent ufullstendig for sjeldne/historiske koder — se
# kvartalsvis datakvalitetsaudit (steg 4) for løpende kontroll mot fersk data.
MINISTER_TITTEL = {
    "ABS": "arbeids- og sosialministeren", "ARI": "arbeids- og inkluderingsministeren",
    "ASD": "arbeids- og sosialministeren", "BABAD": "barne- og familieministeren",
    "BARNL": "barne- og likestillingsministeren", "BBD": "barne- og familieministeren",
    "BLDII": "barne- og likestillingsministeren", "BLID": "barne-, likestillings- og inkluderingsministeren",
    "DFD": "digitaliserings- og forvaltningsministeren", "DIGFOR": "digitaliserings- og forvaltningsministeren",
    "DIKOD": "distrikts- og digitaliseringsministeren", "DKD": "digitaliseringsministeren",
    "END": "energiministeren", "FD": "forsvarsministeren", "FIN": "finansministeren",
    "FISK": "fiskeriministeren", "FND": "fiskeri- og sjømatministeren",
    "HHD": "helse- og omsorgsministeren", "HOD": "helse- og omsorgsministeren",
    "HODE": "eldre- og folkehelseministeren", "HODH": "helseministeren",
    "JBD": "justis- og beredskapsministeren", "JBDI": "innvandrings- og integreringsministeren",
    "JBI": "justis-, beredskaps- og innvandringsministeren", "JJD": "justis- og innvandringsministeren",
    "JUJUD": "justis- og beredskapsministeren", "KD": "kulturministeren",
    "KKI": "kultur- og kirkeministeren", "KLD": "klima- og miljøministeren",
    "KMD": "kommunal- og moderniseringsministeren", "KMDI": "kommunal- og distriktsministeren",
    "KOMMOD": "kommunal- og moderniseringsministeren", "KRD": "kommunal- og regionalministeren",
    "KUKUD": "kultur- og likestillingsministeren", "KUND": "kunnskapsministeren",
    "KUNDI": "kunnskaps- og integreringsministeren", "KUNFORSK": "forsknings- og høyere utdanningsministeren",
    "KUNSD": "kunnskapsministeren", "LMD": "landbruks- og matministeren",
    "MDK": "klima- og miljøvernministeren", "NFD": "næringsministeren",
    "NFDFH": "fiskeri- og havministeren", "NFDFISK": "fiskeriministeren", "NH": "næringsministeren",
    "OED": "olje- og energiministeren", "SD": "samferdselsministeren",
    "SJD": "samfunnssikkerhetsministeren", "SMK": "statsministeren", "UD": "utenriksministeren",
    "UDEU": "ministeren ved Statsministerens kontor for samordning av EØS-saker og forholdet til EU",
    "UDUT": "utviklingsministeren", "UEU": "ministeren for samordning av EØS-saker og forholdet til EU",
}

AVVISNING_FORMLER = [
    'vedlegges protokollen', 'lagt ved møteboka', 'lagt ved protokollen',
    'å leggja ved', 'å legge ved', 'vedtas ikke', 'vedtas ikkje',
    'blir ikke vedtatt', 'bifalles ikke', 'bifalles ikkje',
]

STIKKORD_PÅLITELIG_GRENSE = 20

# ---------------------------------------------------------------------------
# Generelle XML-hjelpere
# ---------------------------------------------------------------------------

def t(el, tag):
    """Tekstinnhold av barne-element `tag` under `el`, eller None."""
    if el is None:
        return None
    c = el.find(f"{NS}{tag}")
    return c.text if c is not None else None


def sentinel_dato(*vals):
    """Første reelle (ikke-sentinel) dato blant `vals`. Stortinget bruker
    0001-01-01 som sentinel for 'ikke satt' — en slik streng er 'truthy' i
    Python, så hvert felt må sjekkes individuelt (ikke `a or b`)."""
    for v in vals:
        if v and not v.startswith('0001-01-01'):
            return v
    return None


def hent_sesjon_xml(endepunkt, sesjon):
    """Hent ett endepunkt for én sesjon med status=alle (obligatorisk for de
    tre sporsmal-endepunktene, se endringslogg 2026-09-16), og verifiser at
    sesjon_id i responsen faktisk matcher det som ble forespurt."""
    url = f"https://data.stortinget.no/eksport/{endepunkt}?sesjonid={sesjon}&status=alle"
    root = hent_xml(url)
    faktisk_sesjon = t(root, 'sesjon_id')
    if faktisk_sesjon and faktisk_sesjon != sesjon:
        raise RuntimeError(f"{endepunkt}: forespurt sesjon {sesjon}, fikk {faktisk_sesjon} tilbake")
    return root


def upsert_sporsmal_for_sesjon(sesjon, data_sti, dry_run=False):
    """Hent fersk sporsmal-XML (alle tre typer) for ÉN sesjon og upsert mot
    lokal data_sti. Brukes både av oppdater_inkrementell.py (inneværende
    sesjon, hver kjøring) og backfill_sesjon.py (historiske sesjoner,
    engangsjobb). Returnerer {'nye': n, 'oppdatert': n, 'total': n}."""
    eksisterende = last_json(data_sti)
    per_id = {x['id']: x for x in eksisterende}

    nye = 0
    oppdatert = 0
    for endepunkt in SPORSMAL_ENDEPUNKTER:
        root = hent_sesjon_xml(endepunkt, sesjon)
        for kortkode, sp in parse_sporsmal_liste(root):
            rec = parse_sporsmal_record(sp, kortkode, sesjon)
            idv = rec['id']
            if idv not in per_id:
                per_id[idv] = rec
                nye += 1
            elif per_id[idv] != rec:
                per_id[idv] = rec
                oppdatert += 1

    if not dry_run and (nye or oppdatert):
        skriv_json(data_sti, list(per_id.values()))
    return {'nye': nye, 'oppdatert': oppdatert, 'total': len(per_id)}


def hent_xml(url, forsok=3, ventetid=1.5):
    """Hent URL med retry, returner parset XML-rot. Kaster ved varig feil."""
    sisste_feil = None
    for i in range(forsok):
        try:
            with urllib.request.urlopen(url, timeout=30) as resp:
                data = resp.read()
            return ET.fromstring(data)
        except (urllib.error.URLError, ET.ParseError) as e:
            sisste_feil = e
            time.sleep(ventetid)
    raise RuntimeError(f"Klarte ikke hente {url} etter {forsok} forsøk: {sisste_feil}")


def sesjon_for_dato(d):
    startaar = d.year if d.month >= 10 else d.year - 1
    return f"{startaar}-{startaar + 1}"


def resolve_sesjon(verdi, idag=None):
    if verdi is None:
        return None
    if idag is None:
        idag = date.today()
    n = verdi.strip().lower()
    if n in ('inneværende', 'inneverende', 'nåværende', 'current', 'nå'):
        return sesjon_for_dato(idag)
    if n in ('forrige', 'forrige sesjon', 'previous', 'siste avsluttede'):
        cur = sesjon_for_dato(idag)
        y = int(cur.split('-')[0])
        return f"{y - 1}-{y}"
    return verdi


# ---------------------------------------------------------------------------
# Sak-berikelse (per-sak-oppslag mot /eksport/sak?sakid=X)
# ---------------------------------------------------------------------------

def hent_sak_detaljer(sak_id, cache=None, forsok=3):
    """Berik et sak_id med komite/emne/stikkord/henvisning/dokumentgruppe/
    sak_type/forslagstillere fra detaljert sak-endepunkt. `cache` er en dict
    som gjenbrukes på tvers av kall for å unngå duplikate oppslag."""
    if cache is not None and sak_id in cache:
        return cache[sak_id]
    tomt = {'komite': None, 'emne': [], 'stikkord': [], 'henvisning': None,
            'dokumentgruppe': None, 'sak_type': None, 'forslagstillere': []}
    try:
        root = hent_xml(f"https://data.stortinget.no/eksport/sak?sakid={sak_id}", forsok=forsok)
    except RuntimeError:
        if cache is not None:
            cache[sak_id] = tomt
        return tomt

    komite_el = root.find(f"{NS}komite")
    komite = t(komite_el, 'navn') if komite_el is not None else None

    emner = []
    emne_liste_el = root.find(f"{NS}emne_liste")
    if emne_liste_el is not None:
        for e in emne_liste_el:
            nv = t(e, 'navn')
            if nv:
                emner.append(nv)

    stikkord = []
    stikkord_liste_el = root.find(f"{NS}stikkord_liste")
    if stikkord_liste_el is not None:
        for s in stikkord_liste_el:
            if s.text:
                stikkord.append(s.text)

    forslagstillere = []
    sak_opphav = root.find(f"{NS}sak_opphav")
    if sak_opphav is not None:
        fl = sak_opphav.find(f"{NS}forslagstiller_liste")
        if fl is not None:
            for rep in fl:
                fornavn = t(rep, 'fornavn') or ''
                etternavn = t(rep, 'etternavn') or ''
                navn = (fornavn + ' ' + etternavn).strip()
                parti_el = rep.find(f"{NS}parti")
                parti = t(parti_el, 'id') if parti_el is not None else None
                if navn:
                    forslagstillere.append({'navn': navn, 'parti': parti})

    resultat = {
        'komite': komite, 'emne': emner, 'stikkord': stikkord,
        'henvisning': t(root, 'henvisning'), 'dokumentgruppe': t(root, 'dokumentgruppe'),
        'sak_type': t(root, 'type'), 'forslagstillere': forslagstillere,
    }
    if cache is not None:
        cache[sak_id] = resultat
    return resultat


# ---------------------------------------------------------------------------
# Parsing: spørsmål/interpellasjon/spørretime
# ---------------------------------------------------------------------------

def parse_sporsmal_liste(root):
    """Returner (kortkode, xml_element)-par for hver post i en sporsmal_liste."""
    liste = root.find(f"{NS}sporsmal_liste")
    if liste is None:
        return []
    ut = []
    for sp in liste:
        xml_type = t(sp, 'type')
        kortkode = SPORSMAL_XML_TYPE_TIL_KORTKODE.get(xml_type)
        if kortkode:
            ut.append((kortkode, sp))
    return ut


def parse_sporsmal_record(sp, kortkode, sesjon):
    """Bygg en sporsmal.json-post fra ett <sporsmal>-element."""
    idv = t(sp, 'id')
    legacy_id = t(sp, 'legacy_id')
    sporsmal_nummer = t(sp, 'sporsmal_nummer')
    status = t(sp, 'status') or 'besvart'
    dato = sentinel_dato(t(sp, 'besvart_dato'), t(sp, 'sendt_dato'), t(sp, 'datert_dato'))

    fra = sp.find(f"{NS}sporsmal_fra")
    fra_navn = None
    fra_parti = None
    if fra is not None:
        fornavn = t(fra, 'fornavn') or ''
        etternavn = t(fra, 'etternavn') or ''
        fra_navn = (fornavn + ' ' + etternavn).strip() or None
        parti_el = fra.find(f"{NS}parti")
        if parti_el is not None:
            fra_parti = t(parti_el, 'id')

    til_minister_id = t(sp, 'sporsmal_til_minister_id') or t(sp, 'rette_vedkommende_minister_id')

    besvart_av = sp.find(f"{NS}besvart_av")
    besvart_av_navn = None
    if besvart_av is not None:
        fn = t(besvart_av, 'fornavn') or ''
        en = t(besvart_av, 'etternavn') or ''
        besvart_av_navn = (fn + ' ' + en).strip() or None

    tittel = t(sp, 'tittel')
    tittel_midlertidig = False
    if not tittel and kortkode == 'i':
        til_tittel = t(sp, 'sporsmal_til_minister_tittel') or MINISTER_TITTEL.get(til_minister_id, 'statsråden')
        tittel = f"Interpellasjon fra {fra_navn} ({fra_parti}) til {til_tittel}"
        tittel_midlertidig = True

    emner = []
    emne_liste_el = sp.find(f"{NS}emne_liste")
    if emne_liste_el is not None:
        for e in emne_liste_el:
            nv = t(e, 'navn')
            if nv:
                emner.append(nv)

    rec = {
        'id': idv, 'legacy_id': legacy_id, 'type': kortkode, 'sesjon': sesjon,
        'sporsmal_nummer': sporsmal_nummer, 'tittel': tittel, 'fra_navn': fra_navn,
        'fra_parti': fra_parti, 'til_minister_id': til_minister_id,
        'besvart_av_navn': besvart_av_navn, 'status': status, 'emne': emner, 'dato': dato,
    }
    if tittel_midlertidig:
        rec['tittel_midlertidig'] = True
    return rec


# ---------------------------------------------------------------------------
# Parsing: stortingsvedtak (anmodningsvedtak = type ANMOD) og vedtak-oppslag
# ---------------------------------------------------------------------------

def parse_stortingsvedtak_liste(root):
    liste = root.find(f"{NS}stortingsvedtak_liste")
    return list(liste) if liste is not None else []


def bygg_vedtak_oppslag(root_liste_elementer):
    """sak_id -> [(vedtakstype_id, tekst), ...] fra en eller flere
    stortingsvedtak_liste-XML-røtter (kan kombineres på tvers av sesjoner)."""
    oppslag = {}
    for root in root_liste_elementer:
        for v in parse_stortingsvedtak_liste(root):
            sak_id = t(v, 'sak_id')
            if not sak_id:
                continue
            type_el = v.find(f"{NS}stortingsvedtak_type")
            type_id = t(type_el, 'id') if type_el is not None else None
            tekst = t(v, 'tekst') or ''
            oppslag.setdefault(sak_id, []).append((type_id, tekst))
    return oppslag


def klassifiser_utfall(sak_id, vedtak_oppslag):
    vedtak_list = vedtak_oppslag.get(sak_id, [])
    if not vedtak_list:
        return 'ukjent', None
    for type_id, tekst in vedtak_list:
        if type_id == 'ANMOD':
            return 'vedtatt (anmodning)', None
    for type_id, tekst in vedtak_list:
        low = tekst.lower()
        if any(formel in low for formel in AVVISNING_FORMLER):
            return 'avvist', None
    _, tekst = vedtak_list[0]
    return 'annet', tekst


def parse_anmodningsvedtak_record(v, sesjon, sak_cache=None):
    """Bygg en anmodningsvedtak.json-post fra ett <stortingsvedtak>-element
    (kaller den beriker med sak-oppslag)."""
    idv = t(v, 'id')
    sak_id = t(v, 'sak_id')
    vedtak_nummer = t(v, 'vedtak_nummer')
    sak_info = hent_sak_detaljer(sak_id, sak_cache) if sak_id else {
        'komite': None, 'emne': [], 'stikkord': [], 'henvisning': None,
        'dokumentgruppe': None, 'sak_type': None}
    return {
        'id': idv, 'sesjon': sesjon, 'dato': t(v, 'dato'), 'sak_id': sak_id,
        'vedtak_nummer': int(vedtak_nummer) if vedtak_nummer else None,
        'tittel': t(v, 'tittel'), 'tekst': t(v, 'tekst'),
        'sak_url': f"https://www.stortinget.no/no/Saker-og-publikasjoner/Saker/Sak/?p={sak_id}" if sak_id else None,
        'vedtak_url': f"https://www.stortinget.no/no/Saker-og-publikasjoner/Vedtak/Vedtak/Sak/?did={idv}&p={sak_id}" if sak_id else None,
        'komite': sak_info['komite'], 'emne': sak_info['emne'], 'stikkord': sak_info['stikkord'],
        'henvisning': sak_info['henvisning'], 'dokumentgruppe': sak_info['dokumentgruppe'],
        'sak_type': sak_info['sak_type'],
    }


# ---------------------------------------------------------------------------
# Parsing: representantforslag (fra saker-endepunktet)
# ---------------------------------------------------------------------------

def parse_saker_liste(root):
    liste = root.find(f"{NS}saker_liste")
    return list(liste) if liste is not None else []


def parse_representantforslag_grunnrecord(sak, sesjon_fremmet, vedtak_oppslag):
    """Bygg en representantforslag.json-post fra ett <sak>-element i
    saker_liste UTEN per-sak-nettverkskall (kun kalt når dokumentgruppe ==
    'representantforslag'). komite/emne/forslagstillere er ofte tomme i
    bulk-lista — bruk `hent_sak_detaljer()` + `beriket_representantforslag()`
    for å fylle dem inn, men KUN for nye poster (335+ per-sak-kall for hver
    kjøring er for dyrt — se ytelsesfunn 2026-09-16)."""
    idv = t(sak, 'id')
    komite_el = sak.find(f"{NS}komite")
    komite = t(komite_el, 'navn') if komite_el is not None else None
    emner = []
    emne_liste_el = sak.find(f"{NS}emne_liste")
    if emne_liste_el is not None:
        for e in emne_liste_el:
            nv = t(e, 'navn')
            if nv:
                emner.append(nv)
    utfall, utfall_tekst = klassifiser_utfall(idv, vedtak_oppslag)
    return {
        'id': idv, 'sesjon_fremmet': sesjon_fremmet, 'behandlet_sesjon': t(sak, 'behandlet_sesjon_id'),
        'tittel': t(sak, 'tittel'), 'komite': komite, 'emne': emner, 'forslagstillere': [],
        'henvisning': t(sak, 'henvisning'), 'status': t(sak, 'status'),
        'utfall': utfall, 'utfall_tekst': utfall_tekst,
        'sak_url': f"https://www.stortinget.no/no/Saker-og-publikasjoner/Saker/Sak/?p={idv}",
    }


def beriket_representantforslag(rec, sak_cache=None):
    """Fyll inn forslagstillere/komite/emne via per-sak-oppslag (nettverkskall)
    — kall KUN for poster som faktisk trenger det (typisk nye poster)."""
    sak_info = hent_sak_detaljer(rec['id'], sak_cache)
    if sak_info.get('forslagstillere'):
        rec['forslagstillere'] = sak_info['forslagstillere']
    if sak_info.get('komite') and not rec.get('komite'):
        rec['komite'] = sak_info['komite']
    if sak_info.get('emne') and not rec.get('emne'):
        rec['emne'] = sak_info['emne']
    return rec
