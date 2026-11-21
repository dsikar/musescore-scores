#!/usr/bin/env bash
# Re-runnable verification of the three findings in FINDINGS.md.
#
# Usage:  ./verify-findings.sh [path-to-musescore]
#
# Produces evidence/verification-run.txt. Takes a couple of minutes: it does
# five headless renders of the score.
#
# This script temporarily RENAMES libMuseSamplerCoreLib.so to prove MuseSampler
# is doing the synthesis, and renames it back. It restores the library on exit
# even if interrupted.

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MSCORE="${1:-$HOME/.local/bin/musescore}"
SCORE="$HERE/bwv244-54-o-haupt-voll-blut-und-wunden.mscz"
SAMPLER="$HOME/.local/share/MuseSampler/lib/libMuseSamplerCoreLib.so"
OUT="$HERE/evidence/verification-run.txt"
TMP="$(mktemp -d "${TMPDIR:-/tmp}/verify-findings.XXXXXX")"

mkdir -p "$HERE/evidence"
trap 'if [[ -f "$SAMPLER.verifying" ]]; then mv "$SAMPLER.verifying" "$SAMPLER"; echo "sampler restored by trap"; fi; rm -rf "$TMP"' EXIT

render() {  # render <output> [sound-profile]
  local out="$1" prof="${2:-}" args=()
  [[ -n $prof ]] && args=(--sound-profile "$prof")
  QT_QPA_PLATFORM=offscreen timeout 300 "$MSCORE" "${args[@]}" \
      -o "$out" "$SCORE" </dev/null >/dev/null 2>&1
  echo "$?"
}
h() { md5sum "$1" 2>/dev/null | cut -c1-32; }

{
echo "Verification run: $(date -u '+%Y-%m-%d %H:%M:%SZ')"
echo "Host kernel    : $(uname -r)"
echo "MuseScore      : $(QT_QPA_PLATFORM=offscreen "$MSCORE" --long-version 2>/dev/null | grep -o 'Version [0-9.]*; Build [0-9a-f]*' | head -1)"
echo "Sampler        : $([[ -f $SAMPLER ]] && echo "present ($(stat -c%s "$SAMPLER") bytes)" || echo MISSING)"
echo "Muse Choir     : $([[ -d $HOME/Muse\ Sounds/Muse\ Choir ]] && du -sh "$HOME/Muse Sounds/Muse Choir" | cut -f1 || echo MISSING)"
echo

echo "== Finding 0: renders are deterministic =="
echo "(without this, comparing hashes proves nothing)"
render "$TMP/det1.mp3" "MuseScore Basic" >/dev/null
render "$TMP/det2.mp3" "MuseScore Basic" >/dev/null
D1=$(h "$TMP/det1.mp3"); D2=$(h "$TMP/det2.mp3")
echo "  MS Basic render #1 : $D1"
echo "  MS Basic render #2 : $D2"
[[ "$D1" == "$D2" ]] && echo "  RESULT: PASS - deterministic" || echo "  RESULT: FAIL - nondeterministic, later hash tests are meaningless"
echo

echo "== Finding 1: Muse Sounds drives headless CLI rendering =="
render "$TMP/muse.mp3" "MuseSounds" >/dev/null
MUSE=$(h "$TMP/muse.mp3"); BASIC="$D1"
echo "  MuseSounds profile : $MUSE"
echo "  MS Basic profile   : $BASIC"
[[ "$MUSE" != "$BASIC" ]] && echo "  RESULT: PASS - profiles produce different audio" || echo "  RESULT: FAIL - identical, Muse Sounds not engaging"
echo

echo "== Finding 2: with the sampler gone, MuseSounds silently becomes MS Basic =="
if [[ -f "$SAMPLER" ]]; then
  mv "$SAMPLER" "$SAMPLER.verifying"
  RC=$(render "$TMP/nosampler.mp3" "MuseSounds")
  mv "$SAMPLER.verifying" "$SAMPLER"
  NOS=$(h "$TMP/nosampler.mp3")
  echo "  sampler hidden     : $NOS   (exit code $RC)"
  echo "  MS Basic           : $BASIC"
  [[ "$NOS" == "$BASIC" ]] && echo "  RESULT: PASS - falls back to MS Basic" || echo "  RESULT: unexpected - no fallback match"
  [[ "$RC" == "0" ]] && echo "  NOTE: exit code 0 and an MP3 was still written. The failure is silent."
  echo "  sampler restored   : $([[ -f $SAMPLER ]] && echo yes || echo NO-INTERVENE)"
else
  echo "  SKIPPED - sampler not present"
fi
echo

echo "== Finding 3: Muse Choir ignores the notated lyrics =="
if command -v python3 >/dev/null && command -v unzip >/dev/null && command -v zip >/dev/null; then
  rm -rf "$TMP/z"; mkdir -p "$TMP/z"
  unzip -q "$SCORE" -d "$TMP/z"
  MSCX=$(find "$TMP/z" -name '*.mscx' | head -1)
  N=$(python3 -I -c "
import re,sys
p=sys.argv[1]; d=open(p,encoding='utf-8').read()
n=len(re.findall(r'<Lyrics>',d))
open(p,'w',encoding='utf-8').write(re.sub(r'<Lyrics>.*?</Lyrics>\s*','',d,flags=re.S))
print(n)" "$MSCX")
  (cd "$TMP/z" && zip -q -r "$TMP/nolyrics.mscz" .)
  QT_QPA_PLATFORM=offscreen timeout 300 "$MSCORE" --sound-profile MuseSounds \
      -o "$TMP/nolyrics.mp3" "$TMP/nolyrics.mscz" </dev/null >/dev/null 2>&1
  NL=$(h "$TMP/nolyrics.mp3")
  echo "  lyric blocks removed : $N"
  echo "  with lyrics          : $MUSE"
  echo "  without lyrics       : $NL"
  if [[ -z "$NL" ]]; then
    echo "  RESULT: INCONCLUSIVE - stripped score failed to render"
  elif [[ "$NL" == "$MUSE" ]]; then
    echo "  RESULT: PASS - byte-identical, lyrics do not affect playback"
  else
    echo "  RESULT: lyrics DO affect playback on this setup (differs from the recorded finding)"
  fi
else
  echo "  SKIPPED - needs python3, unzip and zip"
fi
echo

echo "== Recorded sound assignments in the committed score =="
unzip -p "$SCORE" audiosettings.json 2>/dev/null | python3 -I -c "
import json,sys
d=json.load(sys.stdin)
print('  activeSoundProfile:', d['activeSoundProfile'])
for t in sorted(d['tracks'], key=lambda t: t['instrumentId']):
    a=t['in']['resourceMeta'].get('attributes',{})
    print(f\"  {t['instrumentId']:10} -> {a.get('musePack','(fluid)'):12} / {a.get('museName','-'):10} uid={a.get('museUID','-')}\")
" 2>/dev/null || echo "  (could not read audiosettings.json)"
} 2>&1 | tee "$OUT"

echo
echo "Written to: $OUT"
