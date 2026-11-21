# MuseScore SATB choir playback experiment

**Purpose.** Determine whether MuseScore Studio on this desktop can play a four-part
SATB choral score using a real vocal sound library, and produce a saved, reviewable
score that demonstrates it.

**Outcome.** Successful. All four voices play through **Muse Sounds → Muse Choir**
(Sopranos / Altos / Tenors / Basses), the assignments survive saving and reopening, and
Muse Choir also works for **headless command-line rendering**, not just the GUI.

One requirement could not be met as asked: Muse Choir does **not** sing the notated
lyrics. This was tested directly rather than assumed — see
[What playback actually supports](#what-playback-actually-supports).

> **Findings that apply beyond this experiment are collected in
> [`FINDINGS.md`](FINDINGS.md)** — Muse Sounds working for headless CLI rendering (which
> contradicts the repository's top-level README), Muse Sounds failing *silently* back to
> MS Basic with a zero exit code, and Muse Choir ignoring lyrics. Re-check them at any
> time with [`./verify-findings.sh`](verify-findings.sh).

---

## Environment

| Item | Value |
|---|---|
| Operating system | Ubuntu 24.04.2 LTS, kernel 7.0.0-38-generic |
| Desktop session | GNOME on Wayland (MuseScore runs via XWayland) |
| MuseScore Studio | **4.7.7**, build `b750c43` (AppImage) |
| AppImage path | `~/Applications/MuseScore-Studio-4.7.7.261109195-x86_64.AppImage` |
| CLI entry point | `~/.local/bin/musescore` → the AppImage above |
| Muse Sounds Manager | **2.2.1.953** (unpackaged `tar.gz` build) |
| MuseSampler | `libMuseSamplerCoreLib.so` **version 0.106.0**, 10,805,120 bytes |
| Sampler path | `~/.local/share/MuseSampler/lib/` |
| Sound library path | `~/Muse Sounds/` — 11 libraries, 17 GB total |
| Muse Choir size | 607 MB |

A second MuseScore AppImage (4.5.2) is also present on this machine but was **not**
used; `~/.local/bin/musescore` points at 4.7.7.

---

## The work

| Field | Value |
|---|---|
| Title | *O Haupt voll Blut und Wunden* |
| Work | Chorale No. 54 from the *St Matthew Passion*, BWV 244 |
| Composer | Johann Sebastian Bach (1685–1750) |
| Chorale melody | Hans Leo Hassler (1564–1612), *Mein G'müt ist mir verwirret* |
| Text | Paul Gerhardt (1607–1676), after *Salve caput cruentatum* |
| Voicing | SATB, a cappella (four vocal staves) |
| Excerpt? | **Complete movement** — not an excerpt |
| Measures | 15 (a pickup bar numbered 0, then bars 1–14) with one backward repeat |
| Key signature | One flat |
| Time signature | 4/4 (common time) |
| Fermatas | 24 (phrase endings, as normal for a Bach chorale) |
| Saved tempo | ♩ = 72 |
| Verified duration | **1:09.72** (MP3); MuseScore's own metadata reports 67 s |

Both durations are well inside the five-minute limit. The small gap between them is the
reverb tail at the end of the rendered audio.

### Source and rights

The notes were **not** hand-entered. They come from an existing MusicXML encoding:

- **Source file:** `music21` corpus, `music21/corpus/bach/bwv244.54.mxl`
- **Source URL:** https://github.com/cuthbertLab/music21/blob/master/music21/corpus/bach/bwv244.54.mxl
- **Retrieved:** 21 November 2026, via the GitHub contents API
- **Encoding credit carried inside the file:** `PDF © 2004 Margaret Greentree — used by permission`
- **Encoding software recorded in the file:** music21 v5.3.0 / MuseScore 2.1.0, encoded 2018-08-11

Rights, with the composition and the encoding kept separate:

- **The composition** is unambiguously public domain. Bach died in 1750; the chorale
  melody and text are older still.
- **The encoding** is a modern work with its own terms. It derives from Margaret
  Greentree's Bach chorale edition and is distributed in the music21 corpus. The corpus
  licence (saved here as `source/music21-corpus-license.txt`) states that works are
  "either out of copyright in the United States or licensed for use", that the
  "encodings may be under copyright but have been licensed for use", and that **there
  may be restrictions on commercial use**.

So: fine for this non-commercial experiment, and the Greentree attribution is preserved
in the score's footer. Anyone reusing this encoding commercially should check the terms
first. Nothing was paid for and no access restriction was bypassed.

CPDL was tried first but blocks automated requests (HTTP 403), so the music21 corpus was
used instead.

### Changes made to the source

| Change | Reason |
|---|---|
| Added tempo ♩ = 72 | The source encoding had **no** tempo marking at all; without one MuseScore defaults to 120, which is far too fast for this chorale |
| Set title, subtitle, composer | The source's title fields both read literally `bwv244.54.mxl` |
| Replaced a `BWV 244.54` credit block | It was overriding the title frame |
| Fixed footer spacing | Two adjacent `<credit-words>` rendered as `Greentreeused by permission`; now reads `Greentree — used by permission` |

**No notes, rhythms, rests, clefs, key or time signatures, fermatas, repeats or lyrics
were altered.** The German text is present as encoded: **one stanza** of Gerhardt's
hymn (all eight lines), laid out as two lyric lines under the repeated opening, and only
on the **Soprano staff** — the Alto, Tenor and Bass staves carry no lyrics in the source
encoding. Bach's setting in the Passion uses a second stanza (*Du edles Angesichte*),
which is **not** in this encoding and was not added.

Worth flagging: the **Tenor staff uses a bass clef**, as in the source encoding, rather
than the octave-treble clef often used in modern vocal scores. This was preserved
deliberately. It does not affect playback pitch.

---

## Sound assignments

Read directly from `audiosettings.json` inside the saved `.mscz`, and confirmed visually
in the Mixer (screenshots 02 and 03).

Note the distinction the brief asks for: the **staff instrument names** are singular
(Soprano, Alto, Tenor, Bass); the **sounds actually selected** are the plural Muse Choir
section presets.

| Staff | `instrumentId` | Library (`musePack`) | Preset (`museName`) | `museUID` | `playbackSetupData` |
|---|---|---|---|---|---|
| Soprano | `soprano` | Muse Choir | **Sopranos** | 19 | `voices.choir.soprano` |
| Alto | `alto` | Muse Choir | **Altos** | 20 | `voices.choir.alto` |
| Tenor | `tenor` | Muse Choir | **Tenors** | 21 | `voices.choir.tenor` |
| Bass | `bass` | Muse Choir | **Basses** | 22 | `voices.choir.bass` |

All four are `"type": "muse_sampler_sound_pack"`, `"vendor": "MuseSounds"`.

Also present, and deliberately left alone:

- **Metronome** — `MS Basic`, `"type": "fluid_soundfont"`, `"vendor": "Fluid"`. This is
  the only part of the score not using Muse Sounds.
- **Muse Reverb** on aux 1, with a 0.3 send from each of the four voices. This is
  MuseScore's default for Muse Sounds, not something configured here.
- `activeSoundProfile` is `MuseSounds`.

Muse Choir ships seven presets — `Sopranos`, `Altos`, `Tenors`, `Basses`, `Men`,
`Women`, `Full Choir`. The four section presets were used.

### A detail worth knowing

When the `.mscz` is written by the **command line**, `audiosettings.json` contains
`"activeSoundProfile": "MuseSounds"` but an **empty** `"tracks": []`. The sounds are
resolved at load time from the profile plus each staff's instrument ID. Playback is
correct, but nothing is pinned in the file.

After opening the score in the GUI and pressing Ctrl+S, `tracks[]` is written out in
full with the explicit Muse Choir resource metadata shown in the table above. **The
version saved in this directory is the GUI-saved one**, so the assignments are explicit
rather than inferred.

---

## How playback was tested

Every check below was actually run; nothing here is assumed.

**1. The sampler loads.** On each load MuseScore logs:

```
MuseSamplerResolver::init | MuseSampler successfully inited:
  /home/daniel/.local/share/MuseSampler/lib/libMuseSamplerCoreLib.so, version: 0.106.0
MuseSamplerWrapper::initSampler | Successfully initialized sampler ...   (×4)
```

Four initialisations — one per SATB staff.

**2. Muse Choir really is doing the synthesis.** The strongest evidence, because it
rules out a different Fluid preset masquerading as Muse Sounds. First, renders were
confirmed byte-for-byte deterministic (the same score rendered twice under MS Basic gave
an identical MD5). Then:

| Condition | MP3 MD5 (first 8) |
|---|---|
| `--sound-profile MuseSounds`, sampler present | `6937d2f5` |
| `--sound-profile "MuseScore Basic"` | `bff1bc21` |
| `--sound-profile MuseSounds`, **sampler library temporarily renamed** | `bff1bc21` |

With the sampler hidden, the MuseSounds render collapses to be *byte-identical* to the
MS Basic render. So MuseSampler is genuinely producing the audio — and **Muse Sounds
fails silently back to MS Basic when the sampler is missing**, with no warning and a
zero exit code. The library was renamed back immediately and verified restored.

**3. Each voice individually.** Each part was extracted to its own single-staff score
and rendered under both profiles. All four differ between profiles, so all four are
genuinely on Muse Choir:

| Voice | Notated range | Duration | Mean level | MuseSounds vs MS Basic |
|---|---|---|---|---|
| Soprano | G4–G5 | 1:09.72 | −29.5 dB | differs |
| Alto | D4–C5 | 1:09.72 | −34.7 dB | differs |
| Tenor | G3–A4 | 1:09.72 | −27.5 dB | differs |
| Bass | G2–D4 | 1:09.72 | −32.8 dB | differs |

Every range sits in the correct tessitura for its voice, and every render is audible.

**4. The full ensemble.** 1:09.72, mean −24.2 dB, peak −7.3 dB. The MS Basic comparison
render is 1:09.72, mean −26.5 dB.

**5. Persistence across save and reopen.** The score was saved from the GUI, MuseScore
was fully closed (process exit confirmed), and the score reopened. On reopen the sampler
again initialised four times and the Mixer still showed Sopranos / Altos / Tenors /
Basses — screenshot `03-mixer-after-close-and-reopen.png`.

**6. Headless rendering.** All exports in `exports/` were produced with
`QT_QPA_PLATFORM=offscreen` from the command line, with Muse Choir active.

### What was checked against the source

The notes were taken from an existing encoding rather than transcribed, so note-by-note
proofreading against a separate edition was **not** performed — this is the main
verification gap. What was checked: part names and count (4: Soprano/Alto/Tenor/Bass),
measure count (15), key signature (one flat), time signature (4/4), clefs (G, G, F, F),
fermata count (24), repeat structure (one backward repeat, present in all four parts),
and that the lyric text (one stanza, Soprano staff only) survived the round-trip. MuseScore's `--score-meta`
independently confirms 15 measures, 4/4, key −1, tempo 72 and four parts.

---

## What playback actually supports

**Muse Choir does not sing the notated lyrics on this setup.** This was tested, not
inferred: a copy of the score with all 52 lyric elements stripped out was rendered under
Muse Choir and compared with the normal render. The two MP3s are **byte-identical**
(`6937d2f5` both). The German text therefore has *no* effect whatsoever on the audio.

What you actually hear is a sustained vowel choir — Muse Choir is built on vowel samples
(the library is advertised with *Ahh*, *Ooh* and *Mmm*). Every syllable is sung on the
same vowel; the lyrics exist in the notation and the PDF only.

It has been reported that lyric text can trigger different phoneme samples in choral
libraries, and MuseScore forum threads report this working inconsistently or not at all.
**No official documentation link was found to support this, so treat it as an
unverified claim; in any case it was not observed here** — on MuseScore
4.7.7 with Muse Choir and MuseSampler 0.106.0, stripping the lyrics changed nothing. It
is possible the feature requires different markup, a different library, or a setting not
found during this experiment.

Other limitations observed or relevant:

- Vowel samples have a slow attack, so fast passages can sound late. Not a problem at
  ♩ = 72 in a chorale, but it would be in quicker music.
- The metronome track stays on MS Basic; it is not a Muse Sounds instrument.
- Muse Sounds requires a Muse account to download. The libraries themselves then work
  offline.

---

## Reproducing this on another machine

**Dependencies:** MuseScore Studio 4.x, Muse Sounds Manager, and the Muse Choir library
(607 MB). Muse Sounds will not work from the soundfont alone — the closed-source
`libMuseSamplerCoreLib.so` must be present.

1. Install MuseScore Studio 4.7.7 (AppImage from https://musescore.org/en/download).
2. Install Muse Sounds Manager. On Linux it is **not** called Muse Hub:
   - `.deb` — https://muse-cdn.com/Muse_Sounds_Manager_x64.deb (needs root)
   - `.rpm` — https://muse-cdn.com/Muse_Sounds_Manager_x64.rpm (needs root)
   - `.tar.gz` — https://muse-cdn.com/Muse_Sounds_Manager_x64.tar.gz (**no root needed**)

   The `tar.gz` was used here because this machine has no passwordless `sudo`. It is
   self-contained: extract it and run `bin/muse-sounds-manager`. Its auto-updater is
   disabled, so updates are manual. Requires glibc ≥ 2.34 (this machine has 2.39).
3. Sign in with a Muse account in Muse Sounds Manager and install **Muse Choir**. It
   lands in `~/Muse Sounds/Muse Choir/` and the bridge in `~/.local/share/MuseSampler/`.
4. Restart MuseScore, then open `bwv244-54-o-haupt-voll-blut-und-wunden.mscz`.

**To check playback:** open the Mixer (F10). The Sound row should read Sopranos, Altos,
Tenors, Basses. If it reads *MS Basic* instead, MuseScore has not found MuseSampler —
remember that this failure is silent.

**To re-render from the command line:**

```bash
QT_QPA_PLATFORM=offscreen musescore --sound-profile MuseSounds \
  -o out.mp3 bwv244-54-o-haupt-voll-blut-und-wunden.mscz
```

---

## Files

```
musescore-choir-experiment/
├── README.md                                        this file
├── FINDINGS.md                                      findings that apply repo-wide
├── PROMPT.md                                        the original task brief
├── verify-findings.sh                               re-runnable check of every finding
├── bwv244-54-o-haupt-voll-blut-und-wunden.mscz      MAIN SCORE (GUI-saved, assignments pinned)
├── evidence/
│   ├── verification-run.txt                         output of verify-findings.sh
│   └── musesampler-init-log.txt                     MuseScore loading the sampler 4x
├── source/
│   ├── bwv244.54.mxl                                unmodified source encoding as downloaded
│   ├── bwv244.54-prepared.musicxml                  source + tempo and title edits
│   └── music21-corpus-license.txt                   corpus licence text
├── exports/
│   ├── bwv244-54-o-haupt-voll-blut-und-wunden.pdf             2-page score
│   ├── ...-musesounds.mp3                           Muse Choir render (the demonstration)
│   ├── ...-msbasic.mp3                              MS Basic render, for comparison
│   └── per-voice/
│       ├── soprano-muse-choir.mp3                   each voice alone, Muse Choir
│       ├── alto-muse-choir.mp3
│       ├── tenor-muse-choir.mp3
│       └── bass-muse-choir.mp3
└── screenshots/
    ├── 01-satb-score-in-musescore.png               all four labelled staves
    ├── 02-mixer-muse-choir-assignments.png          Mixer showing the four presets
    └── 03-mixer-after-close-and-reopen.png          same, after a full reopen
```

---

## Known limitations and unresolved problems

1. **Lyrics are not sung.** Verified byte-identical renders with and without lyrics. The
   lyric-driven phoneme playback reported elsewhere (unsourced; see above) was not observed here.
2. **No independent note-by-note proofread.** The notes come from the Greentree/music21
   encoding and were checked structurally, not compared bar-by-bar against a separate
   edition such as the Neue Bach-Ausgabe.
3. **Muse Sounds fails silently.** If MuseSampler is missing, `--sound-profile MuseSounds`
   still exits 0 and still writes an MP3 — one rendered in MS Basic. Always verify the
   output rather than trusting the exit code.
4. **Encoding licence is not fully open.** Public-domain composition, but the encoding
   may carry commercial-use restrictions.
5. **Screenshots needed a workaround.** GNOME's Wayland screenshot D-Bus method returns
   `AccessDenied`, and `import -window root` fails under Wayland. The screenshots here
   were captured from MuseScore's XWayland window with `import -window <id>`, using a
   locally extracted `xdotool` (no root) to drive the GUI. Nothing was installed
   system-wide.
6. **No official documentation links.** Capability statements here rest on the tests
   described above, not on cited MuseScore or Muse Sounds documentation.

## Note for the parent repository

The top-level `README.md` of `musescore-scores` states that *"Muse Sounds is not
installed for command-line rendering."* **That is now out of date** — Muse Sounds is
installed and verified working headlessly. `tools/publish-score` already accepts
`--sound-profile MuseSounds`, so existing scores can be re-rendered with Muse Sounds
without any tooling change.

Two files need changing together to correct this, because the second regenerates the
first: the sentence in the top-level `README.md`, and `tools/build-index.py:73` which
emits it. Neither was touched here, both being outside the experiment directory.

Before switching published pieces over, read the caveat in
[`FINDINGS.md`](FINDINGS.md): Muse Sounds is a ~17 GB local install requiring a Muse
account, and it fails *silently* to MS Basic on machines that lack it — with a zero exit
code. MS Basic remains the right default for `publish-score`.
