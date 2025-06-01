def generate_messages(domain_str: str) -> list:
    return [
        {
            "role": "system",
            "content": (
                "You are a PDDL expert assisting with domain file optimization. "
                "Your goal is to reorder domain actions to improve heuristic planner performance, "
                "following best practices from Vallati et al. (2015)."
            )
        },
        {
            "role": "user",
            "content": (
                "Let’s first reason about how we might reorder this domain based on heuristic search performance. "
                "Think step by step about action ordering, preconditions, and effects."
            )
        },
        {
            "role": "assistant",
            "content": (
                "Understood. Please provide the domain file to analyze."
            )
        },
        {
            "role": "user",
            "content": domain_str
        },
        {
            "role": "user",
            "content": (
                "Now output the fully reordered domain file. IMPORTANT: "
                "Return only the valid PDDL code beginning with (define and ending with the final parenthesis. "
                "Do not include any explanation, commentary, or formatting. Only the clean PDDL domain."
            )
        }
    ]
