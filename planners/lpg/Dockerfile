FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Systempakete installieren
RUN apt-get update && apt-get install -y \
    build-essential wget unzip tar make

# Arbeitsverzeichnis für die Installation
WORKDIR /opt/lpg

# Lokale Datei ins Image kopieren
COPY planners/lpg/lpgtd-1_4-linux.tar .

# Entpacken & vorbereiten
RUN tar -xf lpgtd-1_4-linux.tar && \
    mv LPG-td-1.4 lpg-td && \
    chmod +x lpg-td/lpg-td && \
    rm lpgtd-1_4-linux.tar

# Arbeitsverzeichnis für Input-Dateien (PDDL)
WORKDIR /workspace

# planner_exec-Skript ins Image kopieren
COPY planners/lpg/planner_exec /planner_exec
RUN chmod +x /planner_exec

# Standard-Einstiegspunkt setzen
ENTRYPOINT ["/planner_exec"]

