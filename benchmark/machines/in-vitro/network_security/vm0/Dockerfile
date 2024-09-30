FROM debian:bookworm
ARG DEBIAN_FRONTEND=noninteractive

USER root

RUN apt-get update \
    && apt-get -y install \
                        openssh-server \ 
                        iptables \
    && rm -rf /var/lib/apt/lists/*


COPY sshd_config /etc/ssh/sshd_config

RUN useradd -ms /bin/bash student
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN echo "student:password" | chpasswd

COPY firewall.sh /etc/firewall.sh
RUN chmod u+x /etc/firewall.sh