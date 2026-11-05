"""Midlertidig kartlegging av arbeidstilsynet.no, runde 2: hva står på paragrafsider og temasider."""
import re, urllib.request
from bs4 import BeautifulSoup

UA = {"User-Agent": "regelverksbase-kartlegging/1.0"}
def hent(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return r.read().decode("utf-8", "replace")

B = "https://www.arbeidstilsynet.no"
SIDER = [
    "/regelverk/lover/arbeidsmiljoloven--aml/14/14-9/",
    "/regelverk/lover/arbeidsmiljoloven--aml/10/10-4/",
    "/regelverk/forskrifter/forskrift-om-organisering-ledelse-og-medvirkning/3/3-1/",
    "/regelverk/forskrifter/forskrift-om-utforelse-av-arbeid/",
    "/regelverk/om-regelverket/",
    "/arbeidstid-og-organisering/arbeidstid/",
    "/lonn-og-ansettelse/ansettelse/",
]
for sti in SIDER:
    print("\n=====", sti)
    try:
        soup = BeautifulSoup(hent(B + sti), "lxml")
    except Exception as e:
        print("FEIL", e); continue
    main = soup.find("main") or soup.body
    for s in main(["script", "style", "nav", "footer"]): s.decompose()
    for h in main.find_all(re.compile("^h[1-4]$"))[:25]:
        print(h.name, h.get_text(" ", strip=True)[:100])
    tekst = main.get_text("\n", strip=True)
    for ord_ in ("Veiledning", "veiledning", "kommentar", "Kommentar", "Rundskriv", "rundskriv", "Tolkning", "tolkning", "Sist endret", "Publisert", "Oppdatert"):
        n = tekst.count(ord_)
        if n: print(f"  {ord_}: {n}")
    print("--- tekst (første 1500 tegn)")
    print(tekst[:1500])
