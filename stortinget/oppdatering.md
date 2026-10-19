# Oppdatering av Stortinget-indeksen

# Oppdatering av Stortinget-indeksen

**Merk: skillen er delt i to periode-pakker** (`aid-stortinget-2013-2021` og `aid-stortinget-fra2021`) fordi samlet data oversteg claude.ai sin 30 MB-grense for skill-pakker. Nye sesjoner skal ALLTID legges til i `aid-stortinget-fra2021` (perioden vokser videre) — aldri i `aid-stortinget-2013-2021`, som er en avsluttet, historisk periode (Solberg-regjeringen). Se punkt 5 under for hvordan periodegrensen ble satt og hvorfor.

Fremgangsmåte for å hente en ny sesjon (f.eks. når 2026-2027 åpner i oktober) eller friske opp inneværende sesjon.

## 1. Bekreft riktig sesjon-ID

**Bruk `curl` direkte, ikke nettoppslagsverktøy** — sistnevnte har vist seg å returnere feilcachet innhold uten feilmelding.

```bash
curl -s "https://data.stortinget.no/eksport/sesjoner" -o sesjoner.xml
```
Sjekk `<innevaerende_sesjon><id>`.

## 2. Hent rådata for alle fire datatyper

**KRITISK: bruk `&status=alle` på de tre `sporsmal`-endepunktene** (`skriftligesporsmal`, `interpellasjoner`, `sporretimesporsmal`). Uten denne parameteren returnerer disse tre endepunktene **kun poster med status `besvart`** — stille, uten feilmelding eller advarsel. Bekreftet gjennom direkte test 2026-09-16: for sesjon 2025-2026 alene manglet 162 poster (128 `til_behandling`, 31 `trukket`, 3 `bortfalt`) fordi standardkallet ble brukt. Dette ble første gang oppdaget da brukeren la merke til at en interpellasjon fra Kjersti Toppe (fremmet 4/8-2026, synlig på stortinget.no) ikke fantes i indeksen — ikke fordi data.stortinget.no hang etter stortinget.no i tid, men fordi selve spørringen filtrerte den bort.

`stortingsvedtak`- og `saker`-endepunktene har **ikke** dette problemet — testet og bekreftet identisk postantall med og uten `&status=alle` (saker: 666/666, stortingsvedtak: 1166/1166). Legg parameteren til likevel av konsistenshensyn, men det er ikke kritisk der.

```bash
for endepunkt in stortingsvedtak saker; do
  curl -s "https://data.stortinget.no/eksport/${endepunkt}?sesjonid=SESJON-ID&status=alle" -o "${endepunkt}_SESJON-ID.xml"
done
for endepunkt in skriftligesporsmal interpellasjoner sporretimesporsmal; do
  curl -s "https://data.stortinget.no/eksport/${endepunkt}?sesjonid=SESJON-ID&status=alle" -o "${endepunkt}_SESJON-ID.xml"
done
```

**Verifiser** at `<sesjon_id>` i responsen matcher det du ba om, og at datoer ligger i sesjonens tidsrom (normalt okt-sept), før du bruker dataene videre.

