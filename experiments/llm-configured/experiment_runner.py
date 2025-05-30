from llms import get_llm_model
from planners import get_planner_runner
from prompts import get_prompt_function
from utils.validity import is_valid_with_val
from pathlib import Path
import time

def run_experiment(domain_file, problem_file, planner, llm_name, prompt_style, skip_llm=False):
    domain_path = Path(domain_file).resolve()
    problem_path = Path(problem_file).resolve()

    if skip_llm:
        # 🟢 Domain bereits generiert, LLM überspringen
        planner_fn = get_planner_runner(planner)
        planner_result = planner_fn(domain_path, problem_path)

        return {
            "Domain": domain_path.name,
            "Problem": problem_path.name,
            "Planner": planner,
            "LLM_Model": llm_name,
            "Prompt_ID": prompt_style,
            **planner_result
        }

    # 🔁 Sonst: LLM generiert Domain (Einzelfall)
    with open(domain_path, "r") as f:
        original_domain = f.read()

    prompt_fn = get_prompt_function(prompt_style)
    prompt_string = prompt_fn(original_domain)

    llm = get_llm_model(llm_name)
    start_llm = time.time()
    generated_domain = llm.generate(prompt_string)
    end_llm = time.time()

    llm_api_time = round(end_llm - start_llm, 4)

    if not is_valid_with_val(generated_domain, problem_path):
        return {
            "Domain": domain_path.name,
            "Problem": problem_path.name,
            "Planner": planner,
            "LLM_Model": llm_name,
            "Prompt_ID": prompt_style,
            "LLM_API_Time_s": llm_api_time,
            "Status": "INVALID_DOMAIN"
        }

    # Temporäre Domain speichern
    tmp_path = domain_path.parent / f"tmp_domain_llm.pddl"
    with open(tmp_path, "w") as f:
        f.write(generated_domain)

    planner_fn = get_planner_runner(planner)
    planner_result = planner_fn(tmp_path, problem_path)
    tmp_path.unlink(missing_ok=True)

    return {
        "Domain": domain_path.name,
        "Problem": problem_path.name,
        "Planner": planner,
        "LLM_Model": llm_name,
        "Prompt_ID": prompt_style,
        "LLM_API_Time_s": llm_api_time,
        **planner_result
    }