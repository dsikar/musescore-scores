# Task prompt: add three more carols to the SATB set

Extend the existing set in this directory (`experiments/christmas-carols-satb/`) from 12 to
**15 carols**. All requirements in [`PROMPT.md`](PROMPT.md) still apply unless this brief
changes them. Read `PROMPT.md`, `README.md` and two or three carols' `NOTES.md` first, and
match the existing layout, naming, style (`tools/carols.mss`) and documentation.

Before any dependent work, verify that you can inspect and control the MuseScore desktop
application, access this workspace, and capture screenshots. Report any missing
capability.

## The carols

| Slug | Carol | Notes |
|---|---|---|
| `once-in-royal-davids-city` | *Once in Royal David's City* | Tune *Irby*, H. J. Gauntlett (1849); words C. F. Alexander (1848) |
| `while-shepherds-watched` | *While Shepherds Watched Their Flocks* | Tune *Winchester Old* (Este's *Psalter*, 1592) is the usual English choice; words Nahum Tate (1700). State which tune you use |
| `we-three-kings` | *We Three Kings of Orient Are* | Words, tune and harmony by J. H. Hopkins Jr. (1857) |

The first two were rejected in the first run only because they are not in the Open
Hymnal (see the README's "Considered and rejected" section). If *We Three Kings* cannot
be sourced, use *Away in a Manger* (tune *Cradle Song*, W. J. Kirkpatrick, 1895) from a
source with four distinguishable voices, and document the substitution. Deliver 3. If you
deliver only 2, explain exactly what blocked the third.

## Sources: this is the hard part

Open Hymnal does not have the first two, and the first run found these limits on
automated access:

- CPDL returns HTTP 403.
- musescore.com needs a login to download.
- IMSLP has download timers.
- Mutopia has few carols.

Find another route without bypassing any of them. Options to try:

- **Open Hymnal** first, in case *We Three Kings* is there. Reuse the existing ABC
  pipeline (`build.sh`, `tools/`) if it is.
- **Internet Archive** (archive.org) scans of public-domain hymnals, for example *Hymns
  Ancient and Modern* (1861/1875 editions) for *Irby* and *Winchester Old*. These are
  usually freely downloadable PDFs.
- **Wikimedia Commons**, **Hymnary.org** (only where a page image or PDF can be fetched
  without logging in), and any of the sources above if a manual route exists.
- **Ask the repository owner.** If the only good source needs a login or a manual
  browser download, stop and ask the owner to download it. Do not work around the
  restriction.

Rights warnings specific to these carols:

- **Do not use David Willcocks's descant or arrangement** of *Once in Royal David's City*
  (from the 1960s, still in copyright). Use Gauntlett's harmony or another setting
  published before 1929 whose harmoniser died more than 70 years ago (A. H. Mann,
  d. 1929, qualifies).
- **Avoid *The English Hymnal* (1906) harmonies credited to Vaughan Williams** (d. 1958;
  in copyright under life + 70 until 2029). The same applies to any other harmoniser who
  died after 1955.
- As before, keep the rights in the composition, text, setting and scan or edition
  separate, and keep the starter file in `source/` when its terms allow.

## Entering the notes

Sources other than Open Hymnal will probably be **page scans with no machine-readable
data**. In that case:

- Enter the notes in MuseScore by hand or from a MusicXML you type up. If you use OMR,
  correct its output.
- **Proofread every bar of every voice against the scan**, and record in `NOTES.md` that
  you did. There is no independent MIDI to cross-check against this time. Say so plainly
  instead of implying that the automated check in `verify-carols.sh` covered these
  carols.
- A hymnal short score (two staves) must be split into four labelled staves, as for the
  existing carols. Where the voice-leading is ambiguous (chords without clear voice
  separation), say how you resolved it.
- Lyrics go on the Soprano staff, as in the rest of the set. State exactly which stanzas
  are underlaid, which are printed as text, and which are omitted. Use the stanza
  wording in the chosen source.

## Sounds, export and checks

- Assign Muse Choir Sopranos, Altos, Tenors and Basses, and save from the GUI so the
  assignments are recorded in `audiosettings.json`.
- Export each score to a PDF.
- Extend `verify-carols.sh` (or `tools/carols.tsv`) so the new carols get checks 1–5. If
  the MIDI cross-check (check 6) cannot apply, report it as skipped, with the reason,
  rather than passed.
- **Screenshots and the restart check were skipped in the first run.** Do them this time
  for at least one new carol:
  - a screenshot of the score
  - a mixer screenshot after a full MuseScore restart, showing the four presets

  If GNOME again opens MuseScore minimised, ask the owner to restore the window by hand
  rather than skipping the check.

## Documentation

- Add the three carols to the index table in `README.md`, keeping its columns. Update
  the count ("Twelve" → "Fifteen") everywhere it appears.
- Update the "Considered and rejected" section: remove the two carols now included, and
  record any new rejections.
- Give each new carol a full `NOTES.md` covering the same sections as the existing ones,
  including the source URL, the scan's page number or hymn number, and the retrieval date.

## Delivery

Work on a new branch and open a pull request against `main`. Do not merge it. Change
only files in `experiments/christmas-carols-satb/`, and do not modify the 12 existing
carols' scores or PDFs.

Finish with a concise report giving:

- each new carol's slug, source, setting or harmoniser, and duration
- the starter files kept versus only linked
- the screenshot and restart checks performed
- any unmet requirements
