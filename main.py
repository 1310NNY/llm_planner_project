from llm.llm_handler import reorder_with_llm
from planner.planner_interface import run_planner
from config import DOMAIN_PATH, PROBLEM_PATH

def main():
    with open(DOMAIN_PATH, "r") as f:
        domain = f.read()

    reordered = reorder_with_llm(domain, heuristic="EFF1")

    with open("results/reordered-domain.pddl", "w") as f:
        f.write(reordered)

    plan = run_planner("results/reordered-domain.pddl", PROBLEM_PATH)
    print(plan)

if __name__ == "__main__":
    main()
