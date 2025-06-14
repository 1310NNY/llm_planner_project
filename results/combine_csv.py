import pandas as pd
import glob

# Alle .csv-Dateien im Ordner (nur echte Ergebnisse)
csv_files = glob.glob("../results/*.csv")

# Zusammenführen
dfs = [pd.read_csv(f) for f in csv_files]
df_all = pd.concat(dfs, ignore_index=True)

# Optional: Spalten aufräumen, falls PlanCost doppelt
if "PlanCost.1" in df_all.columns:
    df_all["PlanCost"] = df_all["PlanCost"].fillna(df_all["PlanCost.1"])
    df_all.drop(columns=["PlanCost.1"], inplace=True)

# Speichern als große Datei
df_all.to_csv("../results/all_llm_combined.csv", index=False)


