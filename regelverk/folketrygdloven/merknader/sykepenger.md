> **Flyttet fra skillen `aid-ftrl-sykepenger`** 16.10.2026 og ryddet 18.10.2026. Merknaden er hjelp til å finne fram og unngå vanlige feil, ikke lov- eller forskriftstekst. Kildereglene i CLAUDE.md gjelder foran det som står her.

# Oppslag i folketrygdloven - sykepenger og pleiepenger

## Hva merknaden gjelder

Regelverksspørsmål om kap. 8 og 9 i folketrygdloven: tolkning av bestemmelser, regelverksanvendelse på et gitt (generisk) faktum, sammenligning av kap. 8 og 9, og utkast til tekst som beskriver regelverket (f.eks. til orienteringsnotater, svar på henvendelser, eller undervisningsmateriell).

Svar er alltid generelle regelverksfortolkninger - de bygger ikke videre på en identifiserbar sak eller person selv om detaljer skulle dukke opp i en henvendelse, men det er ikke noe å stoppe opp for eller lage apparat rundt.

**Denne merknaden gjelder kap. 8 og 9.** For AAP (kap. 11/11 A), uføretrygd (kap. 12), grunnstønad/hjelpestønad (kap. 6), hjelpemidler (kap. 10) og andre kapitler: se tabellen over merknader og rundskriv i `regelverk/folketrygdloven/VEIVISER.md`.

## Vanlige feil

Generell kunnskap om folketrygdloven kan være utdatert, upresis på leddnivå eller rett og slett feil. Det gjelder også når spørsmålet virker kjent eller enkelt. Er spørsmålet uspesifikt formulert, identifiser riktig kapittel og paragraf først (se tabellen under), les filen, og svar deretter.

## Hvilket kapittel gjelder spørsmålet? (ruter)

| Tema | Kapittel |
|---|---|
| Sykepenger, egenmelding, arbeidsuførhet | 8 |
| Omsorgspenger, pleiepenger, opplæringspenger (barn/nærstående sykdom) | 9 |

Når kapittel er identifisert (eller gitt direkte via paragrafnummer), les `regelverk/folketrygdloven/merknader/temaoppslag-sykepenger.md` for detaljert paragrafoversikt for det aktuelle kapitlet. Filen har egne seksjoner for kapittel 8 og kapittel 9 - ikke les hele filen rutinemessig hvis spørsmålet gjelder ett konkret kapittel.

## Hva som finnes av kilder

- **Lovtekst** (`regelverk/folketrygdloven/lov/`): full, uavkortet paragraftekst hentet fra Lovdatas åpne API (NLOD 2.0), oppdatert automatisk gjennom den ukentlige regelverkssjekken. Flat struktur - én fil per paragraf (`par-8-4.md`, `par-9-5.md` osv.). Paragraflisten gruppert på kapittel står i `regelverk/folketrygdloven/VEIVISER.md`, og tema→paragraf-tabellen for begge kapitler, med paralleller mellom dem, står i `regelverk/folketrygdloven/merknader/temaoppslag-sykepenger.md`. Lovtekst er det eneste som skal siteres som gjeldende rett. Veiviseren viser `Sist endret i kraft`-dato for loven som helhet.
- **Rundskriv** (`regelverk/folketrygdloven/rundskriv/ftrl/kap-8/`, `kap-9/`): NAVs kommentarer til hver paragraf, hentet fra R08-00 og R09-00 (28.08.2026 - manuelt hentet, oppdateres ikke automatisk). Dette er NAVs praktisering og tolkning av loven - **ikke** loven selv. Rundskriv kan gi en snevrere eller videre fortolkning enn ordlyden isolert sett tilsier. Svar som bruker rundskriv skal eksplisitt markere kilden som forvaltningspraksis ("NAV legger til grunn i rundskrivet at …"), atskilt fra det som er sitert fra selve lovteksten.
  - **Filstruktur:** paragrafer med kort kommentar ligger som én fil (`par-8-2.md`). Paragrafer med lang kommentar (§ 8-4, 8-5, 8-7, 8-7a, 8-8, 8-9, 8-17, 8-34) er delt i flere filer pga. lengde: `par-<paragraf>-00-oversikt.md` lister underseksjonene, `par-<paragraf>-01-...md` osv. inneholder selve innholdet. Les oversiktsfilen først for å finne riktig underseksjon - ikke les alle underseksjonene rutinemessig hvis spørsmålet gjelder ett konkret ledd.
  - § 9-1 a og § 9-11 a har ingen egen kommentarseksjon - bruk lovtekst for disse. § 9-12 er opphevet og har bare en henvisning til opphevelsesloven.
  - `sist_endret_rundskriv` i frontmatter (rundskrivfilene) er metadata om når NAVs kommentar sist ble omarbeidet - ikke det samme som lovtekstfilens `Endringshistorikk` (som gjelder selve lovbestemmelsen).
