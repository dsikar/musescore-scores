"""Hand-entered source ledger and MusicXML builder for the three added carols.

Pitch names are sounding pitches; durations are quarter-note units. Each '|'
is a barline in the starter PDF, including its short phrase-boundary bars.
This is a transcription, not an automatic PDF conversion. See each NOTES.md.
Run from any directory: python3 tools/additional_carols.py
Outputs MusicXML and a readable source ledger beside each new score.
"""
from pathlib import Path
from fractions import Fraction
import argparse
import re
import zipfile
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parents[1]
VOICES = ('Soprano', 'Alto', 'Tenor', 'Bass')
DATA = {
    'once-in-royal-davids-city': {
        'title': "Once in Royal David's City", 'key': 1, 'time': (4, 4), 'tempo': 88,
        'composer': 'H. J. Gauntlett (1805–1876)\nIrby; Historical Edition, 1909',
        'lyricist': 'Cecil Frances Alexander (1818–1895)',
        'lengths': [2, 4, 2, 2, 4, 2, 2, 4, 2, 2, 4, 2], 'repeat': 5,
        'parts': [
            'D4:1 F#4:1 | G4:1.5 G4:.5 G4:.5 F#4:.5 G4:.5 A4:.5 | A4:1 G4:1 | G4:1 B4:1 | D5:1.5 B4:.5 B4:.5 A4:.5 G4:.5 F#4:.5 | G4:2 | E5:1 E5:1 | D5:1.5 A4:.5 C5:1 C5:1 | B4:2 | E5:1 E5:1 | D5:1.5 B4:.5 B4:.5 A4:.5 G4:.5 F#4:.5 | G4:2',
            'D4:1 C4:1 | D4:1.5 D4:.5 D4:1 D4:.5 F#4:.5 | F#4:1 G4:1 | D4:1 E4:.5 G4:.5 | D4:1.5 G4:.5 E4:1 D4:1 | D4:2 | G4:1 G4:1 | G4:.5 F#4:.5 G4:.5 G4:.5 G4:1 F#4:.5 E4:.5 | D#4:2 | E4:.5 F#4:.5 G4:.5 A4:.5 | D4:.5 F#4:.5 G4:.5 D4:.5 E4:1 D4:1 | D4:2',
            'B3:1 A3:1 | G3:1.5 B3:.5 B3:.5 A3:.5 B3:.5 C4:.5 | C4:1 B3:1 | B3:1 G3:1 | G3:1.5 D4:.5 D4:.5 C4:.5 B3:.5 A3:.5 | B3:2 | C4:1 C4:1 | B3:.5 C4:.5 D4:.5 B3:.5 C4:1 A3:.5 G3:.5 | F#3:2 | C4:1 C4:1 | C4:.5 A3:.5 B3:.5 D4:.5 D4:.5 C4:.5 B3:.5 A3:.5 | B3:2',
            'G2:1 A2:1 | B2:1.5 G2:.5 D3:1 D3:1 | D3:1 G3:1 | G3:1 E3:1 | B2:1.5 G2:.5 C3:1 D3:1 | G2:2 | C3:1 E3:1 | G3:.5 A3:.5 B3:.5 G3:.5 A3:1 A2:1 | B2:2 | C3:.5 D3:.5 E3:.5 F#3:.5 | G3:1.5 G3:.5 C3:1 D3:1 | G2:2',
        ],
        # Two underlay lines in the repeated opening belong to ONE stanza.
        'lyrics': [
            ['Once in', 'roy- al Da- _ vid’s _', 'ci- ty', 'Stood a', 'low- ly cat- _ tle _', 'shed;', 'Ma- ry', 'was that Mo- ther', 'mild,', 'Je- sus', 'Christ her lit- _ tle _', 'Child.'],
            ['Where a', 'Mo- ther laid _ her _', 'Ba- by', 'In a', 'man- ger for _ His _', 'bed;', '', '', '', '', '', ''],
        ],
        'slurs': [(0, 1, 2, 3), (0, 1, 4, 5), (0, 4, 2, 3), (0, 4, 4, 5), (0, 10, 2, 3), (0, 10, 4, 5)],
        'ties': [],
        'stanzas': [
            '2. He came down to earth from heaven,\nWho is God and Lord of all,\nAnd His shelter was a stable,\nAnd His cradle was a stall;\nWith the poor, and mean, and lowly,\nLived on earth our Saviour Holy.',
            '3. And through all His wondrous Childhood\nHe would honour and obey,\nLove, and watch the lowly Maiden,\nIn whose gentle arms He lay;\nChristian children all must be\nMild, obedient, good as He.',
            '4. For He is our childhood’s pattern,\nDay by day like us He grew,\nHe was little, weak, and helpless,\nTears and smiles like us He knew;\nAnd He feeleth for our sadness,\nAnd He shareth in our gladness.',
            '5. And our eyes at last shall see Him,\nThrough His own redeeming love,\nFor that Child so dear and gentle\nIs our Lord in heav’n above;\nAnd He leads His children on\nTo the place where He is gone.',
            '6. Not in that poor lowly stable,\nWith the oxen standing by,\nWe shall see Him; but in heaven,\nSet at God’s right hand on high;\nWhen like stars His children crown’d\nAll in white shall wait around. Amen.',
        ],
    },
    'while-shepherds-watched': {
        'title': 'While Shepherds Watched Their Flocks', 'key': -1, 'time': (4, 2), 'tempo': 160,
        'composer': 'Winchester Old (1592)\nHymns Ancient and Modern, 1909',
        'lyricist': 'Nahum Tate (1652–1715)',
        'lengths': [2, 8, 6, 2, 8, 6, 2, 8, 6, 2, 8, 6],
        'parts': [
            'F4:2 | A4:3 A4:1 G4:2 F4:2 | Bb4:2 Bb4:2 A4:2 | G4:2 | A4:2 C5:2 C5:2 B4:2 | C5:6 | A4:2 | D5:3 C5:1 Bb4:2 A4:2 | G4:2 F4:2 E4:2 | A4:2 | G4:2 F4:2 F4:2 E4:2 | F4:6',
            'C4:2 | F4:3 F4:1 E4:2 D4:2 | D4:2 F4:2 F4:2 | E4:2 | F4:2 G4:2 G4:2 G4:2 | E4:6 | F4:2 | F4:3 F4:1 F4:2 F4:2 | E4:2 D4:2 C#4:2 | C4:2 | E4:2 D4:2 D4:2 C4:2 | C4:6',
            'A3:2 | C4:3 C4:1 C4:2 A3:2 | Bb3:2 D4:2 C4:2 | C4:2 | C4:2 C4:2 D4:2 D4:2 | C4:6 | C4:2 | Bb3:3 A3:1 Bb3:2 C4:2 | C4:2 A3:2 A3:2 | A3:2 | C4:2 A3:2 Bb3:2 G3:2 | A3:6',
            'F3:2 | F3:3 F3:1 C3:2 D3:2 | Bb2:2 Bb2:2 F3:2 | C3:2 | F3:2 E3:2 G3:2 G3:2 | C3:6 | F3:2 | Bb3:3 F3:1 D3:2 F3:2 | C3:2 D3:2 A2:2 | F3:2 | C3:2 D3:2 Bb2:2 C3:2 | F3:6',
        ],
        'lyrics': [['While', 'shep- herds watch’d their', 'flocks by night,', 'All', 'seat- ed on the', 'ground,', 'The', 'An- gel of the', 'Lord came down,', 'And', 'glo- ry shone a-', 'round.']],
        'slurs': [], 'ties': [], 'accidentals': {(1, 9, 0): 'natural'},
        'stanzas': [
            '2. “Fear not,” said he; for mighty dread\nHad seized their troubled mind;\n“Glad tidings of great joy I bring\nTo you and all mankind.”',
            '3. “To you in David’s town this day\nIs born of David’s line\nThe Saviour, Who is Christ the Lord;\nAnd this shall be the sign:”',
            '4. “The heav’nly Babe you there shall find\nTo human view display’d,\nAll meanly wrapp’d in swathing bands,\nAnd in a manger laid.”',
            '5. Thus spake the seraph; and forthwith\nAppear’d a shining throng\nOf Angels praising God, who thus\nAddress’d their joyful song:',
            '6. “All glory be to God on high,\nAnd on the earth be peace;\nGood-will henceforth from heav’n to men\nBegin and never cease.” Amen.',
        ],
    },
    'we-three-kings': {
        'title': 'We Three Kings of Orient Are', 'key': 1, 'time': (6, 8), 'tempo': 90,
        'composer': 'John Henry Hopkins Jr. (1820–1891)',
        'lyricist': 'John Henry Hopkins Jr.', 'lengths': [3] * 17,
        'parts': [
            'B4:1 A4:.5 G4:1 E4:.5 | F#4:.5 G4:.5 F#4:.5 E4:1.5 | B4:1 A4:.5 G4:1 E4:.5 | F#4:.5 G4:.5 F#4:.5 E4:1.5 | G4:1 G4:.5 A4:1 A4:.5 | B4:1 B4:.5 D5:.5 C5:.5 B4:.5 | A4:.5 B4:.5 A4:.5 G4:1 F#4:.5 | E4:3 | F#4:1.5 A4:1.5 | G4:1 G4:.5 G4:1 E4:.5 | G4:1 E4:.5 G4:1.5 | G4:1 G4:.5 G4:1 E4:.5 | G4:1 E4:.5 G4:1.5 | G4:1 G4:.5 A4:1 B4:.5 | C5:1 B4:.5 A4:1 B4:.5 | G4:1 G4:.5 G4:1 E4:.5 | G4:1 E4:.5 G4:1.5',
            'G4:1 F#4:.5 E4:1 E4:.5 | D#4:.5 D#4:.5 D#4:.5 E4:1.5 | G4:1 F#4:.5 E4:1 E4:.5 | D#4:.5 D#4:.5 D#4:.5 E4:1.5 | E4:1 E4:.5 F#4:1 F#4:.5 | G4:1 G4:.5 G4:.5 F#4:.5 G4:.5 | E4:.5 E4:.5 E4:.5 E4:1 D#4:.5 | E4:3 | D4:1.5 D4:1.5 | D4:1 D4:.5 D4:1 B3:.5 | E4:1 C4:.5 D4:1.5 | D4:1 D4:.5 D4:1 B3:.5 | E4:1 C4:.5 D4:1.5 | E4:1 E4:.5 F#4:1 G4:.5 | G4:1 G4:.5 F#4:1 G4:.5 | D4:1 D4:.5 D4:1 B3:.5 | E4:1 C4:.5 D4:1.5',
            'B3:1 B3:.5 B3:1 G3:.5 | A3:.5 B3:.5 A3:.5 G3:1.5 | B3:1 B3:.5 B3:1 G3:.5 | A3:.5 B3:.5 A3:.5 G3:1.5 | B3:1 B3:.5 D4:1 D4:.5 | D4:1 D4:.5 B3:.5 C4:.5 D4:.5 | C4:.5 C4:.5 C4:.5 B3:1 A3:.5 | G3:3 | A3:1.5 C4:1.5 | B3:1 B3:.5 B3:1 G3:.5 | G3:1 G3:.5 B3:1.5 | B3:1 B3:.5 B3:1 G3:.5 | G3:1 G3:.5 B3:1.5 | B3:1 B3:.5 D4:1 D4:.5 | E4:1 D4:.5 D4:1 D4:.5 | B3:1 B3:.5 B3:1 G3:.5 | G3:1 G3:.5 B3:1.5',
            'E3:1 E3:.5 E3:1 E3:.5 | B2:.5 B2:.5 B2:.5 E3:1.5 | E3:1 E3:.5 E3:1 E3:.5 | B2:.5 B2:.5 B2:.5 E3:1.5 | E3:1 E3:.5 D3:1 D3:.5 | G3:1 G3:.5 G3:.5 A3:.5 G3:.5 | A3:.5 A3:.5 A3:.5 B3:1 B2:.5 | E3:3 | D3:1.5 D3:1.5 | G3:1 G3:.5 G3:1 G3:.5 | C3:1 C3:.5 G2:1.5 | G3:1 G3:.5 G3:1 G3:.5 | C3:1 C3:.5 G2:1.5 | E3:1 E3:.5 D3:1 G3:.5 | C3:1 G3:.5 D3:1 G3:.5 | G3:1 G3:.5 G3:1 G3:.5 | C3:1 C3:.5 G2:1.5',
        ],
        'lyrics': [['We three kings of', 'O- ri- ent are;', 'Bear- ing gifts we', 'trav- erse a- far,', 'Field and foun- tain,', 'moor and moun- _ tain,', 'Fol- low- ing yon- der', 'star.', 'O _', 'star of won- der,', 'star of night,', 'star with roy- al', 'beau- ty bright,', 'West- ward lead- ing,', 'still pro- ceed- ing,', 'Guide us to thy', 'per- fect light.']],
        'slurs': [(2,3,0,1), (0,5,2,3), (1,5,2,3), (2,5,2,3), (3,5,2,3), (0,6,0,1), (0,8,0,1), (2,8,0,1)],
        'ties': [(1,3,0,1), (1,6,0,1), (2,6,0,1), (1,8,0,1), (3,8,0,1)],
        'stanzas': [
            '2. Born a King on Bethlehem’s plain,\nGold I bring to crown Him again,\nKing for ever, ceasing never,\nOver us all to reign. [Refrain]',
            '3. Frankincense to offer have I;\nIncense owns a Deity nigh;\nPrayer and praising, all men raising,\nWorship Him, God on high. [Refrain]',
            '4. Myrrh is mine; its bitter perfume\nBreathes a life of gathering gloom;\nSorr’wing, sighing, bleeding, dying,\nSealed in a stone-cold tomb. [Refrain]',
            '5. Glorious now behold Him arise;\nKing and God and Sacrifice:\nAlleluia, Alleluia!\nEarth to heav’n replies. [Refrain]',
        ],
    },
}


