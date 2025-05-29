def generate_prompt(domain_str: str) -> str:
    return f"""Here is a PDDL domain file:

{domain_str}

Please reorder this domain file to make it more heuristic-friendly for modern planners such as Fast Downward, following the insights from Vallati et al. (2015) on domain model configuration.

IMPORTANT:
- Do **not** change the semantics of any action.
- Do **not** rename, remove, or logically alter anything.
- Only adjust the **order** of elements.

Follow these reordering rules:

1. Actions that are typically used earlier or more frequently should appear higher in the domain.
2. In `:precondition` blocks: Place goal-relevant predicates first, supporting ones after.
3. In `:effect` blocks: List positive effects first, then deletion effects (e.g., `(not ...)`).
4. Keep logically related predicates (e.g., `(on ...)`, `(clear ...)`) close together.
5. Maintain consistent parameter order across actions.
6. Do not remove any content – this is purely a structural reordering.

Return only the updated, syntactically valid PDDL domain file – **no explanation, no comments, no extra text**. The output must begin with `(define` and end with the last closing parenthesis."""