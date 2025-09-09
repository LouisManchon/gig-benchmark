# ------------------------------------------------------------------------------
# Base image: Python 3.11 slim (balanced size + great binary wheels support)
# ------------------------------------------------------------------------------
FROM python:3.11-slim

# ------------------------------------------------------------------------------
# Prevent Python from writing .pyc files and enable unbuffered logs (Docker best practices)
# ------------------------------------------------------------------------------
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ------------------------------------------------------------------------------
# Install system packages commonly required by Django stacks:
# - build-essential: compilers for native extensions (e.g., mysqlclient, pillow)
# - default-libmysqlclient-dev: MySQL client headers for mysqlclient
# - libjpeg-dev, zlib1g-dev: common for Pillow (image processing)
# - curl, ca-certificates: network tooling and TLS trust store
# ------------------------------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    libjpeg-dev \
    zlib1g-dev \
    curl \
    ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------------------
# Create a non-root user for better security
# ------------------------------------------------------------------------------
RUN useradd -m appuser
USER appuser

# ------------------------------------------------------------------------------
# Set the working directory inside the container
# ------------------------------------------------------------------------------
WORKDIR /app

# ------------------------------------------------------------------------------
# Install Python dependencies
# - Copy requirements first to leverage Docker layer caching
# - Upgrade pip for better resolver and binary wheel support
# ------------------------------------------------------------------------------
COPY --chown=appuser:appuser scraper/requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# ------------------------------------------------------------------------------
# Copy the rest of the project (Django app code will live under /app)
# ------------------------------------------------------------------------------
COPY --chown=appuser:appuser . /app

# ------------------------------------------------------------------------------
# Runtime configuration via environment variables
# - PORT: HTTP port inside the container (default 8000)
# - DJANGO_SETTINGS_MODULE: Django settings module path
# - DJANGO_WSGI_MODULE: WSGI entrypoint "package.module"
# - STATIC_ROOT: where collectstatic will place compiled assets
# ------------------------------------------------------------------------------
ENV PORT=8000 \
    DJANGO_SETTINGS_MODULE=app.settings \
    DJANGO_WSGI_MODULE=app.wsgi \
    STATIC_ROOT=/app/staticfiles

# ------------------------------------------------------------------------------
# Ensure STATIC_ROOT exists (collectstatic can target this directory)
# Note: actual 'python manage.py collectstatic --noinput' is typically run via CI
# or in an entrypoint after settings are in place.
# ------------------------------------------------------------------------------
RUN mkdir -p "${STATIC_ROOT}"

# ------------------------------------------------------------------------------
# Expose HTTP port
# ------------------------------------------------------------------------------
EXPOSE 8000

# ------------------------------------------------------------------------------
# Default command: production-grade WSGI server with Gunicorn
# - Binds to 0.0.0.0:$PORT
# - 3 workers is a sensible default; adjust per CPU/memory
# ------------------------------------------------------------------------------
CMD ["sh", "-lc", "gunicorn --bind 0.0.0.0:${PORT} --workers 3 --timeout 60 ${DJANGO_WSGI_MODULE}:application"]

