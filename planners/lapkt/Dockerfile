FROM lapkt/lapkt-public

# Set workspace
WORKDIR /workspace

# Copy Exec in Container
COPY planners/lapkt/planner_exec /planner_exec
RUN chmod +x /planner_exec

ENTRYPOINT ["/planner_exec"]