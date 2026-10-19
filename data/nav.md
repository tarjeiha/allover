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
| `aap-*-desember/` | AAP-mottakere etter alder/kjønn og diagnose, desember hvert år | desember 2010–2025 |
| `uforetrygd-*/` | Mottakere av uføretrygd: fylke, kommune, alder, kjønn, uføregrad, innvandrerstatus, barnetillegg, nye mottakere og avgang, diagnoser | Måned (til aug. 2026), kvartal (til juni 2026) og år (til 2025) |
| `uforetrygd-desember-*/`, `uforetrygd-kvartal-*/` | Navs webtabeller for uføretrygd: antall og andel etter kjønn, alder, fylke, uføregrad, utbetalingsgrad, ytelse (kroner), innvandrerstatus, ung ufør, nye mottakere og avgang. Én fil per webtabell, kolonnen `gruppe` er overskriften over hver deltabell (for eksempel «Kvinner.») | 31. desember 2016–2025 og 30. juni 2017–2026 |
| `nedsatt-arbeidsevne-*/` | Personer med nedsatt arbeidsevne etter alder, kjønn, fylke, kommune og innvandrerbakgrunn | Måned (jan.–aug. 2026) og 2. kvartal 2026 |
| `alderspensjon-*/` | Alderspensjonister etter kjønn, alder, fylke, kommune, bosted, innvandrer, delytelse, gradert uttak, minstepensjon, inntekts- og garantipensjon, nye alderspensjonister, avgangsalder og utbetaling | Tidsserier og måneder til 2. kv. 2026; utbetaling og avgangsalder til 2025 |
| `helt-ledige-*/`, `hovedtall-arbeidsmarkedet*/` | Helt ledige etter kjønn, alder, fylke, kommune, utdanning, yrke, varighet og innvandrerbakgrunn; hovedtall (permitterte, delvis ledige, sesongjustert, tilgang av arbeidssøkere); fylkesserier tilbake til 1951 (`helt-ledige-fylke-mnd-*`) | Måned (til sep. 2026), år og historiske serier |
| `ledige-stillinger-*/` | Tilgang av ledige stillinger etter kilde, fylke og yrke | Måned (til sep. 2026) og år |
| `tiltaksdeltakere-*/`, `tiltak-nedsatt-arbeidsevne-*/` | Tiltaksdeltakere etter tiltakstype, demografi og fylke, og personer med nedsatt arbeidsevne på tiltak | Måned (til sep. 2026) og år (til 2025) |
| `arbeidsindikator-*/` | Navs arbeidsindikator: resultater og tidsserier for landet, fylker, tiltak og avtaler | Mars 2026 |
| `afp-privat-*/` | AFP i privat sektor: mottakere etter kjønn og fylke, nye mottakere og gjennomsnittlig årlig pensjon. Gjelder ikke AFP i offentlig sektor | Tidsserier til 2. kv. 2026 og år til 2025 |
| `gjenlevende-*/`, `barnepensjon-*/`, `omstillingsstonad/` | Ytelser til gjenlevende: antall og andel med redusert ytelse, utbetalt pensjon, barnepensjonister og omstillingsstønad | Tidsserier til 2. kv. 2026 og år til 2025 |
| `krigspensjon/`, `supplerende-stonad-alderspensjon/` | Mottakere av krigspensjon og av supplerende stønad til alderspensjonister | Tidsserier til 2. kv. 2026 |
| `kontantstotte-fylke-kommune/` | Barn med kontantstøtte etter fylke og kommune | September 2026 |
| `utbetalinger-*/` | Utbetalinger fra Nav i Norge (per fylke, kommune, kjønn, alder, innvandrer) og til utlandet, med tidsserier 2013–2025 | 2025 |
| `utenforskap-*/`, `trygdesvindel/`, `stonadsmottakere-2007-2016/` | Utenforskap fra arbeidslivet (20–29 og 20–66 år), trygdesvindel og personer med stønad 2007–2016 | 2025 (stønadsmottakere til 2016) |

**Kvartal i sykefraværstabellene:** Nav leverer én fil per kvartal, men i basen er de slått sammen til én TSV per tabell og ark. Kolonnen `kvartal` sier hvilket kvartal raden gjelder, og årskolonnene viser utviklingen for samme kvartal fra år til år. Kvartaler som ikke er publisert for et år (f.eks. 3. og 4. kvartal 2026) har tom celle. Linjen `# Kvartaler:` øverst viser hvilke kvartaler som er lagt inn. Originalfilene ligger i `original/`.

## Slik brukes dem

Kildeprofiler for sykefravær, dagpenger og helt ledige, AAP og uføretrygd (hvilken tabell som svarer på hva, og forbehold) står i `data/nav-profiler.md`. Når Nav sist oppdaterte hver kildeside står i `data/nav/sider.json`.

- Sykefravær er **legemeldt** fravær og ikke sesongjustert. Sammenlign samme kvartal på tvers av år. SSBs sykefraværstall (se `data/ssb.md`) inkluderer egenmeldt fravær og kan avvike. Si hvilken kilde tallet kommer fra.
- Brudd i sykefraværsserien: 2009 ny næringsgruppering (SN2007), 2015 innføring av A-ordningen. Fra 1. kvartal 2022 nytt mottak for sykmeldinger. Fra 1. kvartal 2026 ny gruppeinndeling av diagnoser, og kreft er egen hovedgruppe.
- Dagpenger: det er brudd i statistikken over arbeidsledige fra november 2018 (ny registreringsmetode), se `om.md`.
- Nav gir ikke ut diagnosedata per virksomhet.

## Navs pressemeldinger om statistikk

Navs egne pressemeldinger om statistikken (AAP, uføretrygd, arbeidsledighet, sykefravær, pensjon, familie og andre områder) ligger som tekst i `data/nav/tekster/<område>/<dato>-<navn>.md`, fra januar 2024. `data/nav/tekster/indeks.tsv` lister dem med dato, område, tittel og adresse, nyeste først. Jobben «Hent Nav-pressemeldinger» sjekker nav.no hver hverdag etter kl. 08 og legger inn nye. Tekstene slettes ikke, også når Nav tar dem ned.

- Teksten er Navs egen. Tallene i filen er kontrollert mot Navs side. Figurer er lenket, ikke lagret.
- Nav tar ned pressemeldinger etter omtrent ett år. Eldre tekster er hentet fra Internet Archives kopi av Navs side, og filen sier det. Oppgi da Nav som kilde og nevn at siden ikke lenger ligger ute.
- Bruk pressemeldingen til å si hva Nav selv peker på og forklarer. Tallene hentes fra tabellene over. Pressemeldingen og tabellene kan ha ulik periode.
- En pressemelding er Navs framstilling, ikke departementets vurdering.

## Nav-statistikk som ikke er lagt inn

Se `data/nav-oversikt.md` for oversikt over filer og sider. Gjelder bl.a. barnetrygd, barnebidrag, enslig mor eller far, pleiepenger, foreldrepenger, AFP i offentlig sektor, sosialhjelp, grunnstønad og hjelpestønad. Nav publiserer ikke disse som xlsx (kun nettabeller, pdf eller bilder), og dagpenger etter alder/fylke for tidligere måneder. For slike spørsmål: vis til Navs statistikkside, og ikke svar fra hukommelsen.
