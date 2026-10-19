#!/usr/bin/env python3
"""
Henter Stortingets budsjettvedtak fra data.stortinget.no og legger dem i budsjett/ÅR/stortinget/.

For hver sesjon fra START_SESJON til inneværende sesjon finner skriptet sakene om statsbudsjettet
(Prop. 1 S med tillegg, revidert nasjonalbudsjett, endringsproposisjoner og ny saldering), henter
innstillingene som XML og voteringene i sakene, og skriver per budsjettår:

    vedtak.tsv            Beløp per kapittel og post i komiteens tilråding, ett steg per rad
                          (saldert = vedtatt budsjett, rnb, endring, nysaldering). Kroner.
    rammevedtak.tsv       Rammevedtakene i Innst. 2 S (sum per rammeområde). Kroner.
    partiforslag.tsv      Sammenligningstabellene i fagkomiteenes budsjettinnstillinger: Prop. 1 S og
                          hvert partis forslag per post (tusen kroner). Kolonnen flertall=ja markerer
                          partiene som fremmet tilrådingen, altså budsjettforliket.
    anmodningsvedtak.tsv  Vedtak med vedtakskode «Anmodning» i budsjettsakene, med vedtaksnummer og tekst.
    kilder.tsv            Innstillingene som er brukt, med saker og om tilrådingen ble vedtatt.

Råfilene mellomlagres i STORTINGET_CACHE (standard .cache/stortinget), så en ny kjøring bare henter
det som mangler. Inneværende og forrige sesjon hentes alltid på nytt, med mindre STORTINGET_OFFLINE er satt.
"""

import csv
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROT = Path(__file__).resolve().parent.parent
BUDSJETT = ROT / "budsjett"
CACHE = Path(os.environ.get("STORTINGET_CACHE", ROT / ".cache" / "stortinget"))
API = "https://data.stortinget.no/eksport"
START_SESJON = "2021-2022"
AGENT = "regelverksbasen (github.com/tarjeiha/allover)"

PARTI = {
    "Arbeiderpartiet": "A", "Høyre": "H", "Fremskrittspartiet": "FrP", "Senterpartiet": "Sp",
    "Sosialistisk Venstreparti": "SV", "Rødt": "R", "Venstre": "V", "Miljøpartiet De Grønne": "MDG",
    "Kristelig Folkeparti": "KrF", "Pasientfokus": "PF",
}


# ---------- henting ----------

def hent(url, navn, fersk=False):
    sti = CACHE / navn
    if sti.exists() and (not fersk or os.environ.get("STORTINGET_OFFLINE")):
        return sti.read_bytes()
    if os.environ.get("STORTINGET_OFFLINE"):
        raise urllib.error.HTTPError(url, 404, "ikke i mellomlageret", None, None)
    for forsok in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": AGENT})
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
            break
        except Exception:  # noqa: BLE001
            if forsok == 3:
                raise
            time.sleep(2 ** (forsok + 1))
    sti.parent.mkdir(parents=True, exist_ok=True)
    sti.write_bytes(data)
    time.sleep(0.2)
    return data


def hent_json(sti, navn, fersk=False):
    sep = "&" if "?" in sti else "?"
    d = json.loads(hent(f"{API}/{sti}{sep}format=json", navn, fersk).decode("utf-8-sig"))
    return d


def liste(d):
    return next((v for v in d.values() if isinstance(v, list)), [])


def sesjoner():
    d = hent_json("sesjoner", "sesjoner.json", fersk=True)
    naa = d["innevaerende_sesjon"]["id"]
    alle = sorted(s["id"] for s in liste(d))
    return [s for s in alle if START_SESJON <= s <= naa], naa


# ---------- utvalg av saker ----------

def aar_fra_innst(kode):
    """inns-202425-099s -> ('Innst. 99 S (2024–2025)', 2024, 2025)"""
    m = re.match(r"inns-(\d{4})(\d{2})-(\d{3})s$", kode)
    y1 = int(m.group(1))
    return f"Innst. {int(m.group(3))} S ({y1}–{y1 + 1})", y1, y1 + 1


