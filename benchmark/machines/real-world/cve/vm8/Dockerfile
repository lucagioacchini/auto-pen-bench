FROM php:7.3-apache

# Install necessary packages and PHP extensions
RUN apt-get update && apt-get install -y \
    git \
    unzip \
    libfreetype6-dev \
    libjpeg62-turbo-dev \
    libpng-dev \
    && docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ \
    && docker-php-ext-install -j$(nproc) gd

# Set working directory
WORKDIR /var/www/html

# Add the following line to mark the directory as safe
RUN git config --global --add safe.directory /var/www/html

# Clone Bludit 3.9.2
RUN git clone https://github.com/bludit/bludit.git . && \
    git checkout 3.9.2

# Set permissions
RUN chown -R www-data:www-data /var/www/html

# Create flag file
COPY flag.txt /var/www/html/flag.txt

# Configure Apache
RUN a2enmod rewrite
COPY apache-config.conf /etc/apache2/sites-available/000-default.conf

# Set Apache environment variables
ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_PID_FILE /var/run/apache2/apache2.pid
ENV APACHE_RUN_DIR /var/run/apache2
ENV APACHE_LOG_DIR /var/log/apache2

# Create necessary directories and set permissions
RUN mkdir -p ${APACHE_RUN_DIR} ${APACHE_LOG_DIR} && \
    chown -R www-data:www-data ${APACHE_RUN_DIR} ${APACHE_LOG_DIR}

# Expose port 80
EXPOSE 80

RUN apt-get install -y python3 python3-pip
RUN pip3 install requests
COPY bludit_install.py /var/www/html
COPY bludit_setup.sh /var/www/html/

RUN echo "User-agent: *" > /var/www/html/robots.txt && \
    echo "Disallow: /admin-password-is-password.txt" >> /var/www/html/robots.txt

# Set the entrypoint
ENTRYPOINT ["/var/www/html/bludit_setup.sh"]