# Once in Royal David's City

| Item | Value |
|---|---|
| Files | [MuseScore](once-in-royal-davids-city.mscz) · [PDF](once-in-royal-davids-city.pdf) · [MP3](once-in-royal-davids-city.mp3) · [MusicXML](once-in-royal-davids-city.musicxml) |
| Tune | *Irby*, H. J. Gauntlett (1805–1876), 1849 |
| Words | Cecil Frances Alexander (1818–1895), 1848 |
| Source | *Hymns Ancient and Modern*, Historical Edition, London: William Clowes and Sons, 1909, hymn 566, printed pp. **708–709**, PDF pages **852–853** |
| Key / editorial meter | G major / 4/4 |
| Written source bars | 12 per part, counting the short phrase bars and pickup as separate positions |
| Editorial tempo | ♩ = **88**; no metronome mark is printed in the source |
| Duration | **33 s** (`--score-meta`); **35.79 s** MP3 including reverb tail |
| Lyrics | Stanza **1** underlaid on Soprano; stanzas **2–6** printed as text. None omitted |

## Source and rights

- Full source: <https://archive.org/details/hymnsancientmode0000vari_q0j0>.
- Exact downloaded PDF: <https://archive.org/download/hymnsancientmode0000vari_q0j0/hymnsancientmode0000vari_q0j0.pdf>.
- Downloaded **21 November 2026**; inspected and transcribed **22 November 2026**.
- The **complete original PDF is retained, byte-for-byte**, as
  [`source/hymns-ancient-and-modern-1909.pdf`](source/hymns-ancient-and-modern-1909.pdf).
  SHA-256: `063a9e527b0d24cbfe319bb60dcf22cec7ab3365f984730f93dde9f9ddaead49`.
  The same file is linked from *While Shepherds Watched*'s source folder.
- [`source/hymns-1909-hymn-566.pdf`](source/hymns-1909-hymn-566.pdf) is a convenient
  **page extract** made with `pdfseparate`/`pdfunite`; its notation and page images
  were not edited. It is not presented as a byte-identical copy of the complete book.
  The Archive metadata is also retained.
- **Composition and text:** Gauntlett and Alexander died in 1876 and 1895;
  these nineteenth-century works are public domain in the UK and US.
- **Setting/edition:** the source's commentary on p. 709 says Gauntlett made the
  four-part setting, and explicitly notes **altered harmonies in this edition**.
  The credit therefore identifies the 1909 Historical Edition, rather than claiming
  this reproduces the unaltered 1849 harmony. The anonymous editorial alterations
  and the printed edition were published in 1909; no modern arrangement was used.
  The retained scan is a reproduction of that historical printing. No Willcocks
  descant or Vaughan Williams harmonisation was used.

## Entry, restructuring and musical choices

Manually entered from the source PDF using
[`tools/additional_carols.py`](../tools/additional_carols.py), then imported into
MuseScore with the existing `tools/carols.mss` style. **No OMR or MIDI import.**
The source prints a separate melody above a two-staff SATB harmonisation. The
redundant melody staff is omitted; S/A and T/B are separated into four staves,
with the Tenor on octave-treble clef at its original sounding pitch. The melody
staff's syllabic slurs are retained on Soprano.

The source has **no time signature**. Editorial 4/4 is supplied, retaining its
actual note values and short phrase bars as irregular measures, without padding
rests. Its double barlines are retained. The backward repeat after the opening
six written bars is retained: that passage plays twice, followed by the final
six bars. This performs **one complete stanza** (48 quarter-note beats), not two
stanzas. No repeat is added for stanzas 2–6.

Stanza 1's first four lines use **two lyric rows over the repeated passage**;
they are two halves of the **same stanza**. Its final two lines use one row.
Stanzas 2–6 follow as text. Small capitals, quotation typography and hyphenation
are normalised; no stanza wording is deliberately omitted. The source's historical
Alexander birth-year annotation is not repeated: the score uses 1818.

### Source proofread record

| Source bar positions | Checked in every voice |
|---|---|
| 1–6, repeated opening | All pitches and durations; alto's split eighth notes; bass pickup and cadences; exact repeat placement; both halves of stanza 1 |
| 7–12, final two lines | All pitches and durations; bass C3–E3 pickup and A2 before B2 cadence; C3–D3–E3–F♯3 bass run; alto D♯4; soprano's final syllabic slurs |

Notated note counts S/A/T/B: **35 / 38 / 40 / 33**. The ledger and native export
agree exactly. The final PDF has **2 pages**, with all music on page 1 and the
additional stanza text on page 2.

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
