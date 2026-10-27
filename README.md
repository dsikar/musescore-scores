# MuseScore scores

Scores written in MuseScore Studio, exported automatically by [`tools/publish-score`](tools/publish-score): PDF score, MusicXML and an MP3 render.

**Listen in the browser:** https://dsikar.github.io/musescore-scores/

| Piece | Composer | Length | Score | Audio | Source |
|---|---|---|---|---|---|
| **Symphony No. 8 (in G major ∙ op. 88)** `dvorak-8-mvt-1` | Antonín Dvořák | 9:15 | [PDF](pieces/dvorak-8-mvt-1/exports/dvorak-8-mvt-1.pdf) · [MusicXML](pieces/dvorak-8-mvt-1/exports/dvorak-8-mvt-1.musicxml) · [pages](pieces/dvorak-8-mvt-1/exports/png) | [MP3](pieces/dvorak-8-mvt-1/exports/dvorak-8-mvt-1.mp3) (8.9 MB) · [▶ play](https://dsikar.github.io/musescore-scores/#dvorak-8-mvt-1) | [.mscz](pieces/dvorak-8-mvt-1/dvorak-8-mvt-1.mscz) |

## Publishing a score

```
publish-score path/to/score.mscz [slug]
```

Copies the score to `pieces/<slug>/`, exports PDF, MusicXML, MP3 and page PNGs with the MuseScore CLI (headless), regenerates this README and `index.html`, then commits and pushes. Re-running on an unchanged score does nothing. Options: `--force`, `--no-png`, `--no-push`, `--sound-profile "MuseScore Basic"|MuseSounds`, `--video` (build an MP4 slideshow), `--youtube` (build the video and upload it unlisted).

Videos: `make-video <slug>` writes `pieces/<slug>/exports/<slug>.mp4` (1080p, page turns timed from the score's measure positions; not committed). `youtube-upload [--privacy unlisted|private|public] <slug>` uploads it and adds the YouTube link here.

Audio is rendered with MuseScore's built-in *MS Basic* soundfont (Muse Sounds is not installed for command-line rendering).
