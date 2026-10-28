# Kildeprofiler for Nav-statistikk

Én profil per statistikkområde: hvilken tabell som svarer på vanlige spørsmål, hva tallet måler, og forbehold som er relevante for slike svar. Profilene hjelper deg å finne riktig tabell. De erstatter ikke `om.md` i tabellmappen, som er Navs egen beskrivelse. Legg ikke forbehold i svaret med mindre de berører perioden eller tallene svaret viser (se «Slik svarer du» i `data/VEIVISER.md`).

Stier er relative til `data/nav/`. «Kilde» er Navs side; når siden sist ble oppdatert står i `data/nav/sider.json`.

## Sykefravær

- **Kilde:** Nav, sykefraværsstatistikk (legemeldt fravær). `https://www.nav.no/no/nav-og-samfunn/statistikk/sykefravar-statistikk/sykefravar`. Publiseres kvartalsvis.
- **Hovedtall:** `sykefravar-tidsserie-kvartal/sykefravaersprosent.tsv` (prosent), `antall-sykmeldte.tsv`, `antall-tilfeller.tsv`, `tapte-dagsverk.tsv`. Kolonner: `gruppe`, `år`, `1.–4. kvartal`. Ikke publiserte kvartal står som `****`.
- **Nedbrytning:** `sykefravar-alder/`, `-naering/`, `-sektor/`, `-yrke/`, `-bosted/`, `-diagnose-*/`, `-varighetsgrupper/` m.fl. Alle kvartaler ligger i samme fil, med kolonnen `kvartal`.
- **Måler:** legemeldt sykefravær, tapte dagsverk i prosent av avtalte dagsverk. Egenmeldt fravær er ikke med.
- **Sammenlign** samme kvartal på tvers av år, fordi tallene ikke er sesongjustert.
- **Brudd:** nytt mottak for sykmeldinger fra 1. kvartal 2022, ny diagnoseinndeling fra 1. kvartal 2026 (gjelder diagnosetabellene). Bruddene tas bare med når svaret berører de periodene eller diagnosene.
- **Annen kilde:** SSB har egen sykefraværsstatistikk som inkluderer egenmeldt fravær (`data/ssb.md`). Tallene avviker, så vis begge eller tilby SSB-tallet når kilden nevnes.

## Dagpenger og helt ledige

- **Kilde:** Nav, «Stønader til arbeidssøkere» (dagpenger) og «Hovedtall om arbeidsmarkedet» / «Helt ledige». `https://www.nav.no/no/nav-og-samfunn/statistikk/arbeidssokere-og-stillinger-statistikk/`. Månedlig.
- **Dagpengemottakere:** `dagpenger-kjonn-alder-maaned/` (ark `Alder`, `Kjønn og arbeidsmarkedsstatus`, `Andel helt ledige med dagpenger`), `dagpenger-fylke-kommune-maaned/`, `-varighet-`, `-yrke-`, `-soknader-`.  Tabellene har månedene i inneværende år; sjekk perioden øverst i filen og `indeks.tsv`.
- **Helt ledige:** `hovedtall-arbeidsmarkedet/` (landet), `helt-ledige-kjonn-alder-maaned/`, `-fylke-kommune-maaned/`, `-historisk/`, `helt-ledige-fylke-mnd-*` (tilbake til 1951). Sesongjusterte tall: `hovedtall-arbeidsmarkedet-sesongjustert/`.
- **Måler:** registrerte hos Nav, ikke arbeidsledighet etter internasjonal definisjon. Dagpengemottakere er en del av gruppen helt ledige, ikke det samme.
- **Brudd:** ny registreringsmetode fra november 2018, og endret publisering fra april 2025 (se «Om statistikken – arbeidssøkere»). Nevn bare ved sammenligning på tvers av bruddet.
- **Annen kilde:** SSBs arbeidskraftsundersøkelse (AKU) gir arbeidsledighet etter ILO-definisjon, og tallet er et annet. Vis begge eller tilby AKU-tallet når forskjellen nevnes.

## Arbeidsavklaringspenger (AAP)

