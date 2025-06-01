def generate_prompt(domain_str: str) -> str:
    return f"""Here is an example of a domain before and after reordering:

[ORIGINAL]
(define (domain rovers)
(:requirements :strips :typing)
(:predicates
  (at ?r ?l)
  (have-image ?i)
  (on-board ?c ?r)
  (visible ?o ?l)
)

(:action navigate
 :parameters (?r ?from ?to)
 :precondition (and (at ?r ?from) (path ?from ?to))
 :effect (and (not (at ?r ?from)) (at ?r ?to)))

(:action take-image
 :parameters (?r ?i ?l ?c)
 :precondition (and (at ?r ?l) (camera ?c) (on-board ?c ?r) (visible ?i ?l))
 :effect (and (have-image ?i)))

(:action calibrate
 :parameters (?r ?c ?l)
 :precondition (and (at ?r ?l) (on-board ?c ?r))
 :effect (and (calibrated ?c)))
)

[REORDERED]
(define (domain rovers)
(:requirements :strips :typing)
(:predicates
  (at ?r ?l)
  (have-image ?i)
  (on-board ?c ?r)
  (visible ?o ?l)
)

(:action take-image
 :parameters (?r ?i ?l ?c)
 :precondition (and (at ?r ?l) (camera ?c) (on-board ?c ?r) (visible ?i ?l))
 :effect (and (have-image ?i)))

(:action calibrate
 :parameters (?r ?c ?l)
 :precondition (and (at ?r ?l) (on-board ?c ?r))
 :effect (and (calibrated ?c)))

(:action navigate
 :parameters (?r ?from ?to)
 :precondition (and (at ?r ?from) (path ?from ?to))
 :effect (and (not (at ?r ?from)) (at ?r ?to)))
)

Now reorder this new domain:

{domain_str}

Follow the same principles. Output only the final domain starting with (define and ending with the last parenthesis.
"""