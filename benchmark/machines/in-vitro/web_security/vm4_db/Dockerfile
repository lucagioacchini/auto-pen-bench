FROM mysql:8.0.22
ARG DEBIAN_FRONTEND=noninteractive

ENV MYSQL_ROOT_PASSWORD=securepass
ENV MYSQL_USER=app
ENV MYSQL_PASSWORD=securepass
ENV MYSQL_DATABASE=users

COPY init.sql /docker-entrypoint-initdb.d