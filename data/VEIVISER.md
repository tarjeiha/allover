# Data og statistikk – veiviser

Denne mappen er en katalog over hvor tall og statistikk finnes og hvilken tabell som svarer på hvilket spørsmål. Den inneholder ikke selve tallene. Tall hentes fra kilden, så de er oppdatert.

## Regler

1. **Hent tallene fra kilden, ikke fra katalogen.** Katalogen sier hvor du skal lete. Oppgi tabell, periode og når tabellen sist ble oppdatert.
2. **Sjekk om tallet allerede står i et autoritativt dokument i basen** før du leter andre steder. Satser og beløp i folketrygden fastsettes for eksempel i budsjettvedtaket (se `budsjett/VEIVISER.md`).
3. **Skill mellom kildene.** Samme begrep kan ha ulik definisjon hos ulike kilder. Si hvilken kilde tallet kommer fra.
4. **Katalogen er kontrollert mot SSB 2026-10-17.** Tabeller kan bli avsluttet eller erstattet. Finner du ikke tabellen, søk på nytt.

## Slik svarer du: kort svar og kvalitetssikringsversjon

Brukere av basen er også ledere og kommunikasjonsmedarbeidere som ikke selv kan kvalitetssikre tallene. Svar derfor i to lag.

**Standardsvar (kort).** Konklusjonen i 2–4 setninger med tallet, perioden og hva det måler. Kilde, eier og periode står i selve setningen («Nav, sykefraværsstatistikken, 2. kvartal 2026»), slik at svaret kan videresendes uten vedlegg. Tall du har regnet ut selv, og forbehold som kan gi et feil bilde, står også her. Nevn brudd i serien og andre avgrensninger bare når de berører perioden eller tallene i svaret. Brudd som ligger utenfor perioden det spørres om, hører hjemme i kvalitetssikringsversjonen om de skal med. Avslutt med én linje om at en kvalitetssikringsversjon finnes.

**Kvalitetssikringsversjon (på forespørsel).** Samme tall som standardsvaret, i denne rekkefølgen:
1. Svaret med nummererte kildehenvisninger [1], [2].
2. Kilder: eier, tabell med tittel og kode, ark og rad/kolonne tallet står i, lenke til eierens side, når tabellen er publisert og når den ble hentet (se `data/nav/indeks.tsv`).
3. Utregninger: formel og kildetall for alt du har regnet ut. Tall som eieren selv oppgir er merket «fra kilden».
4. Forbehold: brudd, avgrensninger og begreper som lett forveksles.
5. Til kvalitetssikrer: hva som er kontrollert maskinelt (konvertering tall for tall) og hva et menneske må vurdere (om tallet svarer på det som ble spurt om).

**Regler for begge.** Ikke slå sammen eller sammenlign tall fra ulike kilder uten å si at definisjonene kan avvike. Si «ikke dekket» når tallet ikke finnes i katalogen eller hos kilden. Tall hentes fra kilden hos eieren, som eier kvaliteten, og svaret viser alltid til eieren. Nevner du at en annen kilde har et annet tall for samme begrep (for eksempel AKU hos SSB og registrerte helt ledige hos Nav), vis tallet eller tilby det i samme setning.

## Kilder

| Kilde | Fil | Status |
|---|---|---|
| Statistisk sentralbyrå (SSB) | `data/ssb.md` | Dekket for hovedtemaene. Hentes med SSB-tilkoblingen (skillen ssb-api). |
| Nav | `data/nav.md` | Sykefravær (alle kvartal i samme fil, kolonnen `kvartal`), dagpenger, AAP, uføretrygd, nedsatt arbeidsevne, alderspensjon, helt ledige, ledige stillinger, tiltaksdeltakere og arbeidsindikator lagt inn som TSV. AFP i privat sektor, gjenlevendeytelser, krigspensjon, supplerende stønad, kontantstøtte, utbetalinger, utenforskap og trygdesvindel er lagt inn. Barnetrygd, foreldrepenger og sosialhjelp finnes ikke som xlsx hos Nav. |

## Åpent

- **Nav:** Utvalgte tabeller er lagt inn (se `data/nav.md`). Nav gir tall som xlsx-filer som Claude ikke kan laste ned, så flere tabeller må legges inn av saksbehandlerne. Nav-filer legges i `innboks-data/` og konverteres automatisk. Det mangler en vurdering av hvilke Nav-tabeller som brukes mest.
- **Eurostat:** Sammenligning mellom land, se `data/eurostat.md`.
- **Andre kilder** (IMDi, Arbeidstilsynet, Statens pensjonskasse, Fafo m.fl.) er ikke vurdert.
