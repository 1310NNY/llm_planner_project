from .downward_runner import run_downward
from .mercury_runner import run_mercury
from .lpg_runner import run_lpg
from .lapkt_runner import run_lapkt
from .madagascar_runner import run_madagascar

def get_planner_runner(name: str):
    if name == "downward":
        return run_downward
    elif name == "mercury":
        return run_mercury
    elif name == "lpg":
        return run_lpg
    elif name == "lapkt":
        return run_lapkt
    elif name == "madagascar":
        return run_madagascar
    else:
        raise ValueError(f"Unknown planner: {name}")