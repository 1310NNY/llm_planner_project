import os
import pandas as pd
from run_lapkt import run_lapkt

def run_all_lapkt():
    benchmark_root = "benchmarks"
    all_results = []

    for domain_folder in sorted(os.listdir(benchmark_root)):
        domain_path = os.path.join(benchmark_root, domain_folder)
        if not os.path.isdir(domain_path):
            continue

        domain_file = os.path.join(domain_path, "domain.pddl")
        instances_path = os.path.join(domain_path, "instances")

        if not os.path.isfile(domain_file):
            print(f"[WARN] Keine domain.pddl in {domain_path}")
            continue
        if not os.path.isdir(instances_path):
            print(f"[WARN] Kein 'instances/'-Ordner in {domain_path}")
            continue

        for file in sorted(os.listdir(instances_path)):
            if file.endswith(".pddl"):
                problem_file = os.path.join(instances_path, file)
                
                # Fortschrittsanzeige
                print(f"[INFO] Running planner on:")
                print(f"  Domain: {domain_folder}")
                print(f"  Problem: {file}")

                result = run_lapkt(domain_file, problem_file)
                result["Domain"] = domain_folder
                result["Problem"] = file
                result["Planner"] = "LAPKT"
                all_results.append(result)

    df = pd.DataFrame(all_results)
    os.makedirs("results", exist_ok=True)
    df.to_csv("results/lapkt_results.csv", index=False)
    print("\n[INFO] Results saved to results/lapkt_results.csv")

if __name__ == "__main__":
    run_all_lapkt()

