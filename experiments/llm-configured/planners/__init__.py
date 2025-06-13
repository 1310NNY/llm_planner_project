from .bfs_f_runner import run_bfs_f
from .fd_runner import run_fd
from .mercury_runner import run_mercury
from .siw_runner import run_siw
from .madagascar_runner import run_madagascar

def get_planner_runner(name: str):
    if name == "bsf_f":
        return run_bfs_f
    elif name == "fd":
        return run_fd
    elif name == "mercury":
        return run_mercury
    elif name == "siw":
        return run_siw
    elif name == "madagascar":
        return run_madagascar
    else:
        raise ValueError(f"Unknown planner: {name}")