# ------------------------------------------------------------------------------
# Lightweight, production-friendly Python base (Debian slim variant).
# Python 3.11 chosen for broad compatibility with common scraping libraries.
# ------------------------------------------------------------------------------
FROM python:3.11-slim

# ------------------------------------------------------------------------------
# System build tools and headers commonly required by scraping stacks:
# - build-essential: compilers for native extensions
# - libxml2-dev, libxslt1-dev: enable lxml (HTML/XML parsing)
# - libffi-dev: required by some cryptography/auth libraries
# - curl, ca-certificates: network tooling and TLS roots
# Keep it minimal; add only what's necessary for your dependencies.
# ------------------------------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    libffi-dev \
    curl \
    ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------------------
# Create a non-root runtime user for better container security.
# ------------------------------------------------------------------------------
RUN useradd -m appuser
USER appuser

# ------------------------------------------------------------------------------
# Workdir for the scraper application code.
# ------------------------------------------------------------------------------
WORKDIR /app

# ------------------------------------------------------------------------------
# Install Python dependencies via requirements.txt (added in next step).
# Copying the manifest first leverages Docker layer caching.
# If the file is absent/empty, pip will no-op.
# ------------------------------------------------------------------------------
COPY --chown=appuser:appuser requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt || true

# ------------------------------------------------------------------------------
# Copy the rest of the project files (your scraper sources).
# ------------------------------------------------------------------------------
COPY --chown=appuser:appuser . /app

# ------------------------------------------------------------------------------
# Default command (override with docker compose if needed).
# ------------------------------------------------------------------------------
CMD ["python", "app.py"]

