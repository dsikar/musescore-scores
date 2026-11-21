# SATB Christmas carols with Muse Choir

Twelve well-known Christmas carols, each set as a four-staff SATB choir score in
MuseScore Studio. Every score is assigned to **Muse Sounds → Muse Choir** (Sopranos, Altos,
Tenors, Basses), has a PDF export, and is built from an unmodified public-domain starter
file that is kept in the repository. The brief is in [`PROMPT.md`](PROMPT.md).

This applies the method of the earlier single-piece experiment,
[`../musescore-choir-experiment/`](../musescore-choir-experiment/), to a set of carols. The
MuseScore and MuseSampler versions are the same as that experiment's, so its findings were
reused rather than re-investigated: headless Muse Sounds rendering, the silent fallback to
MS Basic, Muse Choir ignoring lyrics, and CLI-written scores not pinning their sounds.

## The carols

All twelve come from the **Open Hymnal Project** (openhymnal.org, ed. Brian J. Dumont),
retrieved on 21 November 2026. Every one is marked public domain in words, music and
setting; see [Rights](#rights). Durations are for **one pass through the music** at the
saved tempo, as reported by `musescore --score-meta`. Each tempo is the source's own.

| # | Title | Composer / harmoniser | Text | Source (starter PDF) | Licence | Stanzas included | Tempo | Duration | Files |
|---|---|---|---|---|---|---|---|---|---|
| 1 | O Come, All Ye Faithful | J. F. Wade (*Adeste Fideles*, c. 1743); setting *A Hymnal* (Episcopal) 1916, alt. | J. F. Wade; tr. F. Oakeley 1841 (st. 1–3, 6), W. T. Brooke (st. 4–5) | [Open Hymnal](http://openhymnal.org/Pdf/O_Come_All_Ye_Faithful-Adeste_Fideles-Portugese_Hymn.pdf) | Public domain | 1–5 underlaid; 6–8 as text (as in source) | ♩ = 120 | 40 s | [mscz](o-come-all-ye-faithful/o-come-all-ye-faithful.mscz) · [pdf](o-come-all-ye-faithful/o-come-all-ye-faithful.pdf) · [starter](o-come-all-ye-faithful/source/O_Come_All_Ye_Faithful-Adeste_Fideles-Portugese_Hymn.pdf) |
| 2 | Hark! The Herald Angels Sing | F. Mendelssohn (*Festgesang*, 1840); setting W. H. Cummings 1857 | Charles Wesley 1739, alt. | [Open Hymnal](http://openhymnal.org/Pdf/Hark_The_Herald_Angels_Sing-Mendelssohn.pdf) | Public domain | 1–5 | ♩ = 100 | 48 s | [mscz](hark-the-herald-angels-sing/hark-the-herald-angels-sing.mscz) · [pdf](hark-the-herald-angels-sing/hark-the-herald-angels-sing.pdf) · [starter](hark-the-herald-angels-sing/source/Hark_The_Herald_Angels_Sing-Mendelssohn.pdf) |
| 3 | Silent Night | F. X. Gruber 1818; setting *Concordia Kinderchöre* 1908 | Joseph Mohr 1818; tr. J. F. Young (st. 1, 3), anon. (st. 2, 4) | [Open Hymnal](http://openhymnal.org/Pdf/Silent_Night-Stille_Nacht.pdf) | Public domain | 1–4 | ♩ = 60 | 36 s | [mscz](silent-night/silent-night.mscz) · [pdf](silent-night/silent-night.pdf) · [starter](silent-night/source/Silent_Night-Stille_Nacht.pdf) |
| 4 | Joy to the World | after Handel (*Antioch*); setting Lowell Mason 1836 | Isaac Watts 1719 | [Open Hymnal](http://openhymnal.org/Pdf/Joy_To_The_World-Antioch.pdf) | Public domain | 1–4 | ♩ = 80 | 29 s | [mscz](joy-to-the-world/joy-to-the-world.mscz) · [pdf](joy-to-the-world/joy-to-the-world.pdf) · [starter](joy-to-the-world/source/Joy_To_The_World-Antioch.pdf) |
| 5 | God Rest Ye Merry, Gentlemen | traditional English; setting *Carols Old and Carols New* 1918 | traditional English | [Open Hymnal](http://openhymnal.org/Pdf/God_Rest_Ye_Merry_Gentlemen-God_Rest_Ye_Merry_Gentlemen.pdf) | Public domain | 1–5 underlaid; 6–8 as text (as in source) | ♩ = 160 | 28 s | [mscz](god-rest-ye-merry-gentlemen/god-rest-ye-merry-gentlemen.mscz) · [pdf](god-rest-ye-merry-gentlemen/god-rest-ye-merry-gentlemen.pdf) · [starter](god-rest-ye-merry-gentlemen/source/God_Rest_Ye_Merry_Gentlemen-God_Rest_Ye_Merry_Gentlemen.pdf) |
| 6 | The First Noel | traditional English; setting *Methodist Sunday School Hymnal* 1911 | traditional English | [Open Hymnal](http://openhymnal.org/Pdf/The_First_Noel-The_First_Noel.pdf) | Public domain | 1–5 | ♩ = 100 | 43 s | [mscz](the-first-noel/the-first-noel.mscz) · [pdf](the-first-noel/the-first-noel.pdf) · [starter](the-first-noel/source/The_First_Noel-The_First_Noel.pdf) |
| 7 | O Little Town of Bethlehem | L. H. Redner (*St. Louis*) 1868; setting *The Chapel Hymnal* 1898 | Phillips Brooks 1867 | [Open Hymnal](http://openhymnal.org/Pdf/O_Little_Town_Of_Bethlehem-St_Louis.pdf) | Public domain | 1–5 | ♩ = 100 | 38 s | [mscz](o-little-town-of-bethlehem/o-little-town-of-bethlehem.mscz) · [pdf](o-little-town-of-bethlehem/o-little-town-of-bethlehem.pdf) · [starter](o-little-town-of-bethlehem/source/O_Little_Town_Of_Bethlehem-St_Louis.pdf) |
| 8 | In the Bleak Midwinter | Gustav Holst (*Cranham*) 1906, alt.; Holst's own setting | Christina Rossetti 1872, alt. | [Open Hymnal](http://openhymnal.org/Pdf/In_The_Bleak_MidWinter-Cranham.pdf) | Public domain (US; life + 70 since 2005) | 1–5 | ♩ = 100 | 38 s | [mscz](in-the-bleak-midwinter/in-the-bleak-midwinter.mscz) · [pdf](in-the-bleak-midwinter/in-the-bleak-midwinter.pdf) · [starter](in-the-bleak-midwinter/source/In_The_Bleak_MidWinter-Cranham.pdf) |
| 9 | Angels from the Realms of Glory | Henry Smart (*Regent Square*) 1867; setting *Psalms and Hymns for Divine Worship* 1867 | James Montgomery 1816 | [Open Hymnal](http://openhymnal.org/Pdf/Angels_From_The_Realms_Of_Glory-Regent_Square.pdf) | Public domain | 1–5 | ♩ = 100 | 29 s | [mscz](angels-from-the-realms-of-glory/angels-from-the-realms-of-glory.mscz) · [pdf](angels-from-the-realms-of-glory/angels-from-the-realms-of-glory.pdf) · [starter](angels-from-the-realms-of-glory/source/Angels_From_The_Realms_Of_Glory-Regent_Square.pdf) |
| 10 | It Came Upon the Midnight Clear | R. S. Willis (*Carol*) 1850s; setting *Order of Worship…Reformed Church* 1866 | E. H. Sears 1849 | [Open Hymnal](http://openhymnal.org/Pdf/It_Came_Upon_A_Midnight_Clear-Carol.pdf) | Public domain | 1–5 | ♩ = 60 (in 6/8) | 48 s | [mscz](it-came-upon-the-midnight-clear/it-came-upon-the-midnight-clear.mscz) · [pdf](it-came-upon-the-midnight-clear/it-came-upon-the-midnight-clear.pdf) · [starter](it-came-upon-the-midnight-clear/source/It_Came_Upon_A_Midnight_Clear-Carol.pdf) |
| 11 | What Child Is This? | *Greensleeves*, 16th-c. English; traditional setting, *Sunday School Hymnal and Service Book* 1871 | W. C. Dix 1865 | [Open Hymnal](http://openhymnal.org/Pdf/What_Child_Is_This-Greensleeves.pdf) | Public domain | 1–3 | ♩ = 80 (in 6/8) | 36 s | [mscz](what-child-is-this/what-child-is-this.mscz) · [pdf](what-child-is-this/what-child-is-this.pdf) · [starter](what-child-is-this/source/What_Child_Is_This-Greensleeves.pdf) |
| 12 | Good King Wenceslas | *Tempus Adest Floridum* (*Piae Cantiones* 1582); setting *Carols Old and Carols New* 1916 | J. M. Neale 1853 | [Open Hymnal](http://openhymnal.org/Pdf/Good_King_Wenceslas-Tempus_Adest_Floridum.pdf) | Public domain | 1–5 | ♩ = 140 | 29 s | [mscz](good-king-wenceslas/good-king-wenceslas.mscz) · [pdf](good-king-wenceslas/good-king-wenceslas.pdf) · [starter](good-king-wenceslas/source/Good_King_Wenceslas-Tempus_Adest_Floridum.pdf) |

In every carol the lyrics are on the **Soprano staff only**. "Stanzas included" counts
whole stanzas, never one stanza laid out over a repeat; none of these carols has a repeat.
**No stanza present in a source was omitted.** Each carol's `NOTES.md` gives full details:
the refrain lines, parenthesised notes, dotted ties, and anything specific to that carol.

**The durations are for one pass through the music.** The stanzas are stacked under the
same notes, as in the hymnal, and no repeats were added, so playback plays the music
once. Even if the music were replayed once for every underlaid stanza, the longest would
be about 4 minutes (*Hark!* and *It Came Upon*: 5 × 48 s).

## Directory layout

```
christmas-carols-satb/
├── PROMPT.md                 the brief
├── README.md                 this file
├── build.sh                  starter ABC -> SATB .mscz (CLI stage; see "How the scores were made")
├── verify-carols.sh          re-runnable checks of everything claimed below
├── tools/                    pipeline scripts, shared style, carol list
├── evidence/                 output of verify-carols.sh and the Muse Sounds check
├── screenshots/              GUI screenshots (see "Verification")
└── <carol-slug>/
    ├── <carol-slug>.mscz     SATB score, Muse Choir pinned (GUI-saved)
    ├── <carol-slug>.pdf      PDF export (A4)
    ├── NOTES.md              per-carol notes
    └── source/
        ├── <Name>.pdf        starter score, unmodified (Open Hymnal)
        ├── <Name>.abc        the same edition's ABC source, unmodified
        ├── <Name>.mid        the same edition's MIDI, unmodified (used only for checking)
        └── openhymnal-copying.txt   Open Hymnal's copying/licence page
```

## Environment

| Item | Value |
|---|---|
| OS | Ubuntu 24.04.2 LTS, kernel 7.0.0-38-generic, GNOME on Wayland (MuseScore via XWayland) |
| MuseScore Studio | **4.7.7**, build `b750c43` (AppImage, `~/.local/bin/musescore`) |
| MuseSampler | `libMuseSamplerCoreLib.so` **0.106.0** |
| Muse Choir | installed under `~/Muse Sounds/Muse Choir/` (607 MB); presets Sopranos, Altos, Tenors, Basses |
| Muse Sounds Manager | 2.2.1.953 (`tar.gz` build) |
| abc2xml | v269 by Willem Vree (<https://wim.vree.org/svgParse/abc2xml.html>), run with pyparsing 3.3.3 |
| music21 | 10.5.2 (only for the MIDI cross-check) |

These are the same MuseScore and MuseSampler versions as the earlier experiment, so its
findings carry over unchanged.

## Reproducing playback on another machine

Install MuseScore Studio 4.x, Muse Sounds Manager, and the Muse Choir library. The steps,
including the no-root `tar.gz` installer for Linux, are in the earlier experiment's
[Reproducing this on another machine](../musescore-choir-experiment/README.md#reproducing-this-on-another-machine).
Then open any `<slug>/<slug>.mscz` and press F10 for the Mixer. The Sound row should read
Sopranos, Altos, Tenors, Basses. If it reads MS Basic, MuseSampler was not found, and
**that failure is silent**
([FINDINGS.md, finding 2](../musescore-choir-experiment/FINDINGS.md#2-muse-sounds-fails-silently--the-exit-code-lies)).

To rebuild the scores from the starter files you also need Python 3 with `pyparsing`, and
`abc2xml.py` v269. abc2xml is not committed; it is third-party (LGPL).

```bash
ABC2XML=/path/to/abc2xml.py ./build.sh            # writes build/<slug>.mscz (git-ignored)
```

`build.sh` produces the **CLI stage** only. The committed scores were then opened in the
GUI and saved with Ctrl+S. That save is what writes the explicit Muse Choir entries into
`audiosettings.json`: a CLI-written `.mscz` has an empty `tracks[]` and resolves its sounds
at load time (see the earlier experiment's FINDINGS, "Smaller observations").

## How the scores were made

Every carol was **converted from the edition's own source code, not transcribed**. Open
Hymnal publishes each hymn as an ABC file, and typesets its PDF from that file with
abcm2ps. Converting the ABC therefore reads exactly the note data the starter PDF was
printed from, with no OMR and no manual entry. The steps, all in `build.sh`:

1. `tools/prep_abc.py` changes only the staff layout: `%%staves (S1V1 S1V2) | (S2V1 S2V2)`
   becomes one staff per voice, and the voices are named Soprano, Alto, Tenor and Bass. It
   also passes the custom `!()!` (parenthesised note) decoration through as `!open!`,
   because abc2xml would otherwise drop it.
2. **abc2xml** converts the ABC to MusicXML.
3. `tools/fix_xml.py` sets `voice.*` instrument sounds in place of the ABC's piano MIDI
   program; gives the Tenor an octave-treble clef (display only, since pitches are
   absolute); turns `!open!` into parenthesised noteheads; removes the forced stem
   directions; and tidies the title and credits. Notes, rhythms, ties, slurs (including
   dotted), lyrics and tempo pass through untouched.
4. MuseScore imports the MusicXML with the shared style `tools/carols.mss` (A4, extra
   lyric spacing). Because the parts are named Soprano, Alto, Tenor and Bass with `voice.*`
   sounds, MuseScore assigns its `soprano`, `alto`, `tenor` and `bass` instruments, and
   under the MuseSounds profile those resolve to Muse Choir.
5. `tools/add_text_stanzas.py` copies stanzas that the source prints as text only
   (*O Come*, *God Rest Ye*: stanzas 6–8) into a text frame at the end.
6. **GUI step:** each score was opened in MuseScore 4.7.7 and saved with Ctrl+S, then
   MuseScore was closed before the next one. This was automated with xdotool (an
   unpackaged local copy; nothing was installed system-wide).

**Restructuring, the same for all twelve:** the source's two-staff short score
(S + A on treble, T + B on bass) became four staves, with the Tenor on an octave-treble
clef. The organ-intro brackets (⌐ ¬) and page furniture (category label, scripture refs,
metre) were dropped. Each carol's `NOTES.md` has the specifics.

## Sound assignments

Verified by reading `audiosettings.json` inside every committed `.mscz`
(`verify-carols.sh`, check 2). All twelve are identical:

| Staff | `instrumentId` | Library | Preset |
|---|---|---|---|
| Soprano | `soprano` | Muse Choir | Sopranos |
| Alto | `alto` | Muse Choir | Altos |
| Tenor | `tenor` | Muse Choir | Tenors |
| Bass | `bass` | Muse Choir | Basses |

`activeSoundProfile` is `MuseSounds`. The metronome track stays on MS Basic, as in the
earlier experiment.

**Muse Sounds is actually engaged.** Two scores were rendered headless under both
profiles: [`evidence/musesounds-engagement.txt`](evidence/musesounds-engagement.txt).
The MuseSounds and MS Basic MP3s differ (*Silent Night* `ef70e072…` vs `301b70b4…`;
*Good King Wenceslas* `5febb4d2…` vs `bba45579…`). The earlier experiment showed that
renders are deterministic and that the MuseSounds profile collapses to the MS Basic bytes
when the sampler is missing, so a difference means Muse Choir produced the audio. No MP3s
are committed; the brief makes them optional.

**What you hear is vowel-based choral playback, not sung lyrics.** Muse Choir ignores
lyric text. The earlier experiment verified this with byte-identical renders with and
without lyrics, and it was not re-tested here because the versions are identical.

### Documented vs observed

- **Documented:** nothing in this README rests on official MuseScore or Muse Sounds
  documentation. No official page was found covering CLI rendering with Muse Sounds,
  `audiosettings.json`, or Muse Choir and lyrics. A handbook URL that looked likely
  (`musescore.org/en/handbook/4/muse-sounds`) returned HTTP 404, so no documentation link
  is given.
- **Observed** (this experiment and the earlier one, same versions): the preset mapping
  above, the headless rendering, the silent fallback, lyrics having no effect, and
  CLI-saved files leaving `tracks[]` empty.

## Verification

Run `./verify-carols.sh` (set `PYTHON` to an interpreter with music21 to include the MIDI
cross-check). Its last output is in
[`evidence/verify-carols-run.txt`](evidence/verify-carols-run.txt). It runs these checks
for each carol:

1. **Four labelled staves.** `musescore --score-meta` opens the `.mscz` and reports exactly
   four parts, Soprano, Alto, Tenor and Bass. **12/12 pass.**
2. **Muse Choir presets** read from `audiosettings.json`. **12/12 pass.**
3. **Duration ≤ 5 minutes** from `--score-meta`. **12/12 pass** (28–48 s).
4. **The PDF exists**, with a sensible page count. **12/12 pass:** 1 page (4 carols) or
   2 pages (8 carols). Where there is a second page it holds the last system and, for
   *O Come* and *God Rest Ye*, the text stanzas.
5. **The starter files are present** (PDF and ABC). **12/12 pass.**
6. **Notes against an independent rendering.** Every voice's sequence of pitches and
   onset intervals is searched for in the edition's own MIDI file. Open Hymnal made that
   MIDI from the same ABC with abc2midi, a different converter from abc2xml, so this
   catches conversion errors in pitch or rhythm. **8/12 match exactly. The other 4**
   (*O Come*, *First Noel*, *O Little Town*, *Bleak Midwinter*) **match once same-pitch
   splits are merged.** Those carols use dotted ties and parenthesised notes for
   stanza-dependent rhythms, and the MIDI plays a different stanza's version at those
   points. The merged comparison cannot tell a tie from a re-struck note, so those spots
   were also checked visually.

Beyond the script:

- **Visual comparison**, page against page, of each rendered PDF with its starter PDF.
  This covered the notes, the ties and slurs (including dotted ones), accidentals, stanza
  numbering, parenthesised notes and the text stanzas. It was done at page resolution, so
  check 6 is the note-by-note guarantee and the visual pass is the backstop for notation.
- **GUI open** of every score during the Ctrl+S step: each opened without error, in a
  window titled with the score's name.
- **Screenshots and reopen-after-restart:** see [Known limitations](#known-limitations).

## Rights

For each carol the **composition and text** (composer, harmoniser, author, translator) are
listed above and in its `NOTES.md`. Every one is public domain: the people involved died
before 1955, and every setting was published before 1929 (the US public-domain line).
*In the Bleak Midwinter* (Holst, d. 1934) is the latest; it is public domain in the US and
in life + 70 countries since 2005.

The **edition**, meaning Open Hymnal's encoding and typesetting, is a separate matter. Each
score states *"copyright: public domain. This score is a part of the Open Hymnal Project"*,
and the project's copying page ([saved copy](o-come-all-ye-faithful/source/openhymnal-copying.txt)
in every `source/` folder) places the project's own work in the public domain. That page
assesses status under **US law** and leaves other jurisdictions to the user. On that basis
the starter PDFs, ABC and MIDI files are **kept in the repository**; none are only
linked. Nothing required a login, payment, or getting past a download limit or bot check.

Some ABC files also cite *Lutheran Worship* (1982) as a music source next to the
19th-century setting they credit (*Hark!*, *Silent Night*, *Joy to the World*,
*O Little Town*, *What Child*). The credited settings are public domain. If the 1982 book
introduced any editorial changes, Open Hymnal has still marked the result public domain.
This was not checked independently against the original 19th-century printings.

## Known limitations

1. **Screenshots and the restart test: see the pull request.** The GUI step worked, but
   when the screenshots were taken GNOME was opening every new MuseScore window minimised
   (`WM_STATE: Iconic`), and the window could not be restored from a script. GNOME Shell
   `Eval` is disabled, `_NET_ACTIVE_WINDOW` requests were ignored, and XWayland cannot
   capture an unmapped window. The pull request records whether this was resolved; until
   `screenshots/` holds files, treat the mixer and restart check as **not performed**.
   What *was* verified without a screenshot: MuseScore was fully quit after each GUI save,
   and `audiosettings.json` was then read from the files on disk (check 2).
2. **Lyrics are not sung.** Muse Choir plays vowels; see above.
3. **Lyrics are on the Soprano staff only**, as in the source's short score. Alto, Tenor
   and Bass have no words.
4. **Playback is one pass through the music** and does not repeat it for each stanza.
5. **Stanza-dependent notation follows stanza 1 in playback.** Dotted ties play as ties,
   and parenthesised notes are played.
6. **The visual proofread was page-level.** Note-level correctness rests on the automated
   MIDI cross-check (check 6).
7. **US-centred rights assessment** (Open Hymnal's own). Holst is the only figure whose
   status depends on jurisdiction, and he is public domain under life + 70 as well.
8. **Text alterations.** Several sources mark the words or music "alt." (altered by
   editors over the years). The scores reproduce Open Hymnal's text as it is, not the
   original texts.

## Considered and rejected

| Candidate | Reason |
|---|---|
| CPDL editions | CPDL returns HTTP 403 to automated requests (as the earlier experiment found); not tried further |
| musescore.com uploads | Downloads require a login, which the brief rules out |
| Mutopia Project | Only four carols on a "carol" search, mostly melody-only (e.g. *Good King Wenceslas* "for Voice"); LilyPond is not installed to convert them |
| IMSLP hymnal scans | Scans only (PDF), with download timers for non-members; would need full manual transcription, while Open Hymnal offers the same public-domain settings with machine-readable source |
| *Once in Royal David's City*, *While Shepherds Watched* | Not in the Open Hymnal 2026.11 collection |
| *Away in a Manger* (Open Hymnal) | Encoded as chords on two staves (`V: S1`, `V: S2`) rather than four separate voices, so it cannot be split into SATB without guessing the voice-leading |
| *Angels We Have Heard on High* (Open Hymnal) | Setting by Edward Shippen Barnes (1887–1958): public domain in the US, but still in copyright in life + 70 countries until 2029 |

## Could not be verified

- Official MuseScore or Muse Sounds documentation for any of the playback behaviour
  described here (see "Documented vs observed").
- The reliability of Open Hymnal's own transcription against the original printed
  hymnals. The check here is "faithful to the Open Hymnal edition", not "faithful to the
  1857, 1898, … printings".
- Lyric-driven phoneme playback in Muse Choir. It was not observed in the earlier
  experiment and was not re-tested.
