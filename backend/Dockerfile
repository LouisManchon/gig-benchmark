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
# - default-libmysqlclient-dev: MySQL client headers for mysqlclient
# - curl, ca-certificates: network tooling and TLS trust store
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
# Set the working directory inside the container
# ------------------------------------------------------------------------------
WORKDIR /app

# ------------------------------------------------------------------------------
# Install Python dependencies
# - Copy requirements first to leverage Docker layer caching
# ------------------------------------------------------------------------------
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

# ------------------------------------------------------------------------------
# Copy the rest of the project (Django app code will live under /app)
# ------------------------------------------------------------------------------
COPY . /app

# ------------------------------------------------------------------------------
# Create a non-root user for better security & give it ownership of the app & venv
# ------------------------------------------------------------------------------
RUN useradd -m appuser \
    && chown -R appuser:appuser /app /venv
USER appuser

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
# ------------------------------------------------------------------------------
RUN mkdir -p "${STATIC_ROOT}"

# ------------------------------------------------------------------------------
# Expose HTTP port
# ------------------------------------------------------------------------------
EXPOSE 8000

# ------------------------------------------------------------------------------
# Default command: production-grade WSGI server with Gunicorn
# ------------------------------------------------------------------------------
CMD ["sh", "-lc", "gunicorn --bind 0.0.0.0:${PORT} --workers 3 --timeout 60 ${DJANGO_WSGI_MODULE}:application"]
