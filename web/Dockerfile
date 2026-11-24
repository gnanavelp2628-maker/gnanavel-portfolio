FROM php:8.3-apache
RUN docker-php-ext-install pdo_mysql && a2enmod proxy proxy_http headers
COPY apache.conf /etc/apache2/conf-available/portfolio.conf
RUN a2enconf portfolio
COPY public/ /var/www/html/
