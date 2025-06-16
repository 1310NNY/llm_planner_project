from llms import get_llm_model
from prompts import get_prompt
from utils.validity import is_valid_with_val
from utils.extraction import extract_pddl_from_response

from pathlib import Path
from dotenv import load_dotenv
import csv
import os
import pandas as pd

load_dotenv()

# === Konfiguration ===
domains = [
     "visit-all-sequential-agile",
     "transport-sequential-agile",
     "genome-edit-distances-sequential-agile",
     "barman-sequential-agile",
    "thoughtful-sequential-agile"
]

temperatures = [0.0 , 0.2, 0.5, 0.7]

llms = [
     "gemini",
     "claude",
     "deepseek",
     "llama3",
     "mixtral",
     "gpt-4o",
     "o4-mini",
]

prompts = [
     "zero_shot_short",
     "zero_shot_long",
     "few_shot_short",
     "few_shot_long",
    "cot"
]

results_dir = Path("results")
results_dir.mkdir(parents=True, exist_ok=True)
csv_path = results_dir / "llm_domain_rewrites.csv"
csv_headers = [
    "domain", "problem", "LLM_Model",
    "Prompt_ID", "LLM_Temperature", "LLM_API_Time_s", "Valid_Domain"
]

# Bestehende Ergebnisse laden
if csv_path.exists():
    existing_df = pd.read_csv(csv_path)
else:
    existing_df = pd.DataFrame(columns=csv_headers)

# === Hauptschleife ===
with open(csv_path, "a", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=csv_headers)

    if f.tell() == 0:
        writer.writeheader()

    for domain in domains:
        domain_file = Path(f"benchmarks/{domain}/domain.pddl")
        original_domain = domain_file.read_text()
        instances_dir = domain_file.parent / "instances"
        problem_files = sorted([p for p in instances_dir.glob("*.pddl") if "plan" not in p.name])

        for prompt_style in prompts:
            prompt_fn, prompt_format = get_prompt(prompt_style)

            for llm_name in llms:
                for temperature in temperatures:
                    output_name = f"{domain}__{llm_name.replace('-', '').replace('/', '')}__{prompt_style.replace(' ', '_')}__{temperature}.pddl"
                    generated_domain_path = domain_file.parent / output_name
                    cot_txt_path = generated_domain_path.with_suffix(".txt")

                    # Prüfen, ob diese Konfiguration bereits vollständig vorhanden ist
                    already_done = all(
                        (existing_df[
                            (existing_df["domain"] == output_name) &
                            (existing_df["problem"] == pf.name) &
                            (existing_df["LLM_Model"] == llm_name) &
                            (existing_df["Prompt_ID"] == prompt_style) &
                            (existing_df["LLM_Temperature"] == temperature)
                        ].shape[0] > 0)
                        for pf in problem_files
                    )
                    if already_done:
                        print(f"⏩ Überspringe bereits vorhandene Kombination: {output_name}")
                        continue

                    print(f"\n🚀 Generiere: {domain} | {prompt_style} | {llm_name} | T={temperature}")
                    llm = get_llm_model(llm_name, temperature=temperature, top_p=1.0, max_tokens=None)

                    try:
                        prompt_input = prompt_fn(original_domain)
                        llm_result = llm.generate(prompt_input)
                        llm_response = llm_result.get("response")

                        # 📝 Speichere CoT-Output in .txt
                        if prompt_format == "cot":
                            cot_txt_path.write_text(llm_response)

                        # 🔁 Nur Mixtral: .txt wieder einlesen
                        if llm_name == "mixtral" and prompt_format == "cot":
                            print("ℹ️ Mixtral mit CoT erkannt – extrahiere PDDL aus .txt-Datei")
                            llm_response = cot_txt_path.read_text()

                    except Exception as e:
                        error_msg = str(e).lower()
                        if "500" in error_msg or "internal server error" in error_msg:
                            print(f"⚠️ Mixtral-Fehler (500): {e} – überspringe Kombination.")
                            continue
                        else:
                            print(f"❌ LLM-Fehler: {e}")
                            llm_response = None

                    if not llm_response:
                        print("⚠️ Fehlerhafte oder leere Antwort – markiere alle Instanzen als ungültig.")
                        for problem_file in problem_files:
                            writer.writerow({
                                "domain": output_name,
                                "problem": problem_file.name,
                                "LLM_Model": llm_name,
                                "Prompt_ID": prompt_style,
                                "LLM_Temperature": temperature,
                                "LLM_API_Time_s": None,
                                "Valid_Domain": False
                            })
                        continue

                    # 📦 Domain extrahieren und speichern
                    generated_domain = extract_pddl_from_response(llm_response)
                    generated_domain_path.write_text(generated_domain)

                    for problem_file in problem_files:
                        print(f"🔍 Validierung mit Problem: {problem_file.name}")
                        is_valid = is_valid_with_val(generated_domain, str(problem_file))

                        writer.writerow({
                            "domain": output_name,
                            "problem": problem_file.name,
                            "LLM_Model": llm_name,
                            "Prompt_ID": prompt_style,
                            "LLM_Temperature": temperature,
                            "LLM_API_Time_s": llm_result.get("api_time", None),
                            "Valid_Domain": is_valid
                        })

print("\n✅ Alle Ergebnisse gespeichert.")

