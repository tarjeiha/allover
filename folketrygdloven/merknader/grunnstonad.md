> **Flyttet fra skillen `aid-ftrl-grunnstonad`** 16.10.2026. Teksten er ellers uendret, bortsett fra stiene.
> Alle stier er relative til basens rot. Hele lov- og forskriftsteksten ligger nå i basen. Der teksten
> sier at «denne skillen» bare dekker enkelte kapitler, at et regelverk «ikke er dekket», eller viser til
> andre skills, kan det være utdatert: sjekk tabellen i CLAUDE.md og veiviseren til loven.
> Kildereglene i CLAUDE.md gjelder foran det som står her.

# Oppslag i folketrygdloven - grunnstønad og hjelpestønad

## Hva denne skillen er for

Regelverksspørsmål om kap. 6 i folketrygdloven: tolkning av bestemmelser, regelverksanvendelse på et gitt (generisk) faktum, og utkast til tekst som beskriver regelverket (f.eks. til orienteringsnotater, svar på henvendelser, eller undervisningsmateriell).

Svar er alltid generelle regelverksfortolkninger - skillen bygger ikke videre på en identifiserbar sak eller person selv om detaljer skulle dukke opp i en henvendelse, men det er ikke noe å stoppe opp for eller lage apparat rundt.

**Denne skillen dekker kun kap. 6.** Spørsmål om sykepenger/pleiepenger (kap. 8/9), AAP (kap. 11/11 A), uføretrygd (kap. 12) eller hjelpemidler (kap. 10) hører til andre skills i samme familie (`folketrygdloven/merknader/sykepenger.md`, `folketrygdloven/merknader/aap.md`, `folketrygdloven/merknader/uforetrygd.md`, `folketrygdloven/merknader/hjelpemidler.md`) - foreslå riktig skill fremfor å svare utenfor eget kunnskapsgrunnlag.

## Kritisk: bruk alltid kildefilene - ikke svar fra generell kunnskap

At denne skillen er trigget, er ikke i seg selv en beskyttelse mot feil svar. Beskyttelsen ligger i at de faktiske fil-oppslagene under faktisk gjøres. Selv når et spørsmål virker kjent, enkelt, eller likt noe du "vet" om folketrygdloven fra før: **åpne og les den faktiske lovtekst- og/eller rundskrivfilen før du svarer om innholdet i en konkret paragraf eller diagnose.** Generell kunnskap om ftrl kan være utdatert, upresis på ledd-nivå, eller rett og slett feil - hele poenget med denne skillen er å erstatte den kunnskapen med et faktisk filoppslag, ikke å supplere den. Dette gjelder også når spørsmålet er uspesifikt formulert - identifiser riktig paragraf/diagnose først, les filen, svar deretter.

**Når brukeren ber om å se/vise lovteksten eller forskriftsteksten:** gjengi kildefilen ordrett og i sin helhet – inkludert bokstavpunkter, underoverskrifter og leddnummerering slik de står i kildefilen. Ikke sammenfatt, omformuler eller utelat strukturelementer med mindre brukeren eksplisitt ber om et sammendrag.

## Hva som finnes av kilder

- **Lovtekst** (`folketrygdloven/lov/`): full, uavkortet paragraftekst hentet fra Lovdatas åpne API (NLOD 2.0), oppdatert automatisk gjennom den ukentlige regelverkssjekken. Flat struktur - én fil per paragraf (`par-6-3.md` osv.), pluss `oversikt.md` og `temaoppslag.md`. Full dekning - alle ti paragrafer (§ 6-1 til § 6-9, inkl. § 6-1 a). Lovtekst er det eneste som skal siteres som gjeldende rett.
- **Rundskriv til kapittel 6** (`folketrygdloven/rundskriv/ftrl/kap-6/`): NAVs kommentarer til hver paragraf, hentet fra R06-00 (28.08.2026 - manuelt hentet, oppdateres ikke automatisk), pluss `generell-del.md`. Full dekning. Dette er NAVs praktisering og tolkning av loven - **ikke** loven selv. Svar som bruker rundskriv skal eksplisitt markere kilden som forvaltningspraksis, atskilt fra det som er sitert fra selve lovteksten.
  - **Filstruktur for lange kommentarer:** `par-<paragraf>-00-oversikt.md` lister underseksjonene der kommentaren er delt opp. Les oversiktsfilen først.
