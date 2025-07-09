FROM lucagioacchini/kali-linux-headless:latest

USER root

ENV DEBIAN_FRONTEND noninteractive
ENV KALI_PKG=kali-linux-headless

RUN pip3 install pycryptodome
RUN mkdir /root/scripts

# update mirrors

# RUN wget https://archive.kali.org/archive-keyring.gpg -O /usr/share/keyrings/kali-archive-keyring.gpg
RUN wget -q https://http.kali.org/pool/main/k/kali-archive-keyring/kali-archive-keyring_2025.1_all.deb \
    && dpkg -i kali-archive-keyring_2025.1_all.deb \
    && rm kali-archive-keyring_2025.1_all.deb

#RUN sed -i 's|http://http.kali.org/kali|http://kali.mirror.garr.it/mirrors/kali|g' /etc/apt/sources.list
RUN apt-get update
RUN apt -y install --no-install-recommends ${KALI_PKG}
RUN apt-get full-upgrade -y
RUN apt-get purge -y vim vim-nox vim-tiny
RUN apt-get install -y openssh-server
RUN apt-get install -y xxd
RUN setcap -r /usr/lib/nmap/nmap
# Copy the adapted exploits including the flags or missing exploits
COPY adapted_exploits/openssl_heartbleed.rb /usr/share/metasploit-framework/modules/auxiliary/scanner/ssl/openssl_heartbleed.rb
COPY adapted_exploits/geoserver_unauth_rce_cve_2024_36401.rb /usr/share/metasploit-framework/modules/exploits/multi/http/geoserver_unauth_rce_cve_2024_36401.rb
COPY adapted_exploits/log4shell_scanner.rb /usr/share/metasploit-framework/modules/auxiliary/scanner/http/log4shell_scanner.rb