**Håndtering av ubesvarte spørsmål/interpellasjoner i `sporsmal.json`:**
- `status`-feltet kan nå være `besvart`, `til_behandling`, `trukket` eller `bortfalt` (representantforslag/saker har fra før `behandlet`, `til_behandling`, `mottatt`, `trukket`, `varslet` — allerede dekket, ingen endring nødvendig der).
- `besvart_dato`, `sendt_dato` OG `datert_dato` kan **hver for seg** være `0001-01-01T00:00:00Z` (sentinel, ikke reell dato) avhengig av hvor i prosessen posten står — f.eks. har `trukket`-poster ofte sentinel på både `besvart_dato` og `sendt_dato`, med reell verdi kun i `datert_dato`. Ikke bruk `sendt_dato or datert_dato` (en sentinel-streng er "truthy" i Python og vinner feilaktig over en reell fallback-verdi) — sjekk hvert felt individuelt mot sentinelen og ta første reelle: `next((d for d in (besvart_dato, sendt_dato, datert_dato) if d and not d.startswith('0001-01-01')), None)`. Denne feilen oppstod og ble rettet i samme runde (34 poster fikk `0001-01-01` liggende i `dato`-feltet før det ble oppdaget og fikset).
- For skriftlige spørsmål og spørretimespørsmål er `tittel` alltid fylt ut (inneholder spørsmålsteksten) uansett status. For **interpellasjoner** er `tittel` derimot tom (`None`) helt til behandlingen er formelt fastsatt — konstruer da en midlertidig tittel av typen `"Interpellasjon fra {fra_navn} ({fra_parti}) til {til_minister_tittel}"` og sett `tittel_midlertidig: true` på posten, slik at den er tydelig merket som ikke-offisiell. Søkeskriptet viser markeringen automatisk i treff.
- Historisk backfill (sesjon 2013-2014 t.o.m. 2024-2025) er **ikke** gjort — kun inneværende sesjon er rettet per 2026-09-16. Gamle sesjoner kan fortsatt mangle `trukket`/`bortfalt`-poster som aldri ble besvart (de vil aldri dukke opp av seg selv siden sesjonen er avsluttet). Lavere prioritet enn løpende dekning, men bør gjøres for fullstendighet — se endringslogg.

**Bruk ElementTree, ikke regex, for parsing.** Regex på nøstet XML feiler stille — et representantforslag inneholder en nøstet `<sak>`-tag som brøt en regex-basert utpakking (104 reelle poster ble til 49 pga. feil matching). Rot-elementets liste-tag heter `saker_liste` for saker, `sporsmal_liste` for spørsmål/interpellasjoner/spørretime, `stortingsvedtak_liste` for vedtak — ikke anta navnet, sjekk med `root.findall(list(root))` ved usikkerhet.

**Batching:** over ~300 kall i én shell-kjøring har truffet execution timeout i dette miljøet. Del opp med `timeout 280 ./skript.sh` i flere omganger — skript bør være gjenopptakbare (`if [ -s "$fname" ]; then continue; fi`).

## 3. Parse og bygg de tre datafilene

Kjør `bygg_stortinget_data.py`-mønsteret (se skillens byggehistorikk i endringslogg for full kildekode-logikk):

**Anmodningsvedtak:** filtrer `stortingsvedtak` på `stortingsvedtak_type/id == ANMOD`, berik med sak-oppslag (komite/emne/stikkord/henvisning) — se egen seksjon under, dette er den eneste datatypen som krever per-sak API-kall.

**Spørsmål (skriftlig/interpellasjon/spørretime):** samme XML-skjema for alle tre («likt format for de tre forespørslene» ifølge Stortingets egen dokumentasjon). `tittel`-feltet inneholder allerede full spørsmålstekst — ingen per-post-berikelse nødvendig. URL bygges fra `legacy_id` (ikke `id` — Stortinget byttet ID-skjema i 2024, offentlige URL-er bruker fortsatt det gamle):
- Skriftlig: `https://www.stortinget.no/no/Saker-og-publikasjoner/Sporsmal/Skriftlige-sporsmal-og-svar/Skriftlig-sporsmal/?qnid={legacy_id}`
- Interpellasjon: `https://www.stortinget.no/no/Saker-og-publikasjoner/Sporsmal/Interpellasjoner/Interpellasjon/?qnid={legacy_id}`
- Spørretime: `https://www.stortinget.no/no/Saker-og-publikasjoner/Sporsmal/Sporretimesporsmal/et-sporretimesporsmal/?qnid={legacy_id}`

Selve **svarteksten** er ikke i denne listen — krever `enkeltsporsmal?sporsmalid={id}` (den NYE id-en, ikke legacy_id) per post. Ikke forhåndshent dette i bulk (39 000+ poster ville vært svært mange kall) — se SKILL.md for live-oppslag-mønsteret.

**Representantforslag:** hent fra `saker`-endepunktet (ikke et eget endepunkt), filtrer `dokumentgruppe == representantforslag`. `sak_url` bygges direkte: `https://www.stortinget.no/no/Saker-og-publikasjoner/Saker/Sak/?p={sak_id}`.

