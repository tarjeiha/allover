# Spørsmålskatalog: fra hverdagsspørsmål til tabell

Brukere stiller spørsmål uten fagord. Tabellen under kobler vanlige spørsmål til kilden som svarer på dem. Bruk den til å velge tabell, og følg svarreglene i `data/VEIVISER.md` («Slik svarer du»). Stier til Nav-tabeller er relative til `data/nav/`, til Eurostat-tabeller til `data/eurostat/` og til OECD-tabeller til `data/oecd/`. Profiler med forbehold per område står i `data/nav-profiler.md`.

Katalogen er et førsteutkast bygget ut fra tabellene som finnes i basen, ikke ut fra hvilke spørsmål brukerne faktisk stiller. Legg til spørsmål som dukker opp, og stryk de som ikke brukes.

Hvem som eier kvaliteten: Nav, SSB, Eurostat og OECD eier tallene. Svaret skal alltid si hvem tallet kommer fra.

## Arbeidsmarked og ledighet

| Spørsmål | Kilde og tabell | Merknad |
|---|---|---|
| Hvor mange er arbeidsledige nå? | Nav `hovedtall-arbeidsmarkedet/1-hovedgrupper-kjonn.tsv` (registrerte helt ledige) og SSB 13760 (AKU) | To ulike tall. Si hvilket du bruker, og vis eller tilby det andre. |
| Hva er ledigheten blant kvinner/menn/unge/innvandrere? | Nav `helt-ledige-kjonn-alder-maaned/`, `helt-ledige-innvandrerbakgrunn-maaned/`. SSB 13760 og 14714 | |
| Hvor mange er ledige i min kommune/mitt fylke? | Nav `helt-ledige-fylke-kommune-maaned/` | Nav-tall. |
| Hvor mange får dagpenger? | Nav `dagpenger-kjonn-alder-maaned/alder.tsv` (rad `I alt`) | Dagpengemottakere er en del av helt ledige. |
| Hvor mange er permittert? | Nav `hovedtall-arbeidsmarkedet-permitterte/` | |
| Hvor mange ledige stillinger finnes? | Nav `ledige-stillinger-tilgang-*` | Tilgang av stillinger Nav kjenner til, ikke alle ledige stillinger i økonomien. |
| Hvor mange er på tiltak fra Nav? | Nav `tiltaksdeltakere-hovedgruppe-maaned/` | |
| Hvor mange går mellom jobb og ledighet? | SSB 11433 | |

## Helse og trygd

| Spørsmål | Kilde og tabell | Merknad |
|---|---|---|
| Hva er sykefraværet? | Nav `sykefravar-tidsserie-kvartal/sykefravaersprosent.tsv` (legemeldt). SSB 12439 inkluderer egenmeldt | Sammenlign samme kvartal på tvers av år. |
| Sykefravær i en næring/sektor/yrke/aldersgruppe/diagnose? | Nav `sykefravar-naering/`, `-sektor/`, `-yrke/`, `-alder/`, `-diagnose-hovedgrupper/` | Alle kvartaler i samme fil, kolonnen `kvartal`. |
| Hvor mange er sykmeldte? | Nav `sykefravar-tidsserie-kvartal/antall-sykmeldte.tsv` | Unike personer i kvartalet. |
| Hvor mange er på AAP? | Nav `aap-alder-kjonn-desember/1a-alder-i-alt-antall.tsv` (desember, 2010–2025), `aap-alder-kjonn-kvartal/` (siste kvartal), `aap-alder-kjonn-maaned/` (siste måneder) | Si hvilken måned tallet gjelder. |
| Hvor mange kommer inn på eller går ut av AAP? | Nav `aap-tilgang-alder-kjonn-kvartal/`, `aap-avgang-alder-kjonn-kvartal/` (også etter fylke) | Samme kvartal hvert år fra 2010. Avgang ligger ett kvartal etter tilgang. |
| Hvor mange unge er på AAP? | Nav `aap-unge-alder-fylke-kvartal/` | Antall og andel av befolkningen. |
| Hvor mange er uføre? | Nav `uforetrygd-uforegrad-kjonn-maaned/antall.tsv` (siste måneder) | |
| Hvordan har antall uføre utviklet seg? | Nav `uforetrygd-desember-kjonn-alder-antall/` (31.12 2016–2025), før 2016 `stonadsmottakere-2007-2016/` | Andel av befolkningen: `uforetrygd-desember-andel-kjonn-alder-prosent/`, aldersstandardisert per fylke: `uforetrygd-desember-andel-fylke-kjonn-aldersstandardisert-prosent/`. |
| Hvor stor andel er uføre i mitt fylke? | Nav `uforetrygd-andel-fylke-alder-kvartal/fylke-og-alder.tsv` | Andel av befolkningen 18–67 år. |
| Hvor mange blir nye uføretrygdede? | Nav `uforetrygd-desember-nye-kjonn-alder-antall/` (per år 2016–2025), `uforetrygd-desember-avgang-kjonn-alder-antall/` (avgang), `uforetrygd-nye-*-maaned/` (inneværende år) | |
| Hvor mange får alderspensjon? | Nav `alderspensjon-kjonn-alder-fylke/1-alder.tsv` (rad `I alt`, juni hvert år fra 2016) | Stand i juni. |
| Hvor mange nye alderspensjonister kommer det? | Nav `alderspensjon-nye-kjonn-alder/` | Kvartalstall. |
| Hvor mange tar ut gradert alderspensjon? | Nav `alderspensjon-gradert-tidsserie/1-antall-grad.tsv` | |
| Hvor mange har minstepensjon? | Nav `alderspensjon-minste-tidsserie/1-antall.tsv` (antall og andel) | |
| Hvor mye får en alderspensjonist i gjennomsnitt? | Nav `alderspensjon-utbetalt-aar/` (årlig beløp) | Sjekk ark og gruppering i filen før du oppgir et gjennomsnitt. |
| Når slutter folk å jobbe? | Nav `alderspensjon-avgangsalder/1-avgangsalder-kjonn.tsv` | Gjennomsnittlig avgangsalder fra arbeidslivet. |
| Hvor mange uføre har barnetillegg? | Nav `uforetrygd-barnetillegg-fylke-kvartal/ark1.tsv` | |
| Hva er sykefraværet i mitt fylke? | Nav `sykefravar-bosted/sykefravaersprosent.tsv` (fylke, etter bosted, ikke arbeidssted). Kommune: SSB 12451 | |
| Hvor mange er på AFP i privat sektor? | Nav `afp-privat-mottakere/` | Gjelder ikke AFP i offentlig sektor. |
| Hvor mange får sosialhjelp? | SSB 08900 | Nav har ikke sosialhjelp som tabell. |

