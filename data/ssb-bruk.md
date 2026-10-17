# SSB – slik henter du tall

Gjelder når du bruker SSB-tilkoblingen med verktøyene `ssb_search`, `ssb_table_metadata`, `ssb_get_data` og `ssb_get_url`. Hvilken tabell som svarer på hva, står i `data/ssb.md`. Er tilkoblingen ikke tilgjengelig, henvis brukeren til https://www.ssb.no/statbank og foreslå søkeord og variabler å se etter.

## Arbeidsflyt

1. **Avklar behovet.** Fenomen, geografi (landet, fylke, kommune), tidsperiode og nedbrytning (kjønn, alder, næring). Er spørsmålet vagt, still ett oppfølgingsspørsmål.
2. **Søk med `ssb_search`.** Bruk norske fagtermer (`konsumprisindeks`, `sysselsatte`) og vurder synonymer (folkemengde, befolkning). `title:` gir presise treff. Sjekk `timeUnit` og `lastPeriod`. Avsluttede tabeller har «(avslutta serie)» i tittelen, og tas med bare ved `include_discontinued: true`. Gjett aldri tabell-ID. De endres og avsluttes løpende.
3. **Les metadata med `ssb_table_metadata`.** `ContentsCode` sier hva som måles, `unit` hvilken enhet. Variabler med `elimination: true` kan utelates, med `elimination: false` må de med. Kodelister (`agg_KommFylker`, `agg_FemAarigGruppering`) gir aggregering. ID-ene er case-sensitive.
4. **Hent med `ssb_get_data`.** Filtrer i rekkefølgen tid, region, `ContentsCode`, andre variabler. Start smalt. Hent aldri store tabeller uten filter (maks 800 000 celler).
5. **Presenter.** Tabell med norsk tallformat (mellomrom som tusenskille), enhet, og kilde i formen «SSB, tabell {id}, sist oppdatert {dato}». Følg ellers svarreglene i `data/VEIVISER.md`. `ssb_get_url` gir en lenke brukeren kan åpne eller dele.

Gjør aldri: bland ikke koder fra ulike kodelister, anta ikke at kommunekoder er stabile over tid (sammenslåinger), og presenter ikke tall uten å forklare enheten.

## Filtersyntaks i `valueCodes`

| Uttrykk | Eksempel | Betydning |
|---|---|---|
| Eksplisitte koder | `["0301", "1103"]` | Bestemte verdier fra metadata |
| `from()` / `to()` | `["from(2020)"]` | Fra og med / til og med |
| `range()` | `["range(2018,2023)"]` | Intervall, begge endepunkter med |
| `top()` / `bottom()` | `["top(5)"]` | De siste (nyeste) / første (eldste) N |
| `*` og `?` | `["46*"]`, `["?301"]` | Null eller flere tegn / ett tegn |

Regler: `from()`, `to()`, `range()`, `top()` og `bottom()` står alene i arrayet. Eksplisitte koder og `*`/`?` kan kombineres (`["0301", "46*"]`). Tidsformat: årlig `2024`, månedlig `2024M01`, kvartalsvis `2024K1`. Kodeliste angis slik: `{"variableCode": "Region", "valueCodes": ["03","11","46"], "codelist": "agg_KommFylker"}`.

## Feilsøking

| Problem | Løsning |
|---|---|
| Resultatet overstiger 800 000 celler | Begrens tid (`top(5)`), region, kjønn eller alder, eller bruk kodeliste. Celler = produktet av antall verdier i alle variabler. |
| Tabellen finnes ikke (404) | Kontroller ID, søk på nytt. Tabellen kan være erstattet. |
| Ugyldig filter (400) | Variabel- og verdikoder må matche metadata nøyaktig. Sjekk tidsformat og at variabler med `elimination: false` har verdi. |
| Tidsavbrudd | Prøv igjen, eller snevre inn uttaket. |
| Tomt søk | Prøv synonymer, `title:` eller `include_discontinued: true`. |
| NULL-verdier | Ofte normalt i detaljerte nedbrytninger (kommune × alder × kjønn). |
| Uventede tall | Sjekk `ContentsCode` og enhet. Noen tabeller har både antall og prosent, eller indekser med basisår. |
| Brudd i tidsserier | Kommunesammenslåinger (2020, 2024) endrer kommunekoder. Næringsgrupperinger og KPI-basisår revideres. Nevn dette bare når det berører perioden i svaret. |