def velg_saker(saker):
    """Gir {innstillingskode: {aar, fase, saker, titler}}."""
    valgt = {}
    for s in saker:
        tittel = re.sub(r"\s+", " ", s.get("korttittel") or "")
        henv = s.get("henvisning") or ""
        m = re.search(r"statsbudsjettet\s+(\d{4})", tittel, re.I)
        if not m or re.search(r"Riksrevisjon|Svalbard", tittel):
            continue
        for nr, a, b in re.findall(r"Innst\. (\d+) S \((\d{4})-(\d{4})\)", henv):
            kode = f"inns-{a}{b[2:]}-{int(nr):03d}s"
            _, y1, y2 = aar_fra_innst(kode)
            aar = int(m.group(1))
            if aar == y1:
                fase = "nysaldering"
            elif re.search(r"Revidert nasjonalbudsjett|Tilleggsbevilgninger og omprioriteringer", tittel):
                fase = "rnb"
            elif re.match(r"(Statsbudsjettet|Endring av Prop\. 1 S|Finansinnstillingen)", tittel):
                fase = "rammer" if int(nr) == 2 else "saldert"
            else:
                fase = "endring"
            v = valgt.setdefault(kode, {"aar": aar, "fase": fase, "saker": [], "titler": []})
            if ["rnb", "rammer", "saldert", "nysaldering", "endring"].index(fase) < \
                    ["rnb", "rammer", "saldert", "nysaldering", "endring"].index(v["fase"]):
                v["fase"] = fase
            if s["id"] not in v["saker"]:
                v["saker"].append(s["id"])
                v["titler"].append(tittel)
    return valgt


# ---------- lesing av innstillinger ----------

def tekst(e):
    return re.sub(r"\s+", " ", "".join(e.itertext())).strip()


def tall(s):
    s = s.replace("−", "-").replace("–", "-").replace(" ", "").replace("\xa0", "")
    return int(s) if re.fullmatch(r"-?\d+", s) else None


FRA_TIL = re.compile(r"fr[aå]\s+(?:kr\.?\s*)?(-?[\d  ]+?)\s+til\s+(?:kr\.?\s*)?(-?[\d  ]+)")
ENDRING = re.compile(r"(økes|auka|aukast|forhøyes|reduseres|redusert|reduserast|nedsettes|nedjusteres|oppjusteres)\s+med", re.I)
NED = re.compile(r"redu|ned", re.I)


def postnavn(f):
    me = ENDRING.search(f)
    navn = f[:me.start()] if me else f
    return re.sub(r"[\s,]*\b(blir|vert|skal)?\s*$", "", navn).strip(" ,")


