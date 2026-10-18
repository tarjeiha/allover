# Innboks for budsjettdokumenter

Legg budsjettdokumenter her, så legges de inn i `budsjett/` automatisk i løpet av et par minutter.

## Slik gjør du

1. Last ned dokumentet fra regjeringen.no (Word for proposisjoner, Excel for datagrunnlaget).
2. Døp filen om etter mønsteret under. `ÅR` er budsjettåret, for eksempel 2027 for Prop. 1 S (2026–2027).
3. Åpne mappen `innboks-budsjett` på GitHub, velg **Add file → Upload files**, dra inn filene, velg **Commit directly to the main branch** og trykk **Commit changes**.

| Filnavn | Dokument | Havner i |
|---|---|---|
| `prop-1-s-ÅR-aid.docx` | AIDs Prop. 1 S | `budsjett/ÅR/prop-1-s-aid/` |
| `gul-bok-ÅR.docx` | Prop. 1 S Gul bok | `budsjett/ÅR/gul-bok/` |
| `nasjonalbudsjettet-ÅR.docx` | Meld. St. 1 Nasjonalbudsjettet | `budsjett/ÅR/nasjonalbudsjettet/` |
| `gul-bok-bevilgninger-ÅR.xlsx` | Datagrunnlag til Gul bok (alle departementer, kroner) | `budsjett/ÅR/gul-bok-bevilgninger.tsv` |

Du kan laste opp flere filer samtidig. Tall (datagrunnlaget) kan gå lenger tilbake enn tekst (proposisjonene).

## Hva som skjer

- Word-filene deles i én fil per kapittel eller delkapittel. Selve Word-filen slettes etterpå, siden den ligger på regjeringen.no.
- Excel-filen gjøres om til TSV. Første rad må ha kolonnene `kap_nr`, `post_nr` og `beløp`.
- `budsjett/VEIVISER.md` får en oversikt over hvilke år som ligger i basen.
- **Ny versjon:** Last opp en fil med samme navn, så erstattes den gamle mappen.

## Når noe stopper

Jobben legger ikke inn noe den er usikker på. Filen blir da liggende her, og en fil med samme navn og `.FEIL.txt` forklarer hvorfor. Vanlige grunner:

- Filnavnet passer ikke mønsteret.
- Word-filen har andre stilnavn enn dagens utgaver fra regjeringen.no. Eldre år kan ha en annen oppbygning.
- Excel-filen har ikke de forventede kolonnene.

Rett opp og last opp filen på nytt. `.FEIL.txt`-filen forsvinner når filen er lagt inn.
