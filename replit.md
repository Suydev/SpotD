# SpotDL

Flask-based web app for downloading Spotify playlists/albums/tracks and YouTube videos.
No credentials, no Premium. Track metadata scraped from Spotify's public embed page;
audio/video pulled from YouTube via yt-dlp; cover art + lyrics embedded with mutagen.

## Stack
- Python 3.12, Flask 3, gunicorn
- yt-dlp, mutagen, requests, pillow, flask-sqlalchemy
- ffmpeg (system dep, for audio conversion)

## Layout
- `src/web_app.py` — single-file Flask app (routes, scraper, downloader, tagger)
- `src/templates/` — Jinja2 templates (base, index, status, downloads, settings, deploy, browse)
- `src/static/` — PWA manifest, icons, service worker
- `data/config.json` — persisted user preferences
- `data/sessions.json` — persisted download history (survives restarts)
- `downloads/<dl_id>/…zip` — completed ZIP files (kept for `retention_hours`, default 24h)
- `install.sh` — one-line installer for Linux / macOS / Termux / servers
- `Dockerfile` + `docker-compose.yml` — container deployment
- `requirements.txt` — Python deps

## Replit Setup
- Workflow `Server` runs `python3 src/web_app.py` on port 5000 (binds `0.0.0.0`).
- Deployment target: **vm** with gunicorn:
  `gunicorn --bind=0.0.0.0:5000 --workers=2 --threads=4 --timeout=600 --chdir src web_app:app`

## Key behaviors
- **Concurrent downloads**: configurable parallel workers (default 4) speed up playlists ~4×.
- **Persistent files**: ZIPs live under `downloads/<dl_id>/` until they age out
  (configurable retention, default 24h) — re-downloads work indefinitely.
- **Restart-safe**: session metadata persisted to `data/sessions.json`; entries whose
  files no longer exist are pruned on load.
- **Spotify scraper**: parses `__NEXT_DATA__` from `open.spotify.com/embed/<kind>/<id>`
  with a fallback to legacy script-tag JSON.

## Env vars (all optional)
- `PORT` (default 5000)
- `SESSION_SECRET` (auto-generated if missing)
- `FLASK_DEBUG` (set `true` for dev mode)