def vedtaksrader(rot):
    """Rader fra beløpstabellene under komiteens tilråding."""
    ut = []
    for vedtak in rot.iter("VedtakS"):
        for tbl in vedtak.iter("table"):
            th = tbl.find("tgroup/thead")
            hode = tekst(th) if th is not None else ""
            if "Kap" not in hode or "Kroner" not in hode or "Formål" not in hode:
                continue
            type_, kap, kapnavn, forrige = "", None, "", None
            for row in tbl.find("tgroup/tbody").iter("row"):
                celler = [tekst(e) for e in row.findall("entry")]
                if len(celler) == 1:
                    t = celler[0].lower()
                    type_ = "utgift" if "utgift" in t else "inntekt" if "inntekt" in t else type_
                    continue
                if len(celler) < 3:
                    continue
                k, p, f = celler[0], celler[1], celler[2]
                belop = [b for b in (tall(c) for c in celler[3:]) if b is not None]
                m = FRA_TIL.search(f)
                if m and forrige and not p:
                    forrige["fra"], forrige["til"] = tall(m.group(1)), tall(m.group(2))
                    continue
                if re.fullmatch(r"\d+", k):
                    kap = int(k)
                    if not p:
                        kapnavn = f.rstrip(":")
                        continue
                if not (re.fullmatch(r"\d+", p) and kap is not None and belop):
                    continue
                d = {"type": type_ or ("utgift" if kap < 3000 else "inntekt"), "kap": kap, "kapnavn": kapnavn,
                     "post": int(p), "postnavn": postnavn(f),
                     "belop": belop[0], "endring": "", "fra": ""}
                me = ENDRING.search(f)
                if me:
                    d["endring"] = -belop[0] if NED.match(me.group(1)) else belop[0]
                    m = FRA_TIL.search(f)
                    if m:
                        d["fra"], d["til"] = tall(m.group(1)), tall(m.group(2))
                ut.append(d)
                forrige = d
    for d in ut:
        d["merknad"] = ""
        if d["endring"] != "":
            til = d.pop("til", None)
            if til is None or d["fra"] in ("", None):
                d["belop"], d["fra"] = "", ""
                d["merknad"] = "innstillingen oppgir ikke fra og til"
            elif til - d["fra"] != d["endring"]:
                d["belop"] = til
                d["merknad"] = f"innstillingen oppgir fra kr {d['fra']} til kr {til}, som ikke stemmer med endringen"
            else:
                d["belop"] = til
    return ut


def rammevedtak(rot):
    ut = []
    for vedtak in rot.iter("VedtakS"):
        for tbl in vedtak.iter("table"):
            th = tbl.find("tgroup/thead")
            if th is None or "Betegnelse" not in tekst(th):
                continue
            for row in tbl.find("tgroup/tbody").iter("row"):
                c = [tekst(e) for e in row.findall("entry")]
                if len(c) >= 3 and tall(c[-1]) is not None:
                    ut.append({"nr": c[0], "betegnelse": c[1], "belop": tall(c[-1])})
        break
    return ut


def tilradingspartier(rot):
    kt = rot.find(".//KomTilrading")
    if kt is None:
        return set()
    t = tekst(kt)[:600]
    m = re.search(r"fremmes av (?:komiteens )?medlem\w*(?: i komiteen)? fra (.+?)\.", t)
    if not m:
        return set()
    navn, ut = m.group(1), set()
    for n in sorted(PARTI, key=len, reverse=True):  # «Venstre» står også i «Sosialistisk Venstreparti»
        if n in navn:
            ut.add(PARTI[n])
            navn = navn.replace(n, "")
    return ut


def partiforslag(rot, flertall):
    ut = []
    for tbl in rot.iter("table"):
        th = tbl.find("tgroup/thead")
        if th is None:
            continue
        hode = [tekst(e) for e in th.iter("entry")]
        if len(hode) < 5 or not hode[3].startswith("Prop. 1 S"):
            continue
        partier = hode[4:]
        type_, kap, kapnavn = "", None, ""
        for row in tbl.find("tgroup/tbody").iter("row"):
            c = [tekst(e) for e in row.findall("entry")]
            if len(c) == 1:
                t = c[0].lower()
                type_ = "utgift" if "utgift" in t else "inntekt" if "inntekt" in t else type_
                continue
            if len(c) < len(hode):
                continue
            if re.fullmatch(r"\d+", c[0]):
                kap = int(c[0])
                if not c[1]:
                    kapnavn = c[2]
                    continue
            if not re.fullmatch(r"\d+", c[1]) or kap is None:
                continue
            prop = tall(c[3]) if c[3] else None
            for parti, verdi in zip(partier, c[4:]):
                m = re.match(r"(-?[\d  ]+)\s*\(([^)]*)\)", verdi)
                forslag = tall(m.group(1)) if m else tall(verdi)
                if forslag is None:
                    continue
                koder = {x.strip() for x in re.split(r",| og ", re.sub(r"^Komiteens tilråding \((.*)\)$", r"\1", parti))}
                ut.append({"type": type_ or ("utgift" if kap < 3000 else "inntekt"), "kap": kap, "kapnavn": kapnavn,
                           "post": int(c[1]), "postnavn": c[2], "prop_1_s": "" if prop is None else prop, "parti": parti,
                           "forslag": forslag, "endring": "" if prop is None else forslag - prop,
                           "flertall": "ja" if flertall and koder == flertall else ""})
    return ut


