from llms import get_llm_model
from prompts import get_prompt
from utils.validity import is_valid_with_val
from utils.extraction import extract_pddl_from_response

from pathlib import Path
import csv

# === Konfiguration ===
domain_name = "transport-sequential-agile"
llm_name = "llama3"  # ← nur Mixtral braucht Workaround
temperature = 0.5
prompt_style = "cot"

# === Pfade und Dateien ===
domain_file = Path(f"benchmarks/{domain_name}/domain.pddl")
instances_dir = domain_file.parent / "instances"
problem_files = sorted([p for p in instances_dir.glob("*.pddl") if "plan" not in p.name])

original_domain = domain_file.read_text()
prompt_fn, prompt_format = get_prompt(prompt_style)
llm = get_llm_model(llm_name, temperature=temperature)

output_basename = f"{domain_name}__{llm_name}__{prompt_style}__{temperature}"
cot_txt_path = Path("test.txt")
analysis_txt_path = Path("test_analysis.txt")
csv_path = Path("test.csv")

# === Hilfsfunktion: Analyse extrahieren ===
def extract_analysis_from_cot_output(full_output: str) -> str:
    return full_output.split("(define", 1)[0].strip()

# === LLM-Aufruf ===
print(f"🚀 Starte Einzeltest: {output_basename}")
try:
    prompt_input = prompt_fn(original_domain)
    llm_result = llm.generate(prompt_input)
    llm_response = llm_result.get("response")
except Exception as e:
    print(f"❌ Fehler beim LLM-Aufruf: {e}")
    exit(1)

# === Speichere vollständige Antwort
cot_txt_path.write_text(llm_response)

# === Optional: Analyse extrahieren (Step 1)
analysis = extract_analysis_from_cot_output(llm_response)
analysis_txt_path.write_text(analysis)

# === Extrahiere PDDL
if llm_name == "mixtral":
    print("ℹ️ Mixtral-Modell erkannt – extrahiere PDDL aus Datei")
    full_output_from_file = cot_txt_path.read_text()
    generated_pddl = extract_pddl_from_response(full_output_from_file)
else:
    generated_pddl = extract_pddl_from_response(llm_response)

# === Validierung und CSV-Schreiben ===
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "domain", "problem", "LLM_Model", "Prompt_ID",
        "LLM_Temperature", "LLM_API_Time_s", "Valid_Domain"
    ])
    writer.writeheader()

    for problem_file in problem_files:
        print(f"🔍 Teste mit Problem: {problem_file.name}")
        is_valid = is_valid_with_val(generated_pddl, str(problem_file))

        writer.writerow({
            "domain": output_basename + ".pddl",
            "problem": problem_file.name,
            "LLM_Model": llm_name,
            "Prompt_ID": prompt_style,
            "LLM_Temperature": temperature,
            "LLM_API_Time_s": llm_result.get("api_time", None),
            "Valid_Domain": is_valid
        })

print("\n✅ Test abgeschlossen – Ergebnisse:")
print(f"- Voller Output: {cot_txt_path}")
print(f"- Analyse (Step 1): {analysis_txt_path}")
print(f"- Validierungsergebnisse: {csv_path}")
