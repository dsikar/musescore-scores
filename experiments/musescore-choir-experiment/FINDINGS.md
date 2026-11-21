# Findings

Four reusable findings about Muse Sounds on this desktop, separated out from the
experiment write-up because they apply to **any** score in this repository, not just the
chorale used to test them.

Each one was verified by experiment, not inferred from documentation. Every claim below
can be re-checked by running:

```bash
./verify-findings.sh
```

That script re-renders the score under both sound profiles, temporarily hides the
sampler library, strips the lyrics, and compares MD5s. Its output is saved to
`evidence/verification-run.txt`; the run that produced the numbers quoted here is
committed alongside this file.

Environment: Ubuntu 24.04.2, MuseScore Studio **4.7.7** build `b750c43`, MuseSampler
**0.106.0**, Muse Choir 607 MB, Muse Sounds Manager 2.2.1.953.

---

## 0. Renders are byte-for-byte deterministic

This one is load-bearing: the other findings compare MD5s, and that is only meaningful
if identical inputs give identical bytes.

Rendering the same score twice under `--sound-profile "MuseScore Basic"` gives the
identical MD5 `bff1bc21…`. So any hash difference below reflects a real difference in
synthesis, not encoder jitter.

---

## 1. Muse Sounds works for headless command-line rendering

**This contradicts the repository's top-level `README.md`**, which states that *"Muse
Sounds is not installed for command-line rendering."* That was true before Muse Sounds
Manager was installed on 21 November 2026. It is no longer true.

Rendering the same score with `QT_QPA_PLATFORM=offscreen`, changing only the profile:

| Profile | MD5 | Mean level |
|---|---|---|
| `MuseSounds` | `6937d2f585941cf1deb92e82d0313c5f` | −24.2 dB |
| `MuseScore Basic` | `bff1bc2163ed856d29be11165dacb75f` | −26.5 dB |

Different audio, from the same score, headless. Confirmed independently by MuseScore's
own startup log (`evidence/musesampler-init-log.txt`), which reports the sampler library
loading and then initialising **four times** — once per SATB staff:

```
MuseSamplerResolver::init | MuseSampler successfully inited:
  /home/daniel/.local/share/MuseSampler/lib/libMuseSamplerCoreLib.so, version: 0.106.0
MuseSamplerWrapper::initSampler | Successfully initialized sampler ...   (x4)
```

**Why this matters here.** `tools/publish-score` already accepts
`--sound-profile MuseSounds` and already renders with `QT_QPA_PLATFORM=offscreen`, so
existing pieces can be re-rendered through Muse Sounds with no tooling change:

```bash
publish-score --sound-profile MuseSounds --force path/to/score.mscz
```

Two things to fix if you want the docs to match reality — they must change together,
because the second one regenerates the first:

- `README.md` (top level), the "Audio is rendered with MuseScore's built-in *MS Basic*
  soundfont…" sentence
- `tools/build-index.py:73`, which generates that sentence

Neither was changed as part of this experiment, since both are outside the experiment
directory.

**Caveat.** Muse Sounds is a ~17 GB local install that cannot be committed, and it needs
a Muse account to obtain. Anyone cloning this repository will render MS Basic unless they
install it themselves — see the parent README's reproduction steps. So MS Basic remains
the sensible default for `publish-score`; Muse Sounds should stay opt-in.

---

## 2. Muse Sounds fails silently — the exit code lies

The most operationally dangerous finding. If MuseSampler is unavailable, MuseScore does
**not** error. It renders the score in MS Basic, writes a perfectly valid MP3, and exits
`0`.

Demonstrated by renaming the sampler library and re-rendering with the profile unchanged:

| Condition | MD5 | Exit code |
|---|---|---|
| `MuseSounds`, sampler present | `6937d2f5…` | 0 |
| `MuseSounds`, **sampler hidden** | `bff1bc21…` | 0 |
| `MuseScore Basic` | `bff1bc21…` | 0 |

