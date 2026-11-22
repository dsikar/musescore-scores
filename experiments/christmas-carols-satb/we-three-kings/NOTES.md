# We Three Kings of Orient Are

| Item | Value |
|---|---|
| Files | [MuseScore](we-three-kings.mscz) · [PDF](we-three-kings.pdf) · [MP3](we-three-kings.mp3) · [MusicXML](we-three-kings.musicxml) |
| Words and music credit | John Henry Hopkins Jr. (1820–1891), 1857 |
| Source edition | Mobile Hymns, *We Three Kings*, one-page SATB short score; no separate harmoniser or typesetter is named |
| Key / time | E minor (one sharp) / 6/8 |
| Measures | 17, verse plus refrain; no repeats |
| Editorial tempo | ♩ = **90**, equivalent to dotted quarter = 60; source has no metronome mark |
| Duration | **34 s** (`--score-meta`); **37.07 s** MP3 including reverb tail |
| Lyrics | Stanza **1 and refrain** underlaid on Soprano; stanzas **2–5** printed as text, referring back to the refrain. None omitted |

## Source and rights

- Exact starter PDF, downloaded **22 November 2026**:
  <https://www.mobilehymns.org/PDF/We_Three_Kings.pdf>.
- Retained **unmodified** as [`source/We_Three_Kings.pdf`](source/We_Three_Kings.pdf).
- Publisher/site: [Mobile Hymns](https://www.mobilehymns.org/). The PDF credits
  **John Henry Hopkins Jr.** and explicitly marks the score **Public Domain**.
  It does not name a distinct harmoniser or engraving editor.
- **Composition and text:** Hopkins died in 1891; his nineteenth-century tune and
  text are public domain. **This edition:** redistribution here relies on its
  explicit public-domain marking, with its source attribution preserved.
  The site's [copyright-handling page](https://mobilehymns.org/copyright.html),
  retained as [`source/mobilehymns-copyright.html`](source/mobilehymns-copyright.html),
  distinguishes public-domain songs from permission-based copyrighted material.
- This is a transcription of the **Mobile Hymns SATB version**, not a claim to
  reproduce Hopkins's original 1863 voicing unchanged. The original book
  [*Carols, Hymns, and Songs*](https://archive.org/details/carolshym00hopk), pp. 12–13,
  and Hutchins's carol 344 were checked as candidates: their verses are a **trio
  of named kings with keyboard accompaniment**, not the requested SATB layout.
- A Wikimedia Commons PDF labelled *We Three Kings* was rejected after opening:
  it actually contains Michel Rondeau's **2000 two-trumpet arrangement**, despite
  the page's public-domain/mixed-chorus metadata. It is not a source for this score.
  Hymnary downloads returned 403; Stackapella's licensed SATB download required
  an account. Neither restriction was bypassed. **No substitution was needed.**

## Entry, restructuring and musical choices

Manually entered from the starter PDF using
[`tools/additional_carols.py`](../tools/additional_carols.py), then imported into
MuseScore with the existing `tools/carols.mss`. **No OMR or MIDI import.** The
clearly distinguishable upper/lower notes of the two staves supply S/A and T/B;
they are separated into four labelled staves. Shared unison noteheads are
assigned to both voices. Tenor's octave-treble clef preserves the sounding pitch.

All pitches, durations, accidentals, ties, slurs and the 6/8 meter are retained.
The source's guitar chord labels are omitted: this is unaccompanied SATB, and
there is no chord-symbol playback or extra accompaniment. Tempo 90 is editorial.
Playback performs one verse and its refrain, without adding stanza repeats.

Stanza 1 and the common refrain are underlaid on **Soprano only**. Stanzas 2–5,
originally stacked under the same notes, move to a text frame after the music.
`[Refrain]` cues refer to the words already underlaid. Apostrophe typography and
line breaking are normalised, retaining the chosen source's wording (including
“all men raising” and “Earth to heav'n replies”), rather than substituting a
modern hymnal's text.

### Source proofread record

| Measures | Checked in every voice |
|---|---|
| 1–4 | All pitches and rhythms; recurring D♯ in Alto; Alto tie and Tenor slur at the start of bar 4 |
| 5–8 | All notes; the four voices' different slurs in bar 6; Alto/Tenor ties in bar 7; dotted-half unisons in bar 8 |
| 9–13 | Refrain opening melismas; Alto and Bass ties in bar 9, contrasted with Soprano/Tenor slurs; all chord/unison pitches and durations |
| 14–17 | Every note and duration through the final refrain cadence; no appended instrumental interlude or repeats |

Each part has **62 notated notes**. Native export agrees with the ledger exactly;
ties, slurs and lyric syllables also survive the round-trip. The PDF has **2 pages**:
all music on page 1, additional stanzas on page 2.

## Playback and verification

Each file has exactly four labelled staves and was opened and saved in **MuseScore
Studio 4.7.5, build 3654226** on 22 November 2026. The installed **MuseSampler 0.106.0**
loaded successfully. The saved `audiosettings.json` assigns **Muse Choir → Sopranos,
Altos, Tenors, Basses**, with no vocal mute or solo enabled. The metronome is muted.

The source was read **bar by bar in all four voices**, including note values,
accidentals and any ties, slurs or repeats. `source-ledger.tsv` records that manual
reading (quarter-note duration units, sounding pitches, source bar positions starting
at 1). It is an audit aid, not an independently sourced MIDI file.

[`tools/verify_additional.py`](../tools/verify_additional.py) opens the final native
score in MuseScore, exports it back to MusicXML and checks all four voices' pitches,
durations and bar divisions against that ledger. It also checks ties, slurs, lyric
syllables, repeats, sound assignments, duration and the PDF. This verifies that
MuseScore preserved the entered reading; **the script does not read the PDF's notes**.
The independent MIDI check is **SKIPPED** because no independent MIDI of this exact
edition was used. See [`additional-score-check.json`](../evidence/additional-score-check.json).

All three final PDFs were rendered and inspected. The MP3 fully decodes, is audible
by signal-level analysis, and does not clip; see
[`additional-audio-check.json`](../evidence/additional-audio-check.json). No human
listen-through or expert editorial certification is claimed.

A **full GUI restart** and a visual Mixer check were completed on the new *We Three
Kings* score; the four presets survived. Both its score and Mixer screenshots are in
[`evidence/screenshots/`](../evidence/screenshots/). For the other two new scores,
GUI open/save and the saved preset metadata were checked; separate restart screenshots
were not taken, as the additional-carols brief requires this for at least one.

**Ordinary words are not sung.** The *We Three Kings* render is byte-identical with
and without its lyrics, and differs from MS Basic. The official
[Muse Choir guide](https://production-v2.muse-cdn.com/library-user-guides/2be98874-810b-485a-b238-d7c1eb857372.pdf)
documents special Ahh, Ooh and Mmm vowel controls via staff text or lyrics. That is
different from synthesising the English carol text. No special vowel changes were added.
