#!/usr/bin/env python3
"""
Legger inn statsregnskapet fra DFØs nedlasting (statsregnskapet.dfo.no/last-ned).

Filen er DFØs rådatauttrekk: én rad per år, måned, post, artskonto og virksomhet, i kroner.
Den kan være en .csv eller en .zip med én .csv. Hvert år i filen skrives på nytt under
budsjett/ÅR/statsregnskap/:

    poster.tsv      regnskap per kapittel og post for året (eller hittil i året)
    maaned.tsv      regnskap per kapittel og post per måned
    artskonto.tsv   regnskap per kapittel, post og artskonto (hva pengene er brukt til)
    virksomhet.tsv  regnskap per kapittel, post og virksomheten som har ført det

budsjett/statsregnskap.tsv viser hvilke år som ligger inne og siste måned for hvert år.
År som ikke er med i filen, røres ikke. En fil som har langt færre poster eller færre
måneder for et år enn det som ligger inne, stoppes (sjekk_omfang).

Bruk: python3 verktoy/statsregnskap.py FIL   (eller via innboks-budsjett/statsregnskapet*.zip|csv)
"""

import collections
import csv
import io
import sys
import zipfile
from datetime import date
from decimal import Decimal
from pathlib import Path

ROT = Path(__file__).resolve().parent.parent
BUDSJETT = ROT / "budsjett"
STATUS = BUDSJETT / "statsregnskap.tsv"

KOLONNER = ["År", "Periode", "Konto_no", "Konto", "Programområde_id", "Programområde", "Programkategori_id",
            "Programkategori", "Fagdepartement_id", "Fagdepartement", "Kapittel_id", "Kapittel", "Post_id", "Post",
            "Post_type", "Kontoklasse_id", "Kontoklasse", "Kontogruppe_id", "Kontogruppe", "Artskonto_id", "Artskonto",
            "Fagdepartement_Virksomhet_id", "Fagdepartement_Virksomhet", "Virksomhet_id", "Virksomhet",
            "Regnskapsfører_id", "Regnskapsfører", "Beløp"]


def _apne(sti: Path):
    """Gir rå byte-strøm for CSV-filen, også når den ligger i en zip."""
    if sti.suffix.lower() == ".zip":
        z = zipfile.ZipFile(sti)
        csver = [n for n in z.namelist() if n.lower().endswith(".csv")]
        if len(csver) != 1:
            raise ValueError(f"zip-filen skal ha nøyaktig én .csv, fant {len(csver)}")
        return z.open(csver[0])
    return sti.open("rb")


def _tekst(rå):
    start = rå.read(4096)
    try:
        start.decode("utf-8")
        koding = "utf-8-sig"
    except UnicodeDecodeError:
        koding = "cp1252"
    return io.TextIOWrapper(io.BufferedReader(_Forlenget(start, rå)), encoding=koding, newline="")


class _Forlenget(io.RawIOBase):
    """Leser først bytene vi alt har lest, så resten av strømmen."""

    def __init__(self, start, rest):
        self.start, self.rest = start, rest

    def readable(self):
        return True

    def readinto(self, b):
        if self.start:
            n = min(len(b), len(self.start))
            b[:n], self.start = self.start[:n], self.start[n:]
            return n
        data = self.rest.read(len(b))
        b[:len(data)] = data
        return len(data)


def _belop(s):
    s = s.replace("\xa0", "").replace(" ", "").replace(",", ".")
    return Decimal(s) if s not in ("", ".", "-") else Decimal(0)


def _kr(d):
    return str(int(d.quantize(Decimal(1), rounding="ROUND_HALF_UP")))


def les(sti: Path):
    rader = csv.reader(_tekst(_apne(sti)), delimiter=";")
    hode = [h.strip() for h in next(rader)]
    mangler = [k for k in KOLONNER if k.lower() not in {h.lower() for h in hode}]
    if mangler:
        raise ValueError("filen mangler kolonnene " + ", ".join(mangler) + ". Er det DFØs rådatauttrekk?")
    i = {h.lower(): n for n, h in enumerate(hode)}
    c = {k: i[k.lower()] for k in KOLONNER}
    d = dict(post=collections.defaultdict(Decimal), mnd=collections.defaultdict(Decimal),
             art=collections.defaultdict(Decimal), virk=collections.defaultdict(Decimal),
             navn={}, artnavn={}, virknavn={}, perioder=collections.defaultdict(set), n=0,
             uten_kap=collections.Counter())
    for r in rader:
        if not r:
            continue
        d["n"] += 1
        aar, per = r[c["År"]], r[c["Periode"]]
        if not r[c["Kapittel_id"]].strip():
            # Føringer på statskontoer utenfor kapittel og post (mellomværende, avregninger). Ikke bevilgningsregnskap.
            d["uten_kap"][aar] += 1
            continue
        kap, post = str(int(r[c["Kapittel_id"]])), str(int(r[c["Post_id"]][-2:]))
        b = _belop(r[c["Beløp"]])
        k = (aar, kap, post)
        d["post"][k] += b
        d["mnd"][(aar, per[-2:], kap, post)] += b
        d["art"][k + (r[c["Artskonto_id"]],)] += b
        d["virk"][k + (r[c["Virksomhet_id"]],)] += b
        d["navn"][k] = [r[c[x]] for x in ("Fagdepartement_id", "Fagdepartement", "Programområde_id", "Programområde",
                                          "Programkategori_id", "Programkategori", "Kapittel", "Post", "Post_type")]
        d["artnavn"][r[c["Artskonto_id"]]] = r[c["Artskonto"]]
        d["virknavn"][r[c["Virksomhet_id"]]] = r[c["Virksomhet"]]
        d["perioder"][aar].add(per[-2:])
    if not d["n"]:
        raise ValueError("filen har ingen rader")
    return d


