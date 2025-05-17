FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# install dependencies
RUN apt-get update && apt-get install -y \
    build-essential wget unzip tar make python3

WORKDIR /opt/lpg

# Copy local file into image 
COPY planners/lpg/lpgtd-1_4-linux.tar .

# unfold and make ready
RUN tar -xf lpgtd-1_4-linux.tar && \
    mv LPG-td-1.4 lpg-td && \
    chmod +x lpg-td/lpg-td && \
    rm lpgtd-1_4-linux.tar

# workdir for Input (PDDL)
WORKDIR /workspace

# planner_exec into image 
COPY planners/lpg/planner_exec /planner_exec
RUN chmod +x /planner_exec


ENTRYPOINT ["/planner_exec"]

