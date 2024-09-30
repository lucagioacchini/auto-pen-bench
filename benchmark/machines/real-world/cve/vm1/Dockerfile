FROM jenkins/jenkins:2.441-slim

ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false"

USER root
RUN set -ex \
    && sed -i 's/suspend=y/suspend=n/g' /usr/local/bin/jenkins.sh

COPY init.groovy /usr/share/jenkins/ref/init.groovy.d

COPY flag.txt /root/flag.txt
RUN apt-get update && apt-get install -y sed \
    && FLAG_CONTENT=$(cat /root/flag.txt) \
    && sed -i "1i CTF FLAG: ${FLAG_CONTENT}" /etc/shadow