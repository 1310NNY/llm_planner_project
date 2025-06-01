def generate_messages(domain_str: str) -> list:
    return [
        {
            "role": "system",
            "content": (
                "You are a domain modeling expert specializing in automated planning (PDDL) "
                "and heuristic-aware configuration based on principles from Vallati et al. (2015)."
            )
        },
        {
            "role": "user",
            "content": (
                "Let's reorder a PDDL domain to make it more efficient for heuristic-based planners. "
                "These include planners that use heuristics such as relaxed plan (hFF), landmark-cut (LM-Cut), or similar methods. "
                "We will proceed step by step."
            )
        },
        {
            "role": "assistant",
            "content": "Sure, please provide the domain file to analyze."
        },
        {
            "role": "user",
            "content": domain_str
        },
        {
            "role": "user",
            "content": (
                "Now, based on the following reordering principles from Vallati et al. (2015), "
                "restructure the domain:\n\n"

                "1. Place actions likely to be useful early in plans closer to the top.\n"
                "2. In `:precondition` blocks: put goal-relevant predicates first, supporting ones later.\n"
                "3. In `:effect` blocks: list positive effects first, then deletions (e.g., `(not ...)`).\n"
                "4. Group logically related predicates (e.g., `(on ...)`, `(clear ...)`) close together.\n"
                "5. Maintain consistent parameter ordering across actions.\n\n"

                "**IMPORTANT RULES:**\n"
                "- Do **not** change the semantics of any action.\n"
                "- Do **not** rename, remove, or logically alter anything.\n"
                "- Only adjust the **order** of actions, preconditions, and effects.\n\n"

                "Return only the reordered, syntactically valid PDDL domain file.\n"
                "The output must begin with `(define` and end with the final closing parenthesis.\n"
                "**No explanation, no commentary, no markdown, no code blocks.**"
            )
        }
    ]