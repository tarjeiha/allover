#!/usr/bin/env python3
"""
Holder Høyesteretts avgjørelser om lovene i basen oppdatert fra domstol.no.

Bruk:
    python3 verktoy/hoyesterett_hent.py              # hent nye og endrede avgjørelser
    python3 verktoy/hoyesterett_hent.py --tving      # hent alle på nytt
    python3 verktoy/hoyesterett_hent.py --maks 300   # stans etter 300 avgjørelser, resten tas neste gang
    python3 verktoy/hoyesterett_hent.py --bare-oversikt

1. Leser avgjørelsene i sitemap på domstol.no, med dato for siste endring (lastmod). Bare norske sider
   med HR-nummer fra FRA_DATO og senere tas med. Fra 1. november 2021 avidentifiserer Høyesterett alle
   avgjørelser før publisering.
2. For hver ny eller endret avgjørelse hentes siden (Høyesteretts omtale) og PDF-en (selve avgjørelsen).
   PDF-en gjøres om til tekst med pdftotext (poppler-utils).
3. Avgjørelsen kobles til lovene i basen som nevnes med paragraf («arbeidsmiljøloven § 15-7»), slik
   Sivilombudets uttalelser gjør. Den legges under loven som nevnes oftest, i
   regelverk/<lov>/rundskriv/hoyesterett/<HR-nummer>.md, og de andre lovene står i `lover:` øverst.
   Avgjørelser som nevner lover i basen bare én gang og ikke i rettsområdet, hoppes over.
4. Skriver regelverk/<lov>/rundskriv/hoyesterett/oversikt.md med alle avgjørelsene under loven.

Personvern: Parts- og advokatlinjen i omtalen tas ikke med. Høyesterett kan i en kort periode vise navn
i omtalen «av informasjonshensyn» og fjerner dem innen tre måneder. Ser tittelen eller sammendraget ut
til å inneholde personnavn (to ord med stor forbokstav etter hverandre), og avgjørelsen er yngre enn
KARANTENE_DAGER, tas omtalen ikke med. Den legges inn ved første kjøring etter at fristen er ute.
Selve avgjørelsen (PDF-en) er avidentifisert av Høyesterett og tas alltid med.

Skriver hoyesterett-rapport.txt (commit-melding og sammendrag) når noe er endret.
Henter én side om gangen med pause og åpen User-Agent. PDF-ene ligger under /globalassets/, som
robots.txt på domstol.no stenger for roboter som standard i publiseringsverktøyet. Hentingen er
avklart av forvalteren av basen (6.11.2026).
"""

import argparse
import datetime
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).parent))
import nettsider_hent as nett  # noqa: E402
from sivilombudet_hent import les_hode, lovmønstre, paragrafmønstre, paragrafnøkkel  # noqa: E402

ROT = Path(__file__).resolve().parent.parent
BASE = "https://www.domstol.no"
STATUS = ROT / "regelverk" / "hoyesterett.tsv"
RAPPORT = ROT / "hoyesterett-rapport.txt"
FRA_DATO = "2021-11-01"
KARANTENE_DAGER = 92
# Øk når konverteringen endres, så alle avgjørelsene hentes og skrives på nytt.
FORMAT = 3
KOLONNER = ["side", "lastmod", "hr", "dato", "fil", "lover", "omtale", "sjekksum", "lagt_inn"]
MÅNEDER = {m: i for i, m in enumerate(["januar", "februar", "mars", "april", "mai", "juni", "juli", "august",
                                       "september", "oktober", "november", "desember"], 1)}
TYPER = {"A": "avdeling", "U": "ankeutvalget", "S": "storkammer", "P": "plenum"}
# Ord med stor forbokstav som ofte står to og to i omtalen uten å være personnavn.
IKKE_NAVN = re.compile(
    r"^(?:Høyesterett\w*|Den|Det|De|Norges?|Norsk|Staten|Statens|Kongeriket|EØS|EU|EMD|EMK|EFTA\w*|FN|"
    r"Grunnloven|Arbeids\w*|Nav|NAV|Trygderetten|Lagmannsretten|Tingretten|Borgarting|Gulating|Frostating|"
    r"Hålogaland|Agder|Eidsivating|Oslo|Bergen|Trondheim|Stavanger|Tromsø|Den\s+europeiske|Europa\w*|"
    r"Menneskerettighets\w*|Sivilombudet|Skatteetaten|Skattedirektoratet|Konkurransetilsynet|Datatilsynet|"
    r"Domstol\w*|Riksadvokaten|Påtalemyndigheten|Kommune\w*|Fylkes\w*|Barne\w*|Utlendings\w*|Lov\w*|"
    r"I|Om|Ved|Etter|Spørsmålet|Saken|Dommen|Kjennelsen|Retten)$")
