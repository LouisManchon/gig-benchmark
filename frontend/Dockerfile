FROM php:8.3-fpm-alpine

# 1. Installer toutes les dépendances système nécessaires + linux-headers pour sockets
RUN apk add --no-cache \
    libzip-dev \
    freetype-dev \
    libpng-dev \
    libjpeg-turbo-dev \
    linux-headers \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install -j$(nproc) \
    gd \
    pdo \
    pdo_mysql \
    zip \
    sockets

# 2. Installer Composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# 3. Configurer l'environnement
WORKDIR /var/www/html

# 4. Copier les fichiers de dépendances
COPY composer.json composer.lock* ./

# 5. Installer les dépendances Symfony
RUN composer install --optimize-autoloader --no-scripts --no-autoloader --prefer-dist

# 6. Copier le reste de l'application
COPY . .

# 7. Finaliser Composer et générer l'autoloader
RUN composer dump-autoload --optimize \
    && php bin/console cache:clear --no-warmup || true \
    && php bin/console cache:warmup || true

# 8. Créer les dossiers nécessaires et permissions
RUN mkdir -p var/cache var/log \
    && chown -R www-data:www-data /var/www/html \
    && chmod -R 775 var

# 9. Configuration PHP-FPM optimisée
RUN echo 'memory_limit = ${PHP_MEMORY_LIMIT:-256M}' >> /usr/local/etc/php/conf.d/custom.ini \
    && echo 'max_execution_time = ${PHP_MAX_EXECUTION_TIME:-60}' >> /usr/local/etc/php/conf.d/custom.ini \
    && echo 'upload_max_filesize = 50M' >> /usr/local/etc/php/conf.d/custom.ini \
    && echo 'post_max_size = 50M' >> /usr/local/etc/php/conf.d/custom.ini

EXPOSE 9000

# PHP-FPM démarre automatiquement avec l'image de base
CMD ["php-fpm"]
