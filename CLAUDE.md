# Regelverksbasen

Dette repoet er en felles base med lover og forskrifter. Du (Claude) kommer hit fordi en bruker har stilt et spørsmål som kan kreve regelverk, og peker-skillen har sendt deg hit.

## Slik henter du filer

Alle stier i basen er relative til rotadressen:

```
https://raw.githubusercontent.com/tarjeiha/allover/main/
```

Hent med `curl -sL <adresse>` i kodeverktøyet hvis du har det, ellers med nettleser- eller hentverktøyet ditt. Hent bare filene du trenger. Hvis hentingen feiler, si det til brukeren og svar ikke fra hukommelsen.

## Slik finner du fram

Repoet har fem deler. Skriveregler og nynorsk ligger under `sprak/` (start i `sprak/VEIVISER.md`). Lover, forskrifter, tariffavtaler og EU-rettsakter ligger under `regelverk/`, og resten av denne filen gjelder dem. Statsbudsjettet ligger under `budsjett/` (start i `budsjett/VEIVISER.md`), og en katalog over hvor tall og statistikk finnes ligger under `data/` (start i `data/VEIVISER.md`). Stortingets anmodningsvedtak, spørsmål, interpellasjoner og representantforslag ligger under `stortinget/` (start i `stortinget/VEIVISER.md`, og bruk søkeskriptet der).

Basen har tre nivåer. Gå ikke dypere enn nødvendig.

1. **Denne filen**: hvilke regelverk som finnes, og reglene for svar.
2. **`regelverk/<regelverk>/VEIVISER.md`**: hva regelverket gjelder, kjente feller, hvilke merknader som finnes, og en liste over alle paragrafer med stien til filen.
3. **Paragraffilene**: selve lov- og forskriftsteksten, én fil per paragraf.

Noen regelverk har også `rundskriv/` (rundskriv, lagt inn via innboksen eller hentet manuelt) og `merknader/` (hjelpetekst for bestemte temaer). Rundskriv er ikke lov- eller forskriftstekst. Si fra i svaret når du bygger på et rundskriv, og oppgi det med navn. Merknadene er ikke en kilde, se regel 9.

Basen har også to typer kilder som ikke er norsk lov eller forskrift, se tabellene under regelverkslisten:

- **Tariffavtaler** (`regelverk/hovedtariffavtalen/`): avtaletekst. Si at svaret bygger på tariffavtalen.
- **EU-rettsakter** (`regelverk/eu/`): EU-tekst fra EUR-Lex, oftest på engelsk. Veiviseren for hver rettsakt sier hvilken versjon som ligger i basen og om den er kontrollert mot EØS-avtalen. En EU-versjon kan inneholde endringer som ennå ikke gjelder i Norge. Si fra om det når det kan ha betydning, og oversett selv når du forklarer på norsk. Veiviserne til lovene lister hvilke EU-rettsakter lov- og forskriftsteksten viser til.

Vedtatte lov- og forskriftsendringer som ikke er i kraft ennå, hentes fra Norsk Lovtidend ved hvert bygg. De står i veiviseren under «Vedtatte endringer som ikke er i kraft», som et varsel øverst i hver paragraffil som berøres, og med ny ordlyd i `regelverk/<regelverk>/vedtatte-endringer/`.

Vet du allerede hvilken paragraf det gjelder, kan du gå rett til filen. `indeks.tsv` har alle paragrafer i basen med sti, og kan brukes til å søke på tvers av regelverkene.

## Regelverk i basen

