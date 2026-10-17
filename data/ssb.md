# SSB – hvilken tabell svarer på hva

Tabellene er kontrollert mot SSB 2026-10-17 (id, tittel, periode og oppdateringsdato er lest fra SSBs API). Hent data med SSB-tilkoblingen: søk med `ssb_search`, les variablene med `ssb_table_metadata`, hent med `ssb_get_data`, og filtrer alltid på tid.

## Søketips (kontrollert)

- Korte søkeord virker bra: `sysselsatte`, `title:Konsumprisindeks`, `title:Innvandrere`. Lange setninger og lange `title:`-uttrykk ga ingen treff.
- Hvert søk gir mange tabeller med overlappende innhold. Velg etter periode, hyppighet og oppdeling, ikke bare etter tittelen.
- «(K)» i tittelen betyr kommunefordelt, «(F)» fylkesfordelt.

## Arbeidsmarked

| Spørsmål | Tabell | Periode | Merknad |
|---|---|---|---|
| Arbeidsstyrke, sysselsatte og arbeidsledige, månedlig, 15–74 år | **13760** | 2006M01–2026M08 | Oppdelt på kjønn og tre aldersgrupper. Brudd- og sesongjusterte tall. |
| Samme, kvartalsvis | 14483 | 2009K1–2026K2 | Etter arbeidsstyrkestatus, kjønn og alder. |
| Hvor mange går mellom sysselsatt, arbeidsledig og utenfor | 11433 | 2006K2–2026K2 | Sesongjusterte strømmer. |
| Innvandreres arbeidsstyrkestatus | 14714 | 2021K1–2026K2 | Etter landbakgrunn, kjønn og alder. |

**Slik leser du 13760.** Statistikkvariabelen `ArbledProsArbstyrk` gir arbeidsledige i prosent av arbeidsstyrken. Velg `Justering`: `S` er sesongjustert, `T` trend, `IS` ikke sesongjustert, `3MGG` sesongjustert tremåneders glidende gjennomsnitt. **Siste måned mangler for 3MGG.** Eksempel hentet 2026-10-17: sesongjustert ledighet for begge kjønn, 15–74 år, 2026M08 var 4,5 prosent, mens 3MGG for samme måned var tom.

## Lønn

| Spørsmål | Tabell | Periode |
|---|---|---|
| Lønn og sysselsetting etter næring, årlig, lang serie | 09174 | 1970–2025 |
| Lønn og sysselsetting etter næring, kvartalsvis | 09175 | 1995K1–2026K2 |
| Lønnstakere, jobber og lønn etter næring (88 grupper) | 12314 | 2016K1–2026K2 |
| Etter kjønn og alder, arbeidssted | 11652 | 2016K1–2026K2 |
| Etter innvandringskategori | 12315 | 2016K1–2026K2 |

## Sykefravær

Kvartalstall for lønnstakere. Tittelen sier om tabellen viser «egen- og/eller legemeldt» eller bare «legemeldt». De er ikke samme tall.

| Spørsmål | Tabell | Omfang |
|---|---|---|
| Etter type sykefravær og kjønn, sesong- og influensajustert | 12439 | 2000K2–2026K2 |
| Etter næring (17 grupper) og kjønn | 12440 | 2000K2–2026K2 |
| Årlig, etter næring og kjønn | 12441 | 2001–2025 |
| Etter varighet | 12946 | 2015K1–2026K2 |
| Legemeldt, etter fylke, næring og kjønn | 12447 | 2008K1–2026K2 |
| Legemeldt, etter bostedskommune | 12451 | 2000K2–2026K2 |
| Legemeldt og lønn, etter utdanning og alder | 13333 | 2015K1–2026K2 |

## Priser

| Spørsmål | Tabell | Merknad |
|---|---|---|
| KPI etter vare- og tjenestegruppe, månedlig | 14700 | 2000M01–2026M09. Basisår 2025=100. |
| KPI sesongjustert og KPI-JAE | 14708 | 1985M01–2026M09 |
| KPI, lang historisk serie | 14710 (månedlig), 14709 (årlig) | Fra 1920. |
| KPI, årlig | 14701 | 2000–2025 |

Basisåret er endret til 2025=100. Eldre tall som er oppgitt med annet basisår, kan ikke sammenlignes uten omregning.

## Innvandring

| Spørsmål | Tabell | Periode |
|---|---|---|
| Innvandrere etter kjønn og landbakgrunn | 05184 | 1970–2026 |
| Innvandrere etter landbakgrunn og botid (fylke) | 10598 | 2005–2026 |
| Utdanningsnivå for innvandrere | 09623 | 2004–2025 |

## Befolkning

| Spørsmål | Tabell | Periode |
|---|---|---|
| Endringer i befolkningen i løpet av året | 05803 | 1735–2026 |
| Alders- og kjønnsfordeling | 10211 (enkeltalder), 05810 (aldersgrupper) | 1845/1846–2026 |
| Etter kommunestørrelse, alder og kjønn | 12871 | 2017–2026 |
| Grunnkrets | 04317 | 1999–2026 |

## Sosialhjelp

| Spørsmål | Tabell | Periode |
|---|---|---|
| Stønadssatser for sosialhjelp og vedtakstidspunkt (kommune) | 12131 | 2015–2025 |
| Stønadstilfeller etter alder (fylke) | 08900 | 2010–2025 |
| Brutto utbetalt sosialhjelp etter stønadens art og kommunestørrelse | 05973 | 1997–2025 |
| Mottakere etter alder og antall kommuner | 05082 | 1997–2025 |

## Trygdeytelser

SSB har få tabeller om mottakere av arbeidsavklaringspenger og uføretrygd, og flere av dem er gamle. Antall mottakere og utbetalinger per ytelse hører til Navs statistikk, som ikke er dekket ennå (se `data/VEIVISER.md`).

| Tabell | Innhold | Periode |
|---|---|---|
| 13080 | Måneder som mottaker av arbeidsavklaringspenger og sysselsatt lønnstaker | 2018–2025 |
| 11867 | Uføretrygdede og lønnstakere, etter måneder som sysselsatt lønnstaker | 2015–2025 |
| 11079, 11108–11113 | Eldre tabeller om AAP og uføre, oppdatert sist i 2016 | 2006–2014 |

## Det vi ikke fant

- Ungdom utenfor opplæring og arbeid: søket ga ingen relevant tabell. Prøv andre søkeord eller spør SSB.
- Hovedtabell for registerbasert sysselsetting: søk på tittelen ga ingen treff. Bruk 13760 for månedlige tall og 14483 for kvartalstall.
