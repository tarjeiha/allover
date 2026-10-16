> **Flyttet fra skillen `aid-ftrl-uforetrygd`** 16.10.2026. Teksten er ellers uendret, bortsett fra stiene.
> Alle stier er relative til basens rot. Hele loven ligger nå i basen, så der teksten sier at
> «denne skillen» bare dekker enkelte kapitler eller viser til andre skills, gjelder det ikke lenger:
> se veiviseren til loven. Kildereglene i CLAUDE.md gjelder foran det som står her.

# Oppslag i folketrygdloven - uføretrygd

## Hva denne skillen er for

Regelverksspørsmål om kap. 12 i folketrygdloven, inkludert tilhørende forskrifter: tolkning av bestemmelser, regelverksanvendelse på et gitt (generisk) faktum, og utkast til tekst som beskriver regelverket (f.eks. til orienteringsnotater, svar på henvendelser, eller undervisningsmateriell).

Svar er alltid generelle regelverksfortolkninger - skillen bygger ikke videre på en identifiserbar sak eller person selv om detaljer skulle dukke opp i en henvendelse, men det er ikke noe å stoppe opp for eller lage apparat rundt.

**Denne skillen dekker kun kap. 12.** Spørsmål om sykepenger/pleiepenger (kap. 8/9), AAP (kap. 11/11 A), grunnstønad/hjelpestønad (kap. 6) eller hjelpemidler (kap. 10) hører til andre skills i samme familie (`folketrygdloven/merknader/sykepenger.md`, `folketrygdloven/merknader/aap.md`, `folketrygdloven/merknader/grunnstonad.md`, `folketrygdloven/merknader/hjelpemidler.md`) - foreslå riktig skill fremfor å svare utenfor eget kunnskapsgrunnlag.

## Kritisk: bruk alltid kildefilene - ikke svar fra generell kunnskap

At denne skillen er trigget, er ikke i seg selv en beskyttelse mot feil svar. Beskyttelsen ligger i at de faktiske fil-oppslagene under faktisk gjøres. Selv når et spørsmål virker kjent, enkelt, eller likt noe du "vet" om folketrygdloven fra før: **åpne og les den faktiske lovtekst- og/eller rundskrivfilen før du svarer om innholdet i en konkret paragraf eller ytelse.** Generell kunnskap om ftrl kan være utdatert, upresis på ledd-nivå, eller rett og slett feil - hele poenget med denne skillen er å erstatte den kunnskapen med et faktisk filoppslag, ikke å supplere den. Dette gjelder også når spørsmålet er uspesifikt formulert - identifiser riktig paragraf først, les filen, svar deretter.

**Når brukeren ber om å se/vise lovteksten eller forskriftsteksten:** gjengi kildefilen ordrett og i sin helhet – inkludert bokstavpunkter, underoverskrifter og leddnummerering slik de står i kildefilen. Ikke sammenfatt, omformuler eller utelat strukturelementer med mindre brukeren eksplisitt ber om et sammendrag.

## Hva som finnes av kilder

- **Lovtekst** (`folketrygdloven/lov/`): full, uavkortet paragraftekst hentet fra Lovdatas åpne API (NLOD 2.0), oppdatert automatisk gjennom den ukentlige regelverkssjekken. Flat struktur - én fil per paragraf (`par-12-13.md` osv.), pluss `oversikt.md` og `temaoppslag.md`. Full dekning - alle 22 gjeldende paragrafer (§ 12-1 til § 12-21, inkl. § 12-1 a) finnes. Lovtekst er det eneste som skal siteres som gjeldende rett.
- **Forskriftstekst** (`forskrifter/<forskrift-slug>/par-<paragrafnummer>.md`): full forskriftstekst hentet fra Lovdatas API, samme automatiske oppdatering som lovteksten. Tre forskrifter er lagt inn:
  - `omregning-uforepensjon-til-uforetrygd/` - FOR-2014-07-03-947, §1-§10, relevant for § 12-13.
  - `okt-beregningsgrunnlag-gift-samboende/` - FOR-2016-05-26-529, §1-§4, relevant for § 12-13/14.
  - `uforetrygdforskriften/` - FOR-2014-12-05-1602 (Forskrift om uføretrygd fra folketrygden), kap. 1-9, §§1-1 til 9-1 (§7-2 opphevet), relevant for §§ 12-9, 12-11, 12-14 til 12-17 og 21-10.
- **Rundskriv til kapittel 12** (`folketrygdloven/rundskriv/ftrl/kap-12/`): NAVs kommentarer, hentet fra R12-00 (28.08.2026 - manuelt hentet, oppdateres ikke automatisk), pluss `generell-del.md`. Full dekning - alle 22 gjeldende paragrafer har egen kommentar. Dette er NAVs praktisering og tolkning av loven - **ikke** loven selv. Svar som bruker rundskriv skal eksplisitt markere kilden som forvaltningspraksis, atskilt fra det som er sitert fra selve lovteksten.
  - **Filstruktur for lange kommentarer:** `par-<paragraf>-00-oversikt.md` lister underseksjonene, `par-<paragraf>-01-...md` osv. inneholder selve innholdet. Les oversiktsfilen først.
