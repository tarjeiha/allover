---
name: "felles-skillbygger"
description: "Companion-skill til skill-creator for de felles skillene i departementet. Trigges ALLTID SAMMEN MED skill-creator, aldri alene og aldri i stedet for den, når noen skal lage, endre, teste eller forbedre descriptionen til en felles skill eller en egen skill på jobb. Brukes også når noen vurderer om noe bør bli en ny skill eller legges i de felles basene på GitHub. Legger til det som er særskilt for de felles skillene - om det trengs en ny skill i det hele tatt, tynn peker-skill mot innhold i GitHub eller selvstendig skill, kjøremiljø og sensitivitet, kaldtest og feiltyper, lagring og installasjon."
---

# Skill-bygging for de felles skillene

**Versjon 2026-10-22.** Hent også `https://raw.githubusercontent.com/tarjeiha/allover/main/SKILLVERSJONER.md`. Står det en nyere versjon for denne skillen der, si én gang, til slutt i svaret: «Det finnes nyere versjoner av de felles skillene. Si "oppdater skillene" for å få dem.» Feiler hentingen, la det være.

Companion-skill til skill-creator. Den dekker det som er særskilt for de felles skillene: om noe bør bli en skill i det hele tatt, hvor innholdet skal ligge, hvordan skillen testes, og hvordan den lagres og deles. Skillen brukes av alle ansatte som vil lage en skill, ikke bare av prosjektlederen og bidragsyterne, så forklar valgene i vanlig språk, ikke bare utfallet.

## Forhold til skill-creator

**Første handling: finn skill-creator blant de tilgjengelige skillene og åpne dens SKILL.md også.** Gjør det før du svarer, ikke når behovet dukker opp underveis.

Skill-creator dekker den generelle byggeprosessen (SKILL.md-anatomi, progressive disclosure, description, pakking). Denne skillen legger til det som gjelder de felles skillene. Det har vist seg at instruksen om å åpne skill-creator bare følges omtrent hver tredje gang. Derfor gjentas skill-creators fire kjernespørsmål her, slik at de stilles uansett:

1. Hva skal skillen kunne gjøre?
2. Når skal den trigge (hvilke formuleringer og situasjoner)?
3. Hva skal den levere, og i hvilket format?
4. Trengs testspørsmål med fasit, eller holder en vurdering?

Når begge skillene er i bruk, gjelder testmetoden og lagringsreglene her. Det gjelder også hvor mye av skill-creators automatiske testing som kjøres, se «Måling av trigging».

## Tilpass forklaringen til spørsmålet

- **Åpne spørsmål** («jeg vil lage en KI-hjelper for X»): forklar framgangsmåten, også hvorfor testing og plassering av innhold betyr noe.
- **Presise spørsmål** («hvorfor trigget ikke skillen»): gå rett på sak.
- Forklar hva en eksisterende skill gjør i vanlig språk, ikke bare med navnet.

## Steg 1: Trengs en ny skill?

Svar på dette før noe bygges. Det er det viktigste valget.

**Listen over skills har et tak.** I en test med 62 installerte skills ble bare rundt 30 descriptions vist til modellen. Hver ny skill konkurrerer med de andre om å bli sett, også avdelingsskills, fordi de ligger i samme liste hos den som har dem installert.

**Derfor:**
- **Temaet er hovedaksen.** Skills følger fagområde, ikke avdeling. Behov som gjelder én avdeling, legges som en egen mappe eller merknad under temaet i basen, og skillen er felles.
- **En ny skill lages bare når spørsmålene trenger egen trigging**, altså når de ellers ikke ville nådd riktig innhold.
- **Sjekk de felles pekerne først.** Gjelder det lov og forskrift, statistikk eller statsbudsjettet, skal innholdet inn i basen bak `felles-regelverk`, `felles-data` eller `felles-budsjett`, ikke i en ny skill.
- **Hvert tema har én faglig eier** som godkjenner avvik og avdelingsfiler.

## Steg 2: Tynn peker eller selvstendig skill

| Innhold | Hvor det hører hjemme |
|---|---|
| Stort, eller endrer seg (lovtekst, tall, rundskriv, rutiner, maler som oppdateres) | I et repo, med en tynn peker-skill |
| Stabilt: når skillen brukes, arbeidsmåte, svarregler, tone, format, små maler | I selve skillen |
| Skript som må kjøre med skillen (beregninger, filproduksjon) | I selve skillen |

