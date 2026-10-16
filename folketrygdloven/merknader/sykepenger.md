> **Flyttet fra skillen `aid-ftrl-sykepenger`** 16.10.2026. Teksten er ellers uendret, bortsett fra stiene.
> Alle stier er relative til basens rot. Hele loven ligger nå i basen, så der teksten sier at
> «denne skillen» bare dekker enkelte kapitler eller viser til andre skills, gjelder det ikke lenger:
> se veiviseren til loven. Kildereglene i CLAUDE.md gjelder foran det som står her.

# Oppslag i folketrygdloven - sykepenger og pleiepenger

## Hva denne skillen er for

Regelverksspørsmål om kap. 8 og 9 i folketrygdloven: tolkning av bestemmelser, regelverksanvendelse på et gitt (generisk) faktum, sammenligning av kap. 8 og 9, og utkast til tekst som beskriver regelverket (f.eks. til orienteringsnotater, svar på henvendelser, eller undervisningsmateriell).

Svar er alltid generelle regelverksfortolkninger - skillen bygger ikke videre på en identifiserbar sak eller person selv om detaljer skulle dukke opp i en henvendelse, men det er ikke noe å stoppe opp for eller lage apparat rundt.

**Denne skillen dekker kun kap. 8 og 9.** Spørsmål om AAP (kap. 11/11 A), uføretrygd (kap. 12), grunnstønad/hjelpestønad (kap. 6) eller hjelpemidler (kap. 10) hører til andre skills i samme familie (`folketrygdloven/merknader/aap.md`, `folketrygdloven/merknader/uforetrygd.md`, `folketrygdloven/merknader/grunnstonad.md`, `folketrygdloven/merknader/hjelpemidler.md`) - foreslå riktig skill fremfor å svare utenfor eget kunnskapsgrunnlag.

## Kritisk: bruk alltid kildefilene - ikke svar fra generell kunnskap

At denne skillen er trigget, er ikke i seg selv en beskyttelse mot feil svar. Beskyttelsen ligger i at de faktiske fil-oppslagene under faktisk gjøres. Selv når et spørsmål virker kjent, enkelt, eller likt noe du "vet" om folketrygdloven fra før: **åpne og les den faktiske lovtekst- og/eller rundskrivfilen før du svarer om innholdet i en konkret paragraf eller ytelse.** Generell kunnskap om ftrl kan være utdatert, upresis på ledd-nivå, eller rett og slett feil - hele poenget med denne skillen er å erstatte den kunnskapen med et faktisk filoppslag, ikke å supplere den. Dette gjelder også når spørsmålet er uspesifikt formulert (se ruter-tabellen under) - identifiser riktig kapittel/paragraf først, les filen, svar deretter.

**Når brukeren ber om å se/vise lovteksten eller forskriftsteksten:** gjengi kildefilen ordrett og i sin helhet – inkludert bokstavpunkter, underoverskrifter og leddnummerering slik de står i kildefilen. Ikke sammenfatt, omformuler eller utelat strukturelementer med mindre brukeren eksplisitt ber om et sammendrag.

## Hvilket kapittel gjelder spørsmålet? (ruter)

| Tema | Kapittel |
|---|---|
| Sykepenger, egenmelding, arbeidsuførhet | 8 |
| Omsorgspenger, pleiepenger, opplæringspenger (barn/nærstående sykdom) | 9 |

Når kapittel er identifisert (eller gitt direkte via paragrafnummer), les `folketrygdloven/merknader/temaoppslag-sykepenger.md` for detaljert paragrafoversikt for det aktuelle kapitlet. Filen har egne seksjoner for kapittel 8 og kapittel 9 - ikke les hele filen rutinemessig hvis spørsmålet gjelder ett konkret kapittel.

## Hva som finnes av kilder

- **Lovtekst** (`folketrygdloven/lov/`): full, uavkortet paragraftekst hentet fra Lovdatas åpne API (NLOD 2.0), oppdatert automatisk gjennom den ukentlige regelverkssjekken. Flat struktur - én fil per paragraf (`par-8-4.md`, `par-9-5.md` osv.), pluss `oversikt.md` (paragrafliste gruppert på kapittel) og `temaoppslag.md` (tema→paragraf-tabell for begge kapitler, inkl. paralleller mellom dem). Lovtekst er det eneste som skal siteres som gjeldende rett. `oversikt.md` viser `Sist endret i kraft`-dato for loven som helhet.
- **Rundskriv** (`folketrygdloven/rundskriv/ftrl/kap-8/`, `kap-9/`): NAVs kommentarer til hver paragraf, hentet fra R08-00 og R09-00 (28.08.2026 - manuelt hentet, oppdateres ikke automatisk). Dette er NAVs praktisering og tolkning av loven - **ikke** loven selv. Rundskriv kan gi en snevrere eller videre fortolkning enn ordlyden isolert sett tilsier. Svar som bruker rundskriv skal eksplisitt markere kilden som forvaltningspraksis ("NAV legger til grunn i rundskrivet at …"), atskilt fra det som er sitert fra selve lovteksten.
  - **Filstruktur:** paragrafer med kort kommentar ligger som én fil (`par-8-2.md`). Paragrafer med lang kommentar (§ 8-4, 8-5, 8-7, 8-7a, 8-8, 8-9, 8-17, 8-34) er delt i flere filer pga. lengde: `par-<paragraf>-00-oversikt.md` lister underseksjonene, `par-<paragraf>-01-...md` osv. inneholder selve innholdet. Les oversiktsfilen først for å finne riktig underseksjon - ikke les alle underseksjonene rutinemessig hvis spørsmålet gjelder ett konkret ledd.
  - § 9-1 a og § 9-11 a har ingen egen kommentarseksjon - bruk lovtekst for disse. § 9-12 er opphevet og har bare en henvisning til opphevelsesloven.
  - `sist_endret_rundskriv` i frontmatter (rundskrivfilene) er metadata om når NAVs kommentar sist ble omarbeidet - ikke det samme som lovtekstfilens `Endringshistorikk` (som gjelder selve lovbestemmelsen).
