# Folketrygdloven: veiviser

Folketrygdloven regulerer medlemskap i folketrygden og ytelsene derfra: dagpenger, sykepenger, pleiepenger, arbeidsavklaringspenger, uføretrygd, foreldrepenger, stønad til enslig mor eller far, ytelser ved dødsfall, alderspensjon, grunnstønad, hjelpestønad og hjelpemidler. Den har også felles regler om saksbehandling, utbetaling og tilbakekreving. Over 50 forskrifter utfyller loven, blant annet dagpengeforskriften, uføretrygdforskriften, forskrift om alderspensjon og den årlige forskriften om grunnbeløp og satser.

Ansvaret for loven er delt mellom flere departementer. Kapittel 5 (stønad ved helsetjenester) hører til Helse- og omsorgsdepartementet, kapittel 14 (foreldrepenger og engangsstønad) til Barne- og familiedepartementet, og kapittel 23 og 24 (finansiering og avgifter) til Finansdepartementet. Resten av loven forvaltes av Arbeids- og inkluderingsdepartementet, blant annet kapittel 15 (stønad til enslig mor eller far). «Forvaltes av» i kildelisten under gjelder hele loven og sier ikke hvem som har ansvaret for det enkelte kapitlet.

Noen forskrifter under loven forvaltes av andre departementer enn loven: A-trygdforskriften (Nærings- og fiskeridepartementet), tre forskrifter om nedsettelse av pensjonsgivende inntekt mv. (Finansdepartementet), forskriften om disponering av kontantytelser under institusjonsopphold (Helse- og omsorgsdepartementet) og forskriften om utvidet stønad til helsetjenester under opphold i utlandet (sammen med Helse- og omsorgsdepartementet). Se kildelisten under.

Merknadene i basen dekker ikke kapittel 5, 14, 23 og 24, men NAVs rundskriv til dem ligger i basen (se under).

## Slik bruker du veiviseren

Finn paragrafen i listen under «Innhold», og åpne filen før du svarer. Merknadene under er hjelp til å unngå vanlige feil. De er ikke en offisiell tolkning.

Merknadsfilene er flyttet fra de gamle ftrl-skillene og er delt etter ytelse. Bruk tabellen nederst til å finne riktig fil.

NAVs rundskriv ligger i `rundskriv/` og dekker nesten hele loven. Rundskriv er forvaltningspraksis, ikke lov. Skill i svaret mellom det som står i loven eller forskriften og det NAV legger til grunn i rundskrivet. Rundskrivene kan være eldre enn lovteksten, så sjekk datoen i rundskrivfilen, og vær forsiktig med satser og beløp. Er en paragraf opphevet eller endret etter rundskrivets dato, gjelder lovteksten. Rundskrivene hentes hver uke fra Nav rettskilder hos Lovdata, så de følger Navs siste versjon. Datoen rundskrivet sist ble endret hos Nav, står i oversikten øverst i hver rundskrivfil. De ligger i to mappestrukturer:

- `rundskriv/rundskriv-<kode>/` for rundskriv til loven, med Navs dokumentnummer i mappenavnet: `rundskriv-r08-00/` for kapittel 8, `rundskriv-r05-07/` for § 5-7, `rundskriv-r10-07b/` for § 10-7 bokstav b. Hver mappe har `oversikt.md`, `innledning.md` og `par-X-Y.md` per paragraf. Kapittel 3 har tilleggsdeler `rundskriv-r03-01` til `r03-04`, og kapittel 5 har ett rundskriv per paragraf. Kapittel 5, 23 og 24 hører til andre departementer (se over), men rundskrivene ligger i basen. Navs kommentarer til forskrifter som ikke er i basen, ligger også her (for eksempel `rundskriv-r11a-00-for/` til tilleggsstønadsforskriften).
- `rundskriv/forskrifter/<forskrift>/` for Navs kommentarer til forskrifter som ligger i basen. Mappenavnet er det samme som forskriftens mappe under `forskrifter/`, og `par-N.md` er nummerert etter forskriften, ikke loven.

Ikke gjett stien. Slå opp paragrafen i `indeks.tsv` på roten, der alle rundskrivfilene står med sti (dokumentet heter «Rundskriv»), eller les `oversikt.md` i mappen. Lange kommentarer til én paragraf er ikke delt videre, så søk i filen.

| Tema | Les |
|---|---|
| Medlemskap, trygdetid, pensjonsgivende inntekt, omsorgspoeng, grunnbeløp (kap. 1–3) | Rundskriv `rundskriv/rundskriv-r01-00/`, `r02-00/`, `r03-00/` (og `r03-01` til `r03-04`), Navs kommentarer til omsorgspoengforskriftene i `rundskriv/forskrifter/omsorgspoeng/` og `rundskriv/forskrifter/omsorgspoeng-omsorgsarbeid/` |
| Stønad ved helsetjenester (kap. 5) | `rundskriv/rundskriv-r05-00/` (§ 5-1) og ett rundskriv per paragraf, for eksempel `rundskriv/rundskriv-r05-07/` (psykolog) og `rundskriv/rundskriv-r05-14-02/` (legemidler) |
| Dagpenger, permittering, minsteinntekt (kap. 4) | `merknader/dagpenger.md`, rundskriv `rundskriv/rundskriv-r04-00/` |
| Dagpenger og arbeid eller bosted i et annet EØS-land | `regelverk/eu/forordning-883-2004/merknader/dagpenger.md` fra roten (forordningsteksten er på engelsk), og R45 kapittel 4 |
| Alle ytelser ved bosted, arbeid eller trygdetid i et annet EØS-land, medlemskap og lovvalg i EØS | Navs EØS-rundskriv R45-00: `regelverk/eu/forordning-883-2004/rundskriv/r45-00/oversikt.md` fra roten (kapittel 2 for medlemskap og lovvalg, ellers samme kapittelnummer som i loven) |
| Dagpenger ved konkurs, lønnsgaranti | `regelverk/lonnsgarantiloven/VEIVISER.md` |
| Grunnstønad og hjelpestønad (kap. 6) | Rundskriv `rundskriv/rundskriv-r06-00/` |
| Hjelpestønad ved en bestemt diagnose | `rundskriv/rundskriv-r06-04-for/oversikt.md` (R06-04-FOR, ti diagnoser, gjelder § 6-4 og § 6-5 og supplerer kommentarene i R06-00) |
| Gravferdsstønad, båretransport, omstillingsstønad, barnepensjon (kap. 7, 16, 17, 17 A, 18) | `merknader/etterlatte-gravferd.md`, rundskriv `rundskriv/rundskriv-r07-00/` (gravferd, satsen kan være gammel), `r16-00/`, `r17-00/`, `r18-00/` |
| Sykepenger, omsorgspenger, pleiepenger, opplæringspenger (kap. 8 og 9) | `merknader/sykepenger.md`, forskriftene om sykepengeforsikring (`forskrifter/forsikring-arbeidsgiverperioden/`, `forskrifter/forsikring-sykepenger-selvstendige/`, `forskrifter/forsikring-sykepenger-frilansere/`), legeerklæring fra kiropraktor og manuellterapeut, opplæring i sykmeldingsarbeid og gradering av pleiepenger, rundskriv `rundskriv/rundskriv-r08-00/` og `rundskriv/rundskriv-r09-00/` |
| Tilskudd til ekspertbistand ved langvarig eller hyppig sykefravær (§ 8-7 a) | Forskrift om tilskudd til ekspertbistand i `forskrifter/ekspertbistand/`, rundskrivet til § 8-7 a i `rundskriv/rundskriv-r08-00/`, og NAVs rundskriv til forskriften (R08-07A-FOR, én fil per forskriftsparagraf), start med `rundskriv/forskrifter/ekspertbistand/oversikt.md`. Rundskrivet kommenterer ikke § 9a om forsøk med anskaffelse |
| Hjelpemidler, tolk, bil, høreapparat, briller til barn (kap. 10) | Forskriftene i `forskrifter/hjelpemidler/`, `lese-sekretarhjelp/`, `tolkehjelp-horselshemmede/`, `tolke-ledsagerhjelp-dovblinde/`, `ortopediske-hjelpemidler/`, `horeapparat/`, `motorkjoretoy/` og `briller-barn/`. Rundskriv `rundskriv/rundskriv-r10-00/` (ingen kommentar til § 10-4 eller § 10-7) |
| Stønadsformene i § 10-7 | Ett rundskriv per stønadsform under `rundskriv/`: `rundskriv-r10-07a/` (bokstav a, aktivitetshjelpemidler over 26 år), `rundskriv-r10-07acd/` (bokstav a, c og d og annet og tredje ledd; les begge ved spørsmål om bokstav a, og bare denne for c og d), `rundskriv-r10-07b/` (høreapparat), `rundskriv-r10-07e/` (lese- og sekretærhjelp), `rundskriv-r10-07f/` (tolkehjelp for hørselshemmede), `rundskriv-r10-07g/` (tolke- og ledsagerhjelp for døvblinde), `rundskriv-r10-07h/` (motorkjøretøy), `rundskriv-r10-07i/` (ortopediske hjelpemidler), `rundskriv-r10-07-for/` (servicehund), `rundskriv-r10-07/` (reiseutgifter) og `rundskriv-r10-07-4-5-ledd/` (fjerde og femte ledd) |
| Arbeidsavklaringspenger og tilleggsstønader (kap. 11 og 11 A) | Forskrift om arbeidsavklaringspenger i `forskrifter/arbeidsavklaringspenger/`, `merknader/aap.md`, rundskriv `rundskriv/rundskriv-r11-00/` og `rundskriv/rundskriv-r11a-00/`, Navs kommentarer til tilleggsstønadsforskriften i `rundskriv/rundskriv-r11a-00-for/` |
| Uføretrygd (kap. 12) | `merknader/uforetrygd.md` (forskriftene og kommentarene til dem), institusjonsforskriftene i `forskrifter/uredusert-ytelse-institusjon/`, `forskrifter/uforetrygd-institusjon/` og `forskrifter/overgangsregler-institusjon/`, rundskriv `rundskriv/rundskriv-r12-00/` og forskriftskommentarer (se merknaden) |
| Yrkesskade og yrkessykdom (kap. 13) | Rundskriv `rundskriv/rundskriv-r13-00/`, Navs kommentarer til yrkessykdomsforskriften i `rundskriv/forskrifter/yrkessykdommer/` |
| Svangerskapspenger, foreldrepenger, engangsstønad (kap. 14) | Rundskriv `rundskriv/rundskriv-r14-00/` |
| Stønad til enslig mor eller far (kap. 15) | Rundskriv `rundskriv/rundskriv-r15-00/` (aktivitetskravet i § 15-6 er opphevet fra 1. juli 2026) |
| Alderspensjon (kap. 19 og 20) | Rundskriv `rundskriv/rundskriv-r19-00/` og `r20-00/`. Pensjon fra staten og samordning med folketrygden: `regelverk/spk-loven/VEIVISER.md`, `regelverk/samordningsloven/VEIVISER.md`, `regelverk/afp-loven/VEIVISER.md` |
| Saksbehandling, klage og anke (kap. 21) | Rundskriv `rundskriv/rundskriv-r21-00/` |
| Utbetaling, tilbakekreving, foreldelse, Aa-registeret (kap. 22, 25, 26) | Rundskriv `rundskriv/rundskriv-r22-00/`, `r25-00/` og `r26-00/`, Navs kommentarer til forskriftene om Aa-registeret og arbeidsgivers opplysningsplikt i `rundskriv/forskrifter/aa-registeret/` og `rundskriv/forskrifter/opplysningsplikt-arbeidsgiver/` |
| Permisjon ved fødsel og sykdom i familien | `regelverk/arbeidsmiljoloven/VEIVISER.md` |
| NAV-kontoret og etatens organisering | `regelverk/nav-loven/VEIVISER.md` |
| Økonomisk sosialhjelp (subsidiær til folketrygdytelser) | `regelverk/sosialtjenesteloven/VEIVISER.md` |

<!-- AUTO-START: genereres av verktoy/bygg.py, ikke rediger for hånd -->
## Kilder

- **Lov:** Lov om folketrygd (folketrygdloven) – LOV-1997-02-28-19. Sist endret i kraft: 2026-10-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om beregning av arbeidsavklaringspenger etter EØS-avtalen – FOR-2017-12-13-2099. Sist endret i kraft: 2025-02-19. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om alderspensjon i folketrygden – FOR-2009-12-22-1810. Sist endret i kraft: 2025-01-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om dagpenger under arbeidsløshet – FOR-1998-09-16-890. Sist endret i kraft: 2026-09-24. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om dagpenger for fiskere og fangstfolk under arbeidsløshet (A-trygdforskriften) – FOR-2011-06-01-565. Sist endret i kraft: 2012-01-01. Forvaltes av: Nærings- og fiskeridepartementet.
- **Forskrift:** Kunngjøring av virkningstidspunktet for regulering av kravet til minsteinntekt i dagpengeordningen – FOR-2012-05-25-461. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om overgangsregler i forbindelse med ikrafttredelse av endring av folketrygdloven § 4-9 fra 1. januar 2024 – FOR-2023-12-21-2260. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om tilskudd til ekspertbistand – FOR-2019-08-29-1105. Sist endret i kraft: 2026-03-29. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om stønad til enslig mor eller far etter folketrygdloven kapittel 15 – FOR-2015-11-21-1341. Sist endret i kraft: 2026-07-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om overgangsregler i forbindelse med endringer i folketrygdloven § 15-6 og § 15-8 fra 1. februar 2024 – FOR-2024-01-26-123. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om ytelser til gjenlevende ektefelle og tidligere familiepleier etter folketrygdloven kapittel 17 – FOR-2023-06-21-1007. Sist endret i kraft: 2026-07-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om behovsprøvet gravferdsstønad – FOR-2002-12-12-1492. Sist endret i kraft: 2023-07-07. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om gravferdsstønad og stønad til båretransport for person som er pliktig medlem etter § 2-5 i lov om folketrygd og som dør utenfor Norge og om stønad til båretransport når et medlem dør i et av de nordiske land. – FOR-2002-12-12-1493. Sist endret i kraft: 2006-07-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om dekning av utgifter til båretransport i Norge. – FOR-1997-03-11-216. Sist endret i kraft: 2006-07-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om grunnbeløp, reguleringsfaktorer, satser for minste pensjonsnivå og satser for garantipensjon i folketrygden fra 1. mai 2026 og virknings-tidspunkt for regulering av kravet til minsteinntekt for rett til ytelser etter folketrygdloven kapitlene 4, 8, 9 og 14 – FOR-2026-05-22-869. Sist endret i kraft: 2026-09-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om beregning av lønnsveksten som skal benyttes ved regulering av grunnbeløpet og alderspensjon i folketrygden – FOR-2011-05-06-465. Sist endret i kraft: 2022-04-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om gjennomføring av bilaterale trygdeavtaler – FOR-2024-11-15-2778. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om unntak fra medlemskap i folketrygden for person som er omfattet av eller mottar ytelser etter utenlandsk trygdelovgivning mv og vedkommendes familiemedlemmer – FOR-1997-04-15-314. Sist endret i kraft: 2025-02-17. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om trygdedekning for asylsøkere og deres familiemedlemmer – FOR-2008-05-14-460. Sist endret i kraft: 2021-01-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om medlemskap i trygden under fengselsopphold mv. – FOR-2012-06-22-603. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om fastsetting av pensjonsgivende inntekt for året før det året da et medlem får rett til en trygdeytelse – FOR-1997-03-11-202. Sist endret i kraft: 2024-01-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om godskriving av pensjonspoeng (omsorgspoeng) for personer som har omsorg for små barn – FOR-1997-03-11-203. Sist endret i kraft: 2010-11-30. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om godskriving av pensjonspoeng (omsorgspoeng) for omsorgsarbeid for en syk, en funksjonshemmet eller en eldre person – FOR-1997-03-11-204. Sist endret i kraft: 2017-10-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om godskriving av pensjonspoeng for mottakere av avtalefestet pensjon som omfattes av AFP-tilskottsloven § 12 eller avtalefestet pensjon fra offentlig pensjonsordning før fylte 65 år – FOR-2014-11-26-1465. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om nedsettelse av pensjonsgivende inntekt, pensjonsopptjening og avgift når fastsatt skatt og avgift helt eller delvis ikke er betalt – FOR-1997-12-18-1408. Sist endret i kraft: 2026-01-01. Forvaltes av: Finansdepartementet.
- **Forskrift:** Forskrift om gjennomføring av nedsettelse av pensjonsgivende inntekt, pensjonsopptjening og avgift når fastsatt skatt og avgift helt eller delvis ikke er betalt – FOR-1997-12-19-1421. Sist endret i kraft: 2020-11-01. Forvaltes av: Finansdepartementet.
- **Forskrift:** Forskrift om endring i forskrift om nedsettelse av pensjonsgivende inntekt, pensjonsopptjening og avgift når fastsatt skatt og avgift helt eller delvis ikke er betalt – FOR-2025-06-13-1017. Forvaltes av: Finansdepartementet.
- **Forskrift:** Forskrift om fastsettelse av pensjonsgivende inntekt mv. for medlemmer med inntekt som ikke blir skattlagt av norske myndigheter – FOR-2017-02-13-179. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om pensjonsberegning, om tilståelse og beregning av barnetillegg og barnepensjon og om gjennomføringa av folketrygdlovens bestemmelser om inntektsprøving i tilfelle som omfattes av EØS-avtalen. – FOR-1993-12-23-1251. Sist endret i kraft: 1998-01-16. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om behandling av tvister i arbeidsgiverperioden – FOR-1997-03-25-268. Sist endret i kraft: 2006-07-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om unntak fra anke til Trygderetten – FOR-1997-04-15-324. Sist endret i kraft: 2023-09-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om at visse vedtak kan ankes direkte inn for Trygderetten. – FOR-2006-06-30-743. Sist endret i kraft: 2009-01-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om utveksling av opplysninger mellom Arbeids- og velferdsetaten og pensjonsinnretninger, forsikringsselskaper og andre finansinstitusjoner – FOR-2009-03-11-294. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om elektronisk kommunikasjon med Arbeids- og velferdsetaten – FOR-2009-10-02-1285. Sist endret i kraft: 2015-04-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om unntak fra pålegg om elektronisk kommunikasjon ved innsending av erklæringer og uttalelser til Arbeids- og velferdsetaten (NAV) – FOR-2009-12-07-1480. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om at saksopplysninger til Arbeids- og velferdsetaten skal gis elektronisk – FOR-2018-06-20-937. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om økt beregningsgrunnlag for gifte og samboende uføretrygdede som mottar en uføretrygd omregnet fra uførepensjon – FOR-2016-05-26-529. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om omregning av uførepensjon til uføretrygd – FOR-2014-07-03-947. Sist endret i kraft: 2024-01-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om uføretrygd fra folketrygden – FOR-2014-12-05-1602. Sist endret i kraft: 2026-07-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om gjennomføringen av folketrygdloven § 22-18 og bidragsinnkrevingsloven § 34 om utbetalingsmåten for ytelser mv. – FOR-1999-04-23-534. Sist endret i kraft: 2006-07-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om rentesats etter folketrygdloven § 22-17 første ledd – FOR-2009-12-14-1513. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om disponering av kontantytelser fra folketrygden under opphold i kommunal helse- og omsorgsinstitusjon og i helseinstitusjon i spesialisthelsetjenesten – FOR-2014-02-14-137. Sist endret i kraft: 2021-11-01. Forvaltes av: Helse- og omsorgsdepartementet.
- **Forskrift:** Forskrift om overtredelsesgebyr og tvangsmulkt etter folketrygdloven § 25-3 ved brudd på opplysningsplikten til Arbeidsgiver- og arbeidstakerregisteret mv. – FOR-2014-07-10-968. Sist endret i kraft: 2021-01-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift til folketrygdloven § 25-10 om arbeidsgivers og oppdragsgivers opplysningsplikt om arbeidsforhold og inntekt – FOR-2014-07-10-969. Sist endret i kraft: 2021-01-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om føring av statistikk over sykefravær og fravær ved barns sykdom. – FOR-1997-03-25-272. Sist endret i kraft: 2006-07-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om beregning av kapitalverdier av trygdeytelser. – FOR-1997-03-25-273. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om videreføring av to forskrifter gitt med hjemmel i lov om folketrygd – FOR-1998-01-16-37. Sist endret i kraft: 2008-09-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om Arbeidsgiver- og arbeidstakerregisteret – FOR-2008-08-18-942. Sist endret i kraft: 2024-12-23. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om menerstatning ved yrkesskade. – FOR-1997-04-21-373. Sist endret i kraft: 2006-11-24. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om yrkessykdommer, klimasykdommer og epidemiske sykdommer som skal likestilles med yrkesskade. – FOR-1997-03-11-220. Sist endret i kraft: 2020-04-07. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om sykdommer og forgiftninger m.v. som skal likestilles med yrkesskade – FOR-1997-03-11-219. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om et rådgivende yrkessykdomsutvalg for regelmessig revisjon av forskrift over sykdommer som skal likestilles med yrkesskade – FOR-2026-06-23-1356. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om beregning av uførepensjon og godskriving av pensjonspoeng ved yrkesskade. – FOR-1997-03-11-208. Sist endret i kraft: 2002-01-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om beregning av tilleggspensjon ved yrkesskade. – FOR-1997-03-11-209. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om frivillig yrkesskadetrygd for selvstendig næringsdrivende og frilansere – FOR-1997-03-11-210. Sist endret i kraft: 2010-03-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om frivillig yrkesskadetrygd for elever som ikke er obligatorisk yrkesskadedekket. – FOR-1997-03-25-267. Sist endret i kraft: 2006-07-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om arbeidsavklaringspenger – FOR-2017-12-13-2100. Sist endret i kraft: 2026-03-24. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om stønad til hjelpemidler mv til bedring av funksjonsevnen i arbeidslivet og i dagliglivet og til ombygging av maskiner på arbeidsplassen – FOR-1997-04-15-318. Sist endret i kraft: 2026-11-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om stønad til lese- og sekretærhjelp for blinde og svaksynte – FOR-1997-04-15-319. Sist endret i kraft: 2018-10-02. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om stønad til tolkehjelp for hørselshemmede – FOR-1997-04-15-320. Sist endret i kraft: 2026-02-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om stønad til tolke- og ledsagerhjelp for døvblinde – FOR-1997-04-15-321. Sist endret i kraft: 2026-02-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om stønad til dekning av utgifter til ortopediske hjelpemidler, brystprotese, ansiktsdefektprotese, øyeprotese og parykk – FOR-1997-04-18-336. Sist endret i kraft: 2026-07-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om stønad til høreapparat og tinnitusmaskerer – FOR-1997-04-18-337. Sist endret i kraft: 2018-10-02. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om stønad til motorkjøretøy eller annet transportmiddel – FOR-2003-03-07-290. Sist endret i kraft: 2025-11-03. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om stønad til briller til barn – FOR-2022-07-19-1364. Sist endret i kraft: 2023-12-21. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om adgang til å utbetale uredusert ytelse for visse persongrupper i institusjon – FOR-2014-10-31-1375. Sist endret i kraft: 2024-01-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om beregning av uføretrygd og pensjon mv. under opphold i institusjon – FOR-2014-10-31-1376. Sist endret i kraft: 2024-01-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om overgangsregler for beregning av redusert ytelse under opphold i institusjon og under straffegjennomføring – FOR-2014-10-31-1377. Sist endret i kraft: 2024-01-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om gradering av pleiepenger – FOR-2017-09-14-1405. Sist endret i kraft: 2019-07-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om beregning av uføretrygd etter EØS-avtalen – FOR-2015-02-12-130. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om unntak fra vilkåret om legeerklæring når kiropraktorer og manuellterapeuter dokumenterer arbeidsuførheten med erklæring – FOR-2005-12-21-1668. Sist endret i kraft: 2023-01-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om obligatorisk opplæring i sykmeldingsarbeid for leger – FOR-2012-12-07-1147. Sist endret i kraft: 2014-07-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om forsikring mot ansvar for sykepenger i arbeidsgiverperioden for små bedrifter – FOR-1997-03-25-260. Sist endret i kraft: 2016-07-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om forsikring for tillegg til sykepenger for selvstendig næringsdrivende – FOR-1997-03-25-261. Sist endret i kraft: 2019-01-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om forsikring for tillegg til sykepenger for frilansere – FOR-1997-03-25-262. Sist endret i kraft: 2019-01-01. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om stønad til dekning av utgifter til helsetjenester i utlandet. – FOR-1997-04-30-390. Forvaltes av: Arbeids- og inkluderingsdepartementet.
- **Forskrift:** Forskrift om utvidet stønad til helsetjenester under opphold i utlandet – FOR-1997-04-30-391. Sist endret i kraft: 2021-01-01. Forvaltes av: Arbeids- og inkluderingsdepartementet Helse- og omsorgsdepartementet.
- **Forskrift:** Forskrift om overgangsregler i forbindelse med endringer i folketrygdloven kapittel 15, 16 og 17 fra 1. januar 2016 – FOR-2015-07-02-869. Forvaltes av: Arbeids- og inkluderingsdepartementet.

## Tolkningskilder i basen

Dette er ikke lov- eller forskriftstekst. Oppgi kilden med navn i svaret. Listen lages fra mappene ved hvert bygg. Andre tolkningskilder til regelverket er ikke i basen. Hovedtariffavtalen og EU-rettsaktene har egne veivisere.

- Navs rundskriv (R01-00, R02-00, R03-00, R03-01, R03-02, R03-03, R03-04, R03-05, R04-00, R05-00, R05-01a, R05-02 og 62 til) og Navs kommentarer til forskrifter – se «Rundskriv» under «Andre kilder» nederst
- Sivilombudets uttalelser (74 filer) – start med `rundskriv/sivilombudet/oversikt.md`

## Vedtatte endringer som ikke er i kraft

Ingen funnet i Norsk Lovtidend for regelverket i denne mappen.

## Innhold

### Folketrygdloven

**Kapittel 1. Formål og definisjoner m.m.**

- § 1-1. Formål – `lov/par-1-1.md` (rundskriv: `rundskriv/rundskriv-r01-00/par-1-1.md`)
- § 1-2. Vern mot private avtaler – `lov/par-1-2.md` (rundskriv: `rundskriv/rundskriv-r01-00/par-1-2.md`, `rundskriv/rundskriv-r08-00/par-1-2.md`)
- § 1-3. Forholdet til EØS-avtalens hoveddel – `lov/par-1-3.md` (rundskriv: `rundskriv/rundskriv-r01-00/par-1-3.md`)
- § 1-3 a. Gjennomføring av trygdeforordningen og gjennomføringsforordningen – `lov/par-1-3a.md` (rundskriv: `rundskriv/rundskriv-r01-00/par-1-3a.md`)
- § 1-3 b. Andre folkerettslige bestemmelser om trygdekoordinering – `lov/par-1-3b.md` (rundskriv: `rundskriv/rundskriv-r01-00/par-1-3b.md`)
- § 1-4. Grunnbeløpet – `lov/par-1-4.md` (rundskriv: `rundskriv/rundskriv-r01-00/par-1-4.md`)
- § 1-5. Sivilstand – `lov/par-1-5.md` (rundskriv: `rundskriv/rundskriv-r01-00/par-1-5.md`)
- § 1-6. Barn – `lov/par-1-6.md` (rundskriv: `rundskriv/rundskriv-r01-00/par-1-6.md`)
- § 1-7. (Opphevet) – `lov/par-1-7.md` (rundskriv: `rundskriv/rundskriv-r01-00/par-1-7.md`)
- § 1-8. Arbeidstaker – `lov/par-1-8.md` (rundskriv: `rundskriv/rundskriv-r01-00/par-1-8.md`, `rundskriv/rundskriv-r08-00/par-1-8.md`)
- § 1-9. Frilanser – `lov/par-1-9.md` (rundskriv: `rundskriv/rundskriv-r01-00/par-1-9.md`)
- § 1-10. Selvstendig næringsdrivende – `lov/par-1-10.md` (rundskriv: `rundskriv/rundskriv-r01-00/par-1-10.md`)

