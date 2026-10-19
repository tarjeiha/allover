#!/usr/bin/env python3
"""Oppsummerer hva nattbygget har endret, og avgjør om det kan legges rett i main.

Leser endringene som er lagt til med `git add -A` (sammenlignet med HEAD) og skriver en kort
oversikt i Markdown: hvilke regelverk som har fått ny tekst, hvilke paragrafer som er endret,
nye eller borte, vedtatte endringer, og hva som bare er oversikter (veivisere, indeks).

Endringen regnes som trygg å legge rett i main når ingen regelverk mister mange paragraffiler.
Store slettinger skyldes oftere feil i datasettet eller bygget enn at en lov faktisk er opphevet,
og går derfor som pull request.

Bruk: python3 verktoy/byggoppsummering.py --ut oppsummering.md
Skriver `endret=true|false` og `trygg=true|false` til $GITHUB_OUTPUT når den finnes.
"""
import argparse
import os
import re
import subprocess
from collections import defaultdict
from pathlib import Path

ROT = Path(__file__).resolve().parent.parent
MAKS_SLETTET = 5      # flere slettede paragraffiler i ett regelverk gir pull request
MAKS_VIST = 8         # paragrafer som listes per regelverk og type
OVERSIKT = {"indeks.tsv", "CLAUDE.md"}


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROT, capture_output=True, text=True, check=True).stdout


def regelverk_for(sti: str) -> str | None:
    deler = sti.split("/")
    if deler[0] != "regelverk" or len(deler) < 3:
        return None
    return "/".join(deler[:3]) if deler[1] == "eu" else "/".join(deler[:2])


def navn_for(mappe: str) -> str:
    veiviser = ROT / mappe / "VEIVISER.md"
    if veiviser.exists():
        m = re.match(r"#\s+(.+?)(?::\s*veiviser)?\s*$", veiviser.read_text(encoding="utf-8").splitlines()[0])
        if m:
            return m.group(1)
    return mappe.split("/")[-1]


def tittel_for(sti: str) -> str:
    """Overskriften i paragraffilen, ellers filnavnet. Slettede filer leses fra HEAD."""
    fil = ROT / sti
    try:
        tekst = fil.read_text(encoding="utf-8") if fil.exists() else git("show", f"HEAD:{sti}")
    except subprocess.CalledProcessError:
        return Path(sti).stem
    for linje in tekst.splitlines():
        if linje.startswith("#"):
            return linje.lstrip("# ").strip()
    return Path(sti).stem


def sist_endret(tekst: str) -> dict:
    """Regelverk -> «sist endret i kraft» fra tabellen i CLAUDE.md."""
    ut = {}
    for linje in tekst.splitlines():
        m = re.match(r"\|\s*([^|]+?)\s*\|\s*`regelverk/[^`]+`\s*\|\s*([^|]+?)\s*\|$", linje)
        if m:
            ut[m.group(1)] = m.group(2)
    return ut


def naturlig(tittel: str) -> list:
    return [int(d) if d.isdigit() else d for d in re.split(r"(\d+)", tittel)]


def liste(titler: list) -> str:
    titler = sorted(titler, key=naturlig)
    vist = ", ".join(titler[:MAKS_VIST])
    return vist + (f" og {len(titler) - MAKS_VIST} til" if len(titler) > MAKS_VIST else "")


def oppsummer() -> tuple[str, bool, bool]:
    endringer = [l.split("\t") for l in git("diff", "--cached", "--name-status", "--no-renames").splitlines() if l]
    if not endringer:
        return "Ingen endringer.\n", False, True

    per = defaultdict(lambda: defaultdict(list))  # regelverk -> type -> titler
    oversikt = set()
    for status, sti in endringer:
        mappe = regelverk_for(sti)
        if sti in OVERSIKT or sti.endswith("VEIVISER.md") or mappe is None:
            oversikt.add(sti)
            continue
        if "/vedtatte-endringer/" in sti:
            per[mappe]["vedtatt"].append(tittel_for(sti))
            continue
        if "/merknader/" in sti or "/rundskriv/" in sti:
            oversikt.add(sti)
            continue
        type_ = {"A": "ny", "D": "borte"}.get(status, "endret")
        per[mappe][type_].append(tittel_for(sti))

    gammel = sist_endret(git("show", "HEAD:CLAUDE.md"))
    ny = sist_endret((ROT / "CLAUDE.md").read_text(encoding="utf-8"))

    linjer = []
    trygg = True
    for mappe in sorted(per, key=navn_for):
        t = per[mappe]
        navn = navn_for(mappe)
        dato = ""
        if navn in ny and gammel.get(navn) != ny[navn]:
            dato = f" (sist endret i kraft: {gammel.get(navn, '?')} → {ny[navn]})"
        linjer.append(f"**{navn}**{dato}")
        for type_, etikett in (("endret", "Endret"), ("ny", "Ny"), ("borte", "Borte"),
                               ("vedtatt", "Vedtatt, ikke i kraft")):
            if t[type_]:
                linjer.append(f"- {etikett} ({len(t[type_])}): {liste(t[type_])}")
        if len(t["borte"]) > MAKS_SLETTET:
            trygg = False
            linjer.append(f"- ⚠️ {len(t['borte'])} paragraffiler er borte. Sjekk at det stemmer før det tas inn.")
        linjer.append("")

    if not per:
        linjer.append("Ingen endringer i lov-, forskrifts- eller EU-tekst.\n")
    if oversikt:
        linjer.append(f"Oversikter som er bygget på nytt: {len(oversikt)} filer (veivisere, indeks.tsv o.l.).")
    return "\n".join(linjer).strip() + "\n", True, trygg


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ut", type=Path, required=True)
    args = ap.parse_args()
    tekst, endret, trygg = oppsummer()
    args.ut.write_text(tekst, encoding="utf-8")
    print(tekst)
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as f:
            f.write(f"endret={str(endret).lower()}\ntrygg={str(trygg).lower()}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
