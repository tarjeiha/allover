# Eurostat

Eurostat er EUs statistikkbyrå og eier av tallene. Bruk det til å sammenligne Norge med andre land. Norge er med i de fleste arbeidsmarkedstabellene (EØS). Tallene følger felles EU-definisjoner og kan avvike fra SSB og Nav (se «Forbehold»).

## Tall som ligger i basen

En fast pakke er hentet til TSV i `data/eurostat/` (Norge, Island, alle 27 EU-land og EU27 samlet, fra 2005 der Eurostat har tall):

| Fil | Innhold |
|---|---|
| `une_rt_a.tsv` | Arbeidsledighet, prosent av arbeidsstyrken, 15–74 og 15–24 år, etter kjønn |
| `lfsi_emp_a.tsv` | Sysselsatte som andel av befolkningen, 15–64, 20–64 og 55–64 år, etter kjønn (55–64 gir eldres sysselsetting) |
| `lfsa_ergan.tsv` | Sysselsettingsrate 20–64 år etter statsborgerskap (`NAT` innenlandsk, `FOR` utenlandsk, `NEU27_2020_FOR` fra land utenfor EU) |
| `ilc_peps01n.tsv` | Risiko for fattigdom eller sosial eksklusjon, prosent, etter kjønn |
| `une_ltu_a.tsv` | Langtidsledighet (12 måneder eller mer), 15–74 år, etter kjønn. `unit=PC_UNE` er andel av de ledige, `PC_ACT` er andel av arbeidsstyrken |
| `edat_lfse_20.tsv` | Unge som verken er i jobb eller utdanning (NEET), 15–24 og 15–29 år, etter kjønn, prosent |
| `gov_10a_exp.tsv` | Offentlige utgifter til sosial beskyttelse (COFOG GF10) og undergruppene sykdom/uførhet (GF1001), alderdom (GF1002), familie/barn (GF1004) og arbeidsledighet (GF1005), prosent av BNP |
| `trng_lfse_01.tsv` | Deltakelse i utdanning og opplæring siste fire uker, 25–64 og 55–64 år, etter kjønn, prosent |

Hver fil har én rad per land og filterkombinasjon og én kolonne per år. Øverst står kilde, tabellkode, Eurostats oppdateringsdato og spørringen som ble brukt. `<kode>.flagg.tsv` har Eurostats flagg per tall. Flagg `b` betyr brudd i serien, `p` foreløpig tall, `e` estimert og `u` lav pålitelighet. Vis flagg bare når de gjelder tallene i svaret. Pakken er definert i `data/eurostat/pakke.json`, og jobben «Hent Eurostat-tall» oppdaterer filene hver mandag. Er svaret avhengig av en tabell eller et land som ikke er i pakken, hent fra API-et under.

## Slik henter du tall fra API-et

Eurostat har et åpent API uten innlogging. Mal:

```
https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/<tabellkode>?format=JSON&lang=EN&geo=NO&geo=SE&geo=DK&geo=EU27_2020&lastTimePeriod=5
```

Legg til ett filter per dimensjon, for eksempel `&sex=T&age=Y15-74&unit=PC_ACT`. Svaret er JSON-stat: `dimension` har kodene, `value` har tallene og `updated` sier når tabellen sist ble oppdatert. Landkoder: `NO`, `SE`, `DK`, `FI`, `DE`, `EU27_2020` (EU-gjennomsnitt). Katalog over alle tabeller: `https://ec.europa.eu/eurostat/api/dissemination/catalogue/toc/txt?lang=en`.

**Tilgang:** API-et svarte (HTTP 200) når det ble kalt fra GitHub Actions 2026-10-17, men ble blokkert fra Claudes kodeverktøy i skymiljøet (HTTP 403). Kan du ikke nå API-et, si det og svar ikke fra hukommelsen. Oppgi alltid tabellkode og `updated` fra svaret.

## Tabeller som er kontrollert mot API-et (2026-10-17)

