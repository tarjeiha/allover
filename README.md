# allover

Felles base med regelverk som Claude slår opp i når ansatte i departementet stiller spørsmål som krever regelverk.

Repoet er under utprøving. Første lov er offentleglova med offentlegforskrifta.

- **For Claude:** start i [`CLAUDE.md`](CLAUDE.md).
- **For brukere:** installer peker-skillen i [`skills/`](skills/). Den sier fra til Claude når basen skal brukes, og henter innholdet herfra. Du trenger ikke oppdatere noe selv.
- **For redaktører:** endringer gjøres som pull request og godkjennes av eieren av mappen (se [`.github/CODEOWNERS`](.github/CODEOWNERS)). Lovtekst redigeres ikke for hånd. Den bygges fra Lovdata (se [`verktoy/`](verktoy/)).

Lovtekst og forskrifter er hentet fra Lovdatas åpne datasett. Se [`LICENSE.md`](LICENSE.md).
