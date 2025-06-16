from .zero_shot_short import generate_prompt as zero_shot_short_prompt
from .zero_shot_long import generate_prompt as zero_shot_long_prompt
from .few_shot_short import generate_prompt as few_shot_short_prompt
from .few_shot_long import generate_prompt as few_shot_long_prompt
from .cot import generate_messages as cot_prompt

def get_prompt(prompt_style: str):
    if prompt_style == "zero_shot_short":
        return zero_shot_short_prompt, "text"
    elif prompt_style == "zero_shot_long":
        return zero_shot_long_prompt, "text"
    elif prompt_style == "few_shot_short":
        return few_shot_short_prompt, "text"
    elif prompt_style == "few_shot_long":
        return few_shot_long_prompt, "text"
    elif prompt_style == "cot":
        return cot_prompt, "cot"
    else:
        raise ValueError(f"Unknown prompt style: {prompt_style}")

