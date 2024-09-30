FROM debian:bookworm
ARG DEBIAN_FRONTEND=noninteractive

USER root

RUN apt-get update \
    && apt-get -y install \
                    iptables \
                    snmpd \
    && rm -rf /var/lib/apt/lists/*

COPY firewall.sh /etc/firewall.sh
RUN chmod u+x /etc/firewall.sh

COPY snmpd.conf /etc/snmp/snmpd.conf
RUN chmod u+r /etc/snmp/snmpd.conf

EXPOSE 161