#!/usr/bin/env python3
"""Regenerate README.md and index.html (GitHub Pages player) from pieces/*/."""
import json, sys, html, subprocess, re
from pathlib import Path

repo = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
pieces_dir = repo / "pieces"

def remote_slug():
    try:
        url = subprocess.check_output(["git", "-C", str(repo), "remote", "get-url", "origin"], text=True).strip()
        m = re.search(r"github\.com[:/]([^/]+)/(.+?)(\.git)?$", url)
        return (m.group(1), m.group(2)) if m else None
    except Exception:
        return None

def fmt_dur(sec):
    try:
        sec = int(round(float(sec))); return f"{sec // 60}:{sec % 60:02d}"
    except Exception:
        return ""

def mb(p):
    return f"{p.stat().st_size / 1e6:.1f} MB" if p.exists() else ""

pieces = []
for d in sorted(p for p in pieces_dir.iterdir() if p.is_dir()) if pieces_dir.exists() else []:
    slug = d.name
    exp = d / "exports"
    meta = {}
    try: meta = json.loads((exp / "meta.json").read_text())
    except Exception: pass
    pngs = sorted((exp / "png").glob("*.png"), key=lambda p: [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", p.name)]) if (exp / "png").exists() else []
    yt = {}
    try: yt = json.loads((exp / "youtube.json").read_text())
    except Exception: pass
    pieces.append(dict(slug=slug, meta=meta, yt=yt, exp=exp, pngs=pngs,
        files={k: exp / f"{slug}.{k}" for k in ("pdf", "musicxml", "mp3")}, mscz=d / f"{slug}.mscz"))

rs = remote_slug()
pages_url = f"https://{rs[0]}.github.io/{rs[1]}/" if rs else None

def rel(p): return p.relative_to(repo).as_posix()

lines = ["# MuseScore scores", "",
         "Scores written in MuseScore Studio, exported automatically by "
         "[`tools/publish-score`](tools/publish-score): PDF score, MusicXML and an MP3 render.", ""]
if pages_url:
    lines += [f"**Listen in the browser:** {pages_url}", ""]
lines += ["| Piece | Composer | Length | Score | Audio | Source |", "|---|---|---|---|---|---|"]
for p in pieces:
    m = p["meta"]; f = p["files"]
    title = m.get("title") or p["slug"]
    if m.get("subtitle"): title += f" ({m['subtitle']})"
    score = " · ".join(x for x in [
        f"[PDF]({rel(f['pdf'])})" if f["pdf"].exists() else "",
        f"[MusicXML]({rel(f['musicxml'])})" if f["musicxml"].exists() else "",
        f"[pages]({rel(p['exp'] / 'png')})" if p["pngs"] else ""] if x)
    audio = f"[MP3]({rel(f['mp3'])}) ({mb(f['mp3'])})" if f["mp3"].exists() else ""
    if audio and pages_url: audio += f" · [▶ play]({pages_url}#{p['slug']})"
    if p["yt"].get("url"): audio += f" · [YouTube]({p['yt']['url']})"
    src = f"[.mscz]({rel(p['mscz'])})" if p["mscz"].exists() else ""
    lines.append(f"| **{title}** `{p['slug']}` | {m.get('composer','')} | {fmt_dur(m.get('duration'))} | {score} | {audio} | {src} |")
lines += ["", "## Publishing a score", "", "```", "publish-score path/to/score.mscz [slug]", "```", "",
          "Copies the score to `pieces/<slug>/`, exports PDF, MusicXML, MP3 and page PNGs with the "
          "MuseScore CLI (headless), regenerates this README and `index.html`, then commits and pushes. "
          "Re-running on an unchanged score does nothing. Options: `--force`, `--no-png`, `--no-push`, "
          "`--sound-profile \"MuseScore Basic\"|MuseSounds`, `--video` (build an MP4 slideshow), "
          "`--youtube` (build the video and upload it unlisted).", "",
          "Videos: `make-video <slug>` writes `pieces/<slug>/exports/<slug>.mp4` (1080p, page turns timed "
          "from the score's measure positions; not committed). `youtube-upload [--privacy unlisted|private|public] <slug>` "
          "uploads it and adds the YouTube link here.", "",
          "Audio is rendered with MuseScore's built-in *MS Basic* soundfont (Muse Sounds is not installed "
          "for command-line rendering).", ""]
(repo / "README.md").write_text("\n".join(lines))

e = html.escape
cards = []
for p in pieces:
    m = p["meta"]; f = p["files"]
    title = m.get("title") or p["slug"]
    sub = " · ".join(x for x in [m.get("subtitle", ""), m.get("composer", ""), fmt_dur(m.get("duration"))] if x)
    links = " · ".join(x for x in [
        f'<a href="{e(rel(f["pdf"]))}">PDF score</a>' if f["pdf"].exists() else "",
        f'<a href="{e(rel(f["musicxml"]))}">MusicXML</a>' if f["musicxml"].exists() else "",
        f'<a href="{e(rel(f["mp3"]))}" download>MP3</a>' if f["mp3"].exists() else "",
        f'<a href="{e(p["yt"]["url"])}">YouTube video</a>' if p["yt"].get("url") else ""] if x)
    audio = f'<audio controls preload="none" src="{e(rel(f["mp3"]))}"></audio>' if f["mp3"].exists() else ""
    thumb = f'<a href="{e(rel(f["pdf"]))}"><img src="{e(rel(p["pngs"][0]))}" alt="first page" loading="lazy"></a>' if p["pngs"] else ""
    cards.append(f'<section id="{e(p["slug"])}"><h2>{e(title)}</h2><p class="sub">{e(sub)}</p>{audio}<p>{links}</p>{thumb}</section>')
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>MuseScore scores</title>
<style>body{{font-family:system-ui,sans-serif;max-width:760px;margin:2rem auto;padding:0 1rem;color:#222}}
section{{border-top:1px solid #ddd;padding:1rem 0}}audio{{width:100%}}.sub{{color:#666;margin-top:-.5rem}}
img{{max-width:220px;border:1px solid #ccc}}</style></head><body><h1>MuseScore scores</h1>
{''.join(cards) or '<p>No pieces yet.</p>'}</body></html>
"""
(repo / "index.html").write_text(page)
print(f"Index rebuilt: {len(pieces)} piece(s)")
