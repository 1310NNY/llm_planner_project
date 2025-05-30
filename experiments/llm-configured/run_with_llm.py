from experiment_runner import run_experiment
from llms import get_llm_model
from prompts import get_prompt_function
from utils.validity import is_valid_with_val

from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
import time

# 🔐 ENV laden
#load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

# 🔧 Konfiguration
domain_file = Path("benchmarks/blocks-strips-typed copy 2/domain.pddl")
instances_dir = domain_file.parent / "instances"
planner = "downward"
llm_name = "gpt-4"
prompt_style = "zero_shot"

# 📄 Namen für Output
domain_name = domain_file.parent.name.lower().replace(" ", "_")
output_domain_name = f"domain_llm_{llm_name.replace('-', '')}_{prompt_style}.pddl"
generated_domain_path = domain_file.parent / output_domain_name

# 🧠 Prompt & LLM – NUR EINMAL
with open(domain_file, "r") as f:
    original_domain = f.read()

prompt_fn = get_prompt_function(prompt_style)
prompt_string = prompt_fn(original_domain)

llm = get_llm_model(llm_name)
start_llm = time.time()
generated_domain = llm.generate(prompt_string)
end_llm = time.time()
llm_api_time = round(end_llm - start_llm, 4)

# 💾 Domain speichern
with open(generated_domain_path, "w") as f:
    f.write(generated_domain)

# ✅ Validieren gegen eine Beispielinstanz
sample_problem = next(instances_dir.glob("*.pddl"))
if not is_valid_with_val(generated_domain, sample_problem):
    print("❌ INVALID_DOMAIN – Domain wurde trotzdem gespeichert.")
    exit(1)

# ▶️ Alle Instanzen mit dieser Domain durchlaufen
results = []
for problem_file in sorted(instances_dir.glob("*.pddl")):
    if "plan" in problem_file.name:
        continue

    result = run_experiment(
        domain_file=str(generated_domain_path),
        problem_file=str(problem_file),
        planner=planner,
        llm_name=llm_name,
        prompt_style=prompt_style,
        skip_llm=True  # 💡 wichtig!
    )
    result["LLM_API_Time_s"] = llm_api_time
    results.append(result)

# 💾 Ergebnisse speichern
filename = f"results/llm_{domain_name}_{planner}_{llm_name.replace('-', '')}_{prompt_style}.csv"
pd.DataFrame(results).to_csv(filename, index=False)
print(f"\n✅ Ergebnisse gespeichert unter: {filename}")

