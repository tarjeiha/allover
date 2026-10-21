---
name: "felles-regelverk"
description: "Felles regelverksbase for norsk lov og forskrift. Bruk ved spørsmål om hva norsk lov eller forskrift sier (f.eks. arbeidsmiljøloven, folketrygdloven, offentleglova, forvaltningsloven), hovedtariffavtalen i staten og EU-rettsakter - paragrafer, hjemmel, vilkår, rettigheter, unntak, eller om noe er lovlig eller påkrevd etter regelverket - også når spørsmålet stilles uten fagord. Dekker også Stortinget: anmodningsvedtak («har Stortinget bedt regjeringen om»), skriftlige spørsmål, interpellasjoner og spørretimespørsmål, representantforslag og utfallet av dem («har parti X foreslått Y», «hva skjedde med forslaget om Z»), for sesjon 2013-2014 og framover. Skillen sjekker selv hva som er dekket. Last den før du svarer på slike spørsmål, og svar ikke fra hukommelsen. Også når brukeren spør hva basen inneholder, eller har funnet feil eller mangler."
---

# Regelverksbasen

**Versjon 2026-10-21.** Hent også `https://raw.githubusercontent.com/tarjeiha/allover/main/SKILLVERSJONER.md`. Står det en nyere versjon for denne skillen der, si én gang, til slutt i svaret: «Det finnes nyere versjoner av de felles skillene. Si "oppdater skillene" for å få dem.» Står det et driftsvarsel der for et område svaret bygger på, si kort til brukeren at det nyeste fra kilden kan mangle. Feiler hentingen, la det være.

Lov- og forskriftsteksten ligger ikke i denne skillen. Den ligger i et felles repo på GitHub og hentes ved hvert oppslag, så den alltid er oppdatert. Hva basen dekker, står i basen.

## Fremgangsmåte

1. Hent `https://raw.githubusercontent.com/tarjeiha/allover/main/CLAUDE.md` med `curl -sL` i kodeverktøyet, eller med hentverktøyet ditt. Følg den.
2. Sjekk tabellen over regelverk i CLAUDE.md mot spørsmålet.
   - **Dekket:** åpne veiviseren og paragrafene, og svar med kilde.
   - **Ikke dekket:** følg regelen i CLAUDE.md for regelverk som ikke er dekket.
3. **Spør brukeren hva basen inneholder, eller har brukeren funnet en feil eller noe som mangler,** hent `https://raw.githubusercontent.com/tarjeiha/allover/main/OM-BASENE.md` og følg den. Meldinger om feil, mangler og ønsker går på e-post til redaktøren for basene, Tarjei Havnes. Adressen står i skillen `felles-intern`.
4. Hvis hentingen feiler: si det til brukeren med kort feilmelding, og svar ikke fra hukommelsen.
