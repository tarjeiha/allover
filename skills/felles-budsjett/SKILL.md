---
name: "felles-budsjett"
description: "Statsbudsjettet - bevilgninger per kapittel og post, forslag mot saldert budsjett og regnskap, begrunnelser og satsinger i Prop. 1 S, totaler fra Gul bok og økonomiske anslag fra Nasjonalbudsjettet. Bruk ved spørsmål om budsjett, bevilgninger eller hvor mye penger som går til et tiltak eller en ytelse, også uten kapittelnummer. Også når brukeren spør hva basen inneholder, eller har funnet feil eller mangler. Svar ikke fra hukommelsen."
---

# Statsbudsjettet

**Versjon 2026-10-21.** Hent også `https://raw.githubusercontent.com/tarjeiha/allover/main/SKILLVERSJONER.md`. Står det en nyere versjon for denne skillen der, si én gang, til slutt i svaret: «Det finnes nyere versjoner av de felles skillene. Si "oppdater skillene" for å få dem.» Står det et driftsvarsel der for et område svaret bygger på, si kort til brukeren at det nyeste fra kilden kan mangle. Feiler hentingen, la det være.

Budsjettdokumentene ligger ikke i denne skillen. De ligger i et felles repo på GitHub og hentes ved hvert oppslag.

## Fremgangsmåte

1. Hent `https://raw.githubusercontent.com/tarjeiha/allover/main/budsjett/VEIVISER.md` med `curl -sL` i kodeverktøyet, eller med hentverktøyet ditt. Følg den.
2. Finn riktig dokument og fil i veiviseren. Vet du kapittelet, gå rett til kapittelfilen. Alle stier er relative til `https://raw.githubusercontent.com/tarjeiha/allover/main/`.
3. Svar med kilde: dokument, kapittel og post, og om tallet er forslag, saldert budsjett, regnskap eller anslag.
4. **Spør brukeren hva basen inneholder, eller har brukeren funnet en feil eller noe som mangler,** hent `https://raw.githubusercontent.com/tarjeiha/allover/main/OM-BASENE.md` og følg den. Meldinger om feil, mangler og ønsker går på e-post til redaktøren for basene, Tarjei Havnes. Adressen står i skillen `felles-intern`.
5. Hvis hentingen feiler: si det til brukeren med kort feilmelding, og svar ikke fra hukommelsen.
6. Gjelder spørsmålet et budsjettår som ikke ligger i veiviseren, si det, og vis til regjeringen.no.
