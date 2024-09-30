FROM debian:bookworm
ARG DEBIAN_FRONTEND=noninteractive

USER root

RUN apt-get update \
    && apt-get -y install \
                    curl \
                    wget \
                    openssh-server \ 
                    netcat-traditional \
                    tcpdump \
                    nmap \
                    vim \
                    iptables \
                    net-tools \
                    iproute2 \
                    dnsutils \
                    inetutils-ping \
                    sudo \
                    snmpd \
                    python3 \
                    python3-scapy \
                    build-essential socat \
    && rm -rf /var/lib/apt/lists/*    

COPY firewall.sh /etc/firewall.sh
RUN chmod u+x /etc/firewall.sh

COPY duster.sh /etc/duster.sh
RUN chmod u+x /etc/duster.sh