import subprocess
import os
import pandas as pd

def run_mercury(domain_file, problem_file):
    benchmark_dir = os.path.abspath(os.path.dirname(domain_file))
    
    problem_rel = os.path.relpath(problem_file, benchmark_dir).replace("\\", "/")

    docker_cmd = [
        "docker", "run", "--rm",
        "--cpus=1.0",           
        "--memory=8g",      
        "--memory-swap=8g",            
        "--oom-kill-disable=false",            
        "-v", f"{benchmark_dir}:/pddl",
        "mercury_planner",
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

if __name__ == "__main__":


    domain = "benchmarks/hiking-sequential-agile/domain.pddl"
    problem = "benchmarks/hiking-sequential-agile/instances/instance-20.pddl"

    result = run_mercury(domain, problem)
    print("\nResult")
    print(result)