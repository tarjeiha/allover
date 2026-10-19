# OECD

OECD eier tallene. Bruk OECD til å sammenligne Norge med andre land på det Eurostat ikke dekker: indikatorer for selve politikken (tiltak, ytelsesnivå, aktivitetskrav, stillingsvern, pensjon, skatt på arbeid, organisering i arbeidslivet) og land utenfor EU/EØS, som USA og Storbritannia. For ledighet og sysselsetting i Europa er Eurostat førstevalget (se `data/eurostat.md`).

## Tall som ligger i basen

En fast pakke er hentet til TSV i `data/oecd/` for Norge, Sverige, Danmark, Finland, Island, Tyskland, Nederland, Storbritannia, USA og OECD-snittet, fra 2005 der OECD har tall. Ikke alle tabeller har OECD-snitt.

| Fil | Innhold | Viktig å vite |
|---|---|---|
| `arbeidsmarkedstiltak.tsv` | Offentlige utgifter til arbeidsmarkedstiltak (prosent av BNP) og deltakere (prosent av arbeidsstyrken) etter tiltakstype (LMP) | `LMP_10T70` er aktive tiltak i alt (inkludert arbeidsformidling og administrasjon), `LMP_80_90` passive tiltak (ytelser ved ledighet og førtidspensjon) |
| `kompensasjonsgrad-ledighet.tsv` | Netto kompensasjonsgrad ved ledighet: inntekt under ledighet i prosent av inntekten før, etter 2, 12 og 60 måneder | Modellhusholdninger, se «Forbehold» |
| `minsteinntektsytelser.tsv` | Inntekt for husholdninger uten arbeid som får minsteinntektsytelser (i Norge sosialhjelp), i prosent av medianinntekten og i kroner | Modellhusholdninger |
| `aktivitetskrav.tsv` | Hvor strenge krav og sanksjoner er for mottakere av ytelser ved ledighet, skala 1–5 (1 er minst strengt) | Målt 2011, 2014, 2017, 2020, 2022 og 2024 |
| `stillingsvern.tsv` | Hvor strengt stillingsvernet er (EPL), skala 0–6 (6 er strengest), for oppsigelse og for midlertidige ansettelser | Fire metodeversjoner, se «Forbehold» |
| `pensjoner.tsv` | Pensions at a Glance: kompensasjonsgrad, pensjonsalder, inntekt og fattigdom blant eldre, sysselsetting blant eldre, levealder | Kompensasjonsgraden er fremskrevet, se «Forbehold» |
| `sosiale-utgifter.tsv` | Sosiale utgifter etter formål (alderdom, uførhet, familie, arbeidsmarked m.m.), kontant og i natura, prosent av BNP (SOCX) | `ES10` er offentlige utgifter, `ES50` netto totale (etter skatt, med private). Siste år for Norge er 2021 |
| `organisasjonsgrad.tsv` | Fagforeningsmedlemmer i prosent av lønnstakerne | |
| `tariffavtaledekning.tsv` | Lønnstakere omfattet av tariffavtale i prosent | Ikke tall for alle år |
| `gjennomsnittslonn.tsv` | Gjennomsnittlig årslønn per heltidsekvivalent, i nasjonal valuta og USD i kjøpekraftsparitet (KKP), faste (`Q`) og løpende (`V`) priser | Bruk `USD_PPP` for å sammenligne land |
| `lonnsgap-kjonn.tsv` | Lønnsgap mellom kvinner og menn blant heltidsansatte, prosent av menns lønn | `MEDIAN` er OECDs hovedmål |
| `sykefravar.tsv` | Sykefravær: fraværsuker per heltidsansatt lønnstaker per år | Annen definisjon enn Nav og SSB, se «Forbehold» |
| `innvandrere-arbeidsmarked.tsv` | Sysselsetting, ledighet og yrkesdeltakelse for innvandrere (`FB`) og innfødte (`NB`), etter kjønn | |
| `inntektsfordeling.tsv` | Gini-koeffisient og andel med inntekt under fattigdomsgrensen (50 og 60 prosent av median), etter alder | Brudd i inntektsdefinisjonen 2011/2012 |
| `skattekile.tsv` | Skatt på arbeid (Taxing Wages): skattekile, gjennomsnittlig skatt og netto lønn for modellhusholdninger | Modellhusholdninger |
| `sysselsetting-alder.tsv` | Sysselsetting, yrkesdeltakelse og ledighet etter kjønn og alder (15–24, 25–54, 55–64, 65–69, 15–64, 20–64 og 15–74 år) | Overlapper Eurostat for europeiske land |
| `arbeidstimer.tsv` | Gjennomsnittlig antall utførte arbeidstimer per sysselsatt per år | OECD advarer mot å sammenligne nivå mellom land, bruk utviklingen |

