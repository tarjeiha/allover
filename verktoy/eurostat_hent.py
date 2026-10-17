#!/usr/bin/env python3
"""
Henter Eurostat-tabellene i data/eurostat/pakke.json og skriver dem som TSV til data/eurostat/.

Bruk:
    python3 verktoy/eurostat_hent.py

For hver tabell lages to filer:
  <kode>.tsv         én rad per kombinasjon av land og filterdimensjoner, én kolonne per år
  <kode>.flagg.tsv   Eurostats flagg per tall (b = brudd i serien, p = foreløpig, e = estimert m.fl.)
Øverst i hver fil står kilde, tabellkode, spørring og Eurostats oppdateringsdato som #-linjer.
Filene skrives bare på nytt når Eurostats oppdateringsdato har endret seg.
Tall skrives som Eurostat oppgir dem. Tom celle betyr at Eurostat ikke har tall.
"""
import itertools
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROT = Path(__file__).resolve().parent.parent
MAPPE = ROT / "data" / "eurostat"
BASE = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"


def hent(kode, land, filter_, fra_aar):
    par = [("format", "JSON"), ("lang", "EN"), ("sinceTimePeriod", str(fra_aar))]
    par += [("geo", g) for g in land]
    for dim, verdier in filter_.items():
        par += [(dim, v) for v in verdier]
    url = BASE + kode + "?" + urllib.parse.urlencode(par)
    req = urllib.request.Request(url, headers={"User-Agent": "regelverksbasen/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return url, json.loads(r.read().decode("utf-8"))


def til_tsv(kode, tittel, url, j, land):
    ider, storrelser = j["id"], j["size"]
    kat = {}
    for d in ider:
        c = j["dimension"][d]["category"]
        indeks = c["index"]
        koder = sorted(indeks, key=indeks.get) if isinstance(indeks, dict) else list(indeks)
        kat[d] = (koder, c.get("label", {}))
    verdier = j.get("value", {})
    status = j.get("status", {})
    if isinstance(verdier, list):
        verdier = {i: v for i, v in enumerate(verdier) if v is not None}
    rader_dim = [d for d in ider if d not in ("time", "freq")]
    ordnet = ["geo"] + [d for d in rader_dim if d != "geo"]
    aar = kat["time"][0]
    sti = {}
    stride = 1
    for d, s in zip(reversed(ider), reversed(storrelser)):
        sti[d] = stride
        stride *= s

    def pos(d, kode_):
        return kat[d][0].index(kode_) * sti[d]

    kombinasjoner = list(itertools.product(*[kat[d][0] for d in ordnet]))
    # geo først i landrekkefølgen fra pakken
    rang = {g: i for i, g in enumerate(land)}
    kombinasjoner.sort(key=lambda k: (tuple(k[1:]), rang.get(k[0], 99)))
    hode = [
        f"# Kilde: Eurostat, tabell {kode}",
        f"# Tabell: {tittel}",
        f"# Eurostat-tittel: {j.get('label', '')}",
        f"# Oppdatert hos Eurostat: {j.get('updated', '')}",
        f"# Spørring: {url}",
    ]
    for d in ordnet:
        koder, etiketter = kat[d]
        hode.append(f"# {d}: " + "; ".join(f"{k}={etiketter.get(k, k)}" for k in koder))
    tsv = hode + ["\t".join(ordnet + aar)]
    flagg = hode + ["\t".join(ordnet + ["aar", "flagg"])]
    for k in kombinasjoner:
        base = sum(pos(d, kv) for d, kv in zip(ordnet, k))
        celler = []
        for a in aar:
            p = str(base + pos("time", a))
            v = verdier.get(p)
            celler.append("" if v is None else str(v))
            if status.get(p):
                flagg.append("\t".join(list(k) + [a, str(status[p])]))
        if any(celler):
            tsv.append("\t".join(list(k) + celler))
    return "\n".join(tsv) + "\n", "\n".join(flagg) + "\n"


def main():
    pakke = json.loads((MAPPE / "pakke.json").read_text(encoding="utf-8"))
    feil = 0
    for t in pakke["tabeller"]:
        kode = t["kode"]
        try:
            url, j = hent(kode, pakke["land"], t["filter"], pakke["fra_aar"])
        except Exception as e:  # noqa: BLE001
            print(f"FEIL {kode}: {e}")
            feil += 1
            continue
        fil = MAPPE / f"{kode}.tsv"
        ny, flagg = til_tsv(kode, t["tittel"], url, j, pakke["land"])
        if fil.exists() and f"# Oppdatert hos Eurostat: {j.get('updated', '')}" in fil.read_text(encoding="utf-8"):
            print(f"uendret {kode} ({j.get('updated')})")
            continue
        fil.write_text(ny, encoding="utf-8")
        (MAPPE / f"{kode}.flagg.tsv").write_text(flagg, encoding="utf-8")
        print(f"skrev {kode}: {ny.count(chr(10))} linjer, oppdatert {j.get('updated')}")
    return 1 if feil else 0


if __name__ == "__main__":
    sys.exit(main())
