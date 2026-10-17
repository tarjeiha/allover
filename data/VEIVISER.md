# Data og statistikk – veiviser

Denne mappen er en katalog over hvor tall og statistikk finnes og hvilken tabell som svarer på hvilket spørsmål. Den inneholder ikke selve tallene. Tall hentes fra kilden, så de er oppdatert.

## Regler

1. **Hent tallene fra kilden, ikke fra katalogen.** Katalogen sier hvor du skal lete. Oppgi tabell, periode og når tabellen sist ble oppdatert.
2. **Sjekk om tallet allerede står i et autoritativt dokument i basen** før du leter andre steder. Satser og beløp i folketrygden fastsettes for eksempel i budsjettvedtaket (se `budsjett/VEIVISER.md`).
3. **Skill mellom kildene.** Samme begrep kan ha ulik definisjon hos ulike kilder. Si hvilken kilde tallet kommer fra.
4. **Katalogen er kontrollert mot SSB 2026-10-17.** Tabeller kan bli avsluttet eller erstattet. Finner du ikke tabellen, søk på nytt.

## Kilder

| Kilde | Fil | Status |
|---|---|---|
| Statistisk sentralbyrå (SSB) | `data/ssb.md` | Dekket for hovedtemaene. Hentes med SSB-tilkoblingen (skillen ssb-api). |
| Nav | Ikke dekket ennå | Se «Åpent» under. |

## Åpent

- **Nav:** Tall om ledighet, ytelser og tiltak fra Nav er ikke lagt inn. Claude når ikke nav.no fra skymiljøet, så katalogen må skrives med hjelp av saksbehandlere som kjenner tabellene. Det som mangler: hvilke tabeller og filer folk bruker, hvordan de hentes, og forskjellen mellom Navs tall og SSBs tall.
- **Andre kilder** (IMDi, Arbeidstilsynet, Fafo, Eurostat m.fl.) er ikke vurdert.
