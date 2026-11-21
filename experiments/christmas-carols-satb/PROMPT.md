# Task prompt: SATB choir scores for well-known Christmas carols

Produce a set of **between 6 and 12 well-known Christmas carols**, each as a four-part SATB
choir score in MuseScore with a PDF export, using the same approach as the completed
single-piece experiment in
[`../musescore-choir-experiment/`](../musescore-choir-experiment/). Read that
experiment's `README.md`, `FINDINGS.md` and `verify-findings.sh` first and reuse its
methods. Don't repeat investigations it has already settled unless your MuseScore or Muse
Sounds versions differ from the ones it records.

Work in this repository (`dsikar/musescore-scores`). Read any applicable `AGENTS.md`
first. Inspect the installed MuseScore version and sound libraries before starting.
Proceed autonomously with routine choices.

Before any dependent work, verify that you can inspect and control the MuseScore desktop
application, access this workspace, and capture screenshots. Report any missing
capability.

## 1. Choose the carols

- Choose 6 to 12 carols that are widely known in the English-speaking world, for example
  *O Come, All Ye Faithful*, *Hark! The Herald Angels Sing*, *Silent Night*,
  *Joy to the World*, *God Rest You Merry, Gentlemen*, *The First Nowell*,
  *O Little Town of Bethlehem*, *Once in Royal David's City*, *While Shepherds Watched*,
  *Good King Wenceslas*, *In the Bleak Midwinter*, *Angels from the Realms of Glory*.
  This list is only a guide.
- Each carol must be a public-domain composition with words and music that are clearly out
  of copyright. Avoid modern arrangements unless their licence explicitly permits
  redistribution in a public repository.
- Each score must have four voice parts (Soprano, Alto, Tenor, Bass) and must play
  in **no more than five minutes** at its saved tempo. You may omit verses to fit the limit;
  document which ones you omitted.
- Aim for 12. If you deliver fewer, explain why (for example, no suitable source could be
  found). Fewer than 6 is a failure of the task, not a partial success.

## 2. Source ("starter") files: keep and reference them

Every carol must start from a **MuseScore file or a score PDF** obtained from a reputable,
openly accessible source. Suitable sources include MuseScore's score-sharing hub
(musescore.com), CPDL, IMSLP, or the Mutopia Project.

- **Keep the starter file** in the repository, unmodified, in that carol's `source/`
  folder, as long as its licence permits redistribution. If it doesn't, keep the exact URL
  and explain why you didn't keep the file.
- For each carol, record:
  - the exact source URL
  - the retrieval date
  - composer, arranger or harmoniser, and the text author
  - edition or uploader
  - licence
- Keep the rights in the composition and text separate from the rights in the particular
  edition, arrangement or upload.
- Do not bypass logins, paywalls, download limits or bot protection, and do not make
  purchases. If a source is blocked, choose another source and document the change. Note
  that the earlier experiment found that CPDL returns HTTP 403 to automated requests.

## 3. Create each SATB score

- Use exactly four clearly labelled vocal staves: **Soprano, Alto, Tenor, Bass**. Each
  voice gets its own staff even if the source uses two staves (SA/TB) or a hymn-style
  layout. Document any such restructuring.
- Preserve the source's notes, rhythms, rests, key and time signatures, repeats, fermatas
  and essential markings. Set a sensible tempo if the source has none and document it.
- If you transcribe from a PDF, check every bar's notes and rhythms against it. Do not
  trust OMR or automatic conversion without checking.
- Include lyrics where practical. For each carol, state precisely:
  - which stanzas are included
  - which staves carry lyrics
  - any stanzas you omitted

  Do not describe a single stanza laid out over a repeat as "two verses".
- Assign **Muse Sounds → Muse Choir** presets: Sopranos, Altos, Tenors and Basses to the
  matching staves. Save each score from the GUI so the assignments are recorded in
  `audiosettings.json`, as the earlier experiment found. Verify by reading
  `audiosettings.json` inside each `.mscz`.
- Export a **PDF** of each final score. An MP3 render is welcome but optional. If you
  render one, use `--sound-profile MuseSounds` and confirm it differs from an MS Basic
  render, because Muse Sounds fails silently.

## 4. Layout and naming

Keep everything inside `experiments/christmas-carols-satb/`. Do **not** put anything under
`pieces/`, because `tools/publish-score` treats that folder as published material.
Suggested layout:

```
experiments/christmas-carols-satb/
├── PROMPT.md                      this brief
├── README.md                      index and shared notes
├── verify-carols.sh               optional re-runnable checks
└── <carol-slug>/
    ├── <carol-slug>.mscz          SATB score, Muse Choir assigned
    ├── <carol-slug>.pdf           PDF export
    ├── source/                    unmodified starter file(s) and licence text
    └── NOTES.md                   per-carol notes (see below)
```

Use lower-case, hyphenated, descriptive slugs, for example `o-come-all-ye-faithful`.

## 5. Documentation

**`README.md` (index)** must include:

- One table row per carol with these columns:
  - title
  - composer and harmoniser
  - text author
  - source link
  - licence
  - stanzas included
  - tempo
  - verified duration
  - links to the `.mscz`, `.pdf` and starter file
- Environment: the MuseScore version, MuseSampler version, Muse Choir and OS.
- Install steps and dependencies needed to reproduce playback on another machine. You may
  link to the earlier experiment's instructions rather than duplicating them.
- How you verified durations, sound assignments and notes.
- Known limitations, carols you considered and rejected (with reasons), and anything you
  could not verify.

**Each carol's `NOTES.md`** must include:

- source and rights details
- how the score was obtained or entered
- any restructuring, for example from two staves to four
- musical changes and omissions
- lyric coverage
- tempo and duration
- what was checked against the source

**For capability claims**, cite official MuseScore or Muse Sounds documentation where it
exists, and clearly separate documented behaviour from behaviour you observed. Do not claim
the choir sings the lyrics. The earlier experiment showed that Muse Choir ignores them.

## 6. Verification required before finishing

For every carol:

1. Open the `.mscz` in MuseScore and confirm it has four labelled staves.
2. Read `audiosettings.json` and confirm the four Muse Choir presets.
3. Confirm the playback duration is five minutes or less, from `--score-meta` or a render.
4. Confirm the PDF exists and its page count is sensible.
5. Confirm the starter file is present, or explain why it isn't.

For at least two carols, also:

- reopen the score after a full MuseScore restart and capture a mixer screenshot showing
  the presets persisted
- capture a screenshot of the score

Report only checks you actually performed.

## 7. Delivery

Work on a new branch and open a pull request against `main` for review. Do not merge it,
do not publish anything to `pieces/`, and do not modify files outside
`experiments/christmas-carols-satb/`. Do not touch the separate `xmas-repertoire`
repository, which holds trumpet parts.

Finish with a concise report giving:

- the number of carols delivered, and their slugs
- each carol's duration
- confirmation of the sound assignments
- the starter files kept versus only linked
- any unmet requirements or unverifiable claims
