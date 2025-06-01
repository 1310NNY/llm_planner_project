import time
from pathlib import Path
from llms import get_llm_model
from prompts import get_prompt
from planners import get_planner_runner
from utils.validity import is_valid_with_val

def run_experiment(domain_file, problem_file, planner, llm_name, prompt_style, skip_llm=False):
    domain_path = Path(domain_file)
    problem_path = Path(problem_file)
    domain_str = domain_path.read_text()

    if skip_llm:
        # Domain wurde schon generiert & gespeichert
        llm_result = {
            "response": domain_str,
            "api_time": 0.0,
            "tokens_total": None,
            "prompt_length_chars": None,
            "completion_length_chars": None,
        }
        modified_domain_str = domain_str
        t_llm = 0.0
    else:
        # Prompt erzeugen & LLM aufrufen
        prompt_fn = get_prompt(prompt_style)
        prompt = prompt_fn(domain_str)
        llm = get_llm_model(llm_name)

        t0 = time.time()
        llm_result = llm.generate(prompt)
        t_llm = time.time() - t0
        modified_domain_str = llm_result["response"]

        # Neue Domain speichern (eigener Name optional hier)
        domain_path = domain_path.parent / f"domain_llm_{llm_name.replace('-', '')}_{prompt_style}.pddl"
        domain_path.write_text(modified_domain_str)

    # ✅ Validierung
    is_valid = is_valid_with_val(modified_domain_str, str(problem_path))
    if not is_valid:
        return {
            "DomainFile": str(domain_path),
            "ProblemFile": str(problem_path),
            "Planner": planner,
            "LLM_Model": llm_name,
            "Prompt_ID": prompt_style,
            "LLM_API_Time_s": llm_result["api_time"],
            "LLM_API_Time_with_Preproccess_s": t_llm,
            "Tokens_Total": llm_result["tokens_total"],
            "Prompt_Length_Chars": llm_result["prompt_length_chars"],
            "Completion_Length_Chars": llm_result["completion_length_chars"],
            "Status": "INVALID_DOMAIN"
        }

    # 🧠 Planer aufrufen
    planner_fn = get_planner_runner(planner)
    planner_result = planner_fn(str(domain_path), str(problem_path))

    return {
        **planner_result,
        "DomainFile": str(domain_path),
        "ProblemFile": str(problem_path),
        "Planner": planner,
        "LLM_Model": llm_name,
        "Prompt_ID": prompt_style,
        "LLM_API_Time_s": llm_result["api_time"],
        "LLM_API_Time_with_Preproccess_s": t_llm,
        "Tokens_Total": llm_result["tokens_total"],
        "Prompt_Length_Chars": llm_result["prompt_length_chars"],
        "Completion_Length_Chars": llm_result["completion_length_chars"],
    }