<!-- AUTO-START: genereres av verktoy/bygg.py, ikke rediger for hånd -->
| Regelverk | Veiviser | Sist endret i kraft |
|---|---|---|
| Offentleglova | `regelverk/offentleglova/VEIVISER.md` | 2026-07-01 |
| AFP-loven for medlemmer av Statens pensjonskasse | `regelverk/afp-loven/VEIVISER.md` | 2026-01-01 |
| Aldersgrenseloven for statsansatte | `regelverk/aldersgrenseloven/VEIVISER.md` | 2026-01-01 |
| Allmenngjøringsloven | `regelverk/allmenngjoringsloven/VEIVISER.md` | 2025-07-01 |
| Arbeidsmarkedsloven | `regelverk/arbeidsmarkedsloven/VEIVISER.md` | 2024-12-20 |
| Arbeidsmiljøloven | `regelverk/arbeidsmiljoloven/VEIVISER.md` | 2026-07-01 |
| Arbeidstvistloven | `regelverk/arbeidstvistloven/VEIVISER.md` | 2024-01-01 |
| Arkivlova | `regelverk/arkivlova/VEIVISER.md` | 2026-01-01, Kongen fastset |
| Diskrimineringsombudsloven | `regelverk/diskrimineringsombudsloven/VEIVISER.md` | 2026-01-01 |
| Ferieloven | `regelverk/ferieloven/VEIVISER.md` | 2024-01-01 |
| Folketrygdloven | `regelverk/folketrygdloven/VEIVISER.md` | 2026-10-01 |
| Forvaltningsloven | `regelverk/forvaltningsloven/VEIVISER.md` | 2026-01-01 · **vedtatte endringer venter** |
| Forvaltningsloven 2025 (ny lov, ikke i kraft) | `regelverk/forvaltningsloven-2025/VEIVISER.md` | Ikke i kraft (Kongen bestemmer) |
| Integreringsloven | `regelverk/integreringsloven/VEIVISER.md` | 2026-07-01 |
| Karanteneloven | `regelverk/karanteneloven/VEIVISER.md` | 2025-07-01 |
| Likestillings- og diskrimineringsloven | `regelverk/likestillings-og-diskrimineringsloven/VEIVISER.md` | 2024-07-01 |
| Lov om Statens pensjonskasse | `regelverk/spk-loven/VEIVISER.md` | 2026-01-01 |
| Lønnsgarantiloven | `regelverk/lonnsgarantiloven/VEIVISER.md` | 2026-01-01 |
| NAV-loven | `regelverk/nav-loven/VEIVISER.md` | 2026-01-01 |
| Opplæringslova | `regelverk/opplaeringslova/VEIVISER.md` | 2026-08-01 · **vedtatte endringer venter** |
| Permitteringslønnsloven | `regelverk/permitteringslonnsloven/VEIVISER.md` | 2022-03-01 |
| Personopplysningsloven | `regelverk/personopplysningsloven/VEIVISER.md` | 2022-01-01 |
| Samordningsloven | `regelverk/samordningsloven/VEIVISER.md` | 2026-01-01 |
| Sosialtjenesteloven | `regelverk/sosialtjenesteloven/VEIVISER.md` | 2026-01-01 |
| Språklova | `regelverk/spraklova/VEIVISER.md` | 2025-07-01 |
| Statsansatteloven | `regelverk/statsansatteloven/VEIVISER.md` | 2026-01-01 |
| Statsborgerloven | `regelverk/statsborgerloven/VEIVISER.md` | 2024-12-20 |
| Tjenestetvistloven | `regelverk/tjenestetvistloven/VEIVISER.md` | 2012-03-01 |
| Tolkeloven | `regelverk/tolkeloven/VEIVISER.md` | 2022-06-15 |
| Universitets- og høyskoleloven | `regelverk/universitets-og-hoyskoleloven/VEIVISER.md` | 2026-08-01 · **vedtatte endringer venter** |
| Utlendingsloven | `regelverk/utlendingsloven/VEIVISER.md` | 2026-10-01 · **vedtatte endringer venter** |
| Utredningsinstruksen | `regelverk/utredningsinstruksen/VEIVISER.md` | 2024-11-01 |
<!-- AUTO-SLUTT -->

## Tariffavtaler og EU-rettsakter i basen

<!-- AUTO-START andre kilder: genereres av verktoy/bygg.py, ikke rediger for hånd -->
**Tariffavtaler** (ikke lov eller forskrift)

