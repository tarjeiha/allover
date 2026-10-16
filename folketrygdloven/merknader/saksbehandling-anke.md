> **Flyttet fra skillen `aid-ftrl-saksbehandling-anke`** 16.10.2026. Teksten er ellers uendret, bortsett fra stiene.
> Alle stier er relative til basens rot. Hele loven ligger nå i basen, så der teksten sier at
> «denne skillen» bare dekker enkelte kapitler eller viser til andre skills, gjelder det ikke lenger:
> se veiviseren til loven. Kildereglene i CLAUDE.md gjelder foran det som står her.

# Folketrygdloven – saksbehandling og anke

Oppslag i lov 28. februar 1997 nr. 19 om folketrygd, kapittel 21.

## Kritisk

**Åpne alltid de faktiske kildefilene i denne skillen før du svarer.** Ikke svar fra generell kunnskap om folketrygden. Loven er endret svært hyppig, og eldre fremstillinger av sentrale bestemmelser er ofte utdaterte.

Konkret fremgangsmåte:

1. Slå opp i `folketrygdloven/VEIVISER.md` for å finne riktig paragraf
2. Åpne selve paragraffilen (`folketrygdloven/lov/par-<nr>.md`)
3. Sjekk om en forskrift regulerer samme spørsmål – se `folketrygdloven/VEIVISER.md`
4. Gjengi leddnummer når du siterer, og oppgi paragraf i svaret

Dette er en tverrgående skill. Klage- og ankereglene gjelder alle ytelser, så spørsmål havner her uten at brukeren nevner kapittel 21.

Skill mellom klage til NAV Klageinstans og anke til Trygderetten – det er to ulike trinn med ulike frister. Forvaltningsloven gjelder i tillegg og er **ikke** dekket i noen AID-skill.

**Når brukeren ber om å se/vise lovteksten eller forskriftsteksten:** gjengi kildefilen ordrett og i sin helhet – inkludert bokstavpunkter, underoverskrifter og leddnummerering slik de står i kildefilen. Ikke sammenfatt, omformuler eller utelat strukturelementer med mindre brukeren eksplisitt ber om et sammendrag.

## Folketrygdloven er delt på mange skills

Loven har 26 kapitler og er for stor for én skill. Den er delt etter ytelse, med to tverrgående skills i tillegg. Kartet:

| Skill | Kapitler |
|---|---|
| `folketrygdloven/merknader/medlemskap-beregning.md` | 1, 2, 3 – medlemskap, trygdetid, pensjonsgivende inntekt, grunnbeløp |
| `folketrygdloven/merknader/dagpenger.md` | 4 |
| `folketrygdloven/merknader/grunnstonad.md` | 6 |
| `folketrygdloven/merknader/sykepenger.md` | 8, 9 |
| `folketrygdloven/merknader/hjelpemidler.md` | 10 |
| `folketrygdloven/merknader/aap.md` | 11, 11 A |
| `folketrygdloven/merknader/uforetrygd.md` | 12 |
| `folketrygdloven/merknader/yrkesskade.md` | 13 |
| `folketrygdloven/merknader/foreldrepenger.md` | 14 |
| `folketrygdloven/merknader/enslig-forsorger.md` | 15 |
| `folketrygdloven/merknader/etterlatte-gravferd.md` | 7, 16, 17, 17 A, 18 |
| `folketrygdloven/merknader/alderspensjon.md` | 19, 20 |
| `folketrygdloven/merknader/saksbehandling-anke.md` | 21 |
| `folketrygdloven/merknader/utbetaling-tilbakekreving.md` | 22, 25, 26 |

**Ikke dekket i noen skill:** kapittel 5 (stønad ved helsetjenester), 23 og 24 (finansiering og avgifter). Disse hører til Helse- og omsorgsdepartementet og Finansdepartementet. Ved spørsmål om egenandeler, legemidler, behandlingsrefusjon eller trygdeavgift: **si eksplisitt at kapittelet ikke er dekket**.

**Når spørsmålet ligger utenfor dine kapitler:** si hvilken skill som dekker det. Ikke svar fra hukommelsen om paragrafer du ikke har filene til.

## Tverrgående kapitler gjelder også her

Kapittel 1–3 og 21–22 gjelder alle ytelser i folketrygden. Et fullstendig svar krever ofte:

- **Medlemskap og trygdetid** (kap. 2) – ingen ytelse uten medlemskap. `folketrygdloven/merknader/medlemskap-beregning.md`
- **Grunnbeløpet** (kap. 1 § 1-4) – satsene fastsettes årlig i egen forskrift. `folketrygdloven/merknader/medlemskap-beregning.md`
- **Saksbehandling og anke** (kap. 21) – `folketrygdloven/merknader/saksbehandling-anke.md`
- **Utbetaling, tilbakekreving og foreldelse** (kap. 22, 25) – `folketrygdloven/merknader/utbetaling-tilbakekreving.md`

Si fra når svaret krever en av disse, i stedet for å svare ut fra ytelseskapittelet alene.

## Kryssreferanser utenfor folketrygdloven

- **Arbeidsmiljøloven** – permisjonsrettigheter, stillingsvern, arbeidstid: `aid-aml`-familien
- **NAV-loven** – organiseringen av etaten og NAV-kontoret: `nav-loven/merknader/generelt.md`
- **Sosialtjenesteloven** – økonomisk sosialhjelp, subsidiær til folketrygdytelser: `sosialtjenesteloven/merknader/generelt.md`
- **Utenfor dekket regelverk:** forvaltningsloven, trygderettsloven, yrkesskadeforsikringsloven, barnetrygdloven, kontantstøtteloven og EØS-trygdeforordningen (883/2004) er **ikke** dekket i noen AID-skill. EØS-reglene er særlig viktige: de går foran folketrygdlovens egne regler i mange grensekryssende saker. Når et spørsmål krever disse, **si eksplisitt fra at kilden ikke er dekket** – ikke gjett.

Les hele referansekjeden innenfor det skillen faktisk dekker før du trekker en negativ konklusjon.

## Kildegrunnlag og dekningshull

**Kilde:** Lovdata API, datasettene for gjeldende lover og gjeldende sentrale forskrifter, lisensiert NLOD 2.0. Konsolidert (ajourført) tekst.

**Ikke dekket: NAVs rundskriv.** Denne skillen inneholder lovtekst og forskriftstekst, men ingen rundskriv. Det er en forskjell fra de eldste skillene i ftrl-familien (`folketrygdloven/merknader/sykepenger.md`, `folketrygdloven/merknader/aap.md`, `folketrygdloven/merknader/uforetrygd.md`, `folketrygdloven/merknader/grunnstonad.md`, `folketrygdloven/merknader/hjelpemidler.md`), som har rundskriv med.

Folketrygdloven er et rettsområde der NAVs rundskriv er den sentrale kilden til hvordan skjønnsbestemmelsene praktiseres. Når et spørsmål gjelder forvaltningspraksis, si fra at kun lov- og forskriftstekst er gjennomgått.

**Satser og beløp:** de fleste satsene i folketrygden er knyttet til grunnbeløpet, som fastsettes årlig. Grunnbeløpsforskriften ligger i `folketrygdloven/merknader/medlemskap-beregning.md`. Oppgi aldri kronebeløp du ikke finner i en kildefil.

Bruk formuleringen «ingen bestemmelse funnet i gjennomgått materiale» framfor «finnes ikke».

## Endringslogg

Se `endringslogg.md`.
