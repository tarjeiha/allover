#!/usr/bin/env python3
"""Fagansvar for regelverkene: hvem som eier hvert regelverk, og varsler om endringer.

Hvert regelverk i regelverk.json har feltet `fagomrade`. Under `fagomrader` står navnet på
området og eieren, som er et GitHub-brukernavn (`@navn`) eller et team (`@organisasjon/team`).
Eieren står bare ett sted, så et område bytter eier ved å endre én linje.

Bruk:
  python3 verktoy/fagansvar.py --sjekk             # alle regelverk har et kjent fagområde,
                                                   # og .github/CODEOWNERS er oppdatert
  python3 verktoy/fagansvar.py --skriv             # lag .github/CODEOWNERS på nytt
  python3 verktoy/fagansvar.py --varsle --siden "2026-11-04 06:00" --til "2026-11-05 06:00"
                                                   # én sak per regelverk som er endret på main
                                                   # siden tidspunktet (krever GH_TOKEN)
  python3 verktoy/fagansvar.py --varsle --siden ... --tørr   # vis sakene uten å lage dem
"""
import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROT = Path(__file__).resolve().parent.parent
CODEOWNERS = ROT / ".github" / "CODEOWNERS"
ETIKETT = "regelverksendring"
MAKS_VIST = 12

TOPP = """\
# Lages av verktoy/fagansvar.py fra fagområdene i regelverk.json. Rediger ikke for hånd:
# endre eieren under «fagomrader» i regelverk.json og kjør `python3 verktoy/fagansvar.py --skriv`.
#
# Eierne får beskjed når en pull request berører mappene deres, og må godkjenne før den
# tas inn i main. Regelen virker først når «Require review from Code Owners» er slått på
# for main (Settings → Branches eller Rules).

# Felles filer og alt som ikke har egen eier
*  @tarjeiha
"""


def last() -> dict:
    return json.loads((ROT / "regelverk.json").read_text(encoding="utf-8"))


def regelverkene(cfg: dict) -> list[dict]:
    return [r for k in ("lover", "avtaler", "eu") for r in cfg.get(k, [])]


def feil_i(cfg: dict) -> list[str]:
    omr = cfg.get("fagomrader", {})
    feil = []
    for navn, o in omr.items():
        if not re.fullmatch(r"@[\w.-]+(/[\w.-]+)?", o.get("eier", "")):
            feil.append(f"fagområdet {navn} mangler gyldig eier (@bruker eller @organisasjon/team)")
    for r in regelverkene(cfg):
        if r.get("fagomrade") not in omr:
            feil.append(f"{r['mappe']}: fagomrade «{r.get('fagomrade')}» finnes ikke under fagomrader")
    return feil


def codeowners(cfg: dict) -> str:
    omr = cfg["fagomrader"]
    linjer = [TOPP.rstrip("\n")]
    per = defaultdict(list)
    for r in regelverkene(cfg):
        per[r["fagomrade"]].append(r["mappe"])
    for nokkel in omr:
        if not per[nokkel]:
            continue
        linjer.append(f"\n# {omr[nokkel]['navn']}")
        bredde = max(len(m) for m in per[nokkel]) + 3
        for mappe in sorted(per[nokkel]):
            linjer.append(f"/{mappe}/".ljust(bredde) + f"  {omr[nokkel]['eier']}")
    return "\n".join(linjer) + "\n"


# --- Varsler -----------------------------------------------------------------------------

def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROT, capture_output=True, text=True, check=True).stdout


def type_for(sti: str) -> str | None:
    """Hva slags endring en fil er. None betyr at den ikke gir varsel alene."""
    if sti.endswith("VEIVISER.md") or sti.endswith(".tsv") or sti.endswith(".json"):
        return None
    if "/vedtatte-endringer/" in sti:
        return "Vedtatte endringer, ikke i kraft"
    if "/rundskriv/arbeidstilsynet/" in sti:
        return "Arbeidstilsynets kommentarer"
    if "/rundskriv/" in sti:
        return "Rundskriv"
    if "/merknader/" in sti:
        return "Merknader"
    if "/original/" in sti:
        return None
    return "Lov-, forskrifts- eller avtaletekst"


def navn_for(mappe: str, sti: str, typ: str) -> str:
    """Rundskriv listes per rundskriv, paragrafer med overskriften i filen."""
    rest = sti[len(mappe) + 1:].split("/")
    if typ == "Arbeidstilsynets kommentarer":
        return rest[rest.index("arbeidstilsynet") + 1]
    if typ == "Rundskriv":
        i = rest.index("rundskriv")
        return "/".join(rest[i + 1:i + 3]) if rest[i + 1:i + 2] == ["forskrifter"] else rest[i + 1]
    fil = ROT / sti
    if typ.startswith("Lov") and fil.exists():
        for l in fil.read_text(encoding="utf-8").splitlines():
            if l.startswith("#"):
                return l.lstrip("# ").strip()
    return Path(sti).stem


