from pathlib import Path
import pandas as pd
from run_mercury import run_mercury

def run_all_mercury():
    project_root = Path(__file__).resolve().parents[2]
    benchmark_root = project_root / "benchmarks"
    result_file = project_root / "results" / "base" / "mercury_results.csv"

    # Spalten-Layout definieren
    cols = ["domain", "problem", "planner", "PlanCost", "Runtime_internal_s", "Runtime_wall_s", "Status"]

    # Ergebnisverzeichnis vorbereiten
    result_file.parent.mkdir(parents=True, exist_ok=True)

    # Vorhandene Ergebnisse laden (falls vorhanden)
    if result_file.exists():
        existing_df = pd.read_csv(result_file)
    else:
        existing_df = pd.DataFrame(columns=cols)
        existing_df.to_csv(result_file, index=False)

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
            if file.suffix != ".pddl":
                continue

            domain_name = domain_folder.name
            problem_name = file.name
            planner_name = "mercury"

            # ❌ Check: schon vorhanden?
            is_duplicate = (
                (existing_df["domain"] == domain_name) &
                (existing_df["problem"] == problem_name) &
                (existing_df["planner"] == planner_name)
            ).any()

            if is_duplicate:
                print(f"⏭️  Überspringe bereits vorhandene Instanz: {domain_name} | {problem_name}")
                continue

            # ✅ Ausführen und Ergebnis loggen
            print(f"🔍 Running mercury on domain '{domain_name}', problem '{problem_name}'")
            result = run_mercury(str(domain_file), str(file))

            if result is not None:
                row = {
                    "domain": domain_name,
                    "problem": problem_name,
                    "planner": planner_name,
                    "PlanCost": result.get("PlanCost"),
                    "Runtime_internal_s": result.get("Runtime_internal_s"),
                    "Runtime_wall_s": result.get("Runtime_wall_s"),
                    "Status": result.get("Status")
                }
                pd.DataFrame([row])[cols].to_csv(result_file, mode='a', header=False, index=False)

    print("✅ Alle neuen Ergebnisse gespeichert unter:", result_file)

if __name__ == "__main__":
    run_all_mercury()




