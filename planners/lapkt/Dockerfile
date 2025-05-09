FROM lapkt/lapkt-public

# Setze Arbeitsverzeichnis
WORKDIR /workspace

# Kopiere Exec-Skript in Container
COPY planners/lapkt/planner_exec /planner_exec
RUN chmod +x /planner_exec

ENTRYPOINT ["/planner_exec"]