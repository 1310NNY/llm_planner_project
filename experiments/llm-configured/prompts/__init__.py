from .zero_shot_short import generate_prompt as zero_shot_short_prompt
from .zero_shot_long import generate_prompt as zero_shot_long_prompt
from .few_shot_short import generate_prompt as few_shot_short_prompt
from .few_shot_long import generate_prompt as few_shot_long_prompt
from .cot_short import generate_messages as chain_of_thought_short_prompt
from .cot_long import generate_messages as chain_of_thought_long_prompt

def get_prompt(prompt_style: str):
    if prompt_style == "zero_shot_short":
        return zero_shot_short_prompt
    elif prompt_style == "zero_shot_long":
        return zero_shot_long_prompt
    elif prompt_style == "few_shot_short":
        return few_shot_short_prompt
    elif prompt_style == "few_shot_long":
        return few_shot_long_prompt
    elif prompt_style == "cot_short":
        return chain_of_thought_short_prompt
    elif prompt_style == "cot_long":
        return chain_of_thought_long_prompt
    else:
        raise ValueError(f"Unknown prompt style: {prompt_style}")