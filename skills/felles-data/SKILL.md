---
name: "felles-data"
description: "Felles datakatalog for norsk statistikk og tall - SSB, Nav (sykefravær, dagpenger, AAP, uføretrygd, alderspensjon, helt ledige), Eurostat (sammenligning mellom Norge, Norden, Tyskland og EU) og OECD (arbeidsmarkedspolitikk, ytelsesnivå, pensjon, stillingsvern og skatt sammenlignet med andre land, også USA og Storbritannia). Bruk ved alle spørsmål om tall, statistikk, utvikling over tid eller sammenligning mellom land, også uten fagord, f.eks. «hvor mange er sykmeldt», «hvordan går det med ledigheten», «er Norge høyere enn Sverige». Last den før du henter tall, også når du skal bruke SSB-tilkoblingen. Også når brukeren spør hva basen inneholder, eller har funnet feil eller mangler. Svar ikke fra hukommelsen."
---

# Datakatalogen

**Versjon 2026-10-22.** Hent også `https://raw.githubusercontent.com/tarjeiha/allover/main/SKILLVERSJONER.md`. Står det en nyere versjon for denne skillen der, si én gang, til slutt i svaret: «Det finnes nyere versjoner av de felles skillene. Si "oppdater skillene" for å få dem.» Står det et driftsvarsel der for et område svaret bygger på, si kort til brukeren at det nyeste fra kilden kan mangle. Feiler hentingen, la det være.

Selve tallene ligger ikke i denne skillen. Katalogen over hvilken kilde og tabell som svarer på hva ligger i et felles repo på GitHub og hentes ved hvert oppslag. Tallene hentes fra kilden.

## Fremgangsmåte

1. Hent `https://raw.githubusercontent.com/tarjeiha/allover/main/data/VEIVISER.md` med `curl -sL` i kodeverktøyet, eller med hentverktøyet ditt. Følg den, inkludert svarreglene (kort svar først, kvalitetssikringsversjon på forespørsel).
2. Er spørsmålet stilt i hverdagsspråk, start med `data/sporsmal.md`.
3. Finn kilden i tabellen i veiviseren og åpne kildefilen.
   - **Nav, Eurostat og OECD:** tallene ligger som TSV-filer i basen. Les filene som katalogen peker til.
   - **SSB:** hent tallene med SSB-tilkoblingen (`ssb_search`, `ssb_table_metadata`, `ssb_get_data`). Les `data/ssb-bruk.md` for arbeidsmåte og filtersyntaks før du kaller verktøyene. Skillen `ssb-api` trengs ikke når du følger denne.
   - **Diagram:** er brukeren ute etter et diagram, bruk skillen `ssb-dataviz`.
4. Er kilden ikke dekket i katalogen, si det tydelig og ikke gi et selvsikkert svar uten kilde.
5. **Spør brukeren hva basen inneholder, eller har brukeren funnet en feil eller noe som mangler,** hent `https://raw.githubusercontent.com/tarjeiha/allover/main/OM-BASENE.md` og følg den. Meldinger om feil, mangler og ønsker går på e-post til redaktøren for basene, Tarjei Havnes. Adressen står i skillen `felles-intern`.
6. Hvis hentingen feiler: se «Hvis hentingen feiler» under.

## Hvis hentingen feiler

Svar ikke fra hukommelsen. Ser feilen ut som en sperre (for eksempel 403, «not allowed», «blocked» eller nektet tilkobling), si dette, med nettstedet fra adressen som feilet:

«Jeg fikk ikke hentet datakatalogen, fordi Claude ikke har lov til å hente fra nettstedet [nettsted]. Du kan åpne for det selv: Gå til Innstillinger → Funksjoner. Under «Kodekjøring og filoppretting i skyen» skroller du ned til «Tillatelsesliste for domener» og legger til [nettsted]. Spør meg igjen etterpå, gjerne i en ny samtale. Har du Claude på engelsk, si fra, så får du navnene på engelsk.»

Ber brukeren om engelske navn, eller skriver brukeren på engelsk, bruk Settings → Capabilities, «Code execution and file creation» og listen over tillatte domener lenger ned på siden. Nettstedsnavnet er det eneste tekniske ordet som skal stå i svaret.

Ved andre feil: «Jeg fikk ikke hentet datakatalogen nå. Prøv igjen litt senere.»
