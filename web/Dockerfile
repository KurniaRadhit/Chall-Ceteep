FROM php:8.2-cli-alpine

RUN apk add --no-cache --virtual .build-deps $PHPIZE_DEPS mariadb-connector-c-dev \
    && docker-php-ext-install mysqli \
    && apk del .build-deps

COPY src/ /var/www/html/
WORKDIR /var/www/html

ENV PHP_CLI_SERVER_WORKERS=4
EXPOSE 80
CMD ["php", "-S", "0.0.0.0:80", "-t", "/var/www/html"]
