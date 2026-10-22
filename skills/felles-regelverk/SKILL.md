---
name: "felles-regelverk"
description: "Felles regelverksbase for norsk lov og forskrift. Bruk ved spørsmål om hva norsk lov eller forskrift sier (f.eks. arbeidsmiljøloven, folketrygdloven, offentleglova, forvaltningsloven), hovedtariffavtalen i staten og EU-rettsakter - paragrafer, hjemmel, vilkår, rettigheter, unntak, eller om noe er lovlig eller påkrevd etter regelverket - også når spørsmålet stilles uten fagord. Dekker også Stortinget: anmodningsvedtak («har Stortinget bedt regjeringen om»), skriftlige spørsmål, interpellasjoner og spørretimespørsmål, representantforslag og utfallet av dem («har parti X foreslått Y», «hva skjedde med forslaget om Z»), for sesjon 2013-2014 og framover, og Regjeringens plan for Norge (regjeringens mål og prioriteringer). Skillen sjekker selv hva som er dekket. Last den før du svarer på slike spørsmål, og svar ikke fra hukommelsen. Også når brukeren spør hva basen inneholder, eller har funnet feil eller mangler."
---

# Regelverksbasen

**Versjon 2026-10-22.2.** Hent også `https://raw.githubusercontent.com/tarjeiha/allover/main/SKILLVERSJONER.md`. Står det en nyere versjon for denne skillen der, si én gang, til slutt i svaret: «Det finnes nyere versjoner av de felles skillene. Si "oppdater skillene" for å få dem.» Står det et driftsvarsel der for et område svaret bygger på, si kort til brukeren at det nyeste fra kilden kan mangle. Feiler hentingen, la det være.

Lov- og forskriftsteksten ligger ikke i denne skillen. Den ligger i et felles repo på GitHub og hentes ved hvert oppslag, så den alltid er oppdatert. Hva basen dekker, står i basen.

## Fremgangsmåte

1. Hent `https://raw.githubusercontent.com/tarjeiha/allover/main/CLAUDE.md` med `curl -sL` i kodeverktøyet, eller med hentverktøyet ditt. Følg den.
2. Sjekk tabellen over regelverk i CLAUDE.md mot spørsmålet.
   - **Dekket:** åpne veiviseren og paragrafene, og svar med kilde.
   - **Ikke dekket:** følg regelen i CLAUDE.md for regelverk som ikke er dekket.
3. **Spør brukeren hva basen inneholder, eller har brukeren funnet en feil eller noe som mangler,** hent `https://raw.githubusercontent.com/tarjeiha/allover/main/OM-BASENE.md` og følg den. Meldinger om feil, mangler og ønsker går på e-post til redaktøren for basene, Tarjei Havnes. Adressen står i skillen `felles-intern`.
4. Hvis hentingen feiler: se «Hvis hentingen feiler» under.

## Hvis hentingen feiler

Svar ikke fra hukommelsen. Ser feilen ut som en sperre (for eksempel 403, «not allowed», «blocked» eller nektet tilkobling), si dette, med nettstedet fra adressen som feilet:

«Jeg fikk ikke hentet lovteksten, fordi Claude ikke har lov til å hente fra nettstedet [nettsted]. Du kan åpne for det selv: Gå til Innstillinger → Funksjoner. Under «Kodekjøring og filoppretting i skyen» skroller du ned til «Tillatelsesliste for domener» og legger til [nettsted]. Spør meg igjen etterpå, gjerne i en ny samtale. Har du Claude på engelsk, si fra, så får du navnene på engelsk.»

Ber brukeren om engelske navn, eller skriver brukeren på engelsk, bruk Settings → Capabilities, «Code execution and file creation» og listen over tillatte domener lenger ned på siden. Nettstedsnavnet er det eneste tekniske ordet som skal stå i svaret.

Ved andre feil: «Jeg fikk ikke hentet lovteksten nå. Prøv igjen litt senere.»
