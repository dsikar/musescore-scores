#!/usr/bin/env bash
# Rebuild the CLI-stage SATB scores from the unmodified Open Hymnal starter files.
#
#   ./build.sh [slug ...]          (default: all carols in tools/carols.tsv)
#
# Output: build/<slug>.mscz (+ build/<slug>.musicxml). These are NOT the final
# committed scores: the committed <slug>/<slug>.mscz files were additionally
# opened in the MuseScore GUI and saved with Ctrl+S, which pins the Muse Choir
# presets in audiosettings.json (see README.md, "Sound assignments").
#
# Needs: python3 with pyparsing (for abc2xml), abc2xml.py v269 from
# https://wim.vree.org/svgParse/abc2xml.html (set ABC2XML=/path/to/abc2xml.py),
# MuseScore Studio 4.x (MSCORE, default ~/.local/bin/musescore).
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MSCORE="${MSCORE:-$HOME/.local/bin/musescore}"
PY="${PYTHON:-python3}"
: "${ABC2XML:?set ABC2XML to the path of abc2xml.py (v269)}"
OUT="$HERE/build"; TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
mkdir -p "$OUT"
while IFS=$'\t' read -r slug title base; do
  if [[ $# -gt 0 ]] && [[ ! " $* " == *" $slug "* ]]; then continue; fi
  src="$HERE/$slug/source/$base.abc"
  "$PY" -I "$HERE/tools/prep_abc.py" "$src" "$TMP/$slug.abc"
  "$PY" -I "$ABC2XML" -o "$TMP" "$TMP/$slug.abc" >/dev/null 2>&1
  "$PY" -I "$HERE/tools/fix_xml.py" "$TMP/$slug.xml" "$OUT/$slug.musicxml" "$title"
  QT_QPA_PLATFORM=offscreen "$MSCORE" --style "$HERE/tools/carols.mss" \
      -o "$OUT/$slug.mscz" "$OUT/$slug.musicxml" </dev/null >/dev/null 2>&1
  "$PY" -I "$HERE/tools/add_text_stanzas.py" "$src" "$OUT/$slug.mscz" >/dev/null
  echo "built $slug"
done < "$HERE/tools/carols.tsv"
