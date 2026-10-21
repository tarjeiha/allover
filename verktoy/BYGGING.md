# Bygging av regelverksbasen

Håndbok for den som legger til regelverk, endrer byggeverktøyene eller skriver veivisere og merknader. Den samler lærdommene fra de gamle regelverksskillene (folketrygdloven, arbeidsmiljøloven m.fl.), der kildeteksten ble bygget inn i hver skill. Mange av punktene under er feil noen allerede har gjort én gang.

Byggingen skjer nå her i repoet. Skillene er tynne pekere som henter `CLAUDE.md`, så ingen skill må bygges eller lastes opp på nytt når innholdet endres.

## Verktøyene

| Skript | Gjør | Kjøres av |
|---|---|---|
| `bygg.py` | Lov- og forskriftstekst fra Lovdatas åpne datasett, `indeks.tsv` og AUTO-blokkene i `CLAUDE.md` og veiviserne | `bygg-regelverk.yml`, hver natt |
| `parse_lovdata.py` | Parser for Lovdata-XML (brukes av `bygg.py`) | |
| `endringer.py` | Vedtatte endringer som ikke er i kraft, fra Norsk Lovtidend | `bygg.py` |
| `eu.py` | EU-rettsakter fra EUR-Lex med låst versjon | `bygg.py` |
| `rundskriv.py` | Rundskriv fra `innboks/` (PDF, Word, HTML m.m.) | `rundskriv.yml` |
| `rundskriv_hent.py` | Henter NAVs rundskriv til folketrygdloven fra Lovdata til innboksen | `rundskriv-hent.yml`, manuelt |
| `r45.py` | Henter Navs EØS-rundskriv R45-00 fra Lovdata og deler det opp under trygdeforordningen (`regelverk/eu/forordning-883-2004/rundskriv/r45-00/`), bare når «Sist endret» er ny. Innboksen passer ikke for R45, som er delt i kapitler og punkter, ikke paragrafer | `r45-hent.yml`, hver natt |
| `avtale.py` | Deler opp hovedtariffavtalen fra Word | innboksen |
| `budsjett.py` | Deler opp Prop. 1 S, Gul bok og Nasjonalbudsjettet | manuelt |
| `sjekk_tekst.py` | Kontrollerer håndskrevne veivisere og merknader | `sjekk-tekst.yml` |

Hvert skript forklarer bruken øverst i filen. Lov- og forskriftstekst redigeres aldri for hånd. Det som står mellom `AUTO-START` og `AUTO-SLUTT`, skrives over ved hvert bygg.

## Legge til et regelverk

1. Legg loven og forskriftene inn i `regelverk.json` med Lovdata-ID (`LOV-…`, `FOR-…`).
2. Skriv den håndskrevne delen av `VEIVISER.md`: hva loven gjelder, kjente feller og hvilke merknader som finnes.
3. Legg til en linje i temalisten i `CLAUDE.md` med ordene folk faktisk bruker.
4. Legg mappen inn i `.github/CODEOWNERS` med den faglige eieren.
5. Kjør bygget på en testgren og les resultatet (se Verifisering).

### Velge forskrifter

Velg forskrifter ut fra hjemmelsfeltet (`dd.basedOn` i Lovdata-XML-en), ikke ut fra et søk på ord i teksten. Et søk på ord ga 16 treff for sosialtjenesteloven, men bare 4 av dem var reelle. Et av treffene var en forskrift fra 1992 som nå har hjemmel i helse- og omsorgstjenesteloven.

Når en forskrift har hjemmel i flere lover, legges den under loven som har flest av hjemlene, og veiviserne til de andre lovene viser dit. Ikke legg inn to kopier, for de vil gli fra hverandre ved oppdatering.

### Lover et annet departement eier

Når basen bare skal dekke en del av en lov (som utlendingsloven, der det meste hører til Justis- og beredskapsdepartementet), skal veiviseren si hvilke kapitler som er dekket og hvilke som hører til andre. Få avgrensningen bekreftet av fagmiljøet, fordi den er et faglig valg og ikke et teknisk. Bruk ikke for brede ord i temalisten i `CLAUDE.md`. «Oppholdstillatelse» alene trekker for eksempel inn asyl og familieinnvandring.

## Veiviser og merknader