Hver fil har én rad per land og filterkombinasjon og én kolonne per år. Øverst står kilde, OECD-tabell, datoen tallene sist endret seg, OECD-tittel, spørringen som ble brukt og alle koder med etikett. OECD oppgir ingen publiseringsdato i API-et. Linjen «Tall endret» er derfor datoen da den ukentlige hentingen sist fant nye eller reviderte tall, og OECD kan ha publisert dem inntil en uke før. Oppgi den som «hentet fra OECD, tall endret <dato>» når svaret trenger en dato. Variabler som er like for alle rader, står bare i hodet. `<fil>.flagg.tsv` har OECDs merking av enkelttall, for eksempel `E` estimert, `P` foreløpig, `B` brudd i serien, `D` avvikende definisjon og `N` ikke signifikant. Vis flagg bare når de gjelder tallene i svaret. Pakken er definert i `data/oecd/pakke.json`, og jobben «Hent OECD-tall» oppdaterer filene hver mandag.

## Forbehold

- **Modellhusholdninger.** Kompensasjonsgrad, minsteinntektsytelser og skattekile regnes for tenkte husholdninger, for eksempel en enslig uten barn som tjente 67 prosent av gjennomsnittslønnen. De sier hva regelverket gir, ikke hva faktiske mottakere får. Si hvilken husholdning tallet gjelder. `INCOME_PREV` er tidligere lønn, `INCOME_PART` partnerens inntekt, og `SOC_ASS_BENEFIT`/`HOUSE_BENEFIT` sier om sosialhjelp og bostøtte er regnet med.
- **Stillingsvern i versjoner.** OECD har fire metodeversjoner (`VERSION1`–`VERSION4`). Sammenlign bare tall fra samme versjon.
- **Pensjon.** Kompensasjonsgraden i Pensions at a Glance er fremskrevet for en person som begynner å jobbe i dag og jobber hele karrieren. Den sier ikke hva dagens pensjonister får.
- **SOCX ligger etter.** Siste år for Norge er 2021. Si hvilket år tallet gjelder.
- **Sykefravær.** OECD måler fraværsuker per heltidsansatt lønnstaker per år. Nav måler tapte dagsverk som andel av avtalte dagsverk. Tallene kan ikke sammenlignes direkte.
- **Overlapp med Eurostat og SSB.** Ledighet og sysselsetting finnes hos alle tre. Definisjonene er like (ILO), men tallene kan avvike på grunn av revisjoner og aldersgrupper. For Norge avviker OECDs ledighetstall fra Eurostats før 2025 (ledighet 15–24 år i 2019: 10,0 hos OECD og 11,7 hos Eurostat). Bruk Eurostat eller SSB for norske tidsserier og europeiske land, og OECD for land utenfor Europa. Bruk én kilde per sammenligning, og si hvilken.

## Slik henter du tall fra API-et

OECD har et åpent SDMX-API uten innlogging. Mal:

```
https://sdmx.oecd.org/public/rest/data/<byrå>,<tabell>/<nøkkel>?startPeriod=2015&format=csvfilewithlabels
```

`<byrå>,<tabell>` er for eksempel `OECD.ELS.JAI,DSD_LMP@DF_LMP` (se kolonnen «Kilde» øverst i filene). Nøkkelen har én plass per dimensjon, skilt med punktum, og flere koder med `+`. Tom plass betyr alle. Rekkefølgen på dimensjonene står i datastrukturen: `https://sdmx.oecd.org/public/rest/dataflow/<byrå>/<tabell>/latest?references=datastructure`. Liste over alle tabeller: `https://sdmx.oecd.org/public/rest/dataflow/all?detail=allstubs`. Landkoder er ISO3: `NOR`, `SWE`, `DNK`, `FIN`, `DEU`, `USA`, og `OECD` for snittet.

**Tilgang:** API-et svarte fra GitHub Actions 2026-10-18, men er blokkert fra Claudes kodeverktøy i skymiljøet. OECD begrenser antall kall per minutt (HTTP 429). Kan du ikke nå API-et, si det og svar ikke fra hukommelsen. Oppgi alltid OECD-tabellen.

## Andre OECD-tabeller som er relevante, men ikke i pakken

Disse står i OECDs katalog og kan legges til i `data/oecd/pakke.json`:

- `OECD.ELS.SAE,DSD_DUR@DF_DUR_I`: varighet av arbeidsledighet.
- `OECD.ELS.SAE,DSD_INVPT_EMP@DF_INVPT_I`: ufrivillig deltid.
- `OECD.ELS.SAE,DSD_TEMP@DF_TEMP_I`: midlertidige ansettelser.
- `OECD.ELS.SAE,DSD_EARNINGS@MIN2AVE`: minstelønn i forhold til gjennomsnittslønn (ikke Norge, som ikke har lovfestet minstelønn).
- `OECD.ELS.JAI,DSD_TAXBEN_PTR@DF_PTRUB`: effektiv skatt ved overgang fra ytelse til arbeid.
- `OECD.ELS.JAI,DSD_TAXBEN_NCC@DF_NCC`: netto barnehagekostnad.
- `OECD.ELS.IMD,DSD_MIG@DF_MIG`: innvandring og bestand av utenlandsfødte.
- `OECD.ELS.SPD,DSD_PAG@DF_DPS`: oppbygningen av pensjonssystemene.
