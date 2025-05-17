FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive


RUN apt-get update && apt-get install -y \
    bison flex gawk g++-multilib pypy unzip wget tar make time python3

WORKDIR /opt/mercury

# Mercury-ZIP save und unfold 
RUN wget https://github.com/b-it-bots/mercury_planner/raw/master/files/Mercury-fixed.zip && \
    unzip Mercury-fixed.zip && \
    tar -xf seq-agl-mercury.tar.gz && \
    rm -rf Mercury-fixed.zip seq-*.tar.gz

# Preprocess 
WORKDIR /opt/mercury/seq-agl-mercury/src/preprocess
RUN make

# Search-Modul building (plan, plan-ipc)
WORKDIR /opt/mercury/seq-agl-mercury/src/search
RUN sed -i 's/-Werror//g' Makefile && \
    make

# back to Workspace 
WORKDIR /workspace

# planner_exec copy
COPY planners/mercury/planner_exec /planner_exec
RUN chmod +x /planner_exec

ENTRYPOINT ["/planner_exec"]