**Hvilket repo:**
- `tarjeiha/allover` (offentlig): bare innhold som allerede er offentlig eller kan offentliggjøres. Inngangen er `CLAUDE.md` i roten, og veivisere under `regelverk/`, `budsjett/` og `data/`.
- Innhold som ikke skal ligge åpent: i selve skillen, som lastes ned som fil fra intranettet (som `felles-intern` og `felles-sprak`). Et privat repo kan ikke leses av brukere uten egen GitHub-tilkobling, heller ikke med token (testet 21.10.2026).
- Ikke i Claude i det hele tatt: noe som ikke er klarert for lagring hos en ekstern skytjeneste.

Gevinsten med en peker er at innholdet oppdateres uten at noen må laste opp skillen på nytt.

### Mønster for en peker-skill

De tre som finnes (`felles-regelverk`, `felles-data`, `felles-budsjett`) har samme oppbygning. Bruk den:

1. **Description:** bred på tema og hverdagsspråk. Avslutt med «Last den før du svarer, og svar ikke fra hukommelsen.»
2. **Brødtekst:** si at innholdet ikke ligger i skillen, men hentes ved hvert oppslag.
3. **Fremgangsmåte:** hent én inngangsfil med full adresse (`https://raw.githubusercontent.com/tarjeiha/allover/main/...`), med `curl -sL` i kodeverktøyet eller med hentverktøyet. Følg den.
4. **Hvis hentingen feiler:** svar ikke fra hukommelsen. Ta med avsnittet «Hvis hentingen feiler» fra en av de felles skillene, for eksempel `skills/felles-regelverk/SKILL.md` i allover, og bytt ut hva som hentes. Det skiller en sperre i innstillingene fra en midlertidig feil. Ved sperre sier Claude hvilket nettsted brukeren må tillate og hvor i innstillingene det gjøres, med norske menynavn og tilbud om engelske.

Avgrensningen (hva som er dekket og ikke) skal ligge i inngangsfilen i repoet, ikke i skillen. Da kan den endres uten ny opplasting. Hvordan regelverk legges inn og kontrolleres, står i `verktoy/BYGGING.md` i allover.

### Språk mot brukeren

Mange brukere er nye i KI. Alle felles skills skal be Claude snakke enkelt med brukeren og gjøre det tekniske uten å kommentere det. Ord som token, GitHub, repo, allover, filsti, skript, versjonsnummer og feilkode skal ikke stå i svaret. Skriv en eksempelsetning i skillen for det vanligste tilfellet, for eksempel en feilmelding: «Jeg fikk ikke hentet innholdet nå. Prøv igjen litt senere.» Ta det med i kaldtesten. Unntaket er navnet på et nettsted brukeren må tillate i innstillingene, siden brukeren må skrive det inn selv.

## Steg 3: Kjøremiljø og sensitivitet

**Kjøremiljøet varierer mellom brukere:**
- Uten kodeverktøy kan skillen ikke kjøre `curl` eller skript. Hentverktøyet leser åpne adresser, men kan ikke sende token eller egne overskrifter. Det offentlige repoet kan noen ganger leses uten kodeverktøy.
- Skriving til GitHub fra claude.ai er sperret (403, testet 20.10.2026), både med token og uten. En skill kan derfor ikke sende noe til et repo fra vanlig chat. Meldinger om feil går på e-post etter oppskriften i `OM-BASENE.md` i allover.
- Lesing fra et privat repo virker bare for brukere med egen GitHub-tilkobling. Claude.ai stopper forespørselen før et token i skillen blir prøvd (kollegatest 21.10.2026). Legg derfor aldri token i en skill.
- Skills med skript krever kodeverktøy. Skills som henter fra den åpne basen, krever også nettverkstilgang til GitHub. Skriv det i brukerveiledningen, og la skillen si hvilket nettsted som må tillates når hentingen er sperret (se «Mønster for en peker-skill», punkt 4).

**Sensitivitet er en del av designet.** Rammeverket for informasjonssikkerhet sier at blant annet r-notater ikke skal legges inn i KI-verktøy. Spør derfor om skillen vil invitere brukeren til å lime inn noe som ikke får ligge i Claude. Hvis ja, gjør skillen til et oppslagsverk for form og prosess som ikke tar imot saksinnhold. Det avgjørende er om noe avslører status, sannsynlig utfall, timing eller interne politiske vurderinger i en konkret sak, ikke om temaet er politisk følsomt.

