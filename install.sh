#!/usr/bin/env bash
# SpotDL — quick installer for Linux, macOS, Termux (Android), and most servers.
# Detects your platform, installs Python + ffmpeg if missing, then starts the app.
#
# Usage:
#   bash install.sh            # install + start
#   bash install.sh --no-start # only install
set -e

GREEN='\033[1;32m'; YELLOW='\033[1;33m'; RED='\033[1;31m'; NC='\033[0m'
say()  { printf "${GREEN}[spotdl]${NC} %s\n" "$*"; }
warn() { printf "${YELLOW}[spotdl]${NC} %s\n" "$*"; }
die()  { printf "${RED}[spotdl]${NC} %s\n" "$*"; exit 1; }

START=1
for arg in "$@"; do
  [ "$arg" = "--no-start" ] && START=0
done

# ─── Platform detection ───────────────────────────────────────────────────────
IS_TERMUX=0; IS_MAC=0; IS_DEBIAN=0; IS_ALPINE=0; IS_REDHAT=0; IS_ARCH=0
if [ -n "$PREFIX" ] && echo "$PREFIX" | grep -qi "com.termux"; then IS_TERMUX=1
elif [ "$(uname)" = "Darwin" ]; then IS_MAC=1
elif command -v apt-get >/dev/null 2>&1; then IS_DEBIAN=1
elif command -v apk >/dev/null 2>&1; then IS_ALPINE=1
elif command -v dnf >/dev/null 2>&1 || command -v yum >/dev/null 2>&1; then IS_REDHAT=1
elif command -v pacman >/dev/null 2>&1; then IS_ARCH=1
fi

# ─── Install python + ffmpeg ──────────────────────────────────────────────────
install_pkg() {
  if command -v "$1" >/dev/null 2>&1; then return 0; fi
  say "Installing $1…"
  if   [ $IS_TERMUX -eq 1 ];  then pkg install -y "$2"
  elif [ $IS_MAC -eq 1 ];     then command -v brew >/dev/null || die "Install Homebrew first: https://brew.sh"; brew install "$2"
  elif [ $IS_DEBIAN -eq 1 ];  then sudo apt-get update -qq && sudo apt-get install -y "$2"
  elif [ $IS_ALPINE -eq 1 ];  then sudo apk add --no-cache "$2"
  elif [ $IS_REDHAT -eq 1 ];  then sudo dnf install -y "$2" 2>/dev/null || sudo yum install -y "$2"
  elif [ $IS_ARCH -eq 1 ];    then sudo pacman -Sy --noconfirm "$2"
  else die "Unknown platform — install '$2' manually."
  fi
}

if [ $IS_TERMUX -eq 1 ]; then
  pkg update -y >/dev/null 2>&1 || true
  install_pkg python  python
  install_pkg ffmpeg  ffmpeg
  install_pkg git     git
else
  install_pkg python3 python3
  install_pkg ffmpeg  ffmpeg
fi

PY=$(command -v python3 || command -v python)
[ -z "$PY" ] && die "Python not found after install."
say "Using Python: $($PY --version)"

# ─── Install Python deps ──────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
[ -f requirements.txt ] || die "requirements.txt not found in $SCRIPT_DIR"

say "Installing Python packages…"
$PY -m pip install --upgrade pip >/dev/null
# --break-system-packages is needed on newer pip/distro pairings; fall back if unsupported.
$PY -m pip install -r requirements.txt --break-system-packages 2>/dev/null \
  || $PY -m pip install -r requirements.txt

mkdir -p data downloads

if [ $START -eq 0 ]; then
  say "Install complete. Run: $PY src/web_app.py"
  exit 0
fi

# ─── Start the server ─────────────────────────────────────────────────────────
PORT="${PORT:-5000}"
say "Starting SpotDL on http://localhost:$PORT  (Ctrl+C to stop)"
exec $PY src/web_app.py
