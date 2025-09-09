# ------------------------------------------------------------------------------
# Lightweight, production-friendly Python base (Debian slim variant).
# Python 3.11 chosen for broad compatibility with common scraping libraries.
# ------------------------------------------------------------------------------
FROM python:3.11-slim

# ------------------------------------------------------------------------------
# Basic Python container best practices: no .pyc, unbuffered logs, no pip cache
# ------------------------------------------------------------------------------
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# ------------------------------------------------------------------------------
# System deps often needed by scrapers (lxml, cryptography, etc.)
# ------------------------------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libxml2-dev libxslt1-dev libffi-dev \
 && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------------------
# App workspace
# ------------------------------------------------------------------------------
WORKDIR /app

# ------------------------------------------------------------------------------
# Install Python deps (cache-friendly: copy requirements first)
# ------------------------------------------------------------------------------
COPY requirements.txt .
RUN python -m pip install --upgrade pip \
 && pip install -r requirements.txt

# ------------------------------------------------------------------------------
# Copy sources
# ------------------------------------------------------------------------------
COPY . .

# ------------------------------------------------------------------------------
# Default command (override with docker compose if needed).
# ------------------------------------------------------------------------------
CMD ["python", "app.py"]
