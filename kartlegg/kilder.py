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
print("#### Sivilombudet, runde 5")
siv = sitemap = []
for sm in ["https://www.sivilombudet.no/uttalelser-sitemap.xml", "https://www.sivilombudet.no/uttalelser-sitemap2.xml"]:
    t = hent(sm)
    par = re.findall(r"<loc>\s*(.*?)\s*</loc>\s*<lastmod>\s*(.*?)\s*</lastmod>", t)
    print(sm, len(par), "med lastmod", par[:2])
    siv += [u for u, _ in par]
siv = [u for u in siv if u.count("/") == 5 and "/en/" not in u and "/smj/" not in u]
print("uttalelser", len(siv))
for u in siv[-3:-1] + siv[100:101]:
    struktur(u)
    s = BeautifulSoup(hent(u), "lxml")
    a = s.select_one("main article") or s.select_one("article") or s.select_one("main")
    print("  TEKST", re.sub(r"\s+", " ", a.get_text(" "))[:1500])
    print("  LENKER", sorted(set(x["href"] for x in a.find_all("a", href=True)))[:30])
    for el in a.find_all(True):
        if el.get("class") and re.search(r"(?i)meta|tag|term|categ|lov|date|dato|saks", " ".join(el["class"])):
            print("  META-EL", el.name, el["class"], re.sub(r"\s+", " ", el.get_text(" ", strip=True))[:200])
