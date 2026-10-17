#!/usr/bin/env python3
"""
Legger xlsx-filer fra innboks-data/ inn i basen som TSV under data/nav/.

Bruk:
    python3 verktoy/data_innboks.py

For hver .xlsx-fil i innboks-data/:
  1. Filen kobles til en kjent tabell i data/nav/kilder.json (mønster mot filnavnet).
     Kjenner skriptet ikke filen, får mappen navn etter filen og kildesiden settes til «ukjent».
  2. Hvert ark konverteres med verktoy/nav_xlsx.py. Er et tall i xlsx-filen borte i TSV-en
     (eller omvendt), legges ingenting inn.
  3. Originalen flyttes til data/nav/<mappe>/original/, og data/nav/indeks.tsv bygges på nytt.
En ny fil med samme tabell erstatter den gamle. Feiler en fil, blir den liggende, og
<filnavn>.FEIL.txt forklarer hvorfor.

Skriptet skriver en oppsummering til data-innboks-rapport.txt (brukes som commit-melding).
"""
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import nav_xlsx  # noqa: E402

ROT = Path(__file__).resolve().parent.parent
INNBOKS = ROT / "innboks-data"
NAV = ROT / "data" / "nav"


def normaliser(navn):
    return re.sub(r"[\s_.\-]+", "", navn.lower())


def finn_tabell(fil, tabeller):
    n = normaliser(fil.stem)
    for t in tabeller:
        if re.search(t["monster"], n):
            return t
    mappe = nav_xlsx.slug(re.sub(r"^\d{4,6}[_ ]", "", fil.stem))
    return {"mappe": mappe, "tittel": fil.stem.replace("_", " "), "kildeside": "ukjent (ny tabell, legg den til i data/nav/kilder.json)"}


def bygg_indeks():
    rader = ["mappe\ttabell\tfiler\tkildeside\tlagt_inn_eller_oppdatert"]
    for mappe in sorted(p for p in NAV.iterdir() if p.is_dir()):
        tsv = sorted(mappe.glob("*.tsv"))
        if not tsv:
            continue
        meta = {}
        for linje in tsv[0].read_text(encoding="utf-8").splitlines():
            if not linje.startswith("# "):
                break
            if ": " in linje:
                k, v = linje[2:].split(": ", 1)
                meta.setdefault(k, v)
        rader.append("\t".join([
            f"data/nav/{mappe.name}", meta.get("Tabell", ""), " ".join(f.name for f in tsv),
            meta.get("Kildeside", ""), meta.get("Oppdatert") or meta.get("Lagt inn", ""),
        ]))
    (NAV / "indeks.tsv").write_text("\n".join(rader) + "\n", encoding="utf-8")


def main():
    tabeller = json.loads((NAV / "kilder.json").read_text(encoding="utf-8"))["tabeller"]
    filer = sorted(p for p in INNBOKS.iterdir() if p.suffix.lower() == ".xlsx") if INNBOKS.exists() else []
    lagt, feil = [], []
    for fil in filer:
        feilfil = fil.with_name(fil.name + ".FEIL.txt")
        t = finn_tabell(fil, tabeller)
        mappe = NAV / t["mappe"]
        ny = Path(str(mappe) + ".ny")
        try:
            if ny.exists():
                shutil.rmtree(ny)
            antall, avvik = nav_xlsx.main(fil, ny, t["tittel"], t["kildeside"])
            if antall == 0:
                raise ValueError("Fant ingen ark med tabeller (overskriftsrad med årstall, måneder eller kvartaler).")
            if avvik:
                raise ValueError(f"{avvik} tall i xlsx-filen ble ikke likt i TSV-en etter konvertering.")
        except Exception as e:  # noqa: BLE001
            shutil.rmtree(ny, ignore_errors=True)
            feilfil.write_text(f"{fil.name} ble ikke lagt inn.\n{e}\n", encoding="utf-8")
            feil.append(f"{fil.name}: {e}")
            continue
        if mappe.exists():
            shutil.rmtree(mappe)
        ny.rename(mappe)
        (mappe / "original").mkdir()
        shutil.move(str(fil), mappe / "original" / fil.name)
        feilfil.unlink(missing_ok=True)
        lagt.append(f"{fil.name} -> data/nav/{t['mappe']}")
    if lagt or feil:
        bygg_indeks()
        tekst = ["Data: legg inn " + str(len(lagt)) + " fil(er) fra innboks-data", ""] + lagt
        if feil:
            tekst += ["", "Ikke lagt inn:"] + feil
        Path(ROT / "data-innboks-rapport.txt").write_text("\n".join(tekst) + "\n", encoding="utf-8")
        print("\n".join(tekst))
    else:
        print("Innboksen var tom.")


if __name__ == "__main__":
    main()