## 4. Utfall for representantforslag — kritisk fremgangsmåte

Ikke bruk voteringsendepunktet (`/eksport/voteringer?sakid=X`) — testet og forkastet. `vedtatt: true` på en votering betyr ofte at komiteens innstilling om å **avvise** forslaget ble vedtatt, ikke at forslaget selv gikk gjennom. Skiller ikke reelt utfall fra formalitet.

**Riktig metode (validert, 99% dekning på testsesjon):**
1. Bygg ett samlet oppslag `sak_id → [(sesjon, vedtakstype, tekst), ...]` fra de rå `stortingsvedtak`-filene for **alle** sesjoner (ikke bare anmodningsvedtak-filtrert) — dette krever ingen nye API-kall, bare at rådataene fra steg 2 ikke kastes.
2. For hvert representantforslag: slå opp **alle** vedtak knyttet til sak_id, uansett hvilken sesjon de kom i. Et forslag fremmet sent i en sesjon avgjøres ofte i den påfølgende (`behandlet_sesjon_id` kan avvike fra sesjonen det ble fremmet i).
3. Klassifiser: `ANMOD`-type → «vedtatt (anmodning)». Vedtakstekst inneholder en avvisningsformel → «avvist». Annet vedtak funnet → «annet» (vis teksten rått). Ingen vedtak funnet i noen sesjon → «ukjent».

**Avvisningsformler — bekreftet nødvendige varianter** (representantforslag kan skrives på bokmål eller nynorsk):
`vedlegges protokollen`, `lagt ved møteboka`, `lagt ved protokollen`, `å leggja ved`, `å legge ved`, `vedtas ikke`, `vedtas ikkje`, `blir ikke vedtatt`, `bifalles ikke`, `bifalles ikkje`

Denne listen ble bygget iterativt ved å inspisere «annet»-restkategorien etter hver runde — start med de første to-tre, kjør, sjekk restkategorien for mønstre, gjenta. Stopp når restkategorien slutter å krympe merkbart (nådd ved ~2,5% i denne bygningen).

## 5. Størrelsesbudsjett — 30 MB uncompressed er en hard grense

claude.ai avviser skill-pakker der uncompressed innhold overstiger 30 MB. Ukomprimert bygde vi 49,4 MB (se endringslogg 2026-09-10, «Komprimering under 30 MB-grensen») — gikk under ved å:
- Ikke bundle `sporretime_sporsmal` (identisk skjema, men 8,2 MB — vurder om den fortsatt bør holdes utenfor, eller flyttes til egen skill, hvis den legges til igjen)
- Fjerne `url` fra `sporsmal`-poster og rekonstruere fra `type`(kort kode)+`legacy_id` i skriptet
- Fjerne `til_minister_tittel` og slå opp via en liten kodetabell i skriptet i stedet
- Slå sammen `sendt_dato`/`besvart_dato`/`datert_dato` til ett `dato`-felt
- Kompakt JSON (`separators=(',',':')`) i stedet for `indent=2` i alle tre filer

**Ved neste utvidelse:** sjekk total pakkestørrelse (`du -sh data/`) FØR pakking, ikke etter — regn med at hver ny sesjon legger til noen hundre KB per datatype. Bruk `json.dumps(..., separators=(',',':'))` fra start.

## 6. Kvalitetssjekk før publisering

- Ingen duplikate id-er per datatype
- Stikkprøve: sammenlign 2-3 postar sin tekst mot originalens rå XML
- For representantforslag: sjekk utfallsfordelingen er rimelig (avvist bør dominere over vedtatt i et flertallsdemokrati med normal opposisjonsaktivitet — hvis vedtatt/annet dominerer, er avvisningsformel-listen sannsynligvis ufullstendig)
- Sjekk om stikkord-bruddet (se SKILL.md) fortsatt gjelder for anmodningsvedtak

## Kjente feilkilder fra tidligere kjøringer

- Regex-basert XML-parsing feilet stille på nøstet struktur (se punkt 2)
- Ett av flere hundre sak-kall kan feile transient — bygg inn retry (3 forsøk)
- URL-er for spørsmål bruker `legacy_id`, ikke `id` — lett å bytte om
