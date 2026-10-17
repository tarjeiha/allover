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
- **Lang serie:** `aap-alder-kjonn-kvartal/1a-alder-i-alt-antall.tsv` (juni hvert år, 2010–2026). Raden `I alt` er landet.
- **Siste måneder:** `aap-alder-kjonn-maaned/` (inneværende år), `aap-fylke-alder-maaned/`, `aap-kommune-maaned/`, `aap-diagnose-*`.
- **Måler:** mottakere av AAP. Tellebegrepet står i `om.md` og i Navs «Om statistikken»; les det før du kaller tallet «ved årets slutt» eller «i løpet av året».
- **Små tall:** celler under 4 er erstattet med `*`.
- **Annen kilde:** SSB og Nav har ulike tall for AAP-mottakere av ulike grunner. Navs side «Hvorfor har Nav og SSB ulike tall for mottakere av AAP og uføretrygd?» forklarer dette. Bruk Navs tall som standard og si fra om kilden.

## Uføretrygd

- **Kilde:** Nav, uføretrygd. `https://www.nav.no/no/nav-og-samfunn/statistikk/aap-nedsatt-arbeidsevne-og-uforetrygd-statistikk/uforetrygd/`.
- **Antall mottakere:** `uforetrygd-uforegrad-kjonn-maaned/antall.tsv` (landet, per uføregrad og kjønn), `uforetrygd-fylke-alder-maaned/antall.tsv` (fylke og alder), inneværende år per måned.
- **Andel av befolkningen:** `uforetrygd-fylke-alder-maaned/andel-av-befolkningen.tsv`; kvartalsvis `uforetrygd-andel-fylke-alder-kvartal/`. Andelen gjelder befolkningen 18–67 år.
- **Nye mottakere og avgang:** `uforetrygd-nye-*-maaned/`, `uforetrygd-avgang-kjonn-alder-maaned/`. Diagnoser per år: `uforetrygd-diagnose-*-aar/`.
- **Måler:** personer som har fått utbetalt uføretrygd i måneden. Uføregrad og barnetillegg ligger i egne tabeller.
- **Små tall:** celler under 4 er erstattet med `*`.
- **Annen kilde:** som for AAP har SSB andre tall; se Navs forklaringsside.

## Utvidelse

Legg til en profil her når et område tas i bruk i svar. En profil skal være kortere enn én skjermside, og skal bare ha det som er nødvendig for å velge tabell og unngå feil.
