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
Tabeller med "maanedsfiler": true leveres som én fil per måned (Søknader om dagpenger, næring); måneden
leses fra «Januar 2026 fra 01.01 til 31.01», og månedene slås sammen med kolonnen «maaned».
Tabeller med "kvartalsfiler": true i kilder.json (Navs sykefraværstabeller) leveres som egne filer
per kvartal. Kvartalet leses fra overskriftsraden i filen («2. kvartal»). Originalene ligger i
data/nav/<mappe>/original/, og TSV-filene bygges om fra alle originalene hver gang, slik at hver
tabell blir én fil med kolonnen «kvartal» (K1–K4). En ny fil for samme tabell og kvartal erstatter
den gamle. Eldre mapper k1–k4 flyttes til denne strukturen første gang skriptet kjører.
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
import nav_kvartal  # noqa: E402
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


def finn_kvartal(fil):
    """Kvartalet (1-4) fra første celle som ser ut som «2. kvartal» i et ark som har tall."""
    import openpyxl
    wb = openpyxl.load_workbook(fil, read_only=True, data_only=True)
    funnet = set()
    for ws in wb.worksheets:
        for i, rad in enumerate(ws.iter_rows(values_only=True)):
            if i > 12:
                break
            for c in rad:
                m = re.match(r"^\s*([1-4])\.\s*kvartal\s*$", str(c), re.I) if c is not None else None
                if m:
                    funnet.add(m.group(1))
    wb.close()
    if len(funnet) != 1:
        raise ValueError(
            "Fant ikke ett entydig kvartal i overskriftsradene (fant: "
            + (", ".join(sorted(funnet)) or "ingen") + ")."
        )
    return funnet.pop()


def bygg_kvartalstabell(t, ekstra=None):
    """Bygger data/nav/<mappe>/ på nytt fra alle originaler. ekstra: ny fil som ikke er flyttet dit ennå.

    Tabeller med kvartalsfiler får kolonnen «kvartal», tabeller med månedsfiler kolonnen «maaned».
    Returnerer feilmelding eller None. Mappen endres ikke hvis noe feiler.
    """
    mappe = NAV / t["mappe"]
    originaler = {}
    etikett = "kvartal"
    for f in sorted((mappe / "original").glob("*.xlsx")) if (mappe / "original").exists() else []:
        nokkel, etikett, _ = finn_periode(t, f)
        originaler[nokkel] = f
    if ekstra is not None:
        nokkel, etikett, _ = finn_periode(t, ekstra)
        originaler[nokkel] = ekstra  # ny fil for samme periode erstatter den gamle
    if not originaler:
        return None
    tmp = Path(str(mappe) + ".ny")
    shutil.rmtree(tmp, ignore_errors=True)
    kmapper = {}
    maaned = etikett == "maaned"
    try:
        for k, f in sorted(originaler.items()):
            kmapper[k] = tmp / f"p{k}"
            tittel = f"{t['tittel']}, {k}" if maaned else f"{t['tittel']}, {k}. kvartal"
            _, avvik = nav_xlsx.main(f, kmapper[k], tittel, t["kildeside"], prefiks=(etikett, k) if maaned else None)
            if avvik:
                raise ValueError(f"{f.name}: {avvik} tall i xlsx-filen ble ikke likt i TSV-en etter konvertering.")
        ut = tmp / "ut"
        if maaned:
            nav_kvartal.slaa_sammen_perioder(kmapper, etikett, ut, t["tittel"], lambda k: f"{t['tittel']}, {k}")
        else:
            nav_kvartal.slaa_sammen({int(k): m for k, m in kmapper.items()}, ut, t["tittel"])
        avvik = nav_kvartal.kontroller(kmapper, ut)
        if avvik:
            raise ValueError(f"{avvik} tall ble borte eller lagt til da periodene ble slått sammen.")
        if not list(ut.glob("*.tsv")):
            raise ValueError("Fant ingen ark med tabeller (overskriftsrad med årstall, måneder eller kvartaler).")
    except Exception as e:  # noqa: BLE001
        shutil.rmtree(tmp, ignore_errors=True)
        return str(e)
    orig = tmp / "original"
    orig.mkdir()
    for f in originaler.values():
        shutil.copy2(f, orig / f.name)
    for p in list(tmp.glob("p*")):
        shutil.rmtree(p, ignore_errors=True)
    for f in list((tmp / "ut").iterdir()):
        shutil.move(str(f), tmp / f.name)
    (tmp / "ut").rmdir()
    if mappe.exists():
        shutil.rmtree(mappe)
    tmp.rename(mappe)
    if ekstra is not None:
        ekstra.unlink()
    return None


