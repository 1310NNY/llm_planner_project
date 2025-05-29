from pathlib import Path
from experiment_runner import run_experiment
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

domain_file = Path("benchmarks/citycar/domain.pddl")
instances_dir = domain_file.parent / "instances"

results = []
for problem_file in sorted(instances_dir.glob("*.pddl")):
    result = run_experiment(
        domain_file=str(domain_file),
        problem_file=str(problem_file),
        planner="downward",
        llm_name="gpt-4",
        prompt_style="few_shot"
    )
    results.append(result)

# Speichern
df = pd.DataFrame(results)
df.to_csv("results/llm_citycar_gpt4_fewshot.csv", index=False)
print("Ergebnisse gespeichert.")