import subprocess

def run_planner(domain_path, problem_path):
    try:
        result = subprocess.run([
            "fast-downward",
            domain_path,
            problem_path,
            "--search",
            "lazy_greedy([ff()], preferred=[ff()])"
        ], capture_output=True, text=True, timeout=60)
        return result.stdout
    except Exception as e:
        return f"Planner error: {e}"
