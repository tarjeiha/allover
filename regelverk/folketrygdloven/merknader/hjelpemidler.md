> **Flyttet fra skillen `aid-ftrl-hjelpemidler`** 16.10.2026 og ryddet 18.10.2026. Merknaden er hjelp til å finne fram og unngå vanlige feil, ikke lov- eller forskriftstekst. Kildereglene i CLAUDE.md gjelder foran det som står her.

# Oppslag i folketrygdloven - hjelpemidler

Merknaden gjelder kapittel 10 i folketrygdloven. Andre ytelser har egne merknader, se tabellen i `regelverk/folketrygdloven/VEIVISER.md`.

Identifiser riktig paragraf eller stønadsform først (se `regelverk/folketrygdloven/rundskriv/ftrl/kap-10/paragraf-10-7/oversikt.md` for § 10-7), les filen, og svar deretter. Det gjelder også når spørsmålet er uspesifikt formulert.

## Hva som finnes av kilder

- **Lovtekst** (`regelverk/folketrygdloven/lov/`): full, uavkortet paragraftekst bygget fra Lovdatas åpne API (NLOD 2.0). Flat struktur - én fil per paragraf (`par-10-5.md` osv.). Paragraflisten står i `regelverk/folketrygdloven/VEIVISER.md`. Lovtekst er det eneste som skal siteres som gjeldende rett.
- **Rundskriv til kapittel 10** (`regelverk/folketrygdloven/rundskriv/ftrl/kap-10/`): NAVs kommentarer, hentet fra R10-00 (28.08.2026 - manuelt hentet, oppdateres ikke automatisk), pluss `generell-del.md`. Dekker § 10-1, 10-1 a, 10-3, 10-5, 10-6 og 10-8. § 10-4 (Alder) har ingen egen kommentarseksjon i R10-00 - ikke nødvendigvis et hull, kan bety at NAV ikke har funnet behov for å kommentere denne paragrafen særskilt.
- **§ 10-7 (stønadsformer)** har en helt egen kildestruktur, se `regelverk/folketrygdloven/rundskriv/ftrl/kap-10/paragraf-10-7/oversikt.md` FØRST - ikke gjett ut fra filnavn. NAV har ikke ett samlet rundskriv til § 10-7, men ett dokument per bokstav/stønadsform, pluss noen dokumenter som gjelder § 10-7 mer generelt (reiseutgifter, fjerde/femte ledd, en bredere eldre kommentar til bokstav a/c/d):
  - Generelle (ikke bokstav-spesifikke) dokumenter ligger under `regelverk/folketrygdloven/rundskriv/ftrl/kap-10/paragraf-10-7/`.
  - Bokstav-/stønadsformspesifikke dokumenter ligger under `regelverk/folketrygdloven/rundskriv/forskrifter/<slug>/`, siden de kommenterer en navngitt egen forskrift: `aktivitetshjelpemidler-over-26/` (bokstav a), `horeapparat-tinnitusmaskerer/` (bokstav b), `tolkehjelp-horselshemmede/` (bokstav f), `tolke-ledsagerhjelp-dovblinde/` (bokstav g), `anskaffelse-motorkjoretoy/` (bokstav h), `ortopediske-hjelpemidler-proteser-parykk/` (bokstav i), `lese-sekretarhjelp-blinde-svaksynte/` (bokstav e), `servicehund/` (egen ordning, ikke en bokstav i første ledd).
  - Flere er delt i underfiler pga. lengde (samme `par-<paragraf>-00-oversikt.md`-mønster som ellers, der det gjelder en navngitt paragraf).
  - **Merk:** § 10-7 a (stønad til briller til barn) er en egen paragraf, ikke en bokstav i § 10-7 første ledd, og har ingen kommentarseksjon i noen av kildene som er gjennomgått - bruk lovtekst for denne.
  - Selve forskriftstekstene til disse stønadsformene er ikke lagt inn - kun NAVs kommentarer til dem. Si eksplisitt fra at forskriftsteksten ikke er sjekket direkte når disse kildene brukes.

**Kryssreferanser til andre kapitler.** Hele folketrygdloven ligger i basen. Når en paragraf henviser til et annet kapittel, les den paragrafen også. Merknad og rundskriv for det kapitlet finner du i tabellen i `regelverk/folketrygdloven/VEIVISER.md`. Grunnstønad og hjelpestønad (kap. 6), sykepenger og pleiepenger (kap. 8 og 9), AAP og tilleggsstønader (kap. 11 og 11 A) og uføretrygd (kap. 12) henger ofte sammen med hjelpemidler.

## Oppslagslogikk

**1. Direkte paragrafhenvisning.** Gjenkjenn alle vanlige skrivemåter: "§ 10-5", "ftrl § 10-7", "paragraf 10-1 a". Match mot filnavn `regelverk/folketrygdloven/lov/par-10-<paragrafnummer><evt. bokstav>.md`, f.eks. § 10-1 a → `par-10-1a.md`. Les filen direkte og bruk lovteksten. Ber noen om å «vise rundskrivet til» en paragraf, er det rundskrivfilen(e) som skal vises. § 10-4 og § 10-7 a har ingen kommentarseksjon i det som er gjennomgått - bruk lovtekst for disse. For § 10-7 spesifikt: se `regelverk/folketrygdloven/rundskriv/ftrl/kap-10/paragraf-10-7/oversikt.md` først for å finne riktig dokument.

**2. Temaoppslag.** Bruk `regelverk/folketrygdloven/merknader/temaoppslag-hjelpemidler.md` for å finne riktig paragraf ut fra tema.

**3. Henvisningskjeder - avgjørende for negative konklusjoner.** Før en konklusjon av typen «X har ikke...», «det finnes ingen mekanisme for...» trekkes, skal **alle** paragrafer og ledd i henvisningskjeden være lest - ikke bare den første som bekrefter hypotesen. Går kjeden til et annet kapittel, følg den dit.

**4. Substansielle tolkningsspørsmål (hva betyr/hvordan praktiseres § X).** Les både lovtekst og rundskriv - lovteksten gir normen, rundskrivet gir NAVs praktisering. Hvis paragrafen har delt rundskrivfil, les oversiktsfilen først. For § 10-4 og § 10-7 a finnes ingen rundskrivkommentar i det som er gjennomgått - bruk lovtekst. For § 10-7: bruk `regelverk/folketrygdloven/rundskriv/ftrl/kap-10/paragraf-10-7/oversikt.md` til å finne riktig dokument for den aktuelle bokstaven/stønadsformen.

## Format på lovtekstfilene

Hver fil har en overskrift, en `**Kilde:**`-linje, deretter lovteksten med ledd som egne `**N. ledd**`-overskrifter (1., 2., 3. …). Bokstavlister (a, b, c …) er underpunkter i det ledd de hører til, ikke egne ledd. Endringshistorikk står som løpende tekst nederst i filen under `**Endringshistorikk:**` - metadata, ikke gjeldende rett i seg selv.

## Ikke i basen

- Rundskriv til § 10-4 og § 10-7 a - ingen kjent NAV-kilde funnet for disse.
- Selve forskriftsteksten for § 10-7-forskriftene - kun NAVs kommentarer er lagt inn.
- Forarbeider (proposisjoner, høringsnotater).
- Rettspraksis. Rundskrivene refererer relevant rettspraksis der det trengs.