| Avtale | Veiviser | Periode |
|---|---|---|
| Hovedtariffavtalen i staten | `regelverk/hovedtariffavtalen/VEIVISER.md` | 1. mai 2026 – 30. april 2028 |

**EU-rettsakter** (EU-tekst fra EUR-Lex, ikke norsk lov; se veiviseren om hvilken versjon som gjelder i EØS)

| Rettsakt | Nummer | Veiviser | EØS-versjon |
|---|---|---|---|
| Trygdeforordningen | (EF) nr. 883/2004 | `regelverk/eu/forordning-883-2004/VEIVISER.md` | kontrollert |
| Gjennomføringsforordningen til trygdeforordningen | (EF) nr. 987/2009 | `regelverk/eu/forordning-987-2009/VEIVISER.md` | kontrollert |
| Forordningen om fri bevegelighet for arbeidstakere | (EU) nr. 492/2011 | `regelverk/eu/forordning-492-2011/VEIVISER.md` | ikke kontrollert |
| Personvernforordningen (GDPR) | (EU) 2016/679 | `regelverk/eu/forordning-2016-679/VEIVISER.md` | kontrollert |
| Rammedirektivet for helse, miljø og sikkerhet | 89/391/EØF | `regelverk/eu/direktiv-89-391/VEIVISER.md` | ikke kontrollert |
| Utsendingsdirektivet | 96/71/EF | `regelverk/eu/direktiv-96-71/VEIVISER.md` | ikke kontrollert |
| Deltidsdirektivet | 97/81/EF | `regelverk/eu/direktiv-97-81/VEIVISER.md` | ikke kontrollert |
| Masseoppsigelsesdirektivet | 98/59/EF | `regelverk/eu/direktiv-98-59/VEIVISER.md` | ikke kontrollert |
| Direktivet om midlertidig ansettelse | 1999/70/EF | `regelverk/eu/direktiv-1999-70/VEIVISER.md` | ikke kontrollert |
| Direktivet om likebehandling uavhengig av rase eller etnisk opprinnelse | 2000/43/EF | `regelverk/eu/direktiv-2000-43/VEIVISER.md` | ikke kontrollert |
| Rammedirektivet om likebehandling i arbeidslivet | 2000/78/EF | `regelverk/eu/direktiv-2000-78/VEIVISER.md` | ikke kontrollert |
| Virksomhetsoverdragelsesdirektivet | 2001/23/EF | `regelverk/eu/direktiv-2001-23/VEIVISER.md` | ikke kontrollert |
| Direktivet om informasjon og konsultasjon | 2002/14/EF | `regelverk/eu/direktiv-2002-14/VEIVISER.md` | ikke kontrollert |
| Arbeidstidsdirektivet | 2003/88/EF | `regelverk/eu/direktiv-2003-88/VEIVISER.md` | ikke kontrollert |
| Bevegelsesdirektivet (unionsborgerdirektivet) | 2004/38/EF | `regelverk/eu/direktiv-2004-38/VEIVISER.md` | ikke kontrollert |
| Likebehandlingsdirektivet (kjønn i arbeidslivet) | 2006/54/EF | `regelverk/eu/direktiv-2006-54/VEIVISER.md` | ikke kontrollert |
| Insolvensdirektivet (lønnsgaranti) | 2008/94/EF | `regelverk/eu/direktiv-2008-94/VEIVISER.md` | ikke kontrollert |
| Vikarbyrådirektivet | 2008/104/EF | `regelverk/eu/direktiv-2008-104/VEIVISER.md` | ikke kontrollert |
| Håndhevingsdirektivet til utsendingsdirektivet | 2014/67/EU | `regelverk/eu/direktiv-2014-67/VEIVISER.md` | ikke kontrollert |
| Direktivet om tydelige og forutsigbare arbeidsvilkår | (EU) 2019/1152 | `regelverk/eu/direktiv-2019-1152/VEIVISER.md` | ikke kontrollert |
| Direktivet om balanse mellom arbeid og privatliv | (EU) 2019/1158 | `regelverk/eu/direktiv-2019-1158/VEIVISER.md` | ikke kontrollert |
<!-- AUTO-SLUTT andre kilder -->

