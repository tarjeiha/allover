# Statsbudsjettet – veiviser

Denne mappen har statsbudsjettdokumenter for Arbeids- og inkluderingsdepartementet (AID), delt opp slik at du kan gå rett til et kapittel eller en post. Dokumentene er offentlige og hentet fra regjeringen.no. Word- og Excel-filene lastes opp manuelt, fordi regjeringen.no ikke slipper til automatisk henting.

## Kjente feller

- **Prop. 1 S er regjeringens forslag, ikke vedtatt budsjett.** Stortinget vedtar budsjettet i desember, etter budsjettforliket og innstillingene fra komiteene. Tilleggsproposisjoner (Prop. 1 S Tillegg) kan endre forslaget. Si alltid at tallene er forslag, og fra hvilket dokument.
- **Ulike enheter.** Tabellene i proposisjonen er i 1 000 kroner. `gul-bok-bevilgninger.tsv` er i kroner.
- **Tall for alle departementer finner du raskest i `gul-bok-bevilgninger.tsv`.** `gul-bok/forslag-til-vedtak.md` er stor (alle departementers vedtaksforslag), så les den bare når du trenger vedtaksteksten.
- **Anslag er anslag.** Tall for 2026 og 2027 i Nasjonalbudsjettet er Finansdepartementets anslag fra oktober 2026. Si det når du bruker dem.
- **Nynorsk.** AIDs proposisjon er skrevet på nynorsk. Siter på nynorsk, men svar på brukerens språk.
- **Overslagsløyvingar.** Poster merket «overslagsløyving» (f.eks. dagpenger) er anslag. Utgiftene følger regelverket, ikke beløpet.
- **Kapittelnumrene sier hva slags kapittel det er.** Kap. 600–699 er ordinære utgiftskapitler, 2470 er Statens pensjonskasse, 2541–2686 er folketrygden, 3000-kapitlene er inntekter som hører til 600-kapitlene, og 5000-kapitlene er andre inntekter og utgifter (f.eks. 5470 Statens pensjonskasse og 5705 Refusjon av dagpengar). Se programkategori-filene for inndelingen.

## Stortingets vedtak (`budsjett/ÅR/stortinget/`)

Hentes automatisk fra data.stortinget.no hver mandag (`verktoy/stortinget_budsjett.py`). Gjelder alle departementer, fra og med sesjonen 2021–2022. For 2021 er bare ny saldering med. Alle beløp gjelder budsjettåret i mappenavnet.

| Fil | Innhold |
|---|---|
| `vedtak.tsv` | Beløp per kapittel og post i komiteens tilråding, i kroner. Kolonnen `fase` er `saldert` (vedtatt budsjett i desember, fagkomiteenes budsjettinnstillinger), `rnb` (revidert nasjonalbudsjett i juni), `endring` (andre endringsproposisjoner i budsjettåret) eller `nysaldering` (høsten i budsjettåret). For endringer er `belop` beløpet etter vedtaket, `endring` er endringen og `fra` beløpet før. |
| `rammevedtak.tsv` | Rammevedtakene i Innst. 2 S: sum per rammeområde, i kroner. |
| `partiforslag.tsv` | Sammenligningstabellene i fagkomiteenes budsjettinnstillinger, i tusen kroner: Prop. 1 S og hvert partis forslag per post. Bare poster der minst ett parti foreslår noe annet enn regjeringen er med. `flertall=ja` markerer partiene bak tilrådingen, altså budsjettforliket. `endring` er forliket eller partiets forslag minus Prop. 1 S. |
| `anmodningsvedtak.tsv` | Vedtak Stortinget har registrert som anmodningsvedtak i budsjettsakene, med vedtaksnummer, hvem som fremmet forslaget og vedtaksteksten. Anmodningsvedtakene fra budsjettforliket ligger under Innst. 2 S. |
| `kilder.tsv` | Innstillingene som er brukt, med lenke, saker og om tilrådingen ble vedtatt ved votering. |

Feller:

