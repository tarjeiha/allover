#!/usr/bin/env python3
"""
Henter OECD-tabellene i data/oecd/pakke.json og skriver dem som TSV til data/oecd/.

Bruk:
    python3 verktoy/oecd_hent.py

OECDs SDMX-API (sdmx.oecd.org) er åpent og krever ingen nøkkel. For hver tabell
leses rekkefølgen på dimensjonene fra datastrukturen, filteret i pakken gjøres om
til en SDMX-nøkkel, og dataene hentes som SDMX-CSV med etiketter.

For hver tabell lages to filer:
  <fil>.tsv         én rad per serie (land og filterdimensjoner), én kolonne per periode
  <fil>.flagg.tsv   OECDs merking av tall som ikke er vanlige verdier (estimert, foreløpig, brudd m.fl.)
Øverst i hver fil står kilde, tabell, spørring og koder med etiketter som #-linjer.
Filene skrives bare på nytt når innholdet har endret seg.
Tall skrives som OECD oppgir dem, bortsett fra at støy fra enkel presisjon (51.099998)
rundes til 7 gjeldende siffer. Tom celle betyr at OECD ikke har tall.
"""
import csv
import io
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROT = Path(__file__).resolve().parent.parent
MAPPE = ROT / "data" / "oecd"
BASE = "https://sdmx.oecd.org/public/rest/"
FASTE = {"STRUCTURE", "STRUCTURE_ID", "STRUCTURE_NAME", "ACTION", "TIME_PERIOD", "OBS_VALUE",
         "OBS_STATUS", "OBS_STATUS2", "OBS_STATUS3", "UNIT_MULT", "DECIMALS", "CONF_STATUS", "BASE_PER"}


PAUSE = 4  # sekunder mellom kall; OECD begrenser antall kall per minutt (HTTP 429)


def les(url, forsok=4):
    req = urllib.request.Request(url, headers={"User-Agent": "regelverksbasen/1.0 (tarjeiha/allover)"})
    for i in range(forsok):
        time.sleep(PAUSE)
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return r.read().decode("utf-8-sig")
        except urllib.error.HTTPError as e:
            if e.code != 429 or i == forsok - 1:
                raise
            time.sleep(65)


def tall(v):
    """OECD lagrer noen serier med enkel presisjon (51.099998). Slike verdier rundes til 7 gjeldende siffer."""
    if "." in v and len(v.split(".")[1]) >= 6:
        try:
            return f"{float(v):.7g}"
        except ValueError:
            return v
    return v


def dimensjoner(byraa, flyt):
    """Dimensjonene i rekkefølge, lest fra datastrukturen til dataflyten."""
    xml = les(f"{BASE}dataflow/{byraa}/{flyt}/latest?references=datastructure")
    dims = re.findall(r'<structure:Dimension id="([^"]+)"[^>]*position="(\d+)"', xml)
    if not dims:
        raise ValueError("fant ingen dimensjoner i datastrukturen")
    return [d for d, _ in sorted(dims, key=lambda x: int(x[1]))]


def hent(t, land, fra_aar):
    byraa, flyt = t["tabell"].split(",")
    dims = dimensjoner(byraa, flyt)
    filter_ = dict(t.get("filter", {}))
    filter_.setdefault("REF_AREA", land)
    ukjent = set(filter_) - set(dims)
    if ukjent:
        raise ValueError(f"ukjente dimensjoner i filteret: {', '.join(sorted(ukjent))} (tabellen har {', '.join(dims)})")
    nokkel = ".".join("+".join(filter_.get(d, [])) for d in dims)
    par = {"startPeriod": str(t.get("fra_aar", fra_aar)), "format": "csvfilewithlabels"}
    url = f"{BASE}data/{byraa},{flyt}/{nokkel}?{urllib.parse.urlencode(par)}"
    return url, dims, les(url)


