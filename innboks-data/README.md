# Innboks for data

Legg Excel-filer (.xlsx) fra Nav her, så legges tallene inn i basen som TSV-filer i løpet av et par minutter. Filene blir søkbare for alle som bruker basen.

## Slik gjør du

1. Last ned xlsx-filen fra Navs statistikkside (kildesiden står i `data/nav.md`).
2. Åpne mappen `innboks-data` på GitHub, og velg **Add file → Upload files**.
3. Dra inn filen, velg **Commit directly to the main branch**, og trykk **Commit changes**. Behold filnavnet fra Nav.

Du trenger ikke velge mappe. Jobben kjenner igjen tabellene i `data/nav/kilder.json` på filnavnet (for eksempel SYFRA520 eller AAP320).

## Hva som skjer

- Hvert ark med en tabell blir en TSV-fil i `data/nav/<tabell>/`, med kilde og dato øverst. Definisjoner fra arket «Om statistikken» havner i `om.md`.
- Originalfilen legges i `data/nav/<tabell>/original/`, og `data/nav/indeks.tsv` oppdateres.
- **Sykefravær per kvartal:** Navs sykefraværstabeller har én fil per kvartal. Jobben leser kvartalet fra filen og bygger tabellen på nytt fra alle originalene, slik at alle kvartaler havner i samme fil med kolonnen `kvartal`. En ny utgave av samme kvartal erstatter den gamle.
- **Ny versjon:** Laster du opp samme tabell på nytt, erstattes den gamle.
- **Ny tabell** som jobben ikke kjenner, får mappenavn etter filen og kildeside «ukjent». Be Claude eller redaktøren føye den til i `data/nav/kilder.json`, og oppdatere `data/nav.md` med hva tabellen inneholder.

## Kontroll

Jobben sjekker at hvert tall i xlsx-filen finnes igjen i TSV-en. Stemmer det ikke, eller finner jobben ingen tabeller, legges ingenting inn. Filen blir liggende her, og en fil med samme navn og `.FEIL.txt` til slutt forklarer hvorfor. Rett opp og last opp på nytt. Feilfilen forsvinner når filen er lagt inn.

Nye Excel-filer fra andre kilder enn Nav (SSB bruker API-et og trenger ikke dette) kan ha annen oppbygning. Da kan jobben stoppe, og det er riktig oppførsel.