# ---------- voteringer ----------

def voteringer(sak_id, fersk):
    return liste(hent_json(f"voteringer?sakid={sak_id}", f"voteringer/{sak_id}.json", fersk))


def ren_html(s):
    s = re.sub(r"\s+", " ", s or "")
    s = re.sub(r"<li[^>]*>", "\n- ", s)
    s = re.sub(r"</p>|<br\s*/?>", "\n", s)
    s = html.unescape(re.sub(r"<[^>]+>", "", s))
    return "\n".join(re.sub(r"\s+", " ", l).strip() for l in s.splitlines() if l.strip())


def anmodninger(vot, fersk):
    ut = []
    for v in vot:
        if not v.get("vedtatt"):
            continue
        vid = v["votering_id"]
        vedtak = liste(hent_json(f"voteringsvedtak?voteringid={vid}", f"vedtak/{vid}.json", fersk))
        anm = [x for x in vedtak if (x.get("vedtak_kode") or "").lower().startswith("anmodning")]
        if not anm:
            continue
        forslag = liste(hent_json(f"voteringsforslag?voteringid={vid}", f"forslag/{vid}.json", fersk))
        for x in anm:
            ref = x.get("vedtak_referanse") or ""
            nr = re.search(r"nr\. (\d+)", ref)
            kort = ref.strip("() ").rstrip(".")
            f = next((f for f in forslag if (f.get("forslag_betegnelse_kort") or "").strip().rstrip(".") == kort), None)
            if f is None and nr:
                f = next((f for f in forslag if f"nr. {nr.group(1)} " in (f.get("forslag_betegnelse_kort") or "") + " "), None)
            if f is None and len(forslag) == 1:
                f = forslag[0]
            ut.append({"vedtak_nr": x.get("vedtak_nummer"), "referanse": ref.strip("() "),
                       "partier": (f or {}).get("forslag_paa_vegne_av_tekst") or "",
                       "tekst": ren_html((f or {}).get("forslag_tekst") or x.get("vedtak_tekst") or "")})
    return ut


def tilrading_vedtatt(vot):
    rel = [v for v in vot if re.search(r"tilråding|[Rr]omertall|Komiteens", v.get("votering_tema") or "")]
    if not rel:
        return "ukjent"
    return "ja" if any(v.get("vedtatt") for v in rel) else "nei"


# ---------- skriving ----------

