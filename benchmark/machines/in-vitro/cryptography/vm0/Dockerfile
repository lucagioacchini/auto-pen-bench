FROM debian:bookworm
ARG DEBIAN_FRONTEND=noninteractive

USER root

# Install necessary packages
RUN apt-get update \
    && apt-get -y install \
                        python3 \
                        python3-pip \
                        python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment, then install dependencies
RUN python3 -m venv /opt/venv
RUN /opt/venv/bin/pip install pycryptodome flask

# Copy the server script
COPY server.py /root/server.py
COPY source.py /root/source.py
COPY flag /root/key.txt

# Expose port 8080 for the server
EXPOSE 8080

# Start SSH and the server
CMD /opt/venv/bin/python /root/server.py