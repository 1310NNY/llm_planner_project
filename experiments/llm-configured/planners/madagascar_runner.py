import subprocess
from pathlib import Path
import pandas as pd

def run_madagascar(domain_file, problem_file):
    domain_file = Path(domain_file)
    problem_file = Path(problem_file)

    benchmark_dir = domain_file.parent.resolve()
    problem_rel = problem_file.resolve().relative_to(benchmark_dir).as_posix()

    docker_cmd = [
        "docker", "run", "--rm",
        "--cpus=1.0",           
        "--memory=8g",          
        "-v", f"{benchmark_dir}:/pddl",
        "madagascar_planner",
        f"/pddl/{domain_file.name}",
        f"/pddl/{problem_rel}"
    ]

    try:
        result = subprocess.run(
            docker_cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=300  # wie IPC
        )
        output = result.stdout
    except subprocess.TimeoutExpired:
        return {
            "PlanCost": None,
            "Runtime_wall_s": None,
            "Runtime_internal_s": None,
            "Status": "TIMEOUT"
        }
    except subprocess.CalledProcessError:
        return {
            "PlanCost": None,
            "Runtime_wall_s": None,
            "Runtime_internal_s": None,
            "Status": "FAILURE"
        }

    metrics = {
        "PlanCost": None,
        "Runtime_wall_s": None,
        "Runtime_internal_s": None,
        "Status": "FAILURE"
    }

    for line in output.splitlines():
        if "[METRIC] PlanCost" in line:
            try:
                metrics["PlanCost"] = int(line.split(":")[1].strip())
            except ValueError:
                pass
        elif "[METRIC] Runtime_wall_s" in line:
            try:
                metrics["Runtime_wall_s"] = float(line.split(":")[1].strip())
            except ValueError:
                pass
        elif "[METRIC] Runtime_internal_s" in line:
            try:
                metrics["Runtime_internal_s"] = float(line.split(":")[1].strip())
            except ValueError:
                pass
        elif "[RESULT] STATUS: SUCCESS" in line:
            metrics["Status"] = "SUCCESS"

    return metrics

# Optional: Testlauf
if __name__ == "__main__":
    domain = Path("benchmarks/blocks-strips-typed/domain.pddl")
    problem = Path("benchmarks/blocks-strips-typed/instance-1.pddl")
    result = run_madagascar(domain, problem)
    print(result)