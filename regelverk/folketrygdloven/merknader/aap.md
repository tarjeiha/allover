> **Flyttet fra skillen `aid-ftrl-aap`** 16.10.2026 og ryddet 18.10.2026. Merknaden er hjelp til å finne fram og unngå vanlige feil, ikke lov- eller forskriftstekst. Kildereglene i CLAUDE.md gjelder foran det som står her.

# Oppslag i folketrygdloven - arbeidsavklaringspenger

Merknaden gjelder kapittel 11 og 11 A i folketrygdloven. Andre ytelser har egne merknader, se tabellen i `regelverk/folketrygdloven/VEIVISER.md`.

## Hvilket kapittel gjelder spørsmålet?

| Tema | Kapittel |
|---|---|
| Arbeidsavklaringspenger (AAP) | 11 |
| Tilleggsstønader til arbeidsrettede tiltak (AAP-tiltak) | 11 A |

Kapittel 11 A henger innholdsmessig tett sammen med kapittel 11, men er et eget kapittel med egen mappe og egne kilder - ikke anta at dekning eller kommentarer til det ene sier noe om det andre. Ikke forveksle § 11 A-4 med § 11-4 - ulike paragrafer i ulike kapitler.

Når kapittel er identifisert (eller gitt direkte via paragrafnummer), les `regelverk/folketrygdloven/merknader/temaoppslag-aap.md` for detaljert paragrafoversikt for kapittel 11 (kapittel 11 A har ingen egen temaoppslagstabell ennå - se lovtekst direkte).

## Hva som finnes av kilder

- **Lovtekst** (`regelverk/folketrygdloven/lov/`): full, uavkortet paragraftekst for både kap. 11 og kap. 11 A, bygget fra Lovdatas åpne API (NLOD 2.0). Flat struktur - én fil per paragraf (`par-11-5.md`, `par-11a-4.md` osv.). Paragraflisten står i `regelverk/folketrygdloven/VEIVISER.md`. Lovtekst er det eneste som skal siteres som gjeldende rett.
- **Forskriftstekst** (`regelverk/folketrygdloven/forskrifter/eos-beregning-arbeidsavklaringspenger/`): full forskriftstekst, FOR-2017-12-13-2099, §1-§6 (§ 5 opphevet), én fil per paragraf (`par-1.md` osv.). Relevant for § 11-19 (grunnlag for beregning av arbeidsavklaringspenger ved arbeidsperioder i andre EØS-land). Ingen tilhørende rundskrivkommentar er lagt inn for denne forskriften, og NAVs EØS-rundskriv R45-00 er ikke i basen.
- **Rundskriv til kapittel 11** (`regelverk/folketrygdloven/rundskriv/ftrl/kap-11/`): NAVs kommentarer, hentet fra R11-00 (28.08.2026 - manuelt hentet, oppdateres ikke automatisk), pluss `generell-del.md` og `overgangsregler.md`. Full dekning - alle 33 gjeldende og opphevede paragrafer har kommentar. `overgangsregler.md` gjelder overgangsreglene ved lovendringen fra 1.1.2018, ikke én bestemt paragraf.
  - **Filstruktur for lange kommentarer:** `par-<paragraf>-00-oversikt.md` lister underseksjonene, `par-<paragraf>-01-...md` osv. inneholder selve innholdet. Les oversiktsfilen først.
- **Rundskriv til kapittel 11 A** (`regelverk/folketrygdloven/rundskriv/ftrl/kap-11a/`): NAVs kommentarer til hver paragraf (`par-11a-1.md` osv.), hentet fra R11A-00 (28.08.2026). Egen kilde, atskilt fra rundskriv til kapittel 11. § 11 A-1 a har ingen egen kommentarseksjon - bruk lovtekst for denne.
- **Rundskriv til forskrift** (`regelverk/folketrygdloven/rundskriv/forskrifter/tilleggsstonadsforskriften/`): NAVs kommentarer til tilleggsstønadsforskriften (FOR-2015-07-02-867), relevant for § 11 A-4. Nøkket på forskriftens egen paragrafnummerering (§1-§16), ikke ftrl sin. `overgangsregler.md` gjelder ikke én bestemt paragraf. Selve forskriftsteksten er ikke lagt inn - kun NAVs kommentarer. Si eksplisitt fra at forskriftsteksten ikke er sjekket direkte når denne kilden brukes.

**Kryssreferanser til andre kapitler.** Hele folketrygdloven ligger i basen. Når en paragraf henviser til et annet kapittel, les den paragrafen også. Merknad og rundskriv for det kapitlet finner du i tabellen i `regelverk/folketrygdloven/VEIVISER.md`. Sykepenger (kap. 8 og 9), uføretrygd (kap. 12), grunnstønad og hjelpestønad (kap. 6) og hjelpemidler (kap. 10) henger ofte sammen med AAP.

## Oppslagslogikk

**1. Direkte paragrafhenvisning.** Gjenkjenn alle vanlige skrivemåter: "§ 11-5", "ftrl § 11 A-4", "paragraf 11-12 a". Match mot filnavn `regelverk/folketrygdloven/lov/par-<kapittel>-<paragrafnummer><evt. bokstav>.md`, f.eks. § 11-12 a → `par-11-12a.md`, § 11 A-4 → `par-11a-4.md` (merk: kapittelnummer skrives med liten bokstav i filnavnet - `11a`, ikke `11A` eller `11 A`). Les filen direkte og bruk lovteksten. Ber noen om å «vise rundskrivet til» en paragraf, er det rundskrivfilen(e) som skal vises.

**2. Temaoppslag.** Bruk `regelverk/folketrygdloven/merknader/temaoppslag-aap.md` (kap. 11). Kapittel 11 A har ingen egen tabell - les paragrafene direkte.

**3. Henvisningskjeder - avgjørende for negative konklusjoner.** Før en konklusjon av typen «X har ikke...», «det finnes ingen mekanisme for...» trekkes, skal **alle** paragrafer og ledd i henvisningskjeden være lest - ikke bare den første som bekrefter hypotesen. Går kjeden til et annet kapittel, følg den dit.

**4. Substansielle tolkningsspørsmål (hva betyr/hvordan praktiseres § X).** Les både lovtekst og rundskriv - lovteksten gir normen, rundskrivet gir NAVs praktisering. Hvis paragrafen har delt rundskrivfil, les oversiktsfilen først. For § 11 A-4 spesifikt kan `regelverk/folketrygdloven/rundskriv/forskrifter/tilleggsstonadsforskriften/` også være relevant, siden den konkrete utmålingen ofte ligger i forskriftskommentarene. For § 11-19 kan forskriftsteksten i `regelverk/folketrygdloven/forskrifter/eos-beregning-arbeidsavklaringspenger/` også være relevant. Hold kildene atskilt i svaret.

## Format på lovtekstfilene

Hver fil har en overskrift, en `**Kilde:**`-linje, deretter lovteksten med ledd som egne `**N. ledd**`-overskrifter (1., 2., 3. …). Bokstavlister (a, b, c …) er underpunkter i det ledd de hører til, ikke egne ledd. Endringshistorikk står som løpende tekst nederst i filen under `**Endringshistorikk:**` - metadata, ikke gjeldende rett i seg selv.

## Ikke i basen

- Selve forskriftsteksten til tilleggsstønadsforskriften (FOR-2015-07-02-867) - kun NAVs kommentarer er lagt inn.
- NAVs EØS-rundskriv R45-00.
- Forarbeider (proposisjoner, høringsnotater).
- Rettspraksis. Rundskrivene refererer relevant rettspraksis der det trengs.
