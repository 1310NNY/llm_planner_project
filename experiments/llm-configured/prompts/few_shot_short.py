def generate_prompt(domain_str: str) -> str:
    return f"""You are a PDDL domain expert.

Your task is to reorder the following PDDL domain file to improve AI planner efficiency (coverage, time, quality).

You may not change the semantics of the domain in any way. Only reorder elements as described below.

Rules to follow (based on Vallati et al., 2020):

1. Action ordering: Place actions earlier in the domain if they are likely to be used early in plans.
   - Estimate this based on structure only: actions with few preconditions, or effects that serve as preconditions for other actions, should appear early in the domain.

2. Precondition ordering: In `:precondition` blocks, place conditions that are structurally central or frequently reused earlier.
   - Since goals are defined in problem files, estimate importance by predicate roles (e.g., spatial relations, resource states, transport links).

3. Effect ordering: In `:effect` blocks, list add effects first, then delete effects (i.e., `(not ...)`).

4. Predicate grouping: Group similar predicates (e.g., `(on ...)`, `(clear ...)`) together in preconditions and effects. Similarity can be based on name, shared roles, or frequent co-occurrence.

5. Parameter consistency: Use consistent parameter ordering across all actions where applicable.

6. Static predicate grouping: In the `:predicates` section, group predicates that never appear in any `:effect` (i.e., static predicates) near the top.

IMPORTANT:
- Do NOT rename, remove, or semantically change any predicates, parameters, or actions.
- Do NOT add comments, explanations, or formatting.
- Return ONLY a valid reordered PDDL domain file.

---

Example (excerpt from IPC 2014 ELEVATORS domain):

Original (suboptimally structured):
(:action move-elevator
  :parameters (?e - elevator ?from - floor ?to - floor)
  :precondition (and
    (elevator-at ?e ?from)
    (enabled ?e)
    (connected ?from ?to)
    (elevator ?e)
  )
  :effect (and
    (not (elevator-at ?e ?from))
    (elevator-at ?e ?to)
    (increase (total-cost) 1)
  )
)

Reordered (heuristically improved):
(:action move-elevator
  :parameters (?e - elevator ?from - floor ?to - floor)
  :precondition (and
    (elevator ?e)
    (elevator-at ?e ?from)
    (enabled ?e)
    (connected ?from ?to)
  )
  :effect (and
    (elevator-at ?e ?to)
    (not (elevator-at ?e ?from))
    (increase (total-cost) 1)
  )
)

Explanation of applied rules in the example above:

- Rule 1 (Action ordering): `move-elevator` is placed early in the domain file because it is a fundamental mobility primitive used by many later actions like `pickup` or `drop`. Its effects (changing elevator position) are preconditions for those actions.
- Rule 2 (Precondition ordering): `(elevator ?e)` is a static type predicate and placed first, followed by `(elevator-at ?e ?from)` which is critical for movement.
- Rule 3 (Effect ordering): Add effect `(elevator-at ?e ?to)` appears before the delete effect `(not (elevator-at ?e ?from))`, improving relaxed-plan heuristic evaluation.
- Rule 4 (Predicate grouping): Both `(elevator-at ...)` predicates are placed adjacently in preconditions and effects to group related state transitions.
- Rule 5 (Parameter consistency): The parameters `?e`, `?from`, `?to` are consistently ordered across all predicates, ensuring symbolic uniformity.
- Rule 6 (Static predicate grouping – implied): `(elevator ?e)` is a static predicate that never appears in effects. Its placement at the top of the precondition block mirrors a grouped structure in the `:predicates` section, where static predicates are clustered near the top.

---

DOMAIN TO REORDER:
{domain_str}
"""