**Kapittel 2. Medlemskap**

- § 2-1. Personer som er bosatt i Norge – `lov/par-2-1.md` (rundskriv: `rundskriv/rundskriv-r02-00/par-2-1.md`)
- § 2-1 a. Forholdet til bestemmelser om internasjonal trygdekoordinering – `lov/par-2-1a.md`
- § 2-2. Arbeidstakere i Norge og på kontinentalsokkelen – `lov/par-2-2.md` (rundskriv: `rundskriv/rundskriv-r02-00/par-2-2.md`)
- § 2-3. Medlemskap på Svalbard, på Jan Mayen og i norske biland – `lov/par-2-3.md` (rundskriv: `rundskriv/rundskriv-r02-00/par-2-3.md`)
- § 2-4. Avtaler om arbeidstakere mv. på kontinentalsokkelen – `lov/par-2-4.md` (rundskriv: `rundskriv/rundskriv-r02-00/par-2-4.md`)
- § 2-5. Pliktig medlemskap for personer utenfor Norge – `lov/par-2-5.md` (rundskriv: `rundskriv/rundskriv-r02-00/par-2-5.md`)
- § 2-6. Medlemskap som gir trygdedekning bare ved yrkesskade og dødsfall – `lov/par-2-6.md` (rundskriv: `rundskriv/rundskriv-r02-00/par-2-6.md`)
- § 2-7. Frivillig medlemskap for personer i Norge – `lov/par-2-7.md` (rundskriv: `rundskriv/rundskriv-r02-00/par-2-7.md`)
- § 2-7 a. Frivillig medlemskap for personer bosatt i Norge og som er i arbeid på skip registrert i utlandet – `lov/par-2-7a.md` (rundskriv: `rundskriv/rundskriv-r02-00/par-2-7a.md`)
- § 2-8. Frivillig medlemskap for personer utenfor Norge – `lov/par-2-8.md` (rundskriv: `rundskriv/rundskriv-r02-00/par-2-8.md`)
- § 2-9. Trygdedekning ved frivillig medlemskap utenfor Norge – `lov/par-2-9.md` (rundskriv: `rundskriv/rundskriv-r02-00/par-2-9.md`)
- § 2-10. Opptjening av rettigheter for personer med begrenset medlemskap – `lov/par-2-10.md` (rundskriv: `rundskriv/rundskriv-r02-00/par-2-10.md`)
- § 2-11. Unntak for ambassadepersonell o.a. – `lov/par-2-11.md` (rundskriv: `rundskriv/rundskriv-r02-00/par-2-11.md`)
- § 2-12. Unntak for ansatte på turistskip – `lov/par-2-12.md` (rundskriv: `rundskriv/rundskriv-r02-00/par-2-12.md`)
- § 2-13. Unntak for personer med rettigheter i utenlandske trygdeordninger m.m. – `lov/par-2-13.md` (rundskriv: `rundskriv/rundskriv-r02-00/par-2-13.md`)
- § 2-14. Opphør av pliktig medlemskap – `lov/par-2-14.md` (rundskriv: `rundskriv/rundskriv-r02-00/par-2-14.md`)
- § 2-15. Opphør av frivillig medlemskap – `lov/par-2-15.md` (rundskriv: `rundskriv/rundskriv-r02-00/par-2-15.md`)
- § 2-16. Forskrifter om asylsøkere – `lov/par-2-16.md` (rundskriv: `rundskriv/rundskriv-r02-00/par-2-16.md`)
- § 2-17. Medlemskap under fengselsopphold mv. – `lov/par-2-17.md` (rundskriv: `rundskriv/rundskriv-r02-00/par-2-17.md`)

**Kapittel 3. Visse beregningsregler, trygdetid, pensjonspoeng og pensjonsgivende inntekt**

- § 3-1. Forholdet til bestemmelser om internasjonal trygdekoordinering – `lov/par-3-1.md` (rundskriv: `rundskriv/rundskriv-r03-01/par-3-1.md`)
- § 3-2. Grunnpensjon – `lov/par-3-2.md` (rundskriv: `rundskriv/rundskriv-r03-01/par-3-2.md`)
- § 3-3. Særtillegg – `lov/par-3-3.md` (rundskriv: `rundskriv/rundskriv-r03-01/par-3-3.md`)
- § 3-4. (Opphevet) – `lov/par-3-4.md`
- § 3-5. Trygdetid ved beregning av ytelser etter kapitlene 17, 17 A, 18 og 19 – `lov/par-3-5.md` (rundskriv: `rundskriv/rundskriv-r03-01/par-3-5.md`)
- § 3-6. (Opphevet) – `lov/par-3-6.md`
- § 3-7. Trygdetid ved beregning av omstillingsstønad, pensjon og overgangsstønad til gjenlevende ektefelle – `lov/par-3-7.md` (rundskriv: `rundskriv/rundskriv-r03-01/par-3-7.md`)
- § 3-8. Tilleggspensjon – `lov/par-3-8.md` (rundskriv: `rundskriv/rundskriv-r03-02/par-3-8.md`)
- § 3-9. Særregler om tilleggspensjon for personer født før 1937 – `lov/par-3-9.md` (rundskriv: `rundskriv/rundskriv-r03-02/par-3-9.md`)
- § 3-10. Poengår – `lov/par-3-10.md` (rundskriv: `rundskriv/rundskriv-r03-02/par-3-10.md`)
- § 3-11. Sluttpoengtall – `lov/par-3-11.md` (rundskriv: `rundskriv/rundskriv-r03-02/par-3-11.md`)
- § 3-12. Pensjonspoeng – `lov/par-3-12.md` (rundskriv: `rundskriv/rundskriv-r03-02/par-3-12.md`)
- § 3-13. Opptjening av pensjonspoeng – hovedregler – `lov/par-3-13.md` (rundskriv: `rundskriv/rundskriv-r03-02/par-3-13.md`)
- § 3-14. Opptjening av pensjonspoeng for medlemmer som mottar uføretrygd – `lov/par-3-14.md` (rundskriv: `rundskriv/rundskriv-r03-02/par-3-14.md`)
- § 3-15. Pensjonsgivende inntekt – `lov/par-3-15.md` (rundskriv: `rundskriv/rundskriv-r03-02/par-3-15.md`)
- § 3-16. Godskriving av pensjonspoeng for omsorgsarbeid – `lov/par-3-16.md` (rundskriv: `rundskriv/rundskriv-r03-02/par-3-16.md`, `rundskriv/rundskriv-r06-00/par-3-16.md`)
- § 3-17. Fastsetting og godskriving av pensjonspoeng for mottakere av uføretrygd – `lov/par-3-17.md` (rundskriv: `rundskriv/rundskriv-r03-03/par-3-17.md`)
- § 3-18. Beregning av alderspensjon ved yrkesskade – `lov/par-3-18.md` (rundskriv: `rundskriv/rundskriv-r03-03/par-3-18.md`)
- § 3-19. Godskriving av pensjonspoeng for mottakere av avtalefestet pensjon – `lov/par-3-19.md` (rundskriv: `rundskriv/rundskriv-r03-03/par-3-19.md`)
- § 3-20. (Opphevet) – `lov/par-3-20.md`
- § 3-21. (Opphevet) – `lov/par-3-21.md`
- § 3-22. Garantert tilleggspensjon til unge uføre født før 1941 – `lov/par-3-22.md` (rundskriv: `rundskriv/rundskriv-r03-03/par-3-22.md`)
- § 3-23. Beregning av tilleggspensjon til gjenlevende ektefelle – `lov/par-3-23.md` (rundskriv: `rundskriv/rundskriv-r03-04/par-3-23.md`)
- § 3-24. (Opphevet) – `lov/par-3-24.md` (rundskriv: `rundskriv/rundskriv-r03-05/par-3-24.md`)
- § 3-25. (Opphevet) – `lov/par-3-25.md` (rundskriv: `rundskriv/rundskriv-r03-05/par-3-25.md`)
- § 3-26. (Opphevet) – `lov/par-3-26.md` (rundskriv: `rundskriv/rundskriv-r03-05/par-3-26.md`)
- § 3-27. (Opphevet) – `lov/par-3-27.md` (rundskriv: `rundskriv/rundskriv-r26-00/par-3-27.md`)
- § 3-28. (Opphevet) – `lov/par-3-28.md`
- § 3-29. (Opphevet) – `lov/par-3-29.md`
- § 3-30. (Opphevet) – `lov/par-3-30.md`

**Kapittel 4. Dagpenger under arbeidsløshet**

- § 4-1. Formål – `lov/par-4-1.md` (rundskriv: `rundskriv/rundskriv-r04-00/par-4-1.md`)
- § 4-1 a. Forholdet til bestemmelser om internasjonal trygdekoordinering – `lov/par-4-1a.md`
- § 4-2. Opphold i Norge – `lov/par-4-2.md` (rundskriv: `rundskriv/rundskriv-r04-00/par-4-2.md`, `rundskriv/rundskriv-r26-00/par-4-2.md`)
- § 4-3. Tap av arbeidsinntekt og arbeidstid – `lov/par-4-3.md` (rundskriv: `rundskriv/rundskriv-r04-00/par-4-3.md`)
- § 4-4. Krav til minsteinntekt – `lov/par-4-4.md` (rundskriv: `rundskriv/rundskriv-r04-00/par-4-4.md`)
- § 4-5. Reelle arbeidssøkere – `lov/par-4-5.md` (rundskriv: `rundskriv/rundskriv-r04-00/par-4-5.md`)
- § 4-6. Dagpenger under utdanning, opplæring, etablering av egen virksomhet m.v. – `lov/par-4-6.md` (rundskriv: `rundskriv/rundskriv-r04-00/par-4-6.md`)
- § 4-7. Dagpenger til permitterte – `lov/par-4-7.md` (rundskriv: `rundskriv/rundskriv-r04-00/par-4-7.md`)
- § 4-8. Meldeplikt og møteplikt – `lov/par-4-8.md` (rundskriv: `rundskriv/rundskriv-r04-00/par-4-8.md`)
- § 4-9. Egenandel – `lov/par-4-9.md` (rundskriv: `rundskriv/rundskriv-r04-00/par-4-9.md`)
- § 4-10. Sanksjonsperiode ved selvforskyldt arbeidsløshet – `lov/par-4-10.md` (rundskriv: `rundskriv/rundskriv-r04-00/par-4-10.md`)
- § 4-11. Dagpengegrunnlag – `lov/par-4-11.md` (rundskriv: `rundskriv/rundskriv-r04-00/par-4-11.md`)
- § 4-12. Dagpengenes størrelse – `lov/par-4-12.md` (rundskriv: `rundskriv/rundskriv-r04-00/par-4-12.md`)
- § 4-13. Graderte dagpenger – `lov/par-4-13.md` (rundskriv: `rundskriv/rundskriv-r04-00/par-4-13.md`)
- § 4-14. Ferietillegg – `lov/par-4-14.md` (rundskriv: `rundskriv/rundskriv-r04-00/par-4-14.md`)
- § 4-15. Antall stønadsuker (stønadsperiode) – `lov/par-4-15.md` (rundskriv: `rundskriv/rundskriv-r04-00/par-4-15.md`)
- § 4-16. Gjenopptak av løpende stønadsperiode – `lov/par-4-16.md` (rundskriv: `rundskriv/rundskriv-r04-00/par-4-16.md`)
- § 4-17. (Opphevet) – `lov/par-4-17.md`
- § 4-18. Dagpenger til fiskere og fangstmenn – `lov/par-4-18.md` (rundskriv: `rundskriv/rundskriv-r04-00/par-4-18.md`)
- § 4-19. Dagpenger etter avtjent verneplikt – `lov/par-4-19.md` (rundskriv: `rundskriv/rundskriv-r04-00/par-4-19.md`)
- § 4-20. Tidsbegrenset bortfall av dagpenger – `lov/par-4-20.md` (rundskriv: `rundskriv/rundskriv-r04-00/par-4-20.md`)
- § 4-21. Bortfall av retten til dagpenger – `lov/par-4-21.md` (rundskriv: `rundskriv/rundskriv-r04-00/par-4-21.md`)
- § 4-22. Bortfall ved streik og lock-out – `lov/par-4-22.md` (rundskriv: `rundskriv/rundskriv-r04-00/par-4-22.md`)
- § 4-23. Bortfall på grunn av alder – `lov/par-4-23.md` (rundskriv: `rundskriv/rundskriv-r04-00/par-4-23.md`)
- § 4-24. Medlem som har fulle ytelser etter folketrygdloven eller avtalefestet pensjon – `lov/par-4-24.md` (rundskriv: `rundskriv/rundskriv-r04-00/par-4-24.md`)
- § 4-25. Samordning med reduserte ytelser fra folketrygden, eller redusert avtalefestet pensjon – `lov/par-4-25.md` (rundskriv: `rundskriv/rundskriv-r04-00/par-4-25.md`)
- § 4-26. Samordning med ytelser utenfor folketrygden – `lov/par-4-26.md` (rundskriv: `rundskriv/rundskriv-r04-00/par-4-26.md`)
- § 4-27. Fellesbestemmelser ved bortfall/samordning – `lov/par-4-27.md` (rundskriv: `rundskriv/rundskriv-r04-00/par-4-27.md`)
- § 4-28. Utestengning – `lov/par-4-28.md` (rundskriv: `rundskriv/rundskriv-r04-00/par-4-28.md`)

**Kapittel 5. Stønad ved helsetjenester**

- § 5-1. Formål m.m. – `lov/par-5-1.md` (rundskriv: `rundskriv/rundskriv-r05-00/par-5-1.md`, `rundskriv/rundskriv-r05-25/par-5-1.md`)
- § 5-1 a. Forholdet til bestemmelser om internasjonal trygdekoordinering – `lov/par-5-1a.md`
- § 5-2. Medlemskap – `lov/par-5-2.md`
- § 5-3. Utgiftstak for egenandeler – `lov/par-5-3.md`
- § 5-4. Legehjelp – `lov/par-5-4.md` (rundskriv: `rundskriv/rundskriv-r05-25/par-5-4.md`)
- § 5-5. Private laboratorier og røntgeninstitutter – `lov/par-5-5.md`
- § 5-6. Tannlegehjelp – `lov/par-5-6.md` (rundskriv: `rundskriv/rundskriv-r05-25/par-5-6.md`)
- § 5-6 a. Tannpleierhjelp – `lov/par-5-6a.md`
- § 5-7. Psykologhjelp – `lov/par-5-7.md` (rundskriv: `rundskriv/rundskriv-r05-25/par-5-7.md`)
- § 5-8. Fysioterapi – `lov/par-5-8.md` (rundskriv: `rundskriv/rundskriv-r05-25/par-5-8.md`, `rundskriv/rundskriv-r26-00/par-5-8.md`)
- § 5-9. Behandling hos kiropraktor – `lov/par-5-9.md` (rundskriv: `rundskriv/rundskriv-r05-25/par-5-9.md`)
- § 5-10. Behandling hos logoped og audiopedagog – `lov/par-5-10.md`
- § 5-10a. Behandling hos ortoptist – `lov/par-5-10a.md`
- § 5-11. (Opphevet) – `lov/par-5-11.md`
- § 5-12. Jordmorhjelp – `lov/par-5-12.md`
- § 5-13. Stønad ved fødsel utenfor institusjon – `lov/par-5-13.md` (rundskriv: `rundskriv/rundskriv-r05-13/par-5-13.md`)
- § 5-14. Viktige legemidler og spesielt medisinsk utstyr m.m. – `lov/par-5-14.md` (rundskriv: `rundskriv/rundskriv-r05-25/par-5-14.md`)
- § 5-15. Viktige legemidler som også brukes i sykehus – `lov/par-5-15.md`
- § 5-16. (Opphevet) – `lov/par-5-16.md` (rundskriv: `rundskriv/rundskriv-r05-25/par-5-16.md`)
- § 5-17. (Opphevet) – `lov/par-5-17.md`
- § 5-18. (Opphevet) – `lov/par-5-18.md`
- § 5-19. (Opphevet) – `lov/par-5-19.md`
- § 5-20. (Opphevet) – `lov/par-5-20.md`
- § 5-21. Fastlønnstilskott – `lov/par-5-21.md`
- § 5-22. Bidrag til spesielle formål – `lov/par-5-22.md` (rundskriv: `rundskriv/rundskriv-r05-25/par-5-22.md`)
- § 5-23. Unntak for militærpersoner – `lov/par-5-23.md`
- § 5-24. Stønad til helsetjenester i utlandet – `lov/par-5-24.md`
- § 5-24 a. Stønad til helsetjenester i et annet EØS-land – `lov/par-5-24a.md`
- § 5-25. Stønad ved yrkesskade – `lov/par-5-25.md` (rundskriv: `rundskriv/rundskriv-r05-25/par-5-25.md`)
- § 5-26. Stønad ved sykdom som har oppstått i tidsrom uten stønadsrett – `lov/par-5-26.md`

**Kapittel 6. Grunnstønad og hjelpestønad**

- § 6-1. Formål – `lov/par-6-1.md` (rundskriv: `rundskriv/rundskriv-r06-00/par-6-1.md`)
- § 6-1 a. Forholdet til bestemmelser om internasjonal trygdekoordinering – `lov/par-6-1a.md` (rundskriv: `rundskriv/rundskriv-r06-00/par-6-1a.md`)
- § 6-2. Sykdom, skade eller lyte – `lov/par-6-2.md` (rundskriv: `rundskriv/rundskriv-r06-00/par-6-2.md`)
- § 6-3. Grunnstønad – `lov/par-6-3.md` (rundskriv: `rundskriv/rundskriv-r06-00/par-6-3.md`)
- § 6-4. Hjelpestønad – `lov/par-6-4.md` (rundskriv: `rundskriv/rundskriv-r06-00/par-6-4.md`)
- § 6-5. Forhøyet hjelpestønad til barn og unge – `lov/par-6-5.md` (rundskriv: `rundskriv/rundskriv-r06-00/par-6-5-2.md`, `rundskriv/rundskriv-r06-00/par-6-5.md`)
- § 6-6. Reduksjon på grunn av manglende trygdetid – `lov/par-6-6.md` (rundskriv: `rundskriv/rundskriv-r06-00/par-6-6.md`)
- § 6-7. Revurdering – `lov/par-6-7.md` (rundskriv: `rundskriv/rundskriv-r06-00/par-6-7.md`)
- § 6-8. Bortfall av stønad under opphold i institusjon og andre lovregulerte boformer – `lov/par-6-8.md` (rundskriv: `rundskriv/rundskriv-r06-00/par-6-8.md`)
- § 6-9. Stønad ved yrkesskade – `lov/par-6-9.md` (rundskriv: `rundskriv/rundskriv-r06-00/par-6-9.md`)

**Kapittel 7. Stønad ved gravferd**

- § 7-1. Formål – `lov/par-7-1.md` (rundskriv: `rundskriv/rundskriv-r07-00/par-7-1.md`)
- § 7-1 a. Forholdet til bestemmelser om internasjonal trygdekoordinering – `lov/par-7-1a.md` (rundskriv: `rundskriv/rundskriv-r07-00/par-7-1a.md`)
- § 7-2. Gravferdsstønad – `lov/par-7-2.md` (rundskriv: `rundskriv/rundskriv-r07-00/par-7-2.md`, `rundskriv/rundskriv-r19-00/par-7-2.md`)
- § 7-3. Stønad til båretransport – `lov/par-7-3.md` (rundskriv: `rundskriv/rundskriv-r07-00/par-7-3.md`, `rundskriv/rundskriv-r26-00/par-7-3.md`)
- § 7-4. Stønad ved dødsfall utenfor Norge – `lov/par-7-4.md` (rundskriv: `rundskriv/rundskriv-r07-00/par-7-4.md`)
- § 7-5. Stønad ved dødsfall som skyldes yrkesskade – `lov/par-7-5.md` (rundskriv: `rundskriv/rundskriv-r07-00/par-7-5.md`)

**Kapittel 8. Sykepenger**

- § 8-1. Formål – `lov/par-8-1.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-1.md`)
- § 8-1 a. Forholdet til bestemmelser om internasjonal trygdekoordinering – `lov/par-8-1a.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-1a.md`)
- § 8-2. Opptjeningstid – `lov/par-8-2.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-2.md`)
- § 8-3. Tap av pensjonsgivende inntekt og minsteinntekt – `lov/par-8-3.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-3.md`)
- § 8-4. Arbeidsuførhet – `lov/par-8-4.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-4.md`)
- § 8-5. Sykepenger ved friskmelding til arbeidsformidling – `lov/par-8-5.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-5.md`)
- § 8-6. Gradert sykmelding – `lov/par-8-6.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-6.md`)
- § 8-7. Dokumentasjon av arbeidsuførhet – `lov/par-8-7.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-7.md`)
- § 8-7 a. Oppfølging mv. i regi av Arbeids- og velferdsetaten – `lov/par-8-7a.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-7a.md`)
- § 8-8. Medlemmets medvirkning – `lov/par-8-8.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-8.md`)
- § 8-9. Oppholdskrav – `lov/par-8-9.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-9.md`)
- § 8-10. Sykepengegrunnlag – `lov/par-8-10.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-10.md`)
- § 8-11. Sykepengedager – `lov/par-8-11.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-11.md`)
- § 8-12. Antall sykepengedager – `lov/par-8-12.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-12.md`)
- § 8-13. Graderte sykepenger – `lov/par-8-13.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-13.md`)
- § 8-14. Tilskott til arbeidsreiser – `lov/par-8-14.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-14.md`)
- § 8-15. Rett til sykepenger og feriepenger som arbeidstaker – `lov/par-8-15.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-15.md`)
- § 8-16. Sykepengenes størrelse (kompensasjonsnivå) – `lov/par-8-16.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-16.md`)
- § 8-17. Sykepenger fra trygden – `lov/par-8-17.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-17.md`)
- § 8-18. Sykepenger fra arbeidsgiveren – `lov/par-8-18.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-18.md`)
- § 8-19. Beregning av arbeidsgiverperiode – `lov/par-8-19.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-19.md`)
- § 8-20. Risiko for særlig stort sykefravær eller svangerskapsrelatert sykefravær – `lov/par-8-20.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-20.md`)
- § 8-21. Forsikring mot ansvar for sykepenger i arbeidsgiverperioden – `lov/par-8-21.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-21.md`)
- § 8-22. Trygdens ansvar når arbeidsgiveren ikke betaler – `lov/par-8-22.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-22.md`)
- § 8-23. Egenmelding – `lov/par-8-23.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-23.md`)
- § 8-24. Rett til å nytte egenmelding – `lov/par-8-24.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-24.md`)
- § 8-25. Unntak fra retten til å nytte egenmelding – `lov/par-8-25.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-25.md`)
- § 8-26. Egenerklæring – `lov/par-8-26.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-26.md`)
- § 8-27. Tap av retten til å nytte egenmelding – `lov/par-8-27.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-27.md`)
- § 8-28. Sykepengegrunnlaget i arbeidsgiverperioden – `lov/par-8-28.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-28.md`)
- § 8-29. Inntekter som inngår i beregning av den aktuelle månedsinntekten – `lov/par-8-29.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-29.md`)
- § 8-30. Sykepengegrunnlaget når trygden yter sykepenger – `lov/par-8-30.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-30.md`)
- § 8-31. Sykepenger under streik og lockout – `lov/par-8-31.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-31.md`)
- § 8-32. Sykepenger under gå-sakte-aksjon – `lov/par-8-32.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-32.md`)
- § 8-33. Feriepenger – `lov/par-8-33.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-33.md`)
- § 8-34. Sykepengedekning m.m. – `lov/par-8-34.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-34.md`)
- § 8-35. Sykepengegrunnlag – `lov/par-8-35.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-35.md`)
- § 8-36. Forsikring for tillegg til sykepenger – `lov/par-8-36.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-36.md`)
- § 8-37. Opphør av forsikring for tillegg til sykepenger – `lov/par-8-37.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-37.md`)
- § 8-38. Sykepengedekning og sykepengegrunnlag – `lov/par-8-38.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-38.md`)
- § 8-39. Forsikring for tilleggssykepenger – `lov/par-8-39.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-39.md`)
- § 8-40. Arbeidstaker og frilanser – `lov/par-8-40.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-40.md`)
- § 8-41. Arbeidstaker og selvstendig næringsdrivende – `lov/par-8-41.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-41.md`)
- § 8-42. Selvstendig næringsdrivende og frilanser – `lov/par-8-42.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-42.md`)
- § 8-43. Arbeidstaker, selvstendig næringsdrivende og frilanser – `lov/par-8-43.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-43.md`)
- § 8-44. Arbeidstaker på skip – `lov/par-8-44.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-44.md`)
- § 8-45. Fiskere – `lov/par-8-45.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-45.md`)
- § 8-46. Vernepliktige – `lov/par-8-46.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-46.md`)
- § 8-47. Yrkesaktive medlemmer som midlertidig har vært ute av inntektsgivende arbeid – `lov/par-8-47.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-47.md`)
- § 8-48. Forholdet mellom sykepenger og andre folketrygdytelser – `lov/par-8-48.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-48.md`)
- § 8-49. Medlemmer med dagpenger under arbeidsløshet eller ventelønn m.m. – `lov/par-8-49.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-49.md`)
- § 8-50. Medlemmer med uføretrygd – `lov/par-8-50.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-50.md`)
- § 8-51. Medlem mellom 62 og 70 år – `lov/par-8-51.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-51.md`)
- § 8-52. Medlemmer med avtalefestet pensjon – `lov/par-8-52.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-52.md`)
- § 8-53. Sykepenger under opphold i helseinstitusjon o.l. – `lov/par-8-53.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-53.md`)
- § 8-54. Opphold i fengsel – `lov/par-8-54.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-54.md`)
- § 8-55. Sykepenger ved yrkesskade – `lov/par-8-55.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-8-55.md`)

**Kapittel 9. Stønad ved barns og andre nærståendes sykdom**

- § 9-1. Formål – `lov/par-9-1.md` (rundskriv: `rundskriv/rundskriv-r09-00/par-9-1.md`)
- § 9-1 a. Forholdet til bestemmelser om internasjonal trygdekoordinering – `lov/par-9-1a.md`
- § 9-2. Opptjeningstid – `lov/par-9-2.md` (rundskriv: `rundskriv/rundskriv-r09-00/par-9-2.md`)
- § 9-3. Tap av pensjonsgivende inntekt og minsteinntekt – `lov/par-9-3.md` (rundskriv: `rundskriv/rundskriv-r09-00/par-9-3.md`)
- § 9-4. Oppholdskrav – `lov/par-9-4.md` (rundskriv: `rundskriv/rundskriv-r09-00/par-9-4.md`)
- § 9-5. Stønadssituasjonen for omsorgspenger – `lov/par-9-5.md` (rundskriv: `rundskriv/rundskriv-r09-00/par-9-5.md`)
- § 9-6. Antall dager med omsorgspenger – `lov/par-9-6.md` (rundskriv: `rundskriv/rundskriv-r09-00/par-9-6.md`)
- § 9-7. Dokumentasjon av sykdom – `lov/par-9-7.md` (rundskriv: `rundskriv/rundskriv-r09-00/par-9-7.md`)
- § 9-8. Omsorgspenger fra arbeidsgiveren – `lov/par-9-8.md` (rundskriv: `rundskriv/rundskriv-r09-00/par-9-8.md`)
- § 9-9. Omsorgspenger fra trygden – `lov/par-9-9.md` (rundskriv: `rundskriv/rundskriv-r09-00/par-9-9.md`)
- § 9-10. Pleiepenger til medlem med omsorg for syke barn – `lov/par-9-10.md` (rundskriv: `rundskriv/rundskriv-r09-00/par-9-10.md`)
- § 9-11. Graderte pleiepenger – `lov/par-9-11.md` (rundskriv: `rundskriv/rundskriv-r09-00/par-9-11.md`)
- § 9-11 a. (Opphevet) – `lov/par-9-11a.md`
- § 9-12. (Opphevet) – `lov/par-9-12.md` (rundskriv: `rundskriv/rundskriv-r09-00/par-9-12.md`)
- § 9-13. Pleiepenger for pleie av en nærstående i livets sluttfase – `lov/par-9-13.md` (rundskriv: `rundskriv/rundskriv-r09-00/par-9-13.md`)
- § 9-14. Opplæringspenger til et medlem som tar seg av et funksjonshemmet eller langvarig sykt barn – `lov/par-9-14.md` (rundskriv: `rundskriv/rundskriv-r09-00/par-9-14.md`)
- § 9-15. Utbetaling av pleiepenger og opplæringspenger – `lov/par-9-15.md` (rundskriv: `rundskriv/rundskriv-r09-00/par-9-15.md`)
- § 9-16. Krav til dokumentasjon – `lov/par-9-16.md` (rundskriv: `rundskriv/rundskriv-r09-00/par-9-16.md`)
- § 9-17. Feriepenger til arbeidstakere – `lov/par-9-17.md` (rundskriv: `rundskriv/rundskriv-r09-00/par-9-17.md`)

