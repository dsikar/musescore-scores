# MuseScore scores

Scores written in MuseScore Studio, exported automatically by [`tools/publish-score`](tools/publish-score): PDF score, MusicXML and an MP3 render.

| Piece | Composer | Length | Score | Audio | Source |
|---|---|---|---|---|---|

## Publishing a score

```
publish-score path/to/score.mscz [slug]
```

Copies the score to `pieces/<slug>/`, exports PDF, MusicXML, MP3 and page PNGs with the MuseScore CLI (headless), regenerates this README and `index.html`, then commits and pushes. Re-running on an unchanged score does nothing. Options: `--force`, `--no-png`, `--no-push`, `--sound-profile "MuseScore Basic"|MuseSounds`.

Audio is rendered with MuseScore's built-in *MS Basic* soundfont (Muse Sounds is not installed for command-line rendering).