- **Tilråding, ikke vedtakstekst.** Beløpene er lest fra komiteens tilråding. `kilder.tsv` viser om tilrådingen ble vedtatt. Står det `nei` eller `ukjent`, sjekk vedtaket på stortinget.no.
- **Budsjettforliket per post** finnes i `partiforslag.tsv` (flertallets kolonne) eller som forskjellen mellom `saldert` i `vedtak.tsv` og Prop. 1 S. Selve avtaleteksten ligger bare som PDF-vedlegg til Innst. 2 S.
- **Feil i kildene.** Noen innstillinger oppgir «fra kr … til kr …» som ikke stemmer med endringen. Da står det i `merknad`, og `belop` er tallet innstillingen oppgir.
- **Post 24 Driftsresultat** for forvaltningsbedrifter (f.eks. kap. 2470) har underposter uten eget beløp. De er ikke med.
- **Saldert budsjett for AIDs kapitler** er kontrollert mot kolonnen «Saldert budsjett» i neste års Prop. 1 S for 2022–2025, uten avvik.

<!-- AUTO-START budsjettår: genereres av verktoy/budsjett_innboks.py, ikke rediger for hånd -->
## Budsjettår i basen

Hvert budsjettår har sin egen mappe. Tall (datagrunnlaget) kan gå lenger tilbake enn tekst (proposisjonene). Oppgi alltid budsjettår og dokument i svaret, og husk at Prop. 1 S er forslag, ikke vedtatt budsjett.

- **2027:** Prop. 1 S AID (`budsjett/2027/prop-1-s-aid/`), Gul bok (`budsjett/2027/gul-bok/`), Nasjonalbudsjettet (`budsjett/2027/nasjonalbudsjettet/`), datagrunnlag (`budsjett/2027/gul-bok-bevilgninger.tsv`)
- **2026:** Prop. 1 S AID (`budsjett/2026/prop-1-s-aid/`), Stortingets vedtak (`budsjett/2026/stortinget/`), datagrunnlag (`budsjett/2026/gul-bok-bevilgninger.tsv`)
- **2025:** Prop. 1 S AID (`budsjett/2025/prop-1-s-aid/`), Stortingets vedtak (`budsjett/2025/stortinget/`), datagrunnlag (`budsjett/2025/gul-bok-bevilgninger.tsv`)
- **2024:** Prop. 1 S AID (`budsjett/2024/prop-1-s-aid/`), Stortingets vedtak (`budsjett/2024/stortinget/`), datagrunnlag (`budsjett/2024/gul-bok-bevilgninger.tsv`)
- **2023:** Prop. 1 S AID (`budsjett/2023/prop-1-s-aid/`), Gul bok (`budsjett/2023/gul-bok/`), Stortingets vedtak (`budsjett/2023/stortinget/`)
- **2022:** Prop. 1 S AID (`budsjett/2022/prop-1-s-aid/`), Prop. 1 S Tillegg 1 (alle departementer) (`budsjett/2022/prop-1-s-tillegg-1/`), Gul bok (`budsjett/2022/gul-bok/`), Stortingets vedtak (`budsjett/2022/stortinget/`)
- **2021:** Prop. 1 S AID (`budsjett/2021/prop-1-s-aid/`), Stortingets vedtak (`budsjett/2021/stortinget/`)
<!-- AUTO-SLUTT budsjettår -->

## Budsjettår 2027

| Dokument | Sti | Innhold |
|---|---|---|
| Prop. 1 S (2026–2027) AID | `budsjett/2027/prop-1-s-aid/` | Hele proposisjonen, én fil per kapittel |
| Prop. 1 S (2026–2027) Gul bok | `budsjett/2027/gul-bok/` | Hele statsbudsjettet: hovedtall, oljepengebruk, utgiftsvekst, budsjettkonsekvenser 2028–2030, statens lånebehov, vedlegg. Én fil per delkapittel |
| Meld. St. 1 (2026–2027) Nasjonalbudsjettet | `budsjett/2027/nasjonalbudsjettet/` | Økonomiske utsikter og anslag (arbeidsmarked, priser, lønn), budsjettpolitikk, velferd og fordeling. Én fil per delkapittel. `vedlegg-05-…` har historiske tabeller og detaljerte anslagstall |
| Nasjonalbudsjettet, figurdata | `budsjett/2027/nasjonalbudsjettet/figurdata/` | Tallene bak 148 figurer, én TSV per figur. `innhold.tsv` lister figurtitlene |
| Gul bok, datagrunnlag | `budsjett/2027/gul-bok-bevilgninger.tsv` | Alle departementers bevilgningsforslag per kapittel og post (kroner). Kolonner: gdep_nr, avs_nr, gdep_navn, avs_navn, fdep_nr, fdep_navn, omr_nr, kat_nr, omr_navn, kat_navn, kap_nr, post_nr, kap_navn, post_navn, stikkord, beløp |

