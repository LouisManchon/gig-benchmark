# ------------------------------------------------------------------------------
# Base image: Python 3.11 slim (balanced size + great binary wheels support)
# ------------------------------------------------------------------------------
FROM python:3.11-slim

# ------------------------------------------------------------------------------
# Prevent Python from writing .pyc files and enable unbuffered logs (Docker best practices)
# ------------------------------------------------------------------------------
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# ------------------------------------------------------------------------------
# Install system packages commonly required by Django + MySQL:
# - build-essential: compilers for native extensions (e.g., pillow)
# - default-libmysqlclient-dev / libmariadb-dev-compat: headers for mysqlclient
# ------------------------------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    libmariadb-dev-compat \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------------------
# Create and activate a dedicated virtualenv (keeps global site-packages clean)
# ------------------------------------------------------------------------------
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# ------------------------------------------------------------------------------
# Working directory
# ------------------------------------------------------------------------------
WORKDIR /app

# ------------------------------------------------------------------------------
# Install Python dependencies
# ------------------------------------------------------------------------------
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt gunicorn

# ------------------------------------------------------------------------------
# Copy project files (including gunicorn.conf.py and entrypoint.sh)
# ------------------------------------------------------------------------------
COPY . /app

# ------------------------------------------------------------------------------
# Create non-root user and set permissions
# ------------------------------------------------------------------------------
RUN useradd -m appuser \
    && chown -R appuser:appuser /app /venv
USER appuser

# ------------------------------------------------------------------------------
# Runtime environment
# ------------------------------------------------------------------------------
ENV PORT=8000 \
    DJANGO_SETTINGS_MODULE=app.settings \
    DJANGO_WSGI_MODULE=app.wsgi \
    STATIC_ROOT=/app/staticfiles

# ------------------------------------------------------------------------------
# Ensure STATIC_ROOT exists
# ------------------------------------------------------------------------------
RUN mkdir -p "${STATIC_ROOT}"

# ------------------------------------------------------------------------------
# Make entrypoint executable
# ------------------------------------------------------------------------------
RUN chmod +x /app/entrypoint.sh

# ------------------------------------------------------------------------------
# Expose HTTP port
# ------------------------------------------------------------------------------
EXPOSE 8000

# ------------------------------------------------------------------------------
# Start via entrypoint (wait DB -> migrate -> collectstatic -> gunicorn)
# ------------------------------------------------------------------------------
CMD ["/app/entrypoint.sh"]