**Kapittel 10. Stønad for å kompensere for utgifter til bedring av arbeidsevnen og funksjonsevnen i dagliglivet**

- § 10-1. Formål – `lov/par-10-1.md` (rundskriv: `rundskriv/rundskriv-r10-00/par-10-1.md`)
- § 10-1 a. Forholdet til bestemmelser om internasjonal trygdekoordinering – `lov/par-10-1a.md` (rundskriv: `rundskriv/rundskriv-r10-00/par-10-1a.md`)
- § 10-2. (Opphevet) – `lov/par-10-2.md`
- § 10-3. Opphold i Norge eller i utlandet – `lov/par-10-3.md` (rundskriv: `rundskriv/rundskriv-r10-00/par-10-3.md`)
- § 10-4. Alder – `lov/par-10-4.md`
- § 10-5. Stønad til bedring av funksjonsevnen i arbeidslivet – `lov/par-10-5.md` (rundskriv: `rundskriv/rundskriv-r10-00/par-10-5.md`)
- § 10-6. Stønad til bedring av funksjonsevnen i dagliglivet – `lov/par-10-6.md` (rundskriv: `rundskriv/rundskriv-r10-00/par-10-6.md`)
- § 10-7. Stønadsformer – `lov/par-10-7.md` (rundskriv: `rundskriv/rundskriv-r10-07-4-5-ledd/par-10-7.md`, `rundskriv/rundskriv-r10-07acd/par-10-7.md`)
- § 10-7 a. Stønad til briller til barn – `lov/par-10-7a.md`
- § 10-8. Forholdet til ytelser etter annen lovgivning – `lov/par-10-8.md` (rundskriv: `rundskriv/rundskriv-r10-00/par-10-8.md`)
- § 10-9. (Opphevet) – `lov/par-10-9.md`
- § 10-10. (Opphevet) – `lov/par-10-10.md` (rundskriv: `rundskriv/rundskriv-r26-00/par-10-10.md`)
- § 10-11. (Opphevet) – `lov/par-10-11.md`
- § 10-12. (Opphevet) – `lov/par-10-12.md`
- § 10-13. (Opphevet) – `lov/par-10-13.md`
- § 10-14. (Opphevet) – `lov/par-10-14.md`
- § 10-15. (Opphevet) – `lov/par-10-15.md`
- § 10-16. (Opphevet) – `lov/par-10-16.md`
- § 10-17. (Flyttet til § 10-8 ved lov 19 des 2008 nr. 106.) – `lov/par-10-17.md`
- § 10-18. (Opphevet) – `lov/par-10-18.md`

**Kapittel 11. Arbeidsavklaringspenger**

- § 11-1. Formål – `lov/par-11-1.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-1.md`)
- § 11-1 a. Forholdet til bestemmelser om internasjonal trygdekoordinering – `lov/par-11-1a.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-1a.md`)
- § 11-2. Forutgående medlemskap – `lov/par-11-2.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-2.md`)
- § 11-3. Oppholdskrav – `lov/par-11-3.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-3.md`)
- § 11-4. Alder – `lov/par-11-4.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-4.md`)
- § 11-5. Nedsatt arbeidsevne – krav til årsakssammenheng – `lov/par-11-5.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-5.md`)
- § 11-6. Behov for bistand til å skaffe seg eller beholde arbeid – `lov/par-11-6.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-6.md`)
- § 11-7. Medlemmets aktivitetsplikt – `lov/par-11-7.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-7.md`)
- § 11-8. Fravær fra fastsatt aktivitet – `lov/par-11-8.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-8.md`)
- § 11-9. Reduksjon av arbeidsavklaringspenger ved brudd på nærmere bestemte aktivitetsplikter – `lov/par-11-9.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-9.md`)
- § 11-10. Meldeplikt – `lov/par-11-10.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-10.md`)
- § 11-11. Oppfølging fra Arbeids- og velferdsetaten – `lov/par-11-11.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-11.md`)
- § 11-12. Varighet – `lov/par-11-12.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-12.md`)
- § 11-12 a. Opphevet – `lov/par-11-12a.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-12a.md`)
- § 11-13. Arbeidsavklaringspenger til et medlem som ikke har opparbeidet seg ny rett til sykepenger – `lov/par-11-13.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-13.md`)
- § 11-14. Arbeidsavklaringspenger til studenter – `lov/par-11-14.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-14.md`)
- § 11-15. Arbeidsavklaringspenger til et medlem som etablerer egen virksomhet – `lov/par-11-15.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-15.md`)
- § 11-16. (Opphevet) – `lov/par-11-16.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-16.md`)
- § 11-17. Arbeidsavklaringspenger i perioden som arbeidssøker – `lov/par-11-17.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-17.md`)
- § 11-18. Arbeidsavklaringspenger under behandling av krav om uføretrygd – `lov/par-11-18.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-18.md`)
- § 11-19. Grunnlaget for beregningen av arbeidsavklaringspenger – `lov/par-11-19.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-19-2.md`, `rundskriv/rundskriv-r11-00/par-11-19.md`)
- § 11-20. Arbeidsavklaringspengenes størrelse og vilkår om barnetillegg – `lov/par-11-20.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-20.md`)
- § 11-21. (Opphevet) – `lov/par-11-21.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-21.md`)
- § 11-22. Arbeidsavklaringspenger ved yrkesskade – `lov/par-11-22.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-22.md`)
- § 11-23. Reduksjon ved delvis nedsatt arbeidsevne – `lov/par-11-23.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-23.md`)
- § 11-24. Reduksjon av arbeidsavklaringspenger på grunn av ytelser fra en arbeidsgiver – `lov/par-11-24.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-24.md`)
- § 11-25. Arbeidsavklaringspenger under opphold i institusjon – `lov/par-11-25.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-25.md`)
- § 11-26. Arbeidsavklaringspenger under straffegjennomføring – `lov/par-11-26.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-26.md`)
- § 11-27. Forholdet til andre fulle ytelser fra folketrygden – `lov/par-11-27.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-27.md`)
- § 11-28. Forholdet til andre reduserte ytelser fra folketrygden – `lov/par-11-28.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-28.md`)
- § 11-29. Forholdet til ytelser etter annen lovgivning – `lov/par-11-29.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-29.md`)
- § 11-30. Unntak fra kravet om melding om vedtak og unntak fra kravet om forhåndsvarsel – `lov/par-11-30.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-30.md`)
- § 11-31. Nytt krav om arbeidsavklaringspenger – `lov/par-11-31.md` (rundskriv: `rundskriv/rundskriv-r11-00/par-11-31.md`)

**Kapittel 11 A. Tilleggsstønader til arbeidsrettede tiltak**

- § 11 A-1. Formål – `lov/par-11a-1.md` (rundskriv: `rundskriv/rundskriv-r11a-00/par-11a-1.md`)
- § 11 A-1 a. Forholdet til bestemmelser om internasjonal trygdekoordinering – `lov/par-11a-1a.md`
- § 11 A-2. Alder – `lov/par-11a-2.md` (rundskriv: `rundskriv/rundskriv-r11a-00/par-11a-2.md`)
- § 11 A-3. Nedsatt arbeidsevne – krav til årsakssammenheng – `lov/par-11a-3.md` (rundskriv: `rundskriv/rundskriv-r11a-00/par-11a-3.md`)
- § 11 A-4. Tilleggsstønader til arbeidsrettede tiltak – `lov/par-11a-4.md` (rundskriv: `rundskriv/rundskriv-r11a-00/par-11a-4.md`)
- § 11 A-5. Forholdet til ytelser etter annen lovgivning – `lov/par-11a-5.md` (rundskriv: `rundskriv/rundskriv-r11a-00/par-11a-5.md`)

**Kapittel 12. Uføretrygd**

- § 12-1. Formål – `lov/par-12-1.md` (rundskriv: `rundskriv/rundskriv-r12-00/par-12-1.md`)
- § 12-1 a. Forholdet til bestemmelser om internasjonal trygdekoordinering – `lov/par-12-1a.md` (rundskriv: `rundskriv/rundskriv-r12-00/par-12-1a.md`)
- § 12-2. Forutgående medlemskap – `lov/par-12-2.md` (rundskriv: `rundskriv/rundskriv-r12-00/par-12-2.md`)
- § 12-3. Fortsatt medlemskap – `lov/par-12-3.md` (rundskriv: `rundskriv/rundskriv-r12-00/par-12-3.md`)
- § 12-4. Alder – `lov/par-12-4.md` (rundskriv: `rundskriv/rundskriv-r12-00/par-12-4.md`)
- § 12-5. Hensiktsmessig behandling og arbeidsrettede tiltak – `lov/par-12-5.md` (rundskriv: `rundskriv/rundskriv-r12-00/par-12-5.md`)
- § 12-6. Sykdom, skade eller lyte – krav til årsakssammenheng – `lov/par-12-6.md` (rundskriv: `rundskriv/rundskriv-r12-00/par-12-6.md`)
- § 12-7. Nedsatt inntektsevne – `lov/par-12-7.md` (rundskriv: `rundskriv/rundskriv-r12-00/par-12-7.md`, `rundskriv/rundskriv-r26-00/par-12-7.md`)
- § 12-8. Uføretidspunkt – `lov/par-12-8.md` (rundskriv: `rundskriv/rundskriv-r12-00/par-12-8.md`)
- § 12-9. Fastsetting av inntekt før og etter uførhet – `lov/par-12-9.md` (rundskriv: `rundskriv/rundskriv-r12-00/par-12-9.md`)
- § 12-10. Fastsetting og endring av uføregrad – `lov/par-12-10.md` (rundskriv: `rundskriv/rundskriv-r12-00/par-12-10.md`)
- § 12-11. Grunnlaget for beregning av uføretrygd – `lov/par-12-11.md` (rundskriv: `rundskriv/rundskriv-r12-00/par-12-11.md`)
- § 12-12. Trygdetid – `lov/par-12-12.md` (rundskriv: `rundskriv/rundskriv-r12-00/par-12-12.md`, `rundskriv/rundskriv-r26-00/par-12-12.md`)
- § 12-13. Uføretrygdens størrelse – `lov/par-12-13.md` (rundskriv: `rundskriv/rundskriv-r12-00/par-12-13.md`)
- § 12-14. Reduksjon av uføretrygd på grunn av inntekt – `lov/par-12-14.md` (rundskriv: `rundskriv/rundskriv-r12-00/par-12-14.md`)
- § 12-15. Barnetillegg – `lov/par-12-15.md` (rundskriv: `rundskriv/rundskriv-r12-00/par-12-15.md`)
- § 12-16. Reduksjon av barnetillegg på grunn av inntekt – `lov/par-12-16.md` (rundskriv: `rundskriv/rundskriv-r12-00/par-12-16.md`)
- § 12-17. Uføretrygd ved yrkesskade – `lov/par-12-17.md` (rundskriv: `rundskriv/rundskriv-r12-00/par-12-17.md`)
- § 12-18. Tillegg til uføretrygd for gjenlevende ektefelle (gjenlevendetillegg) – `lov/par-12-18.md` (rundskriv: `rundskriv/rundskriv-r12-00/par-12-18.md`)
- § 12-19. Uføretrygd under opphold i institusjon – `lov/par-12-19.md` (rundskriv: `rundskriv/rundskriv-r12-00/par-12-19.md`)
- § 12-20. Uføretrygd under straffegjennomføring – `lov/par-12-20.md` (rundskriv: `rundskriv/rundskriv-r12-00/par-12-20.md`)
- § 12-21. Avkall på uføretrygd – `lov/par-12-21.md` (rundskriv: `rundskriv/rundskriv-r12-00/par-12-21.md`)

**Kapittel 13. Yrkesskadedekning**

- § 13-1. Formål – `lov/par-13-1.md` (rundskriv: `rundskriv/rundskriv-r13-00/par-13-1.md`)
- § 13-1 a. Forholdet til bestemmelser om internasjonal trygdekoordinering – `lov/par-13-1a.md`
- § 13-2. Særfordeler ved yrkesskade – `lov/par-13-2.md` (rundskriv: `rundskriv/rundskriv-r13-00/par-13-2.md`)
- § 13-3. Yrkesskade – `lov/par-13-3.md` (rundskriv: `rundskriv/rundskriv-r13-00/par-13-3.md`)
- § 13-4. Yrkessykdommer som likestilles med yrkesskade – `lov/par-13-4.md` (rundskriv: `rundskriv/rundskriv-r13-00/par-13-4.md`)
- § 13-5. Skadetidspunktet – `lov/par-13-5.md` (rundskriv: `rundskriv/rundskriv-r13-00/par-13-5.md`)
- § 13-6. Arbeidstakere – `lov/par-13-6.md` (rundskriv: `rundskriv/rundskriv-r13-00/par-13-6.md`, `rundskriv/rundskriv-r26-00/par-13-6.md`)
- § 13-7. Fiskere, lottakere, fangstmenn o.a. – `lov/par-13-7.md` (rundskriv: `rundskriv/rundskriv-r13-00/par-13-7.md`)
- § 13-8. Militærpersoner o.a. – `lov/par-13-8.md` (rundskriv: `rundskriv/rundskriv-r13-00/par-13-8.md`)
- § 13-9. Medlemmer som utfører branntjeneste, redningstjeneste e.l. – `lov/par-13-9.md` (rundskriv: `rundskriv/rundskriv-r13-00/par-13-9.md`)
- § 13-10. Elever, studenter o.a. – `lov/par-13-10.md` (rundskriv: `rundskriv/rundskriv-r13-00/par-13-10.md`)
- § 13-11. Deltakere i arbeidsrettede tiltak – `lov/par-13-11.md` (rundskriv: `rundskriv/rundskriv-r13-00/par-13-11.md`)
- § 13-12. Medlemmer som oppholder seg i institusjon, utfører samfunnsstraff, ungdomsstraff, ungdomsoppfølging eller oppfølging i konfliktråd – `lov/par-13-12.md` (rundskriv: `rundskriv/rundskriv-r13-00/par-13-12.md`)
- § 13-13. Selvstendig næringsdrivende og frilansere – `lov/par-13-13.md` (rundskriv: `rundskriv/rundskriv-r13-00/par-13-13.md`)
- § 13-14. Melding av yrkesskade – `lov/par-13-14.md` (rundskriv: `rundskriv/rundskriv-r13-00/par-13-14.md`)
- § 13-15. Forholdet til krigspensjonslovgivningen – `lov/par-13-15.md` (rundskriv: `rundskriv/rundskriv-r13-00/par-13-15.md`)
- § 13-16. Forholdet til loven om yrkesskadetrygd og de tidligere lovene om ulykkestrygd – `lov/par-13-16.md` (rundskriv: `rundskriv/rundskriv-r13-00/par-13-16.md`)
- § 13-17. Menerstatning ved yrkesskade – `lov/par-13-17.md` (rundskriv: `rundskriv/rundskriv-r13-00/par-13-17.md`)

**Kapittel 14. Ytelser ved svangerskap, fødsel og adopsjon**

- § 14-1. Formål – `lov/par-14-1.md` (rundskriv: `rundskriv/rundskriv-r14-00/par-14-1-2.md`, `rundskriv/rundskriv-r14-00/par-14-1.md`)
- § 14-1 a. Forholdet til bestemmelser om internasjonal trygdekoordinering – `lov/par-14-1a.md` (rundskriv: `rundskriv/rundskriv-r14-00/par-14-1a.md`)
- § 14-2. Medlemskap – `lov/par-14-2.md` (rundskriv: `rundskriv/rundskriv-r14-00/par-14-2-2.md`, `rundskriv/rundskriv-r14-00/par-14-2.md`)
- § 14-3. Arbeidsgiverens plikt til å utbetale ytelser i utlandet – `lov/par-14-3.md` (rundskriv: `rundskriv/rundskriv-r14-00/par-14-3-2.md`, `rundskriv/rundskriv-r14-00/par-14-3.md`)
- § 14-4. Svangerskapspenger – `lov/par-14-4.md` (rundskriv: `rundskriv/rundskriv-r14-00/par-14-4-2.md`, `rundskriv/rundskriv-r14-00/par-14-4.md`)
- § 14-5. Generelle bestemmelser – `lov/par-14-5.md` (rundskriv: `rundskriv/rundskriv-r14-00/par-14-5-2.md`, `rundskriv/rundskriv-r14-00/par-14-5.md`)
- § 14-6. Opptjening av rett til foreldrepenger – `lov/par-14-6.md` (rundskriv: `rundskriv/rundskriv-r14-00/par-14-6-2.md`, `rundskriv/rundskriv-r14-00/par-14-6.md`)
- § 14-7. Beregning av foreldrepenger – `lov/par-14-7.md` (rundskriv: `rundskriv/rundskriv-r14-00/par-14-7-2.md`, `rundskriv/rundskriv-r14-00/par-14-7.md`)
- § 14-8. Feriepenger av foreldrepenger – `lov/par-14-8.md` (rundskriv: `rundskriv/rundskriv-r14-00/par-14-8-2.md`, `rundskriv/rundskriv-r14-00/par-14-8.md`)
- § 14-9. Stønadsperioden for foreldrepenger – `lov/par-14-9.md` (rundskriv: `rundskriv/rundskriv-r14-00/par-14-9-2.md`, `rundskriv/rundskriv-r14-00/par-14-9.md`)
- § 14-10. Generelle bestemmelser om uttak av foreldrepenger – `lov/par-14-10.md` (rundskriv: `rundskriv/rundskriv-r14-00/par-14-10-2.md`, `rundskriv/rundskriv-r14-00/par-14-10.md`)
- § 14-10 a. Utvidet stønadsperiode for foreldrepenger ved prematur fødsel – `lov/par-14-10a.md` (rundskriv: `rundskriv/rundskriv-r14-00/par-14-10a-2.md`, `rundskriv/rundskriv-r14-00/par-14-10a.md`)
- § 14-11. Utsettelse av uttak av foreldrepenger – `lov/par-14-11.md` (rundskriv: `rundskriv/rundskriv-r14-00/par-14-11-2.md`, `rundskriv/rundskriv-r14-00/par-14-11.md`)
- § 14-12. Uttak av kvotene – `lov/par-14-12.md` (rundskriv: `rundskriv/rundskriv-r14-00/par-14-12-2.md`, `rundskriv/rundskriv-r14-00/par-14-12.md`)
- § 14-13. Generelle vilkår for farens uttak av foreldrepenger – `lov/par-14-13.md` (rundskriv: `rundskriv/rundskriv-r14-00/par-14-13-2.md`, `rundskriv/rundskriv-r14-00/par-14-13.md`)
- § 14-14. Særlige regler der bare faren har opptjent rett til foreldrepenger – `lov/par-14-14.md` (rundskriv: `rundskriv/rundskriv-r14-00/par-14-14-2.md`, `rundskriv/rundskriv-r14-00/par-14-14.md`)
- § 14-15. Uttak der mor eller far er alene om omsorgen for barnet og ved samlivsbrudd – `lov/par-14-15.md` (rundskriv: `rundskriv/rundskriv-r14-00/par-14-15-2.md`, `rundskriv/rundskriv-r14-00/par-14-15.md`)
- § 14-16. Gradert uttak av foreldrepenger – `lov/par-14-16.md` (rundskriv: `rundskriv/rundskriv-r14-00/par-14-16-2.md`, `rundskriv/rundskriv-r14-00/par-14-16.md`)
- § 14-17. Engangsstønad – `lov/par-14-17.md` (rundskriv: `rundskriv/rundskriv-r14-00/par-14-17-2.md`, `rundskriv/rundskriv-r14-00/par-14-17.md`)
- § 14-18. Forskrifter – `lov/par-14-18.md` (rundskriv: `rundskriv/rundskriv-r14-00/par-14-18-2.md`, `rundskriv/rundskriv-r14-00/par-14-18.md`)

**Kapittel 15. Stønad til enslig mor eller far**

- § 15-1. Formål – `lov/par-15-1.md` (rundskriv: `rundskriv/rundskriv-r15-00/par-15-1.md`)
- § 15-1 a. Forholdet til bestemmelser om internasjonal trygdekoordinering – `lov/par-15-1a.md`
- § 15-2. Forutgående medlemskap – `lov/par-15-2.md` (rundskriv: `rundskriv/rundskriv-r15-00/par-15-2.md`)
- § 15-3. Oppholdskrav – `lov/par-15-3.md` (rundskriv: `rundskriv/rundskriv-r15-00/par-15-3.md`)
- § 15-4. Enslig mor eller far – `lov/par-15-4.md` (rundskriv: `rundskriv/rundskriv-r15-00/par-15-4.md`)
- § 15-5. Overgangsstønad – `lov/par-15-5.md` (rundskriv: `rundskriv/rundskriv-r15-00/par-15-5.md`)
- § 15-6. (Opphevet) – `lov/par-15-6.md` (rundskriv: `rundskriv/rundskriv-r15-00/par-15-6.md`)
- § 15-7. Overgangsstønadens størrelse – `lov/par-15-7.md` (rundskriv: `rundskriv/rundskriv-r15-00/par-15-7.md`)
- § 15-8. (Opphevet) – `lov/par-15-8.md` (rundskriv: `rundskriv/rundskriv-r15-00/par-15-8.md`)
- § 15-9. Avkorting mot inntekt – `lov/par-15-9.md` (rundskriv: `rundskriv/rundskriv-r15-00/par-15-9.md`)
- § 15-10. Stønad til barnetilsyn til enslig mor eller far som er i arbeid – `lov/par-15-10.md` (rundskriv: `rundskriv/rundskriv-r15-00/par-15-10.md`)
- § 15-11. (Opphevet) – `lov/par-15-11.md` (rundskriv: `rundskriv/rundskriv-r15-00/par-15-11.md`)
- § 15-12. Sanksjonsregler – `lov/par-15-12.md` (rundskriv: `rundskriv/rundskriv-r15-00/par-15-12.md`, `rundskriv/rundskriv-r26-00/par-15-12.md`)
- § 15-13. Forholdet til andre folketrygdytelser m.m. – `lov/par-15-13.md` (rundskriv: `rundskriv/rundskriv-r15-00/par-15-13.md`)

**Kapittel 16. (Opphevet)**

- § 16-1. (Opphevet) – `lov/par-16-1.md` (rundskriv: `rundskriv/rundskriv-r16-00/par-16-1.md`)
- § 16-1 a. (Opphevet) – `lov/par-16-1a.md` (rundskriv: `rundskriv/rundskriv-r16-00/par-16-1a.md`)
- § 16-2. (Opphevet) – `lov/par-16-2.md` (rundskriv: `rundskriv/rundskriv-r16-00/par-16-2.md`)
- § 16-3. (Opphevet) – `lov/par-16-3.md` (rundskriv: `rundskriv/rundskriv-r16-00/par-16-3.md`)
- § 16-4. (Opphevet) – `lov/par-16-4.md` (rundskriv: `rundskriv/rundskriv-r16-00/par-16-4.md`)
- § 16-5. (Opphevet) – `lov/par-16-5.md` (rundskriv: `rundskriv/rundskriv-r16-00/par-16-5.md`)
- § 16-6. (Opphevet) – `lov/par-16-6.md` (rundskriv: `rundskriv/rundskriv-r16-00/par-16-6.md`)
- § 16-7. (Opphevet) – `lov/par-16-7.md` (rundskriv: `rundskriv/rundskriv-r16-00/par-16-7.md`)
- § 16-8. (Opphevet) – `lov/par-16-8.md` (rundskriv: `rundskriv/rundskriv-r16-00/par-16-8.md`, `rundskriv/rundskriv-r26-00/par-16-8.md`)
- § 16-9. (Opphevet) – `lov/par-16-9.md` (rundskriv: `rundskriv/rundskriv-r16-00/par-16-9.md`)
- § 16-10. (Opphevet) – `lov/par-16-10.md` (rundskriv: `rundskriv/rundskriv-r16-00/par-16-10.md`)
- § 16-11. (Opphevet) – `lov/par-16-11.md` (rundskriv: `rundskriv/rundskriv-r16-00/par-16-11.md`)
- § 16-12. (Opphevet) – `lov/par-16-12.md` (rundskriv: `rundskriv/rundskriv-r16-00/par-16-12.md`)

**Kapittel 17. Ytelser til gjenlevende ektefelle og tidligere familiepleier**

- § 17-1. Formål – `lov/par-17-1.md` (rundskriv: `rundskriv/rundskriv-r17-00/par-17-1.md`)
- § 17-1 a. Forholdet til bestemmelser om internasjonal trygdekoordinering – `lov/par-17-1a.md` (rundskriv: `rundskriv/rundskriv-r17-00/par-17-1a.md`)
- § 17-2. Forutgående medlemskap – `lov/par-17-2.md` (rundskriv: `rundskriv/rundskriv-r17-00/par-17-2.md`)
- § 17-3. Fortsatt medlemskap – `lov/par-17-3.md` (rundskriv: `rundskriv/rundskriv-r17-00/par-17-3.md`)
- § 17-4. Øvrige vilkår for ytelser – `lov/par-17-4.md` (rundskriv: `rundskriv/rundskriv-r17-00/par-17-4.md`)
- § 17-5. Omstillingsstønad – `lov/par-17-5.md` (rundskriv: `rundskriv/rundskriv-r17-00/par-17-5.md`)
- § 17-6. Omstillingsstønadens størrelse – `lov/par-17-6.md` (rundskriv: `rundskriv/rundskriv-r17-00/par-17-6.md`)
- § 17-7. Plikt til aktivitet med sikte på å komme i arbeid – `lov/par-17-7.md` (rundskriv: `rundskriv/rundskriv-r17-00/par-17-7.md`)
- § 17-8. Sanksjoner – `lov/par-17-8.md` (rundskriv: `rundskriv/rundskriv-r17-00/par-17-8.md`, `rundskriv/rundskriv-r26-00/par-17-8.md`)
- § 17-9. Reduksjon av ytelse på grunn av inntekt – `lov/par-17-9.md` (rundskriv: `rundskriv/rundskriv-r17-00/par-17-9.md`)
- § 17-10. Stønad til barnetilsyn til gjenlevende i arbeid – `lov/par-17-10.md` (rundskriv: `rundskriv/rundskriv-r17-00/par-17-10.md`)
- § 17-10 a. Tilleggsstønader og stønader til skolepenger m.m. – `lov/par-17-10a.md` (rundskriv: `rundskriv/rundskriv-r17-00/par-17-10a.md`)
- § 17-11. Bortfall av ytelser – `lov/par-17-11.md` (rundskriv: `rundskriv/rundskriv-r17-00/par-17-11.md`)
- § 17-12. Stønad etter dødsfall som skyldes yrkesskade – `lov/par-17-12.md` (rundskriv: `rundskriv/rundskriv-r17-00/par-17-12.md`)
- § 17-13. Ytelser under opphold i institusjon – `lov/par-17-13.md` (rundskriv: `rundskriv/rundskriv-r17-00/par-17-13.md`)
- § 17-14. Ytelser under straffegjennomføring – `lov/par-17-14.md` (rundskriv: `rundskriv/rundskriv-r17-00/par-17-14.md`)
- § 17-15. Ytelser til tidligere familiepleier – `lov/par-17-15.md` (rundskriv: `rundskriv/rundskriv-r17-00/par-17-15.md`)

