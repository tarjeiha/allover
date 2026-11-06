"""Midlertidig kartlegging av NVA (nva.sikt.no). Skriver til loggen, lagrer ingenting."""
import json, re, sys, urllib.request, urllib.parse, urllib.error
UA = "Mozilla/5.0 (regelverksbasen; tarjeiha/allover; kartlegging)"
API = "https://api.nva.unit.no"

def get(url, maks=None, accept="application/json", metode="GET"):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept}, method=metode)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            b = r.read() if metode == "GET" else b""
            return r.status, dict(r.headers), b
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()[:2000]
    except Exception as e:
        return 0, {}, str(e).encode()

def vis(tittel, url, maks=3000, **kw):
    s, h, b = get(url, **kw)
    print(f"\n##### {tittel}\n# {url}\n# status {s} {h.get('Content-Type','')} {len(b)} byte")
    print(b[:maks].decode("utf-8", "replace"))
    return s, h, b

def js(url):
    s, h, b = get(url)
    try:
        return s, json.loads(b)
    except Exception:
        return s, None

# 1 robots og nettsted
for u in ["https://nva.sikt.no/robots.txt", f"{API}/robots.txt", "https://nva.sikt.no/sitemap.xml"]:
    vis("robots/sitemap", u, 2500, accept="*/*")
s,h,b = get("https://nva.sikt.no/", accept="text/html")
print("\n##### forside", s, len(b)); print(re.sub(r"\s+"," ",b.decode('utf-8','replace'))[:1500])

# 2 API-dokumentasjon
for u in [f"{API}/search/", f"{API}/search/openapi.json", f"{API}/search/resources/openapi", "https://swagger-ui.nva.unit.no/"]:
    vis("doc", u, 1500, accept="*/*")

# 3 ett søk med full post
s, d = js(f"{API}/search/resources?query=sykefrav%C3%A6r&results=2&aggregation=all")
print("\n##### søk sykefravær status", s)
if d:
    print("nøkler:", list(d.keys()))
    print("totalHits:", d.get("totalHits"))
    print("aggregations:", json.dumps(d.get("aggregations"), ensure_ascii=False)[:6000])
    for hit in d.get("hits", [])[:2]:
        print("--- HIT", json.dumps(hit, ensure_ascii=False)[:5000])

# 4 omfang per tema
TEMA = ["sykefravær","uføretrygd","arbeidsavklaringspenger","dagpenger","arbeidsledighet","arbeidsmarkedstiltak",
        "arbeidsmiljø","arbeidsliv","inkludering","integrering","introduksjonsprogram","innvandrere arbeid",
        "flyktninger","pensjon","tariff","lønnsdannelse","sosialhjelp","velferdsstat","diskriminering arbeidsliv",
        "NAV","folketrygd","sick leave","disability benefit","labour market","immigrant integration","occupational health"]
print("\n##### OMFANG")
for t in TEMA:
    q = urllib.parse.quote(t)
    s, d = js(f"{API}/search/resources?query={q}&results=0&aggregation=all")
    if not d: print(t, "status", s); continue
    ag = d.get("aggregations") or {}
    def kort(n):
        v = ag.get(n)
        if isinstance(v, list): return [(x.get("key"), x.get("count")) for x in v[:8]]
        return v
    print(f"{t}\t{d.get('totalHits')}\tfiler={kort('files')}\tlisens={kort('license')}\ttype={kort('type')}")

# 5 prosjekter
for u in [f"{API}/cristin/project?query=sykefrav%C3%A6r&results=2", f"{API}/search/projects?query=sykefrav%C3%A6r&results=2"]:
    vis("prosjekt", u, 4000)

# 6 organisasjoner (forskningsmiljøer på feltet)
for o in ["Fafo","Frischsenteret","Statens arbeidsmiljøinstitutt","NOVA","Institutt for samfunnsforskning","Arbeidsforskningsinstituttet","Nav"]:
    s, d = js(f"{API}/cristin/organization?query={urllib.parse.quote(o)}&results=3")
    if d:
        hits = d.get("hits", [])
        print("ORG", o, d.get("size"), [(x.get("id"), (x.get("labels") or {}).get("nb")) for x in hits[:3]])
    else:
        print("ORG", o, "status", s)

# 7 fulltekst: finn en post med åpen fil og prøv nedlasting
s, d = js(f"{API}/search/resources?query=sykefrav%C3%A6r&results=20&files=hasPublicFiles")
print("\n##### FILER status", s, d and d.get("totalHits"))
if d:
    for hit in d.get("hits", [])[:20]:
        arts = hit.get("associatedArtifacts") or []
        filer = [a for a in arts if a.get("type") in ("OpenFile","PublishedFile","InternalFile","PendingOpenFile")]
        if not filer: continue
        print("POST", hit.get("id"), json.dumps(filer, ensure_ascii=False)[:1500])
        pid = hit.get("identifier") or hit.get("id","").rsplit("/",1)[-1]
        f = filer[0]; fid = f.get("identifier")
        for u in [f"{API}/download/public/{pid}/files/{fid}", f"{API}/publication/{pid}/filelink/{fid}",
                  f"{API}/download/public/{fid}"]:
            st, hh, bb = get(u, accept="*/*")
            print("  ", st, hh.get("Content-Type"), len(bb), u, bb[:300])
        st, pub = js(f"{API}/publication/{pid}")
        print("  publication", st, json.dumps(pub, ensure_ascii=False)[:2500] if pub else "")
        break

# 8 OAI-PMH og vilkår
for u in [f"{API}/oai-pmh?verb=Identify", f"{API}/oai-pmh/?verb=Identify"]:
    vis("oai", u, 1500, accept="*/*")
for u in ["https://sikt.no/tjenester/nasjonalt-vitenarkiv-nva", "https://sikt.no/nva", "https://nva.sikt.no/about", "https://sikt.no/personvern-nasjonalt-vitenarkiv-nva"]:
    s,h,b = get(u, accept="text/html")
    t = re.sub(r"<[^>]+>"," ",b.decode("utf-8","replace")); t = re.sub(r"\s+"," ",t)
    print(f"\n##### side {u} {s} {len(b)}")
    for m in re.finditer(r"[^.]{0,250}(lisens|vilkår|CC0|CC BY|API|gjenbruk|åpne data|licen)[^.]{0,250}", t, re.I):
        print("  >", m.group(0)[:500])