def flytt_gamle_kvartalsmapper(tabeller):
    """Flytter originaler fra data/nav/<mappe>/k1–k4/original/ til <mappe>/original/ og bygger tabellen på nytt."""
    flyttet = []
    for t in tabeller:
        if not t.get("kvartalsfiler"):
            continue
        mappe = NAV / t["mappe"]
        gamle = [m for m in (mappe / f"k{k}" for k in range(1, 5)) if m.exists()]
        if not gamle:
            continue
        (mappe / "original").mkdir(exist_ok=True)
        for m in gamle:
            for f in (m / "original").glob("*.xlsx"):
                shutil.move(str(f), mappe / "original" / f.name)
        feil = bygg_kvartalstabell(t)
        if feil:
            raise RuntimeError(f"{t['mappe']}: {feil}")
        flyttet.append(t["mappe"])
    return flyttet


MAANEDER = ["januar", "februar", "mars", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "desember"]


def finn_maaned(fil):
    """Måneden (åååå-mm) fra teksten «Januar 2026 fra 01.01 til 31.01» i overskriftsradene."""
    import openpyxl
    wb = openpyxl.load_workbook(fil, read_only=True, data_only=True)
    funnet = set()
    for ws in wb.worksheets:
        for i, rad in enumerate(ws.iter_rows(values_only=True)):
            if i > 12:
                break
            for c in rad:
                m = re.match(r"^\s*(" + "|".join(MAANEDER) + r")\s+(\d{4})\s+fra\b", str(c), re.I) if c is not None else None
                if m:
                    funnet.add(f"{m.group(2)}-{MAANEDER.index(m.group(1).lower()) + 1:02d}")
    wb.close()
    if len(funnet) != 1:
        raise ValueError(
            "Fant ikke en entydig måned i overskriftsradene (fant: "
            + (", ".join(sorted(funnet)) or "ingen") + ")."
        )
    return funnet.pop()


def finn_periode(t, fil):
    """(nøkkel, kolonnenavn, etikett) for en fil i en tabell med kvartals- eller månedsfiler."""
    if t.get("maanedsfiler"):
        m = finn_maaned(fil)
        return m, "maaned", m
    k = finn_kvartal(fil)
    return k, "kvartal", f"K{k}"


def bygg_indeks():
    rader = ["mappe\ttabell\tfiler\tkildeside\tlagt_inn_eller_oppdatert"]
    tsvmapper = sorted({p.parent for p in NAV.rglob("*.tsv") if p.name != "indeks.tsv"})
    for mappe in tsvmapper:
        tsv = sorted(mappe.glob("*.tsv"))
        meta = {}
        for linje in tsv[0].read_text(encoding="utf-8").splitlines():
            if not linje.startswith("# "):
                break
            if ": " in linje:
                k, v = linje[2:].split(": ", 1)
                meta.setdefault(k, v)
        rader.append("\t".join([
            f"data/nav/{mappe.relative_to(NAV).as_posix()}", meta.get("Tabell", ""), " ".join(f.name for f in tsv),
            meta.get("Kildeside", ""), meta.get("Oppdatert") or meta.get("Lagt inn", ""),
        ]))
    (NAV / "indeks.tsv").write_text("\n".join(rader) + "\n", encoding="utf-8")


def main():
    tabeller = json.loads((NAV / "kilder.json").read_text(encoding="utf-8"))["tabeller"]
    filer = sorted(p for p in INNBOKS.iterdir() if p.suffix.lower() == ".xlsx") if INNBOKS.exists() else []
    lagt, feil = [], []
    for m in flytt_gamle_kvartalsmapper(tabeller):
        lagt.append(f"data/nav/{m}: kvartalsmappene k1–k4 er slått sammen til én fil per tabell")
    for fil in filer:
        feilfil = fil.with_name(fil.name + ".FEIL.txt")
        t = finn_tabell(fil, tabeller)
        if t.get("kvartalsfiler") or t.get("maanedsfiler"):
            try:
                melding = bygg_kvartalstabell(t, fil)
            except Exception as e:  # noqa: BLE001
                melding = str(e)
            if melding:
                feilfil.write_text(f"{fil.name} ble ikke lagt inn.\n{melding}\n", encoding="utf-8")
                feil.append(f"{fil.name}: {melding}")
                continue
            feilfil.unlink(missing_ok=True)
            lagt.append(f"{fil.name} -> data/nav/{t['mappe']}")
            continue
        ny = None
        mappe = NAV / t["mappe"]
        tittel = t["tittel"]
        sti = t["mappe"]
        try:
            ny = Path(str(mappe) + ".ny")
            ny.parent.mkdir(parents=True, exist_ok=True)
            if ny.exists():
                shutil.rmtree(ny)
            antall, avvik = nav_xlsx.main(fil, ny, tittel, t["kildeside"])
            if antall == 0:
                raise ValueError("Fant ingen ark med tabeller (overskriftsrad med årstall, måneder eller kvartaler).")
            if avvik:
                raise ValueError(f"{avvik} tall i xlsx-filen ble ikke likt i TSV-en etter konvertering.")
        except Exception as e:  # noqa: BLE001
            if ny is not None:
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
        lagt.append(f"{fil.name} -> data/nav/{sti}")
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