### Slik finner du fram i Prop. 1 S AID

- Vet du kapittelet, gå rett til `kap-NNNN.md` (fire sifre, f.eks. `kap-2541.md` for dagpenger).
- `poster.tsv` viser hvilken fil hver post står i.
- Første del (`del-1-*.md`) har mål, profil og satsinger, utviklingstrekk, oppmodingsvedtak og oversiktstabeller.
- `programkategori-*.md` har innledningen til hver programkategori, med samlet oversikt.
- `tema-*.md` har særlige temaer (bl.a. likestilling, samfunnssikkerhet, fordrevne fra Ukraina).
- `forslag-til-vedtak.md` har vedtaksforslagene og fullmaktene.

Filer i proposisjonen:

| Fil | Tittel |
|---|---|
| `budsjettforslag-innleiing.md` | Arbeids- og inkluderingsdepartementets budsjettforslag for 2027 |
| `del-1-01-mal-for-arbeids-inkluderings-og-velferdspolitikken.md` | Mål for arbeids-, inkluderings- og velferdspolitikken |
| `del-1-02-profil-og-satsingsomrade.md` | Profil og satsingsområde |
| `del-1-03-sentrale-utviklingstrekk.md` | Sentrale utviklingstrekk |
| `del-1-04-oppmodingsvedtak.md` | Oppmodingsvedtak |
| `del-1-05-oversiktstabellar.md` | Oversiktstabellar |
| `forslag-til-vedtak.md` |  |
| `kap-0600.md` | Kap. 600 Arbeids- og inkluderingsdepartementet |
| `kap-0601.md` | Kap. 601 Utgreiingsverksemd, forsking m.m. |
| `kap-0604.md` | Kap. 604 Utviklingstiltak i arbeids- og velferdsforvaltninga |
| `kap-0605.md` | Kap. 605 Arbeids- og velferdsetaten |
| `kap-0606.md` | Kap. 606 Trygderetten |
| `kap-0611.md` | Kap. 611 Pensjonar frå statskassa |
| `kap-0612.md` | Kap. 612 Tilskot til Statens pensjonskasse |
| `kap-0613.md` | Kap. 613 Arbeidsgivaravgift til folketrygda |
| `kap-0621.md` | Kap. 621 Tilskot til sosiale tenester og sosial inkludering |
| `kap-0634.md` | Kap. 634 Arbeidsmarknadstiltak |
| `kap-0635.md` | Kap. 635 Ventelønn |
| `kap-0640.md` | Kap. 640 Arbeidstilsynet |
| `kap-0643.md` | Kap. 643 Statens arbeidsmiljøinstitutt |
| `kap-0646.md` | Kap. 646 Pionerdykkarar i Nordsjøen |
| `kap-0647.md` | Kap. 647 Kompensasjonsordning for oljepionerane |
| `kap-0648.md` | Kap. 648 Arbeidsretten, Riksmeklaren m.m. |
| `kap-0660.md` | Kap. 660 Krigspensjon |
| `kap-0664.md` | Kap. 664 Pensjonsordninga for arbeidstakarar til sjøs |
| `kap-0665.md` | Kap. 665 Pensjonstrygda for fiskarar |
| `kap-0666.md` | Kap. 666 Avtalefesta pensjon (AFP) |
| `kap-0667.md` | Kap. 667 Supplerande stønad |
| `kap-0670.md` | Kap. 670 Integrerings- og mangfaldsdirektoratet |
| `kap-0671.md` | Kap. 671 Busetting av flyktningar og tiltak for innvandrarar |
| `kap-0672.md` | Kap. 672 Opplæring i norsk og samfunnskunnskap for vaksne innvandrarar |
| `kap-2470.md` | Kap. 2470 Statens pensjonskasse |
| `kap-2541.md` | Kap. 2541 Dagpengar |
| `kap-2542.md` | Kap. 2542 Statsgaranti for lønnskrav ved konkurs m.m. |
| `kap-2620.md` | Kap. 2620 Stønad til einsleg mor eller far |
| `kap-2650.md` | Kap. 2650 Sjukepengar m.m. |
| `kap-2651.md` | Kap. 2651 Arbeidsavklaringspengar m.m. |
| `kap-2652.md` | Kap. 2652 Eit enklare Nav – forsøk med aktivitetspengar for unge |
| `kap-2655.md` | Kap. 2655 Uføretrygd m.m. |
| `kap-2661.md` | Kap. 2661 Grunn- og hjelpestønad, hjelpemiddel m.m. |
| `kap-2670.md` | Kap. 2670 Alderdom |
| `kap-2680.md` | Kap. 2680 Etterlatne |
| `kap-2686.md` | Kap. 2686 Stønad ved gravferd |
| `kap-3605.md` | Kap. 3605 Arbeids- og velferdsetaten |
| `kap-3635.md` | Kap. 3635 Ventelønn m.m. |
| `kap-3640.md` | Kap. 3640 Arbeidstilsynet |
| `kap-3670.md` | Kap. 3670 Integrerings- og mangfaldsdirektoratet |
| `kap-3671.md` | Kap. 3671 Busetting av flyktningar og tiltak for innvandrarar |
| `kap-3672.md` | Kap. 3672 Opplæring i norsk og samfunnskunnskap for vaksne innvandrarar |
| `kap-5470.md` | Kap. 5470 Statens pensjonskasse |
| `kap-5701.md` | Kap. 5701 Diverse inntekter |
| `kap-5704.md` | Kap. 5704 Statsgaranti for lønnskrav ved konkurs |
| `kap-5705.md` | Kap. 5705 Refusjon av dagpengar |
| `programkategori-09-00.md` | Programkategori 09.00 Administrasjon |
| `programkategori-09-10.md` | Programkategori 09.10 Administrasjon av arbeids- og velferdspolitikken |
| `programkategori-09-20.md` | Programkategori 09.20 Tiltak for betra levekår m.m. |
| `programkategori-09-30.md` | Programkategori 09.30 Arbeidsmarknad |
| `programkategori-09-40.md` | Programkategori 09.40 Arbeidsmiljø og sikkerheit |
| `programkategori-09-50.md` | Programkategori 09.50 Pensjonar m.m. under Statens pensjonskasse |
| `programkategori-09-60.md` | Programkategori 09.60 Kontantytingar |
| `programkategori-09-70.md` | Programkategori 09.70 Integrering og mangfald |
| `programkategori-29-20.md` | Programkategori 29.20 Einslege forsørgarar |
| `programkategori-29-50.md` | Programkategori 29.50 Inntektssikring ved sjukdom, arbeidsavklaring og uførleik |
| `programkategori-29-60.md` | Programkategori 29.60 Kompensasjon for meirutgifter ved nedsett funksjonsevne m.m. |
| `programkategori-29-70.md` | Programkategori 29.70 Alderdom |
| `programkategori-29-80.md` | Programkategori 29.80 Forsørgartap m.m. |
| `programkategori-29-90.md` | Programkategori 29.90 Diverse inntekter |
| `programkategori-33-30.md` | Programkategori 33.30 Arbeidsliv |
| `tema-01-innspel-fra-pensjonistorganisasjonane-til-utforminga-av-eldr.md` | Innspel frå pensjonistorganisasjonane til utforminga av eldrepolitikken |
| `tema-02-fordrivne-fra-ukraina.md` | Fordrivne frå Ukraina |
| `tema-03-fns-berekraftsmal.md` | FNs berekraftsmål |
| `tema-04-likestilling-og-mangfald.md` | Likestilling og mangfald |
| `tema-05-samfunnstryggleik.md` | Samfunnstryggleik |
| `tema-06-standardiserte-nokkeltal-for-nettobudsjetterte-verksemder-st.md` | Standardiserte nøkkeltal for nettobudsjetterte verksemder – STAMI |
| `tema-07-nye-internasjonale-standardar-fra-ilo.md` | Nye internasjonale standardar frå ILO |

