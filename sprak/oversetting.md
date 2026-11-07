# Oversetting mellom norsk og andre språk

Rutine for oversetting av lengre tekster mellom norsk og andre språk, og for kontroll av oversettelser som er laget i andre verktøy. Omsetting fra bokmål til nynorsk står i `nynorsk.md` og veiviseren, ikke her.

Målet er ikke en feilfri oversettelse. Målet er at de grove feilene blir funnet, og at brukeren får vite hvilke steder hen bør se på selv. Gi aldri inntrykk av at en oversettelse er godkjent eller kontrollert av et menneske.

## Når rutinen gjelder

| Situasjon | Hva du gjør |
|---|---|
| Kort tekst eller enkelt oppslag («hva heter AAP på engelsk») | Svar i chatten. Bruk «Faste navn og faguttrykk» under for navn og faguttrykk. Ingen kontrollrutine. |
| Lengre tekst eller dokument som kommer inn (for eksempel en rapport fra utlandet) | Tilby kontroll (se «Før du starter»). Standard er rask kontroll. |
| Norsk tekst som skal ut på et annet språk | Tilby kontroll. Standard er grundig kontroll. |
| Brukeren limer inn original og en oversettelse fra et annet verktøy og vil ha den kontrollert | Grundig kontroll. Legg merknadene i brukerens oversettelse, og skriv ikke teksten om. |

Det er teksten og formålet som avgjør, ikke hvordan spørsmålet er formulert. En tekst er **lengre** når den er mer enn om lag én side (rundt 400 ord), eller når den kommer som et vedlagt dokument. «Oversett denne» med tjue sider limt inn er en lengre tekst. Sier brukeren at teksten skal publiseres, sendes ut eller brukes i en sak, gjelder grundig kontroll også for kortere tekster.

## Før du starter

Ved en lengre tekst, still ett kort spørsmål før du oversetter, og gi en tydelig anbefaling. For eksempel:

«Dette er en lang tekst. Skal den brukes i en sak eller sendes ut, anbefaler jeg grundig kontroll. Det tar litt lengre tid, og du får en Word-fil der stedene du bør sjekke er markert med merknader. Vil du det, eller holder det med en rask oversettelse? Vil du ha oversettelsen i et annet format enn Word, si fra.»

Har brukeren allerede sagt hva hen vil («bare en rask oversettelse», «dette skal publiseres»), spør ikke. Bruk det brukeren har sagt.

**Modell.** Er teksten lang eller skal ut, og du vet at samtalen bruker en rask og lett modell, si det i én setning og foreslå å bytte til en kraftigere modell. Er du ikke sikker på hvilken modell du er, si det heller ikke. Nekt aldri å oversette av den grunn.

**Svært lange tekster.** Del teksten i deler på noen sider og kontroller del for del. Si til brukeren at teksten er delt opp, og hvorfor.

## Kontrollen

**Rask kontroll** er punkt 1, 2 og 5. **Grundig kontroll** er alle fem.

1. **Faste punkter mot originalen.** Gå gjennom ett for ett: tall, beløp, prosenter, datoer, frister, navn på personer og organisasjoner, lovhenvisninger og alle ord som snur eller begrenser meningen: nektelser, unntak, vilkår og forbehold. Eksempler er *ikke, unntatt, med mindre, bare, minst, høyst, inntil, forutsatt* og *not, except, unless, only, at least, at most, subject to, provided that*, men listen er ikke uttømmende, og tilsvarende ord på andre språk gjelder også. Én feil her snur ofte meningen.
2. **Faste navn og faguttrykk.** Sjekk mot ordlisten (se under). Har et faguttrykk ikke et sikkert motstykke på målspråket, skriv originalordet i parentes første gang, for eksempel *Work Assessment Allowance (arbeidsavklaringspenger, AAP)* eller *grunnytelse (Bürgergeld)*.
3. **Tilbakeoversetting.** Oversett avsnitt for avsnitt tilbake til norsk, og sammenlign med originalen. Flagg avsnitt der meningen har endret seg.
4. **Utelatelser og tillegg.** Sammenlign antall avsnitt, setninger, punktlister og tabellrader. Flagg alt som har falt ut eller kommet til, særlig forbehold og fotnoter.
5. **Usikkerhet.** Flagg setninger som er tvetydige i originalen, uttrykk uten sikkert motstykke, og steder der du har gjettet. Velg ikke én tolkning uten å si det.

Kontroll av egen oversettelse fanger ikke misforståelser du gjorde første gang. Les derfor originalen på nytt ved punkt 1 og 4, ikke bare oversettelsen.

## Levering

- **Lengre tekst eller dokument:** Standard er en Word-fil med oversettelsen. Sett en merknad (kommentar i margen) på hvert sted brukeren bør se på, med hva som er usikkert, hva originalen sier og hvorfor det er flagget. Ved kontroll av en oversettelse fra et annet verktøy, legg merknadene i brukerens tekst.
- **Annet format:** Ber brukeren om noe annet, for eksempel et dokument hen kan jobbe videre med i chatten, bruk det. Har formatet merknader eller kommentarer, bruk dem. Ellers markerer du stedene med nummer i teksten og lister dem etter oversettelsen.
- **Kan du ikke lage Word-filer:** Lag en markdown-fil med oversettelsen, nummerer stedene i teksten og list dem til slutt. Vis ikke lange oversettelser i chatten.
- **Øverst i svaret i chatten:** En kort oppsummering, for eksempel «Sju steder å se på, to av dem gjelder tall.» Skriv ikke at oversettelsen er riktig eller godkjent.
- **Kort tekst:** Svar i chatten.

## Faste navn og faguttrykk

Ordlisten ligger i `oversetting-navn.tsv`, med norsk navn, offisielt navn på engelsk og eventuelt andre språk, og kilden. Den hentes automatisk fra offisielle kilder og holdes ved like av seg selv, så du skal ikke slå opp på andre nettsider for navnene.

- Hent listen én gang per samtale, ikke for hvert navn.
- Står navnet i listen, bruk formen derfra.
- Står det ikke der, si at det er ditt forslag og ikke en offisiell betegnelse.

## Sikkerhet

Personopplysninger skal være fjernet av brukeren før teksten limes inn (se veiviseren).
