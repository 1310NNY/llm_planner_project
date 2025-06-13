from pathlib import Path
from planners import get_planner_runner
from utils.validity import is_valid_with_val


def run_experiment(
    domain_file,
    problem_file,
    planner,
    llm_name,
    prompt_style,
    llm_api_time=None,
    llm_temperature=None
):
    domain_path = Path(domain_file)
    problem_path = Path(problem_file)
    domain_str = domain_path.read_text()

    # ✅ Gültigkeit prüfen
    is_valid = is_valid_with_val(domain_str, str(problem_path))
    if not is_valid:
        return {
            "domain": str(domain_path),
            "problem": str(problem_path),
            "planner": planner,
            "LLM_Model": llm_name,
            "Prompt_ID": prompt_style,
            "LLM_API_Time_s": llm_api_time,
            "LLM_Temperature": llm_temperature,
            "Valid_Domain": False,
            "Status": "INVALID_DOMAIN"
        }

    # ▶️ Planer ausführen
    planner_fn = get_planner_runner(planner)
    planner_result = planner_fn(str(domain_path), str(problem_path))

    return {
        "domain": str(domain_path),
        "problem": str(problem_path),
        "planner": planner,
        **planner_result,
        "LLM_Model": llm_name,
        "Prompt_ID": prompt_style,
        "LLM_API_Time_s": llm_api_time,
        "LLM_Temperature": llm_temperature,
        "Valid_Domain": True    
    }