- **Del etter fagområde, aldri etter kildetype.** Ingen spør «hva sier rundskrivet til § 8-12». De spør «hvor lenge kan man få sykepenger». Merknadsfilene deles derfor etter tema, og lov, forskrift og rundskriv holdes atskilt i mappene, ikke i hver sin inngang.
- **Kapitler som gjelder hele loven.** Virkeområde, beregning, saksbehandling, klage og tilbakekreving gjelder alle ytelser. Veiviseren skal si når svaret krever disse kapitlene i tillegg til ytelseskapitlet. Folketrygdloven kapittel 1–3 og 21–22 er eksempelet.
- **Kildelagene holdes atskilt:** lov (`lov/`), forskrifter (`forskrifter/<slug>/`), rundskriv (`rundskriv/`) og merknader (`merknader/`). Rundskriv til en forskrift følger nummereringen i forskriften, ikke i loven.
- **Si hva som mangler.** Når et kildelag mangler, skal veiviseren si hva konsekvensen er, f.eks. «kan ikke svare på beløp» hvis satsrundskrivet mangler. Det er mer nyttig enn «rundskriv er ikke lagt inn».
- **Kjente feller** skal være konkrete for akkurat dette regelverket, for eksempel at fødselsåret avgjør om folketrygdloven kapittel 19 eller 20 gjelder, eller at arbeidstidsreglene kan fravikes ved tariffavtale.
- **Stier skal være eksakte.** Skriv filnavn, ikke bare mapper. Når filnavnene varierer, skal veiviseren vise til `indeks.tsv`. I kaldtesten 18.10 gjettet modellen feil sti tre ganger fordi veiviseren bare viste til mappen.
- **Merknader flyttet fra de gamle skillene** kan fortsatt si «denne skillen» eller at et regelverk «ikke er i basen». `sjekk_tekst.py` fanger det siste. Les teksten når den flyttes.

## Verifisering

Alle parsefeil som er funnet hittil, har vært stille. De gir ingen feilmelding, bare manglende eller ødelagt innhold. Menerstatningsforskriften hadde riktig antall paragrafer, men manglet 92 % av teksten.

**Kontrollen må gjøres per paragraf og se på strukturen, ikke bare telle ord.** Tre feiltyper slipper gjennom en kontroll av ordmengden:

- **En utflatet tabell mister ingen ord.** Menerstatningsforskriften § 3 ble til «Gruppe Fastsatt invaliditetsgrad Menerstatning 0 Lavere enn 15% Ingen erstatning 1 15 – 24% 7% av grunnbeløpet …». Alle tallene er der, men de hører ikke lenger sammen to og to. Dette er farligere enn manglende innhold, fordi svaret ser fullstendig ut og tallene kobles feil.
- **Tap i én enhet drukner i totalen.** Femten paragrafer mistet hele noteapparatet uten at den samlede dekningen falt merkbart.
- **Innhold på feil plass mister ingen ord.** I EU-teksten ble et avsnitt delt midt i en setning, en artikkel fikk feil endringsmarkør, og en kapitteloverskrift havnet på slutten av forrige artikkel.

**Slik er det i dag:** `bygg.py` kontrollerer hver paragraf på to måter. Minst 98 % av ordene i kilden skal være med, og filen skal ha minst like mange tabeller, noter og listepunkter som kilden (`struktur()`). Endringshistorikken telles ikke med. Avvik gjør bygget rødt. `eu.py` og `avtale.py` kontrollerer bare ordene.

**Til du har bygget noe nytt:** Les minst én ferdig fil i sin helhet før du sier at en lov er ferdig. Velg den paragrafen med mest sammensatt struktur (tabeller, noter, mange endringsmarkører), fordi det er der feilene samler seg. Hvis kilden har tabeller, skal testsettet ha et kontrollspørsmål om tabellinnholdet med kjent fasit, f.eks. «hvilken menerstatning gir 45 % invaliditet».

## Feller i Lovdata-XML

`parse_lovdata.py` håndterer alle disse. Listen er her slik at en endring i parseren ikke innfører dem på nytt.

