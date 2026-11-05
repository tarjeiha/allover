"""Midlertidig kartlegging: robots.txt, sitemap og relevante URL-er for tolkningskilder."""
import re, urllib.request, gzip, collections

UA = {"User-Agent": "regelverksbase-kartlegging/1.0"}
def hent(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
            data = r.read()
            if url.endswith(".gz") or data[:2] == b"\x1f\x8b":
                data = gzip.decompress(data)
            return r.status, data.decode("utf-8", "replace")
    except Exception as e:
        return str(e)[:120], ""

KILDER = {
    "Udir": ("https://www.udir.no", r"rundskriv|regelverkstolk|tolkning|regelverk"),
    "UDI": ("https://www.udiregelverk.no", r"rundskriv|praksis|retningslin|/rs-|/gi-|/g-|tolkning"),
    "DFØ": ("https://dfo.no", r"personalh|phb|sph|hovedtariff|statsansatt"),
    "Regjeringen (Lovavdelingen)": ("https://www.regjeringen.no", r"tolkningsuttal|lovavdeling|lovavd"),
    "Sivilombudet": ("https://www.sivilombudet.no", r"uttalelse|sak/|praksis"),
    "IMDi": ("https://www.imdi.no", r"rundskriv|regelverk|veileder|integreringslov"),
    "HK-dir": ("https://hkdir.no", r"rundskriv|regelverk|veileder|godkjenn|tolkning"),
    "SPK": ("https://www.spk.no", r"regelverk|rundskriv|lov|samordning|afp"),
}

for navn, (base, mønster) in KILDER.items():
    print(f"\n################ {navn} {base}")
    s, robots = hent(base + "/robots.txt")
    print("robots:", s)
    print("\n".join(l for l in robots.splitlines() if l.strip() and not l.startswith("#"))[:1200])
    sitemaps = re.findall(r"(?im)^sitemap:\s*(\S+)", robots) or [base + "/sitemap.xml"]
    urler, kø, sett = [], list(sitemaps), set()
    while kø and len(sett) < 40:
        sm = kø.pop(0)
        if sm in sett: continue
        sett.add(sm)
        s, t = hent(sm)
        print("sitemap", sm, s, len(t))
        if "<sitemapindex" in t:
            kø += re.findall(r"<loc>\s*(.*?)\s*</loc>", t)
        else:
            for blokk in re.findall(r"<url>(.*?)</url>", t, re.S):
                loc = re.search(r"<loc>\s*(.*?)\s*</loc>", blokk)
                mod = re.search(r"<lastmod>\s*(.*?)\s*</lastmod>", blokk)
                if loc: urler.append((loc.group(1), mod.group(1) if mod else ""))
    print(f"URL-er: {len(urler)}, med lastmod: {sum(1 for _, m in urler if m)}, sitemaps lest: {len(sett)}, igjen i kø: {len(kø)}")
    tell = collections.Counter("/".join(u.split("/")[3:5]) for u, _ in urler)
    for k, v in tell.most_common(15): print(f"{v:6}  {k}")
    treff = [(u, m) for u, m in urler if re.search(mønster, u, re.I)]
    print(f"Treff på mønster: {len(treff)}")
    for u, m in treff[:60]: print("  ", m[:10], u)
