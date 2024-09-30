# Use an official PHP image with Apache
FROM php:7.4-apache

# Enable mysqli extension
RUN docker-php-ext-install mysqli

# Copy the HTML and PHP files to the Apache document root
COPY index.html /var/www/html/
COPY app.php /var/www/html/

# Set up the working directory
WORKDIR /var/www/html