### Gul bok

| Fil | Tittel |
|---|---|
| `01-01-hovedtrekk.md` | Hovedtrekk |
| `01-02-regjeringens-hovedprioriteringer.md` | Regjeringens hovedprioriteringer |
| `01-03-omprioriteringer-og-bedre-ressursbruk.md` | Omprioriteringer og bedre ressursbruk |
| `02-01-hovedtall-i-budsjettet.md` | Hovedtall i budsjettet |
| `02-02-statsbudsjettets-inntekter-og-utgifter-utenom-petroleumsvirk.md` | Statsbudsjettets inntekter og utgifter utenom petroleumsvirksomhet og lånetransaksjoner |
| `02-03-statsbudsjettets-lanetransaksjoner-og-finansieringsbehov.md` | Statsbudsjettets lånetransaksjoner og finansieringsbehov |
| `02-04-oversikt-over-utgifter-under-de-ulike-departementene.md` | Oversikt over utgifter under de ulike departementene |
| `02-05-folketrygdens-utgifter-og-inntekter.md` | Folketrygdens utgifter og inntekter |
| `02-06-forslag-til-vedtak.md` | Forslag til vedtak |
| `03-01-budsjettets-samlede-inntekter-og-utgifter.md` | Budsjettets samlede inntekter og utgifter |
| `03-02-gruppering-av-statsbudsjettets-inntekter.md` | Gruppering av statsbudsjettets inntekter |
| `03-03-gruppering-av-budsjettets-utgifter.md` | Gruppering av budsjettets utgifter |
| `03-04-petroleumsvirksomhetens-inntekter-og-utgifter.md` | Petroleumsvirksomhetens inntekter og utgifter |
| `03-05-oppsummering-saldering-av-statsbudsjettet-og-finansieringsbe.md` | Oppsummering. Saldering av statsbudsjettet og finansieringsbehov |
| `04-01-innledning.md` | Innledning |
| `04-02-samlet-utgiftsvekst-for-statsbudsjettet.md` | Samlet utgiftsvekst for statsbudsjettet |
| `04-03-realvekst-pa-statsbudsjettets-utgiftsomrader.md` | Realvekst på statsbudsjettets utgiftsområder |
| `04-04-utvikling-i-statsbudsjettets-utgifter-i-forhold-til-bnp-veks.md` | Utvikling i statsbudsjettets utgifter i forhold til BNP-veksten |
| `04-05-realvekst-i-folketrygdens-utgifter.md` | Realvekst i folketrygdens utgifter |
| `04-06-bevilgninger-over-statsbudsjettet-til-forskning-og-utvikling.md` | Bevilgninger over statsbudsjettet til forskning og utvikling |
| `05-01-forventet-handlingsrom-2028-2030.md` | Forventet handlingsrom 2028–2030 |
| `05-02-flerarige-budsjettkonsekvenser-2028-2030.md` | Flerårige budsjettkonsekvenser 2028–2030 |
| `05-03-ovrige-planer-og-ambisjoner.md` | Øvrige planer og ambisjoner |
| `06-00-gjennomforingen-av-innevaerende-ars-budsjett.md` | Gjennomføringen av inneværende års budsjett |
| `06-01-anslag-pa-regnskap-for-2026.md` | Anslag på regnskap for 2026 |
| `06-02-statsregnskapet-for-forste-halvar-2026.md` | Statsregnskapet for første halvår 2026 |
| `07-01-fullmakt-til-a-ta-opp-statslan-o-a.md` | Fullmakt til å ta opp statslån o.a. |
| `07-02-sammensetningen-av-statsgjelden.md` | Sammensetningen av statsgjelden |
| `07-03-statens-lanebehov-og-behovet-for-lanefullmakter.md` | Statens lånebehov og behovet for lånefullmakter |
| `08-01-budsjettprosessen-status-for-arbeidet-med-endringer.md` | Budsjettprosessen – status for arbeidet med endringer |
| `08-02-innforing-av-felles-regnskapsstandarder-i-statlige-virksomhe.md` | Innføring av felles regnskapsstandarder i statlige virksomheter |
| `08-03-standardisering-av-regnskapsforingen-av-eksternfinansierte-p.md` | Standardisering av regnskapsføringen av eksternfinansierte prosjekter (EFP) |
| `forslag-til-vedtak.md` | Forslag til vedtak |
| `vedlegg-01-oversikt-over-utgifter-og-inntekter-i-statsbudsjettet-for-bu.md` | Vedlegg Oversikt over utgifter og inntekter i statsbudsjettet for budsjetterminen 2027 |
| `vedlegg-02-statsbudsjettet.md` | Vedlegg Statsbudsjettet |
| `vedlegg-03-bevilgningsregnskapet.md` | Vedlegg Bevilgningsregnskapet |
| `vedlegg-04-virksomheter-med-saerskilte-fullmakter-nettobudsjetterte-for.md` | Vedlegg Virksomheter med særskilte fullmakter (nettobudsjetterte forvaltningsorganer) |
| `vedlegg-05-bestillingsfullmakt-tilsagnsfullmakt-og-garantifullmakt.md` | Vedlegg Bestillingsfullmakt, tilsagnsfullmakt og garantifullmakt |