**Kapittel 17 A. Overgangsregler for gjenlevende ektefelle og tidligere familiepleier som har rett til ytelse med virkning før 1. januar 2024**

- § 17 A-1. Hvem kapitlet gjelder for – `lov/par-17a-1.md`
- § 17 A-1 a. Forholdet til bestemmelser om internasjonal trygdekoordinering – `lov/par-17a-1a.md`
- § 17 A-2. Fortsatt medlemskap – `lov/par-17a-2.md`
- § 17 A-3. Stønadsperiode – `lov/par-17a-3.md`
- § 17 A-4. Omregning av ytelsen – `lov/par-17a-4.md`
- § 17 A-5. Bortfall av pensjon eller overgangsstønad til gjenlevende ektefelle – `lov/par-17a-5.md`
- § 17 A-6. Reduksjon av ytelse på grunn av inntekt – `lov/par-17a-6.md`
- § 17 A-7. Ytelser under opphold i institusjon – `lov/par-17a-7.md`
- § 17 A-8. Ytelser under straffegjennomføring – `lov/par-17a-8.md`

**Kapittel 18. Barnepensjon**

- § 18-1. Formål – `lov/par-18-1.md` (rundskriv: `rundskriv/rundskriv-r18-00/par-18-1.md`)
- § 18-1 a. Forholdet til bestemmelser om internasjonal trygdekoordinering – `lov/par-18-1a.md` (rundskriv: `rundskriv/rundskriv-r18-00/par-18-1a.md`)
- § 18-2. Forutgående medlemskap – `lov/par-18-2.md` (rundskriv: `rundskriv/rundskriv-r18-00/par-18-2.md`)
- § 18-3. Fortsatt medlemskap – `lov/par-18-3.md` (rundskriv: `rundskriv/rundskriv-r18-00/par-18-3.md`)
- § 18-4. Stønadsperioden – `lov/par-18-4.md` (rundskriv: `rundskriv/rundskriv-r18-00/par-18-4.md`)
- § 18-5. Beregning av barnepensjon – `lov/par-18-5.md` (rundskriv: `rundskriv/rundskriv-r18-00/par-18-5.md`)
- § 18-6. Bortfall og reduksjon av barnepensjon ved adopsjon – `lov/par-18-6.md` (rundskriv: `rundskriv/rundskriv-r18-00/par-18-6.md`)
- § 18-7. Forholdet til andre ytelser fra folketrygden – `lov/par-18-7.md` (rundskriv: `rundskriv/rundskriv-r18-00/par-18-7.md`)
- § 18-8. Barnepensjon under opphold i institusjon – `lov/par-18-8.md` (rundskriv: `rundskriv/rundskriv-r18-00/par-18-8.md`)
- § 18-9. Barnepensjon under straffegjennomføring – `lov/par-18-9.md` (rundskriv: `rundskriv/rundskriv-r18-00/par-18-9.md`)
- § 18-10. Barnepensjon etter dødsfall som skyldes yrkesskade – `lov/par-18-10.md` (rundskriv: `rundskriv/rundskriv-r18-00/par-18-10.md`)

**Kapittel 19. Alderspensjon**

- § 19-1. Formål og virkeområde – `lov/par-19-1.md` (rundskriv: `rundskriv/rundskriv-r19-00/par-19-1.md`)
- § 19-1 a. Forholdet til bestemmelser om internasjonal trygdekoordinering – `lov/par-19-1a.md` (rundskriv: `rundskriv/rundskriv-r19-00/par-19-1a.md`)
- § 19-2. Forutgående medlemskap – minste trygdetid – `lov/par-19-2.md` (rundskriv: `rundskriv/rundskriv-r19-00/par-19-2.md`)
- § 19-2 a. Krav til forutgående medlemskap for rett til fastsetting av pensjon etter § 19-16 – `lov/par-19-2a.md` (rundskriv: `rundskriv/rundskriv-r19-00/par-19-2a.md`)
- § 19-3. Fortsatt medlemskap – `lov/par-19-3.md` (rundskriv: `rundskriv/rundskriv-r19-00/par-19-3.md`)
- § 19-3 a. Fortsatt medlemskap ved fastsetting av pensjon etter § 19-16 – `lov/par-19-3a.md` (rundskriv: `rundskriv/rundskriv-r19-00/par-19-3a.md`)
- § 19-4. Alder – `lov/par-19-4.md` (rundskriv: `rundskriv/rundskriv-r19-00/par-19-4.md`)
- § 19-5. Basispensjon – `lov/par-19-5.md` (rundskriv: `rundskriv/rundskriv-r19-00/par-19-5.md`)
- § 19-6. Levealdersjustering og nøytralt uttak – `lov/par-19-6.md` (rundskriv: `rundskriv/rundskriv-r19-00/par-19-6.md`)
- § 19-7. Fastsetting av forholdstall – `lov/par-19-7.md` (rundskriv: `rundskriv/rundskriv-r19-00/par-19-7.md`)
- § 19-8. Minste pensjonsnivå – `lov/par-19-8.md` (rundskriv: `rundskriv/rundskriv-r19-00/par-19-8.md`)
- § 19-9. Pensjonstillegg – `lov/par-19-9.md` (rundskriv: `rundskriv/rundskriv-r19-00/par-19-9.md`)
- § 19-9 a. Overgang fra uføretrygd til alderspensjon for personer født i perioden 1944 til 1962 – `lov/par-19-9a.md` (rundskriv: `rundskriv/rundskriv-r19-00/par-19-9a.md`)
- § 19-10. Uttak av alderspensjon – `lov/par-19-10.md` (rundskriv: `rundskriv/rundskriv-r19-00/par-19-10.md`)
- § 19-11. Vilkår for uttak av alderspensjon før 67 år – `lov/par-19-11.md` (rundskriv: `rundskriv/rundskriv-r19-00/par-19-11.md`)
- § 19-12. Omregning av pensjon ved endring i pensjonsgrad – `lov/par-19-12.md` (rundskriv: `rundskriv/rundskriv-r19-00/par-19-12.md`)
- § 19-13. Omregning av pensjon på grunnlag av opptjening mv. etter pensjonsuttak – `lov/par-19-13.md` (rundskriv: `rundskriv/rundskriv-r19-00/par-19-13.md`)
- § 19-14. Regulering av pensjon under opptjening og utbetaling – `lov/par-19-14.md` (rundskriv: `rundskriv/rundskriv-r19-00/par-19-14.md`)
- § 19-15. Alderspensjon til årskullene 1954–1962 – `lov/par-19-15.md` (rundskriv: `rundskriv/rundskriv-r19-00/par-19-15.md`)
- § 19-16. Alderspensjon til gjenlevende ektefelle – `lov/par-19-16.md` (rundskriv: `rundskriv/rundskriv-r19-00/par-19-16.md`)
- § 19-17. Avkall på alderspensjon – `lov/par-19-17.md` (rundskriv: `rundskriv/rundskriv-r19-00/par-19-17.md`)
- § 19-18. Forholdet til avtalefestet pensjon tilstått før 1. januar 2011 – `lov/par-19-18.md` (rundskriv: `rundskriv/rundskriv-r19-00/par-19-18.md`)
- § 19-19. Ventetillegg – `lov/par-19-19.md` (rundskriv: `rundskriv/rundskriv-r19-00/par-19-19.md`)
- § 19-20. Alderspensjon ved yrkesskade – `lov/par-19-20.md` (rundskriv: `rundskriv/rundskriv-r19-00/par-19-20.md`)
- § 19-21. Alderspensjon under opphold i institusjon – `lov/par-19-21.md` (rundskriv: `rundskriv/rundskriv-r19-00/par-19-21.md`)
- § 19-22. Alderspensjon under straffegjennomføring – `lov/par-19-22.md` (rundskriv: `rundskriv/rundskriv-r19-00/par-19-22.md`)

**Kapittel 20. Ny alderspensjon**

- § 20-1. Formål og virkeområde – `lov/par-20-1.md` (rundskriv: `rundskriv/rundskriv-r20-00/par-20-1.md`)
- § 20-1 a. Forholdet til bestemmelser om internasjonal trygdekoordinering – `lov/par-20-1a.md` (rundskriv: `rundskriv/rundskriv-r20-00/par-20-1a.md`)
- § 20-2. Alder – `lov/par-20-2.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-20-2.md`, `rundskriv/rundskriv-r20-00/par-20-2.md`)
- § 20-3. Sammensetning av alderspensjon – `lov/par-20-3.md` (rundskriv: `rundskriv/rundskriv-r20-00/par-20-3.md`)
- § 20-4. Pensjonsbeholdning – `lov/par-20-4.md` (rundskriv: `rundskriv/rundskriv-r20-00/par-20-4.md`)
- § 20-5. Pensjonsopptjening på grunnlag av pensjonsgivende inntekt – `lov/par-20-5.md` (rundskriv: `rundskriv/rundskriv-r20-00/par-20-5.md`)
- § 20-6. Pensjonsopptjening ved avtjening av førstegangstjeneste – `lov/par-20-6.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-20-6.md`, `rundskriv/rundskriv-r20-00/par-20-6.md`)
- § 20-7. Pensjonsopptjening for dagpengemottakere – `lov/par-20-7.md` (rundskriv: `rundskriv/rundskriv-r20-00/par-20-7.md`)
- § 20-7 a. Pensjonsopptjening for mottakere av uføretrygd – `lov/par-20-7a.md` (rundskriv: `rundskriv/rundskriv-r20-00/par-20-7a.md`)
- § 20-8. Pensjonsopptjening ved omsorgsarbeid – `lov/par-20-8.md` (rundskriv: `rundskriv/rundskriv-r20-00/par-20-8.md`)
- § 20-9. Garantipensjon – satser – `lov/par-20-9.md` (rundskriv: `rundskriv/rundskriv-r20-00/par-20-9.md`)
- § 20-10. Garantipensjon – trygdetid – `lov/par-20-10.md` (rundskriv: `rundskriv/rundskriv-r20-00/par-20-10.md`)
- § 20-11. Garantipensjon – beholdning – `lov/par-20-11.md` (rundskriv: `rundskriv/rundskriv-r20-00/par-20-11.md`)
- § 20-12. Levealdersjustering og nøytralt uttak – `lov/par-20-12.md` (rundskriv: `rundskriv/rundskriv-r20-00/par-20-12.md`)
- § 20-13. Fastsetting av delingstall – `lov/par-20-13.md` (rundskriv: `rundskriv/rundskriv-r20-00/par-20-13.md`)
- § 20-14. Uttak av alderspensjon – `lov/par-20-14.md` (rundskriv: `rundskriv/rundskriv-r20-00/par-20-14.md`)
- § 20-15. Vilkår for uttak av alderspensjon før 67 år – `lov/par-20-15.md` (rundskriv: `rundskriv/rundskriv-r20-00/par-20-15.md`)
- § 20-16. Omregning av pensjon ved endring i pensjonsgrad – `lov/par-20-16.md` (rundskriv: `rundskriv/rundskriv-r20-00/par-20-16.md`)
- § 20-17. Omregning av pensjon på grunnlag av opptjening mv. etter pensjonsuttak – `lov/par-20-17.md` (rundskriv: `rundskriv/rundskriv-r20-00/par-20-17.md`)
- § 20-18. Regulering av pensjonsbeholdning og pensjoner – `lov/par-20-18.md` (rundskriv: `rundskriv/rundskriv-r20-00/par-20-18.md`)
- § 20-19. Alderspensjon til årskullene 1954–1962 – `lov/par-20-19.md` (rundskriv: `rundskriv/rundskriv-r20-00/par-20-19.md`)
- § 20-19 a. Gjenlevendetillegg til årskullene 1954–1957 ved uttak av alderspensjon til og med 2019 – `lov/par-20-19a.md` (rundskriv: `rundskriv/rundskriv-r20-00/par-20-19a-2.md`, `rundskriv/rundskriv-r20-00/par-20-19a.md`)
- § 20-20. Garanti for opptjente rettigheter – `lov/par-20-20.md` (rundskriv: `rundskriv/rundskriv-r20-00/par-20-20.md`)
- § 20-21. Pensjon opptjent før 1. januar 2010 – `lov/par-20-21.md` (rundskriv: `rundskriv/rundskriv-r20-00/par-20-21.md`)
- § 20-22. Alderspensjon under opphold i institusjon – `lov/par-20-22.md` (rundskriv: `rundskriv/rundskriv-r20-00/par-20-22.md`)
- § 20-23. Alderspensjon under straffegjennomføring – `lov/par-20-23.md` (rundskriv: `rundskriv/rundskriv-r20-00/par-20-23.md`)

**Kapittel 21. Saksbehandling i trygdesaker. Anke- og klagebehandling m.m.**

- § 21-1. Forholdet til forvaltningsloven – `lov/par-21-1.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-21-1.md`, `rundskriv/rundskriv-r21-00/par-21-1.md`, `rundskriv/rundskriv-r21-00b/par-21-1.md`)
- § 21-1 a. Forholdet til bestemmelser om internasjonal trygdekoordinering – `lov/par-21-1a.md`
- § 21-2. Hvor kravet skal settes fram – `lov/par-21-2.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-21-2.md`, `rundskriv/rundskriv-r21-00/par-21-2.md`, `rundskriv/rundskriv-r21-00b/par-21-2.md`)
- § 21-3. Medlemmets opplysningsplikt – `lov/par-21-3.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-21-3.md`, `rundskriv/rundskriv-r21-00/par-21-3.md`, `rundskriv/rundskriv-r21-00b/par-21-3.md`)
- § 21-4. Innhenting av opplysninger og uttalelser – `lov/par-21-4.md` (rundskriv: `rundskriv/rundskriv-r21-00/par-21-4.md`, `rundskriv/rundskriv-r21-00b/par-21-4.md`)
- § 21-4 a. Innhenting av opplysninger fra tredjemann – stedlig kontroll – `lov/par-21-4a.md` (rundskriv: `rundskriv/rundskriv-r21-00/par-21-4a-2.md`, `rundskriv/rundskriv-r21-00/par-21-4a.md`, `rundskriv/rundskriv-r21-00b/par-21-4a.md`)
- § 21-4 b. Utveksling av opplysninger med finansinstitusjoner – `lov/par-21-4b.md` (rundskriv: `rundskriv/rundskriv-r21-00/par-21-4b.md`)
- § 21-4 c. Nærmere om innhenting av opplysninger – `lov/par-21-4c.md` (rundskriv: `rundskriv/rundskriv-r21-00/par-21-4c.md`, `rundskriv/rundskriv-r21-00b/par-21-4c.md`)
- § 21-4 d. Masseinnhenting av opplysninger i kontrolløyemed – `lov/par-21-4d.md` (rundskriv: `rundskriv/rundskriv-r21-00/par-21-4d.md`)
- § 21-5. Bistand fra barnevernstjenesten, den kommunale helse- og omsorgstjenesten, sosialtjenesten og kommunale organer etter introduksjonsloven – `lov/par-21-5.md`
- § 21-6. Endrede forhold – `lov/par-21-6.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-21-6.md`, `rundskriv/rundskriv-r21-00/par-21-6.md`)
- § 21-7. Uriktige opplysninger m.m. – følger for ytelser fra trygden – `lov/par-21-7.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-21-7.md`, `rundskriv/rundskriv-r21-00/par-21-7.md`, `rundskriv/rundskriv-r21-00b/par-21-7.md`)
- § 21-8. Bortfall av rett til ytelser når mottakeren er skjødesløs med sin helse m.m. – `lov/par-21-8.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-21-8.md`, `rundskriv/rundskriv-r21-00/par-21-8.md`)
- § 21-9. (Opphevet) – `lov/par-21-9.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-21-9.md`, `rundskriv/rundskriv-r21-00/par-21-9.md`)
- § 21-10. Saksbehandlingstid og underretning om vedtak – `lov/par-21-10.md` (rundskriv: `rundskriv/rundskriv-r21-00/par-21-10.md`)
- § 21-11. Vedtak etter loven – `lov/par-21-11.md` (rundskriv: `rundskriv/rundskriv-r21-00/par-21-11.md`, `rundskriv/rundskriv-r21-00b/par-21-11.md`)
- § 21-11 a. Saksbehandling m.m. etter kapittel 5 Stønad ved helsetjenester – `lov/par-21-11a.md` (rundskriv: `rundskriv/rundskriv-r21-00b/par-21-11a-2.md`, `rundskriv/rundskriv-r21-00b/par-21-11a.md`)
- § 21-11 b. Saksbehandling m.m. i saker etter kapittel 21, 22 og 25 med tilknytning til ytelser etter kapittel 5 Stønad ved helsetjenester – `lov/par-21-11b.md`
- § 21-12. Klage og anke i trygdesaker – `lov/par-21-12.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-21-12.md`, `rundskriv/rundskriv-r21-00/par-21-12.md`, `rundskriv/rundskriv-r21-00b/par-21-12.md`)
- § 21-12A. (Opphevet) – `lov/par-21-12a.md`
- § 21-13. Ankenemnda for sykepenger i arbeidsgiverperioden – `lov/par-21-13.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-21-13.md`, `rundskriv/rundskriv-r21-00/par-21-13.md`)
- § 21-14. (Opphevet) – `lov/par-21-14.md` (rundskriv: `rundskriv/rundskriv-r21-00/par-21-14.md`)
- § 21-15. Dagpenger under arbeidsløshet for fiskere og fangstmenn – `lov/par-21-15.md` (rundskriv: `rundskriv/rundskriv-r21-00/par-21-15.md`)
- § 21-16. Saksbehandling i avgiftssaker m.m. – `lov/par-21-16.md`
- § 21-17. Forskrifter – `lov/par-21-17.md` (rundskriv: `rundskriv/rundskriv-r21-00/par-21-17.md`)

**Kapittel 22. Utbetaling**

- § 22-1. Hovedregel om hvem ytelsen skal utbetales til – `lov/par-22-1.md` (rundskriv: `rundskriv/rundskriv-r22-00/par-22-1.md`)
- § 22-1 a. Forholdet til bestemmelser om internasjonal trygdekoordinering – `lov/par-22-1a.md` (rundskriv: `rundskriv/rundskriv-r22-00/par-22-1a.md`)
- § 22-2. Utbetaling ved direkte oppgjør – `lov/par-22-2.md` (rundskriv: `rundskriv/rundskriv-r22-00/par-22-2.md`)
- § 22-2 a. Plikt til direkte oppgjør – `lov/par-22-2a.md` (rundskriv: `rundskriv/rundskriv-r22-00/par-22-2a.md`)
- § 22-3. Utbetaling til arbeidsgiver – `lov/par-22-3.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-22-3.md`, `rundskriv/rundskriv-r22-00/par-22-3.md`)
- § 22-3a. Barnetillegg til bidragspliktige – `lov/par-22-3a.md` (rundskriv: `rundskriv/rundskriv-r22-00/par-22-3a.md`)
- § 22-3b. Ytelser til barn i fosterhjem – `lov/par-22-3b.md` (rundskriv: `rundskriv/rundskriv-r22-00/par-22-3b.md`)
- § 22-4. Disponering av ytelser til langtidspasienter i helseinstitusjon – `lov/par-22-4.md` (rundskriv: `rundskriv/rundskriv-r22-00/par-22-4.md`)
- § 22-5. Felles trivselsordninger for langtidspasienter – `lov/par-22-5.md` (rundskriv: `rundskriv/rundskriv-r22-00/par-22-5.md`)
- § 22-6. Utbetaling til Nav-kontor o.a. – `lov/par-22-6.md` (rundskriv: `rundskriv/rundskriv-r22-00/par-22-6.md`)
- § 22-7. Utsatt utbetaling – `lov/par-22-7.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-22-7.md`, `rundskriv/rundskriv-r22-00/par-22-7.md`)
- § 22-8. Fradrag ved etterbetaling av pensjon o.l. – `lov/par-22-8.md` (rundskriv: `rundskriv/rundskriv-r22-00/par-22-8.md`)
- § 22-9. (Opphevet) – `lov/par-22-9.md`
- § 22-10. Utbetalingsterminer – `lov/par-22-10.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-22-10.md`, `rundskriv/rundskriv-r22-00/par-22-10.md`)
- § 22-11. Avrunding av ytelser – `lov/par-22-11.md` (rundskriv: `rundskriv/rundskriv-r22-00/par-22-11.md`)
- § 22-12. Tidspunkt for utbetaling når rett til en ytelse oppstår eller opphører – `lov/par-22-12.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-22-12.md`, `rundskriv/rundskriv-r22-00/par-22-12.md`)
- § 22-13. Frister for framsetting av krav, virkningstidspunkt og etterbetaling – `lov/par-22-13.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-22-13.md`, `rundskriv/rundskriv-r22-00/par-22-13.md`)
- § 22-14. Foreldelse – `lov/par-22-14.md` (rundskriv: `rundskriv/rundskriv-r22-00/par-22-14.md`)
- § 22-15. Tilbakekreving etter feilaktig utbetaling – `lov/par-22-15.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-22-15.md`, `rundskriv/rundskriv-r22-00/par-22-15.md`)
- § 22-15 a. Tilbakekreving av utbetalinger etter direkte oppgjørsordning – `lov/par-22-15a.md` (rundskriv: `rundskriv/rundskriv-r22-00/par-22-15a.md`)
- § 22-16. Avregning av feilutbetalinger som skyldes for høy inntekt – `lov/par-22-16.md` (rundskriv: `rundskriv/rundskriv-r22-00/par-22-16.md`)
- § 22-17. Renter ved etterbetaling av ytelser – `lov/par-22-17.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-22-17.md`, `rundskriv/rundskriv-r22-00/par-22-17.md`)
- § 22-17 a. Renter og rentetillegg ved tilbakekreving av feilutbetalinger – `lov/par-22-17a.md` (rundskriv: `rundskriv/rundskriv-r22-00/par-22-17a.md`)
- § 22-17 b. Forholdet til erstatning – `lov/par-22-17b.md` (rundskriv: `rundskriv/rundskriv-r22-00/par-22-17b.md`)
- § 22-18. Utbetalingsmåten for ytelser m.m. – `lov/par-22-18.md`
- § 22-19. Utbetaling av små beløp – `lov/par-22-19.md`

**Kapittel 23. Finansiering**

- § 23-1. Folketrygdens utgifter – `lov/par-23-1.md` (rundskriv: `rundskriv/rundskriv-r23-00/par-23-1.md`)
- § 23-2. Arbeidsgiveravgift – `lov/par-23-2.md`
- § 23-2 a. Finansskatt på lønn – `lov/par-23-2a.md`
- § 23-3. Trygdeavgift – `lov/par-23-3.md` (rundskriv: `rundskriv/rundskriv-r23-00/par-23-3.md`)
- § 23-4. Avgifter for visse grupper – `lov/par-23-4.md` (rundskriv: `rundskriv/rundskriv-r23-00/par-23-4.md`)
- § 23-4 a. Avgifter for personer som er omfattet av norsk trygdelovgivning etter trygdeavtale mv. – `lov/par-23-4a.md`
- § 23-5. Produktavgift ved fiske m.m. – `lov/par-23-5.md` (rundskriv: `rundskriv/rundskriv-r23-00/par-23-5.md`)
- § 23-6. Premie for frivillig forsikring for sykepenger og frivillig yrkesskadetrygd – `lov/par-23-6.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-23-6.md`, `rundskriv/rundskriv-r23-00/par-23-6.md`)
- § 23-7. Refusjon av trygdeutgifter ved trafikkskade – `lov/par-23-7.md` (rundskriv: `rundskriv/rundskriv-r23-00/par-23-7.md`)
- § 23-8. Refusjon av trygdeutgifter ved yrkesskade – `lov/par-23-8.md` (rundskriv: `rundskriv/rundskriv-r23-00/par-23-8.md`)
- § 23-9. (Opphevet) – `lov/par-23-9.md` (rundskriv: `rundskriv/rundskriv-r23-00/par-23-9.md`)
- § 23-10. Tilskott fra staten – `lov/par-23-10.md` (rundskriv: `rundskriv/rundskriv-r23-00/par-23-10.md`)
- § 23-11. Folketrygdens midler – `lov/par-23-11.md` (rundskriv: `rundskriv/rundskriv-r23-00/par-23-11.md`)

**Kapittel 24. Saksbehandling i avgiftssaker m.m.**

- § 24-1. Skatteetatens og Arbeids- og velferdsetatens oppgaver – `lov/par-24-1.md` (rundskriv: `rundskriv/rundskriv-r24-00/par-24-1.md`)
- § 24-2. (Opphevet) – `lov/par-24-2.md`
- § 24-3. (Opphevet) – `lov/par-24-3.md`
- § 24-4. (Opphevet) – `lov/par-24-4.md`
- § 24-4 a. (Opphevet) – `lov/par-24-4a.md`
- § 24-5. Forskrifter – `lov/par-24-5.md` (rundskriv: `rundskriv/rundskriv-r24-00/par-24-5.md`)

**Kapittel 25. Forskjellige bestemmelser**

- § 25-1. Arbeidsgiver- og arbeidstakerregisteret – `lov/par-25-1.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-25-1.md`, `rundskriv/rundskriv-r25-00/par-25-1.md`)
- § 25-2. Arbeidsgiverens plikt til å føre statistikk over sykefravær, utarbeide oppfølgingsplan og gjennomføre dialogmøte – `lov/par-25-2.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-25-2.md`, `rundskriv/rundskriv-r25-00/par-25-2.md`)
- § 25-3. Overtredelsesgebyr og tvangsmulkt ved brudd på meldeplikten til Arbeidsgiver- og arbeidstakerregisteret mv. – `lov/par-25-3.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-25-3.md`, `rundskriv/rundskriv-r25-00/par-25-3.md`)
- § 25-3 a. (Opphevet) – `lov/par-25-3a.md`
- § 25-4. Særskilt meldeplikt for samboere – `lov/par-25-4.md` (rundskriv: `rundskriv/rundskriv-r25-00/par-25-4.md`)
- § 25-5. Behandleres plikt til å delta i samarbeidsmøter – `lov/par-25-5.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-25-5.md`, `rundskriv/rundskriv-r25-00/par-25-5.md`)
- § 25-5 a. (Opphevet) – `lov/par-25-5a.md`
- § 25-6. Tap av retten til å praktisere for trygdens regning (Helsedirektoratets myndighet) – `lov/par-25-6.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-25-6.md`, `rundskriv/rundskriv-r25-00/par-25-6.md`)
- § 25-6 a. Overtredelsesgebyr – `lov/par-25-6a.md` (rundskriv: `rundskriv/rundskriv-r25-00/par-25-6a.md`)
- § 25-7. Tap av retten til å praktisere for trygdens regning (Arbeids- og velferdsdirektoratets myndighet) – `lov/par-25-7.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-25-7.md`, `rundskriv/rundskriv-r25-00/par-25-7.md`)
- § 25-7 a. Formell advarsel – `lov/par-25-7a.md` (rundskriv: `rundskriv/rundskriv-r25-00/par-25-7a.md`)
- § 25-8. Tilbakekreving av dokumenter som er utlånt – `lov/par-25-8.md` (rundskriv: `rundskriv/rundskriv-r25-00/par-25-8.md`)
- § 25-9. Arbeids- og velferdsetatens opplysningsplikt om forventet arbeidsinntekt – `lov/par-25-9.md` (rundskriv: `rundskriv/rundskriv-r25-00/par-25-9.md`)
- § 25-10. Arbeidsgivers og oppdragsgivers opplysningsplikt – `lov/par-25-10.md` (rundskriv: `rundskriv/rundskriv-r25-00/par-25-10.md`)
- § 25-10a. (Opphevet) – `lov/par-25-10a.md`
- § 25-11. Opplysningsplikt til barnevernet – `lov/par-25-11.md` (rundskriv: `rundskriv/rundskriv-r25-00/par-25-11.md`)
- § 25-12. Straff for å gi uriktige opplysninger og for ikke å gi nødvendige opplysninger – `lov/par-25-12.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-25-12.md`, `rundskriv/rundskriv-r25-00/par-25-12.md`)
- § 25-13. Forsøksvirksomhet – avvik fra loven – `lov/par-25-13.md` (rundskriv: `rundskriv/rundskriv-r08-00/par-25-13.md`, `rundskriv/rundskriv-r25-00/par-25-13.md`, `rundskriv/rundskriv-r26-00/par-25-13.md`)
- § 25-14. Forholdet til framtidig lovgivning – `lov/par-25-14.md` (rundskriv: `rundskriv/rundskriv-r25-00/par-25-14.md`)
- § 25-15. Forskrifter – `lov/par-25-15.md` (rundskriv: `rundskriv/rundskriv-r25-00/par-25-15.md`)
- § 25-16. Forskrifter ved allmennfarlig smittsom sykdom – `lov/par-25-16.md`
- § 25-17. Unntak fra loven ved krise i freds- og krigstid – `lov/par-25-17.md`
- § 25-18. (Opphevet) – `lov/par-25-18.md`
- § 25-19. (Opphevet) – `lov/par-25-19.md`

