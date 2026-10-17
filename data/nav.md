# Nav-statistikk i basen

Nav publiserer tall som xlsx-filer på nav.no. Claude når ikke filene herfra, så utvalgte filer er lagt inn som TSV under `data/nav/<tabell>/`. Hver mappe har `om.md` (definisjoner fra Navs ark «Om statistikken») og én TSV per ark. Øverst i hver TSV står kilde, kildeside, oppdateringsdato og neste publisering som `#`-linjer. Tall står som i xlsx-filen. `****` og `*` betyr at tallet ikke er publisert eller er skjult av Nav.

Originalfilen ligger i `original/` i hver mappe, og `data/nav/indeks.tsv` lister alle tabellene med kildeside og dato. Filene er en kopi per angitt dato. Sjekk kildesiden hvis det kan ha kommet nyere tall. Nye filer legges i `innboks-data/` (se `innboks-data/README.md`) og konverteres automatisk med `verktoy/nav_xlsx.py`. Kjente tabeller står i `data/nav/kilder.json`.

## Tabeller i basen

| Mappe | Innhold | Periode | Oppdatert | Kildeside |
|---|---|---|---|---|
| `data/nav/sykefravar-tidsserie-kvartal/` | Legemeldt sykefravær per kvartal: sykefraværsprosent, tapte dagsverk, tilfeller, sykmeldte. Alle, kvinner og menn | 1. kv. 2002 – 2. kv. 2026 | 04.09.2026 (neste 26.11.2026) | nav.no/no/nav-og-samfunn/statistikk/sykefravar-statistikk/sykefravar |
| `data/nav/sykefravar-naering/` | Sykefraværsprosent og tapte dagsverk etter næring (SN2007, to siffer) | **Bare 2. kvartal** hvert år 2010–2026 | 04.09.2026 | samme |
| `data/nav/sykefravar-alder/` | Sykefraværsprosent og tapte dagsverk etter alder | **Bare 2. kvartal** hvert år 2010–2026 | 04.09.2026 | samme |
| `data/nav/sykefravar-diagnose-hovedgrupper/` | Tapte dagsverk, andel, per 10 000, tilfeller og sykmeldte etter diagnosehovedgruppe, alle/kvinner/menn | **Bare 2. kvartal** hvert år 2010–2026 | 04.09.2026 | samme |
| `data/nav/dagpenger-tiltakspenger-maaned/` | Mottakere av dagpenger og tiltakspenger per måned, også etter arbeidsmarkedsstatus | jan. 2021 – aug. 2026 | 03.09.2026 | nav.no/no/nav-og-samfunn/statistikk/arbeidssokere-og-stillinger-statistikk/stonader-til-arbeidssokere |
| `data/nav/aap-alder-kjonn-kvartal/` | Mottakere av arbeidsavklaringspenger etter alder og kjønn, antall og andel av befolkningen | juni hvert år 2010–2026 | 15.09.2026 (side) | nav.no/no/nav-og-samfunn/statistikk/aap-nedsatt-arbeidsevne-og-uforetrygd-statistikk/arbeidsavklaringspenger |

## Slik brukes dem

- Sykefravær er **legemeldt** fravær og ikke sesongjustert. Sammenlign samme kvartal på tvers av år. SSBs sykefraværstall (se `data/ssb.md`) inkluderer egenmeldt fravær og kan avvike. Si hvilken kilde tallet kommer fra.
- Brudd i sykefraværsserien: 2009 ny næringsgruppering (SN2007), 2015 innføring av A-ordningen. Fra 1. kvartal 2022 nytt mottak for sykmeldinger. Fra 1. kvartal 2026 ny gruppeinndeling av diagnoser, og kreft er egen hovedgruppe.
- Dagpenger: det er brudd i statistikken over arbeidsledige fra november 2018 (ny registreringsmetode), se `om.md`.
- Nav gir ikke ut diagnosedata per virksomhet.

## Nav-statistikk som finnes, men ikke er lagt inn

Se `data/nav-oversikt.md` for oversikt over filer og sider. Gjelder bl.a. sykefravær etter bosted, sektor, yrke og enkeltdiagnoser, dagpenger etter alder, fylke, yrke og varighet, AAP etter fylke, kommune og diagnose, uføretrygd, familieytelser, pensjon, sosialhjelp, grunnstønad og hjelpestønad. For slike spørsmål: vis til Navs statistikkside, og ikke svar fra hukommelsen.
