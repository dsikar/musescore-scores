"""Verify actual MuseScore exports against the hand-entered source ledger.

This catches import/save/export changes. It does NOT read pitches from the PDF
or replace the manual source proofread documented in the three NOTES.md files.
Outputs evidence/additional-score-check.json. Requires MuseScore and pdfinfo.
"""
from pathlib import Path
from fractions import Fraction
import csv
import hashlib
import json
import os
import subprocess
import tempfile
import xml.etree.ElementTree as ET
import zipfile

HERE = Path(__file__).resolve().parents[1]
SLUGS = ('once-in-royal-davids-city', 'while-shepherds-watched', 'we-three-kings')
NAMES = ('Soprano', 'Alto', 'Tenor', 'Bass')
ENV = dict(os.environ, QT_QPA_PLATFORM='offscreen')


def command(*args):
    return subprocess.run(args, env=ENV, capture_output=True, text=True, check=True, timeout=180)


def score_notes(path):
    root = ET.parse(path).getroot()
    result = []
    for part in root.findall('part'):
        div = 1
        bars = []
        for measure in part.findall('measure'):
            if measure.find('attributes/divisions') is not None:
                div = int(measure.findtext('attributes/divisions'))
            notes = []
            for note in measure.findall('note'):
                assert note.find('chord') is None, 'Unexpected extra chord note'
                p = note.find('pitch')
                assert p is not None, 'Unexpected inserted rest'
                pitch = p.findtext('step') + {0: '', 1: '#', -1: 'b'}[int(p.findtext('alter', '0'))] + p.findtext('octave')
                notes.append((pitch, Fraction(int(note.findtext('duration')), div)))
            bars.append(notes)
        result.append(bars)
    return root, result


def run():
    results = {'musescore_version': command('musescore', '--long-version').stdout.strip(), 'carols': {}}
    with tempfile.TemporaryDirectory(prefix='verify-added-carols-') as temp:
        for slug in SLUGS:
            folder = HERE / slug
            score = folder / (slug + '.mscz')
            exported = Path(temp) / (slug + '.musicxml')
            command('musescore', '-o', str(exported), str(score))
            command('musescore', '-o', str(folder / (slug + '.pdf')), str(score))
            root, actual = score_notes(exported)
            expected = [[] for _ in NAMES]
            for row in csv.DictReader((folder / 'source-ledger.tsv').open(), delimiter='\t'):
                v = NAMES.index(row['voice']); bar = int(row['bar'])
                while len(expected[v]) < bar: expected[v].append([])
                expected[v][bar-1].append((row['pitch'], Fraction(row['duration_quarters'])))
            assert actual == expected, (slug, 'native MusicXML differs from source ledger')
            source_root, source_notes = score_notes(folder / (slug + '.musicxml'))
            assert source_notes == expected
            # Include notation properties that a simple MIDI/pitch check misses.
            for tag in ('tie', 'slur', 'syllabic', 'text'):
                if tag in ('syllabic', 'text'):
                    a = [x.text for x in root.findall('.//lyric/' + tag)]
                    b = [x.text for x in source_root.findall('.//lyric/' + tag)]
                    assert a == b, (slug, tag)
                else:
                    a = sorted(x.get('type') for x in root.iter(tag))
                    b = sorted(x.get('type') for x in source_root.iter(tag))
                    assert a == b, (slug, tag, a, b)
            repeats = root.findall('.//repeat')
            # MusicXML repeats the score-wide barline on each of the four parts.
            assert len(repeats) == (4 if slug == SLUGS[0] else 0)
            if slug == SLUGS[1]:
                # The source explicitly cancels C-sharp in the following short bar.
                assert root.findall('part')[1].findall('measure')[9].findtext('note/accidental') == 'natural'
            m = command('musescore', '--score-meta', str(score)).stdout
            meta = json.loads(m[m.index('{'):]); meta = meta.get('metadata', meta)
            assert [p['name'] for p in meta['parts']] == list(NAMES)
            assert 0 < meta['duration'] <= 300
            with zipfile.ZipFile(score) as z:
                audio = json.loads(z.read('audiosettings.json'))
                assert audio['activeSoundProfile'] == 'MuseSounds'
                presets = {t['instrumentId']: t['in']['resourceMeta'].get('attributes', {}) for t in audio['tracks'] if t['instrumentId'] != 'metronome'}
                assert set(presets) == {'soprano', 'alto', 'tenor', 'bass'}
                for name in NAMES:
                    attrs = presets[name.lower()]
                    assert attrs['musePack'] == 'Muse Choir' and attrs['museName'] == name + ('es' if name == 'Bass' else 's')
                native = ET.fromstring(z.read(next(n for n in z.namelist() if n.endswith('.mscx'))))
                assert 'Additional stanzas' in ''.join(native.itertext())
            pdfinfo = command('pdfinfo', str(folder / (slug + '.pdf'))).stdout
            pages = int(next(x.split(':')[1] for x in pdfinfo.splitlines() if x.startswith('Pages:')))
            assert 1 <= pages <= 4
            if slug != SLUGS[2]:
                full = folder / 'source/hymns-ancient-and-modern-1909.pdf'
                assert hashlib.sha256(full.read_bytes()).hexdigest() == '063a9e527b0d24cbfe319bb60dcf22cec7ab3365f984730f93dde9f9ddaead49'
            results['carols'][slug] = {
                'pass': True, 'parts': list(NAMES), 'bars_per_part': [len(p) for p in actual],
                'notated_notes_per_part': [sum(len(b) for b in p) for p in actual],
                'duration_seconds_score_meta': meta['duration'], 'tempo_quarter_bpm': meta['tempo'],
                'pdf_pages': pages, 'presets': presets, 'source_ledger_roundtrip': 'PASS',
                'ties_slurs_lyrics_repeat': 'PASS',
                'independent_midi_crosscheck': 'SKIPPED: PDF transcription; no same-edition independent MIDI used',
                'source_pdf_note_reading': 'manual; see NOTES.md; not performed by this script',
            }
            print(slug, 'PASS', flush=True)
    (HERE / 'evidence/additional-score-check.json').write_text(json.dumps(results, indent=2) + '\n')


if __name__ == '__main__': run()
