# Endringslogg

Loggen er overtatt fra skillen aid-stortinget-fra2021. Eldre oppføringer nevner skillene og skillmappene som fantes før flyttingen.

## 2026-10-20 – Vedtakstekst fra feil felt, synonymer i søket og liste over nattens endringer

**Funn:** Representantforslag fra sesjon 2025-2026 hadde 0 avviste og 108 «annet» uten vedtakstekst. Stortingets vedtaksliste har prefikset feltene med `stortingsvedtak_` (`stortingsvedtak_tekst`, `_tittel`, `_nummer`, `_dato_tid`), og teksten leveres som HTML. Skriptene leste `tekst`, som er tom, så avvisningsformlene traff aldri. Nye anmodningsvedtak ville fått tom tekst, tittel, nummer og dato. «Annet» ble heller aldri vurdert på nytt, bare «ukjent».

**Endring:** `vedtak_felt()` og `vedtak_tekst()` i `felles.py` leser de nye feltene (med fallback til de gamle) og fjerner HTML. Oppdateringen vurderer nå også «annet» uten vedtakstekst på nytt. Prøvekjørt mot 2025-2026 i GitHub: 102 avviste, 6 «annet» (alle med tekst). Nattjobben i oktober og november kjører forrige sesjon og retter dataene av seg selv.

**Søk:** `SYNONYMER` i `sok_stortinget.py` utvider AIDs fagord med synonymer og nynorske former. Et sammensatt søkeord uten treff deles i to ledd, og skriptet sier fra.

