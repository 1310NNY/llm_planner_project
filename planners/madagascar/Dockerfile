FROM ubuntu:22.04

WORKDIR /opt/madagascar

RUN apt-get update && apt-get install -y \
    build-essential python3

# copy mp binary
COPY planners/madagascar/Mp /usr/local/bin/madagascar
RUN chmod +x /usr/local/bin/madagascar

WORKDIR /workspace

COPY planners/madagascar/planner_exec /planner_exec
RUN chmod +x /planner_exec

ENTRYPOINT ["/planner_exec"]



