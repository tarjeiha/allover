"""Kobler partienes alternative budsjetter mot Prop. 1 S, saldert budsjett og svar på budsjettspørsmål.

Bruk: python3 verktoy/alternative_budsjett.py [ÅR]   (standard: 2027)

Leser budsjett/ÅR/alternative-budsjett/tiltak.tsv (partienes forslag), kobling.tsv (håndført,
én rad per forslag) og virkning.tsv (håndført, kildens fordeling på kap./post per gruppe) og lager
kontroll.tsv i samme mappe. Kontroll.tsv har én rad per forslag på
AIDs område, med postnavn og beløp fra Prop. 1 S (gul-bok-bevilgninger.tsv), saldert budsjett året
før (budsjett/ÅR-1/stortinget/vedtak.tsv), kildene fra kobling.tsv med tittel og lenke, og avviket
mellom partiets beløp og beløpet i kilden.

kobling.tsv har nøkkelen parti, kap, post og tiltak, skrevet nøyaktig som i tiltak.tsv. Feltene er:
gruppe (samler partiets rader for samme tiltak, og kobler til virkning.tsv), riktig_kap_post (kap.post når partiets angivelse ikke finnes i Prop. 1 S), kilde (semikolondelt:
svar/ÅR/RUNDE/fil uten .md, prop/ÅR/kap-NNNN eller saldert/ÅR/kap.post), treff, kilde_mill
(beløpet i kilden, med samme fortegn som partiets endring), adm_kost (det kilden sier om
administrative kostnader og utviklingskostnader), andre_dep (virkninger på andre departementers
kapitler), status (se STATUSER) og merknad.

virkning.tsv har én rad per gruppe og kap./post på AIDs område, slik kilden fordeler beløpet:
gruppe, kap, post, type (utgift, administrativ eller inntekt), kilde_mill, kilde og merknad.
Summen for gruppen regnes av utgift og administrativ. Inntekter vises bare i poster_kun_i_kilde.
Feltene skal bare inneholde fakta: tall, kap./post og forutsetninger, ikke vurderinger av forslagene.
"""
import csv
import re
import sys
from pathlib import Path

ROT = Path(__file__).resolve().parent.parent
BUDSJETT = ROT / "budsjett"
STATUSER = {"samsvarer", "avviker", "rammebeløp", "ikke anslått i svar", "delvis kilde", "ingen kilde"}
NOKKEL = ("parti", "kap", "post", "tiltak")
TYPER = {"utgift", "administrativ", "inntekt"}
UT = ["parti", "side", "kap", "post", "tiltak", "endring_mill", "palopt_mill", "gruppe",
      "riktig_kap_post", "postnavn", "stikkord", "prop_mill", "saldert_mill",
      "kilde", "treff", "kilde_mill", "avvik_mill", "status", "merknad",
      "tiltak_gruppe", "gruppe_endring_mill", "gruppe_kilde_mill", "gruppe_avvik_mill", "poster_kun_i_kilde",
      "adm_kost", "andre_dep", "kildetitler", "lenker"]


def les(f):
    with open(f, encoding="utf-8", newline="") as h:
        return list(csv.DictReader(h, delimiter="\t"))


def tall(s):
    s = (s or "").strip().replace("−", "-").replace(" ", "")
    return float(s.replace(",", ".")) if re.fullmatch(r"-?\d+(,\d+)?", s) else None


def norsk(x):
    if x is None:
        return ""
    x = round(x, 1)
    return (str(int(x)) if x.is_integer() else f"{x:.1f}").replace(".", ",")


def poster(kap, post, riktig):
    """Gir [(kap, post)] for oppslag, eller [] når kapittel eller post ikke er et tall."""
    if riktig:
        m = re.fullmatch(r"(\d+)\.(\d+)", riktig)
        return [(int(m[1]), int(m[2]))] if m else []
    if not kap.isdigit():
        return []
    deler = [p.strip() for p in post.split(",")]
    return [(int(kap), int(p)) for p in deler] if all(p.isdigit() for p in deler) else []


def grupper(ut, virkning, feil):
    """Fyller gruppefeltene: partiets sum, kildens sum og poster som bare står i kilden."""
    medlemmer = {}
    for rad in ut:
        if rad["tiltak_gruppe"]:
            medlemmer.setdefault(rad["tiltak_gruppe"], []).append(rad)
    kilde = {}
    for v in virkning:
        if v["gruppe"] not in medlemmer:
            feil.append(f"virkning.tsv: gruppen {v['gruppe']} finnes ikke i kobling.tsv")
        if v["type"] not in TYPER:
            feil.append(f"virkning.tsv: ukjent type «{v['type']}» i gruppen {v['gruppe']}")
        kilde.setdefault(v["gruppe"], []).append(v)
    for g, rader in medlemmer.items():
        partiets = {(k, p) for r in rader for k, p in poster(r["kap"], r["post"], r["riktig_kap_post"])}
        sum_parti = sum(tall(r["endring_mill"]) or 0 for r in rader)
        vv = kilde.get(g, [])
        sum_kilde = sum(tall(v["kilde_mill"]) or 0 for v in vv if v["type"] != "inntekt")
        bare = []
        for v in vv:
            pp = poster(v["kap"], v["post"], "") or [(int(v["kap"]), None)]
            if not any(p in partiets or (p[1] is None and any(k == p[0] for k, _ in partiets)) for p in pp):
                bare.append(f"{v['kap']}.{v['post'] or '?'} {v['type']} {v['kilde_mill']}")
        uten_post = any(not poster(r["kap"], r["post"], r["riktig_kap_post"]) for r in rader)
        for r in rader:
            r["gruppe_endring_mill"] = norsk(sum_parti)
            if vv:
                r["gruppe_kilde_mill"] = norsk(sum_kilde)
                r["gruppe_avvik_mill"] = norsk(sum_parti - sum_kilde)
                r["poster_kun_i_kilde"] = "partiet oppgir ikke kap./post" if uten_post else "; ".join(bare)


