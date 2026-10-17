# Nav-statistikk i basen

Nav publiserer tall som xlsx-filer på nav.no. Claude når ikke filene herfra, så filene er lagt inn som TSV under `data/nav/<tabell>/`. Hver mappe har `om.md` (definisjoner fra Navs ark «Om statistikken») og én TSV per ark. Øverst i hver TSV står kilde, kildeside, oppdateringsdato og neste publisering som `#`-linjer. Tall står som i xlsx-filen. `****` og `*` betyr at tallet ikke er publisert eller er skjult av Nav.

Originalfilen ligger i `original/` i hver mappe, og `data/nav/indeks.tsv` lister alle tabellene med kildeside og dato. Filene er en kopi per angitt dato. Sjekk kildesiden hvis det kan ha kommet nyere tall. Jobben «Nav-henting» sjekker nav.no hver mandag og legger inn nye filer selv. Filer kan også legges i `innboks-data/` (se `innboks-data/README.md`) og konverteres automatisk med `verktoy/nav_xlsx.py`. Kjente tabeller står i `data/nav/kilder.json`.

## Tabeller i basen

Full liste med mappe, tabell, filer, kildeside og dato står i `data/nav/indeks.tsv`. Mappene er gruppert slik:

| Mappe | Innhold | Periode |
|---|---|---|
| `sykefravar-tidsserie-kvartal/` | Legemeldt sykefravær per kvartal: prosent, tapte dagsverk, tilfeller, sykmeldte | 1. kv. 2002 – 2. kv. 2026 |
| `sykefravar-<tema>/` | Sykefravær etter bosted, næring, sektor, yrke, alder, diagnose (hovedgrupper, undergrupper, enkeltdiagnoser), gradert fravær, varighet (fylke/diagnose og varighetsgrupper), innvandrerstatus og fødeland. **Alle kvartaler ligger i samme fil**, med kolonnen `kvartal` (`K1`–`K4`) først på hver rad. | 2010–2026 for hvert kvartal som er lagt inn |
| `dagpenger-*-maaned/`, `tilleggsstonader-arbeidssokere-maaned/` | Dagpengemottakere (hovedtall, kjønn/alder, fylke/kommune, yrke, varighet, godkjent utdanning), søknader om dagpenger, tilleggsstønader | Måned, til og med september 2026 |
| `aap-*-maaned/` | AAP-mottakere etter alder/kjønn, fylke, kommune, diagnose, innvandrerbakgrunn | jan.–aug. 2026 |
| `aap-*-kvartal/` | AAP-mottakere etter alder/kjønn og diagnose | juni 2010–2026 |
| `uforetrygd-*/` | Mottakere av uføretrygd: fylke, kommune, alder, kjønn, uføregrad, innvandrerstatus, barnetillegg, nye mottakere og avgang, diagnoser | Måned (til aug. 2026), kvartal (til juni 2026) og år (til 2025) |
| `nedsatt-arbeidsevne-*/` | Personer med nedsatt arbeidsevne etter alder, kjønn, fylke, kommune og innvandrerbakgrunn | Måned (jan.–aug. 2026) og 2. kvartal 2026 |
| `alderspensjon-*/` | Alderspensjonister etter kjønn, alder, fylke, kommune, bosted, innvandrer, delytelse, gradert uttak, minstepensjon, inntekts- og garantipensjon, nye alderspensjonister, avgangsalder og utbetaling | Tidsserier og måneder til 2. kv. 2026; utbetaling og avgangsalder til 2025 |

**Kvartal i sykefraværstabellene:** Nav leverer én fil per kvartal, men i basen er de slått sammen til én TSV per tabell og ark. Kolonnen `kvartal` sier hvilket kvartal raden gjelder, og årskolonnene viser utviklingen for samme kvartal fra år til år. Kvartaler som ikke er publisert for et år (f.eks. 3. og 4. kvartal 2026) har tom celle. Linjen `# Kvartaler:` øverst viser hvilke kvartaler som er lagt inn. Originalfilene ligger i `original/`.

## Slik brukes dem

- Sykefravær er **legemeldt** fravær og ikke sesongjustert. Sammenlign samme kvartal på tvers av år. SSBs sykefraværstall (se `data/ssb.md`) inkluderer egenmeldt fravær og kan avvike. Si hvilken kilde tallet kommer fra.
- Brudd i sykefraværsserien: 2009 ny næringsgruppering (SN2007), 2015 innføring av A-ordningen. Fra 1. kvartal 2022 nytt mottak for sykmeldinger. Fra 1. kvartal 2026 ny gruppeinndeling av diagnoser, og kreft er egen hovedgruppe.
- Dagpenger: det er brudd i statistikken over arbeidsledige fra november 2018 (ny registreringsmetode), se `om.md`.
- Nav gir ikke ut diagnosedata per virksomhet.

## Nav-statistikk som ikke er lagt inn

Se `data/nav-oversikt.md` for oversikt over filer og sider. Gjelder bl.a. familieytelser, AFP, sosialhjelp, grunnstønad og hjelpestønad, og dagpenger etter alder/fylke for tidligere måneder. For slike spørsmål: vis til Navs statistikkside, og ikke svar fra hukommelsen.
