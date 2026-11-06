"""Midlertidig kartlegging av NVA, runde 2. Skriver til loggen, lagrer ingenting."""
import json, re, urllib.request, urllib.parse, urllib.error, subprocess, os
UA = "Mozilla/5.0 (regelverksbasen; tarjeiha/allover; kartlegging)"
API = "https://api.nva.unit.no"
def get(url, accept="application/json"):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()[:2000]
    except Exception as e:
        return 0, {}, str(e).encode()
def js(url):
    s, h, b = get(url)
    try: return s, h, json.loads(b)
    except Exception: return s, h, None

# 1 aggregeringer: navn og topp-verdier
s, h, d = js(f"{API}/search/resources?query=sykefrav%C3%A6r&results=0&aggregation=all")
print("HODER", {k: v for k, v in h.items() if re.search("rate|limit|retry|cache", k, re.I)})
for navn, v in (d.get("aggregations") or {}).items():
    if isinstance(v, list):
        eks = v[0]["id"].split("&")[-1] if v and v[0].get("id") else ""
        print("AGG", navn, "param:", eks.split("=")[0], [(x.get("key"), (x.get("labels") or {}).get("nb"), x.get("count")) for x in v[:12]])
    else:
        print("AGG", navn, json.dumps(v, ensure_ascii=False)[:600])

# 2 hele basen
for q in ["", "query=*"]:
    s, h, d = js(f"{API}/search/resources?{q}&results=0&aggregation=all")
    if d:
        ag = d.get("aggregations") or {}
        print("TOTAL", q, d.get("totalHits"), "filer", [(x["key"], x["count"]) for x in ag.get("files", [])])

# 3 forskningsmiljøer
ORG = {"Fafo": "7425.0.0.0", "Frischsenteret": "7495.0.0.0", "STAMI": "7476.0.0.0", "ISF": "7437.0.0.0"}
for sok in ["Velferdsforskningsinstituttet", "Arbeidsforskningsinstituttet", "Arbeids- og velferdsdirektoratet", "Arbeids- og velferdsetaten", "Senter for seniorpolitikk", "Statistisk sentralbyrå", "Integrerings- og mangfoldsdirektoratet", "Rehabiliteringssenteret AiR", "SINTEF", "NORCE"]:
    s, h, d = js(f"{API}/cristin/organization?query={urllib.parse.quote(sok)}&results=5")
    hits = (d or {}).get("hits", [])
    print("ORGSØK", sok, [(x.get("id","").rsplit("/",1)[-1], (x.get("labels") or {}).get("nb")) for x in hits[:5]])
    if hits: ORG[sok] = hits[0]["id"].rsplit("/",1)[-1]
for navn, oid in ORG.items():
    uri = urllib.parse.quote(f"{API}/cristin/organization/{oid}", safe="")
    for p in ["topLevelOrganization", "unit", "organization"]:
        s, h, d = js(f"{API}/search/resources?{p}={uri}&results=0&aggregation=all")
        if d and d.get("totalHits") is not None:
            ag = d.get("aggregations") or {}
            print(f"ORG {navn} {oid} via {p}: {d.get('totalHits')} filer={[(x['key'],x['count']) for x in ag.get('files',[])]} type={[(x['key'],x['count']) for x in ag.get('type',[])[:8]]}")
            break
        else:
            print(f"ORG {navn} {p} status {s}")

# 4 uten studentoppgaver: rapporter og artikler per tema
TYPER = "ReportResearch,ReportBasic,ReportWorkingPaper,ReportPolicy,AcademicArticle,AcademicChapter,AcademicMonograph,AcademicLiteratureReview,DegreePhd"
for t in ["sykefravær","uføretrygd","arbeidsavklaringspenger","arbeidsmarkedstiltak","arbeidsmiljø","integrering","introduksjonsprogram","pensjon","sosialhjelp","tariff"]:
    for p in ["instanceType", "type"]:
        s, h, d = js(f"{API}/search/resources?query={urllib.parse.quote(t)}&{p}={TYPER}&results=0&aggregation=all")
        if d and d.get("totalHits") is not None:
            ag = d.get("aggregations") or {}
            print(f"FORSK {t} via {p}: {d.get('totalHits')} filer={[(x['key'],x['count']) for x in ag.get('files',[])]}")
            break

# 5 sammendrag og emneord i en rapport
s, h, d = js(f"{API}/search/resources?query=arbeidsavklaringspenger&instanceType=ReportResearch&results=3")
for hit in (d or {}).get("hits", [])[:3]:
    ed = hit.get("entityDescription", {})
    print("RAPPORT", ed.get("mainTitle"), "|", (ed.get("publicationDate") or {}).get("year"), "| abstract:", (ed.get("abstract") or "")[:300].replace("\n"," "), "| tags:", ed.get("tags"), "| fundings:", json.dumps(hit.get("fundings"), ensure_ascii=False)[:400], "| projects:", json.dumps(hit.get("projects"), ensure_ascii=False)[:300])

# 6 nedlasting av én åpen fil via presignert lenke
s, h, d = js(f"{API}/search/resources?query=arbeidsavklaringspenger&instanceType=ReportResearch&files=hasPublicFiles&results=5")
for hit in (d or {}).get("hits", []):
    filer = [a for a in hit.get("associatedArtifacts", []) if a.get("type") == "OpenFile" and a.get("mimeType") == "application/pdf"]
    if not filer: continue
    f = filer[0]; pid = hit["identifier"]
    print("FIL", hit["entityDescription"].get("mainTitle"), f.get("license"), f.get("size"))
    s, h, link = js(f"{API}/publication/{pid}/filelink/{f['identifier']}")
    url = (link or {}).get("id")
    s2, h2, pdf = get(url, accept="*/*") if url else (0, {}, b"")
    print("  PDF", s2, h2.get("Content-Type"), len(pdf))
    if pdf[:4] == b"%PDF":
        open("/tmp/f.pdf","wb").write(pdf)
        r = subprocess.run(["pdftotext","-layout","/tmp/f.pdf","-"], capture_output=True, text=True)
        print("  TEKST", len(r.stdout), "tegn:", re.sub(r"\s+"," ", r.stdout)[:500])
    break

# 7 lisenssider og vilkår
for u in ["https://nva.sikt.no/license/copyright-act/1.0", f"{API}/license/copyright-act/1.0", "https://sikt.no/", "https://nva.sikt.no/manifest.json"]:
    s, h, b = get(u, accept="text/html,*/*")
    t = re.sub(r"\s+"," ", re.sub(r"<[^>]+>"," ", b.decode("utf-8","replace")))
    print("SIDE", u, s, h.get("Server"), h.get("Content-Type"), len(b), t[:400])
# lisenstekst kan ligge i oversettelsesfilene til nettsiden
s, h, b = get("https://nva.sikt.no/", accept="text/html")
js_filer = re.findall(r'(/assets/[^"]+\.js)', b.decode("utf-8","replace"))
funn = 0
for jf in js_filer:
    s, h, bb = get("https://nva.sikt.no" + jf, accept="*/*")
    t = bb.decode("utf-8", "replace")
    for m in re.finditer(r".{0,300}(Generelle bruksvilkår|General Terms of Use|copyright-act|vilkår for bruk|terms of use).{0,600}", t):
        print("JS", jf, m.group(0)[:900]); funn += 1
        if funn > 12: break
    if funn > 12: break
print("JS-filer", len(js_filer))