## Familie, ytelser og penger

| Spørsmål | Kilde og tabell | Merknad |
|---|---|---|
| Hvor mange får kontantstøtte? | Nav `kontantstotte-fylke-kommune/` | |
| Hvor mye betaler Nav ut? | Nav `utbetalinger-*` | |
| Hva er barnetrygd, foreldrepenger, grunnstønad, hjelpestønad? | Ikke dekket som tall | Nav publiserer ikke disse som xlsx. Vis til Navs statistikkside. Satser kan stå i budsjettvedtaket (`budsjett/VEIVISER.md`). |
| Hva er grunnbeløpet? | `regelverk/folketrygdloven/` og budsjettvedtaket | |

## Lønn, priser og befolkning

| Spørsmål | Kilde og tabell | Merknad |
|---|---|---|
| Hva tjener folk? | SSB 09174, 09175, 11652 | |
| Hvor høy er prisveksten? | SSB 14700 (KPI) | Basisår 2025=100. |
| Hvor mange bor i Norge/kommunen? | SSB 05803, 10211, 05810 | |
| Hvor mange innvandrere? | SSB 05184 | |

## Sammenligning med andre land

| Spørsmål | Kilde og tabell | Merknad |
|---|---|---|
| Hvordan ligger Norge an på ledighet? | Eurostat `une_rt_a.tsv` | ILO-definisjon (AKU). Ikke Navs registrerte ledige. |
| Hvordan er sysselsettingen sammenlignet med Norden og EU? | Eurostat `lfsi_emp_a.tsv` | |
| Hvordan er sysselsettingen blant innvandrere? | Eurostat `lfsa_ergan.tsv` (kolonnen `citizen`) | Norge. Statsborgerskap, ikke landbakgrunn. |
| Hvor mange er i risiko for fattigdom? | Eurostat `ilc_peps01n.tsv` | |
| Hvordan ligger Norge an på langtidsledighet? | Eurostat `une_ltu_a.tsv` | Oppgi `PC_UNE` eller `PC_ACT`. AKU-basert. |
| Hvor mange unge er verken i jobb eller utdanning, sammenlignet med andre land? | Eurostat `edat_lfse_20.tsv` | NEET etter Eurostats definisjon. |
| Hvordan er sysselsettingen blant eldre (55–64) sammenlignet med andre land? | Eurostat `lfsi_emp_a.tsv` (`age=Y55-64`) | |
| Hva bruker landet på sosial beskyttelse (alderdom, uførhet, familie, arbeidsledighet)? | Eurostat `gov_10a_exp.tsv` | Prosent av BNP. 2025 mangler for flere land. |
| Hvor stor andel av voksne deltar i utdanning og opplæring? | Eurostat `trng_lfse_01.tsv` | Siste fire uker, 25–64 og 55–64 år. |
| Hvor mye bruker Norge på arbeidsmarkedstiltak sammenlignet med andre land? | OECD `arbeidsmarkedstiltak.tsv` (`LMP_10T70` aktive, `LMP_80_90` passive) | Prosent av BNP. |
| Hvor mye av inntekten beholder man som arbeidsledig? | OECD `kompensasjonsgrad-ledighet.tsv` | Modellhusholdninger. Si hvilken husholdning og varighet. |
| Hvor høy er sosialhjelpen sammenlignet med andre land? | OECD `minsteinntektsytelser.tsv` | Modellhusholdninger, prosent av medianinntekten. |
| Er aktivitetskravene strengere i Norge enn i andre land? | OECD `aktivitetskrav.tsv` | Skala 1–5. |
| Hvor sterkt er stillingsvernet i Norge? | OECD `stillingsvern.tsv` | Sammenlign bare innen samme versjon. |
| Hvor høy pensjon får man i forhold til lønnen, sammenlignet med andre land? | OECD `pensjoner.tsv` (`NPRR100`, `NPRR50`) | Fremskrevet for en som begynner å jobbe i dag. |
| Hva bruker landet på uføre, sykdom, familie og alderdom? | OECD `sosiale-utgifter.tsv`, Eurostat `gov_10a_exp.tsv` | OECD har flere ytelsestyper, men siste år er 2021. Eurostat er nyere. |
| Hvor mange er fagorganisert eller dekket av tariffavtale? | OECD `organisasjonsgrad.tsv`, `tariffavtaledekning.tsv` | |
| Hvordan er lønnsnivået og lønnsgapet mellom kvinner og menn sammenlignet med andre land? | OECD `gjennomsnittslonn.tsv` (`USD_PPP`), `lonnsgap-kjonn.tsv` (`MEDIAN`) | |
| Har Norge høyt sykefravær sammenlignet med andre land? | OECD `sykefravar.tsv` | Uker per heltidsansatt. Ikke samme mål som Navs sykefraværsprosent. |
| Hvordan går det med innvandrere i arbeidsmarkedet sammenlignet med andre land? | OECD `innvandrere-arbeidsmarked.tsv` | Fødeland (`FB`/`NB`), ikke statsborgerskap som i Eurostat. |
| Hvor stor er inntektsforskjellen (Gini) og fattigdommen sammenlignet med andre land? | OECD `inntektsfordeling.tsv` | 50 og 60 prosent av median. Eurostat `ilc_peps01n.tsv` bruker et annet mål. |
| Hvor mye skatt betaler en vanlig lønnstaker sammenlignet med andre land? | OECD `skattekile.tsv` | Modellhusholdninger. |
| Hvordan ligger Norge an mot USA og Storbritannia på sysselsetting og arbeidstid? | OECD `sysselsetting-alder.tsv`, `arbeidstimer.tsv` | Arbeidstimer: sammenlign utvikling, ikke nivå. |

