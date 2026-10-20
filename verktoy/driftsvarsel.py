#!/usr/bin/env python3
"""Skriver driftsvarsel i SKILLVERSJONER.md når en fast hentejobb ikke har lykkes på en stund.

Alle AIDs skills henter SKILLVERSJONER.md ved hver bruk, så et varsel her når brukerne.
For hver hentejobb slås siste vellykkede kjøring opp i GitHubs API. Er den eldre enn
grensen for jobben, får området et varsel. Bare blokken mellom AUTO-markørene skrives om.
Svarer ikke API-et, står blokken urørt.

Bruk: GITHUB_TOKEN=... GITHUB_REPOSITORY=tarjeiha/allover python3 verktoy/driftsvarsel.py
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROT = Path(__file__).resolve().parent.parent
FIL = ROT / "SKILLVERSJONER.md"
AUTO_START = "<!-- AUTO-START: genereres av verktoy/driftsvarsel.py, ikke rediger for hånd -->"
AUTO_SLUTT = "<!-- AUTO-SLUTT -->"

# Arbeidsflyt, området slik brukeren forstår det, og hvor mange dager som kan gå
# mellom vellykkede kjøringer før det varsles. Grensen gir rom for én feilet kjøring.
JOBBER = [
    ("bygg-regelverk.yml", "Lov- og forskriftsteksten fra Lovdata", 3),
    ("r45-hent.yml", "Navs EØS-rundskriv (R45)", 3),
    ("stortinget-oppdater.yml", "Stortingets saker", 3),
    ("nav-tekster.yml", "Navs pressemeldinger", 4),
    ("nav-hent.yml", "Navs statistikk", 10),
    ("eurostat-hent.yml", "Eurostat-tallene", 10),
    ("oecd-hent.yml", "OECD-tallene", 10),
    ("budsjett-stortinget.yml", "Stortingets budsjettvedtak", 10),
]


def siste_vellykkede(repo: str, token: str, fil: str):
    url = f"https://api.github.com/repos/{repo}/actions/workflows/{fil}/runs?status=success&per_page=1"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as svar:
        kjøringer = json.load(svar).get("workflow_runs", [])
    if not kjøringer:
        return None
    return datetime.fromisoformat(kjøringer[0]["updated_at"].replace("Z", "+00:00"))


def lag(nå: datetime, siste: dict) -> str:
    varsler = []
    for fil, område, grense in JOBBER:
        tid = siste[fil]
        if tid is None:
            varsler.append(f"- **{område}:** ingen vellykket oppdatering er registrert.")
        elif (nå - tid).days > grense:
            varsler.append(f"- **{område}** er ikke oppdatert siden {tid.date().isoformat()}. Det nyeste fra kilden kan mangle.")
    if not varsler:
        return "Ingen driftsvarsel. Alle faste oppdateringer har gått som de skal."
    return "\n".join(varsler)


def main() -> None:
    repo = os.environ.get("GITHUB_REPOSITORY", "tarjeiha/allover")
    token = os.environ.get("GITHUB_TOKEN", "")
    try:
        siste = {fil: siste_vellykkede(repo, token, fil) for fil, _, _ in JOBBER}
    except Exception as feil:  # API-et svarer ikke: behold forrige varsel
        print(f"fikk ikke slått opp kjøringene ({feil}), SKILLVERSJONER.md er uendret", file=sys.stderr)
        return
    tekst = FIL.read_text(encoding="utf-8")
    if AUTO_START not in tekst:
        sys.exit("fant ikke AUTO-blokken i SKILLVERSJONER.md")
    før, _, rest = tekst.partition(AUTO_START)
    _, _, etter = rest.partition(AUTO_SLUTT)
    ny = f"{før}{AUTO_START}\n{lag(datetime.now(timezone.utc), siste)}\n{AUTO_SLUTT}{etter}"
    if ny != tekst:
        FIL.write_text(ny, encoding="utf-8")
        print("skrev driftsvarselet i SKILLVERSJONER.md")
    else:
        print("uendret")


if __name__ == "__main__":
    main()
