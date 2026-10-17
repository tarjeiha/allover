"""Slår sammen Navs kvartalsfiler til én TSV per ark, med kolonnen «kvartal».

Hver kvartalsfil er allerede konvertert med nav_xlsx.py (én mappe per kvartal). Her legges
radene fra kvartal 1–4 under hverandre med K1–K4 først på raden. Årskolonnene settes sammen
til én liste (2026 finnes bare for kvartaler som er publisert), og manglende verdier står tomme.
Ark uten årskolonner (forklaringstekster) tas fra det nyeste kvartalet uten endring.
"""
import re
from collections import Counter
from pathlib import Path


def er_aar(c):
    return bool(re.fullmatch(r"(19|20)\d\d", c.strip()))


def er_overskriftsrad(celler):
    """Overskriftsrad: minst tre årstall som følger hverandre (2010, 2011, 2012 ...)."""
    aar = [int(c) for c in celler if er_aar(c)]
    return len(aar) >= 3 and all(b == a + 1 for a, b in zip(aar, aar[1:]))


def les_tsv(sti):
    """Returnerer (kommentarlinjer, blokker) der en blokk er (merkekolonner, kolonner, rader), eller None uten årsoverskrifter."""
    komm, blokker = [], []
    for linje in Path(sti).read_text(encoding="utf-8").splitlines():
        if linje.startswith("#"):
            komm.append(linje)
            continue
        celler = linje.split("\t")
        if er_overskriftsrad(celler):
            forste = next(i for i, c in enumerate(celler) if er_aar(c))
            merker = [re.sub(r"^\d\. kvartal$", "kvartal (fra arket)", c) for c in celler[:forste]]
            blokker.append((tuple(merker), celler[forste:], []))
        elif blokker:
            blokker[-1][2].append(celler)
        else:
            return komm, None
    return komm, blokker or None


def slaa_sammen(kvartalsmapper, ut, tittel):
    """kvartalsmapper: {1: mappe, 2: mappe, ...}. Skriver sammenslåtte TSV-filer og om.md til ut."""
    ut = Path(ut)
    ut.mkdir(parents=True, exist_ok=True)
    ark = {}
    for k in sorted(kvartalsmapper):
        for fil in sorted(Path(kvartalsmapper[k]).glob("*.tsv")):
            ark.setdefault(fil.name, {})[k] = fil
    for navn, per_kvartal in ark.items():
        lest = {k: les_tsv(f) for k, f in per_kvartal.items()}
        nyeste = max(lest)
        komm = [re.sub(r", \d\. kvartal$", "", l) for l in lest[nyeste][0]]
        if any(b is None for _, b in lest.values()):
            (ut / navn).write_text(per_kvartal[nyeste].read_text(encoding="utf-8").replace(
                f"{tittel}, {nyeste}. kvartal", tittel), encoding="utf-8")
            continue
        kvartaler = " ".join(f"K{k}" for k in sorted(lest))
        linjer = [l for l in komm if not l.startswith("# Kvartaler:")]
        linjer.insert(min(4, len(linjer)), f"# Kvartaler: {kvartaler}")
        blokker = {}  # merkekolonner -> (kolonner, rader per (kvartal, rad))
        for k in sorted(lest):
            for merker, kolonner, rader in lest[k][1]:
                kol, rad = blokker.setdefault(merker, ([], []))
                for c in kolonner:
                    if c not in kol:
                        kol.append(c)
                rad += [(k, kolonner, r) for r in rader]
        for merker, (kol, rader) in blokker.items():
            aar = sorted((c for c in kol if er_aar(c)), key=int)
            ekstra = [c for c in kol if not er_aar(c)]
            alle = aar + ekstra
            linjer.append("\t".join(["kvartal", *merker, *alle]))
            for k, kolonner, r in rader:
                n = len(merker)
                verdier = dict(zip(kolonner, r[n:] + [""] * (len(kolonner) - len(r[n:]))))
                linjer.append("\t".join([f"K{k}", *(r[:n] + [""] * (n - len(r[:n]))), *(verdier.get(c, "") for c in alle)]))
        (ut / navn).write_text("\n".join(linjer) + "\n", encoding="utf-8")
    nyeste = max(kvartalsmapper)
    om = (Path(kvartalsmapper[nyeste]) / "om.md")
    if om.exists():
        tekst = om.read_text(encoding="utf-8")
        (ut / "om.md").write_text(tekst.replace(f"{tittel}, {nyeste}. kvartal", tittel), encoding="utf-8")


def slaa_sammen_perioder(mapper, etikett, ut, tittel, tittel_per_periode):
    """Slår sammen TSV-er der hver rad og overskriftslinje allerede har perioden som første kolonne (nav_xlsx prefiks).

    mapper: {periode: mappe}, sortert på periode. Kommentarlinjer tas fra den nyeste perioden.
    En overskriftslinje skrives bare når den er ulik forrige overskrift.
    """
    ut = Path(ut)
    ut.mkdir(parents=True, exist_ok=True)
    perioder = sorted(mapper)
    ark = {}
    for p in perioder:
        for fil in sorted(Path(mapper[p]).glob("*.tsv")):
            ark.setdefault(fil.name, {})[p] = fil
    for navn, per in ark.items():
        nyeste = max(per)
        linjer = []
        for l in per[nyeste].read_text(encoding="utf-8").splitlines():
            if not l.startswith("#"):
                break
            linjer.append(l.replace(tittel_per_periode(nyeste), tittel))
        linjer.insert(min(4, len(linjer)), f"# Perioder: {' '.join(sorted(per))}")
        forrige = None
        for p in sorted(per):
            for l in per[p].read_text(encoding="utf-8").splitlines():
                if l.startswith("#"):
                    continue
                if l.startswith(etikett + "\t"):
                    if l == forrige:
                        continue
                    forrige = l
                linjer.append(l)
        (ut / navn).write_text("\n".join(linjer) + "\n", encoding="utf-8")
    om = Path(mapper[max(mapper)]) / "om.md"
    if om.exists():
        (ut / "om.md").write_text(om.read_text(encoding="utf-8").replace(tittel_per_periode(max(mapper)), tittel), encoding="utf-8")


def tall_i_mappe(mappe):
    """Samme telling som nav_xlsx.tall_i_tsv, men uten kvartalskolonnen (K1–K4 er ikke tall)."""
    import nav_xlsx
    return nav_xlsx.tall_i_tsv(mappe)


def kontroller(kvartalsmapper, ut):
    """Antall tall som er tapt eller lagt til ved sammenslåingen (skal være 0)."""
    kilde = Counter()
    for m in kvartalsmapper.values():
        kilde += tall_i_mappe(m)
    kopi = tall_i_mappe(ut)
    return sum((kilde - kopi).values()) + sum((kopi - kilde).values())
