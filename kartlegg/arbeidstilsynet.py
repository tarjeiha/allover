"""Midlertidig kartlegging av arbeidstilsynet.no: sitemap, robots, feeds og datoer."""
import re, urllib.request, collections
from bs4 import BeautifulSoup

UA = {"User-Agent": "regelverksbase-kartlegging/1.0"}
def hent(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except Exception as e:
        return str(e), ""

B = "https://www.arbeidstilsynet.no"
s, t = hent(B + "/robots.txt"); print("=== robots", s); print(t[:1500])

s, t = hent(B + "/sitemap.xml"); print("=== sitemap", s, len(t)); print(t[:800])
locs = re.findall(r"<loc>(.*?)</loc>", t)
subs = [l for l in locs if l.endswith(".xml")]
alle = []
for sm in subs[:20]:
    s2, t2 = hent(sm); print("sub", sm, s2, len(t2))
    alle += re.findall(r"<url>\s*<loc>(.*?)</loc>(?:\s*<lastmod>(.*?)</lastmod>)?", t2)
if not subs:
    alle = re.findall(r"<url>\s*<loc>(.*?)</loc>(?:\s*<lastmod>(.*?)</lastmod>)?", t)
print("URL-er:", len(alle), "med lastmod:", sum(1 for _, m in alle if m))
tell = collections.Counter("/".join(u.split("/")[3:5]) for u, _ in alle)
for k, v in tell.most_common(60): print(f"{v:6}  {k}")
for u, m in alle:
    if re.search(r"regelverk|rundskriv|tolk|veiled|forskrift", u): print("R", m, u)

for sti in ["/regelverk/", "/", "/nyheter/"]:
    s, t = hent(B + sti); print("=== ", sti, s, len(t))
    if not t: continue
    soup = BeautifulSoup(t, "lxml")
    for l in soup.find_all("link", type=re.compile("rss|atom")): print("FEED", l.get("href"))
    for m in soup.find_all("meta"):
        if any(k in str(m.attrs).lower() for k in ("date", "modified", "published", "updated")): print("META", m.attrs)
    if sti == "/regelverk/":
        for a in soup.find_all("a", href=True):
            if a["href"].startswith("/regelverk") or "arbeidstilsynet.no/regelverk" in a["href"]:
                print("A", a["href"], a.get_text(" ", strip=True)[:80])

for u, m in [x for x in alle if "/regelverk/" in x[0]][:4]:
    s, t = hent(u); print("=== side", u, s)
    for d in re.findall(r"(?i)(sist (?:endret|oppdatert|revidert)[^<]{0,60}|publisert[^<]{0,60}|dateModified[^,]{0,60})", t)[:5]: print("  DATO", d)