## Temaer i hverdagsspråk

Brukere spør ofte uten fagord. Denne listen kobler vanlige formuleringer til riktig regelverk.

| Brukeren spør om | Regelverk |
|---|---|
| innsyn, få se dokumenter, offentlig journal, unnta fra offentlighet, sladde, merinnsyn, pressen ber om et dokument, organinterne dokumenter, klage på avslag om innsyn | Offentleglova |
| AFP i offentlig sektor, offentlig AFP, AFP i staten, gå av med AFP som statsansatt | AFP-loven for medlemmer av Statens pensjonskasse |
| hvor lenge man kan jobbe i staten, må slutte ved en viss alder, gå av tidlig i yrker med lavere aldersgrense, særaldersgrense | Aldersgrenseloven for statsansatte |
| minstelønn i en bransje, lovlig lønn for bygningsarbeidere eller renholdere, hva utenlandske arbeidstakere skal ha betalt, ansvar for lønn hos underleverandør, sjekke at innleide får riktig lønn, allmenngjort tariffavtale, Tariffnemnda, sosial dumping | Allmenngjøringsloven |
| hva slags tiltak NAV kan tilby, komme i arbeid med hjelp fra NAV, tilrettelagt jobb ved nedsatt arbeidsevne, melde fra om oppsigelser, utestengt fra NAV-tiltak, drive bemanningsbyrå, penger mens man er på tiltak, reiseutgifter eller barnepass under tiltak | Arbeidsmarkedsloven |
| sagt opp, oppsigelsestid, midlertidig ansatt eller vikariat, fast jobb, innleie, overtid, hvor mye man kan jobbe, nattarbeid, pauser, turnus, permisjon, sykt barn, varsling, mobbing, tilrettelegging, overvåking av ansatte, arbeidstaker eller oppdragstaker, Arbeidstilsynet | Arbeidsmiljøloven |
| når man har lov til å streike, lønnsoppgjøret, mekling mellom partene, ulovlig streik, lockout, uenighet om en tariffavtale, fredsplikt, Riksmekleren, Arbeidsretten | Arbeidstvistloven |
| hvor mange feriedager, når man kan ta ferie, sjefen bestemmer ferien, syk i ferien, overføre ferie, feriepenger, ferie når man slutter, ferie første året i ny jobb, feriepenger av sykepenger eller foreldrepenger, femte ferieuke | Ferieloven |
| er jeg medlem av folketrygden, jobbe eller bo i utlandet og beholde trygderettigheter, hva grunnbeløpet er nå, G-regulering, trygdetid, pensjonspoeng, poeng for å være hjemme med barn | Folketrygdloven |
| mistet jobben og trenger penger, dagpenger, permittert fra jobben, hvor lenge man kan få dagpenger, sagt opp selv og konsekvenser for stønad, meldekort, må søke jobber for å få støtte, arbeidsgiver gikk konkurs | Folketrygdloven |
| sykmeldt, sykepenger, egenmelding, langtidssykmeldt, mister inntekt fordi man er syk, hjemme med sykt barn, pleiepenger, alvorlig eller kronisk sykt barn, permisjon for å følge opp et sykt barn | Folketrygdloven |
| arbeidsavklaringspenger, AAP, kommer ikke tilbake i jobb pga. sykdom eller skade, blir avklart for arbeid, deltar på tiltak fra NAV, utgifter til reise, flytting eller barnetilsyn under tiltak | Folketrygdloven |
| uføretrygd, blir aldri frisk nok til å jobbe igjen, varig syk eller skadet, kan ikke jobbe lenger pga. helsen, permanent nedsatt arbeidsevne, barnetillegg til uføretrygd | Folketrygdloven |
| skadet seg på jobb, yrkesskade, blitt syk av arbeidet, ulykke i arbeidstiden, erstatning for varig men, menerstatning, sykdom av kjemikalier eller støy på arbeidsplassen | Folketrygdloven |
| foreldrepenger, permisjon med penger når man får barn, hvor lenge man kan være hjemme med baby, pappaperm, adoptere barn og få stønad, engangsstønad, gravid og kan ikke jobbe i jobben sin | Folketrygdloven |
| alene med barn og trenger støtte, aleneforsørger og økonomi, overgangsstønad, må jobbe eller studere for å få stønad, samboer og hvordan det påvirker stønaden, utgifter til barnepass | Folketrygdloven |
| ektefellen døde og økonomien, omstillingsstønad, støtte til begravelse, gravferdsstønad, barnepensjon til barn som har mistet forelder, samboer død og hvilke rettigheter man har, flytte kiste til hjemstedet | Folketrygdloven |
| når man kan ta ut pensjon, alderspensjon fra folketrygden, ta ut pensjon og jobbe samtidig, hvor mye pensjon man får, tidlig pensjon fra 62, hvilke pensjonsregler som gjelder for min årgang | Folketrygdloven |
| ekstrautgifter pga. sykdom eller funksjonsnedsettelse, grunnstønad, hjelpestønad, kronisk sykt barn som trenger mye tilsyn, diagnose (f.eks. Downs syndrom, diabetes, astma) og hva den utløser av støtte | Folketrygdloven |
| hjelpemidler, trenger utstyr hjemme eller på jobb pga. funksjonsnedsettelse, høreapparat, trenger bil pga. bevegelseshemning, trenger tolk eller ledsager, servicehund, briller til barn | Folketrygdloven |
| klage på vedtak fra NAV, anke til Trygderetten, hvor man klager videre, hvor lang tid NAV kan bruke, hva man plikter å opplyse om til NAV, NAV har fått feil opplysninger | Folketrygdloven |
| NAV krever penger tilbake, fått for mye utbetalt, tilbakekreving, hvor langt tilbake NAV kan kreve, trekk i ytelsen, når pengene fra NAV kommer, arbeidsgivers plikt til å melde til Aa-registeret | Folketrygdloven |
| introduksjonsprogram, introduksjonsstønad, nyankommet flyktning, penger mens man går i program, hva kommunen plikter å tilby flyktninger, fordrevne fra Ukraina, norskkurs, læreplan i norsk, språknivå A1–C1, norskprøve, samfunnskunnskap | Integreringsloven |
| bedriften har gått konkurs, ikke fått lønn, få dekket lønn og feriepenger etter konkurs, hvor mye staten dekker når arbeidsgiver ikke kan betale, lønnsgarantiordningen, NAV Lønnsgaranti | Lønnsgarantiloven |
| hvem bestemmer hva på NAV-kontoret, hva NAV har lov å dele av opplysninger, rett til å få vurdert behovet sitt hos NAV, uenighet mellom kommunen og staten om NAV-kontoret, plan som samordner tjenester fra flere instanser | NAV-loven |
| blir permittert, hvem betaler lønn ved permittering, hvor lenge arbeidsgiver må betale, arbeidsgiverperiode, permitteringsvarsel, permitteringslønn, delvis permittering | Permitteringslønnsloven |
| hvorfor blir tjenestepensjonen redusert, trekk i pensjonen fra staten når jeg får pensjon fra NAV, to offentlige pensjoner samtidig, pensjon fra flere offentlige arbeidsgivere, avkorting av pensjon ved uføretrygd eller etterlatteytelse | Samordningsloven |
| har ikke penger til mat eller husleie, søke sosialhjelp, få NAV til å hjelpe med regninger, krav om å jobbe for å få sosialhjelp, akutt bostedsløs, program for å komme i jobb med fast stønad | Sosialtjenesteloven |
| pensjon som statsansatt, pensjonen fra jobben i staten, pensjon fra tidligere statlig arbeidsgiver, statsansatt som blir ufør, pensjon fra staten når ektefellen dør, pensjon til barn etter statsansatt forelder, jobbe ved siden av uførepensjon fra staten | Lov om Statens pensjonskasse |
| bli norsk statsborger, hvor lenge man må ha bodd i Norge, to statsborgerskap, om barn blir norske automatisk, miste statsborgerskap ved å bo i utlandet, straff og statsborgerskap, søke statsborgerskap for barn, statsborgerprøven | Statsborgerloven |
| streik i staten, lønnsoppgjøret i staten, tariffavtaler for statsansatte, hovedsammenslutninger, Statens lønnsutvalg | Tjenestetvistloven |
| når det offentlige må skaffe tolk, bruke familie eller barn som tolk, krav for å jobbe som tolk, klage på en tolk, tolk over skjerm eller telefon, kvalifisert tolk, Nasjonalt tolkeregister, statsautorisert tolk | Tolkeloven |
| skolen, grunnskole, videregående skole, rett til videregående opplæring, lærling og lærekontrakt, fag- og svennebrev, skolemiljø og mobbing i skolen, tilpasset opplæring, spesialundervisning, skoleskyss, voksenopplæring, grunnskole eller videregående for voksne, realkompetansevurdering, privatist, godkjenning av utenlandsk fagbrev | Opplæringslova |
| universitet og høyskole, studier, opptak til høyere utdanning, Samordna opptak, generell studiekompetanse, studiekompetanse med utenlandsk utdanning, godkjenning av utenlandsk høyere utdanning eller utdanning uten dokumentasjon, eksamen og klage på karakter, fusk, studentrettigheter, skolepenger for studenter utenfor EØS, NOKUT, ansettelse som professor eller stipendiat | Universitets- og høyskoleloven |
| ansette noen fra land utenfor EU, flytte til Norge for å jobbe, arbeidstillatelse, registrere seg som EU-borger, jobbe i Norge som svenske eller danske, oppholdstillatelse, oppholdsrett, asyl, familiegjenforening, visum, utvisning | Utlendingsloven |
| ansatt i staten, statsansatt, tilsetting i staten, kvalifikasjonsprinsippet, prøvetid i staten, oppsigelse eller avskjed i staten, suspensjon, ordensstraff, midlertidig ansettelse i staten, embetsmann, innstillingsråd, tilsettingsråd, fortrinnsrett i staten, ventelønn | Statsansatteloven |
| karantene når man slutter i staten, saksforbud, gå fra staten til privat sektor, informasjonsplikt om ny jobb, Karantenenemnda | Karanteneloven |
| enkeltvedtak, forhåndsvarsel, begrunnelse for vedtak, klagefrist, klage på vedtak fra forvaltningen, partsinnsyn, inhabilitet, habilitet, taushetsplikt i forvaltningen, veiledningsplikt, forskrift og høring av forskrift, omgjøring av vedtak | Forvaltningsloven |
| ny forvaltningslov, når den nye forvaltningsloven trer i kraft, endringer i saksbehandlingsreglene | Forvaltningsloven 2025 (ny lov, ikke i kraft) |
| journalføring, arkivplikt, arkivere e-post, bevare dokumenter, kassasjon, slette arkiv, arkivdanning, Arkivverket | Arkivlova |
| utredning av tiltak, konsekvensutredning, utredningsinstruksen, seks spørsmål i utredningsinstruksen, samfunnsøkonomisk analyse, høringsfrist for statlige tiltak | Utredningsinstruksen |
| har Stortinget bedt regjeringen om noe, anmodningsvedtak, er det stilt spørsmål om et tema, spørsmål eller interpellasjon til en statsråd, representantforslag, hva skjedde med forslaget om X, har et parti foreslått noe, ble forslaget vedtatt eller nedstemt | Stortinget (`stortinget/VEIVISER.md`) |
| nynorsk og bokmål i staten, språkkrav i offentlige dokumenter, klarspråk, målbruk, 25 prosent nynorsk, språkform i svar til innbyggere | Språklova |
| diskriminering, likestilling, forskjellsbehandling på grunn av kjønn, etnisitet, religion, funksjonsnedsettelse, seksuell orientering eller alder, trakassering, seksuell trakassering, aktivitetsplikt, universell utforming, lik lønn for arbeid av lik verdi | Likestillings- og diskrimineringsloven |
| Likestillings- og diskrimineringsombudet, Diskrimineringsnemnda, klage på diskriminering, oppreisning fra nemnda | Diskrimineringsombudsloven |
| personvern, personopplysninger, GDPR, behandlingsgrunnlag, innsyn i egne opplysninger, sletting, personvernombud, avvik og brudd på personopplysningssikkerheten, Datatilsynet, kameraovervåking | Personopplysningsloven og personvernforordningen (EU) |
| hovedtariffavtalen, HTA, lønn i staten, lønnstrinn, lokale forhandlinger, overtid i staten, ubekvem arbeidstid, beredskapsvakt, reisetid, velferdspermisjon, permisjon med lønn, ferie i staten, femte ferieuke, fellesbestemmelsene, særavtaler | Hovedtariffavtalen i staten |
| EU-direktiv, EU-forordning, EØS-regler, hva sier direktivet, arbeidstidsdirektivet, vikarbyrådirektivet, utsendingsdirektivet, trygdeforordningen, fri bevegelighet for arbeidstakere | EU-rettsakter (`regelverk/eu/`) |
| bor eller jobber i et annet EØS-land og trygd, EØS-rundskrivet, R45, lovvalg i EØS, eksport av ytelser, sammenlegging av trygdetid, attest A1, EØS-pensjon, Navs EØS-rundskriv | Trygdeforordningen med Navs rundskriv R45-00 (`regelverk/eu/forordning-883-2004/VEIVISER.md`) |

