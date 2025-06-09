from .lama_runner import run_lama
from .probe_runner import run_probe
from .mercury_runner import run_mercury
from .lpg_runner import run_lpg
from .lapkt_runner import run_lapkt
from .madagascar_runner import run_madagascar

def get_planner_runner(name: str):
    if name == "lama":
        return run_lama
    elif name == "probe":
        return run_probe
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