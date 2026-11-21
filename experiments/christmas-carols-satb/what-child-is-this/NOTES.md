# What Child Is This?

| | |
|---|---|
| Score | [`what-child-is-this.mscz`](what-child-is-this.mscz), GUI-saved, with Muse Choir pinned |
| PDF | [`what-child-is-this.pdf`](what-child-is-this.pdf), 2 pages (A4) |
| Starter files | [`source/What_Child_Is_This-Greensleeves.pdf`](source/What_Child_Is_This-Greensleeves.pdf) and [`source/What_Child_Is_This-Greensleeves.abc`](source/What_Child_Is_This-Greensleeves.abc), unmodified |
| Key / time | D major / 6/8 |
| Measures | 17 (as counted by MuseScore, including any pickup bar) |
| Tempo | ♩ = 80, **taken from the source** (`Q:` field). Nothing added |
| Duration | **36 s** for one pass through the music, from `musescore --score-meta` |

## Source and rights

- **Edition:** Open Hymnal Project (openhymnal.org), editor Brian J. Dumont. Score revision 2005, distributed in the Open Hymnal 2026.11 release.
- **Source URLs, retrieved 21 November 2026:**
  - PDF (the starter score): <http://openhymnal.org/Pdf/What_Child_Is_This-Greensleeves.pdf>
  - ABC (the same edition's source code, which produces that PDF): <http://openhymnal.org/Abc/What_Child_Is_This-Greensleeves.abc>
  - MIDI (the same edition's own audio render, used only for checking): <http://openhymnal.org/Midi/What_Child_Is_This-Greensleeves.mid>
- **Music:** *Greensleeves*, 16th-century English traditional.
- **Setting / harmonisation:** traditional, from *The Sunday School Hymnal and Service Book*, 1871 (ed. Charles L. Hutchins). The ABC also cites *Lutheran Worship* (1982), hymn 61, with "very tiny changes".
- **Words:** William Chatterton Dix (1837–1898), 1865. The Open Hymnal metadata gives his dates as 1837–1865; he died in 1898. The text is public domain either way.
- **Composition and text rights:** public domain. All the people named died more than 70 years ago, and the settings were all published before 1929, so they are public domain in the US too.
- **Edition rights:** the score is marked *"copyright: public domain. This score is a part of the Open Hymnal Project"*. The project's copying page (saved as [`source/openhymnal-copying.txt`](source/openhymnal-copying.txt)) assesses rights under **US law**. It places all of its own compilation and data files in the public domain, and puts the responsibility for checking status in other countries on the user. Redistributing the starter files here is permitted on that basis.
- No login, paywall, purchase or bot protection was involved. The files are plain HTTP downloads.

## How the score was made

The score was **converted, not transcribed**. The Open Hymnal ABC file is the source code for the starter PDF, so this pipeline reads the same note data that the PDF was typeset from. No OMR was used. Each step is in [`../build.sh`](../build.sh):

1. `tools/prep_abc.py` changes only the staff layout: `%%staves (S1V1 S1V2) | (S2V1 S2V2)` becomes one staff per voice, and the four voices are named Soprano, Alto, Tenor and Bass.
2. abc2xml v269 (Willem Vree) converts the ABC to MusicXML.
3. `tools/fix_xml.py` sets the instrument sounds to `voice.soprano/alto/tenor/bass` (in place of the ABC's piano MIDI program), gives the Tenor an octave-treble clef, removes the forced stem directions left over from the two-voices-per-staff layout, and tidies the title and credits.
4. MuseScore 4.7.7 imports the MusicXML with the shared style [`../tools/carols.mss`](../tools/carols.mss) (A4, more lyric spacing).
5. `tools/add_text_stanzas.py` adds any stanzas that the source prints as text only.
6. The score is opened in the MuseScore GUI and saved with Ctrl+S, which pins the Muse Choir presets.

## Restructuring

- **Two staves to four.** The source is a hymn-style short score: Soprano and Alto share the treble staff, and Tenor and Bass share the bass staff. Here each voice has its own labelled staff: **Soprano, Alto, Tenor, Bass**.
- **Tenor clef.** The Tenor moves from the bass staff to an **octave-treble clef** (treble with an 8 below), the modern open-score convention. This changes only how the part is displayed; MusicXML stores absolute pitches, and the MIDI cross-check confirms that the Tenor sounds at the same pitches as before.
- Stems now follow each single voice's own direction instead of the up/down convention for shared staves.

## Musical changes and omissions

- **No notes, rhythms, rests, key or time signatures, ties, slurs or tempo were changed.** The source has no repeats, voltas, fermatas or dynamics to preserve.
- **Omitted:** the Open Hymnal's organ-introduction brackets (⌐ ¬), which mark a passage for the accompanist to play as an intro, are not musical content. Also omitted are the page furniture: the "CHRISTMAS" category label, the scripture references and the metre in the footer.
- **Playback is one pass through the music.** The stanzas are stacked under the same notes, as in the source. No repeat was added to replay the music for each stanza.

## Lyric coverage

Stanzas **1–3** are underlaid on the **Soprano staff**. Each stanza includes its own refrain lines. No stanza was omitted.

The Alto, Tenor and Bass staves carry **no lyrics**. The source prints a single set of words between the staves, aligned to the Soprano line, and copying it to voices whose rhythm sometimes differs was not attempted.

**Playback does not sing these words.** Muse Choir is vowel-based: the earlier experiment showed that removing every lyric produces byte-identical audio. See [`../../musescore-choir-experiment/FINDINGS.md`](../../musescore-choir-experiment/FINDINGS.md), finding 3. That test was not repeated here, because the MuseScore and MuseSampler versions are the same.

## Tempo and duration

♩ = 80 (from the source). One pass lasts **36 s** according to `--score-meta`, well within the 5-minute limit. Even if the music were repeated once for each of the 3 stanzas, it would last about 108 s.

## What was checked against the source

- **Every note's pitch and onset, in every voice**, was compared automatically with the edition's own MIDI file, which Open Hymnal produced from the same ABC with abc2midi, a different converter from abc2xml. Result: **PASS (exact)**. See `tools/midi_check.py` and `../evidence/verify-carols-run.txt`.
- **Visual comparison** of the rendered PDF with the starter PDF, page against page. This confirmed the notes and stems, the ties and slurs (including dotted ones), the accidentals, the stanza count and numbering, and the parenthesised notes. It was done at page resolution, not by zooming in on every notehead. The automated check above is what covers every bar.
- **Structure**, from `--score-meta`: four parts named Soprano, Alto, Tenor and Bass; 17 measures; 6/8; key D major; ♩ = 80.
- **Sounds:** `audiosettings.json` in the committed `.mscz` maps soprano, alto, tenor and bass to Muse Choir Sopranos, Altos, Tenors and Basses.