- **EØS:** Sykepenger, omsorgspenger, opplæringspenger og pleiepenger er ytelser ved sykdom etter trygdeforordningen (§ 8-1 a og § 9-1 a). Trygdeforordningen (EF) nr. 883/2004 og gjennomføringsforordningen (EF) nr. 987/2009 ligger i `regelverk/eu/forordning-883-2004/VEIVISER.md` og `regelverk/eu/forordning-987-2009/VEIVISER.md`, på engelsk. Ytelser ved sykdom står i trygdeforordningen avdeling III kapittel 1 (artikkel 17–35), kontantytelser i artikkel 21, og gjennomføringsforordningen artikkel 27 gjelder kontantytelser ved arbeidsuførhet ved opphold eller bosted i en annen medlemsstat. Bruk dem sammen med § 8-9 når spørsmålet gjelder sykepenger under opphold i et annet EØS-land. Det finnes ingen merknad om sykepenger og forordningene, og NAVs EØS-rundskriv (R45-00) er ikke i basen.
- **Ikke i basen:** ikrafttredelse og overgangsregler for kap. 9 (V2-09-00). Veiledning for utfylling av sykmeldingsblankett (praktisk/administrativ, ikke regelverkstolkning - se nav.no for gjeldende blankett).

**Kryssreferanser til andre kapitler.** Når en paragraf i kap. 8/9 henviser til en paragraf i et annet kapittel, åpne den paragrafen før du sier noe om innholdet. Hele loven ligger i `regelverk/folketrygdloven/lov/`, og merknadene for de andre kapitlene finnes via tabellen i `regelverk/folketrygdloven/VEIVISER.md`. Kapittel 1–3 (medlemskap, grunnbeløp) og 21–22 (saksbehandling, utbetaling, tilbakekreving) gjelder også sykepenger.

## Oppslagslogikk

**1. Direkte paragrafhenvisning.** Gjenkjenn alle vanlige skrivemåter: "§ 8-4", "ftrl § 9-5", "paragraf 8-13", "§ 9-1 a". Match mot filnavn `regelverk/folketrygdloven/lov/par-<kapittel>-<paragrafnummer><evt. bokstav>.md`, f.eks. § 8-4 → `par-8-4.md`, § 9-1 a → `par-9-1a.md`. Les filen direkte og bruk lovteksten.

Hvis noen ber om å "vise rundskrivet til" en paragraf, eller "hva sier NAV om ...", er det rundskrivfilen(e) som skal vises/brukes.

**2. Temaoppslag.** Bruk ruter-tabellen over til å finne riktig kapittel, deretter `regelverk/folketrygdloven/merknader/temaoppslag-sykepenger.md` for riktig paragraf.

**3. Sammenligning kap. 8 vs. 9.** Bruk paralleltabellen i `regelverk/folketrygdloven/merknader/temaoppslag-sykepenger.md`.

**4. Henvisningskjeder - avgjørende for negative konklusjoner.** Mange paragrafer henviser videre til andre paragrafer/ledd, ofte flere samlet (f.eks. § 8-38 femte ledd viser til § 8-28, § 8-29 og § 8-30 første til tredje ledd for frilanseres sykepengegrunnlag). Før en konklusjon av typen «X har ikke...», «Y gjelder ikke for...», «det finnes ingen mekanisme for...» trekkes, skal **alle** paragrafer/ledd i henvisningskjeden være lest - ikke bare den første som bekrefter hypotesen. Å finne ett unntak eller én begrensning i den første henviste bestemmelsen er ikke nok til å konkludere at noe mangler; en senere bestemmelse i kjeden kan gi det tilbake på annet grunnlag. Hvis kjeden går til et annet kapittel, les også de bestemmelsene.

**5. Substansielle tolkningsspørsmål (hva betyr/hvordan praktiseres § X).** Les både lovtekst og rundskriv - lovteksten gir normen, rundskrivet gir NAVs praktisering. Hvis paragrafen har delt rundskrivfil, les oversiktsfilen først. For § 9-1 a, § 9-11 a og § 9-12: bruk lovtekst alene.

## Format på lovtekstfilene

Hver fil har en overskrift (`# § 8-4. Arbeidsuførhet`), en `**Kilde:**`-linje, deretter lovteksten med ledd som egne `**N. ledd**`-overskrifter (1., 2., 3. …). Bokstavlister (a, b, c …) er underpunkter i det ledd de hører til, ikke egne ledd. Endringshistorikk står som løpende tekst nederst i filen under `**Endringshistorikk:**` - det er metadata om når bestemmelsen sist ble endret, ikke gjeldende rett i seg selv, og skal ikke brukes som grunnlag for tolkning.

## Fremtidig utvidelse (ikke igangsatt)

- Rundskriv til § 9-1 a og § 9-11 a - ingen kjent NAV-kilde funnet for disse.
- Forarbeider (proposisjoner, høringsnotater).
- Rettspraksis - lavere prioritert enn forarbeider, siden rundskrivene allerede refererer relevant rettspraksis der det trengs.