**Kapittel 26. Ikrafttredelse og overgangsbestemmelser. Endringer i andre lover**

- § 26-1. Ikrafttredelse – `lov/par-26-1.md` (rundskriv: `rundskriv/rundskriv-r26-00/par-26-1.md`)
- § 26-2. Overgangsbestemmelser – `lov/par-26-2.md` (rundskriv: `rundskriv/rundskriv-r26-00/par-26-2.md`)
- § 26-3. Endringer i andre lover – `lov/par-26-3.md` (rundskriv: `rundskriv/rundskriv-r26-00/par-26-3.md`)

**Innhold utenfor paragrafene**

- Vedlegg, tabeller o.l. – `lov/utenfor-paragrafene.md`

### Forskrift om beregning av arbeidsavklaringspenger etter EØS-avtalen

- § 1. Virkeområde – `forskrifter/eos-beregning-arbeidsavklaringspenger/par-1.md`
- § 2. Arbeidsperioder i andre medlemsland – `forskrifter/eos-beregning-arbeidsavklaringspenger/par-2.md`
- § 3. Beregnet inntekt for arbeidsperioder i andre medlemsland – `forskrifter/eos-beregning-arbeidsavklaringspenger/par-3.md`
- § 4. Grunnlaget for inntektsavhengige ytelser – `forskrifter/eos-beregning-arbeidsavklaringspenger/par-4.md`
- § 5. (Opphevet) – `forskrifter/eos-beregning-arbeidsavklaringspenger/par-5.md`
- § 6. Ikrafttredelse – `forskrifter/eos-beregning-arbeidsavklaringspenger/par-6.md`

### Forskrift om alderspensjon i folketrygden

**Kapittel 1. Innledende bestemmelser**

- § 1-1. Virkeområde – `forskrifter/alderspensjon-i-folketrygden/par-1-1.md`
- § 1-2. Definisjoner – `forskrifter/alderspensjon-i-folketrygden/par-1-2.md`

**Kapittel 2. Pensjonsopptjening ved avtjening av førstegangstjeneste, pensjonsopptjening for dagpengemottakere og pensjonsopptjening for mottakere av uføretrygd ved yrkesskade**

- § 2-1. Virkeområde – `forskrifter/alderspensjon-i-folketrygden/par-2-1.md`
- § 2-2. Førstegangstjeneste – `forskrifter/alderspensjon-i-folketrygden/par-2-2.md`
- § 2-3. Pensjonsopptjening for førstegangstjeneste – `forskrifter/alderspensjon-i-folketrygden/par-2-3.md`
- § 2-4. Krav til sammenhengende tjeneste – `forskrifter/alderspensjon-i-folketrygden/par-2-4.md`
- § 2-5. Fastsetting av inntekt for pensjonsopptjeningen etter folketrygdloven § 20-7 – `forskrifter/alderspensjon-i-folketrygden/par-2-5.md`
- § 2-6. Pensjonsopptjening for fiskere og fangstmenn som mottar arbeidsledighetstrygd i fiske – `forskrifter/alderspensjon-i-folketrygden/par-2-6.md`
- § 2-7. Pensjonsopptjening for mottakere av uføretrygd når uførheten helt eller delvis skyldes yrkesskade – `forskrifter/alderspensjon-i-folketrygden/par-2-7.md`

**Kapittel 3. Pensjonsopptjening ved omsorgsarbeid**

- § 3-1. Virkeområde – `forskrifter/alderspensjon-i-folketrygden/par-3-1.md`
- § 3-2. Omsorgsopptjening – `forskrifter/alderspensjon-i-folketrygden/par-3-2.md`
- § 3-3. Omsorgsyter – `forskrifter/alderspensjon-i-folketrygden/par-3-3.md`
- § 3-4. Tildeling av omsorgsopptjening – `forskrifter/alderspensjon-i-folketrygden/par-3-4.md`
- § 3-5. Overføring av omsorgsopptjeningen mellom omsorgsyterne – `forskrifter/alderspensjon-i-folketrygden/par-3-5.md`
- § 3-6. Omsorgsarbeidets omfang – `forskrifter/alderspensjon-i-folketrygden/par-3-6.md`
- § 3-7. Omsorgsarbeid for flere personer – `forskrifter/alderspensjon-i-folketrygden/par-3-7.md`
- § 3-8. Flere utøver omsorgsarbeid for samme person – `forskrifter/alderspensjon-i-folketrygden/par-3-8.md`
- § 3-9. Avgrensing mot omsorgsarbeid utført av personer i omsorgsyrker – `forskrifter/alderspensjon-i-folketrygden/par-3-9.md`
- § 3-10. Framsetting av krav om omsorgsopptjening – `forskrifter/alderspensjon-i-folketrygden/par-3-10.md`
- § 3-11. Forhøyet hjelpestønad – `forskrifter/alderspensjon-i-folketrygden/par-3-11.md`
- § 3-12. Attestasjon – `forskrifter/alderspensjon-i-folketrygden/par-3-12.md`
- § 3-13. Pleieforhold som strekker seg over flere kalenderår – `forskrifter/alderspensjon-i-folketrygden/par-3-13.md`

**Kapittel 4. Levealdersjustering. Beregning og fastsetting av forholdstall og delingstall. Fastsetting av skjermingstillegg for mottakere av uføretrygd ved overgang til alderspensjon**

- § 4-1. Virkeområde – `forskrifter/alderspensjon-i-folketrygden/par-4-1.md`
- § 4-2. Tidspunkt for fastsetting av forholdstall og delingstall – `forskrifter/alderspensjon-i-folketrygden/par-4-2.md`
- § 4-3. Dødelighet og forventet gjenstående levetid – `forskrifter/alderspensjon-i-folketrygden/par-4-3.md`
- § 4-4. Delingstall – `forskrifter/alderspensjon-i-folketrygden/par-4-4.md`
- § 4-5. Forholdstall – `forskrifter/alderspensjon-i-folketrygden/par-4-5.md`
- § 4-6. Gradvis innfasing av levealdersjusteringen – `forskrifter/alderspensjon-i-folketrygden/par-4-6.md`
- § 4-7. Fastsetting av skjermingstillegg – folketrygdloven § 19-9a – `forskrifter/alderspensjon-i-folketrygden/par-4-7.md`

**Kapittel 5. Beregning av særtillegg og minste samlede pensjonsnivå for pensjonistpar**

- § 5-1. Virkeområde – `forskrifter/alderspensjon-i-folketrygden/par-5-1.md`
- § 5-2. Beregning av særtillegg for pensjonistpar som mottar alderspensjon eller avtalefestet pensjon – `forskrifter/alderspensjon-i-folketrygden/par-5-2.md`
- § 5-3. Virkeområde – `forskrifter/alderspensjon-i-folketrygden/par-5-3.md`
- § 5-4. Beregning av minste pensjonsnivå og tillegg til pensjonen – `forskrifter/alderspensjon-i-folketrygden/par-5-4.md`
- § 5-5. Samlet pensjon – `forskrifter/alderspensjon-i-folketrygden/par-5-5.md`
- § 5-6. Omregning, nytt tillegg og bortfall av tillegg – `forskrifter/alderspensjon-i-folketrygden/par-5-6.md`
- § 5-7. Virkeområde – `forskrifter/alderspensjon-i-folketrygden/par-5-7.md`
- § 5-8. Beregning av minste pensjonsnivå og tillegg til pensjonen – `forskrifter/alderspensjon-i-folketrygden/par-5-8.md`
- § 5-9. Samlet pensjon – `forskrifter/alderspensjon-i-folketrygden/par-5-9.md`
- § 5-10. Omregning og bortfall av tillegg – `forskrifter/alderspensjon-i-folketrygden/par-5-10.md`

**Kapittel 6. Omregning av pensjonen på grunnlag av opptjening mv. etter pensjonsuttak**

- § 6-1. Virkeområde – `forskrifter/alderspensjon-i-folketrygden/par-6-1.md`
- § 6-2. Negative størrelser ved omregning etter folketrygdloven § 19-13 – `forskrifter/alderspensjon-i-folketrygden/par-6-2.md`
- § 6-3. Omregning ved negativt restpensjonstillegg ved gradert uttak – `forskrifter/alderspensjon-i-folketrygden/par-6-3.md`
- § 6-4. Omregning av pensjon ved endring i sivilstand mv. etter uttak – `forskrifter/alderspensjon-i-folketrygden/par-6-4.md`
- § 6-5. Omregning av pensjon ved endring i medlemskap etter uttak – `forskrifter/alderspensjon-i-folketrygden/par-6-5.md`
- § 6-6. Beregning og omregning av pensjon for personer født i årene 1944 til 1948 som ble tilstått avtalefestet pensjon før 2011 – `forskrifter/alderspensjon-i-folketrygden/par-6-6.md`
- § 6-7. Beregning og omregning av pensjon ved yrkesskade – `forskrifter/alderspensjon-i-folketrygden/par-6-7.md`
- § 6-8. Negative størrelser ved omregning etter folketrygdloven § 20-17 – `forskrifter/alderspensjon-i-folketrygden/par-6-8.md`
- § 6-9. Omregning ved negativ garantipensjonsbeholdning ved gradert uttak – `forskrifter/alderspensjon-i-folketrygden/par-6-9.md`
- § 6-10. Omregning av garantipensjon ved endring i sivilstand mv. etter uttak – `forskrifter/alderspensjon-i-folketrygden/par-6-10.md`

**Kapittel 7. (Opphevet)**

- § 7-1. (Opphevet) – `forskrifter/alderspensjon-i-folketrygden/par-7-1.md`
- § 7-2. (Opphevet) – `forskrifter/alderspensjon-i-folketrygden/par-7-2.md`

**Kapittel 8. Regulering av pensjon ved endring av pensjonsgrad**

- § 8-1. Virkeområde – `forskrifter/alderspensjon-i-folketrygden/par-8-1.md`
- § 8-2. Endring av pensjonsgrad – `forskrifter/alderspensjon-i-folketrygden/par-8-2.md`
- § 8-3. Regulering av restpensjon, pensjonsbeholdning og garantipensjonsbeholdning etter endring av pensjonsgrad – `forskrifter/alderspensjon-i-folketrygden/par-8-3.md`
- § 8-4. Regulering av pensjon under utbetaling etter endring av pensjonsgrad – `forskrifter/alderspensjon-i-folketrygden/par-8-4.md`

**Kapittel 9. Garanti for opptjente rettigheter pr. 31. desember 2009**

- § 9-1. Virkeområde – `forskrifter/alderspensjon-i-folketrygden/par-9-1.md`
- § 9-2. Fastsetting av garantert opptjening – `forskrifter/alderspensjon-i-folketrygden/par-9-2.md`
- § 9-3. Levealdersjustering av opptjente rettigheter – `forskrifter/alderspensjon-i-folketrygden/par-9-3.md`
- § 9-4. Beregning av garantitillegg – `forskrifter/alderspensjon-i-folketrygden/par-9-4.md`
- § 9-5. Endringer i pensjon etter fylte 67 år – `forskrifter/alderspensjon-i-folketrygden/par-9-5.md`

**Kapittel 10. Fastsetting av pensjonsbeholdning for pensjonsgivende inntekt og pensjonspoeng mv. opptjent før 1. januar 2010**

- § 10-1. Virkeområde – `forskrifter/alderspensjon-i-folketrygden/par-10-1.md`
- § 10-2. Pensjonsopptjening for omsorgsarbeid – `forskrifter/alderspensjon-i-folketrygden/par-10-2.md`
- § 10-3. Inntekter som ikke er ferdig lignet pr. 1. januar 2010 – `forskrifter/alderspensjon-i-folketrygden/par-10-3.md`
- § 10-4. Tildeling av pensjonsopptjening for omsorgsarbeid for små barn for år før 1992 – `forskrifter/alderspensjon-i-folketrygden/par-10-4.md`
- § 10-5. Overføring av pensjonsopptjening for omsorgsarbeid mellom omsorgsyterne – `forskrifter/alderspensjon-i-folketrygden/par-10-5.md`

**Kapittel 10A. Alderspensjon til gjenlevende ektefelle ved ny opptjening, endret uttaksgrad og endring i sivilstand. Beregning av minste pensjonsnivå**

- § 10A-1. Virkeområde – `forskrifter/alderspensjon-i-folketrygden/par-10a-1.md`
- § 10A-2. Gjenlevendefordel – `forskrifter/alderspensjon-i-folketrygden/par-10a-2.md`
- § 10A-3. Økt opptjening, trygdetid og endring i sivilstand – `forskrifter/alderspensjon-i-folketrygden/par-10a-3.md`
- § 10A-4. Endret uttaksgrad – `forskrifter/alderspensjon-i-folketrygden/par-10a-4.md`
- § 10A-5. Samlet pensjon skal minst utgjøre minste pensjonsnivå – `forskrifter/alderspensjon-i-folketrygden/par-10a-5.md`

**Kapittel 11. Overgangsbestemmelser**

- § 11-1. Virkeområde – `forskrifter/alderspensjon-i-folketrygden/par-11-1.md`
- § 11-2. Restpensjon pr. 1. januar 2011 for personer født i 1943 som tar ut og stanser eller gir avkall på pensjon i 2010 – `forskrifter/alderspensjon-i-folketrygden/par-11-2.md`
- § 11-3. Omregning av pensjon pr. 1. januar 2011 for visse grupper personer født i 1943 som mottok pensjon pr. 31. desember 2010 – `forskrifter/alderspensjon-i-folketrygden/par-11-3.md`
- § 11-4. Omregning av pensjon for personer født i 1943 som mottok pensjon pr. 31. desember 2010 ved endring i pensjonsgrad eller økt opptjening etter uttak – `forskrifter/alderspensjon-i-folketrygden/par-11-4.md`
- § 11-5. Omregning av pensjon for personer født i 1943 som mottok pensjon pr. 31. desember 2010 ved endring i sivilstand mv. etter uttak – `forskrifter/alderspensjon-i-folketrygden/par-11-5.md`
- § 11-6. Omregning av pensjon for personer født i 1943 som mottok pensjon pr. 31. desember 2010 ved endring i medlemskap etter uttak – `forskrifter/alderspensjon-i-folketrygden/par-11-6.md`
- § 11-6a. Omregning av pensjon pr. 1. september 2016 for personer født i 1943 som mottok pensjon pr. 31. desember 2010 – `forskrifter/alderspensjon-i-folketrygden/par-11-6a.md`
- § 11-7. Omregning av pensjon for personer født til og med 1942 ved økt opptjening og endring i sivilstand mv. etter uttak – `forskrifter/alderspensjon-i-folketrygden/par-11-7.md`
- § 11-8. Omregning av pensjon for personer født til og med 1942 ved endring i medlemskap etter uttak – `forskrifter/alderspensjon-i-folketrygden/par-11-8.md`
- § 11-9. Omregning av pensjon pr. 1. september 2016 for personer født til og med 1942 – `forskrifter/alderspensjon-i-folketrygden/par-11-9.md`
- § 11-10. Omregning av pensjon pr. 1. september 2016 for personer født fra og med 1944 – `forskrifter/alderspensjon-i-folketrygden/par-11-10.md`

**Kapittel 12. Avsluttende bestemmelser**

- § 12-1. Ikraftsetting – `forskrifter/alderspensjon-i-folketrygden/par-12-1.md`

**Innhold utenfor paragrafene**

- Vedlegg, tabeller o.l. – `forskrifter/alderspensjon-i-folketrygden/utenfor-paragrafene.md`

### Forskrift om dagpenger under arbeidsløshet

**Kapittel 1. Unntak fra kravet om opphold i Norge**

- § 1-1. (utbetaling av dagpenger på Svalbard) – `forskrifter/dagpengeforskriften/par-1-1.md`
- § 1-2. (Utbetaling av dagpenger som forskutterte lønnsgarantimidler til medlemmer bosatt i utlandet) – `forskrifter/dagpengeforskriften/par-1-2.md`
- § 1-3. (Dagpenger ved midlertidig opphold i utlandet ved etablering av egen virksomhet) – `forskrifter/dagpengeforskriften/par-1-3.md`
- § 1-4. (Dagpenger ved midlertidig opphold i utlandet på grunn av jobbintervju) – `forskrifter/dagpengeforskriften/par-1-4.md`
- § 1-5. (Opphevet) – `forskrifter/dagpengeforskriften/par-1-5.md`
- § 1-6. (helgefravær i utlandet) – `forskrifter/dagpengeforskriften/par-1-6.md`
- § 1-7. (søke arbeid i et annet EØS-land) – `forskrifter/dagpengeforskriften/par-1-7.md`
- § 1-8. (bosted i et annet EØS-land under siste arbeidsforhold i Norge) – `forskrifter/dagpengeforskriften/par-1-8.md`
- § 1-9. (utsendte arbeidstakere i et annet EØS-land som blir delvis arbeidsledig eller delvis permittert) – `forskrifter/dagpengeforskriften/par-1-9.md`

**Kapittel 2. Konkurs m.v.**

- § 2-1. (dagpenger ved konkurs m.v.) – `forskrifter/dagpengeforskriften/par-2-1.md`
- § 2-2. (om stønadsperiode og unntak fra egenandel) – `forskrifter/dagpengeforskriften/par-2-2.md`
- § 2-3. (forholdet til minsteinntekt, jf. folketrygdloven § 4-4) – `forskrifter/dagpengeforskriften/par-2-3.md`
- § 2-4. (Opphevet ved forskrift 2 aug 2004 nr. 1143.) – `forskrifter/dagpengeforskriften/par-2-4.md`

**Kapittel 3. Arbeidsmarkedstiltak**

- § 3-1. (lønn i arbeidsmarkedstiltak som ikke skal regnes med i kravet til minsteinntekt) – `forskrifter/dagpengeforskriften/par-3-1.md`

**Kapittel 3A. Søknadstidspunkt, opptjeningstid mv.**

- § 3A-1. Søknadstidspunkt – `forskrifter/dagpengeforskriften/par-3a-1.md`
- § 3A-2. Siste avsluttede kalendermåned – `forskrifter/dagpengeforskriften/par-3a-2.md`

**Kapittel 4. Aktivitetskrav, utdanning/opplæring, ulønnet arbeid etc.**

- § 4-1. (aktiv arbeidssøking) – `forskrifter/dagpengeforskriften/par-4-1.md`
- § 4-2. (fellesbestemmelser for deltaking i utdanning eller opplæring og ulønnet arbeid) – `forskrifter/dagpengeforskriften/par-4-2.md`
- § 4-3. (deltakelse i arbeidsmarkedstiltak) – `forskrifter/dagpengeforskriften/par-4-3.md`
- § 4-3a. (opplæring for innvandrere) – `forskrifter/dagpengeforskriften/par-4-3a.md`
- § 4-3b. (grunnskoleopplæring, videregående opplæring og opplæring i grunnleggende ferdigheter) – `forskrifter/dagpengeforskriften/par-4-3b.md`
- § 4-3c. (høyere yrkesfaglig utdanning) – `forskrifter/dagpengeforskriften/par-4-3c.md`
- § 4-3d. (høyere utdanning) – `forskrifter/dagpengeforskriften/par-4-3d.md`
- § 4-3e. (deltakelse på kurs mv.) – `forskrifter/dagpengeforskriften/par-4-3e.md`
- § 4-3f. (opplæringsplan) – `forskrifter/dagpengeforskriften/par-4-3f.md`
- § 4-3g. (opphevet) – `forskrifter/dagpengeforskriften/par-4-3g.md`
- § 4-4. (ulønnet arbeid) – `forskrifter/dagpengeforskriften/par-4-4.md`
- § 4-5. (unntak fra reglene om gradering for fosterforeldre og meddommere) – `forskrifter/dagpengeforskriften/par-4-5.md`

**Kapittel 5. Etablerere**

- § 5-1. (vilkår for å motta dagpenger under etablering) – `forskrifter/dagpengeforskriften/par-5-1.md`

**Kapittel 6. Permitterte**

- § 6-1. (vilkår for å motta dagpenger under permittering) – `forskrifter/dagpengeforskriften/par-6-1.md`
- § 6-2. (permittering i visse virksomheter) – `forskrifter/dagpengeforskriften/par-6-2.md`
- § 6-3. (avkortning mot fortsatt lønnsutbetaling fra permitterende arbeidsgiver) – `forskrifter/dagpengeforskriften/par-6-3.md`
- § 6-4. (anvisning og utbetaling) – `forskrifter/dagpengeforskriften/par-6-4.md`
- § 6-5. (konsekvenser av avbrudd i permitteringen) – `forskrifter/dagpengeforskriften/par-6-5.md`
- § 6-6. (stønadsperiode ved permittering som skyldes arbeidstvist) – `forskrifter/dagpengeforskriften/par-6-6.md`
- § 6-7. (Permittering i fiskeforedlingsindustrien, sjømatindustrien og fiskeoljeindustrien) – `forskrifter/dagpengeforskriften/par-6-7.md`
- § 6-7a. (Opphevet) – `forskrifter/dagpengeforskriften/par-6-7a.md`
- § 6-8. (Dagpenger utover begrensningen i folketrygdloven § 4-7 annet ledd) – `forskrifter/dagpengeforskriften/par-6-8.md`
- § 6-9. (unntak fra kravet i folketrygdloven § 4-5 om å være arbeidsfør for permitterte deltakere i arbeidsmarkedstiltaket varig lønnstilskudd) – `forskrifter/dagpengeforskriften/par-6-9.md`
- § 6-10. (Opphevet) – `forskrifter/dagpengeforskriften/par-6-10.md`
- § 6-11. (Opphevet) – `forskrifter/dagpengeforskriften/par-6-11.md`

**Kapittel 7. Barnetillegg**

- § 7-1. (stønadens størrelse) – `forskrifter/dagpengeforskriften/par-7-1.md`
- § 7-2. (unntak fra bostedskravet) – `forskrifter/dagpengeforskriften/par-7-2.md`

**Kapittel 8. Ferietillegg**

- § 8-1. (beregning av ferietillegg) – `forskrifter/dagpengeforskriften/par-8-1.md`
- § 8-2. (utbetaling av ferietillegget) – `forskrifter/dagpengeforskriften/par-8-2.md`

**Kapittel 9. Ytelser fra arbeidsgiver ved opphør av arbeidsforhold**

- § 9-1. (samordning med ytelser fra arbeidsgiver) – `forskrifter/dagpengeforskriften/par-9-1.md`

**Kapittel 10. Utbetaling og stans**

- § 10-1. (anvisning og utbetaling av dagpenger) – `forskrifter/dagpengeforskriften/par-10-1.md`
- § 10-2. (forskuddsanvisning) – `forskrifter/dagpengeforskriften/par-10-2.md`
- § 10-3. (korrigering av forskuddsanvisning) – `forskrifter/dagpengeforskriften/par-10-3.md`
- § 10-4. (stans av dagpenger når vilkårene for rett til dagpenger ikke lenger er oppfylt) – `forskrifter/dagpengeforskriften/par-10-4.md`

**Kapittel 11. Vanlig arbeidstid**

- § 11-1. (innhold) – `forskrifter/dagpengeforskriften/par-11-1.md`
- § 11-2. (beregning av vanlig arbeidstid) – `forskrifter/dagpengeforskriften/par-11-2.md`
- § 11-2a. (Opphevet) – `forskrifter/dagpengeforskriften/par-11-2a.md`
- § 11-3. (maksimal vanlig arbeidstid) – `forskrifter/dagpengeforskriften/par-11-3.md`

**Kapittel 12. Unntak fra plikten til å gi melding om vedtak**

- § 12-1. (unnlatt melding om vedtak om reduksjon eller stans av utbetalingen) – `forskrifter/dagpengeforskriften/par-12-1.md`

**Kapittel 13. Supplerende regler til Europaparlaments- og rådsforordning (EF) nr. 883/2004 om koordinering av trygdeordninger (trygdeforordningen)**

- § 13-1. (særlige regler for sammenlegging av perioder i nordisk konvensjon om trygd) – `forskrifter/dagpengeforskriften/par-13-1.md`
- § 13-2. (Opphevet) – `forskrifter/dagpengeforskriften/par-13-2.md`
- § 13-3. (maksimal varighet for eksport av dagpenger etter trygdeforordningen artikkel 64) – `forskrifter/dagpengeforskriften/par-13-3.md`
- § 13-4. (supplerende regler til trygdeforordningen artikkel 64 nr. 1 bokstav a) – `forskrifter/dagpengeforskriften/par-13-4.md`

**Innhold utenfor paragrafene**

- Vedlegg, tabeller o.l. – `forskrifter/dagpengeforskriften/utenfor-paragrafene.md`

### Forskrift om dagpenger for fiskere og fangstfolk under arbeidsløshet (A-trygdforskriften)

- § 1. Formål – `forskrifter/dagpenger-fiskere/par-1.md`
- § 2. Virkeområde – `forskrifter/dagpenger-fiskere/par-2.md`
- § 3. Forhold som gir rett til dagpenger til fiskere og fangstfolk med fartøytilknytning – `forskrifter/dagpenger-fiskere/par-3.md`
- § 4. Forhold som gir rett til dagpenger til fiskere og fangsfolk uten fartøytilknytning – `forskrifter/dagpenger-fiskere/par-4.md`
- § 5. Forhold som ikke gir rett til dagpenger – `forskrifter/dagpenger-fiskere/par-5.md`
- § 6. Forhold som gir reduksjon i dagpenger – `forskrifter/dagpenger-fiskere/par-6.md`
- § 7. Søknad om dagpenger og melding om fortsatt ledighet – `forskrifter/dagpenger-fiskere/par-7.md`
- § 8. Krav til minsteinntekt – `forskrifter/dagpenger-fiskere/par-8.md`
- § 9. Dagpengegrunnlag – `forskrifter/dagpenger-fiskere/par-9.md`
- § 10. Antall stønadsuker (Stønadsperiode) – `forskrifter/dagpenger-fiskere/par-10.md`
- § 11. Utbetaling av dagpenger – `forskrifter/dagpenger-fiskere/par-11.md`
- § 12. Trekk i dagpenger – `forskrifter/dagpenger-fiskere/par-12.md`
- § 13. Tilbakekreving etter feilaktige utbetalinger og sanksjoner – `forskrifter/dagpenger-fiskere/par-13.md`
- § 14. Vedtak og saksbehandling – `forskrifter/dagpenger-fiskere/par-14.md`
- § 15. Ikrafttredelse og overgangsordning – `forskrifter/dagpenger-fiskere/par-15.md`

### Kunngjøring av virkningstidspunktet for regulering av kravet til minsteinntekt i dagpengeordningen

