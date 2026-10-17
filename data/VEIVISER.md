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
| Nav | `data/nav.md` | Sykefravær (alle kvartal i samme fil, kolonnen `kvartal`), dagpenger, AAP, uføretrygd, nedsatt arbeidsevne, alderspensjon, helt ledige, ledige stillinger, tiltaksdeltakere og arbeidsindikator lagt inn som TSV. AFP i privat sektor, gjenlevendeytelser, krigspensjon, supplerende stønad, kontantstøtte, utbetalinger, utenforskap og trygdesvindel er lagt inn. Barnetrygd, foreldrepenger og sosialhjelp finnes ikke som xlsx hos Nav. |

## Åpent

- **Nav:** Utvalgte tabeller er lagt inn (se `data/nav.md`). Nav gir tall som xlsx-filer som Claude ikke kan laste ned, så flere tabeller må legges inn av saksbehandlerne. Nav-filer legges i `innboks-data/` og konverteres automatisk. Det mangler en vurdering av hvilke Nav-tabeller som brukes mest.
- **Andre kilder** (IMDi, Arbeidstilsynet, Fafo, Eurostat m.fl.) er ikke vurdert.
