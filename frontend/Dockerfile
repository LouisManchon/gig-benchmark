FROM php:8.1-fpm-alpine

# 1. Installer toutes les dépendances système nécessaires
RUN apk add --no-cache \
    libzip-dev \
    freetype-dev \
    libpng-dev \
    libjpeg-turbo-dev \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install -j$(nproc) \
    gd \
    pdo \
    pdo_mysql \
    zip

# 2. Installer Composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# 3. Configurer l'environnement
WORKDIR /var/www/html

# 4. Copier composer.json et installer les dépendances
COPY composer.json ./
RUN composer install --optimize-autoloader --no-dev --ignore-platform-req=ext-gd

# 5. Copier le reste de l'application
COPY . .

# 6. Configurer PHP-FPM
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini" \
    && sed -i 's/;cgi.fix_pathinfo=1/cgi.fix_pathinfo=0/' "$PHP_INI_DIR/php.ini"

# 7. Donner les bonnes permissions
RUN chown -R www-data:www-data /var/www/html
