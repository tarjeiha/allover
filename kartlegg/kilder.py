"""Midlertidig kartlegging, runde 2. Samme åpne User-Agent som før; sider som avviser oss, hoppes over."""
import re, urllib.request, gzip, collections

UA = {"User-Agent": "regelverksbase-kartlegging/1.0"}
def hent(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
            data = r.read()
            if data[:2] == b"\x1f\x8b": data = gzip.decompress(data)
            return r.status, data.decode("utf-8", "replace")
    except Exception as e:
        return str(e)[:120], ""

def urler(sm, maks=40):
    ut, kø, sett = [], [sm], set()
    while kø and len(sett) < maks:
        s = kø.pop(0)
        if s in sett: continue
        sett.add(s); st, t = hent(s)
        if "<sitemapindex" in t: kø += re.findall(r"<loc>\s*(.*?)\s*</loc>", t)
        for b in re.findall(r"<url>(.*?)</url>", t, re.S):
            l = re.search(r"<loc>\s*(.*?)\s*</loc>", b); m = re.search(r"<lastmod>\s*(.*?)\s*</lastmod>", b)
            if l: ut.append((l.group(1), m.group(1)[:10] if m else ""))
    return ut

print("\n#### Udir")
u = urler("https://www.udir.no/sitemap.xml")
c = collections.Counter("/".join(x.split("/")[3:6]) for x, _ in u if "/regelverk-og-tilsyn/" in x)
for k, v in c.most_common(40): print(f"{v:5} {k}")
for x, m in u:
    if re.search(r"(?i)udir-\d|rundskriv|regelverkstolk|tolkning", x) and "Tidligere-rundskriv/Udir-1-2015" not in x: print("  ", m, x)

print("\n#### Sivilombudet")
u = urler("https://www.sivilombudet.no/uttalelser-sitemap.xml") + urler("https://www.sivilombudet.no/uttalelser-sitemap2.xml")
print("uttalelser:", len(u), "eldste", min(m for _, m in u if m), "nyeste", max(m for _, m in u if m))
for x, m in u[:5] + u[-5:]: print("  ", m, x)
for x, m in urler("https://www.sivilombudet.no/post_tag-sitemap.xml"):
    if re.search(r"offentlig|forvaltningslov|innsyn|taushet|habil|klage", x): print("  TAG", m, x)
st, side = hent(u[-1][0]); print("side", st, len(side))
print(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", side))[:1500])

print("\n#### IMDi")
for x, m in urler("https://imdi.no/sitemap.xml"):
    if "/regelverk/" in x: print("  ", m, x)

for navn, base in [("DFØ", "https://www.dfo.no"), ("HK-dir", "https://www.hkdir.no"), ("SPK", "https://www.spk.no")]:
    print(f"\n#### {navn}")
    st, r = hent(base + "/robots.txt"); print("robots", st)
    print("\n".join(l for l in r.splitlines() if l.strip())[:800])
    sm = re.findall(r"(?im)^sitemap:\s*(\S+)", r) or [base + "/sitemap.xml"]
    sm = [s if s.startswith("http") else base + s for s in sm]
    u = urler(sm[0])
    print("URL-er", len(u), "lastmod", sum(1 for _, m in u if m))
    for k, v in collections.Counter("/".join(x.split("/")[3:5]) for x, _ in u).most_common(25): print(f"{v:6} {k}")
    for x, m in u:
        if re.search(r"(?i)rundskriv|personalh|regelverk/|samordning|veiledning", x): print("  ", m, x)

print("\n#### Statens personalhåndbok på Lovdata")
for url in ["https://lovdata.no/dokument/SPH/sph-2026", "https://lovdata.no/sph", "https://lovdata.no/dokument/SPH"]:
    st, t = hent(url); print(url, st, len(t))
    for l in sorted(set(re.findall(r'href="(/[^"]*(?:SPH|sph)[^"]*)"', t)))[:30]: print("   ", l)
