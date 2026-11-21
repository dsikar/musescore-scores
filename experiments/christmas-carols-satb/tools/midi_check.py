"""Independent check: compare each voice of the prepared MusicXML against the
Open Hymnal MIDI rendering (made by abc2midi from the same ABC, a different
converter from abc2xml). Reports how many times the full single-pass
(pitch, onset-interval) sequence occurs in the MIDI track, and the best
partial alignment if it never occurs."""
import sys, music21 as m
from fractions import Fraction as F
xmlf, midf = sys.argv[1], sys.argv[2]
def seq_xml(part):
    out = []
    for n in part.flatten().notes:
        if n.tie is not None and n.tie.type in ('stop', 'continue'):
            continue  # tied continuation: no new onset
        for p in (n.pitches if n.isChord else [n.pitch]):
            out.append((F(n.getOffsetInHierarchy(part)).limit_denominator(48), p.midi))
    return out
def seq_mid(part):
    out = []
    for n in part.flatten().notes:
        for p in (n.pitches if n.isChord else [n.pitch]):
            out.append((F(n.offset).limit_denominator(48), p.midi))
    out.sort(); return out
def merge_repeats(seq):
    """Collapse consecutive onsets of the same pitch (a tie in one source, a
    re-struck note in the other: the Open Hymnal's stanza-dependent dotted ties)."""
    out = []
    for o, p in seq:
        if out and out[-1][1] == p: continue
        out.append((o, p))
    return out
def sig(seq):  # pitches + inter-onset intervals
    return [(seq[i][1], seq[i+1][0]-seq[i][0] if i+1 < len(seq) else None) for i in range(len(seq))]
x = m.converter.parse(xmlf); mi = m.converter.parse(midf)
def find(a, b, k0=0):
    # k0=1 ignores the first onset interval: at the start of a pass a merged
    # repeat can swallow the previous stanza's last note (e.g. optional pickups)
    n = len(a)
    return [st for st in range(len(b) - n + 1)
            if all(b[st+k][0] == a[k][0] and (k == n-1 or k < k0 or b[st+k][1] == a[k][1]) for k in range(n))]
ok = True; tol_ok = True
for i, (xp, mp) in enumerate(zip(x.parts, mi.parts)):
    a, b = sig(seq_xml(xp)), sig(seq_mid(mp))
    tol = len(find(sig(merge_repeats(seq_xml(xp))), sig(merge_repeats(seq_mid(mp))), k0=1))
    n = len(a); hits = []
    for st in range(len(b) - n + 1):
        if all(b[st+k][0] == a[k][0] and (k == n-1 or b[st+k][1] == a[k][1]) for k in range(n)):
            hits.append(st)
    name = xp.partName
    if hits:
        print(f'  {name:8} {n:3} onsets  exact full-pass matches in MIDI: {len(hits)}')
    else:
        ok = False
        if tol == 0: tol_ok = False
        best = (0, 0)
        for st in range(len(b)):
            k = 0
            while k < n and st+k < len(b) and b[st+k][0] == a[k][0] and (k == n-1 or b[st+k][1] == a[k][1]): k += 1
            best = max(best, (k, st))
        k, st = best
        xs = seq_xml(xp)
        print(f'  {name:8} {n:3} onsets  no exact match (diverges at score offset {float(xs[k][0]) if k < n else "-"} ql); with same-pitch splits merged: {tol} match(es)')
        print('     xml :', a[k:k+6]); print('     midi:', b[st+k:st+k+6] if st+k < len(b) else [])
print('RESULT', 'PASS (exact)' if ok else ('PASS (after merging same-pitch splits)' if tol_ok else 'MISMATCH - inspect'))
