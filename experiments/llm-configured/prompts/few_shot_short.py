def generate_prompt(domain_str: str) -> str:
    return f"""Here is an example of a domain before and after reordering:

[ORIGINAL]
(define (domain elevators)
(:requirements :strips :typing)
(:predicates (at ?p ?f) (lift-empty ?l) (onboard ?p ?l) (served ?f) (waiting ?p ?f))
(:action board
 :parameters (?p ?l ?f)
 :precondition (and (at ?p ?f) (lift-empty ?l))
 :effect (and (not (at ?p ?f)) (onboard ?p ?l) (not (lift-empty ?l))))
(:action depart
 :parameters (?p ?l ?f)
 :precondition (and (onboard ?p ?l))
 :effect (and (served ?f) (lift-empty ?l) (not (onboard ?p ?l))))
)

[REORDERED]
(define (domain elevators)
(:requirements :strips :typing)
(:predicates (at ?p ?f) (lift-empty ?l) (onboard ?p ?l) (served ?f) (waiting ?p ?f))
(:action depart
 :parameters (?p ?l ?f)
 :precondition (and (onboard ?p ?l))
 :effect (and (served ?f) (lift-empty ?l) (not (onboard ?p ?l))))
(:action board
 :parameters (?p ?l ?f)
 :precondition (and (at ?p ?f) (lift-empty ?l))
 :effect (and (not (at ?p ?f)) (onboard ?p ?l) (not (lift-empty ?l))))
)

Now reorder this new domain:

{domain_str}

Return only the reordered domain file, starting with (define.
"""