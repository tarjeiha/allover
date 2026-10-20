# Om basene

Denne filen er for Claude. Hent den når brukeren spør hva basene inneholder, har funnet en feil eller noe som mangler, eller ønsker at noe nytt skal legges inn. Svar på brukerens språk, kort og uten filstier.

## Hva basene er

AID har felles baser som Claude slår opp i. Innholdet hentes fra kildene (Lovdata, regjeringen.no, Stortinget, Nav, Eurostat, OECD) og holdes oppdatert av faste jobber, de fleste hver natt eller hver uke. Brukeren trenger ikke oppdatere noe selv.

- **Den åpne basen** har regelverk, statsbudsjettet, statistikk og Stortingets saker. Oversikten under viser hva den inneholder nå.
- **Den interne basen** har AIDs egne rutiner og maler: tidsplan for saksbehandling, PowerPoint-malen, behandling av invitasjoner til politisk ledelse og skriveregler og nynorsk. Den er ikke åpen, og innholdet beskrives ikke her.

Basene er ikke en offisiell tolkning. Ved tvil skal brukeren gå til kilden, forarbeidene eller fagmiljøet som forvalter regelverket eller statistikken.

## Når brukeren spør hva basene inneholder

Svar ut fra oversikten under. Gjelder spørsmålet ett område, for eksempel om en bestemt lov eller et budsjettår er med, kan du også hente veiviseren for området (`CLAUDE.md` for regelverk, `budsjett/VEIVISER.md`, `data/VEIVISER.md` eller `stortinget/VEIVISER.md`) og svare derfra.

## Når brukeren har funnet en feil, noe mangler, eller noe nytt bør inn

1. **Er skillen `aid-meldinger` installert, bruk den.** Den sender meldingen til basens redaktør.
2. **Ellers:** skriv en ferdig melding som brukeren kan sende til Tarjei Havnes, som er redaktør for basene. Meldingen skal si
   - om det gjelder en feil, noe som mangler, eller et ønske om noe nytt,
   - hvilken base og hvilket sted (lov og paragraf, budsjettår og kapittel, tabell),
   - hva brukeren spurte om og hva svaret sa, kort,
   - hva som er riktig, og hvilken kilde som viser det,
   - brukerens navn og avdeling.
3. **Ta ikke med** personopplysninger, opplysninger fra enkeltsaker eller interne vurderinger i meldingen.
4. Si til brukeren at feilen blir kontrollert mot kilden før noe rettes, og at du ikke kan rette basen selv.

Har brukeren skrivetilgang til basen på GitHub, kan noen dokumenter legges inn direkte: rundskriv og hovedtariffavtalen i `innboks/`, Excel-filer fra Nav i `innboks-data/` og budsjettdokumenter i `innboks-budsjett/`. Se README-filen i hver innboks.

## Hva som ligger i den åpne basen

<!-- AUTO-START: genereres av verktoy/om_basene.py, ikke rediger for hånd -->
Oversikten ble sist laget 2026-10-20.

### Regelverk

- **30 lover og instrukser** med 202 forskrifter: Offentleglova, AFP-loven for medlemmer av Statens pensjonskasse, Aldersgrenseloven for statsansatte, Allmenngjøringsloven, Arbeidsmarkedsloven, Arbeidsmiljøloven, Arbeidstvistloven, Arkivlova, Diskrimineringsombudsloven, Ferieloven, Folketrygdloven, Forvaltningsloven, Forvaltningsloven 2025 (ny lov, ikke i kraft), Integreringsloven, Karanteneloven, Likestillings- og diskrimineringsloven, Lov om Statens pensjonskasse, Lønnsgarantiloven, NAV-loven, Permitteringslønnsloven, Personopplysningsloven, Samordningsloven, Sosialtjenesteloven, Språklova, Statsansatteloven, Statsborgerloven, Tjenestetvistloven, Tolkeloven, Utlendingsloven og Utredningsinstruksen.
- **Hovedtariffavtalen i staten**, 1. mai 2026 – 30. april 2028.
- **21 EU-rettsakter** (forordninger og direktiver fra EUR-Lex).
- **24 rundskriv** og veiledninger til lovene, blant dem Navs rundskriv til folketrygdloven.
- **Stortinget:** se eget avsnitt under.

Lov- og forskriftsteksten hentes fra Lovdata hver natt.

### Statsbudsjettet

- **2021:** Prop. 1 S for AID og Stortingets vedtak.
- **2022:** Prop. 1 S for AID, Prop. 1 S Tillegg 1, Gul bok og Stortingets vedtak.
- **2023:** Prop. 1 S for AID, Gul bok og Stortingets vedtak.
- **2024:** Prop. 1 S for AID, bevilgninger fra Gul bok (tabell) og Stortingets vedtak.
- **2025:** Prop. 1 S for AID, bevilgninger fra Gul bok (tabell) og Stortingets vedtak.
- **2026:** Prop. 1 S for AID, bevilgninger fra Gul bok (tabell), Stortingets vedtak og svar på budsjettspørsmål fra Stortinget.
- **2027:** Prop. 1 S for AID, Gul bok, bevilgninger fra Gul bok (tabell) og Nasjonalbudsjettet.
- **Satstabeller over flere år:** grunnstønad og hjelpestønad.

Budsjettdokumentene lastes opp for hånd. Stortingets vedtak hentes hver uke.

### Statistikk

- **Nav:** 221 tabeller (sykefravær, arbeidsledighet, AAP, uføretrygd, pensjon, familieytelser m.m.), hentet hver uke.
- **Navs pressemeldinger:** 71 fra januar 2024 og framover.
- **Eurostat:** 8 tabeller for sammenligning med Norden og EU.
- **OECD:** 17 tabeller for sammenligning med andre OECD-land.
- **SSB:** tallene ligger ikke i basen, men katalogen viser hvilke SSB-tabeller som svarer på hva. Claude henter dem med SSB-tilkoblingen.

### Stortinget

Fra sesjon 2013-2014 til 2026-2027, oppdatert 2026-10-20:

- **4 088 anmodningsvedtak**
- **39 901 spørsmål** (skriftlige spørsmål, spørretime og interpellasjoner)
- **2 813 representantforslag** med utfall
<!-- AUTO-SLUTT -->
