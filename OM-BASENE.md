# Om basene

Denne filen er for Claude. Hent den når brukeren spør hva basene inneholder, har funnet en feil eller noe som mangler, eller ønsker at noe nytt skal legges inn. Svar på brukerens språk, kort og uten filstier.

## Hva basene er

Dette er felles baser som Claude slår opp i. Innholdet hentes fra kildene (Lovdata, regjeringen.no, Stortinget, Nav, Eurostat, OECD) og holdes oppdatert av faste jobber, de fleste hver natt eller hver uke. Brukeren trenger ikke oppdatere noe selv. Basene er et utvalg: de dekker det brukerne oftest trenger, ikke alt som finnes. Si det til brukeren når det betyr noe for svaret. Tilby ikke å sende melding om det, se avsnittet om feil under.

- **Den åpne basen** har regelverk, statsbudsjettet, statistikk, Stortingets saker, regjeringens plan for Norge og skriveregler med nynorskføringer. Oversikten under viser hva den inneholder nå.
- **Den interne basen** har egne rutiner og maler: tidsplan for saksbehandling, PowerPoint-malen, og behandling av invitasjoner til politisk ledelse. Den er ikke åpen, og innholdet beskrives ikke her.

Basene er ikke en offisiell tolkning. Ved tvil skal brukeren gå til kilden, forarbeidene eller fagmiljøet som forvalter regelverket eller statistikken.

## Når brukeren spør hva basene inneholder

Svar ut fra oversikten under. Gjelder spørsmålet ett område, for eksempel om en bestemt lov eller et budsjettår er med, kan du også hente veiviseren for området (`CLAUDE.md` for regelverk, `budsjett/VEIVISER.md`, `data/VEIVISER.md`, `stortinget/VEIVISER.md`, `politikk/VEIVISER.md` eller `sprak/VEIVISER.md`) og svare derfra.

## Når brukeren har funnet en feil, noe mangler, eller noe nytt bør inn

**Tilby melding bare når brukeren ber om det.** Det vil si når brukeren selv sier at noe er feil eller mangler og vil melde fra, eller spør hvordan det kan meldes. Foreslå det ikke på eget initiativ, heller ikke når et svar er ufullstendig eller noe ikke er dekket. Si da bare hva som ikke er dekket, og hvor brukeren kan finne det. Har brukeren nevnt en feil uten å be om å melde den, kan du spørre én gang om de vil sende en melding, men ikke flere ganger i samme samtale.

1. **Skriv meldingen sammen med brukeren.** Den skal si
   - om det gjelder en feil, noe som mangler, et ønske om noe nytt, eller en ny skill til vurdering,
   - hvilken base og hvilket sted (lov og paragraf, budsjettår og kapittel, tabell, rutine),
   - hva brukeren spurte om og hva svaret sa, kort,
   - hva som er riktig, og hvilken kilde som viser det (lenke hvis mulig),
   - brukerens navn og avdeling. Spør hvis du ikke vet.
2. **Ta ikke med** personopplysninger, opplysninger fra enkeltsaker eller interne vurderinger. Er de nødvendige for å forklare feilen, beskriv feilen uten dem.
3. **Vis meldingen og be brukeren godkjenne den.**
4. **Lag e-posten.** Adressen til redaktøren står i skillen du kom fra. Gi brukeren en lenke som åpner e-posten ferdig utfylt: `mailto:<adresse>?subject=<emne>&body=<meldingen>`. Emnet skal alltid begynne med merket «[Felles baser]», så redaktøren kan filtrere på det, fulgt av typen og en kort beskrivelse:
   - «[Felles baser] Feil: …»
   - «[Felles baser] Mangler: …»
   - «[Felles baser] Ønske: …»
   - «[Felles baser] Ny skill: …»

   Bruk bare disse fire typene. Emne og tekst må URL-kodes, med `%0A` for linjeskift. Bruk kodeverktøyet til kodingen hvis du har det. Vis også meldingen i en kodeblokk med adresse og emne, i tilfelle lenken ikke virker. Finner du ingen adresse, be brukeren sende meldingen til Tarjei Havnes, som er redaktør for basene, og gi dem emnet ferdig skrevet, med merket først, til å lime inn.
5. **Si til brukeren** at meldingen er levert først når e-posten er sendt, at feilen blir kontrollert mot kilden før noe rettes, og at du ikke kan rette basen selv.