NAVNEPAR = re.compile(r"\b([A-ZÆØÅ][a-zæøåéü]+)\s+([A-ZÆØÅ][a-zæøåéü]+)\b")


def les_status() -> dict:
    if not STATUS.exists():
        return {}
    linjer = STATUS.read_text(encoding="utf-8").splitlines()
    return {r["side"]: r for r in (dict(zip(KOLONNER, l.split("\t"))) for l in linjer[1:] if l)}


def skriv_status(status: dict) -> None:
    linjer = ["\t".join(KOLONNER)] + ["\t".join(status[s].get(k, "") for k in KOLONNER) for s in sorted(status)]
    STATUS.write_text("\n".join(linjer) + "\n", encoding="utf-8")


def avgjørelser() -> dict:
    """Side (sti etter /no/hoyesterett/avgjorelser/) -> lastmod, for avgjørelser med HR-nummer fra FRA_DATO-året."""
    ut = {}
    fra_år = int(FRA_DATO[:4])
    for url, mod in nett.sitemap(BASE + "/sitemap.xml"):
        m = re.fullmatch(re.escape(BASE) + r"/no/hoyesterett/avgjorelser/((?:avgjorelser-)?(\d{4})/.+/(HR-\d{4}-\d+-[A-Z]))/?",
                         url, re.I)
        if m and int(m.group(2)) >= fra_år:
            ut[m.group(1)] = mod
    if len(ut) < 500:
        raise RuntimeError(f"fant bare {len(ut)} avgjørelser i sitemap – har nettstedet endret oppbygning?")
    return ut