### Nasjonalbudsjettet

| Fil | Tittel |
|---|---|
| `01-00-hovedlinjer-i-den-okonomiske-politikken-og-utsiktene-for-nor.md` | Hovedlinjer i den økonomiske politikken og utsiktene for norsk økonomi |
| `02-01-internasjonal-okonomi.md` | Internasjonal økonomi |
| `02-02-norsk-okonomi.md` | Norsk økonomi |
| `02-03-risikobildet.md` | Risikobildet |
| `02-04-naermere-om-arbeidsmarkedet.md` | Nærmere om arbeidsmarkedet |
| `03-00-budsjettpolitikken.md` | Budsjettpolitikken |
| `03-01-innretning-av-budsjettpolitikken-2027.md` | Innretning av budsjettpolitikken 2027 |
| `03-02-oppdatert-informasjon-om-budsjettpolitikken-i-2026.md` | Oppdatert informasjon om budsjettpolitikken i 2026 |
| `03-03-handlingsrommet-i-finanspolitikken-fremover.md` | Handlingsrommet i finanspolitikken fremover |
| `03-04-det-okonomiske-opplegget-for-kommunesektoren.md` | Det økonomiske opplegget for kommunesektoren |
| `03-05-utviklingen-i-offentlige-finanser-og-sammenligning-med-andre.md` | Utviklingen i offentlige finanser og sammenligning med andre land |
| `04-01-pengepolitikken.md` | Pengepolitikken |
| `04-02-finansiell-stabilitet.md` | Finansiell stabilitet |
| `04-03-sysselsettingspolitikken-og-det-inntektspolitiske-samarbeide.md` | Sysselsettingspolitikken og det inntektspolitiske samarbeidet |
| `04-04-forvaltningen-av-statens-pensjonsfond.md` | Forvaltningen av Statens pensjonsfond |
| `04-05-statens-gjeldsforvaltning.md` | Statens gjeldsforvaltning |
| `04-06-klimapolitikken.md` | Klimapolitikken |
| `05-01-betydningen-av-effektiv-ressursbruk.md` | Betydningen av effektiv ressursbruk |
| `05-02-sysselsetting.md` | Sysselsetting |
| `05-03-produktivitet.md` | Produktivitet |
| `05-04-faktorer-som-pavirker-produktiviteten.md` | Faktorer som påvirker produktiviteten |
| `05-05-offentlig-tjenesteproduksjon.md` | Offentlig tjenesteproduksjon |
| `05-06-hovedtrekk-i-regjeringens-tiltak-for-bedre-bruk-av-samfunnet.md` | Hovedtrekk i regjeringens tiltak for bedre bruk av samfunnets ressurser |
| `06-00-velferd-fordeling-og-ulikhet.md` | Velferd, fordeling og ulikhet |
| `06-01-maling-av-velferd-livskvalitet-og-levekar.md` | Måling av velferd, livskvalitet og levekår |
| `06-02-okonomisk-ulikhet-i-norge.md` | Økonomisk ulikhet i Norge |
| `forslag-til-vedtak.md` | Forslag til vedtak |
| `vedlegg-01-beregning-av-strukturell-oljekorrigert-budsjettbalanse.md` | Vedlegg Beregning av strukturell oljekorrigert budsjettbalanse |
| `vedlegg-02-beskrivelse-av-budsjetteffektberegningene.md` | Vedlegg Beskrivelse av budsjetteffektberegningene |
| `vedlegg-05-historiske-tabeller-og-detaljerte-anslagstall.md` | Vedlegg Historiske tabeller og detaljerte anslagstall |

## Oppdatering

Nye år legges inn ved å laste opp Word- og Excel-filene i `innboks-budsjett/` (se `innboks-budsjett/README.md`). Da kjører `verktoy/budsjett_innboks.py` automatisk. Manuelt: filene i `prop-1-s-aid/` lages med `python3 verktoy/budsjett.py <prop.docx> budsjett/ÅR/prop-1-s-aid "<kildenavn>"` og skal ikke redigeres for hånd. Gul bok og Nasjonalbudsjettet deles med samme skript og valget `--generell`. Gul bok-datagrunnlaget og figurdataene er Excel-filene fra regjeringen.no gjort om til TSV.