1. **Paragrafoverskriften står på ulike nivåer.** I lover står den på `h3`, i mange forskrifter på `h2`.
2. **Innhold kan ligge utenfor `legalP`.** Lister kan stå rett under `legalArticle`. Gå gjennom alle de direkte barna.
3. **Kapitler kan ha underinndeling.** Folketrygdloven kapittel 3, 8, 9 og 14 har romertall mellom kapittel og paragraf. Søk etter paragrafer rekursivt, og finn kapitler med `^kap\d+[A-Za-z]*$`.
4. **Viktig innhold kan stå helt utenfor paragrafene:** tabeller (menerstatningsforskriften), kommentarer (medleverforskriften) og forskrifter uten paragrafer (teater- og operaforskriften). Det skal i en egen fil (`utenfor-paragrafene.md` eller `tekst.md`).
5. **Tabeller inne i paragrafer** kan stå vilkårlig dypt i leddet. Hent ut lister og tabeller før teksten leses.
6. **Fotnoter** står i `<footer class="footnotes">` og falt tidligere bort uten varsel, mens tallet for henvisningen ble stående som et løst siffer i teksten. De gir ofte ikrafttredelse og avgrensning.
7. **Seksjonsinndelte forskrifter uten paragrafer** (læreplanene i norsk og samfunnskunnskap) må siteres med forskriftsnavn og overskrift, ikke med paragrafnummer.

Leddnummeret står i `id`-attributtet (`…-ledd-3`).

## Rundskriv og annet fra innboksen

- **Hvordan dokumentene er bygget opp, varierer.** NAVs hovedrundskriv har én overskrift per paragraf. Noen kapitler har paragrafene ett nivå høyere. Forskriftsrundskriv bruker nummereringen i forskriften. Folketrygdloven § 10-7 er kommentert i ni–ti separate dokumenter, ett per stønadsform. Undersøk hvordan et nytt dokument er bygget opp før du stoler på at det er delt riktig.
- **Lister og endringshistorikk i Word** står ofte som tabeller mellom avsnittene. Hvis bare avsnittene leses, faller de bort uten varsel.
- **Satsrundskriv** (f.eks. de veiledende retningslinjene for økonomisk stønad) erstattes hvert år. Et utdatert satsrundskriv er verre enn ingen, fordi svaret ser sikkert ut.
- **Endringer i et rundskriv:** NAV merker endringer med «Sist endret DD.MM.ÅÅÅÅ» og kortformen «[Endret M/ÅÅ]». Bruk datoene til å finne stedet, men les teksten før du konkluderer.
- **Tilgang:** Lovdatas sider for NAV-rundskriv og nav.no gir 403 fra Claudes sandkasse, men virker fra GitHub Actions. Bruk arbeidsflytene (`rundskriv-hent.yml`, `hent-url.yml`) i stedet for å lete etter andre veier.

## EU-rettsakter

- **Lås versjonen.** EUR-Lex viser EU-versjonen. En endring gjelder i Norge først når den er tatt inn i EØS-avtalen og har trådt i kraft der, og det kan ta flere år. `eu.py` skifter aldri versjon selv, men melder i veiviseren når det finnes en nyere.
- **Originalen og den konsoliderte versjonen** skilles bare av første siffer i CELEX-nummeret: `32004R0883` er originalen og `02004R0883` den konsoliderte versjonen.
- **Kontroller mot norsk lov før du fyller ut `eos`.** For trygdeforordningene viser folketrygdloven § 1-3 a hvilke endringsforordninger som gjelder i Norge. Sammenlign med listen over endringer i EUR-Lex-teksten.
- **Språk:** Det finnes ingen offisiell norsk konsolidert tekst (Lovdata bruker dansk). Engelsk er standard, og svaret må si at det er oversatt.

## Testing av basen

Kaldtest betyr å stille spørsmål til en økt som bare har skillen og ingen kontekst. Bruk spørsmålene i dette mønsteret: dekket med fagord, dekket med hverdagsspråk, ikke dekket (skal si fra og vise til Lovdata), og ikke regelverk (skal ikke bruke basen). Test også sømmene, altså spørsmål som trenger to regelverk eller lov sammen med EU-rett, og ikke bare kjernen.

Når skillen trigger og leser riktig, men svaret likevel blir feil, ligger feilen som oftest i basen: en sti som ikke finnes, en foreldet merknad eller en veiviser som peker feil. Rett den i basen, ikke i skillen.