**Varsel:** Nattjobben skriver `siste-endringer.json` med nye poster og spørsmål som har fått svar, til varselet om nye stortingssaker (PR #67).

## 2026-10-19 – Flyttet til allover

**Endring:** Begge skillpakkene (aid-stortinget-2013-2021 og aid-stortinget-fra2021) er slått sammen til `stortinget/` i allover, med én datafil per sesjon og datatype. Søkeskriptet og oppdateringsskriptene er tilpasset (`last_json`/`skriv_json` arbeider på mapper). Oppdateringen kjører som Action hver natt.

**Funn:** 287 representantforslag i 2013-2021-dataene sto to ganger, med to ulike `sesjon_fremmet`, fordi samme sak er listet i to påfølgende sesjoner. Dublettene er fjernet ved sammenslåingen, og første forekomst er beholdt.

## 2026-10-13 – Lenkefeil: `qid` → `qnid` i URL-malene

**Funn:** Lenkene til spørsmål på stortinget.no brukte parameteret `?qid=`, som gir serverfeil. Riktig parameter er `?qnid=`. Bekreftet av bruker 13.10.2026 for alle tre spørsmålstyper (f.eks. `?qid=127672` feiler, `?qnid=127672` gir riktig side).

**Endring:** `URLS` i `scripts/felles.py` og URL-mønstrene i `references/oppdatering.md` endret fra `qid` til `qnid`. Datafilene lagrer ikke lenker (de bygges fra `legacy_id` ved visning), så ingen data måtte bygges om. Samme rettelse gjort i companion-skillen `aid-stortinget-2013-2021`.

## 2026-09-22 – Ordbasert matching og retningslinjer for brede søk

**Funn:** Fraseoverensstemmelse i `matcher_tekstfelt()` krevde at hele søkeordet stod sammenhengende i ett felt. Testet konkret: «pårørendestøtte» (ett ord) ga 0 treff, mens 11 spørsmål inneholdt både «pårørende» og «støtte» separat i tittelen. Uavhengig av dette ble et relevant spørsmål (qid=108210, 2026-04-17, om oppfølging av anmodningsvedtak 147/23) luket bort manuelt i en brukersamtale, fordi kompakt-visningen (>20 treff) kuttet tittelen til «Hva vil ... nå gjøre for å følge opp Stortingets…» — dette skjulte at spørsmålet gjaldt nettopp det aktuelle vedtaket. Ikke en datafeil (`--format json` viser alltid full, utrunkert tekst), men en kombinasjon av kompakt-trunkering og manuell kuratering fra titler alene. Videre bekreftet: samme anmodningsvedtak (147/23) hadde spørsmål stilt til to ulike statsråder (arbeids- og inkluderingsministeren og helse- og omsorgsministeren) — innsnevring på `--minister` ville kuttet bort en del av den sammenhengende tråden. Emne-dekning for datatypen `sporsmal` er dessuten kun 13,5 %, så emne-basert filtrering er lite pålitelig for denne datatypen.

**Endring:**
1. `matcher_tekstfelt()` endret fra fraseoverensstemmelse til ordbasert AND (alle ord i søket må finnes et sted i feltene, uansett rekkefølge/felt). Strengt supersett av gammel oppførsel — utvider aldri innskrenker treffmengden. Løser IKKE sammensatte ord (se «Matching er ordbasert AND» i SKILL.md).
2. Nye retningslinjer i SKILL.md: ikke kurer fra kompakt titteltavisning over 20 treff (bruk `--format json` eller spør bruker om innsnevring); unngå `--minister`/`--komite` som første innsnevringsakse på tverrgående velferdstemaer.
3. Samme kodeendring gjort i companion-skillen `aid-stortinget-2013-2021` (egen, uavhengig kopi av skriptet — ikke delt via felles.py, siden matcher_tekstfelt kun brukes av søkeskriptet, ikke av vedlikeholdsskriptene).

**Basert på:** Brukersamtale 2026-09-22 der et konkret glipp (qid=108210) ble diagnostisert trinnvis, inkludert kvantifisert emne-dekning og et manuelt ord-vs-frase-forsøk før koden ble endret.

**Ikke gjort ennå:** OR-modus i tillegg til AND (vurdert, ikke bygget — ingen påvist behov ennå). Finere relevans-rangering som skiller "alle ord funnet" fra "eksakt frase funnet" utover det `relevans_niva()` allerede gjør. Kaldtest av de nye retningslinjene i en frittstående samtale.

**Vurdert og forkastet:** Full semantisk/emne-indeksering (topic-tagging) av ~19 000 spørsmål — vurdert som et for stort tiltak sammenlignet med påvist behov; ordbasert matching løser det konkrete tilfellet som utløste diskusjonen, uten ny infrastruktur. Kan revurderes hvis ordbasert matching senere viser seg utilstrekkelig (f.eks. ved systematiske synonym-glipp).

## 2026-09-16 – Permanente vedlikeholdsskript (felles.py, oppdater_inkrementell.py, backfill_sesjon.py) + fullført historisk backfill

**Bakgrunn:** Etter dagens tredje kjøring på rad ble det tydelig at det ukentlige/daglige oppdateringsarbeidet ble gjort som ad hoc Python skrevet på nytt hver gang, ut fra prosa i `references/oppdatering.md` — samme minister-tabell, URL-mønstre, sentinel-datohåndtering og avvisningsformler ble reimplementert i stedet for gjenbrukt. Bruker påpekte dette eksplisitt og ba om et permanent skript.

**Design, avklart i samtale før bygging:**
1. Oppdateringsskriptet skal ikke bare LEGGE TIL nye poster, men også REKONSILIERE eksisterende poster hvis status har endret seg siden sist (spørsmål besvart, representantforslag fått utfall) — ren tillegg ble vurdert utilstrekkelig gitt formålet «erstatte behovet for varsling direkte fra Stortinget».
2. Rekonsiliering avgrenset til INNEVÆRENDE sesjon i det lette skriptet (billig, siden vi uansett henter full sesjons-XML hver kjøring). Historisk backfill av avsluttede sesjoner er en egen, sjeldnere engangsjobb — avsluttede sesjoner endrer seg ikke, så periodisk gjentakelse ville vært bortkastet arbeid.
3. Representantforslag-UTFALL rekonsilieres på tvers av ALLE sesjoner (ikke bare inneværende) hver kjøring, siden vedtak-oppslaget uansett bygges gratis fra fersk `stortingsvedtak`-XML.

**Endring:**
- Ny fil `scripts/felles.py`: samler all delt logikk — MINISTER_TITTEL, SPORSMAL_URL_MONSTER, AVVISNING_FORMLER, sentinel-datohåndtering, sak-berikelse (`hent_sak_detaljer`), utfall-klassifisering, samt parse-funksjoner for alle tre datatyper. `scripts/sok_stortinget.py` refaktorert til å importere disse i stedet for å duplisere dem (testet etter refaktorering — søk fungerer identisk).
- Ny fil `scripts/oppdater_inkrementell.py`: lett, idempotent, kjøres av den daglige scheduled-oppgaven («Nye spørsmål på Stortinget») for inneværende sesjon. `--dry-run` støttet.
- Ny fil `scripts/backfill_sesjon.py`: engangsjobb for historiske sesjoner, gjenbruker samme `felles.py`-logikk.
- **Ytelsesfunn under bygging:** første versjon av representantforslag-oppdateringen gjorde ett per-sak-nettverkskall for HVER av de 335 representantforslagene i inneværende sesjon, hver kjøring — timet ut etter 2 minutter. Fikset ved å skille billig grunnrecord (rein bulk-XML, ingen nettverkskall — status/utfall er nok for rekonsiliering) fra kostbar berikelse (forslagstillere/komite/emne via per-sak-oppslag), og kun berike GENUINT NYE poster.
- **Datafunn under testing (fanget FØR skriving, ikke etterpå):** første versjon av `parse_sporsmal_record` hardkodet `emne: []` for alle spørsmål — kopiert fra dagens tidligere ad hoc-skript. Dry-run mot historiske sesjoner viste 440+ falske «oppdatert»-treff der eneste forskjell var at ekte, allerede-kategoriserte emne-data (`emne_liste` FINNES i bulk-XML-en for spørsmål, ble bare aldri lest av noe skript — heller ikke det opprinnelige byggeskriptet) ville blitt overskrevet med tom liste. Rettet før noe ble skrevet til disk. Dette gjelder alle sesjoner, ikke bare de historiske — inneværende sesjons spørsmål har nå også fått emne-data for første gang.
- **Kjørt:** `oppdater_inkrementell.py` (inneværende sesjon, 2025-2026) og `backfill_sesjon.py` (2021-2022 t.o.m. 2024-2025). Resultat: +133 nye spørsmål/interpellasjoner/spørretime på tvers av de fire historiske sesjonene (51+32+33+17), pluss emne-berikelse på ca. 1370 eksisterende poster (424 inneværende sesjon + ~950 historiske) som aldri hadde emne fra før. `sporsmal.json` er nå 19166 poster, verifisert 0 duplikater, idempotens verifisert (ny dry-run kjøring viser 0/0 overalt).
- SKILL.md oppdatert: tall, fjernet «historisk backfill ikke gjort»-begrensningen, ny seksjon under «Datakilde og oppdatering» som peker til de nye skriptene i stedet for kun prosa-fremgangsmåten.
- Den daglige scheduled-oppgaven («Nye spørsmål på Stortinget», trig_01BYZJgVezHP7egb8xaahpMJ) fikk steg 1 omskrevet til å kalle `oppdater_inkrementell.py` direkte i stedet for å be Claude lese `oppdatering.md` og reimplementere logikken hver gang.

**Etterfølgende, samme dag:** `emne`-feltet inkludert i `matcher_tekstfelt()`/`relevans_niva()` for sporsmal-datatypen (samme mønster som stikkord for anmodningsvedtak, men uten behov for en bloat-grense — fordeling sjekket: maks 18 emne per post, median rundt 3-4 blant poster som har emne, ingen tegn til sak-nivå-bloat slik stikkord hadde). Testet med `--id 70221` og fritekstsøk.

**Ikke gjort ennå:**
- Kvartalsvis datakvalitetsaudit (egen scheduled task opprettet samme dag) vil neste gang sjekke om 139-duplikat-funnet nevnt i forrige logglinje fortsatt er reelt — ved siste sjekk i dag var representantforslag.json allerede uten duplikater (1367 total = 1367 unike), så det kan ha vært rettet i en mellomliggende økt eller vært en forbigående observasjon. Ikke gravd videre i akkurat dette.

**Basert på:** Brukerens eksplisitte ønske om et permanent skript («la oss gjøre begge»), etter en designdiskusjon steg for steg samme dag (add-only vs. rekonsiliering; avgrensning av rekonsiliering til inneværende sesjon; frekvens for tyngre vedlikehold).


## 2026-09-16 – Ukentlig inkrementell oppdatering (automatisert), runde 2 samme dag

**Endring:** Hentet fersk XML for sesjon 2025-2026 (alle fem endepunkter, `status=alle`) og sammenlignet mot lokale ID-er (som nå inkluderer dagens tidligere `status=alle`-backfill). Lagt til: 14 nye poster i `sporsmal.json` (id 127251–127276: 13 skriftlige spørsmål + 1 interpellasjon fra Kjersti Toppe til helse- og omsorgsministeren om Finnmarkssykehuset, alle `til_behandling`). 0 nye anmodningsvedtak, 0 nye representantforslag.

Relevante for AID blant de 14: 1 stilt direkte til ARI (id 127263, vertskommuners dekning av merutgifter ved asylmottak). 2 traff temaklyngen integrering/migrasjon ved bredt søk (id 127264: UDI-saksbehandlingstid for oppholdstillatelse til sesongarbeidere; id 127267: adgang for Gaza-studenter/-forskere til å fortsette utdanning i Norge, sistnevnte grensetilfelle).

**Merk om «endringslogg 2026-09-14»:** Oppgaveteksten for denne kjøringen viste igjen til en kjent synk-etterslep-oppføring datert 2026-09-14. Bekreftet på nytt (som i forrige kjøring samme dag): ingen slik oppføring finnes i denne loggen. Flagget til bruker i oppsummeringen i stedet for å anta innhold — samme observasjon som forrige runde, gjentas her for sporbarhet.

**Basert på:** Automatisert ukentlig kjøring (scheduled task), 2026-09-16, andre gang denne dagen.


## 2026-09-16 – Fiks: `status=alle` lagt til, ubesvarte spørsmål/interpellasjoner tilbakefylt for inneværende sesjon

**Endring:** Basert på rotårsaksfunnet rett under (samme dag): lagt til 162 poster i `sporsmal.json` for sesjon 2025-2026 som manglet pga. det stille `besvart`-filteret (128 `til_behandling`, 31 `trukket`, 3 `bortfalt` — fordelt 126 skriftlige spørsmål, 33 spørretime, 3 interpellasjoner). Inkluderer Toppe-interpellasjonen (id 126876) brukeren opprinnelig meldte fra om.

- `references/oppdatering.md` oppdatert: `&status=alle` lagt til som obligatorisk parameter på de tre `sporsmal`-endepunktene (bekreftet at `stortingsvedtak` og `saker` IKKE har samme filterproblem — testet 666/666 og 1166/1166 med/uten parameteren). Dokumentert håndtering av `besvart_dato`-sentinelverdi (`0001-01-01`) og manglende `tittel` for ubesvarte interpellasjoner.
- `scripts/sok_stortinget.py`: nytt `--status`-filter (besvart/til_behandling/trukket/bortfalt). Statusmerke `[TIL BEHANDLING]` osv. vises nå i alle visningsnivåer når status ≠ besvart, ikke bare i full visning. Ny `MERK`-linje i kort-format når treff inkluderer ikke-besvarte poster.
- For interpellasjoner uten fastsatt tittel (skjer før formell behandling): konstruert midlertidig tittel av typen «Interpellasjon fra {fra_navn} ({fra_parti}) til {til_minister_tittel}», merket med `tittel_midlertidig: true` på posten og vist med eksplisitt forklaring i søketreff — ikke presentert som Stortingets offisielle tittel.
- SKILL.md: tallet for `sporsmal` oppdatert til 19019, «Kjente begrensninger» utvidet med status-dekning og at historisk backfill (sesjon 2021-2022 t.o.m. 2024-2025) ikke er gjort.

**Ikke gjort:** Historisk backfill av de 12 tidligere sesjonene (2013-2014-pakken er en egen skill og uberørt av dette; 2021-2022 t.o.m. 2024-2025 i DENNE skillen er ikke sjekket for gjenværende `trukket`/`bortfalt`-poster som aldri ble besvart). Lavere prioritet siden formålet fremover er løpende dekning, men bør vurderes for et fullstendig historisk bilde.

**Følgefeil oppdaget og rettet i samme runde:** Første implementasjon av dato-fallback brukte `sendt_dato or datert_dato`, som feilaktig lot en `0001-01-01`-sentinelstreng (truthy i Python) vinne over en reell dato — rammet 34 poster (typisk `trukket` spørretimespørsmål, der både `besvart_dato` og `sendt_dato` er sentinel og bare `datert_dato` er reell). Rettet ved å sjekke hvert datofelt individuelt mot sentinelen. `references/oppdatering.md` oppdatert med riktig mønster.

**Basert på:** Brukerens eksplisitte ønske om at indeksen skal dekke alle statuser («målet må jo være at dette erstatter behovet for varsling direkte fra Stortinget»), 2026-09-16.

## 2026-09-16 – Rotårsak funnet: ubesvarte spørsmål/interpellasjoner mangler helt (ikke synk-lag)

**Funn:** Brukeren husket et konkret tilfelle — en interpellasjon fra Kjersti Toppe (Sp) til helse- og omsorgsministeren, fremmet 4. august 2026, synlig på stortinget.no men fraværende fra vår lokale indeks. Testet direkte mot data.stortinget.no: standardkallet `interpellasjoner?sesjonid=2025-2026` (uten `status`-parameter) returnerer **kun poster med status `besvart`** — 30 stk. Med `&status=alle` lagt til kommer 33 poster: 2 `til_behandling` (inkl. Toppes, sporsmal_nummer 33, id 126876, sendt 04.08.2026) og 1 `bortfalt`.

Samme mønster bekreftet på de to andre spørsmålstypene for inneværende sesjon alene: `skriftligesporsmal` går fra 3660 (kun besvart) til 3786 med `status=alle` (+126 `til_behandling`), `sporretimesporsmal` fra 524 til 557 (+31 `trukket`, +2 `bortfalt`). Til sammen minst 162 poster usynlige i denne ene sesjonen alene, sannsynligvis flere i de 12 tidligere sesjonene siden samme standardfilter høyst sannsynlig gjaldt ved førstebyggingen.

**Dette er ikke synk-etterslep mellom stortinget.no og data.stortinget.no** (det brukeren og jeg opprinnelig antok, og som den nå fjernede oppgaveteksten viste til) — det er et stille filter på API-kallet vi bruker: alt som ikke er `besvart` (til_behandling, trukket, bortfalt) forsvinner helt fra listen inntil status endrer seg. En interpellasjon sendt inn midt i sommerferien, med planlagt behandling først i oktober (etter sesjonsslutt 30/9), kan dermed være usynlig i ukesvis i vår indeks selv om den ligger åpent på stortinget.no hele tiden.

**Ikke rettet ennå:** Selve datainnhentingen (`references/oppdatering.md` og det ukentlige inkrementelle skriptet) bruker fortsatt standardkallet uten `status=alle`. Å legge til parameteren er en liten endring, men reiser spørsmål som bør avklares før implementering: skjemaet for ubesvarte poster mangler `tittel` og andre felt (kun fylt ut ved besvart) — trenger egen håndtering i skjemaet i `sporsmal.json`, og `--status`-filter bør trolig legges til i søkeskriptet slik at brukeren kan skille «besvart» fra «til behandling»/«trukket»/«bortfalt» i søk. Historisk backfill (om de 12 tidligere sesjonene har samme hull) er heller ikke gjort.

**Basert på:** Brukerens observasjon av Toppe-interpellasjonen, verifisert direkte mot data.stortinget.no, 2026-09-16.

## 2026-09-16 – Ukentlig inkrementell oppdatering (automatisert)

**Endring:** Hentet fersk XML for sesjon 2025-2026 (alle fire datatyper) og sammenlignet mot lokale ID-er. Lagt til: 10 nye spørsmål/interpellasjoner/spørretime (id-er 126991–127163, datert 28.08–15.09.2026). 0 nye anmodningsvedtak, 0 nye representantforslag denne runden. Ingen av de 10 nye spørsmålene var stilt til ARI eller traff AID-ens temaklynger (trygdeytelser, arbeidsliv, NAV, integrering/migrasjon) — sjekket manuelt siden volumet var lite.

**Datakvalitetsfunn (ikke rettet, utenfor omfanget av denne kjøringen):** `representantforslag.json` har 1506 poster men bare 1367 unike id-er — 139 duplikate id-er finnes allerede i datasettet (bekreftet før denne kjøringens skriving, dette er ikke noe jeg introduserte). Bør ryddes ved neste større vedlikehold.

**Ikke funnet:** Oppgaveteksten for denne kjøringen viste til «endringslogg 2026-09-14» om kjent synk-etterslep mellom stortinget.no og data.stortinget.no. Ingen slik oppføring finnes i denne loggen — verken 2026-09-14 eller andre datoer nevner synk-etterslep. Kan skyldes at oppføringen ble skrevet i en økt som ikke har syncet hit, eller at referansen i oppgaveteksten er feil. Flagget til bruker i stedet for å anta innhold.

**Basert på:** Automatisert ukentlig kjøring (scheduled task), 2026-09-16.

## 2026-09-10 – Fortsatt uløst: web_search foretrukket fremfor skill (test 5, gjentatt)

**Funn:** Brukerens egen re-test bekreftet at forrige runde sin SKILL.md-skjerping ikke løste web_search-vs-skill-prioriteringsfeilen (se forrige oppføring). Samme spørsmålstype trigget fortsatt web_search først.

**Endring:** Lagt til navngitt-parti-mønster i trigger-beskrivelsen («har SV/Venstre/FrP/Ap foreslått X», «hva skjedde med forslaget om X») — testspørsmålet brukte et konkret partinavn («Venstre»), ikke det generiske «opposisjonen» som allerede lå i beskrivelsen. Lav tiltro til at dette alene løser problemet.

**Basert på:** Brukerens re-test, 2026-09-10.

**Ærlig vurdering, ikke bare "ikke gjort ennå":** Dette kan være et strukturelt triggerproblem som SKILL.md-tekst ikke kan løse fullt ut — jf. prosjektets egne notater om at automatisk samvalg mellom skill og generelt verktøy er upålitelig. Hvis neste testrunde fortsatt viser samme mønster etter denne justeringen, bør vi vurdere at dette er en aksepert restrisiko fremfor å fortsette å justere beskrivelsestekst uten empirisk støtte for at det hjelper.

## 2026-09-10 – Kaldtest runde 2: web_search foretrukket fremfor skill, hallusinert forklaring, tapte lenker

**Funn:** Kjørte 7 testspørsmål med kjent fasit dekkende de nye datatypene og companion-skill-grensen. 4 av 7 uten anmerkning eller med bare oppklarende spørsmål. 3 reelle funn:

1. **Test 4 (hallusinasjon, alvorlig):** Svar om skriftlige spørsmål til helse- og omsorgsministeren inneholdt en oppdiktet forklaring på engelsk om når sesjoner tekniske sett avsluttes («last written questions logged into early October...») — denne informasjonen finnes ikke i kildedataene eller SKILL.md. Selve svartallet (330) var korrekt; forklaringen rundt var ren oppspinn, og på feil språk.
2. **Test 5 (prioriteringsfeil, mest alvorlig):** På spørsmålet «har Venstre foreslått lobbyregister» ble web_search brukt i stedet for denne skillen, til tross for at spørsmålet er en lærebokeksempel på hva skillen er bygget for. Skillen ble først brukt etter at bruker presiserte spørsmålet. Brukeren påpekte i tillegg at siden spørsmålet ikke oppga tidsperiode, burde svaret enten sjekket begge companion-skillene eller eksplisitt sagt hvilken periode som ble dekket.
3. **Test 6 (regresjon på tidligere fiks):** Et bredt spørsmål (50 treff) ble besvart med en tematisk gruppering i prosa — helt uten enkelt-lenker, til tross for at «alltid ta med lenke» ble innført som fast krav i forrige testrunde. Svaret lovet også en full liste med lenker som aldri ble levert i samme svar.

**Endring:** SKILL.md (begge pakker) utvidet med: (a) eksplisitt forbud mot web_search som førstevalg for disse datatypene, (b) krav om norsk bokmål og forbud mot å spekulere/dikte prosedyredetaljer utover kildedataene, (c) krav om å opplyse periodedekning eksplisitt ved uspesifisert tidsperiode, (d) presisert at lenke-kravet gjelder også ved tematisk gruppering — enten full liste med lenker per gruppe, eller minst én representativ lenke per tema, aldri lenkefri prosa. (e) Lagt til et eksplisitt krav om å levere det man lover i samme svar, ikke utsette til neste tur.

**Basert på:** Brukerens rapporterte kaldtestresultater, 2026-09-10.

**Ikke gjort ennå:** Kaldtest runde 3 bør spesifikt re-teste om web_search-prioriteringsfeilen er rettet (samme type spørsmål som test 5), og om lenker faktisk følger med ved tematisk gruppering av mange treff (samme type spørsmål som test 6). Companion-skill-samtrigging (test 1) så ut til å fungere denne runden, men bør bekreftes på nytt i en frisk samtale.

## 2026-09-10 – Splitt i to periode-pakker, spørretime gjeninnført

**Funn:** Brukeren ønsket spørretimespørsmål tilbake (tatt ut i forrige revisjon pga. 30 MB-grensen), og foreslo å løse plassproblemet ved å dele skillen i to periode-pakker i stedet for å kutte innhold — splittet ved regjeringsskiftet Solberg→Støre (sesjon 2020-2021/2021-2022), som gir både en naturlig politisk skillelinje og god størrelsesbalanse.

**Endring:**
- Skillen delt i `aid-stortinget-2013-2021` (Solberg-perioden, avsluttet) og `aid-stortinget-fra2021` (denne pakken, 5+ sesjoner, Støre-perioden — vokser videre, dette er stedet nye sesjoner alltid legges til)
- Spørretimespørsmål lagt til igjen i begge pakker (samme komprimeringsmønster som skriftlig/interpellasjon: kort typekode, ministertittel-oppslag, rekonstruert lenke)
- Størrelse denne pakken: 14,6 MB (1695 anmodningsvedtak + 18847 spørsmål/interpellasjon/spørretime + 1506 representantforslag)
- Søkeskriptet identisk mellom pakkene bortsett fra `PERIODE_START_AAR`/`PERIODE_SLUTT_AAR`/`COMPANION_SKILL`-konstantene, som styrer et presist varsel når en sesjon utenfor denne periodens dekning etterspørres — skiller eksplisitt mellom «feil periode, bruk companion-skillen» og «ikke oppdatert ennå», slik at Claude ikke feilaktig konkluderer at indeksen må friskes opp når det egentlig er snakk om å bruke den andre skillen

**Basert på:** Bygge-samtale 2026-09-10, brukerens forslag om periodedeling som løsning på størrelsesbegrensningen.

**Ikke gjort ennå:** Kaldtest av companion-skill-henvisningen spesifikt — bør inkludere et testtilfelle som sjekker om Claude faktisk konsulterer begge skillene ved et periodeoverskridende spørsmål, gitt at automatisk samtrigging mellom skills er kjent ustabil.

**Vurdert og forkastet:** Å beholde én skill og heller kutte mer innhold (f.eks. `tittel`-feltet) for å få plass til spørretime — forkastet fordi periodedeling bevarer alt innhold uten informasjonstap, og gir dessuten en intuitiv, brukervendt inndeling (regjeringsperiode) i stedet for en vilkårlig teknisk begrensning.

## 2026-09-10 – Komprimering under 30 MB-grensen

**Funn:** Første pakkeforsøk feilet med «Zip file uncompressed exceeds 30 MB» — claude.ai har en hard grense for skill-pakker. Total data var 49,4 MB (sporsmal alene 40,6 MB, dominert av `skriftlig_sporsmal` med 32814 poster).

**Endring:**
- Fjernet `sporretime_sporsmal` fra pakken (8,2 MB) — dette var mitt eget forslag om å ta med i samme slengen, ikke noe brukeren opprinnelig ba om. Gjenoppretter dermed det faktiske opprinnelige omfanget (skriftlig spørsmål + interpellasjon).
- `url` fjernet fra lagrede poster i `sporsmal` — rekonstrueres i skriptet fra `type` (nå kort kode: `s`/`i`) + `legacy_id`. Null informasjonstap, siden URL-mønsteret er deterministisk.
- `til_minister_tittel` fjernet — erstattet med en 52-oppførings oppslagstabell (`MINISTER_TITTEL`) i skriptet, indeksert på `til_minister_id`. Null informasjonstap for de 52 kjente kodene; se advarsel i skriptet om at sjeldne/historiske koder kan mangle.
- `sendt_dato`/`datert_dato` slått sammen til ett `dato`-felt (prioriterer `besvart_dato`, faller tilbake til `sendt_dato`) — **reelt informasjonstap**: skiller ikke lenger mellom når spørsmålet ble sendt og når det ble besvart.
- Alle tre datafiler skrevet som kompakt JSON (`separators=(',',':')`) i stedet for `indent=2`.

Resultat: 49,4 MB → 25,9 MB. Testet grundig at rekonstruert lenke og ministertittel stemmer med rådataene (stikkprøve: qid=60781 for et kjent spørsmål, matcher original XML).

**Basert på:** Feilmelding fra bruker ved installasjonsforsøk, 2026-09-10.

**Ikke gjort ennå:** Spørretimespørsmål som egen, separat skill (data finnes allerede i `stortinget_raw/`, bare ikke bundlet). Vurdere om `datert_dato` bør gjeninnføres hvis noen faktisk trenger sendt-vs-besvart-skillet.

**Vurdert og forkastet:** Å beholde spørretimespørsmål og heller kutte i `tittel`-feltet (selve spørsmålsteksten) — forkastet fordi lengdefordelingen viste at innholdet er jevnt fordelt (median 276 tegn), ikke dominert av noen få ekstremt lange poster. Å korte ned til f.eks. 300 tegn ville skadet 45% av postene for en besparelse på bare 4,6 MB — dårlig bytte sammenlignet med å droppe en hel, mindre etterspurt datatype.

## 2026-09-10 – Utvidelse: spørsmål, interpellasjoner, spørretime, representantforslag

**Funn:** Brukeren ønsket tilsvarende indeksering av skriftlige spørsmål og interpellasjoner. Diskusjon avdekket flere designspørsmål underveis:
1. Bør dette være egen skill eller del av anmodningsvedtak-skillen? Løst med presedens fra regelverksskillene: del etter fagområde (alt fra Stortinget), ikke kildetype. Én skill, ikke tre-fire.
2. Bør datasettet avgrenses til AID-relevante saker (f.eks. spørsmål til AID-ministeren)? Forkastet — samme begrunnelse som at anmodningsvedtak dekker alle departementer. Mottaker er dessuten et svakere avgrensningssignal enn komité, siden regjeringsomdanninger flytter ansvarsområder uten at spørsmålets innhold endres. Løsning: full dekning + `--minister`/`--komite` som søkefilter, ikke innebygd avgrensning.
3. Skulle vi ta med spørretimespørsmål og representantforslag også? Ja til begge — spørretimespørsmål har identisk skjema og kostnad som skriftlig/interpellasjon (naturlig å ta med samtidig). Representantforslag ble inkludert etter diskusjon om at avviste forslag ellers usynliggjøres helt (et forslag som stemmes ned produserer aldri et anmodningsvedtak).
4. Volumsjekk før bygging: skriftlige spørsmål er ~15x volumet av anmodningsvedtak per sesjon. Løst ved å oppdage at liste-endepunktet allerede inneholder full spørsmålstekst + metadata — ingen per-post-berikelse nødvendig (i motsetning til anmodningsvedtak, som krengte sak-oppslag). Selve svarteksten er likevel ikke inkludert (krever `enkeltsporsmal`-oppslag, upraktisk i bulk for 39 000+ poster) — hentes live ved behov i stedet.
5. **Representantforslag-utfall var den krevende delen.** Første forsøk (voteringsendepunktet, `vedtatt: true/false` per votering) ble testet og forkastet — feltet skiller ikke reelt vedtatt forslag fra vedtatt *avvisning* av forslaget. Løsningen ble å gjenbruke rådata vi allerede hadde (alle vedtakstyper, ikke bare ANMOD, fra alle 13 sesjoner) og matche på sak_id — men et forslags vedtak kan komme i en **senere** sesjon enn den det ble fremmet i (`behandlet_sesjon_id` kan avvike). Løst med ett samlet sak_id-til-vedtak-oppslag på tvers av alle sesjoner (2,9 sek å bygge, null nye API-kall). Avvisningsformelen viste seg å ha mange varianter på bokmål og nynorsk (`vedlegges protokollen`, `vedtas ikke`, `lagt ved møteboka`, `blir å leggja ved`, m.fl.) — funnet iterativt ved å inspisere restkategorien «annet» etter hver runde til den sluttet å krympe merkbart.

**Endring:**
- Ny fil `data/sporsmal_2013-2026.json` (39040 poster: skriftlig spørsmål, interpellasjon, spørretimespørsmål — samme skjema, type-felt skiller dem)
- Ny fil `data/representantforslag_2013-2026.json` (3220 poster, utfallsfordeling: 56% avvist, 28% vedtatt som anmodning, 2,5% annet, 14% ukjent)
- Søkeskriptet omdøpt til `scripts/sok_stortinget.py`, utvidet med `--datatype`, `--minister`, `--sporsmalstype`, `--parti`, `--utfall`. Søker i alle tre datatyper samtidig med mindre `--datatype` er angitt.
- Skillen omdøpt til `aid-stortinget-fra2013` (fra `aid-anmodningsvedtak-fra2013`) siden omfanget nå er bredere. Se tidligere omdøpingshistorikk under.

**Basert på:** Bygge-samtale 2026-09-10.

**Ikke gjort ennå:**
- Kaldtest av de tre nye datatypene og av kryss-type-søk (kun anmodningsvedtak-delen er kaldtestet så langt)
- Undersøke om «ukjent»-kategorien for representantforslag (14%, mest status=behandlet uten synlig vedtak) kan reduseres ytterligere — foreløpig ikke prioritert gitt at forklaringsgraden allerede er høy
- Levere partimeninger/stemmegivning som eget søkbart lag — brukeren ba eksplisitt om å vente med dette

**Vurdert og forkastet:** Voteringsendepunktet (`/eksport/voteringer?sakid=X`) som kilde til representantforslag-utfall — testet grundig på 104 saker, forkastet fordi `vedtatt: true` ikke skiller forslagets skjebne fra avvisningens vedtaksstatus.

## 2026-09-10 – Omdøping

**Funn:** Ikke et funn, men en bevisst navneendring — fra `aid-anmodningsvedtak` til `aid-anmodningsvedtak-fra2013`, for å gjøre datadekningens startpunkt synlig i navnet uten å bake inn et sluttår som blir feil ved neste sesjonsoppdatering (mellomforslag som inkluderte sluttår, f.eks. `-2013til2026`, ble forkastet av nettopp denne grunnen).

**Endring:** `name`-felt i SKILL.md, mappenavn, og referanse i denne loggens tittel oppdatert. Ingen funksjonell endring i skript eller data.

**Basert på:** Brukerens eksplisitte ønske, 2026-09-10.

**Ikke gjort ennå:** Brukeren må selv slette den tidligere installerte `aid-anmodningsvedtak` (annet navn = ny skill for claude.ai, ikke en oppdatering av den gamle).

**Vurdert og forkastet:** Navn med eksplisitt sluttår (`aid-anmodningsvedtak-2013til2026`, `aid-sesjon2013-14-til-siste`) — forkastet fordi sluttåret uansett må oppdateres i SKILL.md-teksten ved hver sesjon, og et navn som også må vedlikeholdes er en unødvendig ekstra feilkilde. Endelig navn holder kun startåret, som er stabilt.

## 2026-09-10 – Kaldtest runde 1: stikkord-bloat, manglende lenke, upresist "viser X"

**Funn:** Kjørte 5 testspørsmål med kjent fasit (se forrige runde for spørsmålsteksten). Resultat: 2 av 5 helt uten anmerkning (test 2, test 4), 3 med reelle funn.

1. **Test 1 (Modus B, mindre alvorlig):** Korrekt innhold, men lenken til vedtaket manglet i svaret — brukeren måtte etterspørre den. Skriptet leverer alltid `vedtak_url`; problemet lå i hvordan Claude formulerte svaret, ikke i dataene.
2. **Test 3 (Modus B, reell unøyaktighet):** Svaret sa «viser 50, 43 til finnes ikke vist» (93 totalt), men listet faktisk bare opp 10 vedtak (én dags klynge). Tallene stemte ikke overens — Claude valgte selv å korte ytterligere ned for lesbarhet, men oppdaterte ikke det oppgitte tallet til å reflektere det faktiske utvalget.
3. **Test 5 (strukturell datafeil, alvorlig):** Fritekstsøk på «trygd», «sykepenger», «dagpenger», «uføre» og «arbeidsavklaringspenger» i sesjon 2013-2014 ga alle nøyaktig de samme 7 falske treffene, alle fra sak_id 59868 («Tilleggsbevilgninger og omprioriteringer i statsbudsjettet 2014»). Årsak: stikkord tildeles på SAK-nivå i Stortingets data, og denne saken har 297 stikkord som dekker hele budsjettproposisjonen — ingen av de 7 vedtakene handlet faktisk om trygd. Bekreftet systematisk ved fordelingsanalyse: median 3 stikkord/sak, men 79 av 1364 saker har over 20 (62 av disse er budsjettsaker).

**Endring:**
1. + 2. SKILL.md: lagt til eksplisitte presisjonskrav — alltid inkluder `vedtak_url`, og hold "viser X" synkronisert med hva som faktisk listes opp i svaret, selv når Claude selv velger å korte ytterligere ned.
3. `scripts/sok_anmodningsvedtak.py`: innført `STIKKORD_PÅLITELIG_GRENSE = 20`. Stikkord fra saker over denne grensen ekskluderes fra både `treffer()`-matching og `relevans_niva()`-rangering — treff må da komme fra tittel eller tekst direkte. Verifisert at fiksen fjerner alle 7 falske treff fra sak 59868 på alle fem testordene, uten å fjerne reelle treff andre steder.

**Basert på:** Brukerens rapporterte kaldtestresultater, 2026-09-10.

**Ikke gjort ennå:**
- Kaldtest runde 2 — bør inkludere et nytt kontrollspørsmål som spesifikt re-tester «trygd i 2013-2014» mot ny fasit (nå 1 treff, sak 59870 — fortsatt en svak substrengs-treff via «Folketrygdloven» i en 11-ords stikkordliste, ikke en ekte trygdesak. Vurder om dette er akseptabelt eller bør strammes ytterligere).
- Vurdere om samme stikkord-bloat-mønster finnes for `emne`-feltet (foreløpig antatt nei, siden emne typisk er 1-3 ord selv for store saker — ikke verifisert systematisk).

**Vurdert og forkastet:** Å prompte brukeren om å presisere søket *før* et bredt fritekstsøk kjøres (brukerens eget forslag). Forkastet fordi rotårsaken var en datakvalitetsfeil (sak-nivå stikkord-bloat), ikke at søket i seg selv var for bredt — presisering ville skjult symptomet uten å fikse at samme feilkilde ville dukket opp igjen på et annet bredt søkeord. Beholder «be om presisering» som en mulig fremtidig UX-forbedring for øvrig, men det var ikke riktig fiks for akkurat dette funnet.

## 2026-09-10 – Dynamisk sesjon, adaptiv visning, relevanssortering

**Funn:** Brukeren påpekte tre svakheter i førsteversjonen før kaldtest: (1) SKILL.md hardkodet "inneværende sesjon er 2025-2026" som tekst — ville blitt feil når ny sesjon åpner ca. 1. oktober 2026, tre uker frem i tid; (2) `--limit 50` med full tekst per vedtak er uleselig ved brede søk; (3) datosortering av filtrert treffliste var i realiteten *stigende* (arvet fra hvordan `data/`-filen ble bygget), som kombinert med `--limit` aktivt skjulte alle nyere treff ved brede søk — testet med søkeordet «barn» (705 treff): topp-50 med daværende sortering viste utelukkende vedtak fra 2013-2014, null fra de siste ti årene.

**Endring:** (a) Lagt til `resolve_sesjon()` som oversetter `inneværende`/`forrige` til faktisk sesjon-id fra dagens dato (sesjon = 1. okt-30. sep), og et eksplisitt varsel når en etterspurt sesjon ikke finnes i indeksen ennå (skiller «ikke oppdatert» fra «ingen treff»). (b) Adaptiv visning: ≤5 treff = full tekst, 6-20 = forkortet, >20 = kompakt liste. (c) Sortering: relevans (tittel > stikkord > tekst) med nyeste dato som sekundærnøkkel ved fritekstsøk; ren datosortering synkende ved rene filtersøk.

**Basert på:** Bygge-samtale 2026-09-10, direkte respons på brukerens spørsmål om sårbar hardkoding og sortering.

**Ikke gjort ennå:** Kaldtest i frittstående samtale — bør nå inkludere et testtilfelle som spesifikt sjekker at «inneværende»/«forrige» løses riktig, og et bredt søk som sjekker at nyere vedtak faktisk kommer med.

## 2026-09-10 – Førstebygging

**Funn:** Ingen tidligere skill dekket anmodningsvedtak. Bygget fra bunn basert på data.stortinget.no sitt åpne API. To vesentlige datakvalitetsfunn underveis:
1. Stikkord-feltet sluttet å bli registrert av Stortinget fra og med sesjon 2021-2022, og er nær fraværende 2024-2026 — strukturelt brudd, ikke tilfeldig manglende data (bekreftet ved sesjonsvis fordeling: 0 mangler t.o.m. 2020-2021, deretter stigende til 486/486 i 2025-2026).
2. Komité-tildeling på budsjettvedtak ble først mistenkt som en feilkilde (hovedsak fikk «Finanskomiteen» selv når enkeltvedtak dreide seg om andre fagområder), men brukeren vurderte dette som meningsfull informasjon (Finanskomiteen ⇒ typisk budsjettforlik, fagkomité ⇒ typisk ordinær budsjettbehandling), ikke en feil å rette.

**Endring:** Bygget søkbar indeks over 4070 ANMOD-vedtak (sesjon 2013-2014 t.o.m. 2025-2026), beriket med komite/emne/stikkord/henvisning fra sak-endepunktet (1364 unike sak-oppslag). Søkeskript (`scripts/sok_anmodningsvedtak.py`) med filtrering på query/sesjon/komite/emne/id, i stedet for at Claude leser hele datasettet direkte — datamengden (5,3 MB) er for stor til pålitelig manuell gjennomgang.

**Basert på:** Bygge-samtale 2026-09-10 (sesjon-for-sesjon verifisering av data.stortinget.no, pilot på 37 saker i sesjon 2013-2014 før full berikelse av alle 1364 saker).

**Ikke gjort ennå:**
- Kaldtest i frittstående samtale
- Automatisert oppdateringsskript (i dag: manuell prosedyre i `references/oppdatering.md`)
- Oppfølgingsstatus (utkvittert/ikke avsluttet) — bevisst utelatt i denne omgang
- Skriftlige spørsmål og interpellasjoner — bevisst utsatt til anmodningsvedtak er godt utprøvd
- Testsett med kjent fasit for kaldtesting

**Vurdert og forkastet:** Splitting av data i mindre referansefiler per sesjon/komité (regelverksskill-mønsteret) — forkastet fordi anmodningsvedtak mangler den hierarkiske strukturen paragrafer har, og tverrgående søk («alt om uføretrygd») ville krevd at Claude uansett åpnet mange filer. Søkeskript med filtrering ble valgt i stedet.