- **Rundskriv til forskrift** (`folketrygdloven/rundskriv/forskrifter/<forskrift-slug>/`): NAVs kommentarer til enkeltforskrifter, nøkket på forskriftens egen paragrafnummerering, ikke ftrl sin.
  - `omregning-uforepensjon-til-uforetrygd/` - til § 12-13. Full paragrafinndeling (`par-1.md` til `par-9.md`). Selve forskriftsteksten finnes i `folketrygdloven/forskrifter/omregning-uforepensjon-til-uforetrygd/`.
  - `okt-beregningsgrunnlag-gift-samboende/` - til § 12-13/14. **Ikke splittet per paragraf** - hele forskriften (§1-§4) er kommentert i én sammenhengende fil (`innledning.md`), siden originaldokumentet ikke skiller paragrafene på overskriftsnivå. Slå opp i innholdet, ikke bare filnavnet. Selve forskriftsteksten finnes i `folketrygdloven/forskrifter/okt-beregningsgrunnlag-gift-samboende/`.
  - `uforetrygdforskriften-kap7/` - til § 12-9/12-11 (fastsetting av inntekt/uførepensjon). Kommenterer kun forskriftens EGET kapittel 7 (§7-1 til §7-6, § 7-4 finnes ikke i kildematerialet). FOR-nummer bekreftet: FOR-2014-12-05-1602. Forskriftsteksten finnes i `folketrygdloven/forskrifter/uforetrygdforskriften/`.
  - `overgangsregler-barnetillegg-uforetrygd-2015/` - til § 12-15/12-16, FOR-2015-09-23-1095. Ingen tilhørende forskriftstekst er lagt inn.
  - `uredusert-ytelse-institusjon/` - til § 12-19, FOR-2014-10-31-1375. Ingen tilhørende forskriftstekst er lagt inn.
  - `beregning-uforetrygd-institusjon/` - til § 12-19, FOR-2014-10-31-1376. Ingen tilhørende forskriftstekst er lagt inn.
  - Der forskriftstekst ikke er nevnt over, er den ikke lagt inn - kun NAVs kommentarer. Si eksplisitt fra at forskriftsteksten ikke er sjekket direkte i disse tilfellene.

**Kryssreferanser utenfor denne skillen.** Når en paragraf henviser til et annet kapittel, gjengi henvisningen som den står i loven, men ikke gjett på innholdet. Si eksplisitt fra at kryssreferansen ikke er sjekket. For kap. 6, 8, 9, 10 og 11/11 A finnes egne skills (`folketrygdloven/merknader/grunnstonad.md`, `folketrygdloven/merknader/sykepenger.md`, `folketrygdloven/merknader/hjelpemidler.md`, `folketrygdloven/merknader/aap.md`) - nevn hvilken hvis relevant. Andre kapitler (1-5, 7, 13, 14, 21, 22 m.fl.) er ikke dekket av noen av disse skillene ennå.

## Oppslagslogikk

**1. Direkte paragrafhenvisning.** Gjenkjenn alle vanlige skrivemåter: "§ 12-13", "ftrl § 12-7", "paragraf 12-1 a". Match mot filnavn `folketrygdloven/lov/par-12-<paragrafnummer><evt. bokstav>.md`, f.eks. § 12-1 a → `par-12-1a.md`. Les filen direkte og bruk lovteksten.

**Når noen ber om å "vise" en paragraf, skal svaret være selve lovteksten - ordrett, alle ledd, ikke en oppsummering.** Oppsummering leveres bare når det eksplisitt er bedt om, eller når paragrafen inngår som ledd i en drøftelse av noe annet. Hvis noen ber om å "vise rundskrivet til" en paragraf, er det rundskrivfilen(e) som skal vises/brukes.

**2. Temaoppslag.** Bruk `folketrygdloven/merknader/temaoppslag-uforetrygd.md` for å finne riktig paragraf ut fra tema.

**3. Henvisningskjeder - avgjørende for negative konklusjoner.** Før en konklusjon av typen «X har ikke...», «det finnes ingen mekanisme for...» trekkes, skal **alle** paragrafer/ledd i henvisningskjeden som ligger innenfor kap. 12 være lest - ikke bare den første som bekrefter hypotesen. Hvis kjeden går til et kapittel utenfor kap. 12, stopp der og flagg det.

**4. Substansielle tolkningsspørsmål (hva betyr/hvordan praktiseres § X).** Les både lovtekst og rundskriv - lovteksten gir normen, rundskrivet gir NAVs praktisering. Hvis paragrafen har delt rundskrivfil, les oversiktsfilen først. For § 12-9, § 12-11, § 12-13 til § 12-17, § 12-19 og § 21-10 kan `forskrifter/<slug>/` og `folketrygdloven/rundskriv/forskrifter/<slug>/` også være relevant - se oversikten over forskriftskildene over for hvilken mappe som hører til hvilken paragraf. Hold kildene atskilt i svaret.

## Format på lovtekstfilene

Hver fil (lovtekst og forskriftstekst) har en overskrift, en `**Kilde:**`-linje, deretter teksten med ledd som egne `**N. ledd**`-overskrifter (1., 2., 3. …). Bokstavlister (a, b, c …) er underpunkter i det ledd de hører til, ikke egne ledd. Endringshistorikk står som løpende tekst nederst i filen under `**Endringshistorikk:**` - metadata, ikke gjeldende rett i seg selv.

## Fremtidig utvidelse (ikke igangsatt)

- Selve forskriftsteksten for de tre resterende forskriftene (overgangsregler barnetillegg, de to institusjonsforskriftene) - ikke lagt inn ennå, kun NAVs kommentarer.
- Forarbeider (proposisjoner, høringsnotater).
- Rettspraksis - lavere prioritert enn forarbeider, siden rundskrivene allerede refererer relevant rettspraksis der det trengs.
- Fellesbestemmelser (kap. 1, 2, 21, 22 m.fl.) - vurderes når behovet er tydeligere.