## Kjente regelverk som ikke er i basen

Følgende er ikke dekket. Spørsmål om dem skal ikke besvares fra hukommelsen, se regel 4 under: barnetrygdloven, kontantstøtteloven, trygderettsloven, yrkesskadeforsikringsloven, straffeloven, domstolloven og skatteloven. Listen er ikke uttømmende. Er regelverket ikke i tabellen over, er det ikke i basen.

## Regler for svar

1. **Åpne alltid kildefilene før du svarer.** Svar ikke på regelverksspørsmål fra generell kunnskap. Les veiviseren og de paragrafene som er relevante, også unntak og henvisninger til andre paragrafer.
2. **Oppgi kilde i svaret:** regelverk, paragraf og ledd, f.eks. «offentleglova § 14 første ledd». Brukeren skal kunne kontrollere svaret selv.
3. **Skill mellom kildetypene.** Si om en regel står i lov, forskrift, instruks, tariffavtale eller EU-rettsakt.
4. **Når regelverket ikke er i basen.** Basen bygges ut gradvis.
   - Finnes det en egen skill for regelverket, bruk den.
   - Finnes det ingen, si tydelig at regelverket ikke er dekket. Nevn hvilket regelverk som trolig gjelder, og vis til Lovdata (lovdata.no). Ikke konkluder på spørsmålet.
   - Er regelverket i basen, men paragrafene svarer ikke på spørsmålet, si det. Skriv «ingen bestemmelse funnet i det jeg har gått gjennom», ikke «finnes ikke». Gi aldri et selvsikkert svar uten kilde.
