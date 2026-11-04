# Innboks for rundskriv

Legg rundskriv her, så legges de inn i basen automatisk i løpet av et par minutter.

## Slik gjør du

1. Åpne mappen `innboks` på GitHub, og velg **Add file → Upload files**.
2. Dra inn filen. PDF, Word (.docx), ODT, HTML, Markdown og ren tekst virker. En nettside kan lagres som HTML (i nettleseren: Lagre som → «Nettside, bare HTML»). Menyer, topp- og bunntekst tas bort.
3. Velg **Commit directly to the main branch**, og trykk **Commit changes**.

Du trenger ikke velge lov. Jobben finner loven ut fra teksten.

## Hva som skjer

- **Loven** velges ut fra hvilken lov i basen teksten viser tydeligst til. NAV-rundskriv med nummer som R08-00 hører til folketrygdloven. Vil du bestemme selv, la filnavnet starte med lovmappen, for eksempel `arbeidsmiljoloven-rundskriv-om-innleie.pdf`.
- **Forskrifter:** Står navnet på en forskrift som ligger i basen, i tittelen på rundskrivet (som i Navs «Utfyllende regler - Forskrift om tilskudd til ekspertbistand»), er det et rundskriv til forskriften. Det legges da sammen med de andre kommentarene til forskrifter under loven. Paragrafnumrene gjelder forskriften, ikke loven.
- **Paragrafer:** Har rundskrivet overskrifter som «Til § 8-4», «§ 8-4. Tittel» eller «Forskrift om X § 3 skal forstås slik», deles det i én fil per paragraf. Ellers blir det én fil. En innholdsfortegnelse fra Word tas bort.
- **Tittel:** Er filen lastet ned fra Lovdata, brukes «Sammendrag» øverst som tittel, med dokumentnummeret.
- **Resultatet** havner i `regelverk/<lov>/rundskriv/<filnavn>/`, eller i `regelverk/<lov>/rundskriv/forskrifter/<forskrift>/` for rundskriv til en forskrift, med en `oversikt.md` og originalfilen i `original/`. Rundskrivet kan søkes opp i `indeks.tsv` med en gang. Veiviseren for loven viser det fra neste nattlige bygg.
- **Ny versjon:** Legg inn en fil med samme navn, så erstattes den gamle teksten. For rundskriv til en forskrift erstattes teksten uansett filnavn.

## Når noe stopper

Jobben legger ikke inn noe den er usikker på. Filen blir da liggende her, og en fil med samme navn og `.FEIL.txt` til slutt forklarer hvorfor. Vanlige grunner:

- Teksten viser ikke tydelig til en lov som finnes i basen. Gi filen et navn som starter med lovmappen, eller legg loven inn i basen først.
- Teksten viser til flere lover omtrent like mye. Gi filen et navn som starter med lovmappen.
- Filen er en skannet PDF uten tekstlag.
- Filen er ikke et rundskriv, men en EU-rettsakt (forordning, direktiv). EU-rettsakter legges inn ved å føye dem til under `eu` i `regelverk.json`, så hentes de fra EUR-Lex.

Rett opp og last opp filen på nytt. `.FEIL.txt`-filen forsvinner når filen er lagt inn.

## Hovedtariffavtalen

Hovedtariffavtalen i staten legges også inn her. Last ned Word-filen fra regjeringen.no og last den opp med et filnavn som begynner på `hovedtariffavtale`, for eksempel `hovedtariffavtale_2026-2028.docx`. Den deles da opp i `regelverk/hovedtariffavtalen/`, perioden hentes fra forsiden og skrives i `regelverk.json`, og Word-filen slettes etterpå. Gjør det ved hvert hovedoppgjør og mellomoppgjør. Bygget åpner en sak i GitHub når det er tid for å se etter ny utgave.
