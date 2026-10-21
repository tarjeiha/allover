# allover

Felles base som Claude slår opp i når noen stiller spørsmål som krever regelverk, budsjett eller statistikk. Repoet er under utprøving.

- [`regelverk/`](regelverk/): lover og forskrifter fra Lovdata, hovedtariffavtalen i staten og EU-rettsakter.
- [`budsjett/`](budsjett/): statsbudsjettet.
- [`data/`](data/): katalog over hvor tall og statistikk finnes.
- [`sprak/`](sprak/): skriveregler og nynorskføringer.

- **For Claude:** start i [`CLAUDE.md`](CLAUDE.md).
- **Hva som ligger her, og hvordan du melder feil:** se [`OM-BASENE.md`](OM-BASENE.md).
- **For brukere:** installer skillen `felles-intern` fra redaktøren og si «installer de felles skillene». Da får du peker-skillene, som sier fra til Claude når basen skal brukes og henter innholdet herfra. Du trenger ikke oppdatere noe selv.
- **For redaktører:** endringer gjøres som pull request og godkjennes av eieren av mappen (se [`.github/CODEOWNERS`](.github/CODEOWNERS)). Lovtekst redigeres ikke for hånd. Den bygges fra Lovdata (se [`verktoy/`](verktoy/)). Hvordan nytt regelverk legges til og kontrolleres, står i [`verktoy/BYGGING.md`](verktoy/BYGGING.md).

Lovtekst og forskrifter er hentet fra Lovdatas åpne datasett. Se [`LICENSE.md`](LICENSE.md).
