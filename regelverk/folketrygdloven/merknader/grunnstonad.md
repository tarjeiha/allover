> **Flyttet fra skillen `aid-ftrl-grunnstonad`** 16.10.2026 og ryddet 18.10.2026. Merknaden er hjelp til å finne fram og unngå vanlige feil, ikke lov- eller forskriftstekst. Kildereglene i CLAUDE.md gjelder foran det som står her.

# Oppslag i folketrygdloven - grunnstønad og hjelpestønad

Merknaden gjelder kapittel 6 i folketrygdloven. Andre ytelser har egne merknader, se tabellen i `regelverk/folketrygdloven/VEIVISER.md`.

Identifiser riktig paragraf eller diagnose først, les filen, og svar deretter. Det gjelder også når spørsmålet er uspesifikt formulert.

## Hva som finnes av kilder

- **Lovtekst** (`regelverk/folketrygdloven/lov/`): full, uavkortet paragraftekst bygget fra Lovdatas åpne API (NLOD 2.0). Flat struktur - én fil per paragraf (`par-6-3.md` osv.). Paragraflisten står i `regelverk/folketrygdloven/VEIVISER.md`. Full dekning - alle ti paragrafer (§ 6-1 til § 6-9, inkl. § 6-1 a). Lovtekst er det eneste som skal siteres som gjeldende rett.
- **Rundskriv til kapittel 6** (`regelverk/folketrygdloven/rundskriv/ftrl/kap-6/`): NAVs kommentarer til hver paragraf, hentet fra R06-00 (28.08.2026 - manuelt hentet, oppdateres ikke automatisk), pluss `generell-del.md`. Full dekning. Dette er NAVs praktisering og tolkning av loven - **ikke** loven selv. Svar som bruker rundskriv skal eksplisitt markere kilden som forvaltningspraksis, atskilt fra det som er sitert fra selve lovteksten.
  - **Filstruktur for lange kommentarer:** `par-<paragraf>-00-oversikt.md` lister underseksjonene der kommentaren er delt opp. Les oversiktsfilen først.
- **Diagnosebaserte retningslinjer** (`regelverk/folketrygdloven/rundskriv/ftrl/kap-6/retningslinjer-diagnoser/`): NAVs retningslinjer for hjelpestønad/forhøyet hjelpestønad ved ti navngitte diagnoser (astma, blødersykdommer, cystisk fibrose, diabetes, Downs syndrom, døvhet/sterk tunghørthet, fenylketonuri, hofteleddsdysplasi, kreft hos barn, psykisk utviklingshemming), hentet fra R06-04-FOR (28.08.2026). Organisert per diagnose, ikke per paragraf - gjelder § 6-4 og § 6-5 samlet. Les `oversikt.md` for å finne riktig fil. Supplerer, erstatter ikke, hovedrundskrivets kommentarer til § 6-4/§ 6-5.

**Kryssreferanser til andre kapitler.** Hele folketrygdloven ligger i basen. Når en paragraf henviser til et annet kapittel, les den paragrafen også. Merknad og rundskriv for det kapitlet finner du i tabellen i `regelverk/folketrygdloven/VEIVISER.md`. Hjelpemidler (kap. 10), sykepenger og pleiepenger (kap. 8 og 9), AAP (kap. 11 og 11 A) og uføretrygd (kap. 12) henger ofte sammen med grunnstønad og hjelpestønad.

## Oppslagslogikk

**1. Direkte paragrafhenvisning.** Gjenkjenn alle vanlige skrivemåter: "§ 6-3", "ftrl § 6-4", "paragraf 6-1 a". Match mot filnavn `regelverk/folketrygdloven/lov/par-6-<paragrafnummer><evt. bokstav>.md`, f.eks. § 6-1 a → `par-6-1a.md`. Les filen direkte og bruk lovteksten. Ber noen om å «vise rundskrivet til» en paragraf, er det rundskrivfilen(e) som skal vises.

**2. Temaoppslag.** Bruk `regelverk/folketrygdloven/merknader/temaoppslag-grunnstonad.md` for å finne riktig paragraf ut fra tema.

**3. Henvisningskjeder - avgjørende for negative konklusjoner.** Før en konklusjon av typen «X har ikke...», «det finnes ingen mekanisme for...» trekkes, skal **alle** paragrafer og ledd i henvisningskjeden være lest - ikke bare den første som bekrefter hypotesen. Går kjeden til et annet kapittel, følg den dit.

**4. Substansielle tolkningsspørsmål (hva betyr/hvordan praktiseres § X).** Les både lovtekst og rundskriv - lovteksten gir normen, rundskrivet gir NAVs praktisering. Hvis paragrafen har delt rundskrivfil, les oversiktsfilen først. For § 6-4/§ 6-5 ved en navngitt diagnose: sjekk også `regelverk/folketrygdloven/rundskriv/ftrl/kap-6/retningslinjer-diagnoser/oversikt.md`. Hold kildene atskilt i svaret.

## Format på lovtekstfilene

Hver fil har en overskrift, en `**Kilde:**`-linje, deretter lovteksten med ledd som egne `**N. ledd**`-overskrifter (1., 2., 3. …). Bokstavlister (a, b, c …) er underpunkter i det ledd de hører til, ikke egne ledd. Endringshistorikk står som løpende tekst nederst i filen under `**Endringshistorikk:**` - metadata, ikke gjeldende rett i seg selv.

## Ikke i basen

- Forarbeider (proposisjoner, høringsnotater).
- Rettspraksis. Rundskrivene refererer relevant rettspraksis der det trengs.
