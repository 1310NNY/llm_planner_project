def generate_prompt(domain_str: str) -> str:
    return f"""You are a PDDL domain expert.

Your task is to reorder the following PDDL domain file to improve AI planner efficiency (coverage, time, quality).

You may not change the semantics of the domain in any way. Only reorder elements as described below.

Rules to follow (based on Vallati et al., 2015):

1. Action ordering: Place actions earlier in the domain if they are semantically related to goals or likely to be used early in typical plans, based on their structure.
2. Precondition ordering: In :precondition blocks, list goal-relevant predicates first, supporting predicates after.
3. Effect ordering: In :effect blocks, place positive effects first, then deletions (e.g., (not ...)).
4. Predicate grouping: Keep logically related predicates (e.g., (on ...), (clear ...)) close together within :precondition and :effect blocks.
5. Parameter consistency: Maintain consistent parameter ordering across all actions.
6. Static predicate grouping: In the domain header, group static predicates (i.e., those that do not change during planning) together near the top.

IMPORTANT:
- Do NOT rename, remove, or semantically alter any action, predicate, or parameter.
- Do NOT add comments, explanations, or formatting.
- Return ONLY a syntactically valid PDDL domain file that respects the structure of the original.

---

Example (excerpt from IPC8 TETRIS domain):

ORIGINAL:
(:action move_square
  :parameters (?xy_initial - position ?xy_final - position ?element - one_square)
  :precondition (and 
    (clear ?xy_final) 
    (at_square ?element ?xy_initial) 
    (connected ?xy_initial ?xy_final)
    (connected ?xy_final ?xy_initial)  
  )
  :effect (and  
    (clear ?xy_initial)
    (at_square ?element ?xy_final)
    (not (clear ?xy_final))
    (not (at_square ?element ?xy_initial))
    (increase (total-cost) 1)
  )
)

REORDERED:
(:action move_square
  :parameters (?xy_initial - position ?xy_final - position ?element - one_square)
  :precondition (and 
    (at_square ?element ?xy_initial)
    (clear ?xy_final)
    (connected ?xy_initial ?xy_final)
    (connected ?xy_final ?xy_initial)
  )
  :effect (and  
    (at_square ?element ?xy_final)
    (clear ?xy_initial)
    (not (at_square ?element ?xy_initial))
    (not (clear ?xy_final))
    (increase (total-cost) 1)
  )
)

---

DOMAIN TO REORDER:
{domain_str}
"""

