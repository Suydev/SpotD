FROM python:3.11-slim

# Install ffmpeg (required by yt-dlp for audio conversion)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Create runtime directories
RUN mkdir -p data/sessions downloads

ENV PORT=5000
EXPOSE 5000

# 2 workers, 300s timeout to handle long playlist downloads
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "300", "src.web_app:app"]
