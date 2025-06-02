import os
import sys
import time
import re
import pandas as pd
from openai import OpenAI
from difflib import unified_diff
from datetime import datetime
from dotenv import load_dotenv

# Automatically detect project root
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.insert(0, project_root)

# Import run_downward (assumed to be in experiments/base/)
from experiments.base.run_downward import run_downward
#what if dont find?

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def extract_action_order(domain_text):
    return re.findall(r'\(:action\s+(\w+)', domain_text)

def compare_order(original, modified):
    if set(original) != set(modified):
        return -1
    return sum(o != m for o, m in zip(original, modified))

def extract_action_blocks(text):
    actions = {}
    pattern = re.findall(
        r'\(:action\s+(\w+).*?:precondition\s+\((.*?)\).*?:effect\s+\((.*?)\)',
        text, re.DOTALL
    )
    for name, pre, eff in pattern:
        pre_clean = re.findall(r'\([^\(\)]+\)', pre)
        eff_clean = re.findall(r'\([^\(\)]+\)', eff)
        actions[name] = (pre_clean, eff_clean)
    return actions

def compare_reordering(dict1, dict2):
    pre_total = 0
    eff_total = 0
    for name in dict1:
        if name not in dict2:
            return -1, -1
        pre1, eff1 = dict1[name]
        pre2, eff2 = dict2[name]

        if set(pre1) != set(pre2) or set(eff1) != set(eff2):
            return -1, -1

        pre_total += sum(a != b for a, b in zip(pre1, pre2))
        eff_total += sum(a != b for a, b in zip(eff1, eff2))
    return pre_total, eff_total


def detect_semantic_differences(original_blocks, modified_blocks):
    action_changes = 0
    pre_added = 0
    pre_removed = 0
    eff_added = 0
    eff_removed = 0

    for name, (pre1, eff1) in original_blocks.items():
        if name not in modified_blocks:
            action_changes += 1
            continue
        pre2, eff2 = modified_blocks[name]
        pre_added += len(set(pre2) - set(pre1))
        pre_removed += len(set(pre1) - set(pre2))
        eff_added += len(set(eff2) - set(eff1))
        eff_removed += len(set(eff1) - set(eff2))
        if set(pre1) != set(pre2) or set(eff1) != set(eff2):
            action_changes += 1

    for name in modified_blocks:
        if name not in original_blocks:
            action_changes += 1

    semantic_change = action_changes > 0 or pre_added > 0 or pre_removed > 0 or eff_added > 0 or eff_removed > 0

    return {
        "Num_Semantic_Action_Changes": action_changes,
        "Num_Preconditions_Added": pre_added,
        "Num_Preconditions_Removed": pre_removed,
        "Num_Effects_Added": eff_added,
        "Num_Effects_Removed": eff_removed,
        "Semantic_Change_Detected": semantic_change
    }

def load_prompt_template(prompt_path, domain_content):
    with open(prompt_path, "r") as f:
        template = f.read()
    return template.replace("{domain_content}", domain_content)

def build_output_filename(llm_model, prompt_path, planner, domain_file):
    domain_group = os.path.basename(os.path.dirname(domain_file))
    prompt_id = os.path.splitext(os.path.basename(prompt_path))[0]
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    return f"{domain_group}_domain_{llm_model}_{prompt_id}_{planner}_{timestamp}.pddl"

def optimize_domain_with_llm(domain_content, prompt_path, model="gpt-4"):
    full_start = time.time()
    prompt = load_prompt_template(prompt_path, domain_content)

    api_start = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a PDDL expert."},
            {"role": "user", "content": prompt}
        ]
    )
    api_end = time.time()
    full_end = time.time()

    content = response.choices[0].message.content
    usage = response.usage

    return {
        "modified_domain": content,
        "model": model,
        "api_duration": round(api_end - api_start, 3),
        "full_duration": round(full_end - full_start, 3),
        "tokens_prompt": usage.prompt_tokens,
        "tokens_completion": usage.completion_tokens,
        "tokens_total": usage.total_tokens,
        "prompt_length_chars": len(prompt),
        "completion_length_chars": len(content)
    }

def run_for_all_instances(domain_file, instances_folder, prompt_path, output_csv=None, planner="downward", model="gpt-4"):
    results = []
    llm_start_time = time.time()

    with open(domain_file, "r") as f:
        domain_content = f.read()

    original_order = extract_action_order(domain_content)
    original_blocks = extract_action_blocks(domain_content)

    llm_result = optimize_domain_with_llm(domain_content, prompt_path, model=model)
    modified_domain = llm_result["modified_domain"]

    modified_order = extract_action_order(modified_domain)
    modified_blocks = extract_action_blocks(modified_domain)

    reorder_distance = compare_order(original_order, modified_order)
    pre_diff, eff_diff = compare_reordering(original_blocks, modified_blocks)

    semantic_metrics = detect_semantic_differences(original_blocks, modified_blocks)

    benchmark_dir = os.path.dirname(domain_file)
    domain_filename = build_output_filename(model, prompt_path, planner, domain_file)
    domain_path = os.path.join(benchmark_dir, domain_filename)

    with open(domain_path, "w") as f:
        f.write(modified_domain)

    print(f"[INFO] Modified domain: {domain_path}")

    def extract_number(filename):
        match = re.search(r'(\d+)', filename)
        return int(match.group(1)) if match else float('inf')

    instance_files = sorted(
        [f for f in os.listdir(instances_folder) if f.endswith(".pddl")],
        key=extract_number
    )

    for filename in instance_files:
        instance_path = os.path.join(instances_folder, filename)
        result = run_downward(domain_path, instance_path)

        result.update({
            "DomainFile": os.path.basename(domain_path),
            "ProblemFile": filename,
            "LLM_Model": model,
            "Prompt_ID": os.path.splitext(os.path.basename(prompt_path))[0],
            "Planner": planner,
            "LLM_API_Time_s": llm_result["api_duration"],
            "LLM_API_Time_with_Preproccess_s": llm_result["full_duration"],
            "Tokens_Total": llm_result["tokens_total"],
            "Prompt_Length_Chars": llm_result["prompt_length_chars"],
            "Completion_Length_Chars": llm_result["completion_length_chars"],
            "Action_Reorder_Distance": reorder_distance,
            "Precondition_Reorder_Distance": pre_diff,
            "Effect_Reorder_Distance": eff_diff,
            **semantic_metrics
        })

        results.append(result)

    df = pd.DataFrame(results)
    if output_csv:
        os.makedirs(os.path.dirname(output_csv), exist_ok=True)
        write_header = not os.path.exists(output_csv)
        df.to_csv(output_csv, mode='a', header=write_header, index=False)
        print(f"[INFO] Results saved to: {output_csv}")
    return df

if __name__ == "__main__":
    domain_file = "benchmarks/test/domain.pddl"
    instance_path = "benchmarks/test/instances/instance-1.pddl"
    prompt_file = "experiments/llm-configured/prompts/reorder_prompt_vallati.txt"
    model = "gpt-4"
    planner = "downward"

    prompt_id = os.path.splitext(os.path.basename(prompt_file))[0]
    output_csv = f"results/{planner}_{model}_{prompt_id}_results.csv"

    all_results = run_for_all_instances(
        domain_file,
        os.path.join(os.path.dirname(instance_path), ""),
        prompt_file,
        output_csv=output_csv,
        planner=planner,
        model=model
    )
    print("[ALL INSTANCE RESULTS]:")
    print(all_results)