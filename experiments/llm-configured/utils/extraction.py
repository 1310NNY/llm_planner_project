import re
import json

def extract_pddl_from_response(response_text: str) -> str:
    """
    Extrahiert echten PDDL-Text, auch wenn er als escaped-String (JSON-Stil) kommt.
    """
    if not isinstance(response_text, str):
        return ""

    # Sonderfall: string wie '"(define...\\n...)"' → versuche JSON-Unescaping
    if response_text.strip().startswith('"') and "\\n" in response_text:
        try:
            response_text = json.loads(response_text)
        except json.JSONDecodeError:
            pass  # wenn fehlschlägt, normal weitermachen

    start_idx = response_text.find("(define")
    if start_idx == -1:
        return ""

    pddl_candidate = response_text[start_idx:]

    balance = 0
    end_idx = None
    for i, char in enumerate(pddl_candidate):
        if char == "(":
            balance += 1
        elif char == ")":
            balance -= 1
            if balance == 0:
                end_idx = i
                break

    return pddl_candidate[:end_idx + 1].strip() if end_idx is not None else pddl_candidate.strip()