Har brukeren skrivetilgang til basen på GitHub, kan noen dokumenter legges inn direkte: rundskriv og hovedtariffavtalen i `innboks/`, Excel-filer fra Nav i `innboks-data/` og budsjettdokumenter i `innboks-budsjett/`. Se README-filen i hver innboks.

## Hva som ligger i den åpne basen

<!-- AUTO-START: genereres av verktoy/om_basene.py, ikke rediger for hånd -->
Oversikten ble sist laget 2026-10-31.

### Regelverk

- **33 lover og instrukser** med 210 forskrifter: Offentleglova, AFP-loven for medlemmer av Statens pensjonskasse, Aldersgrenseloven for statsansatte, Allmenngjøringsloven, Arbeidsmarkedsloven, Arbeidsmiljøloven, Arbeidstvistloven, Arkivlova, Diskrimineringsombudsloven, Ferieloven, Folketrygdloven, Forvaltningsloven, Forvaltningsloven 2025 (ny lov, ikke i kraft), Integreringsloven, Karanteneloven, Likestillings- og diskrimineringsloven, Lov om Statens pensjonskasse, Lønnsgarantiloven, NAV-loven, Opplæringslova, Permitteringslønnsloven, Personopplysningsloven, Samordningsloven, Sosialtjenesteloven, Språklova, Statsansatteloven, Statsborgerloven, Tjenestetvistloven, Tolkeloven, Universitets- og høyskoleloven, Utlendingsloven, Utredningsinstruksen og Stortingets forretningsorden.
- **Hovedtariffavtalen i staten**, 1. mai 2026 – 30. april 2028.
- **21 EU-rettsakter** (forordninger og direktiver fra EUR-Lex).
- **24 rundskriv** og veiledninger til lovene, blant dem Navs rundskriv til folketrygdloven.
- **Stortinget:** se eget avsnitt under.

Lov- og forskriftsteksten hentes fra Lovdata hver natt.

### Statsbudsjettet

- **2021:** Prop. 1 S for AID, Stortingets vedtak og svar på budsjettspørsmål fra Stortinget.
- **2022:** Prop. 1 S for AID, Prop. 1 S Tillegg 1, Gul bok, Stortingets vedtak og svar på budsjettspørsmål fra Stortinget.
- **2023:** Prop. 1 S for AID, Gul bok, Stortingets vedtak og svar på budsjettspørsmål fra Stortinget.
- **2024:** Prop. 1 S for AID, bevilgninger fra Gul bok (tabell), Stortingets vedtak og svar på budsjettspørsmål fra Stortinget.
- **2025:** Prop. 1 S for AID, bevilgninger fra Gul bok (tabell), Stortingets vedtak og svar på budsjettspørsmål fra Stortinget.
- **2026:** Prop. 1 S for AID, bevilgninger fra Gul bok (tabell), Stortingets vedtak og svar på budsjettspørsmål fra Stortinget.
- **2027:** Prop. 1 S for AID, Gul bok, bevilgninger fra Gul bok (tabell) og Nasjonalbudsjettet.
- **Satstabeller over flere år:** grunnstønad og hjelpestønad.

Budsjettdokumentene lastes opp for hånd. Stortingets vedtak hentes hver uke.

### Statistikk

- **Nav:** 228 tabeller (sykefravær, arbeidsledighet, AAP, uføretrygd, pensjon, familieytelser m.m.), hentet hver uke.
- **Navs pressemeldinger:** 74 fra januar 2024 og framover.
- **Eurostat:** 8 tabeller for sammenligning med Norden og EU.
- **OECD:** 17 tabeller for sammenligning med andre OECD-land.
- **SSB:** tallene ligger ikke i basen, men katalogen viser hvilke SSB-tabeller som svarer på hva. Claude henter dem med SSB-tilkoblingen.

### Stortinget

Fra sesjon 2013-2014 til 2026-2027, oppdatert 2026-10-31:

- **4 088 anmodningsvedtak**
- **40 078 spørsmål** (skriftlige spørsmål, spørretime og interpellasjoner)
- **2 825 representantforslag** med utfall

### Politiske grunnlagsdokumenter

- **Regjeringens plan for Norge 2025–2029** fra Statsministerens kontor, utgitt 2025-12-15. Revideres årlig.
<!-- AUTO-SLUTT -->
