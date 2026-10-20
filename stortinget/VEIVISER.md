# Stortinget: søkbar indeks

Fire typer saker fra [data.stortinget.no](https://data.stortinget.no), for sesjon 2013-2014 til og med inneværende sesjon. Dekker alle departementers områder, ikke bare AID. Dataene er offentlige og oppdateres automatisk hver natt (`.github/workflows/stortinget-oppdater.yml`). Sist kjørte oppdatering står i `siste-oppdatering.json`, og nye saker og nye svar fra den kjøringen i `siste-endringer.json`.

| Datatype | Mappe | Hva det er |
|---|---|---|
| `anmodningsvedtak` | `data/anmodningsvedtak/` | Vedtak der Stortinget ber regjeringen om noe |
| `sporsmal` | `data/sporsmal/` | Skriftlige spørsmål, interpellasjoner og spørretimespørsmål (tre undertyper). Alle statuser (besvart, til_behandling, trukket, bortfalt) fra sesjon 2021-2022, se begrensninger |
| `representantforslag` | `data/representantforslag/` | Forslag fremmet av representanter, med utfall der det er kjent |

Hver mappe har én fil per sesjon, for eksempel `data/sporsmal/2025-2026.json`. Hele indeksen er rundt 31 MB, så hent bare det du trenger.

## Slik søker du

Søk alltid med skriptet. Svar ikke på spørsmål om disse datatypene fra generell kunnskap eller nettsøk. Nettsøk gir usystematiske og ufullstendige treff, og en kaldtest viste at spørsmål av typen «har parti X foreslått Y» ble besvart med nettsøk i stedet for med indeksen.

1. Hent mappen `stortinget/` med sparse checkout, som tar med alle sesjonene:

   ```bash
   git clone --depth 1 --filter=blob:none --sparse https://github.com/tarjeiha/allover
   cd allover && git sparse-checkout set stortinget
   ```

   Hvis spørsmålet gjelder én sesjon, kan du i stedet hente bare skriptene (`scripts/felles.py`, `scripts/sok_stortinget.py`) og filene for sesjonen via `https://raw.githubusercontent.com/tarjeiha/allover/main/stortinget/…`, i samme mappestruktur.

2. Kjør:

   ```bash
   python3 stortinget/scripts/sok_stortinget.py --query "SØKEORD" [--datatype anmodningsvedtak|sporsmal|representantforslag] [--sesjon inneværende|forrige|ÅÅÅÅ-ÅÅÅÅ] [flere filtre]
   ```

Uten `--datatype` søkes alle tre typer. Gjenta `--datatype` for å velge flere.

Felles filtre: `--query`, `--sesjon` (bruk `inneværende` eller `forrige` i stedet for å anta et årstall, for sesjonen løper 1. oktober til 30. september), `--emne`, `--id`, `--limit` (standard 50), `--format kort|json`.

Filtre per type:
- `--komite`: anmodningsvedtak og representantforslag
- `--minister`: sporsmal (del av statsrådens tittel)
- `--sporsmalstype skriftlig_sporsmal|interpellasjon|sporretime_sporsmal`
- `--status besvart|til_behandling|trukket|bortfalt`: sporsmal
- `--parti`: representantforslag (eksakt partikode)
- `--utfall "vedtatt (anmodning)"|avvist|annet|ukjent`: representantforslag

Visningen tilpasses antall treff: opptil 5 gir full tekst, 6–20 forkortet, flere enn 20 kompakt. Fritekstsøk sorteres etter relevans og deretter nyeste, andre søk nyeste først.

Matchingen er ordbasert OG: alle ordene må finnes et sted i de søkte feltene, uansett rekkefølge. Vanlige fagord i AIDs område utvides med synonymer og nynorske former (AAP gir også arbeidsavklaringspenger, sykepenger også sjukepengar), se `SYNONYMER` i `scripts/sok_stortinget.py`. Et sammensatt ord som ikke finnes i noen post, deles i to ledd, og skriptet sier fra om det («pårørendestøtte» blir «pårørende» + «støtte»). Et sammensatt ord som finnes, deles ikke, så søk også på leddene hver for seg når dekningen betyr noe.

## Krav til svaret

Bekreftet nødvendig gjennom kaldtester.

- **Ta med lenken** til hvert treff du presenterer, også når du grupperer mange treff under temaer. Enten list alle treff med lenke, eller gi minst én lenke per tema. Ikke gi en oppsummering helt uten lenker.
- **«Viser X» må stemme** med det du faktisk lister opp.
- **Lever det du sier du skal levere.** Ikke avslutt med et tilbud om en full liste uten å vise den, hvis spørsmålet var bredt nok til at listen er naturlig.
- **Over 20 treff:** ikke velg ut treff fra den kompakte visningen. Titlene er kuttet ved 90 tegn, og et sentralt treff kan se perifert ut. Rapporter antall treff og spør hvordan søket skal snevres inn, eller hent `--format json` med fulltekst før du velger.
- **Unngå `--minister` og `--komite` som første innsnevring** på tverrgående velferdstemaer (sykefravær, pårørende, uføre, familieytelser). Samme sak kan være stilt til flere statsråder. Bruk flere og mer presise søkeord i stedet.
- **Ikke spekuler om prosedyre** utover det dataene og denne veiviseren viser, for eksempel når en sesjon teknisk avsluttes. Er du usikker, si det.
- **Skriptet varsler om en sesjon nyere enn sist kjente** (typisk rett etter at en ny sesjon åpner 1. oktober): da er dataene ikke oppdatert ennå. Kjør oppdateringen, se `oppdatering.md`.

## Kjente begrensninger

**Anmodningsvedtak:** Stikkord mangler fra sesjon 2021-2022 og er nær fraværende i 2024-2026, så fritekstsøk er svakere i nyere sesjoner enn i 2013-2021. Emne mangler på rundt 40 prosent, komité på rundt 3,4 prosent (redegjørelser). Komité på budsjettvedtak viser budsjettforlik (Finanskomiteen) eller ordinær fagbehandling, ikke en feil. Oppfølgingsstatus er ikke dekket. Stikkord brukes ikke i søket for saker med over 20 stikkord.

**Spørsmål:** Bare spørsmålsteksten ligger i indeksen, ikke statsrådens svar. Hent svaret direkte bare når brukeren spør om et konkret svar: `https://data.stortinget.no/eksport/enkeltsporsmal?sporsmalid=ID` (feltet `id`, ikke `legacy_id`). Ubesvarte poster (`til_behandling`, `trukket`, `bortfalt`) er med for sesjon 2021-2022 og senere. For 2013-2014 til 2020-2021 er bare besvarte spørsmål med. Interpellasjoner uten fastsatt tittel har en konstruert tittel merket `tittel_midlertidig: true`. Presenter den ikke som Stortingets offisielle tittel.

**Representantforslag:** Utfallet er beregnet, ikke hentet direkte. Rundt 83 prosent er vedtatt eller avvist, rundt 2,5 prosent «annet» (vis `utfall_tekst` rått) og rundt 15 prosent «ukjent», mest forslag som ikke er ferdigbehandlet.

## Oppdatering

Nattjobben kjører `scripts/oppdater_inkrementell.py`: den legger til nye poster og oppdaterer status på eksisterende (spørsmål som er besvart, forslag som har fått utfall, også på tvers av sesjoner). Jobben er idempotent og kan kjøres for hånd under Actions («Oppdater Stortinget»). `scripts/backfill_sesjon.py` er en sjelden engangsjobb for avsluttede sesjoner. Fremgangsmåte for en helt ny sesjon og kvalitetskontroll står i `oppdatering.md`. Endringer i indeksen er logget i `endringslogg.md`.