def main():
    aar = int(sys.argv[1]) if len(sys.argv) > 1 else 2027
    mappe = BUDSJETT / str(aar) / "alternative-budsjett"
    tiltak = les(mappe / "tiltak.tsv")
    kobling = {tuple(r[k] for k in NOKKEL): r for r in les(mappe / "kobling.tsv")}
    feil = []

    gul = {}
    for r in les(BUDSJETT / str(aar) / "gul-bok-bevilgninger.tsv"):
        gul[(int(r["kap_nr"]), int(r["post_nr"]))] = r
    saldert = {}
    vedtak = BUDSJETT / str(aar - 1) / "stortinget" / "vedtak.tsv"
    if vedtak.exists():
        for r in les(vedtak):
            if r["fase"] == "saldert" and r["kap"].isdigit() and r["post"].isdigit():
                saldert[(int(r["kap"]), int(r["post"]))] = int(r["belop"])
    svar = {}
    for f in BUDSJETT.glob("*/sporsmal/*/sporsmal.tsv"):
        for r in les(f):
            svar[f"svar/{f.parent.parent.parent.name}/{f.parent.name}/{r['fil'][:-3]}"] = r

    kjente = {tuple(r[k] for k in NOKKEL) for r in tiltak}
    for k in kobling:
        if k not in kjente:
            feil.append(f"kobling.tsv: finner ikke forslaget i tiltak.tsv: {' | '.join(k)}")

    ut, uten = [], 0
    for t in tiltak:
        k = tuple(t[n] for n in NOKKEL)
        if t["dep"] != "AID" and k not in kobling:
            continue
        kb = kobling.get(k, {})
        uten += not kb
        rad = {n: t.get(n, "") for n in UT}
        rad["tiltak_gruppe"] = kb.get("gruppe", "")
        for n in ("riktig_kap_post", "kilde", "treff", "kilde_mill", "adm_kost", "andre_dep", "status", "merknad"):
            rad[n] = kb.get(n, "")
        if rad["status"] and rad["status"] not in STATUSER:
            feil.append(f"kobling.tsv: ukjent status «{rad['status']}» for {t['parti']}: {t['tiltak']}")

        pp = poster(t["kap"], t["post"], rad["riktig_kap_post"])
        if pp and all(p in gul for p in pp):
            rad["postnavn"] = "; ".join(gul[p]["post_navn"] for p in pp)
            rad["stikkord"] = "; ".join(s for s in dict.fromkeys(gul[p]["stikkord"] for p in pp) if s)
            rad["prop_mill"] = norsk(sum(float(gul[p]["beløp"]) for p in pp) / 1e6)
            if all(p in saldert for p in pp):
                rad["saldert_mill"] = norsk(sum(saldert[p] for p in pp) / 1e6)

        titler, lenker = [], []
        for ref in filter(None, (s.strip() for s in rad["kilde"].split(";"))):
            if ref.startswith("svar/"):
                s = svar.get(ref)
                if not s:
                    feil.append(f"kobling.tsv: finner ikke svaret {ref}")
                    continue
                aar_s = ref.split("/")[1]
                titler.append(f"{s['parti']} nr. {s['nr']} ({aar_s}): {s['undertittel']}")
                lenker.append(s.get("lenke", ""))
            elif ref.startswith("prop/"):
                _, a, fil = ref.split("/")
                if not (BUDSJETT / a / "prop-1-s-aid" / f"{fil}.md").exists():
                    feil.append(f"kobling.tsv: finner ikke {ref}")
                titler.append(f"Prop. 1 S ({int(a) - 1}–{a}) {fil.replace('kap-', 'kap. ').lstrip('0')}")
            elif ref.startswith("saldert/"):
                titler.append(f"Saldert budsjett {ref.split('/')[1]}, kap. {ref.split('/')[2]}")
            else:
                feil.append(f"kobling.tsv: ukjent kilde {ref}")
        rad["kildetitler"] = " | ".join(titler)
        rad["lenker"] = " ".join(l for l in lenker if l)

        e, kmill = tall(t["endring_mill"]), tall(rad["kilde_mill"])
        if rad["status"] in ("samsvarer", "avviker") and e is not None and kmill is not None:
            rad["avvik_mill"] = norsk(e - kmill)
        ut.append(rad)

    grupper(ut, les(mappe / "virkning.tsv") if (mappe / "virkning.tsv").exists() else [], feil)

    for f in feil:
        print(f, file=sys.stderr)
    if feil:
        return 1
    with open(mappe / "kontroll.tsv", "w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, UT, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(ut)
    print(f"{len(ut)} forslag i kontroll.tsv, {uten} uten rad i kobling.tsv.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
