"""Midlertidig kartlegging av arbeidstilsynet.no, runde 3: HTML-struktur og navn på forskriftene."""
import re, urllib.request, json
from bs4 import BeautifulSoup

UA = {"User-Agent": "regelverksbase-kartlegging/1.0"}
def hent(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read().decode("utf-8", "replace")

B = "https://www.arbeidstilsynet.no"
sm = hent(B + "/sitemap.xml")
slugs = sorted({m for m in re.findall(r"/regelverk/forskrifter/([^/<]+)/", sm)})
print("FORSKRIFTER", len(slugs))
for s in slugs:
    try:
        soup = BeautifulSoup(hent(f"{B}/regelverk/forskrifter/{s}/"), "lxml")
    except Exception as e:
        print("FEIL", s, e); continue
    h1 = soup.find("h1").get_text(" ", strip=True) if soup.find("h1") else ""
    lov = sorted(set(re.findall(r"lovdata\.no/[^\"' ]*?(\d{4}-\d{2}-\d{2}-\d+)", str(soup))))[:3]
    fid = sorted(set(re.findall(r"FOR-\d{4}-\d{2}-\d{2}-\d+", soup.get_text(" "))))[:4]
    n = soup.get_text(" ").count("Arbeidstilsynets kommentar")
    print(f"F\t{s}\t{h1}\tkommentarer={n}\tlovdata={lov}\tFOR={fid}")

html = hent(B + "/regelverk/forskrifter/forskrift-om-utforelse-av-arbeid/")
i = html.find("Arbeidstilsynets kommentar")
print("\n===== HTML rundt første kommentar")
print(html[i-6000:i+5000])
