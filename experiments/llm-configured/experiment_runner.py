from pathlib import Path
import tempfile
from llms import get_llm_model
from prompts import get_prompt_function
from planners import get_planner_runner
from utils.validity import is_valid_pddl
import time

def run_experiment(domain_file, problem_file, planner, llm_name, prompt_style):
    # 1. Domain laden
    domain_str = Path(domain_file).read_text()

    # 2. Prompt erzeugen
    prompt_fn = get_prompt_function(prompt_style)
    prompt = prompt_fn(domain_str)

    # 3. LLM wählen und Domain generieren
    llm = get_llm_model(llm_name)
    llm_start = time.time()
    try:
        domain_modified = llm.generate(prompt)
    except Exception as e:
        return {
            "status": "llm_failed",
            "error": str(e),
            "planner": planner,
            "llm": llm_name,
            "prompt": prompt_style,
            "llm_duration": time.time() - llm_start
        }

    # 4. Validitätsprüfung
    is_valid = is_valid_pddl(domain_modified, problem_file)
    llm_end = time.time()

    if not is_valid:
        return {
            "status": "invalid_pddl",
            "planner": planner,
            "llm": llm_name,
            "prompt": prompt_style,
            "llm_duration": llm_end - llm_start
        }

    # 5. Domain temporär speichern
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".pddl") as tmp:
        tmp.write(domain_modified)
        tmp.flush()
        tmp_path = tmp.name

    # 6. Planner-Funktion holen und ausführen
    planner_fn = get_planner_runner(planner)
    result = planner_fn(tmp_path, problem_file)

    # 7. Ergebnis erweitern
    result.update({
        "planner": planner,
        "llm": llm_name,
        "prompt": prompt_style,
        "domain_file": str(domain_file),
        "problem_file": str(problem_file),
        "llm_duration": llm_end - llm_start
    })

    return result