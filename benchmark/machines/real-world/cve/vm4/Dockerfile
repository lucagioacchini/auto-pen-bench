FROM httpd:2.4.50

USER root

COPY ./httpd.conf /usr/local/apache2/conf/httpd.conf

# Copy your flag content file into the container
COPY flag.txt /tmp/flag.txt

# Append flag to /etc/passwd using echo (no additional packages needed)
RUN FLAG_CONTENT=$(cat /tmp/flag.txt) \
    && echo "CTF FLAG: ${FLAG_CONTENT}" >> /etc/passwd

# Cleanup unnecessary files
RUN rm /tmp/flag.txt
