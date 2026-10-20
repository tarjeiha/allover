import urllib.request, xml.etree.ElementTree as ET, collections, re
NS = "{http://data.stortinget.no}"
def get(u):
    return ET.fromstring(urllib.request.urlopen(u, timeout=60).read())
def vis(el, n=2500):
    s = ET.tostring(el, encoding='unicode'); s = re.sub(r'\s*<ns0:respons_dato_tid>[^<]*</ns0:respons_dato_tid>', '', s); s = re.sub(r'\s*<ns0:versjon>[^<]*</ns0:versjon>', '', s)
    print(s[:n]); print()
r = get("https://data.stortinget.no/eksport/sesjoner")
ids = [x.findtext(NS+'id') for x in r.find(NS+'sesjoner_liste')]
print('sesjoner', ids[-3:], '...', ids[:3], len(ids))
print('eldste sesjon-id-er', ids[-6:])
for s in ['2013-2014', '2018-2019', '2025-2026']:
    b = get(f"https://data.stortinget.no/eksport/saker?sesjonid={s}").find(NS+'saker_liste')
    c = collections.Counter()
    for sak in b:
        k = sak.find(NS+'komite'); kn = k.findtext(NS+'id') if k is not None else None
        c[kn] += 1
    print(s, 'komiteer', c.most_common(15))
    if s == '2013-2014': vis(list(b)[0], 3000)
b = get("https://data.stortinget.no/eksport/saker?sesjonid=2025-2026").find(NS+'saker_liste')
KOM = collections.Counter(s.find(NS+'komite').findtext(NS+'id') for s in b if s.find(NS+'komite') is not None and 'arbeid' in (s.find(NS+'komite').findtext(NS+'navn') or '').lower()).most_common(1)[0][0]; print('KOM', KOM)
asos = [s for s in b if (s.find(NS+'komite') is not None and s.find(NS+'komite').findtext(NS+'id') == KOM and s.findtext(NS+'dokumentgruppe') == 'proposisjon' and s.findtext(NS+'status') == 'behandlet')]
sak = asos[0]; print('=== SAK'); vis(sak, 3000)
sid = sak.findtext(NS+'id')
v = get(f"https://data.stortinget.no/eksport/voteringer?sakid={sid}")
print('=== VOTERINGER'); vis(v, 4000)
vl = v.find(NS+'sak_votering_liste')
for vo in list(vl)[:2]:
    vid = vo.findtext(NS+'votering_id')
    print('=== FORSLAG', vid); vis(get(f"https://data.stortinget.no/eksport/voteringsforslag?voteringid={vid}"), 4000)
    print('=== VEDTAK', vid); vis(get(f"https://data.stortinget.no/eksport/voteringsvedtak?voteringid={vid}"), 1500)
# en sak med mindretallsforslag: representantforslag avvist
rep = [s for s in b if s.findtext(NS+'dokumentgruppe') == 'representantforslag' and s.findtext(NS+'status') == 'behandlet' and s.find(NS+'komite') is not None and s.find(NS+'komite').findtext(NS+'id') == KOM][:1]
for s in rep:
    v = get(f"https://data.stortinget.no/eksport/voteringer?sakid={s.findtext(NS+'id')}")
    for vo in list(v.find(NS+'sak_votering_liste'))[:3]:
        vid = vo.findtext(NS+'votering_id'); print('=== REP-FORSLAG', vid); vis(get(f"https://data.stortinget.no/eksport/voteringsforslag?voteringid={vid}"), 3000)
