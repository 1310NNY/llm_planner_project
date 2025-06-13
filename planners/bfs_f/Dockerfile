FROM lapkt/lapkt-public

WORKDIR /workspace

COPY planners/bfs_f/planner_exec /planner_exec
RUN chmod +x /planner_exec

ENTRYPOINT ["/planner_exec"]