def til_tsv(t, url, dims, tekst, land):
    rader = list(csv.reader(io.StringIO(tekst)))
    if len(rader) < 2:
        raise ValueError("svaret har ingen tall")
    hode, data = rader[0], rader[1:]
    pos = {k: i for i, k in enumerate(hode)}
    # I SDMX-CSV med etiketter står etiketten i kolonnen rett etter koden.
    def etikett_kol(k):
        i = pos[k] + 1
        return i if i < len(hode) and hode[i] not in dims and hode[i] not in FASTE else None

    rad_dims = ["REF_AREA"] + [d for d in dims if d != "REF_AREA" and d != "TIME_PERIOD" and d in pos]
    etiketter = {d: {} for d in rad_dims}
    serier, perioder, flagg = {}, set(), []
    status_kol = pos.get("OBS_STATUS")
    status_lbl = etikett_kol("OBS_STATUS") if "OBS_STATUS" in pos else None
    for r in data:
        if len(r) < len(hode):
            continue
        k = tuple(r[pos[d]] for d in rad_dims)
        for d in rad_dims:
            i = etikett_kol(d)
            etiketter[d].setdefault(r[pos[d]], r[i] if i is not None else r[pos[d]])
        p = r[pos["TIME_PERIOD"]]
        perioder.add(p)
        verdi = tall(r[pos["OBS_VALUE"]])
        serier.setdefault(k, {})[p] = verdi
        # Flagg tas bare med for tall som finnes (tomme celler forklarer seg selv).
        if verdi and status_kol is not None and r[status_kol] not in ("", "A"):
            tekst_ = r[status_lbl] if status_lbl is not None else ""
            flagg.append(list(k) + [p, r[status_kol], tekst_])
    # Variabler med bare én verdi i hele uttrekket tas bort fra radene og nevnes i hodet.
    faste = [d for d in rad_dims[1:] if len(etiketter[d]) == 1]
    vis = [d for d in rad_dims if d not in faste]
    idx = [rad_dims.index(d) for d in vis]
    rang = {g: i for i, g in enumerate(land)}
    perioder = sorted(perioder)
    hode_ut = [
        f"# Kilde: OECD, tabell {t['tabell']}",
        f"# Tabell: {t['tittel']}",
        f"# OECD-tittel: {data[0][pos['STRUCTURE_NAME']] if 'STRUCTURE_NAME' in pos else ''}",
        f"# Spørring: {url}",
    ]
    for d in faste:
        kode, lbl = next(iter(etiketter[d].items()))
        hode_ut.append(f"# {d} (lik for alle rader): {kode}={lbl}")
    for d in vis:
        hode_ut.append(f"# {d}: " + "; ".join(f"{k}={v}" for k, v in sorted(etiketter[d].items())))
    tsv = hode_ut + ["\t".join(vis + perioder)]
    nokler = sorted(serier, key=lambda k: (tuple(k[1:]), rang.get(k[0], 99), k[0]))
    for k in nokler:
        celler = [serier[k].get(p, "") for p in perioder]
        if any(celler):
            tsv.append("\t".join([k[i] for i in idx] + celler))
    flagg_ut = hode_ut + ["\t".join(vis + ["periode", "flagg", "betydning"])]
    for f in sorted(flagg, key=lambda f: (tuple(f[1:len(rad_dims)]), rang.get(f[0], 99), f[len(rad_dims)])):
        flagg_ut.append("\t".join([f[i] for i in idx] + f[len(rad_dims):]))
    return "\n".join(tsv) + "\n", "\n".join(flagg_ut) + "\n", len(tsv) - len(hode_ut) - 1


def main():
    pakke = json.loads((MAPPE / "pakke.json").read_text(encoding="utf-8"))
    feil = 0
    for t in pakke["tabeller"]:
        fil = MAPPE / f"{t['fil']}.tsv"
        try:
            url, dims, tekst = hent(t, pakke["land"], pakke["fra_aar"])
            ny, flagg, n = til_tsv(t, url, dims, tekst, pakke["land"])
        except urllib.error.HTTPError as e:
            print(f"FEIL {t['fil']} ({t['tabell']}): HTTP {e.code} {e.reason}")
            feil += 1
            continue
        except Exception as e:  # noqa: BLE001
            print(f"FEIL {t['fil']} ({t['tabell']}): {e}")
            feil += 1
            continue
        gammel = fil.read_text(encoding="utf-8") if fil.exists() else ""
        if gammel == ny:
            print(f"uendret {t['fil']}")
            continue
        fil.write_text(ny, encoding="utf-8")
        (MAPPE / f"{t['fil']}.flagg.tsv").write_text(flagg, encoding="utf-8")
        print(f"skrev {t['fil']}: {n} serier")
    return 1 if feil else 0


if __name__ == "__main__":
    sys.exit(main())
