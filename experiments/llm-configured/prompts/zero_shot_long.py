def generate_prompt(domain_str: str) -> str:
    return f"""You are a PDDL domain expert.

Your task is to reorder the following PDDL domain file to improve AI planner efficiency (coverage, time, quality).

You may not change the semantics of the domain in any way. Only reorder elements as described below.

Rules to follow (based on Vallati et al., 2020):

1. Action ordering: Place actions earlier in the domain if they are likely to be used earlier in plans.
   - Estimate this based on structural cues: actions with fewer preconditions, or those whose effects support other actions, may be used earlier.

2. Precondition ordering: Place more relevant conditions earlier in `:precondition` blocks.
   - Since goals are not visible in the domain file, treat commonly used predicates or those central to object manipulation (e.g., `(at ...)`, `(loaded ...)`, `(carrying ...)`) as likely goal-relevant.

3. Effect ordering: In `:effect` blocks, list add effects first, then delete effects (i.e., `(not ...)`).

4. Predicate grouping: In preconditions and effects, group similar predicates together (e.g., those with the same name or referring to the same objects or resources).

5. Parameter consistency: Use the same parameter order across all actions when possible.

6. Static predicate grouping: In the `:predicates` section, group predicates that are never changed in any `:effect` block (i.e., static predicates) near the top.

IMPORTANT:
- Do NOT rename, remove, or semantically change any predicates, parameters, or actions.
- Do NOT add comments, explanations, or formatting.
- Return ONLY a valid reordered PDDL domain file.

DOMAIN TO REORDER:
{domain_str}
"""