## Description og trigging

- Ta med ordene folk faktisk bruker ved siden av fagordene («har ikke penger til husleie», ikke bare «økonomisk stønad»).
- Grensen er 1024 tegn. Unngå anførselstegn og kolon som kan ødelegge YAML-en. Skriv frontmatter med `yaml.dump()`, ikke med strengerstatning.
- Avgrens mot nabo-skillene, og si hva skillen ikke er for, når nabotemaet ligger nær.
- Skills som skal brukes sammen, kan ikke regne med at begge trigger samtidig (lykkes omtrent hver tredje gang). Gi en eksplisitt instruks om å åpne den andre.

## Testmetode: kaldtest

En kaldtest stiller spørsmålet til en økt som bare har skillen, uten forklaring og uten å nevne skillen.

**To måter, og begge trengs før en skill deles bredt:**
- **Underagent** (i et prosjekt eller Claude Code): raskt, kan kjøres i serier. Tester trigging og innhold, men i et miljø med kodeverktøy.
- **Ny chat i claude.ai**, helst utenfor prosjekt og helst uten kodeverktøy: tester det miljøet kollegene faktisk bruker.

**Testsettet** bør ha fire typer spørsmål: dekket med fagord, dekket med hverdagsspråk, rett utenfor avgrensningen (skal si fra, ikke svare fra hukommelsen), og ikke relevant (skal ikke trigge). Ta med kontrollspørsmål med kjent, kildekontrollert fasit, og spørsmål mot tabellinnhold når kilden har tabeller. Test sømmene mellom skills og baser, ikke bare kjernen. Foretrekk flere små runder (4–5 spørsmål) med retting mellom, framfor én stor.

**Feiltyper:**
- **A – Aldri synlig:** skillen trigger ikke.
- **B – Lest, men utelatt:** kilden leses, men informasjonen kommer ikke med i svaret.
- **C – Overflatisk:** SKILL.md lastes, men kildefilene åpnes aldri.
- **D – Overtrigging:** skillen trigger utenfor det den dekker og svarer fra hukommelsen i stedet for å si fra. Godkjent er å la være å trigge, eller å trigge og si at temaet ikke er dekket.
- **E – Basen leder feil:** skillen trigger og henter riktig, men inngangsfilen, veiviseren eller en merknad i repoet sender modellen feil vei (sti som ikke finnes, foreldet merknad, mappe i stedet for filnavn). Rett i repoet, ikke i skillen.

**Kaldtest fanger ikke byggefeil.** En skill som mangler innhold, svarer «ingen bestemmelse funnet i gjennomgått materiale», og det ser riktig ut. En utflatet tabell gir et selvsikkert svar med feilkoblede tall. Slike feil må fanges når innholdet bygges, og av kontrollspørsmål med fasit.

### Måling av trigging

Når Claude Code er tilgjengelig (`claude -p` kan kjøres), kan triggingen måles med skill-creators skript. Hver kjøring koster tokens, så bruk dem slik:

- **Skills som skal deles** (pekere og felles skills): kjør én måling med `run_eval.py` når descriptionen er ny eller endret. Bruk 20 realistiske spørsmål, omtrent halvparten som skal trigge og halvparten som ikke skal. De vanskelige spørsmålene ligger tett opptil en nabo-skill. Claude lager et utkast, og den som bygger retter det.
- **Forbedringsløpet** (`run_loop.py`) kjøres bare når målingen viser at skillen trigger dårlig. Det gjør flere runder med nye descriptions og koster mange ganger mer enn én måling.
- **Små skills til eget bruk:** noen få spørsmål for hånd holder.

Målingen sier om descriptionen treffer. Den sier ikke om svaret blir riktig, så kontrollspørsmål med fasit og kaldtest i vanlig chat trengs fortsatt før en skill deles bredt.

Skriv ned resultatet før du retter. Terskelen for når en skill er testet nok, avgjøres av prinsippet om kvalitet før bredde, ikke her.

## Lagring, installasjon og deling

