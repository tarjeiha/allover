# Politiske grunnlagsdokumenter – veiviser

Denne mappen har dokumenter der regjeringen beskriver sin politikk og sine prioriteringer. De er verken lov, forskrift eller budsjett. Dokumentene er offentlige, lastes ned fra regjeringen.no og legges inn for hånd, fordi regjeringen.no ikke slipper til automatisk henting.

## Dokumenter

| Dokument | Utgave | Utgitt av | Mappe |
|---|---|---|---|
| Regjeringens plan for Norge | 2025–2029, utgitt desember 2025 | Statsministerens kontor | `politikk/regjeringens-plan-for-norge/` |

## Regjeringens plan for Norge

Planen beskriver hva regjeringen vil prioritere i stortingsperioden 2025–2029. Den har en innledning og fem kapitler. Hvert kapittel har først en beskrivelse av situasjonen og deretter avsnittet «Regjeringen prioriterer» med satsingsområder og tiltak for 2026.

| Fil | Innhold |
|---|---|
| `00-innledning.md` | Innledning: hva planen bygger på og at den revideres hvert år |
| `01-trygghet-for-okonomien.md` | Økonomisk styring, 150 000 flere i jobb og sysselsettingsandel på 82 prosent innen 2030, integrering, boliger, fornying av offentlig sektor og mål om KI i offentlige virksomheter |
| `02-trygghet-for-arbeids-og-naeringslivet.md` | Konkurransekraft, klima, skattereform, EØS og handel, organisert arbeidsliv (fagforeningsfradrag, Arbeidstilsynet, sosial dumping, plattformarbeid, yrkesskade) og kunstig intelligens |
| `03-trygghet-for-barn-og-unge.md` | Skole og lesing, Ungdomsløftet (30 000 flere unge i jobb, lønnstilskudd til unge uføre), barne- og ungdomskriminalitet, skjermbruk og kultur |
| `04-trygghet-for-helsa.md` | Sykefravær og frafall fra arbeidslivet, ventetider, eldre og helsereform |
| `05-trygghet-for-landet.md` | Forsvar, beredskap, økonomisk sikkerhet, utenrikspolitikk, kriminelle nettverk og innvandringspolitikk |

Teksten er gjengitt ordrett fra PDF-utgaven. Bare innholdsfortegnelsen, sidetallene og kolofonen er tatt ut.

## Kjente feller

- **Politikk, ikke vedtak.** Planen er regjeringens prioriteringer. Den binder ikke Stortinget og gir ingen rettigheter. Tiltakene gjennomføres gjennom budsjett, lovforslag og andre vedtak. Si at svaret bygger på regjeringens plan, og vis til regelverket eller budsjettet når spørsmålet gjelder hva som faktisk er vedtatt.
- **Bygger på ett partis program.** Planen sier selv at den bygger på Arbeiderpartiets partiprogram og valgløftene fra 2025. Den er ikke en avtale mellom flere partier, slik en regjeringsplattform kan være.
- **Revideres hvert år.** Planen sier at den revideres årlig, og at måloppnåelsen avhenger av det økonomiske handlingsrommet. Tiltak merket «I 2026» gjelder planen fra desember 2025. Oppgi utgaven når du siterer, og si at en nyere utgave kan finnes hvis datoen tilsier det.
- **Tallmål er mål.** Mål som 150 000 flere i jobb, 82 prosent sysselsetting og 130 000 nye boliger innen 2030 er ambisjoner. Bruk statistikkatalogen (`data/VEIVISER.md`) for hvordan det faktisk går.
- **Bokmål.** Planen er skrevet på bokmål. Siter ordrett.

## Ny utgave

Nattbygget åpner en sak i GitHub når en ny utgave ventes (`verktoy/politikk.py`). Datoen regnes fra `utgitt` i `politikk/dokumenter.json`. Når en ny utgave legges inn, erstattes filene i mappen, og `utgitt`, `utgave` og tabellene over oppdateres. Den forrige utgaven finnes i historikken til repoet.
