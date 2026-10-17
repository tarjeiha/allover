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
| Nav | `data/nav.md` | Seks utvalgte tabeller lagt inn som TSV (sykefravær, dagpenger, AAP). Resten av Navs statistikk er ikke lagt inn. |

## Åpent

- **Nav:** Bare utvalgte tabeller er lagt inn (se `data/nav.md`). Nav gir tall som xlsx-filer som Claude ikke kan laste ned, så flere tabeller må legges inn av saksbehandlerne. Det mangler en fast rutine (innboks med automatisk konvertering) og en vurdering av hvilke Nav-tabeller som brukes mest.
- **Andre kilder** (IMDi, Arbeidstilsynet, Fafo, Eurostat m.fl.) er ikke vurdert.
