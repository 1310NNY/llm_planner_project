import json

def extract_pddl_from_response(response_text: str) -> str:
    if not isinstance(response_text, str):
        return ""

    # Sonderfall: GPT-4o oder o4-mini liefert evtl. escaped string
    if response_text.strip().startswith('"') and "\\n" in response_text:
        try:
            response_text = json.loads(response_text)
        except json.JSONDecodeError:
            pass  # fallback ohne Änderung

    # 🔧 Wandle explizite "\\n" in echte Zeilenumbrüche um (falls json.loads nicht nötig war)
    response_text = response_text.replace("\\n", "\n")

    # Starte bei "(define"
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
                end_idx = i + 1
                break

    if end_idx is None:
        return ""

    return pddl_candidate[:end_idx].strip()