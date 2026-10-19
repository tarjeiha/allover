# Navs statistikk: oversikt til utvelgelse (hentet 2026-10-17)

Kilde: nav.no/no/nav-og-samfunn/statistikk. Sidene er lest, filene ikke åpnet. Alle datafiler er xlsx (noen også pdf). «Filnivå» betyr at jeg har åpnet siden og sett filene. «Sidenivå» betyr at jeg bare har sett at siden finnes.

## Anbefalt første runde
| Nr | Fil | Periode | Hvorfor |
|---|---|---|---|
| 1 | Sykefravær, tidsserie per kvartal (SYFRA 2002) | 2002–2. kv. 2026 | Mest spurt om, og lite i SSB-tabellene på legemeldt fravær |
| 2 | Sykefravær etter næring (SYFRA520) | 2010–2026 | Næringssammenligning |
| 3 | Sykefravær etter alder (SYFRA550) | 2010–2026 | |
| 4 | Sykefravær etter diagnosehovedgrupper (SYFRA2400) | 2010–2026 | |
| 5 | Mottakere av dagpenger og tiltakspenger, tidsserie måned (ARBS050) | til aug. 2026 | Hovedtall dagpenger |
| 6 | AAP-mottakere, alder og kjønn, tidsserie kvartal (AAP320) | juni 2010–2. kv. 2026 | Hovedtall AAP |

## Filnivå

### Sykefravær (oppdatert 04.09.2026, neste 26.11.2026, legemeldt, ikke sesongjustert)
Tidsserie per kvartal (2002–), etter alder (SYFRA550), bosted (510), næring (520), sektor (530), yrke (540, 2014–), diagnosehovedgrupper (2400), diagnoseundergrupper (2402), enkeltdiagnoser (2401, 2015–), gradert fravær etter diagnosegrupper (2501), varighet avsluttede tilfeller etter fylke og diagnose, varighetsgrupper (2002–), innvandrerstatus, fødeland. Alle 2010–2026 om ikke annet er oppgitt.

### Stønader til arbeidssøkere (oppdatert 03.09.2026, statistikk per august 2026)
- Søknader om dagpenger per måned (tidsserie) og per næring (én fil per måned)
- Mottakere av dagpenger og tiltakspenger, tidsserie måned (ARBS050)
- Mottakere av dagpenger etter kjønn og alder (051), fylke og kommune (052), yrke (053), varighet (058), godkjent utdanning (A365)
- Tilleggsstønader for arbeidssøkere (057)
- Årsgjennomsnitt helt ledige 1965–2025 (tabell 13), dagpengemottakere totalt 1971–2025 (tabell 14), xls
- Brukt opp dagpengeperioden 2019–2024: webtabeller, ikke filer

### AAP (side oppdatert 15.09.2026)
- Måned jan–aug 2026: alder og kjønn (AAP120), fylke og alder (150), kommune (155), diagnose og alder (160), diagnose og kjønn (170), diagnose detaljer (180), innvandrerbakgrunn (190)
- Kvartal juni 2010–2. kv. 2026: alder og kjønn (320), diagnose og alder (360), diagnose og kjønn (370)
- Øvrige tabeller (nye mottakere, avgang, varighet) er webtabeller

### Uføretrygd, kvartalsstatistikk (oppdatert 13.08.2026)
Andel av befolkningen etter fylke og alder 2025–2026 (tabell 12), med barnetillegg etter fylke 2024–2026 (tabell 18), kommune 2024–2026 (tabell 20). Resten er webtabeller.

## Sidenivå (ikke åpnet)
- **Arbeidssøkere og stillinger:** hovedtall om arbeidsmarkedet, helt ledige, tiltaksdeltakere, ledige stillinger, arbeidssøkere, permitterte og masseoppsigelser, avgang til arbeid og stønad, avgang fra tiltak, historisk statistikk, fravær fra arbeid, arbeidsindikator (alle per september 2026 der periode er oppgitt)
- **AAP/uføre, øvrige:** nedsatt arbeidsevne, uføretrygd månedsstatistikk (juli 2026), diagnoser uføretrygd (des. 2025), uføretrygd og yrkesskade (des. 2025), statistikknotater
- **Familie (per 30.6.2026):** kontantstøtte, foreldrepenger/engangsstønad/svangerskapspenger, barnebidrag, enslig mor eller far, barnetrygd, pleiepenger sykt barn (2025)
- **Pensjon (per 30.6.2026):** alderspensjon, ytelser til gjenlevende, AFP, krigspensjon, supplerende stønad
- **Flere områder:** sosialhjelp (1. tertial 2026), grunnstønad og hjelpestønad (30.6.2026), utbetalinger i Norge og utlandet (2025), utenforskap fra arbeidslivet (2025), trygdemisbruk (2025), tall for tolk (2025)

## Kildekart: hva som hentes automatisk (oppdatert 2026-10-17)

Nav-henting (`.github/workflows/nav-hent.yml`) går hver mandag, og tirsdag morgen etter at Nav har lagt ut AAP-tallene kl. 08, gjennom kildesidene som står i `data/nav/kilder.json`, laster ned nye xlsx-filer og legger dem inn. Hver tabells kildeside og siste innlegging står i `data/nav/indeks.tsv`. Alt under `https://www.nav.no/no/nav-og-samfunn/statistikk/`:

| Side | Status |
|---|---|
| `sykefravar-statistikk/sykefravar` | Hentes (kvartal) |
| `arbeidssokere-og-stillinger-statistikk/` helt-ledige, hovedtall-om-arbeidsmarkedet, ledige-stillinger, tiltaksdeltakere, arbeidsindikator, historisk-statistikk, stonader-til-arbeidssokere | Hentes |
| `aap-nedsatt-arbeidsevne-og-uforetrygd-statistikk/` arbeidsavklaringspenger, nedsatt-arbeidsevne, uforetrygd (+ diagnoser, månedsstatistikk) | Hentes |
| `pensjon-statistikk/` alderspensjon, avtalefestet-pensjon-afp, krigspensjon, supplerende-stonad, ytelser-til-gjenlevende | Hentes (AFP kun privat sektor) |
| `familie-statistikk/kontantstotte` | Hentes |
| `familie-statistikk/` barnetrygd, barnebidrag, enslig-mor-eller-far, pleiepenger-sykt-barn | Ingen xlsx (nettabeller) |
| `familie-statistikk/` foreldrepenger (+ engangsstønad og svangerskapspenger) | Bare pdf |
| `flere-statistikkomrader/` utbetalinger-til-personer-i-norge-per-fylke-og-kommune, utbetalinger-til-personer-i-utlandet, utenforskap-fra-arbeidslivet, trygdemisbruk, stonadsmottakere | Hentes |
| `flere-statistikkomrader/` sosialhjelp | Bare pdf |
| `flere-statistikkomrader/` grunnstonad, hjelpestonad | Bare bilder (png) |

Nye filer på disse sidene som ikke passer et mønster i `kilder.json`, står i rapporten fra Nav-henting («uten treff i kilder.json»). Nye sider eller nye underområder hos Nav finnes ikke av seg selv: sjekk gruppesidene `arbeidssokere-og-stillinger-statistikk`, `aap-nedsatt-arbeidsevne-og-uforetrygd-statistikk`, `pensjon-statistikk`, `familie-statistikk`, `flere-statistikkomrader` og `sykefravar-statistikk` for nye undersider.
