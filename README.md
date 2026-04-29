# SpotD - Spotify Downloader

A cross-platform Spotify downloader application with Android and desktop versions.

## Project Structure

- `android/` - Android application code
- `src/` - Python backend and web application
- `.github/workflows/` - GitHub Actions CI/CD pipelines

## GitHub Actions Workflows

### 1. Android Build (`android.yml`)
Builds debug and release APKs for the Android application.

### 2. Docker Build (`docker.yml`)
Builds and pushes Docker images to Docker Hub.

### 3. Python Package CI (`python-package.yml`)
Builds, tests, and packages the Python backend for multiple Python versions (3.10, 3.11, 3.12).

## Development Setup

### Python Backend
```bash
pip install -r requirements.txt
pip install -e .
```

### Android Development
See `android/README.md` for Android-specific setup instructions.

## License
MIT License