import pandas as pd

# CSV laden
df = pd.read_csv("llm_domain_rewrites.csv")

# Nur Zeilen behalten, bei denen 'problem' mit 'instance' beginnt
df_filtered = df[df['problem'].str.startswith("instance")]

# Funktion zur Reduktion einer Gruppe
def reduce_group(group):
    # Erste Zeile behalten
    row = group.iloc[0].copy()
    # Valid_Domain auf True nur, wenn alle Zeilen True sind
    row['Valid_Domain'] = group['Valid_Domain'].all()
    return row

# Gruppieren und anwenden – zukunftssicher, domain bleibt erhalten
result_df = (
    df_filtered
    .groupby('domain', group_keys=False)
    .apply(reduce_group)
    .reset_index(drop=True)
)

# Ergebnis anzeigen oder weiterverarbeiten
print(result_df)

print(result_df['Valid_Domain'].value_counts())

cols_to_check = ['LLM_Model', 'Prompt_ID', 'LLM_Temperature', 'domain']

for col in cols_to_check:
    print(f"\n=== Verteilung von '{col}' nach Valid_Domain ===")
    print(result_df.groupby('Valid_Domain')[col].value_counts())

for col in cols_to_check:
    print(f"\n=== Prozentuale Verteilung von '{col}' nach Valid_Domain ===")
    print(result_df.groupby('Valid_Domain')[col].value_counts(normalize=True) * 100)
