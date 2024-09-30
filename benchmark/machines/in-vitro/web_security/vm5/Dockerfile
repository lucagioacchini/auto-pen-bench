# Use an official PHP image with Apache
FROM php:7.4-apache

COPY app /var/www/html

# Create the uploads directory and set permissions
RUN mkdir -p /var/www/html/uploads && \
    chown -R www-data:www-data /var/www/html/uploads && \
    chmod -R 755 /var/www/html/uploads

# Ensure the Apache server runs as the correct user
USER www-data

EXPOSE 80