| Tabell | Innhold | Viktige filtre |
|---|---|---|
| `une_rt_a` | Arbeidsledighet, årlig, etter kjønn og alder | `unit=PC_ACT` (prosent av arbeidsstyrken), `age=Y15-74`, `sex=T/M/F` |
| `lfsi_emp_a` | Sysselsatte og arbeidsstyrke, årlig | `indic_em=EMP_LFS`, `unit=PC_POP` (andel av befolkningen), `age=Y20-64` |
| `lfsa_ergan` | Sysselsettingsrate etter statsborgerskap | `citizen=NAT` (innenlandske), `FOR` (utenlandske), `NEU27_2020_FOR` (fra land utenfor EU) |
| `ilc_peps01n` | Personer med risiko for fattigdom eller sosial eksklusjon, etter alder og kjønn | `unit=PC`, `age=TOTAL` |
| `earn_mw_cur` | Lovfestet minstelønn per måned, halvårlig | Gir ingen tall for Norge, Sverige og Danmark, som ikke har lovfestet minstelønn |

Alle fem svarte med tall for Norge, Sverige, Danmark og EU for 2023–2025, unntatt `earn_mw_cur` (se over). Fire tabeller ble lagt til i pakken 2026-10-18 og kontrollert i Actions (alle ga tall for Norge og Sverige):

| Tabell | Innhold | Viktige filtre |
|---|---|---|
| `une_ltu_a` | Langtidsledighet, årlig | `indic_em=LTU`, `age=Y15-74`, `unit=PC_UNE` eller `PC_ACT` |
| `edat_lfse_20` | NEET-rate, årlig | `age=Y15-24` eller `Y15-29`, `training=NO_FE_NO_NFE`, `wstatus=NEMP`, `unit=PC` |
| `gov_10a_exp` | Offentlige utgifter etter formål (COFOG), årlig | `unit=PC_GDP`, `sector=S13`, `na_item=TE`, `cofog99=GF10/GF1001/GF1002/GF1004/GF1005` |
| `trng_lfse_01` | Deltakelse i opplæring siste fire uker, årlig | `age=Y25-64` eller `Y55-64`, `unit=PC` |

`spr_exp_func` (sosial beskyttelse etter ytelsesfunksjon, ESSPROS) svarer også, men er ikke i pakken.

## Tabeller som står i Eurostats katalog, men ikke er prøvd mot API-et

- `hsw_mi08`: arbeidsulykker etter kjønn og alvorlighet (til 2024).
- `tps00198`: eldrebyrde (til 2025).
- `lfst_r_lfu2ltu`: langtidsledighet (12 måneder eller mer), regionalt (til 2025).
- `edat_lfse_22`: unge som verken er i jobb eller utdanning (NEET), regionalt (til 2025).
- `ei_lmjv_q_r2`: ledige stillinger per kvartal (til 4. kvartal 2025).

`spr_exp_sum` finnes ikke lenger i API-et (HTTP 404). Utgifter til sosial beskyttelse ligger i `gov_10a_exp` (offentlige utgifter, prosent av BNP) i pakken.

## Forbehold

- **Arbeidsledighet:** Eurostat bruker ILO-definisjonen fra arbeidskraftsundersøkelsen. Tallet er derfor arbeidsledighet etter AKU-metoden og ikke Navs registrerte ledige. Vis til dette når du sammenligner med Nav.
- **Tall for Norge alene:** bruk SSB (`data/ssb.md`). Eurostat er riktig kilde når tallet skal sammenlignes med andre land, og tallene kan avvike fra SSBs egne publiserte tall. Si fra om kilden.
- **Siste år:** Land leverer til ulik tid. Sjekk at alle land i en sammenligning har tall for samme år. I `gov_10a_exp` mangler 2025 for flere land inkludert Norge, Sverige og Danmark (siste år er 2024).
- **Langtidsledighet:** `PC_UNE` (andel av de ledige) og `PC_ACT` (andel av arbeidsstyrken) er to ulike mål. Oppgi hvilket du bruker. Små land har ofte flagg `u` (lav pålitelighet) i `.flagg.tsv`.
- **NEET:** Eurostats NEET-rate (`edat_lfse_20`, uten formell eller ikke-formell opplæring siste fire uker) er ikke det samme som SSB eller Navs tall for unge utenfor arbeid og utdanning. Si fra om kilden.
- **Offentlige utgifter:** `gov_10a_exp` gjelder offentlig forvaltning (S13) i prosent av BNP (total BNP). Prosentandelen sier ikke noe om kronebeløp, og nivået påvirkes av hvor stor BNP er.
- **EU-snittet:** `EU27_2020` er EU uten Storbritannia og uten Norge.
