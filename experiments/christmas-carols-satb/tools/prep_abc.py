"""Prepare an Open Hymnal ABC file for abc2xml: one staff per voice.
Only the staff layout and voice names/clefs change; notes, lyrics, tempo are untouched."""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
d = open(src, encoding='latin-1').read()
d, n = re.subn(r'^%%staves.*$', '%%score S1V1 S1V2 S2V1 S2V2', d, flags=re.M)
assert n == 1, n
names = {'S1V1': ('Soprano', 'S.', 'treble'), 'S1V2': ('Alto', 'A.', 'treble'),
         'S2V1': ('Tenor', 'T.', 'bass'), 'S2V2': ('Bass', 'B.', 'bass')}
def rep(m):
    v = m.group(1); nm, ab, cl = names[v]
    return f'V: {v} clef={cl} name="{nm}" sname="{ab}"'
d, n = re.subn(r'^V:\s*(S[12]V[12])\b.*$', rep, d, flags=re.M)
assert n == 4, n
# '!()!' is an Open Hymnal custom decoration (parenthesised note); abc2xml drops it.
# Pass it through as !open! so fix_xml.py can turn it into a parenthesised notehead.
assert '!open!' not in d
d = d.replace('!()!', '!open!')
open(dst, 'w', encoding='utf-8').write(d)
