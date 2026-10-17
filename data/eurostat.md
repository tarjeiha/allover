# Eurostat

Eurostat er EUs statistikkbyrå og eier av tallene. Bruk det til å sammenligne Norge med andre land. Norge er med i de fleste arbeidsmarkedstabellene (EØS). Tallene følger felles EU-definisjoner og kan avvike fra SSB og Nav (se «Forbehold»).

## Tall som ligger i basen

En fast pakke er hentet til TSV i `data/eurostat/` (Norge, Sverige, Danmark, Finland, Tyskland og EU27, fra 2005 der Eurostat har tall):

| Fil | Innhold |
|---|---|
| `une_rt_a.tsv` | Arbeidsledighet, prosent av arbeidsstyrken, 15–74 og 15–24 år, etter kjønn |
| `lfsi_emp_a.tsv` | Sysselsatte som andel av befolkningen, 15–64 og 20–64 år, etter kjønn |
| `lfsa_ergan.tsv` | Sysselsettingsrate 20–64 år etter statsborgerskap (`NAT` innenlandsk, `FOR` utenlandsk, `NEU27_2020_FOR` fra land utenfor EU) |
| `ilc_peps01n.tsv` | Risiko for fattigdom eller sosial eksklusjon, prosent, etter kjønn |

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

Alle fem svarte med tall for Norge, Sverige, Danmark og EU for 2023–2025, unntatt `earn_mw_cur` (se over).

## Tabeller som står i Eurostats katalog, men ikke er prøvd mot API-et

- `hsw_mi08`: arbeidsulykker etter kjønn og alvorlighet (til 2024).
- `tps00198`: eldrebyrde (til 2025).
- `lfst_r_lfu2ltu`: langtidsledighet (12 måneder eller mer), regionalt (til 2025).
- `edat_lfse_22`: unge som verken er i jobb eller utdanning (NEET), regionalt (til 2025).
- `ei_lmjv_q_r2`: ledige stillinger per kvartal (til 4. kvartal 2025).

`spr_exp_sum` (sosial beskyttelse) finnes ikke lenger i API-et (HTTP 404). Finn riktig tabell for utgifter til sosial beskyttelse i katalogen før du svarer på slike spørsmål.

## Forbehold

- **Arbeidsledighet:** Eurostat bruker ILO-definisjonen fra arbeidskraftsundersøkelsen. Tallet er derfor arbeidsledighet etter AKU-metoden og ikke Navs registrerte ledige. Vis til dette når du sammenligner med Nav.
- **Tall for Norge alene:** bruk SSB (`data/ssb.md`). Eurostat er riktig kilde når tallet skal sammenlignes med andre land, og tallene kan avvike fra SSBs egne publiserte tall. Si fra om kilden.
- **Siste år:** Land leverer til ulik tid. Sjekk at alle land i en sammenligning har tall for samme år.
- **EU-snittet:** `EU27_2020` er EU uten Storbritannia og uten Norge.
