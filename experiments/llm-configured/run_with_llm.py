from experiment_runner import run_experiment
from llms import get_llm_model
from prompts import get_prompt
from utils.validity import is_valid_with_val

from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd

load_dotenv()

# 🔧 Konfiguration
domain_file = Path("benchmarks/test/domain.pddl")
instances_dir = domain_file.parent / "instances"
planner = "lpg"
llm_name = "llama3"
prompt_style = "zero_shot_long"
llm_temperature = 0.2  
top_p = 1.0
max_tokens = None

# 📅 Zeitstempel
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# 📄 Ausgabedatei benennen
domain_name = domain_file.parent.name.lower().replace(" ", "_")
output_domain_name = f"domain_llm_{llm_name.replace('-', '')}_{prompt_style}_{timestamp}.pddl"
generated_domain_path = domain_file.parent / output_domain_name

# 🧠 Prompt + LLM
original_domain = domain_file.read_text()
prompt_fn = get_prompt(prompt_style)
prompt_string = prompt_fn(original_domain)

llm = get_llm_model(llm_name, temperature=llm_temperature, top_p=top_p, max_tokens=max_tokens)
llm_result = llm.generate(prompt_string)
generated_domain = llm_result["response"]

# 💾 Speichern
generated_domain_path.write_text(generated_domain)

# ✅ Validieren
sample_problem = next(instances_dir.glob("*.pddl"))
if not is_valid_with_val(generated_domain, str(sample_problem)):
    print("❌ INVALID_DOMAIN – Domain wurde trotzdem gespeichert.")
    exit(1)

# ▶️ Instanzen durchlaufen
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
        original_domain_str=original_domain,
        llm_api_time=llm_result["api_time"],
        llm_temperature=llm_temperature
    )
    results.append(result)

# 💾 CSV speichern
csv_filename = f"results/llm_{domain_name}_{planner}_{llm_name.replace('-', '')}_{prompt_style}_{timestamp}.csv"
pd.DataFrame(results).to_csv(csv_filename, index=False)
print(f"\n✅ Ergebnisse gespeichert unter: {csv_filename}")