- **Diagnosebaserte retningslinjer** (`folketrygdloven/rundskriv/ftrl/kap-6/retningslinjer-diagnoser/`): NAVs retningslinjer for hjelpestønad/forhøyet hjelpestønad ved ti navngitte diagnoser (astma, blødersykdommer, cystisk fibrose, diabetes, Downs syndrom, døvhet/sterk tunghørthet, fenylketonuri, hofteleddsdysplasi, kreft hos barn, psykisk utviklingshemming), hentet fra R06-04-FOR (28.08.2026). Organisert per diagnose, ikke per paragraf - gjelder § 6-4 og § 6-5 samlet. Les `oversikt.md` for å finne riktig fil. Supplerer, erstatter ikke, hovedrundskrivets kommentarer til § 6-4/§ 6-5.

**Kryssreferanser utenfor denne skillen.** Når en paragraf henviser til et annet kapittel, gjengi henvisningen som den står i loven, men ikke gjett på innholdet. Si eksplisitt fra at kryssreferansen ikke er sjekket. For kap. 8, 9, 10, 11/11 A og 12 finnes egne skills (`folketrygdloven/merknader/sykepenger.md`, `folketrygdloven/merknader/hjelpemidler.md`, `folketrygdloven/merknader/aap.md`, `folketrygdloven/merknader/uforetrygd.md`) - nevn hvilken hvis relevant. Andre kapitler (1-5, 7, 13, 14, 21, 22 m.fl.) er ikke dekket av noen av disse skillene ennå.

## Oppslagslogikk

**1. Direkte paragrafhenvisning.** Gjenkjenn alle vanlige skrivemåter: "§ 6-3", "ftrl § 6-4", "paragraf 6-1 a". Match mot filnavn `folketrygdloven/lov/par-6-<paragrafnummer><evt. bokstav>.md`, f.eks. § 6-1 a → `par-6-1a.md`. Les filen direkte og bruk lovteksten.

**Når noen ber om å "vise" en paragraf, skal svaret være selve lovteksten - ordrett, alle ledd, ikke en oppsummering.** Oppsummering leveres bare når det eksplisitt er bedt om, eller når paragrafen inngår som ledd i en drøftelse av noe annet. Hvis noen ber om å "vise rundskrivet til" en paragraf, er det rundskrivfilen(e) som skal vises/brukes.

**2. Temaoppslag.** Bruk `folketrygdloven/merknader/temaoppslag-grunnstonad.md` for å finne riktig paragraf ut fra tema.

**3. Henvisningskjeder - avgjørende for negative konklusjoner.** Før en konklusjon av typen «X har ikke...», «det finnes ingen mekanisme for...» trekkes, skal **alle** paragrafer/ledd i henvisningskjeden som ligger innenfor kap. 6 være lest - ikke bare den første som bekrefter hypotesen. Hvis kjeden går til et kapittel utenfor kap. 6, stopp der og flagg det.

**4. Substansielle tolkningsspørsmål (hva betyr/hvordan praktiseres § X).** Les både lovtekst og rundskriv - lovteksten gir normen, rundskrivet gir NAVs praktisering. Hvis paragrafen har delt rundskrivfil, les oversiktsfilen først. For § 6-4/§ 6-5 ved en navngitt diagnose: sjekk også `folketrygdloven/rundskriv/ftrl/kap-6/retningslinjer-diagnoser/oversikt.md`. Hold kildene atskilt i svaret.

## Format på lovtekstfilene

Hver fil har en overskrift, en `**Kilde:**`-linje, deretter lovteksten med ledd som egne `**N. ledd**`-overskrifter (1., 2., 3. …). Bokstavlister (a, b, c …) er underpunkter i det ledd de hører til, ikke egne ledd. Endringshistorikk står som løpende tekst nederst i filen under `**Endringshistorikk:**` - metadata, ikke gjeldende rett i seg selv.

## Fremtidig utvidelse (ikke igangsatt)

- Forarbeider (proposisjoner, høringsnotater).
- Rettspraksis - lavere prioritert enn forarbeider, siden rundskrivene allerede refererer relevant rettspraksis der det trengs.
- Fellesbestemmelser (kap. 1, 2, 21, 22 m.fl.) - vurderes når behovet er tydeligere.
