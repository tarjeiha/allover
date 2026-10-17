# Statsbudsjettet – veiviser

Denne mappen har statsbudsjettdokumenter for Arbeids- og inkluderingsdepartementet (AID), delt opp slik at du kan gå rett til et kapittel eller en post. Dokumentene er offentlige og hentet fra regjeringen.no. Word- og Excel-filene lastes opp manuelt, fordi regjeringen.no ikke slipper til automatisk henting.

## Kjente feller

- **Prop. 1 S er regjeringens forslag, ikke vedtatt budsjett.** Stortinget vedtar budsjettet i desember, etter budsjettforliket og innstillingene fra komiteene. Tilleggsproposisjoner (Prop. 1 S Tillegg) kan endre forslaget. Si alltid at tallene er forslag, og fra hvilket dokument.
- **Ulike enheter.** Tabellene i proposisjonen er i 1 000 kroner. `gul-bok-bevilgninger.tsv` er i kroner.
- **Nynorsk.** AIDs proposisjon er skrevet på nynorsk. Siter på nynorsk, men svar på brukerens språk.
- **Overslagsløyvingar.** Poster merket «overslagsløyving» (f.eks. dagpenger) er anslag. Utgiftene følger regelverket, ikke beløpet.
- **Kapittelnumrene sier hva slags kapittel det er.** Kap. 600–699 er ordinære utgiftskapitler, 2470 er Statens pensjonskasse, 2541–2686 er folketrygden, 3000-kapitlene er inntekter som hører til 600-kapitlene, og 5000-kapitlene er andre inntekter og utgifter (f.eks. 5470 Statens pensjonskasse og 5705 Refusjon av dagpengar). Se programkategori-filene for inndelingen.

## Budsjettår 2027

| Dokument | Sti | Innhold |
|---|---|---|
| Prop. 1 S (2026–2027) AID | `budsjett/2027/prop-1-s-aid/` | Hele proposisjonen, én fil per kapittel |
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

## Oppdatering

Filene i `prop-1-s-aid/` lages med `python3 verktoy/budsjett.py <prop.docx> budsjett/ÅR/prop-1-s-aid "<kildenavn>"` og skal ikke redigeres for hånd. Gul bok-datagrunnlaget er Excel-filen fra regjeringen.no gjort om til TSV.