def parse_part(text):
    return [[(p, Fraction(q)) for p, q in (t.split(':') for t in bar.split())]
            for bar in text.split('|')]


def sub(parent, tag, text=None, **attrs):
    element = ET.SubElement(parent, tag, attrs)
    if text is not None:
        element.text = str(text)
    return element


def build(slug, d):
    parts = [parse_part(p) for p in d['parts']]
    for name, bars in zip(VOICES, parts):
        assert len(bars) == len(d['lengths']), (slug, name)
        for i, (bar, length) in enumerate(zip(bars, d['lengths'])):
            assert sum(q for _, q in bar) == length, (slug, name, i, bar)
    root = ET.Element('score-partwise', version='4.0')
    sub(sub(root, 'work'), 'work-title', d['title'])
    ident = sub(root, 'identification')
    sub(ident, 'creator', d['composer'], type='composer')
    sub(ident, 'creator', d['lyricist'], type='lyricist')
    sub(ident, 'rights', 'Public-domain source; SATB transcription. Source and editorial details: NOTES.md')
    pl = sub(root, 'part-list')
    for i, name in enumerate(VOICES):
        sp = sub(pl, 'score-part', id=f'P{i+1}')
        sub(sp, 'part-name', name)
        sub(sp, 'part-abbreviation', ('S.', 'A.', 'T.', 'B.')[i])
        si = sub(sp, 'score-instrument', id=f'I{i+1}')
        sub(si, 'instrument-name', name)
        sub(si, 'instrument-sound', 'voice.' + name.lower())
    ledger = ['voice\tbar\tevent\tpitch\tduration_quarters']
    types = {Fraction(1, 2): ('eighth', False), Fraction(1): ('quarter', False),
             Fraction(3, 2): ('quarter', True), Fraction(2): ('half', False),
             Fraction(3): ('half', True), Fraction(4): ('whole', False),
             Fraction(6): ('whole', True)}
    for pi, bars in enumerate(parts):
        part = sub(root, 'part', id=f'P{pi+1}')
        for bi, bar in enumerate(bars):
            partial = d['lengths'][bi] != Fraction(d['time'][0]*4, d['time'][1])
            m = sub(part, 'measure', number=str(bi if slug != 'we-three-kings' else bi+1),
                    **({'implicit': 'yes'} if partial else {}))
            if bi == 0:
                a = sub(m, 'attributes'); sub(a, 'divisions', 2)
                sub(sub(a, 'key'), 'fifths', d['key'])
                ts = sub(a, 'time'); sub(ts, 'beats', d['time'][0]); sub(ts, 'beat-type', d['time'][1])
                c = sub(a, 'clef'); sub(c, 'sign', 'F' if pi == 3 else 'G'); sub(c, 'line', 4 if pi == 3 else 2)
                if pi == 2: sub(c, 'clef-octave-change', -1)
                if pi == 0:
                    direction = sub(m, 'direction', placement='above')
                    dt = sub(direction, 'direction-type'); met = sub(dt, 'metronome')
                    sub(met, 'beat-unit', 'half' if slug == 'while-shepherds-watched' else 'quarter')
                    sub(met, 'per-minute', d['tempo']//2 if slug == 'while-shepherds-watched' else d['tempo'])
                    sub(direction, 'sound', tempo=str(d['tempo']))
            for ni, (pitch, dur) in enumerate(bar):
                n = sub(m, 'note'); p = sub(n, 'pitch')
                match = re.fullmatch(r'([A-G])([#b]?)(\d)', pitch)
                step, accidental, octave = match.groups()
                sub(p, 'step', step)
                alter = {'#': 1, 'b': -1}.get(accidental, 0)
                sub(p, 'alter', alter); sub(p, 'octave', octave)
                sub(n, 'duration', int(dur*2))
                ties = [(a,b) for v,m_,a,b in d['ties'] if v==pi and m_==bi]
                for a,b in ties:
                    if ni == a: sub(n, 'tie', type='start')
                    if ni == b: sub(n, 'tie', type='stop')
                typ, dot = types[dur]; sub(n, 'type', typ)
                if dot: sub(n, 'dot')
                explicit_accidental = d.get('accidentals', {}).get((pi, bi, ni))
                if explicit_accidental: sub(n, 'accidental', explicit_accidental)
                notations = []
                for a,b in ties:
                    if ni == a: notations.append(('tied', {'type':'start'}))
                    if ni == b: notations.append(('tied', {'type':'stop'}))
                for si,(v,m_,a,b) in enumerate(d['slurs']):
                    if v==pi and m_==bi:
                        if ni==a: notations.append(('slur', {'type':'start','number':str(si%6+1)}))
                        if ni==b: notations.append(('slur', {'type':'stop','number':str(si%6+1)}))
                if notations:
                    nt=sub(n, 'notations')
                    for tag,attrs in notations:sub(nt,tag,**attrs)
                if pi == 0:
                    for li, lyrics in enumerate(d['lyrics'],1):
                        words=lyrics[bi].split()
                        if not words: continue
                        assert len(words)==len(bar),(slug, bi, words,bar)
                        word=words[ni]
                        if word == '_': continue
                        ly=sub(n,'lyric',number=str(li))
                        prev=words[ni-1] if ni else ''
                        syll=('middle' if prev.endswith('-') else 'begin') if word.endswith('-') else ('end' if prev.endswith('-') else 'single')
                        sub(ly,'syllabic',syll);sub(ly,'text',word.removesuffix('-'))
                        if ni+1<len(words) and words[ni+1]=='_':sub(ly,'extend',type='start')
                ledger.append(f'{VOICES[pi]}\t{bi+1}\t{ni+1}\t{pitch}\t{dur}')
            if bi == d.get('repeat'):
                bl=sub(m,'barline',location='right');sub(bl,'repeat',direction='backward')
            elif bi == len(bars)-1:
                sub(sub(m,'barline',location='right'),'bar-style','light-heavy')
            elif slug != 'we-three-kings' and bi in (2,5,8):
                sub(sub(m,'barline',location='right'),'bar-style','light-light')
    folder=HERE/slug
    ET.indent(root)
    ET.ElementTree(root).write(folder/f'{slug}.musicxml', encoding='utf-8',xml_declaration=True)
    (folder/'source-ledger.tsv').write_text('\n'.join(ledger)+'\n')
    print(slug, len(bars), 'source bars;', sum(d['lengths']), 'quarters before repeats')


def append_stanzas(slug, data):
    path = HERE / slug / (slug + '.mscz')
    with zipfile.ZipFile(path) as z:
        files = {n: z.read(n) for n in z.namelist()}
    name = next(n for n in files if n.endswith('.mscx'))
    root = ET.fromstring(files[name])
    staff = root.find('Score/Staff')
    assert staff is not None
    # Safe to repeat this operation on a CLI-stage score.
    for frame in list(staff.findall('VBox')):
        if any('Additional stanzas' in ''.join(t.itertext()) for t in frame.findall('Text')):
            staff.remove(frame)
    text = 'Additional stanzas — repeat the music when singing; playback runs once.\n\n' + '\n\n'.join(data['stanzas'])
    vbox = sub(staff, 'VBox')
    sub(vbox, 'height', 6 + 2.8 * len(text.splitlines()))
    txt = sub(vbox, 'Text');sub(txt, 'style', 'frame');sub(txt, 'fontSize', 10)
    # MuseScore's text field contains its own escaped rich-text markup.
    sub(txt, 'text', text)
    files[name] = ET.tostring(root, encoding='utf-8', xml_declaration=True)
    tmp = path.with_suffix('.tmp')
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as z:
        for n, content in files.items(): z.writestr(n, content)
    tmp.replace(path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--append-stanzas', action='store_true', help='append text to existing CLI-stage .mscz files, before GUI save')
    args = parser.parse_args()
    for slug, data in DATA.items():
        if args.append_stanzas: append_stanzas(slug, data)
        else: build(slug, data)