- Hele teksten (dokumentet har ikke paragrafer) – `forskrifter/minsteinntekt-virkningstidspunkt/tekst.md`

### Forskrift om overgangsregler i forbindelse med ikrafttredelse av endring av folketrygdloven § 4-9 fra 1. januar 2024

- § 1. – `forskrifter/overgangsregler-2023/par-1.md`
- § 2. – `forskrifter/overgangsregler-2023/par-2.md`

### Forskrift om tilskudd til ekspertbistand

- § 1. Formål – `forskrifter/ekspertbistand/par-1.md`
- § 2. Personkrets – `forskrifter/ekspertbistand/par-2.md`
- § 3. Innhold – `forskrifter/ekspertbistand/par-3.md`
- § 4. Vilkår – `forskrifter/ekspertbistand/par-4.md`
- § 5. Tilskudd – `forskrifter/ekspertbistand/par-5.md`
- § 6. Krav til søknad – `forskrifter/ekspertbistand/par-6.md`
- § 7. Vedtaksmyndighet og klageadgang – `forskrifter/ekspertbistand/par-7.md`
- § 8. Kontroll og sanksjoner – `forskrifter/ekspertbistand/par-8.md`
- § 9. Støtte etter gruppeunntaket for tjenester av allmenn økonomisk betydning – `forskrifter/ekspertbistand/par-9.md`
- § 9a. Forsøk med anskaffelse av ekspertbistand – `forskrifter/ekspertbistand/par-9a.md`
- § 10. Ikrafttredelse – `forskrifter/ekspertbistand/par-10.md`

### Forskrift om stønad til enslig mor eller far etter folketrygdloven kapittel 15

- § 1. Unntak fra kravet til forutgående medlemskap – `forskrifter/stonad-enslig-mor-far/par-1.md`
- § 2. (Opphevet) – `forskrifter/stonad-enslig-mor-far/par-2.md`
- § 3. Nære boforhold – `forskrifter/stonad-enslig-mor-far/par-3.md`
- § 4. (Opphevet) – `forskrifter/stonad-enslig-mor-far/par-4.md`
- § 5. (Opphevet) – `forskrifter/stonad-enslig-mor-far/par-5.md`
- § 6. (Opphevet) – `forskrifter/stonad-enslig-mor-far/par-6.md`
- § 7. (Opphevet) – `forskrifter/stonad-enslig-mor-far/par-7.md`
- § 8. Beregning av stønad til barnetilsyn – `forskrifter/stonad-enslig-mor-far/par-8.md`
- § 9. Behandling av personopplysninger om andre familiemedlemmer – `forskrifter/stonad-enslig-mor-far/par-9.md`
- § 10. Ikrafttredelse mv. – `forskrifter/stonad-enslig-mor-far/par-10.md`

### Forskrift om overgangsregler i forbindelse med endringer i folketrygdloven § 15-6 og § 15-8 fra 1. februar 2024

- § 1. Endringen i folketrygdloven § 15-6 femte ledd første punktum – `forskrifter/overgangsregler-par15/par-1.md`
- § 2. Endringen i folketrygdloven § 15-8 første ledd andre punktum – `forskrifter/overgangsregler-par15/par-2.md`
- § 3. Ikrafttredelse – `forskrifter/overgangsregler-par15/par-3.md`

### Forskrift om ytelser til gjenlevende ektefelle og tidligere familiepleier etter folketrygdloven kapittel 17

**Kapittel 1. Innledende bestemmelser**

- § 1. Virkeområde – `forskrifter/ytelser-gjenlevende/par-1.md`

**Kapittel 2. Aktivitetsplikten**

- § 2. Unntak fra aktivitetsplikten – `forskrifter/ytelser-gjenlevende/par-2.md`
- § 3. Utvidet aktivitetskrav – `forskrifter/ytelser-gjenlevende/par-3.md`
- § 4. Reell arbeidssøker – `forskrifter/ytelser-gjenlevende/par-4.md`
- § 5. Nødvendig og hensiktsmessig utdanning eller opplæring – `forskrifter/ytelser-gjenlevende/par-5.md`
- § 6. Etablering av egen virksomhet – `forskrifter/ytelser-gjenlevende/par-6.md`
- § 7. Krav til opplysninger – `forskrifter/ytelser-gjenlevende/par-7.md`

**Kapittel 3. Sanksjoner**

- § 8. Opphør ved langvarig manglende aktivitet – `forskrifter/ytelser-gjenlevende/par-8.md`

**Kapittel 4. Reduksjon av stønad på grunnlag av pensjonsgivende inntekt m.m.**

- § 9. Gjennomføring av inntektsavkorting – `forskrifter/ytelser-gjenlevende/par-9.md`
- § 10. Tidspunkt for når omstillingsstønaden skal reduseres på grunn av inntekten og fordeling av reduksjon gjennom kalenderåret – `forskrifter/ytelser-gjenlevende/par-10.md`

**Kapittel 5. Forskjellige bestemmelser**

- § 11. Stønad til dekning av utgifter til skolepenger mv. – `forskrifter/ytelser-gjenlevende/par-11.md`
- § 12. Beregning av stønad til barnetilsyn – `forskrifter/ytelser-gjenlevende/par-12.md`

**Kapittel 6. Ikrafttredelse**

- § 13. Ikrafttredelse – `forskrifter/ytelser-gjenlevende/par-13.md`

### Forskrift om behovsprøvet gravferdsstønad

- § 1. Utgiftsgrunnlag – `forskrifter/behovsprovd-gravferdsstonad/par-1.md`
- § 2. Formue – `forskrifter/behovsprovd-gravferdsstonad/par-2.md`
- § 3. Dokumentasjon – `forskrifter/behovsprovd-gravferdsstonad/par-3.md`
- § 4. Sivilstand – `forskrifter/behovsprovd-gravferdsstonad/par-4.md`
- § 5. Skadeserstatning – `forskrifter/behovsprovd-gravferdsstonad/par-5.md`
- § 6. Tjenestepensjon – `forskrifter/behovsprovd-gravferdsstonad/par-6.md`
- § 7. Begrensning når utgiftene dekkes etter andre bestemmelser i loven – `forskrifter/behovsprovd-gravferdsstonad/par-7.md`
- § 8. Ikrafttredelse – `forskrifter/behovsprovd-gravferdsstonad/par-8.md`

### Forskrift om gravferdsstønad og stønad til båretransport for person som er pliktig medlem etter § 2-5 i lov om folketrygd og som dør utenfor Norge og om stønad til båretransport når et medlem dør i et av de nordiske land

- § 1. – `forskrifter/gravferdsstonad-baretransport/par-1.md`
- § 2. – `forskrifter/gravferdsstonad-baretransport/par-2.md`
- § 3. – `forskrifter/gravferdsstonad-baretransport/par-3.md`
- § 4. – `forskrifter/gravferdsstonad-baretransport/par-4.md`

### Forskrift om dekning av utgifter til båretransport i Norge

- § 1. – `forskrifter/baretransport/par-1.md`
- § 2. – `forskrifter/baretransport/par-2.md`
- § 3. – `forskrifter/baretransport/par-3.md`
- § 4. – `forskrifter/baretransport/par-4.md`

### Forskrift om grunnbeløp, reguleringsfaktorer, satser for minste pensjonsnivå og satser for garantipensjon i folketrygden fra 1. mai 2026 og virknings-tidspunkt for regulering av kravet til minsteinntekt for rett til ytelser etter folketrygdloven kapitlene 4, 8, 9 og 14

- § 1. – `forskrifter/grunnbelop-og-satser/par-1.md`
- § 2. – `forskrifter/grunnbelop-og-satser/par-2.md`
- § 3. – `forskrifter/grunnbelop-og-satser/par-3.md`
- § 4. – `forskrifter/grunnbelop-og-satser/par-4.md`
- § 5. – `forskrifter/grunnbelop-og-satser/par-5.md`
- § 6. – `forskrifter/grunnbelop-og-satser/par-6.md`
- § 7. – `forskrifter/grunnbelop-og-satser/par-7.md`

### Forskrift om beregning av lønnsveksten som skal benyttes ved regulering av grunnbeløpet og alderspensjon i folketrygden

- § 1. Virkeområde – `forskrifter/regulering-lonnsvekst/par-1.md`
- § 2. Lønnsvekst i reguleringsåret og avvik mellom forventet og faktisk lønnsutvikling siste to år – `forskrifter/regulering-lonnsvekst/par-2.md`
- § 2a. Særskilt om fastsettelse av forventet lønnsutvikling for 2020 – `forskrifter/regulering-lonnsvekst/par-2a.md`
- § 3. Beregning av lønnsveksten som skal benyttes ved reguleringen – `forskrifter/regulering-lonnsvekst/par-3.md`
- § 3a. Lønnsvekst som skal benyttes ved reguleringen i 2021 – `forskrifter/regulering-lonnsvekst/par-3a.md`
- § 4. Prisvekst i reguleringsåret og avvik mellom forventet og faktisk prisvekst året før reguleringsåret – `forskrifter/regulering-lonnsvekst/par-4.md`
- § 5. Drøfting med organisasjonene – `forskrifter/regulering-lonnsvekst/par-5.md`
- § 6. Ikraftsetting – `forskrifter/regulering-lonnsvekst/par-6.md`

### Forskrift om gjennomføring av bilaterale trygdeavtaler

- § 1. – `forskrifter/bilaterale-trygdeavtaler/par-1.md`
- § 2. – `forskrifter/bilaterale-trygdeavtaler/par-2.md`

### Forskrift om unntak fra medlemskap i folketrygden for person som er omfattet av eller mottar ytelser etter utenlandsk trygdelovgivning mv og vedkommendes familiemedlemmer

- § 1. Obligatorisk unntak – `forskrifter/unntak-medlemskap/par-1.md`
- § 2. Unntak etter individuell søknad – `forskrifter/unntak-medlemskap/par-2.md`
- § 3. Unntak i særlige tilfelle – `forskrifter/unntak-medlemskap/par-3.md`
- § 4. Forsørgede familiemedlemmer – `forskrifter/unntak-medlemskap/par-4.md`
- § 5. Ikrafttredelse – `forskrifter/unntak-medlemskap/par-5.md`

### Forskrift om trygdedekning for asylsøkere og deres familiemedlemmer

- § 1. Definisjoner – `forskrifter/trygdedekning-asylsokere/par-1.md`
- § 2. Trygdedekningen – `forskrifter/trygdedekning-asylsokere/par-2.md`
- § 3. (Opphevet) – `forskrifter/trygdedekning-asylsokere/par-3.md`
- § 4. Ikrafttredelse – `forskrifter/trygdedekning-asylsokere/par-4.md`

### Forskrift om medlemskap i trygden under fengselsopphold mv

**Kapittel 1. Innledende bestemmelser**

- § 1. Hva forskriften gjelder – `forskrifter/medlemskap-fengsel/par-1.md`
- § 2. Definisjoner – `forskrifter/medlemskap-fengsel/par-2.md`
- § 3. Medlemskap under frihetsberøvelse – `forskrifter/medlemskap-fengsel/par-3.md`

**Kapittel 2. Ytelser under frihetsberøvelse**

- § 4. Generelt – `forskrifter/medlemskap-fengsel/par-4.md`
- § 5. Sak om utvisning fra riket – `forskrifter/medlemskap-fengsel/par-5.md`
- § 6. Krav om trygdetilknytning før stønadstilfellet – `forskrifter/medlemskap-fengsel/par-6.md`
- § 7. Vedtak om utvisning – `forskrifter/medlemskap-fengsel/par-7.md`
- § 8. Etterlatte – `forskrifter/medlemskap-fengsel/par-8.md`
- § 9. Helsetjenester – `forskrifter/medlemskap-fengsel/par-9.md`

- § 10. Ikrafttredelse – `forskrifter/medlemskap-fengsel/par-10.md`

### Forskrift om fastsetting av pensjonsgivende inntekt for året før det året da et medlem får rett til en trygdeytelse

- § 1. – `forskrifter/pensjonsgivende-inntekt-uforetidspunkt/par-1.md`
- § 2. – `forskrifter/pensjonsgivende-inntekt-uforetidspunkt/par-2.md`
- § 3. – `forskrifter/pensjonsgivende-inntekt-uforetidspunkt/par-3.md`

### Forskrift om godskriving av pensjonspoeng (omsorgspoeng) for personer som har omsorg for små barn

- § 1. Omsorgsyter – `forskrifter/omsorgspoeng/par-1.md`
- § 2. Tildeling av omsorgspoeng – `forskrifter/omsorgspoeng/par-2.md`
- § 3. Overføring av omsorgspoeng mellom omsorgsyterne – `forskrifter/omsorgspoeng/par-3.md`
- § 4. Ikrafttredelse – `forskrifter/omsorgspoeng/par-4.md`

### Forskrift om godskriving av pensjonspoeng (omsorgspoeng) for omsorgsarbeid for en syk, en funksjonshemmet eller en eldre person

- § 1. Omsorgsarbeidets omfang – `forskrifter/omsorgspoeng-omsorgsarbeid/par-1.md`
- § 2. Omsorgsarbeid for flere personer – `forskrifter/omsorgspoeng-omsorgsarbeid/par-2.md`
- § 3. Flere utøver omsorgsarbeid for samme person – `forskrifter/omsorgspoeng-omsorgsarbeid/par-3.md`
- § 4. Avgrensing mot personer i omsorgsyrker – `forskrifter/omsorgspoeng-omsorgsarbeid/par-4.md`
- § 5. Framsetting av krav om omsorgspoeng – `forskrifter/omsorgspoeng-omsorgsarbeid/par-5.md`
- § 6. Forhøyet hjelpestønad – `forskrifter/omsorgspoeng-omsorgsarbeid/par-6.md`
- § 7. Attestasjon – `forskrifter/omsorgspoeng-omsorgsarbeid/par-7.md`
- § 8. Pleieforhold som strekker seg over flere kalenderår – `forskrifter/omsorgspoeng-omsorgsarbeid/par-8.md`
- § 9. Ikrafttredelse – `forskrifter/omsorgspoeng-omsorgsarbeid/par-9.md`

### Forskrift om godskriving av pensjonspoeng for mottakere av avtalefestet pensjon som omfattes av AFP-tilskottsloven § 12 eller avtalefestet pensjon fra offentlig pensjonsordning før fylte 65 år

- § 1. Virkeområde – `forskrifter/omsorgspoeng-afp/par-1.md`
- § 2. Godskriving av pensjonspoeng – `forskrifter/omsorgspoeng-afp/par-2.md`
- § 3. Ikrafttredelse – `forskrifter/omsorgspoeng-afp/par-3.md`

### Forskrift om nedsettelse av pensjonsgivende inntekt, pensjonsopptjening og avgift når fastsatt skatt og avgift helt eller delvis ikke er betalt

**I**

- § 1. – `forskrifter/nedsettelse-pensjonsgivende-inntekt/par-1.md`
- § 2. – `forskrifter/nedsettelse-pensjonsgivende-inntekt/par-2.md`
- § 3. – `forskrifter/nedsettelse-pensjonsgivende-inntekt/par-3.md`
- § 4. – `forskrifter/nedsettelse-pensjonsgivende-inntekt/par-4.md`
- § 5. – `forskrifter/nedsettelse-pensjonsgivende-inntekt/par-5.md`
- § 6. – `forskrifter/nedsettelse-pensjonsgivende-inntekt/par-6.md`
- § 7. – `forskrifter/nedsettelse-pensjonsgivende-inntekt/par-7.md`
- § 8. – `forskrifter/nedsettelse-pensjonsgivende-inntekt/par-8.md`

### Forskrift om gjennomføring av nedsettelse av pensjonsgivende inntekt, pensjonsopptjening og avgift når fastsatt skatt og avgift helt eller delvis ikke er betalt

**I**

- § 1. – `forskrifter/gjennomforing-nedsettelse/par-1.md`
- § 2. – `forskrifter/gjennomforing-nedsettelse/par-2.md`
- § 3. – `forskrifter/gjennomforing-nedsettelse/par-3.md`
- § 4. – `forskrifter/gjennomforing-nedsettelse/par-4.md`
- § 5. – `forskrifter/gjennomforing-nedsettelse/par-5.md`

**Innhold utenfor paragrafene**

- Vedlegg, tabeller o.l. – `forskrifter/gjennomforing-nedsettelse/utenfor-paragrafene.md`

### Forskrift om endring i forskrift om nedsettelse av pensjonsgivende inntekt, pensjonsopptjening og avgift når fastsatt skatt og avgift helt eller delvis ikke er betalt

- Hele teksten (dokumentet har ikke paragrafer) – `forskrifter/endring-nedsettelse/tekst.md`

### Forskrift om fastsettelse av pensjonsgivende inntekt mv. for medlemmer med inntekt som ikke blir skattlagt av norske myndigheter

- § 1. Personkrets – `forskrifter/pensjonsgivende-inntekt-utland/par-1.md`
- § 2. Medlemmets opplysningsplikt – `forskrifter/pensjonsgivende-inntekt-utland/par-2.md`
- § 3. Fastsettelse av pensjonsgivende inntekt mv. – `forskrifter/pensjonsgivende-inntekt-utland/par-3.md`
- § 4. Forskjellige bestemmelser – `forskrifter/pensjonsgivende-inntekt-utland/par-4.md`
- § 5. Delegering av myndighet – `forskrifter/pensjonsgivende-inntekt-utland/par-5.md`
- § 6. Ikrafttredelse – `forskrifter/pensjonsgivende-inntekt-utland/par-6.md`

### Forskrift om pensjonsberegning, om tilståelse og beregning av barnetillegg og barnepensjon og om gjennomføringa av folketrygdlovens bestemmelser om inntektsprøving i tilfelle som omfattes av EØS-avtalen

**I. Forskriftens omfang**

- § 1. EØS-land – `forskrifter/pensjonsberegning-barnetillegg/par-1.md`
- § 2. Hvilke tilfelle som reguleres – `forskrifter/pensjonsberegning-barnetillegg/par-2.md`
- § 3. Definisjoner – `forskrifter/pensjonsberegning-barnetillegg/par-3.md`

**II. Beregning av pensjon fra folketrygden etter koordineringsreglene i EØS-avtalen.**

- § 4. Det teoretiske beløp. – `forskrifter/pensjonsberegning-barnetillegg/par-4.md`
- § 5. Det faktiske beløp – `forskrifter/pensjonsberegning-barnetillegg/par-5.md`

**III. Inntektsprøving av ektefelletillegg – folketrygdloven § 7-8 A.**

- § 6. Ektefelletillegget – `forskrifter/pensjonsberegning-barnetillegg/par-6.md`
- § 7. Fribeløpet – `forskrifter/pensjonsberegning-barnetillegg/par-7.md`
- § 8. Inntektsgrunnlaget – `forskrifter/pensjonsberegning-barnetillegg/par-8.md`

**IV. Særlig om tilståelse og beregning av barnetillegg og barnepensjoner.**

- § 9. Tilståelse av barnetillegg – `forskrifter/pensjonsberegning-barnetillegg/par-9.md`
- § 10. Beregning av barnetillegg – `forskrifter/pensjonsberegning-barnetillegg/par-10.md`
- § 11. Differanse-barnetillegg – `forskrifter/pensjonsberegning-barnetillegg/par-11.md`
- § 12. Barnepensjon – `forskrifter/pensjonsberegning-barnetillegg/par-12.md`
- § 13. Stans av barnetillegg/barnepensjon – `forskrifter/pensjonsberegning-barnetillegg/par-13.md`

**V. Prøving mot arbeidsinntekt – folketrygdloven §§ 7-10 og 10-5 nr. 3**

- § 14. Pensjonen – `forskrifter/pensjonsberegning-barnetillegg/par-14.md`
- § 15. Fribeløpet – `forskrifter/pensjonsberegning-barnetillegg/par-15.md`
- § 16. Inntektsgrunnlaget – `forskrifter/pensjonsberegning-barnetillegg/par-16.md`

**VI. Ikrafttredelse**

- § 17. Ikrafttredelse – `forskrifter/pensjonsberegning-barnetillegg/par-17.md`

**Innhold utenfor paragrafene**

- Vedlegg, tabeller o.l. – `forskrifter/pensjonsberegning-barnetillegg/utenfor-paragrafene.md`

### Forskrift om behandling av tvister i arbeidsgiverperioden

**I. Saklig myndighetsområde**

- § 1. – `forskrifter/tvister-arbeidsgiverperioden/par-1.md`
- § 2. – `forskrifter/tvister-arbeidsgiverperioden/par-2.md`
- § 3. – `forskrifter/tvister-arbeidsgiverperioden/par-3.md`
- § 4. – `forskrifter/tvister-arbeidsgiverperioden/par-4.md`

**II. Organisasjon**

- § 5. – `forskrifter/tvister-arbeidsgiverperioden/par-5.md`
- § 6. – `forskrifter/tvister-arbeidsgiverperioden/par-6.md`
- § 7. – `forskrifter/tvister-arbeidsgiverperioden/par-7.md`

**III. Anke og saksforberedelse**

- § 8. – `forskrifter/tvister-arbeidsgiverperioden/par-8.md`
- § 9. – `forskrifter/tvister-arbeidsgiverperioden/par-9.md`
- § 10. – `forskrifter/tvister-arbeidsgiverperioden/par-10.md`
- § 11. – `forskrifter/tvister-arbeidsgiverperioden/par-11.md`

**IV. Ankebehandling**

- § 12. – `forskrifter/tvister-arbeidsgiverperioden/par-12.md`
- § 13. – `forskrifter/tvister-arbeidsgiverperioden/par-13.md`

**V. Forskjellige bestemmelser**

- § 14. – `forskrifter/tvister-arbeidsgiverperioden/par-14.md`
- § 15. – `forskrifter/tvister-arbeidsgiverperioden/par-15.md`
- § 16. – `forskrifter/tvister-arbeidsgiverperioden/par-16.md`
- § 17. – `forskrifter/tvister-arbeidsgiverperioden/par-17.md`
- § 18. – `forskrifter/tvister-arbeidsgiverperioden/par-18.md`
- § 19. – `forskrifter/tvister-arbeidsgiverperioden/par-19.md`

### Forskrift om unntak fra anke til Trygderetten

- § 1. Vedtak som unntas – `forskrifter/unntak-anke-trygderetten/par-1.md`
- § 2. Ikrafttredelse – `forskrifter/unntak-anke-trygderetten/par-2.md`

### Forskrift om at visse vedtak kan ankes direkte inn for Trygderetten

- § 1. Vedtak som skal ankes direkte inn for Trygderetten – `forskrifter/anke-direkte-trygderetten/par-1.md`
- § 2. Overgangsregler – `forskrifter/anke-direkte-trygderetten/par-2.md`
- § 3. Ikrafttredelse – `forskrifter/anke-direkte-trygderetten/par-3.md`

### Forskrift om utveksling av opplysninger mellom Arbeids- og velferdsetaten og pensjonsinnretninger, forsikringsselskaper og andre finansinstitusjoner

- § 1. Virkeområde – `forskrifter/utveksling-opplysninger/par-1.md`
- § 2. Når kan opplysninger utveksles etter folketrygdlovens § 21-4b – `forskrifter/utveksling-opplysninger/par-2.md`
- § 3. Hvilke opplysninger som kan utleveres – `forskrifter/utveksling-opplysninger/par-3.md`
- § 4. Hvilke organer som vurderer om opplysninger kan gis – `forskrifter/utveksling-opplysninger/par-4.md`
- § 5. Hvordan opplysningene skal gis – `forskrifter/utveksling-opplysninger/par-5.md`
- § 6. Taushetsplikt – `forskrifter/utveksling-opplysninger/par-6.md`
- § 7. Krav til oppbevaring og sletting av opplysninger mv. – `forskrifter/utveksling-opplysninger/par-7.md`
- § 8. Ikrafttredelse – `forskrifter/utveksling-opplysninger/par-8.md`

### Forskrift om elektronisk kommunikasjon med Arbeids- og velferdsetaten

- § 1. Formål – `forskrifter/elektronisk-kommunikasjon/par-1.md`
- § 2. Virkeområde – `forskrifter/elektronisk-kommunikasjon/par-2.md`
- § 3. Pålegg om elektronisk kommunikasjon med Arbeids- og velferdsetaten – `forskrifter/elektronisk-kommunikasjon/par-3.md`
- § 4. Formkrav – `forskrifter/elektronisk-kommunikasjon/par-4.md`
- § 5. Unntak – `forskrifter/elektronisk-kommunikasjon/par-5.md`
- § 6. Manglende oppfyllelse av forskriften – `forskrifter/elektronisk-kommunikasjon/par-6.md`
- § 7. Ikrafttredelse – `forskrifter/elektronisk-kommunikasjon/par-7.md`

### Forskrift om unntak fra pålegg om elektronisk kommunikasjon ved innsending av erklæringer og uttalelser til Arbeids- og velferdsetaten (NAV)

- § 1. Unntak uten søknad – `forskrifter/unntak-elektronisk-innsending/par-1.md`
- § 2. Innsending på annen måte enn over linje – `forskrifter/unntak-elektronisk-innsending/par-2.md`
- § 3. Unntak etter søknad – `forskrifter/unntak-elektronisk-innsending/par-3.md`
- § 4. Endringer i legens praksis – `forskrifter/unntak-elektronisk-innsending/par-4.md`
- § 5. Ikrafttredelse – `forskrifter/unntak-elektronisk-innsending/par-5.md`

### Forskrift om at saksopplysninger til Arbeids- og velferdsetaten skal gis elektronisk

- § 1. Opplysninger fra arbeidsgiver – `forskrifter/saksopplysninger-elektronisk/par-1.md`
- § 2. Ikrafttredelse – `forskrifter/saksopplysninger-elektronisk/par-2.md`

### Forskrift om økt beregningsgrunnlag for gifte og samboende uføretrygdede som mottar en uføretrygd omregnet fra uførepensjon

- § 1. Virkeområdet – `forskrifter/okt-beregningsgrunnlag-gift-samboende/par-1.md`
- § 2. Uføretrygd – `forskrifter/okt-beregningsgrunnlag-gift-samboende/par-2.md`
- § 3. Økning av beregningsgrunnlaget – `forskrifter/okt-beregningsgrunnlag-gift-samboende/par-3.md`
- § 4. Ikrafttredelse – `forskrifter/okt-beregningsgrunnlag-gift-samboende/par-4.md`

### Forskrift om omregning av uførepensjon til uføretrygd

- § 1. Virkeområde – `forskrifter/omregning-uforepensjon-til-uforetrygd/par-1.md`
- § 2. Overgang til uføretrygd – `forskrifter/omregning-uforepensjon-til-uforetrygd/par-2.md`
- § 3. Grunnlaget for beregning av uføretrygd – `forskrifter/omregning-uforepensjon-til-uforetrygd/par-3.md`
- § 4. Grunnlaget for beregning av uføretrygd der mottakeren ikke er medlem av trygden, får uførepensjon beregnet etter EØS-forordning 883/2004 eller 1408/71 eller får uførepensjon beregnet etter en trygdeavtale som gir rett til sammenlegging av trygdeperioder – `forskrifter/omregning-uforepensjon-til-uforetrygd/par-4.md`
- § 5. Grunnlaget for beregning av uføretrygd der mottaker har uførepensjon med yrkesskadefordeler – `forskrifter/omregning-uforepensjon-til-uforetrygd/par-5.md`
- § 6. Grunnlaget for beregning av uføretrygd der mottaker har en uførepensjon som er redusert fordi mottakeren oppholder seg på en institusjon per 31. desember 2014 – `forskrifter/omregning-uforepensjon-til-uforetrygd/par-6.md`
- § 7. Tillegg til uføretrygd for person som mottar uførepensjon til gjenlevende ektefelle (gjenlevendetillegg) – `forskrifter/omregning-uforepensjon-til-uforetrygd/par-7.md`
- § 8. Ektefelletillegg – `forskrifter/omregning-uforepensjon-til-uforetrygd/par-8.md`
- § 9. Uføretrygd for minstepensjonister som forsørger en ektefelle som har fylt 60 år – `forskrifter/omregning-uforepensjon-til-uforetrygd/par-9.md`
- § 10. Ikrafttredelse – `forskrifter/omregning-uforepensjon-til-uforetrygd/par-10.md`

