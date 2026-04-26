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
- **Catalog search**: `/api/search` uses iTunes Search API (free, no auth, works from
  cloud IPs) for tracks + albums; falls back to Spotify's API only for playlists.
  Search results download via artist+title lookup on YouTube — no Spotify URL needed.
- **Anonymous Spotify token**: scraped from `/embed/playlist/...` `__NEXT_DATA__`
  because `/get_access_token` is blocked from data-center IPs.

## API endpoints (JSON)
- `GET  /api/search?q=…&limit=8&type=all|track|album|playlist` — catalog search
- `GET  /api/stats` — `{active, total_downloads, total_songs, total_size}`
- `GET  /api/status/<dl_id>` — live progress incl. `tracks_progress[]`
- `GET  /qr/<dl_id>` — PNG QR code linking to the ZIP download
- `POST /start_download` — accepts `playlist_url` OR `itunes_album_id` OR
  `itunes_track="artist|title|cover|album"`

## Pages
- `/landing` — public marketing landing page (white, mint/teal accents,
  emergent.sh-inspired, with hero, dark showcase frame, features grid, CTA strip).
- `/login`   — split-screen sign-in (left: brand + password form, right: dark
  showcase). Renders even when auth is disabled, showing an "open instance" badge.
- `/`        — main app (dark theme). Redirects to `/landing` if auth is enabled
  and the user isn't signed in.
- `/logout`  — clears the session and bounces to `/landing`.

## Env vars (all optional)
- `PORT` (default 5000)
- `SESSION_SECRET` (auto-generated if missing)
- `FLASK_DEBUG` (set `true` for dev mode)
- `SPOTDL_PASSWORD` — when set, requires this access code at `/login` to use the
  app. When unset, the app is open and `/login` shows an "open instance" notice.
- `SPOTDL_ADMIN_PASSWORD` — when set, enables the hidden operator console at
  `/admin` (reachable by tapping the `♪ SpotDL` brand logo 7 times within 3
  seconds). When unset, all `/admin*` routes return 404.

## Hidden console (`/admin`)
Tap the brand logo 7× in 3s → enter `SPOTDL_ADMIN_PASSWORD` → operator panel:
- Live download queue + recent history
- Disk + storage stats, retention/worker config snapshot
- One-click actions: run cleanup, cancel all active, wipe history
- Tail of last 200 server log lines (auto-refreshing every 4s)
- Independent auth (separate `admin_authed` session flag, doesn't touch
  the public `SPOTDL_PASSWORD` gate)

## Android APK (`android/`)
Native Kotlin wrapper. Single `MainActivity` hosting a `WebView` pointed at the
deployed Flask URL (configured in `app/src/main/res/values/strings.xml`).
File downloads are handed to Android's `DownloadManager` and saved to
`/Music/SpotDL/`. Built automatically by `.github/workflows/android.yml` on
every push that touches `android/**`. See `android/README.md` for the full
build + sideload instructions.

## Retention
- Default retention is **72 hours** (3 days). Configurable in Settings between
  1 hour and 30 days. A background sweep runs hourly.