def endringer(siden: str, til: str | None, mapper: dict) -> dict:
    """mappe -> {"typer": {type: set(filnavn)}, "commits": [(sha, melding)]}"""
    ut = defaultdict(lambda: {"typer": defaultdict(set), "commits": []})
    grense = [f"--until={til}"] if til else []
    logg = git("log", "HEAD", f"--since={siden}", *grense, "--first-parent", "--diff-merges=first-parent",
               "--no-renames",
               "--format=@@%H %s", "--name-only", "--", "regelverk/")
    sha = melding = None
    for linje in logg.splitlines():
        if linje.startswith("@@"):
            sha, _, melding = linje[2:].partition(" ")
            continue
        if not linje.strip():
            continue
        mappe = next((m for m in mapper if linje.startswith(m + "/")), None)
        typ = type_for(linje) if mappe else None
        if typ is None:
            continue
        ut[mappe]["typer"][typ].add(navn_for(mappe, linje, typ))
        if not ut[mappe]["commits"] or ut[mappe]["commits"][-1][0] != sha:
            ut[mappe]["commits"].append((sha, melding))
    return ut


def naturlig(tekst: str) -> list:
    return [int(d) if d.isdigit() else d for d in re.split(r"(\d+)", tekst)]


def saktekst(eier: str, endr: dict, repo: str) -> str:
    linjer = [f"{eier}: det er lagt inn endringer i regelverket på ditt område. "
              "Se gjennom, og lukk saken når den er sett.", ""]
    for typ, filer in sorted(endr["typer"].items()):
        navn = sorted(filer, key=naturlig)
        vist = ", ".join(navn[:MAKS_VIST]) + (f" og {len(navn) - MAKS_VIST} til" if len(navn) > MAKS_VIST else "")
        linjer.append(f"- {typ} ({len(navn)}): {vist}")
    linjer += ["", "Endringene:"]
    for sha, melding in reversed(endr["commits"]):
        linjer.append(f"- {melding} ({os.environ.get('GITHUB_SERVER_URL', 'https://github.com')}/{repo}/commit/{sha})")
    return "\n".join(linjer) + "\n"


def gh(*args: str) -> str:
    return subprocess.run(["gh", *args], cwd=ROT, capture_output=True, text=True, check=True).stdout


def varsle(cfg: dict, siden: str, til: str | None, dato: str, tørr: bool) -> int:
    omr = cfg["fagomrader"]
    mapper = {r["mappe"]: r for r in regelverkene(cfg)}
    repo = os.environ.get("GITHUB_REPOSITORY", "tarjeiha/allover")
    alle = endringer(siden, til, mapper)
    if not alle:
        print(f"Ingen endringer i regelverket siden {siden}.")
        return 0
    if not tørr:
        gh("label", "create", ETIKETT, "--color", "0E8A16", "--force",
           "--description", "Endringer i regelverket som den fagansvarlige skal se gjennom")
    for mappe in sorted(alle, key=lambda m: mapper[m]["navn"]):
        eier = omr[mapper[mappe]["fagomrade"]]["eier"]
        tittel = f"Endret: {mapper[mappe]['navn']} ({dato})"
        tekst = saktekst(eier, alle[mappe], repo)
        if tørr:
            print(f"## {tittel}\n{tekst}")
            continue
        finnes = gh("issue", "list", "--state", "all", "--label", ETIKETT, "--search",
                    f'"{tittel}" in:title', "--json", "title", "--jq", ".[].title").splitlines()
        if tittel in finnes:
            print(f"Finnes allerede: {tittel}")
            continue
        args = ["issue", "create", "--title", tittel, "--label", ETIKETT, "--body", tekst]
        if "/" not in eier:  # en person kan tildeles saken, et team nevnes bare i teksten
            args += ["--assignee", eier.lstrip("@")]
        print(gh(*args).strip())
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--sjekk", action="store_true")
    g.add_argument("--skriv", action="store_true")
    g.add_argument("--varsle", action="store_true")
    ap.add_argument("--siden", help="tidspunkt git forstår, f.eks. «2026-11-05 06:00 +0000»")
    ap.add_argument("--til", help="til og med dette tidspunktet (standard: nå)")
    ap.add_argument("--dato", help="dato i sakstittelen (standard: dagens dato)")
    ap.add_argument("--tørr", action="store_true", help="vis sakene uten å lage dem")
    args = ap.parse_args()

    cfg = last()
    feil = feil_i(cfg)
    if feil:
        print("\n".join(f"FEIL: {f}" for f in feil))
        return 1
    if args.skriv:
        CODEOWNERS.write_text(codeowners(cfg), encoding="utf-8")
        print(f"Skrev {CODEOWNERS.relative_to(ROT)}")
        return 0
    if args.sjekk:
        if not CODEOWNERS.exists() or CODEOWNERS.read_text(encoding="utf-8") != codeowners(cfg):
            print("FEIL: .github/CODEOWNERS stemmer ikke med fagområdene i regelverk.json. "
                  "Kjør python3 verktoy/fagansvar.py --skriv")
            return 1
        print(f"Fagansvar OK: {len(regelverkene(cfg))} regelverk i {len(cfg['fagomrader'])} fagområder.")
        return 0
    if not args.siden:
        ap.error("--varsle krever --siden")
    dato = args.dato or subprocess.run(["date", "+%Y-%m-%d"], capture_output=True, text=True).stdout.strip()
    return varsle(cfg, args.siden, args.til, dato, args.tørr)


if __name__ == "__main__":
    sys.exit(main())
