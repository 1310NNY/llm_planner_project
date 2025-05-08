FROM ubuntu:22.04

WORKDIR /opt/madagascar

# Systemtools
RUN apt-get update && apt-get install -y \
    build-essential

# TAR-Datei ins Image kopieren
COPY planners/madagascar/madagascar.tar .

# Entpacken (flacher Inhalt)
RUN tar -xf madagascar.tar && \
    chmod +x plan && \
    mv plan /usr/local/bin/madagascar && \
    rm madagascar.tar

# Arbeitsverzeichnis für PDDL
WORKDIR /workspace


