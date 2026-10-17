> **Flyttet fra skillen `aid-ftrl-hjelpemidler`** 16.10.2026. Teksten er ellers uendret, bortsett fra stiene.
> Alle stier er relative til basens rot. Hele lov- og forskriftsteksten ligger nå i basen. Der teksten
> sier at «denne skillen» bare dekker enkelte kapitler, at et regelverk «ikke er dekket», eller viser til
> andre skills, kan det være utdatert: sjekk tabellen i CLAUDE.md og veiviseren til loven.
> Kildereglene i CLAUDE.md gjelder foran det som står her.

# Oppslag i folketrygdloven - hjelpemidler

## Hva denne skillen er for

Regelverksspørsmål om kap. 10 i folketrygdloven: tolkning av bestemmelser, regelverksanvendelse på et gitt (generisk) faktum, og utkast til tekst som beskriver regelverket (f.eks. til orienteringsnotater, svar på henvendelser, eller undervisningsmateriell).

Svar er alltid generelle regelverksfortolkninger - skillen bygger ikke videre på en identifiserbar sak eller person selv om detaljer skulle dukke opp i en henvendelse, men det er ikke noe å stoppe opp for eller lage apparat rundt.

**Denne skillen dekker kun kap. 10.** Spørsmål om sykepenger/pleiepenger (kap. 8/9), AAP (kap. 11/11 A), uføretrygd (kap. 12) eller grunnstønad/hjelpestønad (kap. 6) hører til andre skills i samme familie (`folketrygdloven/merknader/sykepenger.md`, `folketrygdloven/merknader/aap.md`, `folketrygdloven/merknader/uforetrygd.md`, `folketrygdloven/merknader/grunnstonad.md`) - foreslå riktig skill fremfor å svare utenfor eget kunnskapsgrunnlag.

## Kritisk: bruk alltid kildefilene - ikke svar fra generell kunnskap

At denne skillen er trigget, er ikke i seg selv en beskyttelse mot feil svar. Beskyttelsen ligger i at de faktiske fil-oppslagene under faktisk gjøres. Selv når et spørsmål virker kjent, enkelt, eller likt noe du "vet" om folketrygdloven fra før: **åpne og les den faktiske lovtekst- og/eller rundskrivfilen før du svarer om innholdet i en konkret paragraf eller stønadsform.** Generell kunnskap om ftrl kan være utdatert, upresis på ledd-nivå, eller rett og slett feil - hele poenget med denne skillen er å erstatte den kunnskapen med et faktisk filoppslag, ikke å supplere den. Dette gjelder også når spørsmålet er uspesifikt formulert - identifiser riktig paragraf/stønadsform først (se `folketrygdloven/rundskriv/ftrl/kap-10/paragraf-10-7/oversikt.md` for § 10-7), les filen, svar deretter.

**Når brukeren ber om å se/vise lovteksten eller forskriftsteksten:** gjengi kildefilen ordrett og i sin helhet – inkludert bokstavpunkter, underoverskrifter og leddnummerering slik de står i kildefilen. Ikke sammenfatt, omformuler eller utelat strukturelementer med mindre brukeren eksplisitt ber om et sammendrag.

## Hva som finnes av kilder

- **Lovtekst** (`folketrygdloven/lov/`): full, uavkortet paragraftekst hentet fra Lovdatas åpne API (NLOD 2.0), oppdatert automatisk gjennom den ukentlige regelverkssjekken. Flat struktur - én fil per paragraf (`par-10-5.md` osv.), pluss `oversikt.md` og `temaoppslag.md`. Lovtekst er det eneste som skal siteres som gjeldende rett.
- **Rundskriv til kapittel 10** (`folketrygdloven/rundskriv/ftrl/kap-10/`): NAVs kommentarer, hentet fra R10-00 (28.08.2026 - manuelt hentet, oppdateres ikke automatisk), pluss `generell-del.md`. Dekker § 10-1, 10-1 a, 10-3, 10-5, 10-6 og 10-8. § 10-4 (Alder) har ingen egen kommentarseksjon i R10-00 - ikke nødvendigvis et hull, kan bety at NAV ikke har funnet behov for å kommentere denne paragrafen særskilt.
- **§ 10-7 (stønadsformer)** har en helt egen kildestruktur, se `folketrygdloven/rundskriv/ftrl/kap-10/paragraf-10-7/oversikt.md` FØRST - ikke gjett ut fra filnavn. NAV har ikke ett samlet rundskriv til § 10-7, men ett dokument per bokstav/stønadsform, pluss noen dokumenter som gjelder § 10-7 mer generelt (reiseutgifter, fjerde/femte ledd, en bredere eldre kommentar til bokstav a/c/d):
  - Generelle (ikke bokstav-spesifikke) dokumenter ligger under `folketrygdloven/rundskriv/ftrl/kap-10/paragraf-10-7/`.
  - Bokstav-/stønadsformspesifikke dokumenter ligger under `folketrygdloven/rundskriv/forskrifter/<slug>/`, siden de kommenterer en navngitt egen forskrift: `aktivitetshjelpemidler-over-26/` (bokstav a), `horeapparat-tinnitusmaskerer/` (bokstav b), `tolkehjelp-horselshemmede/` (bokstav f), `tolke-ledsagerhjelp-dovblinde/` (bokstav g), `anskaffelse-motorkjoretoy/` (bokstav h), `ortopediske-hjelpemidler-proteser-parykk/` (bokstav i), `lese-sekretarhjelp-blinde-svaksynte/` (bokstav e), `servicehund/` (egen ordning, ikke en bokstav i første ledd).
  - Flere er delt i underfiler pga. lengde (samme `par-<paragraf>-00-oversikt.md`-mønster som ellers, der det gjelder en navngitt paragraf).
  - **Merk:** § 10-7 a (stønad til briller til barn) er en egen paragraf, ikke en bokstav i § 10-7 første ledd, og har ingen kommentarseksjon i noen av kildene som er gjennomgått - bruk lovtekst for denne.
  - Selve forskriftstekstene til disse stønadsformene er ikke lagt inn - kun NAVs kommentarer til dem. Si eksplisitt fra at forskriftsteksten ikke er sjekket direkte når disse kildene brukes.