def _skriv(sti: Path, hode, rader):
    sti.parent.mkdir(parents=True, exist_ok=True)
    with sti.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(hode)
        w.writerows(rader)


def _sortering(k):
    return (int(k[1]), int(k[2]))


def skriv(d):
    aarene = sorted(d["perioder"])
    for aar in aarene:
        mappe = BUDSJETT / aar / "statsregnskap"
        nøkler = sorted((k for k in d["post"] if k[0] == aar), key=_sortering)
        _skriv(mappe / "poster.tsv",
               ["kap", "post", "fdep_nr", "fdep_navn", "omr_nr", "omr_navn", "kat_nr", "kat_navn", "kap_navn",
                "post_navn", "posttype", "belop"],
               [[k[1], k[2], *d["navn"][k][:6], *d["navn"][k][6:], _kr(d["post"][k])] for k in nøkler])
        _skriv(mappe / "maaned.tsv", ["kap", "post", "maaned", "belop"],
               [[k[2], k[3], k[1], _kr(v)] for k, v in sorted(d["mnd"].items(), key=lambda x: (int(x[0][2]), int(x[0][3]), x[0][1])) if k[0] == aar])
        _skriv(mappe / "artskonto.tsv", ["kap", "post", "artskonto", "artskonto_navn", "belop"],
               [[k[1], k[2], k[3], d["artnavn"][k[3]], _kr(v)] for k, v in sorted(d["art"].items(), key=lambda x: (_sortering(x[0]), x[0][3])) if k[0] == aar])
        _skriv(mappe / "virksomhet.tsv", ["kap", "post", "orgnr", "virksomhet", "belop"],
               [[k[1], k[2], k[3], d["virknavn"][k[3]], _kr(v)] for k, v in sorted(d["virk"].items(), key=lambda x: (_sortering(x[0]), x[0][3])) if k[0] == aar])
    status = {}
    if STATUS.exists():
        with STATUS.open(encoding="utf-8") as f:
            status = {r["aar"]: r for r in csv.DictReader(f, delimiter="\t")}
    for aar in aarene:
        siste = max(d["perioder"][aar])
        status[aar] = {"aar": aar, "siste_maaned": siste, "helt_aar": "ja" if siste == "12" else "nei",
                       "poster": str(sum(1 for k in d["post"] if k[0] == aar)),
                       "rader_uten_kapittel": str(d["uten_kap"][aar]), "lagt_inn": date.today().isoformat()}
    _skriv(STATUS, ["aar", "siste_maaned", "helt_aar", "poster", "rader_uten_kapittel", "lagt_inn"],
           [[r.get(k, "") for k in ("aar", "siste_maaned", "helt_aar", "poster", "rader_uten_kapittel", "lagt_inn")] for _, r in sorted(status.items())])
    return aarene


def sjekk_omfang(d):
    """Stopper en fil som ville erstattet et år med langt færre poster, f.eks. et uttrekk for ett departement."""
    if not STATUS.exists():
        return
    with STATUS.open(encoding="utf-8") as f:
        før = {r["aar"]: r for r in csv.DictReader(f, delimiter="\t")}
    for aar in d["perioder"]:
        if aar not in før:
            continue
        nå, gammel = sum(1 for k in d["post"] if k[0] == aar), int(før[aar]["poster"])
        if nå < 0.9 * gammel:
            raise ValueError(
                f"{aar} har {nå} poster i filen, men {gammel} i basen. Filen ser ut til å være et utvalg (f.eks. ett "
                "departement). Last ned alle departementer for årene som skal oppdateres"
            )
        if max(d["perioder"][aar]) < før[aar]["siste_maaned"]:
            raise ValueError(f"{aar} går bare til måned {max(d['perioder'][aar])} i filen, men til {før[aar]['siste_maaned']} i basen")


def legg_inn(sti: Path):
    d = les(sti)
    sjekk_omfang(d)
    aarene = skriv(d)
    return f"{d['n']} rader, år {aarene[0]}–{aarene[-1]}" if len(aarene) > 1 else f"{d['n']} rader, år {aarene[0]}"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    print(legg_inn(Path(sys.argv[1])))