## Eksempler på korte svar

Eksemplene er regnet ut fra tallene i basen 2026-10-17. Hvert svar avslutter med linjen om kvalitetssikringsversjon (utelatt her).

**«Hva er sykefraværet?»** Legemeldt sykefravær var 5,7 prosent i 2. kvartal 2026, mot 5,6 prosent i 2. kvartal 2025 (Nav, sykefraværsstatistikken, publisert 04.09.2026).

**«Hvor mange er arbeidsledige?»** Nav hadde 59 413 registrerte som helt ledige i september 2026, 2,0 prosent av arbeidsstyrken og 2 542 færre enn i september 2025 (Nav, hovedtall om arbeidsmarkedet). Vil du ha tall for arbeidsledige etter SSBs arbeidskraftsundersøkelse (AKU) i tillegg? De måles på en annen måte.

**«Hvor mange er på AAP?»** 168 628 mottok arbeidsavklaringspenger i juni 2026, 3 067 flere enn i juni 2025 (Nav, AAP etter alder og kjønn).

**«Er ledigheten i Norge høy sammenlignet med andre land?»** Arbeidsledigheten blant 15–74-åringer var 4,5 prosent i Norge i 2025, mot 8,8 i Sverige, 6,4 i Danmark, 9,7 i Finland, 3,8 i Tyskland og 6,0 i EU (Eurostat, `une_rt_a`, ILO-definisjon). Sysselsettingsraten for 20–64-åringer var 79,5 prosent i Norge, 81,8 i Sverige, 79,8 i Danmark og 76,1 i EU (Eurostat, `lfsi_emp_a`).

**«Hvor mange får barnetrygd?»** Ikke dekket. Nav publiserer ikke barnetrygd som tabell i basen. Se Navs statistikkside for barnetrygd.