**Kryssreferanser utenfor denne skillen.** Når en paragraf henviser til et annet kapittel, gjengi henvisningen som den står i loven, men ikke gjett på innholdet. Si eksplisitt fra at kryssreferansen ikke er sjekket. For kap. 6, 8, 9, 11/11 A og 12 finnes egne skills (`folketrygdloven/merknader/grunnstonad.md`, `folketrygdloven/merknader/sykepenger.md`, `folketrygdloven/merknader/aap.md`, `folketrygdloven/merknader/uforetrygd.md`) - nevn hvilken hvis relevant. Andre kapitler (1-5, 7, 13, 14, 21, 22 m.fl.) er ikke dekket av noen av disse skillene ennå.

## Oppslagslogikk

**1. Direkte paragrafhenvisning.** Gjenkjenn alle vanlige skrivemåter: "§ 10-5", "ftrl § 10-7", "paragraf 10-1 a". Match mot filnavn `folketrygdloven/lov/par-10-<paragrafnummer><evt. bokstav>.md`, f.eks. § 10-1 a → `par-10-1a.md`. Les filen direkte og bruk lovteksten.

**Når noen ber om å "vise" en paragraf, skal svaret være selve lovteksten - ordrett, alle ledd, ikke en oppsummering.** Oppsummering leveres bare når det eksplisitt er bedt om, eller når paragrafen inngår som ledd i en drøftelse av noe annet. Hvis noen ber om å "vise rundskrivet til" en paragraf, er det rundskrivfilen(e) som skal vises/brukes. § 10-4 og § 10-7 a har ingen kommentarseksjon i det som er gjennomgått - bruk lovtekst for disse. For § 10-7 spesifikt: se `folketrygdloven/rundskriv/ftrl/kap-10/paragraf-10-7/oversikt.md` først for å finne riktig dokument.

**2. Temaoppslag.** Bruk `folketrygdloven/merknader/temaoppslag-hjelpemidler.md` for å finne riktig paragraf ut fra tema.

**3. Henvisningskjeder - avgjørende for negative konklusjoner.** Før en konklusjon av typen «X har ikke...», «det finnes ingen mekanisme for...» trekkes, skal **alle** paragrafer/ledd i henvisningskjeden som ligger innenfor kap. 10 være lest - ikke bare den første som bekrefter hypotesen. Hvis kjeden går til et kapittel utenfor kap. 10, stopp der og flagg det.

**4. Substansielle tolkningsspørsmål (hva betyr/hvordan praktiseres § X).** Les både lovtekst og rundskriv - lovteksten gir normen, rundskrivet gir NAVs praktisering. Hvis paragrafen har delt rundskrivfil, les oversiktsfilen først. For § 10-4 og § 10-7 a finnes ingen rundskrivkommentar i det som er gjennomgått - bruk lovtekst. For § 10-7: bruk `folketrygdloven/rundskriv/ftrl/kap-10/paragraf-10-7/oversikt.md` til å finne riktig dokument for den aktuelle bokstaven/stønadsformen.

## Format på lovtekstfilene

Hver fil har en overskrift, en `**Kilde:**`-linje, deretter lovteksten med ledd som egne `**N. ledd**`-overskrifter (1., 2., 3. …). Bokstavlister (a, b, c …) er underpunkter i det ledd de hører til, ikke egne ledd. Endringshistorikk står som løpende tekst nederst i filen under `**Endringshistorikk:**` - metadata, ikke gjeldende rett i seg selv.

## Fremtidig utvidelse (ikke igangsatt)

- Rundskriv til § 10-4 og § 10-7 a - ingen kjent NAV-kilde funnet for disse.
- Selve forskriftsteksten for §10-7-forskriftene - ikke lagt inn ennå, kun NAVs kommentarer.
- Forarbeider (proposisjoner, høringsnotater).
- Rettspraksis - lavere prioritert enn forarbeider, siden rundskrivene allerede refererer relevant rettspraksis der det trengs.
- Fellesbestemmelser (kap. 1, 2, 21, 22 m.fl.) - vurderes når behovet er tydeligere.