5. **Ordrett gjengivelse når brukeren ber om lovteksten.** Gjengi filen i sin helhet, med ledd, bokstavpunkter og overskrifter slik de står. Lovtekst på nynorsk siteres på nynorsk. Ellers svarer du på brukerens språk.
6. **Oppgi hvor oppdatert teksten er** når det kan ha betydning, med datoen for «sist endret i kraft» fra veiviseren.
7. **Si fra om vedtatte endringer.** Har en paragraf du bygger på et varsel om vedtatt endring, eller viser veiviseren en vedtatt endring som berører spørsmålet, skal svaret si det: hva som endres, når endringen trer i kraft (eller at Kongen ikke har bestemt tidspunktet ennå), og at svaret bygger på teksten som gjelder i dag. Les den nye ordlyden i `vedtatte-endringer/` før du beskriver endringen.
8. **Basen er ikke en offisiell tolkning.** Veiviserne og merknadene er hjelp til deg for å finne fram og unngå vanlige feil. Ved tvil om tolkning skal brukeren vises til forarbeider, veiledere og fagmiljøet som forvalter regelverket.
9. **Snakk om kildene, ikke om basen.** Brukeren kjenner ikke oppbygningen av basen.
   - Oppgi kilder med sitt eget navn: lov, forskrift og paragraf, «NAVs rundskriv til § 4-4 (R04-00)», «departementets kommentar til fellesbestemmelsene § 22 i Hovedtariffavtalen i staten». Rundskriv og departementets kommentarer er offisielle kilder og skal oppgis eksplisitt.
   - Ordene veiviser, merknad, indeks, AUTO-blokk og filstier skal ikke stå i svaret.
   - Merknadene er skrevet som hjelpetekst og er ikke godkjent av noe fagmiljø. De oppgis ikke som kilde. Står et poeng bare i en merknad, finn det i lov-, forskrifts- eller rundskrivteksten før du bruker det, eller si at det er din vurdering. En merknad som har eier og dato i toppen (`eier:`), er skrevet av et fagmiljø og kan oppgis med eier og dato.
   - Kall basen «regelverksbasen» når dekningen betyr noe for svaret, for eksempel «Barnetrygdloven er ikke med i regelverksbasen jeg har tilgang til. Se lovdata.no.» eller «Veiledere og rettspraksis er ikke med i regelverksbasen.» Ikke nevn regelverksbasen ellers.

