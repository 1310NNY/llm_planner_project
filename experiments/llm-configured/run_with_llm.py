from experiment_runner import run_experiment
from dotenv import load_dotenv
load_dotenv()

result = run_experiment(
    domain_file="benchmarks/citycar/domain.pddl",
    problem_file="benchmarks/citycar/instances/p01.pddl",
    planner="downward",
    llm_name="gpt-4",
    prompt_style="few_shot"
)

print(result)