- **Forarbeider** (`folketrygdloven/forarbeider/`): tomt foreløpig.
- **Ikke dekket:** ikrafttredelse/overgangsregler for kap. 9 (V2-09-00) - ikke innarbeidet ennå, se rundskriv-ftrl-sjekkliste. Veiledning for utfylling av sykmeldingsblankett (praktisk/administrativ, ikke regelverkstolkning - se nav.no for gjeldende blankett). EØS/rådsforordning knyttet til § 8-9 (sykepenger ved opphold i andre EØS-land) - ikke innarbeidet, avventer avklaring av metodikk for EU/EØS-regelverk generelt (jf. `aid-ftrl-dagpenger/eu-eos/` for et annet, allerede bygget eksempel).

**Kryssreferanser utenfor denne skillen.** Når en paragraf i kap. 8/9 henviser til en paragraf i et annet kapittel, gjengi henvisningen som den står i loven, men ikke gjett på innholdet. Si eksplisitt fra at kryssreferansen ikke er sjekket. For kap. 6, 10, 11, 11 A og 12 finnes egne skills (`folketrygdloven/merknader/grunnstonad.md`, `folketrygdloven/merknader/hjelpemidler.md`, `folketrygdloven/merknader/aap.md`, `folketrygdloven/merknader/uforetrygd.md`) - nevn hvilken hvis relevant. Andre kapitler (1-5, 7, 13, 14, 21, 22 m.fl.) er ikke dekket av noen av disse skillene ennå.

## Oppslagslogikk

**1. Direkte paragrafhenvisning.** Gjenkjenn alle vanlige skrivemåter: "§ 8-4", "ftrl § 9-5", "paragraf 8-13", "§ 9-1 a". Match mot filnavn `folketrygdloven/lov/par-<kapittel>-<paragrafnummer><evt. bokstav>.md`, f.eks. § 8-4 → `par-8-4.md`, § 9-1 a → `par-9-1a.md`. Les filen direkte og bruk lovteksten.

**Når noen ber om å "vise" en paragraf ("vis § 8-7", "vis meg 9-5"), skal svaret være selve lovteksten - ordrett, alle ledd, ikke en oppsummering eller et sammendrag.** Oppsummering leveres bare når det eksplisitt er bedt om et sammendrag, eller når paragrafen inngår som ledd i en drøftelse av noe annet. Hvis noen ber om å "vise rundskrivet til" en paragraf, eller "hva sier NAV om ...", er det rundskrivfilen(e) som skal vises/brukes.

**2. Temaoppslag.** Bruk ruter-tabellen over til å finne riktig kapittel, deretter `folketrygdloven/merknader/temaoppslag-sykepenger.md` for riktig paragraf.

**3. Sammenligning kap. 8 vs. 9.** Bruk paralleltabellen i `folketrygdloven/merknader/temaoppslag-sykepenger.md`.

**4. Henvisningskjeder - avgjørende for negative konklusjoner.** Mange paragrafer henviser videre til andre paragrafer/ledd, ofte flere samlet (f.eks. § 8-38 femte ledd viser til § 8-28, § 8-29 og § 8-30 første til tredje ledd for frilanseres sykepengegrunnlag). Før en konklusjon av typen «X har ikke...», «Y gjelder ikke for...», «det finnes ingen mekanisme for...» trekkes, skal **alle** paragrafer/ledd i henvisningskjeden som ligger innenfor kap. 8/9 være lest - ikke bare den første som bekrefter hypotesen. Å finne ett unntak eller én begrensning i den første henviste bestemmelsen er ikke nok til å konkludere at noe mangler; en senere bestemmelse i kjeden kan gi det tilbake på annet grunnlag. Hvis kjeden går til et kapittel utenfor kap. 8/9, stopp der og flagg det.

**5. Substansielle tolkningsspørsmål (hva betyr/hvordan praktiseres § X).** Les både lovtekst og rundskriv - lovteksten gir normen, rundskrivet gir NAVs praktisering. Hvis paragrafen har delt rundskrivfil, les oversiktsfilen først. For § 9-1 a, § 9-11 a og § 9-12: bruk lovtekst alene.

## Format på lovtekstfilene

Hver fil har en overskrift (`# § 8-4. Arbeidsuførhet`), en `**Kilde:**`-linje, deretter lovteksten med ledd som egne `**N. ledd**`-overskrifter (1., 2., 3. …). Bokstavlister (a, b, c …) er underpunkter i det ledd de hører til, ikke egne ledd. Endringshistorikk står som løpende tekst nederst i filen under `**Endringshistorikk:**` - det er metadata om når bestemmelsen sist ble endret, ikke gjeldende rett i seg selv, og skal ikke brukes som grunnlag for tolkning.

## Fremtidig utvidelse (ikke igangsatt)

- Rundskriv til § 9-1 a og § 9-11 a - ingen kjent NAV-kilde funnet for disse.
- Forarbeider (proposisjoner, høringsnotater).
- Rettspraksis - lavere prioritert enn forarbeider, siden rundskrivene allerede refererer relevant rettspraksis der det trengs.
- Fellesbestemmelser (kap. 1, 2, 21, 22 m.fl.) - vurderes når behovet er tydeligere.
