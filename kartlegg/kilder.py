"""Midlertidig kartlegging, runde 3: Statens personalhåndbok på Lovdata."""
import re, urllib.request
UA = {"User-Agent": "regelverksbase-kartlegging/1.0"}
def hent(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read().decode("utf-8", "replace")
html = hent("https://lovdata.no/dokument/SPH/sph")
print("LENGDE", len(html))
i = html.find("documentHeader"); print(re.sub(r"\s+", " ", html[max(0,i-200):i+3000]))
lenker = sorted(set(re.findall(r'href="(/dokument/SPH/sph/KAPITTEL_[\d-]+)', html)), key=lambda s: [int(x) for x in s.split("_")[-1].split("-")])
print("KAPITLER", len(lenker)); print(lenker[:20])
for m in re.finditer(r'<a[^>]*href="/dokument/SPH/sph/KAPITTEL_(\d+)(?:#[^"]*)?"[^>]*>(.*?)</a>', html):
    print("H", m.group(1), re.sub(r"<[^>]+>", "", m.group(2))[:100])
side = hent("https://lovdata.no/dokument/SPH/sph/KAPITTEL_10")
print("\n=== KAPITTEL_10", len(side))
j = side.find('id="KAPITTEL_10"'); print(side[j-500:j+6000])
for k in ["Sist endret", "Publisert", "Ikrafttredelse", "Versjon", "Dato"]:
    for m in re.finditer(k, side): print("META", re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", side[m.start():m.start()+200])))
