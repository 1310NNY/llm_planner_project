from experiment_runner import run_experiment
from llms import get_llm_model
from prompts import get_prompt
from utils.validity import is_valid_with_val
from utils.extraction import extract_pddl_from_response

from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
import csv

load_dotenv()

# 🔧 Konfiguration
domain_file = Path("benchmarks/transport-sequential-agile/domain.pddl")
instances_dir = domain_file.parent / "instances"
planner = "fd"
llm_name = "gpt-4o"
prompt_style = "cot"
llm_temperature = 0.2  
top_p = 1.0
max_tokens = None

# 📅 Zeitstempel
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# 📄 Output-Dateien benennen
domain_name = domain_file.parent.name.lower().replace(" ", "_")
output_domain_name = f"domain_llm_{llm_name.replace('-', '')}_{prompt_style}_{timestamp}.pddl"
generated_domain_path = domain_file.parent / output_domain_name

# 🧠 Prompt + LLM
original_domain = domain_file.read_text()
prompt_fn = get_prompt(prompt_style)
prompt_string = prompt_fn(original_domain)

llm = get_llm_model(llm_name, temperature=llm_temperature, top_p=top_p, max_tokens=max_tokens)
llm_result = llm.generate(prompt_string)

if not llm_result.get("response"):
    print("❌ Empty response from LLM")
    exit(1)

generated_domain = extract_pddl_from_response(llm_result["response"])
generated_domain_path.write_text(generated_domain)

# ✅ Validieren (einmalig vor Run)
sample_problem = next(instances_dir.glob("*.pddl"))
if not is_valid_with_val(generated_domain, str(sample_problem)):
    print("❌ INVALID_DOMAIN – Domain wurde trotzdem gespeichert.")
    exit(1)

# 📁 Ergebnisverzeichnis sicherstellen
results_dir = Path("results")
results_dir.mkdir(parents=True, exist_ok=True)

# 📄 CSV-Datei vorbereiten
csv_filename = results_dir / f"llm_{domain_name}_{planner}_{llm_name.replace('-', '')}_{prompt_style}_{timestamp}.csv"
csv_headers = [
    "domain", "problem", "planner","PlanCost","Runtime_internal_s","Runtime_wall_s", "Status",
    "LLM_Model", "Prompt_ID","LLM_API_Time_s", "LLM_Temperature", "Valid_Domain","PlanCost"
]

# 📄 Header schreiben
with open(csv_filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=csv_headers)
    writer.writeheader()

# ▶️ Instanzen durchlaufen und schreiben
for problem_file in sorted(instances_dir.glob("*.pddl")):
    if "plan" in problem_file.name:
        continue

    print(f"🧪 Running on: {problem_file.name}")

    result = run_experiment(
        domain_file=str(generated_domain_path),
        problem_file=str(problem_file),
        planner=planner,
        llm_name=llm_name,
        prompt_style=prompt_style,
        llm_api_time=llm_result["api_time"],
        llm_temperature=llm_temperature
    )

    with open(csv_filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=csv_headers)
        writer.writerow(result)

print(f"\n✅ Ergebnisse gespeichert unter: {csv_filename}")


