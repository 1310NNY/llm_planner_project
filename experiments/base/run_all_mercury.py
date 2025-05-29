from pathlib import Path
import pandas as pd
from run_mercury import run_mercury

def run_all_mercury():
    project_root = Path(__file__).resolve().parents[2]
    benchmark_root = project_root / "benchmarks"
    all_results = []

    for domain_folder in sorted(benchmark_root.iterdir()):
        if not domain_folder.is_dir():
            continue

        domain_file = domain_folder / "domain.pddl"
        instances_path = domain_folder / "instances"

        if not domain_file.is_file():
            print(f"[WARN] No domain.pddl in {domain_folder}")
            continue

        if not instances_path.is_dir():
            print(f"[WARN] No 'instances/'-folder in {domain_folder}")
            continue

        for file in sorted(instances_path.iterdir()):
            if file.suffix == ".pddl":
                problem_file = file
                result = run_mercury(str(domain_file), str(problem_file))
                
                if result is not None:
                    result["domain"] = domain_folder.name
                    result["problem"] = file.name
                    result["planner"] = "mercury"
                    all_results.append(result)

    out_dir = project_root / "results" / "base"
    out_dir.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(all_results)
    df.to_csv(out_dir / "mercury_results.csv", index=False)
    print("✅ Ergebnisse gespeichert unter:", out_dir / "mercury_results.csv")

if __name__ == "__main__":
    run_all_mercury()


