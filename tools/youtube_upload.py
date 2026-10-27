"""Upload a piece's video (pieces/<slug>/exports/<slug>.mp4) to YouTube.

Usage: youtube-upload [--privacy unlisted|private|public] [--dry-run] [--no-push] <slug>

First run opens a browser for Google sign-in (scope youtube.upload) and saves
the token to ~/.config/publish-score/youtube-token.json (mode 600).
OAuth client: a *Desktop* client JSON from Google Cloud Console, found via
$YOUTUBE_CLIENT_SECRETS or ~/.config/publish-score/client_secret.json.
"""
import argparse, datetime, json, os, re, subprocess, sys
from pathlib import Path

REPO = Path(os.environ.get("SCORES_REPO", Path.home() / "Documents/music/scores"))
CONF = Path.home() / ".config/publish-score"
TOKEN = CONF / "youtube-token.json"
SECRETS = Path(os.environ.get("YOUTUBE_CLIENT_SECRETS", CONF / "client_secret.json")).expanduser()
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

CONSOLE_HELP = """\
You need a Desktop-type OAuth client:
  1. https://console.cloud.google.com/ -> pick (or create) your project
  2. APIs & Services -> Library -> "YouTube Data API v3" -> Enable
  3. APIs & Services -> OAuth consent screen (Google Auth Platform): User type External,
     fill app name + your email; under Audience/Test users add your own Google account
  4. APIs & Services -> Credentials -> Create credentials -> OAuth client ID ->
     Application type "Desktop app" -> Create -> Download JSON
  5. Save it as ~/.config/publish-score/client_secret.json (or set YOUTUBE_CLIENT_SECRETS)"""

def remote():
    url = subprocess.run(["git", "-C", str(REPO), "remote", "get-url", "origin"], capture_output=True, text=True).stdout.strip()
    m = re.search(r"github\.com[:/]([^/]+)/(.+?)(\.git)?$", url)
    return f"https://github.com/{m.group(1)}/{m.group(2)}" if m else None

def check_secrets():
    if not SECRETS.exists():
        sys.exit(f"OAuth client file not found: {SECRETS}\n\n{CONSOLE_HELP}")
    kind = next(iter(json.loads(SECRETS.read_text())), None)  # inspect type only
    if kind != "installed":
        sys.exit(f"{SECRETS} is a '{kind}' OAuth client; a Desktop ('installed') client is required.\n\n{CONSOLE_HELP}")

def credentials():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES) if TOKEN.exists() else None
    if creds and creds.expired and creds.refresh_token:
        try: creds.refresh(Request())
        except Exception: creds = None
    if not creds or not creds.valid:
        check_secrets()
        flow = InstalledAppFlow.from_client_secrets_file(str(SECRETS), SCOPES)
        creds = flow.run_local_server(port=0, open_browser=True, prompt="consent",
                                      success_message="Signed in. You can close this tab and return to the terminal.")
    CONF.mkdir(parents=True, exist_ok=True); os.chmod(CONF, 0o700)
    fd = os.open(TOKEN, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f: f.write(creds.to_json())
    os.chmod(TOKEN, 0o600)
    return creds

def main():
    ap = argparse.ArgumentParser(description="Upload a piece's video to YouTube")
    ap.add_argument("piece")
    ap.add_argument("--privacy", choices=["unlisted", "private", "public"], default="unlisted")
    ap.add_argument("--title"); ap.add_argument("--force", action="store_true", help="upload even if already uploaded")
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--no-push", action="store_true")
    a = ap.parse_args()
    slug = Path(a.piece).name
    d = REPO / "pieces" / slug; exp = d / "exports"
    if not d.is_dir(): sys.exit(f"No such piece: {d}")
    video = exp / f"{slug}.mp4"
    yt_file = exp / "youtube.json"
    if yt_file.exists() and not a.force and not a.dry_run:
        print(f"Already uploaded: {json.loads(yt_file.read_text()).get('url')} (use --force to upload again)"); return
    subprocess.run([str(REPO / "tools/make-video"), slug], check=True)  # builds or confirms up to date
    meta = json.loads((exp / "meta.json").read_text()) if (exp / "meta.json").exists() else {}
    t = meta.get("title") or slug; comp = meta.get("composer")
    title = a.title or (f"{t} – {comp} (MuseScore render)" if comp else f"{t} (MuseScore render)")
    title = re.sub(r"[<>]", "", title)[:100]
    repo_url = remote()
    pdf_url = f"{repo_url}/blob/main/pieces/{slug}/exports/{slug}.pdf" if repo_url else ""
    full = t + (f", {meta['subtitle']}" if meta.get("subtitle") else "") + (f" by {comp}" if comp else "")
    desc = (f"{full}.\nAudio rendered from the MuseScore score with MuseScore Studio's built-in sounds; "
            f"the score pages follow the music.\n\nScore (PDF): {pdf_url}\nAll scores, MusicXML and sources: {repo_url}\n")
    body = {"snippet": {"title": title, "description": desc, "categoryId": "10",
                        "tags": ["MuseScore", "orchestral score", comp or "", t]},
            "status": {"privacyStatus": a.privacy, "selfDeclaredMadeForKids": False}}
    body["snippet"]["tags"] = [x for x in body["snippet"]["tags"] if x]
    if a.dry_run:
        print(json.dumps({"file": str(video), "size_mb": round(video.stat().st_size / 1e6, 1), **body}, indent=2, ensure_ascii=False))
        check_secrets(); print("Client secrets OK (Desktop client)."); return
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError
    yt = build("youtube", "v3", credentials=credentials(), cache_discovery=False)
    req = yt.videos().insert(part="snippet,status", body=body,
                             media_body=MediaFileUpload(str(video), mimetype="video/mp4", chunksize=8 * 1024 * 1024, resumable=True))
    resp = None
    try:
        while resp is None:
            status, resp = req.next_chunk()
            if status: print(f"  uploaded {int(status.progress() * 100)}%", flush=True)
    except HttpError as e:
        msg = str(e)
        if "accessNotConfigured" in msg or "has not been used" in msg or "SERVICE_DISABLED" in msg:
            sys.exit(f"YouTube Data API v3 is not enabled on this Google Cloud project.\n{msg}\n\n{CONSOLE_HELP}")
        raise
    vid = resp["id"]; url = f"https://youtu.be/{vid}"
    actual = resp.get("status", {}).get("privacyStatus", a.privacy)
    yt_file.write_text(json.dumps({"id": vid, "url": url, "privacy": actual, "title": title,
        "uploaded_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")}, indent=2, ensure_ascii=False) + "\n")
    print(f"Uploaded: {url} (privacy: {actual})")
    if actual != a.privacy:
        print("Note: YouTube locked the video to private; unverified API projects can only upload private videos. "
              "Change visibility in YouTube Studio.", file=sys.stderr)
    subprocess.run([sys.executable, str(REPO / "tools/build-index.py"), str(REPO)], check=True)
    g = ["git", "-C", str(REPO)]
    subprocess.run(g + ["add", str(yt_file), "README.md", "index.html"], check=True)
    if subprocess.run(g + ["diff", "--cached", "--quiet"]).returncode:
        subprocess.run(g + ["commit", "-q", "-m", f"Add YouTube link for {slug}"], check=True)
        if not a.no_push: subprocess.run(g + ["push", "-q"], check=True); print("README updated and pushed.")

if __name__ == "__main__":
    main()
