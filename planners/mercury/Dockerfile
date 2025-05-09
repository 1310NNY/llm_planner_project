FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Systempakete installieren

RUN apt-get update && apt-get install -y \
    bison flex gawk g++-multilib pypy unzip wget tar make time

# Arbeitsverzeichnis für Installation
WORKDIR /opt/mercury

# Mercury-ZIP laden und entpacken (AGL-Version)
RUN wget https://github.com/b-it-bots/mercury_planner/raw/master/files/Mercury-fixed.zip && \
    unzip Mercury-fixed.zip && \
    tar -xf seq-agl-mercury.tar.gz && \
    rm -rf Mercury-fixed.zip seq-*.tar.gz

# Preprocess bauen
WORKDIR /opt/mercury/seq-agl-mercury/src/preprocess
RUN make

# Search-Modul bauen (enthält plan, plan-ipc)
WORKDIR /opt/mercury/seq-agl-mercury/src/search
RUN sed -i 's/-Werror//g' Makefile && \
    make

# Zurück ins Workspace-Verzeichnis (für Input)
WORKDIR /workspace

# planner_exec-Skript kopieren und ausführbar machen
COPY planners/mercury/planner_exec /planner_exec
RUN chmod +x /planner_exec

ENTRYPOINT ["/planner_exec"]

