# ------------------------------------------------------------------------------
# Base image: Official PHP 8.2 with Apache HTTPD
# Provides Apache + PHP pre-installed (stable, maintained upstream).
# ------------------------------------------------------------------------------
FROM php:8.2-apache AS base

# ------------------------------------------------------------------------------
# Install system dependencies required by PHP extensions and Composer
# - git, unzip: needed by Composer for installing packages
# - libicu-dev: required for intl extension (i18n, formatting, etc.)
# - libzip-dev: required for zip extension
# ------------------------------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    git unzip libicu-dev libzip-dev \
    && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------------------
# Install PHP extensions commonly needed by Symfony
# - pdo_mysql: Database driver for MySQL/MariaDB
# - intl: Internationalization (dates, locales, currencies)
# - zip: Used by Symfony and Composer for archive handling
# - opcache: Boosts PHP performance by caching compiled scripts
# ------------------------------------------------------------------------------
RUN docker-php-ext-configure intl \
    && docker-php-ext-install -j"$(nproc)" pdo_mysql intl zip opcache

# ------------------------------------------------------------------------------
# Enable Apache modules required by Symfony
# - rewrite: allows clean URLs via front controller (index.php)
# - headers: for setting HTTP security and cache headers
# ------------------------------------------------------------------------------
RUN a2enmod rewrite headers

# ------------------------------------------------------------------------------
# Configure Apache DocumentRoot to point to /public (Symfony web root)
# By default it's /var/www/html, we override it to /var/www/html/public
# ------------------------------------------------------------------------------
ENV APACHE_DOCUMENT_ROOT=/var/www/html/public
RUN set -eux; \
    sed -ri "s#DocumentRoot /var/www/html#DocumentRoot ${APACHE_DOCUMENT_ROOT}#g" /etc/apache2/sites-available/000-default.conf; \
    sed -ri "s#<Directory /var/www/>#<Directory ${APACHE_DOCUMENT_ROOT}/>#g" /etc/apache2/apache2.conf; \
    sed -ri "s#<Directory /var/www/html/>#<Directory ${APACHE_DOCUMENT_ROOT}/>#g" /etc/apache2/apache2.conf

# ------------------------------------------------------------------------------
# Add Composer binary (from official Composer image)
# ------------------------------------------------------------------------------
COPY --from=composer:2 /usr/bin/composer /usr/local/bin/composer

# ------------------------------------------------------------------------------
# Set working directory to Symfony project root
# ------------------------------------------------------------------------------
WORKDIR /var/www/html


# ==============================================================================
# Builder stage: install Composer deps with cache-friendly layers
# (no rebuild when you down)
# ==============================================================================
FROM base AS builder

# ------------------------------------------------------------------------------
# Copy only composer files first (cache layer for deps)
# ------------------------------------------------------------------------------
COPY --chown=www-data:www-data composer.json ./

# ------------------------------------------------------------------------------
# Install PHP dependencies (prod by default; switch with --build-arg APP_ENV=dev)
# ------------------------------------------------------------------------------
ARG APP_ENV=prod
ENV APP_ENV=${APP_ENV}

# --no-dev en prod, sinon on garde les dev-deps
RUN if [ "$APP_ENV" = "prod" ]; then \
    composer install --no-dev --no-interaction --prefer-dist --no-progress --optimize-autoloader; \
    else \
    composer install --no-interaction --prefer-dist --no-progress; \
    fi

# ------------------------------------------------------------------------------
# Copy the rest of the application source
# ------------------------------------------------------------------------------
COPY --chown=www-data:www-data . .

# ==============================================================================
# Runtime stage
# ==============================================================================
FROM base AS runtime

# ------------------------------------------------------------------------------
# Copy app from builder (vendor + code + public)
# ------------------------------------------------------------------------------
COPY --from=builder --chown=www-data:www-data /var/www/html /var/www/html

# ------------------------------------------------------------------------------
# Opcache recommended settings (améliore les perfs en prod)
# ------------------------------------------------------------------------------
RUN { \
    echo 'opcache.enable=1'; \
    echo 'opcache.validate_timestamps=0'; \
    echo 'opcache.preload=/var/www/html/config/preload.php'; \
    echo 'opcache.preload_user=www-data'; \
    } > /usr/local/etc/php/conf.d/opcache-recommended.ini || true

# ------------------------------------------------------------------------------
# Permissions: Apache (www-data) should own app dir for cache/logs
# ------------------------------------------------------------------------------
RUN chown -R www-data:www-data /var/www/html
USER www-data

# ------------------------------------------------------------------------------
# Expose Apache default port
# ------------------------------------------------------------------------------
EXPOSE 80

# ------------------------------------------------------------------------------
# Default command (Apache in foreground)
# ------------------------------------------------------------------------------
CMD ["apache2-foreground"]
