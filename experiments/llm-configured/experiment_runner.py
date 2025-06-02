import time
from pathlib import Path
from planners import get_planner_runner
from utils.validity import is_valid_with_val

def count_action_order_changes(original_str: str, modified_str: str) -> int:
    def extract_action_names(pddl_str):
        return [line.split()[1] for line in pddl_str.splitlines() if line.strip().startswith("(:action")]

    orig = extract_action_names(original_str)
    mod = extract_action_names(modified_str)

    # Zählen, wie viele Aktionen sich in der Reihenfolge verändert haben
    return sum(1 for o, m in zip(orig, mod) if o != m)

def run_experiment(domain_file, problem_file, planner, llm_name, prompt_style, original_domain_str=None, llm_api_time=None, llm_temperature=None):
    domain_path = Path(domain_file)
    problem_path = Path(problem_file)
    domain_str = domain_path.read_text()

    # 🟢 Validierung
    is_valid = is_valid_with_val(domain_str, str(problem_path))
    if not is_valid:
        return {
            "DomainFile": str(domain_path),
            "ProblemFile": str(problem_path),
            "Planner": planner,
            "LLM_Model": llm_name,
            "Prompt_ID": prompt_style,
            "LLM_API_Time_s": llm_api_time,
            "LLM_Temperature": llm_temperature,
            "Valid_Domain": False,
            "Num_Actions_Changed": None,
            "Domain_Diff_Chars": None,
            "Status": "INVALID_DOMAIN"
        }

    # 🧠 Planer ausführen
    planner_fn = get_planner_runner(planner)
    planner_result = planner_fn(str(domain_path), str(problem_path))

    # 🔍 Unterschiede berechnen
    num_actions_changed = None
    domain_diff_chars = None
    if original_domain_str:
        num_actions_changed = count_action_order_changes(original_domain_str, domain_str)
        domain_diff_chars = abs(len(domain_str) - len(original_domain_str))

    return {
        **planner_result,
        "DomainFile": str(domain_path),
        "ProblemFile": str(problem_path),
        "Planner": planner,
        "LLM_Model": llm_name,
        "Prompt_ID": prompt_style,
        "LLM_API_Time_s": llm_api_time,
        "LLM_Temperature": llm_temperature,
        "Valid_Domain": True,
        "Num_Actions_Changed": num_actions_changed,
        "Domain_Diff_Chars": domain_diff_chars
    }