### Forskrift om uføretrygd fra folketrygden

**Kapittel 1. Innledende bestemmelser**

- § 1-1. Virkeområde – `forskrifter/uforetrygdforskriften/par-1-1.md`

**Kapittel 2. Inntekt før og etter uførhet**

- § 2-1. Fastsetting av inntekt før uførhet – `forskrifter/uforetrygdforskriften/par-2-1.md`
- § 2-2. Fastsetting av inntekt etter uførhet – `forskrifter/uforetrygdforskriften/par-2-2.md`
- § 2-3. Endring av inntekt før og etter uførhet – `forskrifter/uforetrygdforskriften/par-2-3.md`

**Kapittel 3. Reduksjon av uføretrygd på grunn av inntekt**

- § 3-1. Fribeløp for personer som mottar uføretrygd i varig tilrettelagt arbeid (VTA) – `forskrifter/uforetrygdforskriften/par-3-1.md`
- § 3-2. Pensjonsgivende inntekt som ikke skal føre til reduksjon av uføretrygd – `forskrifter/uforetrygdforskriften/par-3-2.md`
- § 3-3. Tidspunkt for når uføretrygd, barnetillegg og gjenlevendetillegg skal reduseres på grunn av inntekten og fordeling av reduksjon gjennom kalenderåret – `forskrifter/uforetrygdforskriften/par-3-3.md`
- § 3-4. Hvilende rett til uføretrygd når pensjonsgivende inntekt utgjør mer enn 80 prosent av inntekt før uførhet – `forskrifter/uforetrygdforskriften/par-3-4.md`
- § 3-5. Unntak fra ny ventetid for økt fribeløp – `forskrifter/uforetrygdforskriften/par-3-5.md`
- § 3-6. Begrensning av fribeløpet – `forskrifter/uforetrygdforskriften/par-3-6.md`
- § 3-7. Beregning av fribeløpet for et kalenderår – `forskrifter/uforetrygdforskriften/par-3-7.md`

**Kapittel 4. Etteroppgjør**

- § 4-1. Etteroppgjør – `forskrifter/uforetrygdforskriften/par-4-1.md`
- § 4-2. Gjennomføring av tilbakekreving i etteroppgjøret – `forskrifter/uforetrygdforskriften/par-4-2.md`

**Kapittel 5. Barnetillegg**

- § 5-1. Inntektsgrunnlaget – `forskrifter/uforetrygdforskriften/par-5-1.md`
- § 5-2. Type barnetillegg – `forskrifter/uforetrygdforskriften/par-5-2.md`
- § 5-3. Barnetillegg når et barn blir forsørget av flere som mottar uføretrygd – `forskrifter/uforetrygdforskriften/par-5-3.md`

**Kapittel 6. Beregning av uføretrygd ved yrkesskade**

- § 6-1. Uføretrygd som delvis skyldes yrkesskade – `forskrifter/uforetrygdforskriften/par-6-1.md`
- § 6-2. Ytterligere nedsatt inntektsevne – `forskrifter/uforetrygdforskriften/par-6-2.md`
- § 6-3. Grunnlaget for beregning av uføretrygd for år da en person har mottatt uføretrygd som helt eller delvis skyldes yrkesskade – `forskrifter/uforetrygdforskriften/par-6-3.md`

**Kapittel 7. Særlige bestemmelser for personer som har fått uførepensjon omregnet til uføretrygd**

- § 7-1. Omfang – `forskrifter/uforetrygdforskriften/par-7-1.md`
- § 7-2. (Opphevet) – `forskrifter/uforetrygdforskriften/par-7-2.md`
- § 7-3. Ytterligere reduksjon av personens inntektsevne – `forskrifter/uforetrygdforskriften/par-7-3.md`
- § 7-4. Grunnlaget for beregning av uføretrygd for år da en person har mottatt uførepensjon – `forskrifter/uforetrygdforskriften/par-7-4.md`
- § 7-5. Beregning av uføretrygd ved endringer i medlemskap, jf. folketrygdloven § 12-3 – `forskrifter/uforetrygdforskriften/par-7-5.md`
- § 7-6. Særlig om beregning av uføretrygd til unge uføre ved endringer i medlemskap, jf. folketrygdloven § 12-3 – `forskrifter/uforetrygdforskriften/par-7-6.md`

**Kapittel 8. Pensjonspoeng og pensjonsopptjening for inntektsåret 2014**

- § 8-1. Fastsetting av pensjonspoeng og pensjonsopptjening for inntektsåret 2014 – `forskrifter/uforetrygdforskriften/par-8-1.md`

**Kapittel 9. Ikrafttredelse**

- § 9-1. Ikrafttredelse – `forskrifter/uforetrygdforskriften/par-9-1.md`

**Innhold utenfor paragrafene**

- Vedlegg, tabeller o.l. – `forskrifter/uforetrygdforskriften/utenfor-paragrafene.md`

### Forskrift om gjennomføringen av folketrygdloven § 22-18 og bidragsinnkrevingsloven § 34 om utbetalingsmåten for ytelser mv

- § 1. Overføring til konto – `forskrifter/gjennomforing-par22-18/par-1.md`
- § 2. Personer som ikke har bankkonto i Norge – `forskrifter/gjennomforing-par22-18/par-2.md`
- § 3. Unntak for personer som har bankkonto i Norge – `forskrifter/gjennomforing-par22-18/par-3.md`
- § 4. Unntak for personer i utlandet – `forskrifter/gjennomforing-par22-18/par-4.md`
- § 5. Unntak for visse typer utbetalinger – `forskrifter/gjennomforing-par22-18/par-5.md`
- § 6. Ikrafttredelse – `forskrifter/gjennomforing-par22-18/par-6.md`

### Forskrift om rentesats etter folketrygdloven § 22-17 første ledd

- § 1. – `forskrifter/rentesats-par22-17/par-1.md`
- § 2. – `forskrifter/rentesats-par22-17/par-2.md`

### Forskrift om disponering av kontantytelser fra folketrygden under opphold i kommunal helse- og omsorgsinstitusjon og i helseinstitusjon i spesialisthelsetjenesten

**Kapittel 1. Virkeområde**

- § 1. Virkeområde – `forskrifter/disponering-institusjon/par-1.md`

**Kapittel 2. Utbetaling og disponering av kontantytelser**

- § 2. Utbetaling av kontantytelser – `forskrifter/disponering-institusjon/par-2.md`
- § 3. Institusjonens disposisjonsrett – `forskrifter/disponering-institusjon/par-3.md`
- § 4. Om vedtaket – `forskrifter/disponering-institusjon/par-4.md`
- § 5. Fullmakt – `forskrifter/disponering-institusjon/par-5.md`
- § 6. Om disposisjonene – `forskrifter/disponering-institusjon/par-6.md`
- § 7. Bruk av oppsparte midler – `forskrifter/disponering-institusjon/par-7.md`
- § 8. Avvikling – `forskrifter/disponering-institusjon/par-8.md`
- § 9. Regnskap – `forskrifter/disponering-institusjon/par-9.md`

**Kapittel 3. Forskjellige bestemmelser**

- § 10. Klage – `forskrifter/disponering-institusjon/par-10.md`
- § 11. Ikrafttreden – `forskrifter/disponering-institusjon/par-11.md`

### Forskrift om overtredelsesgebyr og tvangsmulkt etter folketrygdloven § 25-3 ved brudd på opplysningsplikten til Arbeidsgiver- og arbeidstakerregisteret mv

- § 1. Forskriftens innhold – `forskrifter/overtredelsesgebyr-tvangsmulkt/par-1.md`
- § 2. En eller flere forsømmelser – `forskrifter/overtredelsesgebyr-tvangsmulkt/par-2.md`
- § 3. Melding til Arbeids- og velferdsdirektoratet om ileggelse av tvangsmulkt – `forskrifter/overtredelsesgebyr-tvangsmulkt/par-3.md`
- § 4. Forholdet mellom overtredelsesgebyr og tvangsmulkt – `forskrifter/overtredelsesgebyr-tvangsmulkt/par-4.md`
- § 5. Økt overtredelsesgebyr og tvangsmulkt ved gjentakelse – `forskrifter/overtredelsesgebyr-tvangsmulkt/par-5.md`
- § 6. Klage over vedtak. Ettergivelse av overtredelsesgebyr og tvangsmulkt – `forskrifter/overtredelsesgebyr-tvangsmulkt/par-6.md`
- § 7. Ikrafttredelse – `forskrifter/overtredelsesgebyr-tvangsmulkt/par-7.md`

### Forskrift til folketrygdloven § 25-10 om arbeidsgivers og oppdragsgivers opplysningsplikt om arbeidsforhold og inntekt

- § 1. Opplysninger om arbeidsforhold – `forskrifter/opplysningsplikt-arbeidsgiver/par-1.md`
- § 2. Opplysninger om inntekt – `forskrifter/opplysningsplikt-arbeidsgiver/par-2.md`
- § 3. Særskilt om opptjeningsperiode for inntekt – `forskrifter/opplysningsplikt-arbeidsgiver/par-3.md`
- § 4. Ikrafttredelse – `forskrifter/opplysningsplikt-arbeidsgiver/par-4.md`

### Forskrift om føring av statistikk over sykefravær og fravær ved barns sykdom

- § 1. Arbeidsgivers plikt til å føre statistikk – `forskrifter/statistikk-sykefravaer/par-1.md`
- § 2. Formålet med sykefraværsstatistikken – `forskrifter/statistikk-sykefravaer/par-2.md`
- § 3. Hvem skal omfattes av registreringen – `forskrifter/statistikk-sykefravaer/par-3.md`
- § 4. Opplysninger som skal registreres – `forskrifter/statistikk-sykefravaer/par-4.md`
- § 5. Registreringsperiode – `forskrifter/statistikk-sykefravaer/par-5.md`
- § 6. Hvem kan kreve innsyn i sykefraværsstatistikken – `forskrifter/statistikk-sykefravaer/par-6.md`
- § 7. Sanksjoner – `forskrifter/statistikk-sykefravaer/par-7.md`
- § 8. Ikrafttredelse – `forskrifter/statistikk-sykefravaer/par-8.md`

### Forskrift om beregning av kapitalverdier av trygdeytelser

- § 1. Virkeområde – `forskrifter/kapitalverdier/par-1.md`
- § 2. Grunnlagsrente – `forskrifter/kapitalverdier/par-2.md`
- § 3. Dødelighetserfaringer – `forskrifter/kapitalverdier/par-3.md`
- § 4. Gjengiftefrekvenser – `forskrifter/kapitalverdier/par-4.md`
- § 5. Ikrafttredelse – `forskrifter/kapitalverdier/par-5.md`

### Forskrift om videreføring av to forskrifter gitt med hjemmel i lov om folketrygd

- Hele teksten (dokumentet har ikke paragrafer) – `forskrifter/viderefoering-forskrifter/tekst.md`

### Forskrift om Arbeidsgiver- og arbeidstakerregisteret

**I. Innledende bestemmelser**

- § 1. Registeransvarlig – `forskrifter/aa-registeret/par-1.md`
- § 2. Formål – `forskrifter/aa-registeret/par-2.md`
- § 3. Definisjoner – `forskrifter/aa-registeret/par-3.md`

**II. Om melding til registeret**

- § 4. Plikt til å registrere seg som arbeidsgiver og oppdragsgiver – `forskrifter/aa-registeret/par-4.md`
- § 5. Melding om arbeidsforhold – `forskrifter/aa-registeret/par-5.md`
- § 6. Meldepliktens omfang – `forskrifter/aa-registeret/par-6.md`
- § 7. Kontroll og forvaltning av Arbeidsgiver- og arbeidstakerregisteret – `forskrifter/aa-registeret/par-7.md`
- § 8. Adgang til å gjøre unntak – `forskrifter/aa-registeret/par-8.md`

**III. Om opplysninger fra registeret**

- § 9. Tilgang til opplysninger fra Arbeidsgiver- og arbeidstakerregisteret ved offentlig myndighetsutøvelse – `forskrifter/aa-registeret/par-9.md`
- § 10. Tilgang til opplysninger fra Arbeidsgiver- og arbeidstakerregisteret for andre – `forskrifter/aa-registeret/par-10.md`
- § 11. Krav til søknad om tilgang – `forskrifter/aa-registeret/par-11.md`
- § 12. Betaling for opplysningene – `forskrifter/aa-registeret/par-12.md`
- § 13. Opplysninger om personer med sperret adresse – `forskrifter/aa-registeret/par-13.md`
- § 14. Avgjørelsesmyndighet – `forskrifter/aa-registeret/par-14.md`

**IV. Tiltak overfor arbeidsgiver eller oppdragsgiver ved brudd på plikten til å gi opplysninger om arbeidsforhold**

- § 15. Overtredelsesgebyr og tvangsmulkt – `forskrifter/aa-registeret/par-15.md`

**V. Forskjellige bestemmelser**

- § 16. Taushetsplikt – `forskrifter/aa-registeret/par-16.md`
- § 17. Behandling av opplysninger fra registeret – `forskrifter/aa-registeret/par-17.md`
- § 18. Klage på vedtak – `forskrifter/aa-registeret/par-18.md`
- § 19. Straffebestemmelse – `forskrifter/aa-registeret/par-19.md`
- § 20. Gjennomføring av forskriften – `forskrifter/aa-registeret/par-20.md`
- § 21. Ikrafttredelse – `forskrifter/aa-registeret/par-21.md`

### Forskrift om menerstatning ved yrkesskade

**Del I. Alminnelige bestemmelser**

- § 1. Innledning – `forskrifter/menerstatning/par-1.md`
- § 2. Fastsetting av medisinsk invaliditet – `forskrifter/menerstatning/par-2.md`
- § 3. Utmåling av menerstatning – `forskrifter/menerstatning/par-3.md`
- § 4. Vedtak og utbetaling – `forskrifter/menerstatning/par-4.md`
- § 5. Ikrafttredelse – `forskrifter/menerstatning/par-5.md`

**Innhold utenfor paragrafene**

- Vedlegg, tabeller o.l. – `forskrifter/menerstatning/utenfor-paragrafene.md`

### Forskrift om yrkessykdommer, klimasykdommer og epidemiske sykdommer som skal likestilles med yrkesskade

- § 1. Yrkessykdommer som skal likestilles med yrkesskade – `forskrifter/yrkessykdommer/par-1.md`
- § 2. Klimasykdommer og epidemiske sykdommer som skal likestilles med yrkesskade – `forskrifter/yrkessykdommer/par-2.md`
- § 3. Ikrafttredelse – `forskrifter/yrkessykdommer/par-3.md`

### Forskrift om sykdommer og forgiftninger m.v. som skal likestilles med yrkesskade

- § 1. – `forskrifter/sykdommer-likestilt-yrkesskade/par-1.md`
- § 2. – `forskrifter/sykdommer-likestilt-yrkesskade/par-2.md`
- § 3. – `forskrifter/sykdommer-likestilt-yrkesskade/par-3.md`

### Forskrift om et rådgivende yrkessykdomsutvalg for regelmessig revisjon av forskrift over sykdommer som skal likestilles med yrkesskade

- § 1. Utvalgets leder, medlemmer og varamedlemmer – `forskrifter/radgivende-yrkessykdomsutvalg/par-1.md`
- § 2. Utvalgets oppgaver – `forskrifter/radgivende-yrkessykdomsutvalg/par-2.md`
- § 3. Utvalgets møter – møteledelse – sekretariat og arkiv – `forskrifter/radgivende-yrkessykdomsutvalg/par-3.md`
- § 4. Møteinnkallelse – saksdokumenter – `forskrifter/radgivende-yrkessykdomsutvalg/par-4.md`
- § 5. Beslutningsdyktighet – `forskrifter/radgivende-yrkessykdomsutvalg/par-5.md`
- § 6. Habilitet og taushetsplikt – `forskrifter/radgivende-yrkessykdomsutvalg/par-6.md`
- § 7. Møtereferat og avstemning – `forskrifter/radgivende-yrkessykdomsutvalg/par-7.md`
- § 8. Innkalling av rådgivere – `forskrifter/radgivende-yrkessykdomsutvalg/par-8.md`
- § 9. Ivaretakelse av visse oppgaver – `forskrifter/radgivende-yrkessykdomsutvalg/par-9.md`
- § 10. Ikrafttredelse – `forskrifter/radgivende-yrkessykdomsutvalg/par-10.md`

### Forskrift om beregning av uførepensjon og godskriving av pensjonspoeng ved yrkesskade

- § 1. Omfang – `forskrifter/beregning-uforepensjon-yrkesskade/par-1.md`
- § 2. Ytelser som delvis skyldes yrkesskade – `forskrifter/beregning-uforepensjon-yrkesskade/par-2.md`
- § 3. Ytterligere nedsatt inntektsevne – `forskrifter/beregning-uforepensjon-yrkesskade/par-3.md`
- § 4. Godskriving av pensjonspoeng når uførheten helt eller delvis skyldes yrkesskade – `forskrifter/beregning-uforepensjon-yrkesskade/par-4.md`
- § 5. Ikrafttredelse – `forskrifter/beregning-uforepensjon-yrkesskade/par-5.md`

### Forskrift om beregning av tilleggspensjon ved yrkesskade

- § 1. Personkrets – `forskrifter/tilleggspensjon-yrkesskade/par-1.md`
- § 2. Kravet til full opptjeningstid – `forskrifter/tilleggspensjon-yrkesskade/par-2.md`
- § 3. Pensjonsprosenten – `forskrifter/tilleggspensjon-yrkesskade/par-3.md`
- § 4. Fastsetting av poengtall når antatt årlig inntekt overstiger seks ganger grunnbeløpet – `forskrifter/tilleggspensjon-yrkesskade/par-4.md`
- § 5. Ikrafttredelse – `forskrifter/tilleggspensjon-yrkesskade/par-5.md`

### Forskrift om frivillig yrkesskadetrygd for selvstendig næringsdrivende og frilansere

- § 1. – `forskrifter/frivillig-yrkesskadetrygd-selvstendig/par-1.md`
- § 2. – `forskrifter/frivillig-yrkesskadetrygd-selvstendig/par-2.md`
- § 3. – `forskrifter/frivillig-yrkesskadetrygd-selvstendig/par-3.md`
- § 4. – `forskrifter/frivillig-yrkesskadetrygd-selvstendig/par-4.md`
- § 5. – `forskrifter/frivillig-yrkesskadetrygd-selvstendig/par-5.md`
- § 6. – `forskrifter/frivillig-yrkesskadetrygd-selvstendig/par-6.md`

### Forskrift om frivillig yrkesskadetrygd for elever som ikke er obligatorisk yrkesskadedekket

- § 1. – `forskrifter/frivillig-yrkesskadetrygd-elever/par-1.md`
- § 2. – `forskrifter/frivillig-yrkesskadetrygd-elever/par-2.md`
- § 3. – `forskrifter/frivillig-yrkesskadetrygd-elever/par-3.md`
- § 4. – `forskrifter/frivillig-yrkesskadetrygd-elever/par-4.md`
- § 5. – `forskrifter/frivillig-yrkesskadetrygd-elever/par-5.md`
- § 6. – `forskrifter/frivillig-yrkesskadetrygd-elever/par-6.md`
- § 7. – `forskrifter/frivillig-yrkesskadetrygd-elever/par-7.md`

### Forskrift om arbeidsavklaringspenger

- § 1. Virkeområde – `forskrifter/arbeidsavklaringspenger/par-1.md`
- § 2. Arbeidsrettet tiltak – `forskrifter/arbeidsavklaringspenger/par-2.md`
- § 3. Fravær fra fastsatt aktivitet – `forskrifter/arbeidsavklaringspenger/par-3.md`
- § 4. Reduksjon av arbeidsavklaringspenger ved brudd på nærmere bestemte aktivitetsplikter – `forskrifter/arbeidsavklaringspenger/par-4.md`
- § 5. (Opphevet) – `forskrifter/arbeidsavklaringspenger/par-5.md`
- § 6. Vedtaksperiode og oppfølging – `forskrifter/arbeidsavklaringspenger/par-6.md`
- § 7. Arbeidsavklaringspenger til studenter – `forskrifter/arbeidsavklaringspenger/par-7.md`
- § 8. Barnetillegg – `forskrifter/arbeidsavklaringspenger/par-8.md`
- § 9. Unntak fra avkortning for fosterforeldre – `forskrifter/arbeidsavklaringspenger/par-9.md`
- § 10. Arbeidsavklaringspenger når medlemmet er nær ved å komme i fullt arbeid – `forskrifter/arbeidsavklaringspenger/par-10.md`
- § 11. Reduksjon av arbeidsavklaringspenger på grunn av ytelser fra arbeidsgiver – `forskrifter/arbeidsavklaringspenger/par-11.md`
- § 12. Når medlemmet skal fortsette i den opprinnelige stønadsperioden – `forskrifter/arbeidsavklaringspenger/par-12.md`
- § 13. Utbetaling og forskuddsanvisning – `forskrifter/arbeidsavklaringspenger/par-13.md`
- § 14. Særlige bestemmelser for medlemmer som før 1. juli 2022 har fått arbeidsavklaringspenger utover ordinær stønadsperiode – `forskrifter/arbeidsavklaringspenger/par-14.md`
- § 15. (Opphevet) – `forskrifter/arbeidsavklaringspenger/par-15.md`
- § 16. Ikrafttredelse – `forskrifter/arbeidsavklaringspenger/par-16.md`

### Forskrift om stønad til hjelpemidler mv til bedring av funksjonsevnen i arbeidslivet og i dagliglivet og til ombygging av maskiner på arbeidsplassen

- § 1. Personkrets og formål – `forskrifter/hjelpemidler/par-1.md`
- § 2. Hjelpemidler, jf folketrygdloven § 10-7 første ledd bokstav a – `forskrifter/hjelpemidler/par-2.md`
- § 3. Grunnmønster til søm av klær, jf folketrygdloven § 10-7 første ledd bokstav c – `forskrifter/hjelpemidler/par-3.md`
- § 4. Førerhund, jf folketrygdloven § 10-7 første ledd bokstav d – `forskrifter/hjelpemidler/par-4.md`
- § 5. Ombygging av maskiner, jf folketrygdloven § 10-7 andre ledd – `forskrifter/hjelpemidler/par-5.md`
- § 6. Opplæringstiltak, jf folketrygdloven § 10-7 tredje ledd – `forskrifter/hjelpemidler/par-6.md`
- § 7. Reise- og oppholdsutgifter – `forskrifter/hjelpemidler/par-7.md`
- § 8. Andre bestemmelser – `forskrifter/hjelpemidler/par-8.md`
- § 9. Annen lovgivning – `forskrifter/hjelpemidler/par-9.md`
- § 10. Ikrafttredelse – `forskrifter/hjelpemidler/par-10.md`

### Forskrift om stønad til lese- og sekretærhjelp for blinde og svaksynte

- § 1. Personkrets, formål og omfang – `forskrifter/lese-sekretarhjelp/par-1.md`
- § 2. Beregning av takster og tid – `forskrifter/lese-sekretarhjelp/par-2.md`
- § 3. Reise- og oppholdsutgifter – `forskrifter/lese-sekretarhjelp/par-3.md`
- § 4. Oppgjørsform – `forskrifter/lese-sekretarhjelp/par-4.md`
- § 5. Forholdet til annen lovgivning – `forskrifter/lese-sekretarhjelp/par-5.md`
- § 6. Ikrafttredelse – `forskrifter/lese-sekretarhjelp/par-6.md`

### Forskrift om stønad til tolkehjelp for hørselshemmede

- § 1. Personkrets, formål og omfang – `forskrifter/tolkehjelp-horselshemmede/par-1.md`
- § 2. Vederlag – `forskrifter/tolkehjelp-horselshemmede/par-2.md`
- § 3. Reise- og oppholdsutgifter til tolk – `forskrifter/tolkehjelp-horselshemmede/par-3.md`
- § 4. Oppgjørsform – `forskrifter/tolkehjelp-horselshemmede/par-4.md`
- § 5. Forholdet til annen lovgivning – `forskrifter/tolkehjelp-horselshemmede/par-5.md`
- § 6. Ikrafttredelse – `forskrifter/tolkehjelp-horselshemmede/par-6.md`

### Forskrift om stønad til tolke- og ledsagerhjelp for døvblinde

- § 1. Personkrets, formål og omfang – `forskrifter/tolke-ledsagerhjelp-dovblinde/par-1.md`
- § 2. Vederlag – `forskrifter/tolke-ledsagerhjelp-dovblinde/par-2.md`
- § 3. Reise- og oppholdsutgifter til tolk – `forskrifter/tolke-ledsagerhjelp-dovblinde/par-3.md`
- § 4. Oppgjørsform – `forskrifter/tolke-ledsagerhjelp-dovblinde/par-4.md`
- § 5. Forholdet til annen lovgivning – `forskrifter/tolke-ledsagerhjelp-dovblinde/par-5.md`
- § 7. Ikrafttredelse – `forskrifter/tolke-ledsagerhjelp-dovblinde/par-7.md`

### Forskrift om stønad til dekning av utgifter til ortopediske hjelpemidler, brystprotese, ansiktsdefektprotese, øyeprotese og parykk

**I Ortopediske hjelpemidler**

- § 1. – `forskrifter/ortopediske-hjelpemidler/par-1.md`
- § 2. – `forskrifter/ortopediske-hjelpemidler/par-2.md`
- § 3. – `forskrifter/ortopediske-hjelpemidler/par-3.md`
- § 4. – `forskrifter/ortopediske-hjelpemidler/par-4.md`

**II Brystprotese, ansiktsdefektprotese, øyeprotese og parykk**

- § 5. Brystprotese – `forskrifter/ortopediske-hjelpemidler/par-5.md`
- § 6. Ansiktsdefektprotese – `forskrifter/ortopediske-hjelpemidler/par-6.md`
- § 7. Øyeprotese – `forskrifter/ortopediske-hjelpemidler/par-7.md`
- § 8. Parykk – `forskrifter/ortopediske-hjelpemidler/par-8.md`

**III Standardprodukter**

- § 9. – `forskrifter/ortopediske-hjelpemidler/par-9.md`
- § 9a. – `forskrifter/ortopediske-hjelpemidler/par-9a.md`

**IV Fellesbestemmelser**

- § 10. – `forskrifter/ortopediske-hjelpemidler/par-10.md`
- § 11. – `forskrifter/ortopediske-hjelpemidler/par-11.md`
- § 12. – `forskrifter/ortopediske-hjelpemidler/par-12.md`
- § 13. – `forskrifter/ortopediske-hjelpemidler/par-13.md`
- § 14. – `forskrifter/ortopediske-hjelpemidler/par-14.md`

### Forskrift om stønad til høreapparat og tinnitusmaskerer

**I Høreapparat**

- § 1. Personkrets – `forskrifter/horeapparat/par-1.md`
- § 2. Stønadsomfang – `forskrifter/horeapparat/par-2.md`
- § 3. Gjenanskaffelse – `forskrifter/horeapparat/par-3.md`
- § 4. Søknad om stønad til høreapparat – `forskrifter/horeapparat/par-4.md`
- § 5. Undersøkelse og tilpasning – `forskrifter/horeapparat/par-5.md`
- § 6. Avtaler om pris og levering – `forskrifter/horeapparat/par-6.md`
- § 7. Eiendomsforhold – `forskrifter/horeapparat/par-7.md`
- § 8. Stønad til høreapparat – `forskrifter/horeapparat/par-8.md`
- § 9. Legeundersøkelse – `forskrifter/horeapparat/par-9.md`
- § 10. Reiseutgifter – `forskrifter/horeapparat/par-10.md`
- § 11. Gjennomføring – `forskrifter/horeapparat/par-11.md`

**II Tinnitusmaskerer**