With the sampler hidden, the "Muse Sounds" render is *byte-identical* to the MS Basic
render. This is also the cleanest proof that MuseSampler — not some different Fluid
preset — is doing the synthesis in finding 1.

**Consequence for this repository:** a `publish-score --sound-profile MuseSounds` run on
a machine without Muse Sounds will quietly publish MS Basic audio, labelled as Muse
Sounds, with a green exit. Nothing in the current tooling would catch it.

If Muse Sounds renders are ever adopted for published pieces, verify the output rather
than trusting the exit status. The cheapest check is a known-good hash comparison, or:

```bash
# non-empty output means the sampler loaded
musescore -d <score> 2>&1 | grep 'MuseSampler successfully inited'
```

---

## 3. Muse Choir does not sing notated lyrics

Tested directly rather than assumed. All **52** `<Lyrics>` blocks were stripped from the
committed `.mscz` and the result rendered under Muse Choir:

| Version | MD5 |
|---|---|
| With the German text (one stanza, Soprano staff) | `6937d2f585941cf1deb92e82d0313c5f` |
| With every lyric removed | `6937d2f585941cf1deb92e82d0313c5f` |

Byte-identical. The text has **no** effect on the audio whatsoever.

What you actually hear is a sustained-vowel choir; Muse Choir is built on vowel samples
(advertised as *Ahh*, *Ooh*, *Mmm*). Lyrics exist in the notation and the PDF only.

Lyric text triggering different phoneme samples in choral libraries has been reported, and
forum reports describe it working erratically or not at all. No official documentation
link was found for it, so it is unverified. **It was not observed here.** It may need different markup, a different
library, or a setting this experiment did not find — but on 4.7.7 with Muse Choir and
MuseSampler 0.106.0, removing the lyrics changed nothing.

**Consequence:** do not describe Muse Choir output as "sung lyrics" in any README or
video description. "Vowel-based choral playback" is accurate.

---

## Smaller observations

- **CLI-written scores do not pin their sounds.** A `.mscz` written by the command line
  has `"activeSoundProfile": "MuseSounds"` but an empty `"tracks": []`; sounds are
  resolved at load time from the profile plus each staff's instrument ID. Opening the
  score in the GUI and saving writes `tracks[]` out in full with explicit Muse Choir
  resource metadata. Both play back correctly — but only the GUI-saved file records
  *which* preset each staff uses. The score committed here is the GUI-saved one.

- **The Linux installer is not called Muse Hub.** It is **Muse Sounds Manager**, and the
  `.tar.gz` build needs no root — useful on machines without passwordless `sudo`. The
  `.deb` and `.rpm` both require root. All three are linked from the MuseScore download
  page; the direct URL is `https://muse-cdn.com/Muse_Sounds_Manager_x64.tar.gz`.

- **Screenshots need a workaround on GNOME Wayland.** The GNOME Shell screenshot D-Bus
  method returns `AccessDenied`, and `import -window root` fails. MuseScore runs under
  XWayland, so `import -window <id>` against its window works. Window IDs come from
  `xwininfo -root -children`.

- **MuseScore's `--score-meta` is a cheap verification tool.** It reports measures, key,
  time signature, tempo, duration and part list as JSON without opening the GUI — handy
  for checking an import landed correctly.

---

## Files backing these claims

| Path | What it shows |
|---|---|
| `verify-findings.sh` | Re-runnable check of all four findings |
| `evidence/verification-run.txt` | Output of the run quoted above |
| `evidence/musesampler-init-log.txt` | MuseScore logging the sampler loading 4× |
| `exports/…-musesounds.mp3` vs `…-msbasic.mp3` | The two renders being compared |
| `exports/per-voice/*.mp3` | Each voice alone, through Muse Choir |
| `screenshots/02…`, `03…` | Mixer presets, before and after a reopen |

See `README.md` for the full experiment write-up, source and rights information.
