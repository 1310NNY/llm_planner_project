FROM lapkt/lapkt-public

# Arbeitsverzeichnis setzen
WORKDIR /workspace

# planner_exec-Skript kopieren und ausführbar machen
COPY planners/siw/planner_exec /planner_exec
RUN chmod +x /planner_exec

ENTRYPOINT ["/planner_exec"]
