---
name: datakatalog
description: Felles datakatalog for norsk statistikk og tall - SSB, Nav (sykefravær, dagpenger, AAP, uføretrygd, alderspensjon, helt ledige) Eurostat (sammenligning mellom Norge, Norden, Tyskland og EU) og OECD (arbeidsmarkedspolitikk, ytelsesnivå, pensjon, stillingsvern og skatt sammenlignet med andre land, også USA og Storbritannia). Bruk ved alle spørsmål om tall, statistikk, utvikling over tid eller sammenligning mellom land, også uten fagord, f.eks. «hvor mange er sykmeldt», «hvordan går det med ledigheten», «er Norge høyere enn Sverige». Last den før du henter tall, også når du skal bruke SSB-tilkoblingen. Svar ikke fra hukommelsen.
---

# Datakatalogen

Selve tallene ligger ikke i denne skillen. Katalogen over hvilken kilde og tabell som svarer på hva ligger i et felles repo på GitHub og hentes ved hvert oppslag. Tallene hentes fra kilden.

## Fremgangsmåte

1. Hent `https://raw.githubusercontent.com/tarjeiha/allover/main/data/VEIVISER.md` med `curl -sL` i kodeverktøyet, eller med hentverktøyet ditt. Følg den, inkludert svarreglene (kort svar først, kvalitetssikringsversjon på forespørsel).
2. Er spørsmålet stilt i hverdagsspråk, start med `data/sporsmal.md`.
3. Finn kilden i tabellen i veiviseren og åpne kildefilen.
   - **Nav, Eurostat og OECD:** tallene ligger som TSV-filer i basen. Les filene som katalogen peker til.
   - **SSB:** hent tallene med SSB-tilkoblingen (`ssb_search`, `ssb_table_metadata`, `ssb_get_data`). Les `data/ssb-bruk.md` for arbeidsmåte og filtersyntaks før du kaller verktøyene. Skillen `ssb-api` trengs ikke når du følger denne.
   - **Diagram:** er brukeren ute etter et diagram, bruk skillen `ssb-dataviz`.
4. Er kilden ikke dekket i katalogen, si det tydelig og ikke gi et selvsikkert svar uten kilde.
5. Hvis hentingen feiler: si det til brukeren med kort feilmelding, og svar ikke fra hukommelsen.
