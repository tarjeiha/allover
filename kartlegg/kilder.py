"""Midlertidig kartlegging, runde 4: sidestruktur hos SPK, IMDi og Sivilombudet."""
import re, time, urllib.request
from collections import Counter
from bs4 import BeautifulSoup
UA = {"User-Agent": "regelverksbase/1.0 (+https://github.com/tarjeiha/allover)"}
def hent(url):
    time.sleep(1)
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read().decode("utf-8", "replace")
def locs(url):
    t = hent(url)
    if "<sitemapindex" in t:
        ut = []
        for u in re.findall(r"<loc>\s*(.*?)\s*</loc>", t): ut += locs(u)
        return ut
    return re.findall(r"<loc>\s*(.*?)\s*</loc>", t)
def struktur(url):
    s = BeautifulSoup(hent(url), "lxml")
    print("\n=== SIDE", url, "| title:", s.title.get_text(strip=True) if s.title else "")
    for sel in ["main article", "article", "main", "[role=main]", "#main-content", ".content"]:
        e = s.select_one(sel)
        if e: print("  sel", sel, len(e.get_text()), "tegn")
    m = s.select_one("main") or s.body
    for el in m.find_all(True, recursive=True)[:400]:
        if el.name in ("div", "section", "article", "aside", "nav", "header", "footer", "ul") and (el.get("class") or el.get("id")):
            d = len(list(el.parents))
            if d < 14: print("  " * (d - 3), el.name, el.get("id") or "", ".".join(el.get("class", []))[:80], len(el.get_text(" ", strip=True)))
    tags = sorted(set(a["href"] for a in s.find_all("a", href=True) if "/tag/" in a["href"] or "/emne" in a["href"] or "/stikkord" in a["href"]))
    print("  TAGS", tags[:40])
    for k in ["Publisert", "Sist endret", "Oppdatert", "Dato", "Saksnummer", "Sak "]:
        for mm in list(re.finditer(k, s.get_text(" ")))[:2]:
            print("  META", re.sub(r"\s+", " ", s.get_text(" ")[mm.start():mm.start()+120]))
print("#### SPK")
spk = locs("https://www.spk.no/sitemap.xml")
print(len(spk))
c = Counter("/".join(u.split("/")[3:5]) for u in spk)
for k, v in c.most_common(60): print(f"  {v:4} {k}")
for u in spk:
    if re.search(r"(?i)regelverk|rundskriv|lov|medlem|rettighet|tolk|retningslin", u): print("  R", u)
for u in [x for x in spk if re.search(r"(?i)regelverk|rundskriv", x)][:2]: struktur(u)
print("\n#### IMDi")
imdi = [u for u in locs("https://imdi.no/sitemap.xml") if "/regelverk/" in u]
for u in imdi: print("  ", u)
for u in imdi[:1] + [x for x in imdi if x.count("/") > 6][:1]: struktur(u)
print("\n#### Sivilombudet")
siv = locs("https://www.sivilombudet.no/uttalelser-sitemap.xml")
print(len(siv), siv[:3], siv[-3:])
for u in siv[-2:]: struktur(u)
struktur("https://www.sivilombudet.no/tag/offentleglova/")