- **Kilde:** Nav, «Mottakere av arbeidsavklaringspenger (AAP)». `https://www.nav.no/no/nav-og-samfunn/statistikk/aap-nedsatt-arbeidsevne-og-uforetrygd-statistikk/arbeidsavklaringspenger`.
- **Lang serie:** `aap-alder-kjonn-desember/1a-alder-i-alt-antall.tsv` (desember hvert år, 2010–2025) og `aap-alder-kjonn-kvartal/` (siste kvartal Nav har publisert, i dag juni 2010–2026). Raden `I alt` er landet. Bruk desemberserien når AAP skal ses sammen med uføretrygd per 31. desember.
- **Siste måneder:** `aap-alder-kjonn-maaned/` (inneværende år), `aap-fylke-alder-maaned/`, `aap-kommune-maaned/`, `aap-diagnose-*`.
- **Tilgang og avgang:** `aap-tilgang-*-kvartal/` (nye mottakere, AAP380–382) og `aap-avgang-*-kvartal/` (avsluttede, AAP390–392), etter alder og kjønn, fylke og alder, og fylke og kjønn. Hver fil har samme kvartal hvert år fra 2010. Avgangstallene kommer ett kvartal senere enn tilgangen, så sjekk perioden øverst i filen.
- **Unge mottakere:** `aap-unge-alder-fylke-kvartal/` (AAP310), antall og andel av befolkningen etter alder og fylke.
- **Måler:** personer som har fått utbetalt AAP i løpet av måneden. Personer som bare får etterbetaling eller G-justering er tatt ut fra august 2020, og historikken er justert. Uteblir utbetalingen i to måneder på rad, telles personen som avgang selv om retten til AAP kan løpe videre.
- **Andel av befolkningen:** befolkningen 18–66 år, med alder ved utgangen av måneden (Navs «Om statistikken – Mottakere av arbeidsavklaringspenger», kapittel 4). Aldersgrensen står ikke i tabellfilene, så oppgi den fra denne profilen.
- **Små tall:** celler under 4 er erstattet med `*`.
- **Annen kilde:** SSB og Nav har ulike tall for AAP-mottakere av ulike grunner. Navs side «Hvorfor har Nav og SSB ulike tall for mottakere av AAP og uføretrygd?» forklarer dette. Bruk Navs tall som standard og si fra om kilden.

## Uføretrygd

- **Kilde:** Nav, uføretrygd. `https://www.nav.no/no/nav-og-samfunn/statistikk/aap-nedsatt-arbeidsevne-og-uforetrygd-statistikk/uforetrygd/`.
- **Lang serie:** `uforetrygd-desember-kjonn-alder-antall/` (antall per 31. desember 2016–2025, i alt, kvinner og menn etter alder) og `uforetrygd-desember-andel-kjonn-alder-prosent/` (andel av befolkningen). Nye mottakere og avgang per år: `uforetrygd-desember-nye-kjonn-alder-antall/` og `uforetrygd-desember-avgang-kjonn-alder-antall/` (hele året, 1.–4. kvartal). Mappene `uforetrygd-desember-*` har alle webtabellene på Navs arkivside for 31. desember; `uforetrygd-kvartal-*` har de samme tabellene for siste kvartal (i dag 30. juni 2017–2026, nye og avgang i 1. halvår).
- **Før 2016:** `stonadsmottakere-2007-2016/tabell.tsv`, raden `Uføretrygd 4)`. Tallet for 2016 (318 244) er det samme som i desemberserien. Uføretrygd erstattet uførepensjon i 2015.
- **Siste måneder:** `uforetrygd-uforegrad-kjonn-maaned/antall.tsv` (landet, per uføregrad og kjønn), `uforetrygd-fylke-alder-maaned/antall.tsv` (fylke og alder), inneværende år per måned.
- **Andel av befolkningen:** `uforetrygd-fylke-alder-maaned/andel-av-befolkningen.tsv`; kvartalsvis `uforetrygd-andel-fylke-alder-kvartal/`. Andelen gjelder befolkningen 18–67 år.
- **Nye mottakere og avgang:** `uforetrygd-nye-*-maaned/`, `uforetrygd-avgang-kjonn-alder-maaned/`. Diagnoser per år: `uforetrygd-diagnose-*-aar/`, **bare 18–29 år**. Nav koder ikke diagnose for uføretrygdede over 30 år, så det finnes ingen diagnosetabell for alle aldre.
- **Måler:** personer som har fått utbetalt uføretrygd i måneden. Uføregrad og barnetillegg ligger i egne tabeller.
- **Små tall:** celler under 4 er erstattet med `*`.
- **Annen kilde:** som for AAP har SSB andre tall; se Navs forklaringsside.

## Utvidelse

Legg til en profil her når et område tas i bruk i svar. En profil skal være kortere enn én skjermside, og skal bare ha det som er nødvendig for å velge tabell og unngå feil.
