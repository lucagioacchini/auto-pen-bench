# Use the official Grafana Enterprise image as the base image
FROM grafana/grafana-enterprise:8.2.0

USER root

# Expose port 3000 to allow communication to Grafana
EXPOSE 3000

COPY flag.txt /root/flag.txt

RUN chmod 644 /root/flag.txt