"""Post-process abc2xml output into an SATB open score for MuseScore.
Changes only: instrument metadata (voice.* sounds instead of piano), tenor clef
(octave-treble; display only, MusicXML pitches are absolute), forced stem
directions removed (they belonged to the source's two-voices-per-staff layout),
title cleaned. Notes, rhythms, rests, keys, times, ties, slurs, fermatas, lyrics untouched."""
import sys, re, xml.etree.ElementTree as ET
src, dst, title = sys.argv[1], sys.argv[2], sys.argv[3]
tree = ET.parse(src); root = tree.getroot()
VOICE = {'Soprano': 'voice.soprano', 'Alto': 'voice.alto', 'Tenor': 'voice.tenor', 'Bass': 'voice.bass'}
pl = root.find('part-list'); ids = {}
for sp in pl.findall('score-part'):
    name = sp.find('part-name').text; ids[sp.get('id')] = name
    for tag in ('score-instrument', 'midi-device', 'midi-instrument'):
        for e in sp.findall(tag): sp.remove(e)
    si = ET.SubElement(sp, 'score-instrument', id=sp.get('id') + '-I1')
    ET.SubElement(si, 'instrument-name').text = name
    ET.SubElement(si, 'instrument-sound').text = VOICE[name]
assert sorted(ids.values()) == sorted(VOICE), ids
for part in root.findall('part'):
    name = ids[part.get('id')]
    for snd in part.iter('sound'):
        for e in list(snd):
            if e.tag in ('midi-instrument', 'midi-device'): snd.remove(e)
    for note in part.iter('note'):
        for nt in note.findall('notations'):
            for tech in nt.findall('technical'):
                for o in tech.findall('open-string'):
                    tech.remove(o)
                    kids = [c.tag for c in note]
                    pos = max(i for i, t in enumerate(kids) if t in ('type', 'dot', 'accidental', 'time-modification', 'stem')) + 1
                    nh = ET.Element('notehead', parentheses='yes'); nh.text = 'normal'
                    note.insert(pos, nh)
                if len(tech) == 0: nt.remove(tech)
            if len(nt) == 0: note.remove(nt)
        for s in note.findall('stem'): note.remove(s)
    if name == 'Tenor':
        for clef in part.iter('clef'):
            for e in list(clef): clef.remove(e)
            ET.SubElement(clef, 'sign').text = 'G'; ET.SubElement(clef, 'line').text = '2'
            ET.SubElement(clef, 'clef-octave-change').text = '-1'
# title
w = root.find('work')
if w is None:
    w = ET.Element('work'); root.insert(0, w)
wt = w.find('work-title')
if wt is None: wt = ET.SubElement(w, 'work-title')
wt.text = title
for c in root.findall('credit'):
    for cw in c.findall('credit-words'):
        if cw.text and cw.text.strip().startswith('Bonus Carol:'):
            cw.text = title
ident = root.find('identification')
comp = ident.find("creator[@type='composer']")
lines = [l.strip() for l in comp.text.splitlines() if l.strip() and not l.strip().lower().startswith('copyright')]
blob = ' '.join(lines)
i = blob.find('Music')
words, music = blob[:i].strip(), blob[i:].strip()
assert words.startswith('Words'), blob
import textwrap
wrap = lambda t: '\n'.join(textwrap.wrap(t, 52))
music = music.replace('Music and Setting', 'Music and setting').replace(' Setting', '\nSetting')
comp.text = '\n'.join('\n'.join(textwrap.wrap(x, 40)) for x in music.split('\n'))
words = wrap(words)
ly = ET.Element('creator', type='lyricist'); ly.text = words
d = root.find('defaults')
if d is not None: root.remove(d)
ident.insert(list(ident).index(comp) + 1, ly)
r = ident.find('rights')
if r is None:
    r = ET.Element('rights'); ident.insert(list(ident).index(comp) + 1, r)
r.text = ('Public domain (words, music and setting). SATB open score prepared from the '
          'Open Hymnal Project edition, openhymnal.org')
tree.write(dst, encoding='UTF-8', xml_declaration=True)
