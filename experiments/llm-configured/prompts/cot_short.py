def generate_messages(domain_str: str) -> list:
    return [
        {
            "role": "system",
            "content": (
                "You are a PDDL expert assisting with domain file optimization. "
                "Your task is to reorder elements in the domain file to improve AI planner efficiency, "
                "based on principles from Vallati et al. (2015). Do not change semantics."
            )
        },
        {
            "role": "user",
            "content": (
                "Let’s reason step by step about how to reorder this domain for better heuristic planning. "
                "Consider:\n"
                "- Which actions are likely used early and should appear earlier?\n"
                "- Are preconditions goal-relevant first, then support ones?\n"
                "- Are positive effects before deletions?\n"
                "- Are predicate groups (like (on ...), (clear ...)) kept together?\n"
                "- Is parameter order consistent across actions?\n"
                "- Are static predicates grouped near the top?\n"
                "Proceed with analysis."
            )
        },
        {
            "role": "assistant",
            "content": "Understood. Please provide the domain file to analyze."
        },
        {
            "role": "user",
            "content": domain_str
        },
        {
            "role": "user",
            "content": (
                "Now output the fully reordered domain file. IMPORTANT:\n"
                "- Do not rename, remove, or alter semantics.\n"
                "- Do not include comments, explanations, or markdown formatting.\n"
                "- Return only the clean PDDL code starting with (define and ending with the last parenthesis."
            )
        }
    ]
