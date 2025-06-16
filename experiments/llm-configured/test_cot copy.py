import pandas as pd
from pathlib import Path

def remove_all_cot_and_mixtral_entries(csv_path: Path) -> None:
    if not csv_path.exists():
        print(f"⚠️ Datei nicht gefunden: {csv_path}")
        return

    # CSV laden
    df = pd.read_csv(csv_path)
    original_count = len(df)

    # Filter anwenden: nur behalten, was weder cot noch mixtral ist
    filtered_df = df[(df["Prompt_ID"] != "cot") & (df["LLM_Model"] != "mixtral")]
    removed_count = original_count - len(filtered_df)

    # Datei überschreiben
    filtered_df.to_csv(csv_path, index=False)
    print(f"✅ Entfernt: {removed_count} Zeile(n) mit Prompt_ID='cot' oder LLM_Model='mixtral' aus {csv_path}")

if __name__ == "__main__":
    csv_file = Path("results/llm_domain_rewrites.csv")
    remove_all_cot_and_mixtral_entries(csv_file)