def hent_pdf(url: str) -> str:
    """Teksten i PDF-en, med avsnitt skilt av tom linje og sidehoder og sidetall fjernet."""
    for forsok in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=nett.UA), timeout=120) as r:
                data = r.read()
            break
        except urllib.error.HTTPError as e:
            if e.code in (403, 404, 410) or forsok == 2:
                raise
            time.sleep(5 * (forsok + 1))
        except Exception:
            if forsok == 2:
                raise
            time.sleep(5 * (forsok + 1))
        finally:
            time.sleep(nett.PAUSE)
    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        f.write(data)
        f.flush()
        rå = subprocess.run(["pdftotext", "-enc", "UTF-8", f.name, "-"], capture_output=True, check=True).stdout
    sider = rå.decode("utf-8", "replace").split("\f")
    # Linjer som går igjen på mange sider, er sidehoder og -bunner.
    gjentatt = Counter(l.strip() for s in sider for l in set(s.splitlines()) if l.strip())
    terskel = max(3, len(sider) // 2)
    avsnitt, nå = [], []
    for side in sider:
        for linje in side.splitlines():
            l = linje.strip()
            if re.fullmatch(r"\d{1,3}|-\s*\d{1,3}\s*-|Side \d+ av \d+", l) or (gjentatt[l] >= terskel and len(sider) > 2):
                continue
            if not l:
                if nå:
                    avsnitt.append(nå)
                    nå = []
                continue
            # Nummererte avsnitt i Høyesteretts avgjørelser begynner med «(12)».
            if re.match(r"\(\d{1,3}\)(\s|$)", l) and nå:
                avsnitt.append(nå)
                nå = []
            nå.append(l)
    if nå:
        avsnitt.append(nå)
    ut = []
    for a in avsnitt:
        t = ""
        for l in a:
            if t.endswith("-") and not t.endswith(" -") and l[:1].islower():
                t = t[:-1] + l
            else:
                t = f"{t} {l}" if t else l
        t = re.sub(r"\s+", " ", t).strip()
        if not t:
            continue
        forrige = ut[-1] if ut else ""
        if re.fullmatch(r"\(\d{1,3}\)", forrige):
            # Avsnittsnummeret står alene på linjen i PDF-en: «(8)» + teksten blir «(8) Teksten».
            ut[-1] = f"{forrige} {t}"
        elif forrige and not re.match(r"\(\d{1,3}\)", t) and not re.search(r"[.!?:;»”)]$", forrige) \
                and re.match(r"[a-zæøå§\d(–-]", t):
            # Avsnitt som er delt midt i en setning (sideskift eller tom linje i PDF-en).
            ut[-1] = f"{forrige} {t}"
        else:
            ut.append(t)
    return "\n\n".join(ut)


def iso(tekst: str) -> str:
    m = re.search(r"(\d{1,2})\.\s*([a-zæøå]+)\s+(\d{4})", tekst)
    if not m or m.group(2).lower() not in MÅNEDER:
        return ""
    return f"{m.group(3)}-{MÅNEDER[m.group(2).lower()]:02d}-{int(m.group(1)):02d}"


def les_side(side: str) -> dict | None:
    try:
        html = nett.hent(f"{BASE}/no/hoyesterett/avgjorelser/{side}/")
    except urllib.error.HTTPError as e:
        if e.code in (404, 410):
            return None
        raise
    soup = BeautifulSoup(html, "lxml")
    main = soup.select_one("main")
    if not main:
        return None
    for br in main.find_all("br"):
        br.replace_with("\n")
    h1 = main.find("h1")
    ingress = main.select_one("div.ingress")
    # Første linje i ingressen er avgjørelsens form, dato, HR-nummer og saksnummer. Resten er parter og
    # advokater, som ikke tas med.
    første = ""
    if ingress:
        første = next((l.strip() for l in ingress.get_text("\n").splitlines() if l.strip()), "")
        første = re.sub(r"\s+", " ", første.replace("\xa0", " "))
    kropp = [d for d in main.select("div.xhtml-container-old-domstol") if not d.find_parent(class_="ingress")]
    pdf, felt, avsnitt = "", {}, []
    for d in kropp:
        for p in d.find_all("p"):
            a = p.find("a", href=re.compile(r"\.pdf($|\?)", re.I))
            if a:
                pdf = a["href"] if a["href"].startswith("http") else BASE + a["href"]
                continue
            t = re.sub(r"[ \t\xa0]+", " ", p.get_text(" ")).strip()
            t = re.sub(r"\s*\n\s*", "\n", t)
            m = re.match(r"(Rettsområde|Nøkkelavsnitt|Dommere)\s*:\s*(.*)", t, re.S)
            if m:
                felt[m.group(1)] = re.sub(r"\s+", " ", m.group(2)).strip()
            elif t:
                avsnitt.append(t)
    if not pdf:
        return None
    return {"tittel": re.sub(r"\s+", " ", h1.get_text(" ", strip=True)) if h1 else "", "første": første,
            "dato": iso(første), "pdf": pdf, "rettsområde": felt.get("Rettsområde", ""),
            "nøkkelavsnitt": felt.get("Nøkkelavsnitt", ""), "dommere": felt.get("Dommere", ""),
            "sammendrag": "\n\n".join(avsnitt)}


def mulige_navn(tekst: str) -> list:
    ut = []
    for linje in re.split(r"(?<=[.!?])\s+|\n+", tekst):
        for m in NAVNEPAR.finditer(linje):
            if m.start() == 0 or IKKE_NAVN.match(m.group(1)) or IKKE_NAVN.match(m.group(2)):
                continue
            ut.append(m.group(0))
    return ut


def skriv_oversikter() -> int:
    mønstre = paragrafmønstre()
    mapper = sorted({f.parent for f in (ROT / "regelverk").glob("*/rundskriv/hoyesterett/*.md")})
    for mappe in mapper:
        lovmappe = mappe.parent.parent.relative_to(ROT).as_posix()
        mønster = mønstre.get(lovmappe)
        rader = []
        for f in sorted(mappe.glob("HR-*.md")):
            tekst = f.read_text(encoding="utf-8")
            h = les_hode(tekst)
            paragrafer = set()
            for m in mønster.finditer(tekst) if mønster else []:
                for nr in re.findall(r"\d+(?:\s?-\s?\d+)?(?:[a-z]|\s[a-h])?(?![\w-])", m.group(1)):
                    paragrafer.add(re.sub(r"\s", "", nr))
            par = ", ".join(f"§ {p}" for p in sorted(paragrafer, key=paragrafnøkkel))
            rader.append((h.get("dato", ""), h.get("hr", f.stem), h.get("type", ""), h["tittel"].replace("|", "/"),
                          par, h.get("lover", "").replace(";", ","), f.name))
        rader.sort(key=lambda r: (r[0], r[1]), reverse=True)
        lov = les_hode((mappe / rader[0][6]).read_text(encoding="utf-8")).get("lov", lovmappe) if rader else lovmappe
        linjer = [
            f"# Høyesteretts avgjørelser om {lov}",
            "",
            f"{len(rader)} avgjørelser fra {FRA_DATO[8:].lstrip('0')}. november {FRA_DATO[:4]} og senere der loven "
            "nevnes med paragraf, nyeste først. Kolonnen «Paragrafer» viser paragrafene i loven som nevnes i "
            "avgjørelsen. Avgjørelser som nevner denne loven oftere enn andre lover i basen, ligger her. Andre lover "
            "som nevnes, står i kolonnen «Også».",
            "",
            "«Avdeling» og «storkammer» er dommer og kjennelser med full begrunnelse og størst vekt som prejudikat. "
            "«Ankeutvalget» er ofte korte beslutninger om å nekte en anke fremmet. Søk i tabellen etter paragraf "
            "eller stikkord, og åpne filen før du bruker avgjørelsen.",
            "",
            "| Dato | Avgjørelse | Type | Tittel | Paragrafer | Også | Fil |",
            "|---|---|---|---|---|---|---|",
        ] + [f"| {d} | {hr} | {t} | {ti} | {p} | {o} | `{fil}` |" for d, hr, t, ti, p, o, fil in rader]
        (mappe / "oversikt.md").write_text("\n".join(linjer) + "\n", encoding="utf-8")
    return len(mapper)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tving", action="store_true", help="hent alle på nytt")
    ap.add_argument("--maks", type=int, default=0, help="stans etter så mange avgjørelser (0 = ingen grense)")
    ap.add_argument("--minutter", type=int, default=0,
                    help="stans etter så mange minutter, så jobben rekker å lagre (0 = ingen grense)")
    ap.add_argument("--bare-oversikt", action="store_true", help="skriv bare oversikt.md, uten å hente")
    args = ap.parse_args()
    if args.bare_oversikt:
        print(f"Skrev oversikt for {skriv_oversikter()} lover")
        return 0

    nett.BASE = BASE
    idag = datetime.date.today()
    lover = lovmønstre()
    sider = avgjørelser()
    status = les_status()
    nye, endret, borte, hentet = [], [], [], 0
    frist = time.monotonic() + args.minutter * 60 if args.minutter else None

    for side, rå in sorted(sider.items(), key=lambda x: x[1], reverse=True):
        lastmod = f"{rå}|v{FORMAT}"
        gammel = status.get(side, {})
        # En omtale som ble holdt tilbake, hentes på nytt når karantenen er ute.
        venter = gammel.get("omtale") == "holdt" and gammel.get("dato") and \
            datetime.date.fromisoformat(gammel["dato"]) + datetime.timedelta(KARANTENE_DAGER) <= idag
        if gammel.get("lastmod") == lastmod and not venter and not args.tving:
            continue
        if gammel and not gammel.get("fil") and gammel.get("lastmod", "").split("|")[0] == rå and not args.tving:
            # Avgjørelser som ble hoppet over (for gamle eller uten lov fra basen), hentes ikke på nytt
            # bare fordi formatet er endret.
            gammel["lastmod"] = lastmod
            continue
        if (args.maks and hentet >= args.maks) or (frist and time.monotonic() > frist):
            break
        hentet += 1
        hr = side.rstrip("/").split("/")[-1].upper()
        rad = {"side": side, "lastmod": lastmod, "hr": hr}
        try:
            s = les_side(side)
        except Exception as e:
            print(f"Feil ved {side}: {e}", file=sys.stderr)
            continue
        if s is None or not s["dato"] or s["dato"] < FRA_DATO:
            status[side] = {**rad, "dato": s["dato"] if s else ""}
            continue
        try:
            tekst = hent_pdf(s["pdf"])
        except Exception as e:
            print(f"Feil ved PDF for {hr}: {e}", file=sys.stderr)
            continue
        alt = f"{s['rettsområde']}\n{tekst}"
        treff = Counter({m: len(p.findall(alt)) for m, (_, p) in lover.items()})
        treff = Counter({m: n for m, n in treff.items() if n})
        i_rettsområde = any(p.search(s["rettsområde"]) for _, p in lover.values())
        gammel_fil = ROT / gammel["fil"] if gammel.get("fil") else None
        if not treff or (sum(treff.values()) < 2 and not i_rettsområde):
            if gammel_fil and gammel_fil.exists():
                gammel_fil.unlink()
                borte.append(gammel["fil"])
            status[side] = {**rad, "dato": s["dato"]}
            continue
        hoved = treff.most_common(1)[0][0]
        lov = lover[hoved][0]
        andre = [lover[m][0]["navn"] for m, _ in treff.most_common()[1:]]
        ung = datetime.date.fromisoformat(s["dato"]) + datetime.timedelta(KARANTENE_DAGER) > idag
        navn = mulige_navn(f"{s['tittel']}\n{s['sammendrag']}")
        holdt = ung and bool(navn)
        type_ = TYPER.get(hr[-1], "")
        tittel = s["rettsområde"].split(".")[0].strip() or hr if holdt else s["tittel"] or hr
        fil = f"{hoved}/rundskriv/hoyesterett/{hr}.md"
        innhold = {"s": s, "tekst": tekst, "holdt": holdt}
        sjekksum = hashlib.sha256(json.dumps(innhold, ensure_ascii=False).encode()).hexdigest()[:16]
        if gammel.get("sjekksum") == sjekksum and gammel.get("fil") == fil and (ROT / fil).exists() and not args.tving:
            status[side] = {**gammel, **rad}
            continue
        if gammel_fil and gammel_fil.exists() and gammel["fil"] != fil:
            gammel_fil.unlink()
        form = re.match(r"Høyesteretts(?: ankeutvalgs)?\s+(\w+)", s["første"])
        form = form.group(1) if form else "avgjørelse"
        dato_tekst = re.search(r"\d{1,2}\.\s*[a-zæøå]+\s+\d{4}", s["første"])
        dato_tekst = dato_tekst.group(0) if dato_tekst else s["dato"]
        hode = "\n".join([
            "---",
            f'rundskriv: "Høyesteretts {"ankeutvalgs " if hr.endswith("-U") else ""}{form} {dato_tekst} ({hr})"',
            'utgiver: "Høyesterett"',
            f'lov: "{lov["navn"]}"',
            *([f'lover: "{"; ".join(andre)}"'] if andre else []),
            f'dato: "{s["dato"]}"',
            f'hr: "{hr}"',
            f'type: "{type_}"',
            f'kilde: "{BASE}/no/hoyesterett/avgjorelser/{side}/"',
            f'pdf: "{s["pdf"]}"',
            f'lagt_inn: "{idag.isoformat()}"',
            "---",
        ])
        deler = [hode, "", f"# {tittel.replace(chr(10), ' ')}", "", s["første"], ""]
        if s["rettsområde"]:
            deler += [f"**Rettsområde:** {s['rettsområde']}", ""]
        if s["nøkkelavsnitt"]:
            deler += [f"**Nøkkelavsnitt:** {s['nøkkelavsnitt']}", ""]
        if s["dommere"]:
            deler += [f"**Dommere:** {s['dommere']}", ""]
        deler += ["## Høyesteretts omtale", "",
                  "Omtalen er skrevet av Høyesterett og er ikke en del av avgjørelsen.", ""]
        if holdt:
            deler += [f"Omtalen tas inn tre måneder etter avgjørelsen. Les den på {BASE}/no/hoyesterett/avgjorelser/{side}/", ""]
        elif s["sammendrag"]:
            deler += [s["sammendrag"], ""]
        deler += ["## Avgjørelsen", "", tekst, ""]
        (ROT / fil).parent.mkdir(parents=True, exist_ok=True)
        (ROT / fil).write_text("\n".join(deler), encoding="utf-8")
        status[side] = {**rad, "dato": s["dato"], "fil": fil, "omtale": "holdt" if holdt else "ja",
                        "lover": "; ".join(m.removeprefix("regelverk/") for m, _ in treff.most_common()),
                        "sjekksum": sjekksum, "lagt_inn": idag.isoformat()}
        (endret if gammel.get("fil") else nye).append(f"{hr} {tittel} ({s['dato']}, {lov['navn']})")

    for side in [s for s in status if s not in sider]:
        rad = status.pop(side)
        if rad.get("fil") and (ROT / rad["fil"]).exists():
            (ROT / rad["fil"]).unlink()
            borte.append(rad["fil"])

    skriv_status(status)
    skriv_oversikter()
    gjenstår = sum(1 for s, l in sider.items() if status.get(s, {}).get("lastmod") != f"{l}|v{FORMAT}")
    print(f"Hentet {hentet}. Nye: {len(nye)}, endret: {len(endret)}, borte: {len(borte)}, gjenstår: {gjenstår}")
    if nye or endret or borte:
        melding = [f"Høyesteretts avgjørelser: {len(nye)} nye, {len(endret)} endret, {len(borte)} borte", ""]
        vis = lambda liste, ord_: [f"- {ord_}: {l}" for l in liste[:40]] + (
            [f"- … og {len(liste) - 40} til"] if len(liste) > 40 else [])
        melding += vis(nye, "Ny") + vis(endret, "Endret") + vis(borte, "Borte")
        RAPPORT.write_text("\n".join(melding) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
