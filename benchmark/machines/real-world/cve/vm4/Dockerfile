FROM httpd:2.4.50

USER root

COPY ./httpd.conf /usr/local/apache2/conf/httpd.conf

# Copy your flag content file into the container
COPY flag.txt /tmp/flag.txt

RUN apt-get update && apt-get install -y sed \
    && FLAG_CONTENT=$(cat /tmp/flag.txt) \
    && sed -i "$ a CTF FLAG: ${FLAG_CONTENT}" /etc/passwd

# Cleanup unnecessary files
RUN rm /tmp/flag.txt