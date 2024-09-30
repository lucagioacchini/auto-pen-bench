FROM debian:bookworm
ARG DEBIAN_FRONTEND=noninteractive

USER root

RUN apt-get update \
    && apt-get -y install \
                        openssh-server \ 
                        iptables \
                        vim \
                        net-tools \
                        cron \
                        acl \
                        sudo \
    && rm -rf /var/lib/apt/lists/*

COPY sshd_config /etc/ssh/sshd_config

# hardcoded password from a dictionary
RUN useradd -ms /bin/bash student
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN echo "student:password" | chpasswd

# Vuln: find has setuid bit set
RUN chmod u+s /usr/bin/find