- § 12. Stønad til tinnitusmaskerer – `forskrifter/horeapparat/par-12.md`

**III Ikrafttredelse**

- § 13. Ikrafttredelse – `forskrifter/horeapparat/par-13.md`

### Forskrift om stønad til motorkjøretøy eller annet transportmiddel

- § 1. Personkrets og formål – `forskrifter/motorkjoretoy/par-1.md`
- § 2. Definisjoner – `forskrifter/motorkjoretoy/par-2.md`
- § 3. Alminnelige vilkår for stønad til anskaffelse av motorkjøretøy mv. – `forskrifter/motorkjoretoy/par-3.md`
- § 4. Kjøretøy til attføringstiltak eller ved overtagelse av tilbudt arbeid – `forskrifter/motorkjoretoy/par-4.md`
- § 5. Regler for valg av kjøretøy – `forskrifter/motorkjoretoy/par-5.md`
- § 6. Rammeavtaler og prisramme – `forskrifter/motorkjoretoy/par-6.md`
- § 7. Registrering av kjøretøyet. Førerkort – `forskrifter/motorkjoretoy/par-7.md`
- § 8. Vilkår for gjenanskaffelse – `forskrifter/motorkjoretoy/par-8.md`
- § 9. Stønad til anskaffelse av kjøretøy – `forskrifter/motorkjoretoy/par-9.md`
- § 10. Utbetaling av stønad – `forskrifter/motorkjoretoy/par-10.md`
- § 11. Tilskudd til spesialutstyr og ombygging – `forskrifter/motorkjoretoy/par-11.md`
- § 12. Kjøreopplæring – `forskrifter/motorkjoretoy/par-12.md`
- § 13. Dekning av reise- og oppholdsutgifter – `forskrifter/motorkjoretoy/par-13.md`
- § 14. Reparasjoner – `forskrifter/motorkjoretoy/par-14.md`
- § 15. Gjeldsoppgjør – `forskrifter/motorkjoretoy/par-15.md`
- § 16. Andre bestemmelser – `forskrifter/motorkjoretoy/par-16.md`
- § 17. Grunnstønad – `forskrifter/motorkjoretoy/par-17.md`
- § 18. Alderspensjon – `forskrifter/motorkjoretoy/par-18.md`
- § 19. Forholdet til annen lovgivning – `forskrifter/motorkjoretoy/par-19.md`
- § 20. Ikrafttredelse – `forskrifter/motorkjoretoy/par-20.md`

### Forskrift om stønad til briller til barn

- § 1. Virkeområde – `forskrifter/briller-barn/par-1.md`
- § 2. Vilkår for rett til stønad – `forskrifter/briller-barn/par-2.md`
- § 3. Antall briller – `forskrifter/briller-barn/par-3.md`
- § 4. Stønadens størrelse – `forskrifter/briller-barn/par-4.md`
- § 5. Søknad på særskilt grunnlag – `forskrifter/briller-barn/par-5.md`
- § 6. Framsetting av krav – `forskrifter/briller-barn/par-6.md`
- § 7. Krav til dokumentasjon – `forskrifter/briller-barn/par-7.md`
- § 8. Unntak fra underretning om vedtak – `forskrifter/briller-barn/par-8.md`
- § 9. Utbetaling – `forskrifter/briller-barn/par-9.md`
- § 10. Retningslinjer – `forskrifter/briller-barn/par-10.md`
- § 11. Ikrafttredelse – `forskrifter/briller-barn/par-11.md`

### Forskrift om adgang til å utbetale uredusert ytelse for visse persongrupper i institusjon

- § 1. Personkrets – `forskrifter/uredusert-ytelse-institusjon/par-1.md`
- § 2. Krav til innhold i avtale – `forskrifter/uredusert-ytelse-institusjon/par-2.md`
- § 3. Vedtak om å utbetale uredusert ytelse – `forskrifter/uredusert-ytelse-institusjon/par-3.md`
- § 4. Ikrafttredelse – `forskrifter/uredusert-ytelse-institusjon/par-4.md`

### Forskrift om beregning av uføretrygd og pensjon mv. under opphold i institusjon

- § 1. Beregning av graderte ytelser – `forskrifter/uforetrygd-institusjon/par-1.md`
- § 2. Tillegg for faste utgifter – `forskrifter/uforetrygd-institusjon/par-2.md`
- § 3. Maksimal ytelse – `forskrifter/uforetrygd-institusjon/par-3.md`
- § 4. Ikrafttredelse – `forskrifter/uforetrygd-institusjon/par-4.md`

### Forskrift om overgangsregler for beregning av redusert ytelse under opphold i institusjon og under straffegjennomføring

- § 1. Virkeområde – `forskrifter/overgangsregler-institusjon/par-1.md`
- § 2. Overgang til nye regler – `forskrifter/overgangsregler-institusjon/par-2.md`
- § 3. Ytelser som er redusert per 31. desember 2014 – `forskrifter/overgangsregler-institusjon/par-3.md`
- § 4. Ytelser som ikke er redusert per 31. desember 2014 – 12 måneders varighet på oppholdet – `forskrifter/overgangsregler-institusjon/par-4.md`
- § 5. Ikrafttredelse – `forskrifter/overgangsregler-institusjon/par-5.md`

### Forskrift om gradering av pleiepenger

- § 1. Virkeområde – `forskrifter/gradering-pleiepenger/par-1.md`
- § 2. Definisjoner – `forskrifter/gradering-pleiepenger/par-2.md`
- § 3. Fastsetting av pleiepengegrad – `forskrifter/gradering-pleiepenger/par-3.md`
- § 4. Tap av pensjonsgivende inntekt – `forskrifter/gradering-pleiepenger/par-4.md`
- § 5. Gradering når to omsorgspersoner tar ut graderte pleiepenger samtidig – `forskrifter/gradering-pleiepenger/par-5.md`
- § 6. Ikrafttredelse – `forskrifter/gradering-pleiepenger/par-6.md`

### Forskrift om beregning av uføretrygd etter EØS-avtalen

- § 1. Virkeområde – `forskrifter/eos-beregning-uforetrygd/par-1.md`
- § 2. Fastsetting av grunnlaget for beregning av uføretrygd – `forskrifter/eos-beregning-uforetrygd/par-2.md`
- § 3. Minste årlig ytelse – `forskrifter/eos-beregning-uforetrygd/par-3.md`
- § 4. Teoretisk beløp – `forskrifter/eos-beregning-uforetrygd/par-4.md`
- § 5. Faktisk beløp – `forskrifter/eos-beregning-uforetrygd/par-5.md`
- § 6. Ikrafttredelse – `forskrifter/eos-beregning-uforetrygd/par-6.md`

### Forskrift om unntak fra vilkåret om legeerklæring når kiropraktorer og manuellterapeuter dokumenterer arbeidsuførheten med erklæring

- § 1. Retten til å dokumentere arbeidsuførhet – `forskrifter/legeerklaering-kiropraktor-manuellterapeut/par-1.md`
- § 2. Erklæring om arbeidsuførhet – `forskrifter/legeerklaering-kiropraktor-manuellterapeut/par-2.md`
- § 3. Utfyllende retningslinjer – `forskrifter/legeerklaering-kiropraktor-manuellterapeut/par-3.md`
- § 4. Ikrafttredelse – `forskrifter/legeerklaering-kiropraktor-manuellterapeut/par-4.md`

### Forskrift om obligatorisk opplæring i sykmeldingsarbeid for leger

- § 1. Formål – `forskrifter/opplaering-sykmeldingsarbeid/par-1.md`
- § 2. Målgrupper – `forskrifter/opplaering-sykmeldingsarbeid/par-2.md`
- § 3. Retten til å dokumentere arbeidsuførhet – `forskrifter/opplaering-sykmeldingsarbeid/par-3.md`
- § 4. Innhold og omfang – `forskrifter/opplaering-sykmeldingsarbeid/par-4.md`
- § 5. Ikrafttredelse – `forskrifter/opplaering-sykmeldingsarbeid/par-5.md`

### Forskrift om forsikring mot ansvar for sykepenger i arbeidsgiverperioden for små bedrifter

- § 1. Forsikringsvilkår – premie og premiegrunnlag – `forskrifter/forsikring-arbeidsgiverperioden/par-1.md`
- § 2. Premie – `forskrifter/forsikring-arbeidsgiverperioden/par-2.md`
- § 3. Forsikringens opphør – premieavregning – `forskrifter/forsikring-arbeidsgiverperioden/par-3.md`
- § 4. Ikrafttredelse – `forskrifter/forsikring-arbeidsgiverperioden/par-4.md`

### Forskrift om forsikring for tillegg til sykepenger for selvstendig næringsdrivende

- § 1. Premie og premiegrunnlag – `forskrifter/forsikring-sykepenger-selvstendige/par-1.md`
- § 2. Endring av premiegrunnlaget – `forskrifter/forsikring-sykepenger-selvstendige/par-2.md`
- § 3. Premiesatser – `forskrifter/forsikring-sykepenger-selvstendige/par-3.md`
- § 4. Premiefritak – `forskrifter/forsikring-sykepenger-selvstendige/par-4.md`
- § 5. Ikrafttredelse – `forskrifter/forsikring-sykepenger-selvstendige/par-5.md`

### Forskrift om forsikring for tillegg til sykepenger for frilansere

- § 1. Premie og premiegrunnlag – `forskrifter/forsikring-sykepenger-frilansere/par-1.md`
- § 2. Endring av premiegrunnlaget – `forskrifter/forsikring-sykepenger-frilansere/par-2.md`
- § 3. Premiesatser – `forskrifter/forsikring-sykepenger-frilansere/par-3.md`
- § 4. Premiefritak – `forskrifter/forsikring-sykepenger-frilansere/par-4.md`
- § 5. Ikrafttredelse – `forskrifter/forsikring-sykepenger-frilansere/par-5.md`

### Forskrift om stønad til dekning av utgifter til helsetjenester i utlandet

- § 1. – `forskrifter/helsetjenester-utlandet/par-1.md`
- § 2. – `forskrifter/helsetjenester-utlandet/par-2.md`
- § 3. – `forskrifter/helsetjenester-utlandet/par-3.md`
- § 4. – `forskrifter/helsetjenester-utlandet/par-4.md`
- § 5. – `forskrifter/helsetjenester-utlandet/par-5.md`

### Forskrift om utvidet stønad til helsetjenester under opphold i utlandet

- § 1. Område – `forskrifter/utvidet-helsetjenester-utlandet/par-1.md`
- § 2. Personkrets – `forskrifter/utvidet-helsetjenester-utlandet/par-2.md`
- § 3. Utvidet stønad – `forskrifter/utvidet-helsetjenester-utlandet/par-3.md`
- § 4. Egenandeler og egenandelstak i utlandet – `forskrifter/utvidet-helsetjenester-utlandet/par-4.md`
- § 5. Oppholdsutgifter under fravær fra hjemmet – `forskrifter/utvidet-helsetjenester-utlandet/par-5.md`
- § 6. Opphør av rett til utvidet stønad til helsetjenester – `forskrifter/utvidet-helsetjenester-utlandet/par-6.md`
- § 7. Ikrafttredelse – `forskrifter/utvidet-helsetjenester-utlandet/par-7.md`

### Forskrift om overgangsregler i forbindelse med endringer i folketrygdloven kapittel 15, 16 og 17 fra 1. januar 2016

- § 1. Stønad under utenlandsopphold – `forskrifter/overgangsregler-kap15-17-2016/par-1.md`
- § 2. Enslig mor eller far – `forskrifter/overgangsregler-kap15-17-2016/par-2.md`
- § 3. Omstillingstid etter skilsmisse, separasjon eller samlivsbrudd mellom ugifte foreldre – `forskrifter/overgangsregler-kap15-17-2016/par-3.md`
- § 4. Brukerkontakt – `forskrifter/overgangsregler-kap15-17-2016/par-4.md`
- § 5. Utdanning som vilkår for overgangsstønad – `forskrifter/overgangsregler-kap15-17-2016/par-5.md`
- § 6. Midlertidig bortfall og utestenging – `forskrifter/overgangsregler-kap15-17-2016/par-6.md`
- § 7. Stønad til barnetilsyn – `forskrifter/overgangsregler-kap15-17-2016/par-7.md`
- § 8. Utdanningsstønad – `forskrifter/overgangsregler-kap15-17-2016/par-8.md`
- § 9. Tidligere familiepleier og gjenlevende – `forskrifter/overgangsregler-kap15-17-2016/par-9.md`
- § 10. Ikrafttredelse – `forskrifter/overgangsregler-kap15-17-2016/par-10.md`

## EU-rettsakter som teksten viser til

Funnet automatisk ved søk etter rettsaktnummer. Stier til `regelverk/eu/` er fra roten av basen.

- **Forordning nr. 883/2004** (Trygdeforordningen) – i basen: `regelverk/eu/forordning-883-2004/VEIVISER.md`. Nevnt i `forskrifter/dagpengeforskriften/par-1-7.md`, `forskrifter/dagpengeforskriften/par-1-8.md`, `forskrifter/dagpengeforskriften/par-1-9.md`, `forskrifter/dagpengeforskriften/utenfor-paragrafene.md`, `forskrifter/eos-beregning-arbeidsavklaringspenger/par-1.md`, `forskrifter/eos-beregning-uforetrygd/par-1.md`, `forskrifter/omregning-uforepensjon-til-uforetrygd/par-4.md`, `lov/par-1-3a.md`
- **Forordning nr. 987/2009** (Gjennomføringsforordningen til trygdeforordningen) – i basen: `regelverk/eu/forordning-987-2009/VEIVISER.md`. Nevnt i `forskrifter/eos-beregning-arbeidsavklaringspenger/par-1.md`, `forskrifter/eos-beregning-uforetrygd/par-1.md`, `lov/par-1-3a.md`
- Forordning nr. 1408/71 – ikke i basen. Nevnt i `forskrifter/bilaterale-trygdeavtaler/par-1.md`, `forskrifter/omregning-uforepensjon-til-uforetrygd/par-4.md`
- Forordning nr. 988/2009 – ikke i basen. Nevnt i `lov/par-1-3a.md`
- Forordning nr. 1244/2010 – ikke i basen. Nevnt i `lov/par-1-3a.md`
- Forordning nr. 1224/2012 – ikke i basen. Nevnt i `lov/par-1-3a.md`
- Forordning nr. 465/2012 – ikke i basen. Nevnt i `lov/par-1-3a.md`
- Forordning nr. 1372/2013 – ikke i basen. Nevnt i `lov/par-1-3a.md`
- Forordning nr. 517/2013 – ikke i basen. Nevnt i `lov/par-1-3a.md`
- Forordning nr. 1368/2014 – ikke i basen. Nevnt i `lov/par-1-3a.md`
- Forordning 2017/492 – ikke i basen. Nevnt i `lov/par-1-3a.md`
- Forordning 2019/1149 – ikke i basen. Nevnt i `lov/par-1-3a.md`

## Andre kilder

Dette er ikke lov- eller forskriftstekst.

### Merknader

- Arbeidsavklaringspenger og tilleggsstønader (kap. 11 og 11 A) – `merknader/aap.md`
- Dagpenger (kap. 4) – `merknader/dagpenger.md`
- Etterlatte og gravferd (kap. 7, 16, 17, 17 A og 18) – `merknader/etterlatte-gravferd.md`
- Folketrygdloven – sykepenger og pleiepenger (kap. 8 og 9) – `merknader/sykepenger.md`
- Folketrygdloven – uføretrygd (kap. 12) – `merknader/uforetrygd.md`

### Rundskriv

- `rundskriv/forskrifter/aa-registeret/` – 23 filer, start med `rundskriv/forskrifter/aa-registeret/oversikt.md`
- `rundskriv/forskrifter/ekspertbistand/` – 12 filer, start med `rundskriv/forskrifter/ekspertbistand/oversikt.md`
- `rundskriv/forskrifter/okt-beregningsgrunnlag-gift-samboende/` – 6 filer, start med `rundskriv/forskrifter/okt-beregningsgrunnlag-gift-samboende/oversikt.md`
- `rundskriv/forskrifter/omregning-uforepensjon-til-uforetrygd/` – 9 filer, start med `rundskriv/forskrifter/omregning-uforepensjon-til-uforetrygd/oversikt.md`
- `rundskriv/forskrifter/omsorgspoeng/` – 5 filer, start med `rundskriv/forskrifter/omsorgspoeng/oversikt.md`
- `rundskriv/forskrifter/omsorgspoeng-omsorgsarbeid/` – 10 filer, start med `rundskriv/forskrifter/omsorgspoeng-omsorgsarbeid/oversikt.md`
- `rundskriv/forskrifter/opplysningsplikt-arbeidsgiver/` – 6 filer, start med `rundskriv/forskrifter/opplysningsplikt-arbeidsgiver/oversikt.md`
- `rundskriv/forskrifter/overgangsregler-institusjon/` – 7 filer, start med `rundskriv/forskrifter/overgangsregler-institusjon/oversikt.md`
- `rundskriv/forskrifter/overgangsregler-kap15-17-2016/` – 12 filer, start med `rundskriv/forskrifter/overgangsregler-kap15-17-2016/oversikt.md`
- `rundskriv/forskrifter/uforetrygdforskriften/` – 6 filer, start med `rundskriv/forskrifter/uforetrygdforskriften/oversikt.md`
- `rundskriv/forskrifter/uredusert-ytelse-institusjon/` – 6 filer, start med `rundskriv/forskrifter/uredusert-ytelse-institusjon/oversikt.md`
- `rundskriv/forskrifter/yrkessykdommer/` – 2 filer, start med `rundskriv/forskrifter/yrkessykdommer/oversikt.md`
- `rundskriv/rundskriv-r01-00/` – 14 filer, start med `rundskriv/rundskriv-r01-00/oversikt.md`
- `rundskriv/rundskriv-r02-00/` – 20 filer, start med `rundskriv/rundskriv-r02-00/oversikt.md`
- `rundskriv/rundskriv-r03-00/` – 2 filer, start med `rundskriv/rundskriv-r03-00/oversikt.md`
- `rundskriv/rundskriv-r03-01/` – 9 filer, start med `rundskriv/rundskriv-r03-01/oversikt.md`
- `rundskriv/rundskriv-r03-02/` – 11 filer, start med `rundskriv/rundskriv-r03-02/oversikt.md`
- `rundskriv/rundskriv-r03-03/` – 8 filer, start med `rundskriv/rundskriv-r03-03/oversikt.md`
- `rundskriv/rundskriv-r03-04/` – 3 filer, start med `rundskriv/rundskriv-r03-04/oversikt.md`
- `rundskriv/rundskriv-r03-05/` – 5 filer, start med `rundskriv/rundskriv-r03-05/oversikt.md`
- `rundskriv/rundskriv-r04-00/` – 29 filer, start med `rundskriv/rundskriv-r04-00/oversikt.md`
- `rundskriv/rundskriv-r05-00/` – 3 filer, start med `rundskriv/rundskriv-r05-00/oversikt.md`
- `rundskriv/rundskriv-r05-01a/` – 2 filer, start med `rundskriv/rundskriv-r05-01a/oversikt.md`
- `rundskriv/rundskriv-r05-02/` – 2 filer, start med `rundskriv/rundskriv-r05-02/oversikt.md`
- `rundskriv/rundskriv-r05-03/` – 8 filer, start med `rundskriv/rundskriv-r05-03/oversikt.md`
- `rundskriv/rundskriv-r05-03d1/` – 9 filer, start med `rundskriv/rundskriv-r05-03d1/oversikt.md`
- `rundskriv/rundskriv-r05-03d2/` – 8 filer, start med `rundskriv/rundskriv-r05-03d2/oversikt.md`
- `rundskriv/rundskriv-r05-05-for-1702/` – 2 filer, start med `rundskriv/rundskriv-r05-05-for-1702/oversikt.md`
- `rundskriv/rundskriv-r05-07/` – 5 filer, start med `rundskriv/rundskriv-r05-07/oversikt.md`
- `rundskriv/rundskriv-r05-08/` – 6 filer, start med `rundskriv/rundskriv-r05-08/oversikt.md`
- `rundskriv/rundskriv-r05-09/` – 8 filer, start med `rundskriv/rundskriv-r05-09/oversikt.md`
- `rundskriv/rundskriv-r05-10/` – 6 filer, start med `rundskriv/rundskriv-r05-10/oversikt.md`
- `rundskriv/rundskriv-r05-10a/` – 7 filer, start med `rundskriv/rundskriv-r05-10a/oversikt.md`
- `rundskriv/rundskriv-r05-12/` – 7 filer, start med `rundskriv/rundskriv-r05-12/oversikt.md`
- `rundskriv/rundskriv-r05-13/` – 3 filer, start med `rundskriv/rundskriv-r05-13/oversikt.md`
- `rundskriv/rundskriv-r05-14-01/` – 12 filer, start med `rundskriv/rundskriv-r05-14-01/oversikt.md`
- `rundskriv/rundskriv-r05-14-02/` – 12 filer, start med `rundskriv/rundskriv-r05-14-02/oversikt.md`
- `rundskriv/rundskriv-r05-14-03/` – 11 filer, start med `rundskriv/rundskriv-r05-14-03/oversikt.md`
- `rundskriv/rundskriv-r05-21/` – 5 filer, start med `rundskriv/rundskriv-r05-21/oversikt.md`
- `rundskriv/rundskriv-r05-22/` – 2 filer, start med `rundskriv/rundskriv-r05-22/oversikt.md`
- `rundskriv/rundskriv-r05-24/` – 2 filer, start med `rundskriv/rundskriv-r05-24/oversikt.md`
- `rundskriv/rundskriv-r05-24a-for/` – 15 filer, start med `rundskriv/rundskriv-r05-24a-for/oversikt.md`
- `rundskriv/rundskriv-r05-25/` – 12 filer, start med `rundskriv/rundskriv-r05-25/oversikt.md`
- `rundskriv/rundskriv-r05-26/` – 2 filer, start med `rundskriv/rundskriv-r05-26/oversikt.md`
- `rundskriv/rundskriv-r06-00/` – 14 filer, start med `rundskriv/rundskriv-r06-00/oversikt.md`
- `rundskriv/rundskriv-r06-04-for/` – 2 filer, start med `rundskriv/rundskriv-r06-04-for/oversikt.md`
- `rundskriv/rundskriv-r07-00/` – 8 filer, start med `rundskriv/rundskriv-r07-00/oversikt.md`
- `rundskriv/rundskriv-r08-00/` – 93 filer, start med `rundskriv/rundskriv-r08-00/oversikt.md`
- `rundskriv/rundskriv-r09-00/` – 25 filer, start med `rundskriv/rundskriv-r09-00/oversikt.md`
- `rundskriv/rundskriv-r10-00/` – 8 filer, start med `rundskriv/rundskriv-r10-00/oversikt.md`
- `rundskriv/rundskriv-r10-07/` – 2 filer, start med `rundskriv/rundskriv-r10-07/oversikt.md`
- `rundskriv/rundskriv-r10-07-4-5-ledd/` – 3 filer, start med `rundskriv/rundskriv-r10-07-4-5-ledd/oversikt.md`
- `rundskriv/rundskriv-r10-07-for/` – 12 filer, start med `rundskriv/rundskriv-r10-07-for/oversikt.md`
- `rundskriv/rundskriv-r10-07a/` – 9 filer, start med `rundskriv/rundskriv-r10-07a/oversikt.md`
- `rundskriv/rundskriv-r10-07acd/` – 4 filer, start med `rundskriv/rundskriv-r10-07acd/oversikt.md`
- `rundskriv/rundskriv-r10-07b/` – 12 filer, start med `rundskriv/rundskriv-r10-07b/oversikt.md`
- `rundskriv/rundskriv-r10-07e/` – 6 filer, start med `rundskriv/rundskriv-r10-07e/oversikt.md`
- `rundskriv/rundskriv-r10-07f/` – 7 filer, start med `rundskriv/rundskriv-r10-07f/oversikt.md`
- `rundskriv/rundskriv-r10-07g/` – 7 filer, start med `rundskriv/rundskriv-r10-07g/oversikt.md`
- `rundskriv/rundskriv-r10-07h/` – 18 filer, start med `rundskriv/rundskriv-r10-07h/oversikt.md`
- `rundskriv/rundskriv-r10-07i/` – 2 filer, start med `rundskriv/rundskriv-r10-07i/oversikt.md`
- `rundskriv/rundskriv-r11-00/` – 36 filer, start med `rundskriv/rundskriv-r11-00/oversikt.md`
- `rundskriv/rundskriv-r11a-00/` – 7 filer, start med `rundskriv/rundskriv-r11a-00/oversikt.md`
- `rundskriv/rundskriv-r11a-00-for/` – 18 filer, start med `rundskriv/rundskriv-r11a-00-for/oversikt.md`
- `rundskriv/rundskriv-r12-00/` – 45 filer, start med `rundskriv/rundskriv-r12-00/oversikt.md`
- `rundskriv/rundskriv-r12-15-for/` – 5 filer, start med `rundskriv/rundskriv-r12-15-for/oversikt.md`
- `rundskriv/rundskriv-r12-19-for-1376/` – 6 filer, start med `rundskriv/rundskriv-r12-19-for-1376/oversikt.md`
- `rundskriv/rundskriv-r13-00/` – 24 filer, start med `rundskriv/rundskriv-r13-00/oversikt.md`
- `rundskriv/rundskriv-r14-00/` – 41 filer, start med `rundskriv/rundskriv-r14-00/oversikt.md`
- `rundskriv/rundskriv-r15-00/` – 15 filer, start med `rundskriv/rundskriv-r15-00/oversikt.md`
- `rundskriv/rundskriv-r15-00-for-1361/` – 16 filer, start med `rundskriv/rundskriv-r15-00-for-1361/oversikt.md`
- `rundskriv/rundskriv-r15-08/` – 2 filer, start med `rundskriv/rundskriv-r15-08/oversikt.md`
- `rundskriv/rundskriv-r16-00/` – 15 filer, start med `rundskriv/rundskriv-r16-00/oversikt.md`
- `rundskriv/rundskriv-r17-00/` – 19 filer, start med `rundskriv/rundskriv-r17-00/oversikt.md`
- `rundskriv/rundskriv-r18-00/` – 13 filer, start med `rundskriv/rundskriv-r18-00/oversikt.md`
- `rundskriv/rundskriv-r19-00/` – 77 filer, start med `rundskriv/rundskriv-r19-00/oversikt.md`
- `rundskriv/rundskriv-r20-00/` – 81 filer, start med `rundskriv/rundskriv-r20-00/oversikt.md`
- `rundskriv/rundskriv-r21-00/` – 33 filer, start med `rundskriv/rundskriv-r21-00/oversikt.md`
- `rundskriv/rundskriv-r21-00b/` – 13 filer, start med `rundskriv/rundskriv-r21-00b/oversikt.md`
- `rundskriv/rundskriv-r22-00/` – 25 filer, start med `rundskriv/rundskriv-r22-00/oversikt.md`
- `rundskriv/rundskriv-r23-00/` – 18 filer, start med `rundskriv/rundskriv-r23-00/oversikt.md`
- `rundskriv/rundskriv-r24-00/` – 4 filer, start med `rundskriv/rundskriv-r24-00/oversikt.md`
- `rundskriv/rundskriv-r25-00/` – 19 filer, start med `rundskriv/rundskriv-r25-00/oversikt.md`
- `rundskriv/rundskriv-r25-03-for/` – 8 filer, start med `rundskriv/rundskriv-r25-03-for/oversikt.md`
- `rundskriv/rundskriv-r25-16-for-368/` – 39 filer, start med `rundskriv/rundskriv-r25-16-for-368/oversikt.md`
- `rundskriv/rundskriv-r26-00/` – 117 filer, start med `rundskriv/rundskriv-r26-00/oversikt.md`
- `rundskriv/sivilombudet/` – 74 filer, start med `rundskriv/sivilombudet/oversikt.md`
<!-- AUTO-SLUTT -->
