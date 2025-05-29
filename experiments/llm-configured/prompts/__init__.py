from .zero_shot import generate_prompt as zero_shot
from .few_shot import generate_prompt as few_shot
from .cot import generate_prompt as cot

def get_prompt_function(name: str):
    if name == "zero_shot":
        return zero_shot
    elif name == "few_shot":
        return few_shot
    elif name == "cot":
        return cot
    else:
        raise ValueError(f"Unknown prompt type: {name}")