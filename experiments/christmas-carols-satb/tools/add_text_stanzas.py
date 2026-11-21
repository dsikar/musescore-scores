"""Append the stanzas that the Open Hymnal ABC prints as text (%%begintext
blocks) to the end of a .mscz as a text frame, as in the source layout."""
import sys, re, zipfile, shutil, html
abc, mscz = sys.argv[1], sys.argv[2]
d = open(abc, encoding='latin-1').read()
blocks = re.findall(r'%%begintext[^\n]*\n(.*?)%%endtext', d, re.S)
lines = []
blocks = [b for b in blocks if re.match(r'\s*%%\s*\d+\.', b)]   # stanzas only, not editorial notes
if not blocks:
    print('no text stanzas'); sys.exit(0)
for b in blocks:
    for l in b.splitlines():
        l = re.sub(r'^%%\s?', '', l).replace('\\t', ' ').strip()
        lines.append(l)
# collapse blank runs; keep stanza separation
text = re.sub(r'\n{3,}', '\n\n', '\n'.join(lines)).strip()
assert re.match(r'^\d+\.', text), text[:80]
text = re.sub(r'\n(?=\d+\.)', '\n\n', re.sub(r'\n\n+', '\n', text))   # one blank line between stanzas
body = '<br/>'.join(html.escape(l, quote=False) for l in text.split('\n'))
vbox = f'''      <VBox>
        <height>{4 + 2.2 * text.count(chr(10))}</height>
        <Text>
          <style>frame</style>
          <text>{body}</text>
          </Text>
        </VBox>
'''
zin = zipfile.ZipFile(mscz); names = zin.namelist(); data = {n: zin.read(n) for n in names}; zin.close()
mx = [n for n in names if n.endswith('.mscx')][0]
s = data[mx].decode('utf-8')
i = s.index('<Staff id="1">', s.index('</Part>'))
j = s.index('</Staff>', i)
s = s[:j] + vbox + s[j:]
data[mx] = s.encode('utf-8')
tmp = mscz + '.tmp'
with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as z:
    for n in names: z.writestr(n, data[n])
shutil.move(tmp, mscz)
print(text)
