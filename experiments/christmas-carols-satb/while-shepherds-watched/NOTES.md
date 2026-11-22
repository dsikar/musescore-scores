# While Shepherds Watched Their Flocks

| Item | Value |
|---|---|
| Files | [MuseScore](while-shepherds-watched.mscz) · [PDF](while-shepherds-watched.pdf) · [MP3](while-shepherds-watched.mp3) · [MusicXML](while-shepherds-watched.musicxml) |
| Tune / setting | **Winchester Old**, from Thomas Este's *Whole Book of Psalmes* (1592), in the 1909 Historical Edition |
| Words | Nahum Tate (1652–1715), 1700 |
| Source | *Hymns Ancient and Modern*, Historical Edition, London: William Clowes and Sons, 1909, hymn **64, Second Tune**, printed pp. **85–86**, PDF pages **229–230** |
| Key / editorial meter | F major / 4/2 |
| Written source bars | 12 per part, counting short phrase bars and pickup |
| Editorial tempo | **Half note = 80** (quarter note = 160); no source metronome mark |
| Duration | **24 s** (`--score-meta`); **27.06 s** MP3 including reverb tail |
| Lyrics | Stanza **1** underlaid on Soprano; stanzas **2–6** printed as text. None omitted |

## Source and rights

- Full source: <https://archive.org/details/hymnsancientmode0000vari_q0j0>.
- Exact PDF: <https://archive.org/download/hymnsancientmode0000vari_q0j0/hymnsancientmode0000vari_q0j0.pdf>.
- Downloaded **21 November 2026**; inspected and transcribed **22 November 2026**.
- The complete, **unmodified** original PDF is retained once in the neighbouring
  carol's source folder and linked here as
  [`source/hymns-ancient-and-modern-1909.pdf`](source/hymns-ancient-and-modern-1909.pdf).
  SHA-256: `063a9e527b0d24cbfe319bb60dcf22cec7ab3365f984730f93dde9f9ddaead49`.
- [`source/hymns-1909-hymn-64.pdf`](source/hymns-1909-hymn-64.pdf) contains extracts
  of PDF pages 229–230 with no alteration to the printed content. Page 85 carries
  all six stanzas and the first tune; **only the second tune on p. 86 is entered**.
  Archive metadata is retained separately.
- **Composition and text:** the sixteenth-century tune and Tate's 1700 words
  are public domain. The edition's commentary traces the tune to T. Est's 1592
  psalter and reproduces G. Kirby's earlier form for comparison.
- **Setting/edition:** this transcription follows the main **Second Tune** printed
  at the top of p. 86, not the smaller historical example below. No separate
  harmoniser is named for this version, so no unsupported harmoniser credit is
  invented. The anonymous historical setting and typesetting were published in
  1909 and are public domain; the scan reproduces that printing.

## Entry, restructuring and musical choices

Manually entered from the PDF with
[`tools/additional_carols.py`](../tools/additional_carols.py), then imported with
`tools/carols.mss`. **No OMR, pre-existing encoding or MIDI import.** The shared
SA/TB staves become four labelled staves; Tenor uses octave-treble clef at the
same sounding pitch. All notes, note values, accidentals and printed phrase
barlines are retained. There are no source repeats, ties, slurs, dynamics or
fermata marks in the selected setting.

The print supplies no time signature. Editorial **4/2** accommodates its original
half-note beat and longer notes; the short pickup and phrase bars remain short,
with no padding rests. The minim tempo is **80**, equivalent to quarter note 160;
the printed note values have **not** been halved. The 64 quarter-note beats take
24 seconds. Playback performs the tune once, not six stanzas.

The source prints all six stanzas as text on p. 85. Stanza 1 is newly underlaid on
Soprano; stanzas 2–6 remain text after the music. Alto, Tenor and Bass have no
lyrics. Small capitals and punctuation are normalised, retaining the source's
wording, including “watch'd”, “the seraph” and the ending “Amen.”

### Source proofread record

| Source bar positions | Checked in every voice |
|---|---|
| 1–6, first two lines | All notes and durations; soprano B-natural in bar 5; dotted values and phrase lengths |
| 7–12, last two lines | All notes and durations; shared **B♭3 dotted half** in Tenor/Bass at bar 8 (a high bass unison, retained); alto C♯4 at bar 9 and explicit C-natural cancellation at bar 10 |

Each part has **28 notated notes**. All four parts and every bar agree exactly
with the ledger after the native round-trip. The PDF is **1 A4 page** and includes
all five additional stanzas beneath the music without clipping.

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
