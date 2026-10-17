# allover

Felles base som Claude slår opp i når noen stiller spørsmål som krever regelverk, budsjett eller statistikk. Repoet er under utprøving.

- [`regelverk/`](regelverk/): lover og forskrifter fra Lovdata, hovedtariffavtalen i staten og EU-rettsakter.
- [`budsjett/`](budsjett/): statsbudsjettet for AID.
- [`data/`](data/): katalog over hvor tall og statistikk finnes.

- **For Claude:** start i [`CLAUDE.md`](CLAUDE.md).
- **For brukere:** installer peker-skillen i [`skills/`](skills/). Den sier fra til Claude når basen skal brukes, og henter innholdet herfra. Du trenger ikke oppdatere noe selv.
- **For redaktører:** endringer gjøres som pull request og godkjennes av eieren av mappen (se [`.github/CODEOWNERS`](.github/CODEOWNERS)). Lovtekst redigeres ikke for hånd. Den bygges fra Lovdata (se [`verktoy/`](verktoy/)).

Lovtekst og forskrifter er hentet fra Lovdatas åpne datasett. Se [`LICENSE.md`](LICENSE.md).