**Kildesannheten:** de åpne felles skillene ligger i `allover/skills/<navn>/SKILL.md`, med en oversikt i `allover/skills/KATALOG.md`. Hent gjeldende versjon derfra før du endrer, og skriv endringen tilbake dit som pull request. En ny skill legges inn i katalogen med hvem den er for. Kildene til skillene som lastes ned som fil, ligger privat hos redaktøren. Felles skills heter `felles-…`, og ingenting i den åpne basen skal vise hvilket departement som står bak: ikke i navn, tekst eller e-postadresser.

**Versjon:** hver SKILL.md har en linje «Versjon ÅÅÅÅ-MM-DD» øverst (med .2, .3 osv. ved flere endringer samme dag), og `SKILLVERSJONER.md` i allover har nyeste versjon av hver skill. Når en skill endres, sett ny versjon begge steder i samme runde. Skillene sjekker filen og sier fra til brukeren når en nyere versjon finnes. Glemmer du allover, får ingen beskjed. Glemmer du skillen, får brukerne beskjed hver gang.

**Å skrive en skillfil er ikke det samme som å installere den.** Filer som lages i en økt, finnes bare der. Si alltid fra, uoppfordret, at endringen må installeres før andre økter ser den. Brukerne installerer og oppdaterer ved å si «oppdater skillene» til `felles-intern`. Den henter kilden fra den åpne basen og legger skillen fram som et kort brukeren lagrer (`propose_skills`). Skills som lastes ned som fil, oppdateres ved at redaktøren legger en ny fil på intranettet. Uten kortverktøyet lager den en zip-fil per skill. Lagring med samme navn erstatter den gamle.

**Endringer i innholdet i et repo krever ingen ny installasjon.** Si det også, slik at ingen laster opp en peker-skill på nytt uten grunn.

## Send skillen til vurdering

En skill en ansatt lager, er til eget bruk. Den som vil, kan sende den til vurdering som felles skill. Redaktøren for basene vurderer om den skal bli en egen felles skill, en del av en eksisterende skill, eller innhold i en av basene på GitHub.

1. Gjør dette bare når brukeren selv spør om skillen kan bli felles, eller vil sende den til vurdering. Ikke foreslå det på eget initiativ.
2. Sjekk at den ikke inneholder token, personopplysninger, saksinnhold eller interne vurderinger.
3. Hent `https://raw.githubusercontent.com/tarjeiha/allover/main/OM-BASENE.md` og følg avsnittet om feil, med type «ny skill» og base «interne rutiner». Skriv i meldingen hva skillen gjør, hvem den er for, og hvordan den er testet. Legg SKILL.md ved som fil, eller lim den inn i e-posten hvis den er kort.
4. Meldingen går til redaktøren for basene, Tarjei Havnes. Adressen står i skillen `felles-intern`.

Si til brukeren at skillen kan brukes selv mens den vurderes, men at hver egen skill konkurrerer med de felles skillene om plassen i lista (se steg 1).

## Dokumentasjon

- **Selvstendige skills:** én `endringslogg.md` i skillens mappe. Én oppføring per endring med **Funn**, **Endring**, **Basert på**, **Ikke gjort ennå** og ved behov **Vurdert og forkastet** (bare når noen sannsynligvis vil foreslå det samme igjen). Skriv oppføringen før du retter.
- **Innhold i repo:** pull requesten og commit-meldingen er loggen. Endringer godkjennes av eieren av mappen (`.github/CODEOWNERS`).
- **Peker-skills** endres sjelden. Når de gjør det, logg det i PR-en.

## Når skills og baser virker sammen

Når en skill for språk eller kommunikasjon bearbeider et svar som bygger på regelverk eller tall, skal kildegrunnlaget fortsatt finnes i samme svar.
- **Internt eller fagpublikum:** kilden kan stå i teksten.
- **Lekfolk (svar til innbygger, pressemelding):** kilden står adskilt, f.eks. som en kort note under utkastet.
- Brukeren skal aldri få bare den ferdige teksten uten at kildegrunnlaget er tilgjengelig.

## Når et funn bør endre denne skillen

Si fra i samtalen når et funn gjelder hvordan neste skill, uansett tema, bør bygges, testes, lagres eller dokumenteres. Eksempler er en ny feiltype eller en ny begrensning i kjøremiljøet. Foreslå konkret hvilket avsnitt som bør endres, og vent på svar. Funn som bare gjelder skillen du bygger, hører hjemme i dens egen logg. Terskelen skal være høy.
