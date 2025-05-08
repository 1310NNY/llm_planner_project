FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Systempakete installieren
RUN apt-get update && apt-get install -y \
    bison flex gawk g++-multilib pypy unzip wget tar make

# Arbeitsverzeichnis
WORKDIR /opt/mercury

# Mercury-ZIP laden und entpacken (AGL-Version)
RUN wget https://github.com/b-it-bots/mercury_planner/raw/master/files/Mercury-fixed.zip && \
    unzip Mercury-fixed.zip && \
    tar -xf seq-agl-mercury.tar.gz && \
    rm -rf Mercury-fixed.zip seq-*.tar.gz

# Kompilieren im richtigen Unterordner
WORKDIR /opt/mercury/seq-agl-mercury/src/search

# Patch: entferne -Werror, damit Warnungen nicht zum Fehler führen
RUN sed -i 's/-Werror//g' Makefile

RUN make

# Zurück ins Arbeitsverzeichnis
WORKDIR /workspace

