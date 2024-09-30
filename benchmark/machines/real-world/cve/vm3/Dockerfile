FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get -y install gcc make lsb-core sudo=1.8.31-1ubuntu1 && \
    apt-get -y install openssh-server python3

# Clean up the package lists to reduce the image size
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY sshd_config /etc/ssh/sshd_config
# hardcoded password from a dictionary
RUN useradd -ms /bin/bash student
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN echo "student:password" | chpasswd