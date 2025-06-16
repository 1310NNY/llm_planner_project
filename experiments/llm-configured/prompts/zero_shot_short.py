def generate_prompt(domain_str: str) -> str:
    return f"""You are a PDDL domain expert.

Your task is to reorder the following PDDL domain file to improve AI planner efficiency (coverage, time, quality) via
reordering actions, preconditions, and effects. You may not change the semantics of the domain in any way.
Follow best practices from planning literature.

IMPORTANT:
- Do NOT rename, remove, or semantically change any predicates, parameters, or actions.
- Do NOT add comments, explanations, or formatting.
- Return ONLY a valid reordered PDDL domain file.

DOMAIN TO REORDER:
{domain_str}
"""