def skriv_tsv(sti, rader, kolonner):
    sti.parent.mkdir(parents=True, exist_ok=True)
    with open(sti, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=kolonner, delimiter="\t", extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        for r in rader:
            w.writerow({k: ("" if r.get(k) is None else str(r.get(k)).replace("\t", " ").replace("\n", " / ")) for k in kolonner})


def main():
    liste_sesjoner, naa = sesjoner()
    forrige = f"{int(naa[:4]) - 1}-{naa[:4]}"
    per_aar = {}
    feil = []
    for ses in liste_sesjoner:
        fersk = ses in (naa, forrige)
        saker = liste(hent_json(f"saker?sesjonid={ses}", f"saker/{ses}.json", fersk))
        for kode, info in velg_saker(saker).items():
            navn, y1, _ = aar_fra_innst(kode)
            a = per_aar.setdefault(info["aar"], {"innst": {}})
            if kode in a["innst"]:
                continue
            a["innst"][kode] = info
            info["navn"] = navn
            fersk_innst = fersk and f"{y1}-{y1 + 1}" in (naa, forrige)
            try:
                xml = hent(f"{API}/publikasjon?publikasjonid={kode}", f"innst/{kode}.xml", fersk_innst)
                info["rot"] = ET.fromstring(xml)
            except urllib.error.HTTPError as e:
                if e.code != 404:
                    feil.append(f"{navn}: kunne ikke hente ({e})")
                info["rot"] = None  # 404: innstillingen er ikke publisert ennå
            except Exception as e:  # noqa: BLE001
                feil.append(f"{navn}: kunne ikke hente eller lese ({e})")
                info["rot"] = None
            vot = []
            for sid in info["saker"]:
                try:
                    vot += voteringer(sid, fersk_innst)
                except Exception as e:  # noqa: BLE001
                    feil.append(f"{navn}, sak {sid}: voteringer feilet ({e})")
            info["vot"] = vot

    for aar, a in sorted(per_aar.items()):
        if all(i["rot"] is None for i in a["innst"].values()):
            print(f"{aar}: ingen innstillinger publisert ennå")
            continue
        vedtak, ramme, parti, anm, kilder = [], [], [], [], []
        for kode, info in sorted(a["innst"].items(), key=lambda x: (x[0][5:11], int(x[0][12:15]))):
            rot = info["rot"]
            base = {"aar": aar, "fase": info["fase"], "innstilling": info["navn"]}
            antall = 0
            if rot is not None:
                try:
                    rader = vedtaksrader(rot)
                    vedtak += [{**base, **r} for r in rader]
                    antall = len(rader)
                    feil += [f"{info['navn']}: kap. {r['kap']} post {r['post']}: {r['merknad']}" for r in rader if r["merknad"]]
                except ValueError as e:
                    feil.append(f"{info['navn']}: {e}")
                if info["fase"] == "rammer":
                    ramme += [{**base, **r} for r in rammevedtak(rot)]
                if info["fase"] == "saldert":
                    parti += [{**base, **r} for r in partiforslag(rot, tilradingspartier(rot))]
            try:
                anm += [{**base, **r} for r in anmodninger(info["vot"], False)]
            except Exception as e:  # noqa: BLE001
                feil.append(f"{info['navn']}: anmodningsvedtak feilet ({e})")
            kilder.append({**base, "saker": ", ".join(map(str, info["saker"])), "titler": " | ".join(info["titler"]),
                           "poster": antall, "tilrading_vedtatt": tilrading_vedtatt(info["vot"]),
                           "lenke": f"https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Innstillinger/Stortinget/"
                                    f"{kode[5:9]}-{int(kode[5:9]) + 1}/{kode}/"})
        mappe = BUDSJETT / str(aar) / "stortinget"
        skriv_tsv(mappe / "vedtak.tsv", vedtak, ["aar", "fase", "innstilling", "type", "kap", "kapnavn", "post", "postnavn", "belop", "endring", "fra", "merknad"])
        skriv_tsv(mappe / "rammevedtak.tsv", ramme, ["aar", "innstilling", "nr", "betegnelse", "belop"])
        skriv_tsv(mappe / "partiforslag.tsv", parti, ["aar", "innstilling", "type", "kap", "kapnavn", "post", "postnavn", "prop_1_s", "parti", "flertall", "forslag", "endring"])
        skriv_tsv(mappe / "anmodningsvedtak.tsv", anm, ["aar", "fase", "innstilling", "vedtak_nr", "referanse", "partier", "tekst"])
        skriv_tsv(mappe / "kilder.tsv", kilder, ["aar", "fase", "innstilling", "saker", "titler", "poster", "tilrading_vedtatt", "lenke"])
        print(f"{aar}: {len(kilder)} innstillinger, {len(vedtak)} postvedtak, {len(ramme)} rammer, {len(parti)} partiforslag, {len(anm)} anmodningsvedtak")
    if feil:
        print("\nAvvik:\n" + "\n".join(f"- {x}" for x in feil))
    return 0


if __name__ == "__main__":
    sys.exit(main())
