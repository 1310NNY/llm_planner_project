def generate_prompt(domain_str: str) -> str:
    return f"""You are a PDDL domain expert.

Your task is to reorder the following PDDL domain file to improve AI planner efficiency (coverage, time, quality).

You may not change the semantics of the domain in any way. Only reorder elements as described below.

Rules to follow (based on Vallati et al., 2015):

1. Action ordering: Place actions earlier in the domain if they are semantically related to goals or likely to be used early in typical plans, based on their structure.
2. Precondition ordering: In `:precondition` blocks, list goal-relevant predicates first, supporting predicates after.
3. Effect ordering: In `:effect` blocks, place positive effects first, then deletions (e.g., `(not ...)`).
4. Predicate grouping in effects/preconditions: Keep logically related predicates (e.g., `(on ...)`, `(clear ...)`) close together.
5. Parameter consistency: Maintain consistent parameter ordering across all actions.
6. Macro positioning: If macro-actions are present, place them directly after the primitive actions they extend.
7. Predicate grouping in header: In the domain header, group static predicates (i.e., those that do not change during planning) together.

IMPORTANT:
- Do NOT rename, remove, or semantically alter any action, predicate, or parameter.
- Do NOT add comments, explanations, or formatting.
- Return ONLY a syntactically valid PDDL domain file that respects the structure of the original.

DOMAIN TO REORDER:
{domain_str}
"""