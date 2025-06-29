import subprocess
import os
import pandas as pd

def run_fd(domain_file, problem_file):
    benchmark_dir = os.path.abspath(os.path.dirname(domain_file))
    
    # Relative path to instance 
    problem_rel = os.path.relpath(problem_file, benchmark_dir).replace("\\", "/")

    docker_cmd = [
        "docker", "run", "--rm",
        "--cpus=1.0",           
        "--memory=8g",      
        "--memory-swap=8g",            
        "--oom-kill-disable=false",            
        "-v", f"{benchmark_dir}:/pddl",
        "fd_planner",
        "/pddl/" + os.path.basename(domain_file),
        "/pddl/" + problem_rel
    ]

    try:
        result = subprocess.run(
            docker_cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=300 
        )
        output = result.stdout
    except subprocess.TimeoutExpired:
        return {
            "PlanCost": None,
            "Runtime_wall_s": None,
            "Runtime_internal_s": None,
            "Status": "TIMEOUT"
        }
    except subprocess.CalledProcessError as e:
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

# for manual tests 
if __name__ == "__main__":
    
    domain = "benchmarks/blocks-strips-typed/domain.pddl"
    problem = "benchmarks/blocks-strips-typed/instances/instance-1.pddl"
    result = run_fd(domain, problem)
    print("\nResult:")
    print(result)

