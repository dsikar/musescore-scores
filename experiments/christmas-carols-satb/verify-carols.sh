#!/usr/bin/env bash
# Re-runnable checks for every carol in this directory.
#
#   ./verify-carols.sh [path-to-musescore]
#
# For each carol listed in tools/carols.tsv:
#   1. the .mscz has exactly four parts named Soprano, Alto, Tenor, Bass
#      (MuseScore --score-meta, i.e. MuseScore itself opens and reads the file)
#   2. audiosettings.json pins Muse Choir Sopranos/Altos/Tenors/Basses
#   3. playback duration at the saved tempo is <= 300 s (--score-meta)
#   4. the PDF exists, and its page count
#   5. the starter files (Open Hymnal PDF + ABC) are present in source/
#   6. optional, if PYTHON has music21: every voice's pitch/onset sequence is
#      found note-for-note in the Open Hymnal MIDI (independent abc2midi render)
#
# Writes evidence/verify-carols-run.txt. Exit status is non-zero if any
# required check (1-5) fails.

set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MSCORE="${1:-$HOME/.local/bin/musescore}"
PY="${PYTHON:-python3}"
OUT="$HERE/evidence/verify-carols-run.txt"
mkdir -p "$HERE/evidence"
FAIL=0

{
echo "Verification run: $(date -u '+%Y-%m-%d %H:%M:%SZ')"
echo "MuseScore      : $(QT_QPA_PLATFORM=offscreen "$MSCORE" --long-version 2>/dev/null | grep -o 'Version [0-9.]*; Build [0-9a-f]*' | head -1)"
HAVE21=no; "$PY" -I -c 'import music21' 2>/dev/null && HAVE21=yes
echo "music21 (for MIDI cross-check): $HAVE21"
echo
while IFS=$'\t' read -r slug title base; do
  d="$HERE/$slug"; m="$d/$slug.mscz"; p="$d/$slug.pdf"
  echo "== $slug ($title)"
  meta=$(QT_QPA_PLATFORM=offscreen timeout 120 "$MSCORE" --score-meta "$m" </dev/null 2>/dev/null)
  r=$(python3 -I -c '
import json,sys
d=json.loads(sys.stdin.read()); d=d.get("metadata",d)
names=[p.get("name") or p.get("instrumentName") for p in d["parts"]]
print("parts=" + "/".join(names), "ok" if names==["Soprano","Alto","Tenor","Bass"] else "BAD")
print("duration=%ss tempo=%s measures=%s time=%s key=%s" % (d["duration"], d["tempo"], d["measures"], d["timesig"], d["keysig"]), "ok" if int(d["duration"])<=300 else "BAD")
' <<<"$meta" 2>&1) || r="score-meta FAILED BAD"
  echo "$r" | sed 's/^/  /'
  a=$(unzip -p "$m" audiosettings.json 2>/dev/null | python3 -I -c '
import json,sys
d=json.load(sys.stdin)
want={"soprano":"Sopranos","alto":"Altos","tenor":"Tenors","bass":"Basses"}
got={t["instrumentId"]:(t["in"]["resourceMeta"].get("attributes",{}).get("musePack"),t["in"]["resourceMeta"].get("attributes",{}).get("museName")) for t in d["tracks"]}
ok=d.get("activeSoundProfile")=="MuseSounds" and all(got.get(k)==("Muse Choir",v) for k,v in want.items())
print("audiosettings: profile=%s " % d.get("activeSoundProfile") + ", ".join("%s->%s/%s" % (k,*got.get(k,("-","-"))) for k in want), "ok" if ok else "BAD")
' 2>&1) || a="audiosettings unreadable BAD"
  echo "  $a"
  if [[ -f $p ]]; then echo "  pdf pages=$(pdfinfo "$p" 2>/dev/null | awk '/^Pages/{print $2}') ok"; else echo "  pdf MISSING BAD"; fi
  for ext in pdf abc; do
    [[ -f "$d/source/$base.$ext" ]] && echo "  starter $base.$ext present ok" || echo "  starter $base.$ext MISSING BAD"
  done
  if [[ $HAVE21 == yes ]]; then
    x=$(mktemp -d); unzip -q "$m" -d "$x"
    QT_QPA_PLATFORM=offscreen timeout 120 "$MSCORE" -o "$x/s.musicxml" "$m" </dev/null >/dev/null 2>&1
    "$PY" -I "$HERE/tools/midi_check.py" "$x/s.musicxml" "$d/source/$base.mid" 2>/dev/null | sed 's/^/  midi: /'
    rm -rf "$x"
  fi
  echo
done < "$HERE/tools/carols.tsv"
} 2>&1 | tee "$OUT"

grep -q 'BAD' "$OUT" && { echo "SOME CHECKS FAILED"; exit 1; }
echo "All required checks passed. Written to: $OUT"
