def generate_messages(domain_str: str) -> list:
    return [
        {
            "role": "system",
            "content": (
                "You are a PDDL domain expert."
            )
        },
        {
            "role": "user",
            "content": (
                "I will give you a PDDL domain. Your task is to reorder its elements to improve planner performance (coverage, time, and plan quality). "
                "IMPORTANT:\n"
                "- Do NOT rename, remove, or change the semantics of any domain elements.\n"
                "- Do NOT add comments, explanations, or extra formatting into the domain.\n"
            )
        },
        {
            "role": "user",
            "content": (
                "Follow these reordering rules, inspired by Vallati et al. (2020), to improve performance:\n\n"
                "1. Action ordering: Place actions earlier in the domain if they are likely to be used earlier in plans.\n"
                "   - Estimate this based on structural cues: actions with fewer preconditions, or those whose effects support other actions, should appear early in the domain.\n\n"
                "2. Precondition ordering: In `:precondition` blocks, place conditions that are structurally central or frequently reused earlier.\n"
                "   - Since goals are defined in problem files, estimate importance by predicate roles (e.g., spatial relations, resource states, transport links).\n\n"
                "3. **Effect ordering**: In `:effect` blocks, list add effects before delete effects (i.e., `(not ...)`).\n\n"
                "4. **Predicate grouping**: Group similar predicates together in preconditions and effects "
                "(e.g., those with the same name or referring to the same objects or resources).\n\n"
                "5. **Parameter consistency**: Use the same parameter ordering across all actions where possible.\n\n"
                "6. **Static predicate grouping**: In the `:predicates` section, place predicates that are never modified in any `:effect` block "
                "(i.e., static predicates) near the top.\n\n"
            )
        },
        {
            "role": "user",
            "content": (
                "Here is the domain you should work with:"
            )
        },
        {
            "role": "user",
            "content": domain_str
        },
        {
            "role": "user",
            "content": (
                "Step 1: Analyze the domain.\n"
                "Summarize your planned reordering strategy briefly."
            )
        },
        {
            "role": "assistant",
            "content": "Understood. I will now analyze the domain and describe how I plan to reorder it."
        },
        {
            "role": "user",
            "content": (
                "Step 2: Apply your strategy and output the fully reordered domain.\n"
                "- Only output valid PDDL code.\n"
                "- Begin with `(define` and end with the final parenthesis."
            )
        }
    ]
