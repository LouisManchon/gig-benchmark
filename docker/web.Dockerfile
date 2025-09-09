# ------------------------------------------------------------------------------
# Base image: Official PHP 8.2 with Apache HTTPD
# Provides Apache + PHP pre-installed (stable, maintained upstream).
# ------------------------------------------------------------------------------
FROM php:8.2-apache

# ------------------------------------------------------------------------------
# Install system dependencies required by PHP extensions and Composer
# - git, unzip: needed by Composer for installing packages
# - libicu-dev: required for intl extension (i18n, formatting, etc.)
# - libzip-dev: required for zip extension
# ------------------------------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    unzip \
    libicu-dev \
    libzip-dev \
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

# ------------------------------------------------------------------------------
# Permissions: Apache (www-data) should own app dir for cache/logs
# ------------------------------------------------------------------------------
RUN chown -R www-data:www-data /var/www/html
USER www-data

# ------------------------------------------------------------------------------
# Expose Apache default port
# ------------------------------------------------------------------------------
EXPOSE 80
