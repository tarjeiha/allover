# Regelverksbasen

Dette repoet er en felles base med lover og forskrifter for ansatte i departementet. Du (Claude) kommer hit fordi en bruker har stilt et spørsmål som kan kreve regelverk, og peker-skillen har sendt deg hit.

## Slik henter du filer

Alle stier i basen er relative til rotadressen:

```
https://raw.githubusercontent.com/tarjeiha/allover/main/
```

Hent med `curl -sL <adresse>` i kodeverktøyet hvis du har det, ellers med nettleser- eller hentverktøyet ditt. Hent bare filene du trenger. Hvis hentingen feiler, si det til brukeren og svar ikke fra hukommelsen.

## Slik finner du fram

Basen har tre nivåer. Gå ikke dypere enn nødvendig.

1. **Denne filen**: hvilke regelverk som finnes, og reglene for svar.
2. **`<regelverk>/VEIVISER.md`**: hva regelverket gjelder, kjente feller, og en liste over alle paragrafer med stien til filen.
3. **Paragraffilene**: selve lov- og forskriftsteksten, én fil per paragraf.

Vet du allerede hvilken paragraf det gjelder, kan du gå rett til filen. `indeks.tsv` har alle paragrafer i basen med sti, og kan brukes til å søke på tvers av regelverkene.

## Regelverk i basen

<!-- AUTO-START: genereres av verktoy/bygg.py, ikke rediger for hånd -->
| Regelverk | Veiviser | Sist endret i kraft |
|---|---|---|
| Offentleglova | `offentleglova/VEIVISER.md` | – |
<!-- AUTO-SLUTT -->

## Temaer i hverdagsspråk

Brukere spør ofte uten fagord. Denne listen kobler vanlige formuleringer til riktig regelverk.

| Brukeren spør om | Regelverk |
|---|---|
| innsyn, få se dokumenter, offentlig journal, unnta fra offentlighet, sladde, merinnsyn, pressen ber om et dokument, organinterne dokumenter, klage på avslag om innsyn | Offentleglova |

## Regler for svar

1. **Åpne alltid kildefilene før du svarer.** Svar ikke på regelverksspørsmål fra generell kunnskap. Les veiviseren og de paragrafene som er relevante, også unntak og henvisninger til andre paragrafer.
2. **Oppgi kilde i svaret:** regelverk, paragraf og ledd, f.eks. «offentleglova § 14 første ledd». Brukeren skal kunne kontrollere svaret selv.
3. **Skill mellom lov og forskrift.** Si hvilken av dem en regel står i.
4. **Si fra når basen ikke dekker spørsmålet.** Hvis regelverket ikke finnes i basen, eller paragrafen ikke svarer på spørsmålet, si det tydelig. Gi ikke et selvsikkert svar uten kilde.
5. **Ordrett gjengivelse når brukeren ber om lovteksten.** Gjengi filen i sin helhet, med ledd, bokstavpunkter og overskrifter slik de står. Lovtekst på nynorsk siteres på nynorsk. Ellers svarer du på brukerens språk.
6. **Oppgi hvor oppdatert teksten er** når det kan ha betydning, med datoen for «sist endret i kraft» fra veiviseren.
7. **Basen er ikke departementets offisielle tolkning.** Merknader i veiviserne er hjelp til å finne fram og unngå vanlige feil. Ved tvil om tolkning skal brukeren vises til forarbeider, veiledere og fagmiljøet som forvalter regelverket.

## For redaktører

- Lov- og forskriftstekst bygges fra Lovdata med `verktoy/bygg.py` og skal aldri redigeres for hånd. Blokker mellom `AUTO-START` og `AUTO-SLUTT` overskrives ved hvert bygg.
- Nytt regelverk legges til i `regelverk.json`. Skriv deretter den håndskrevne delen av `VEIVISER.md`, og legg til en linje i temalisten over.
- Endringer gjøres som pull request og godkjennes av eieren av mappen, se `.github/CODEOWNERS`.