## For redaktører

- Rundskriv legges i `innboks/`, så legges de inn automatisk under riktig lov. Se `innboks/README.md`.
- Merknader, EØS-tekster og rundskriv som ble flyttet fra de gamle skillene, redigeres for hånd. De oppdateres ikke automatisk, så oppgi dato når de hentes på nytt.
- `verktoy/sjekk_tekst.py` kontrollerer merknader og den håndskrevne delen av veiviserne ved hver pull request: at stiene finnes, og at ingen tekst sier at et regelverk i basen «ikke er i basen». Hva som er i basen, står bare i tabellene over. Skriv det ikke i merknadene.
- Budsjettdokumenter (Prop. 1 S, Gul bok, Nasjonalbudsjettet og datagrunnlaget) legges i `innboks-budsjett/` med filnavn etter mønsteret i `innboks-budsjett/README.md`, og legges da inn under `budsjett/<år>/`.
- Hovedtariffavtalen legges inn ved å laste opp Word-filen fra regjeringen.no i `innboks/` med filnavn som begynner på `hovedtariffavtale`. Gjør det ved hvert hovedoppgjør og mellomoppgjør. Word-filen slettes etter oppdelingen, og bygget åpner en sak i GitHub når det er tid for ny utgave.
- EU-rettsakter legges til under `eu` i `regelverk.json` med en låst versjon. Feltet `eos` fylles bare ut når versjonen er kontrollert mot EØS-avtalen. `regelverk/eu/nevnte-rettsakter.md` viser hvilke rettsakter norsk tekst i basen viser til, men som ikke er lagt inn.
- Lov- og forskriftstekst bygges fra Lovdata med `verktoy/bygg.py` og skal aldri redigeres for hånd. Blokker mellom `AUTO-START` og `AUTO-SLUTT` overskrives ved hvert bygg.
- Nytt regelverk legges til i `regelverk.json`. Skriv deretter den håndskrevne delen av `VEIVISER.md`, og legg til en linje i temalisten over.
- Endringer gjøres som pull request og godkjennes av eieren av mappen, se `.github/CODEOWNERS`.
