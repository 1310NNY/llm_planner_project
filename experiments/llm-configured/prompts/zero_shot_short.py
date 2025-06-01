def generate_prompt(domain_str: str) -> str:
    return f"""Reorder this PDDL domain to improve planner efficiency by reordering actions, preconditions, and effects — without changing the meaning.

Do not rename or delete anything. Only change order to follow best practices in planning literature.

Return only the reordered PDDL starting with (define ...):\n\n{domain_str}"""
