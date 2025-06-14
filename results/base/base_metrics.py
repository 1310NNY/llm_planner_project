import pandas as pd
import glob
import os

# === Konfiguration ===
CUTOFF = 300  # Timeout in Sekunden

# === Hilfsfunktion zum Runden
def smart_round(df):
    for col in df.columns:
        if "Coverage" in col or "IPC_Score" in col:
            df[col] = df[col].round(2)
        elif "PAR10" in col:
            df[col] = df[col].round(1)
    return df

# === CSV-Dateien im gleichen Verzeichnis wie dieses Skript finden
script_dir = os.path.dirname(__file__)
csv_files = glob.glob(os.path.join(script_dir, "*_results.csv"))
print("Gefundene CSV-Dateien:", csv_files)

# === Schritt 1: Globale Instanzmenge aufbauen (domain + problem)
all_instances = set()
for file_path in csv_files:
    try:
        df_all = pd.read_csv(file_path)
        if "domain" in df_all.columns and "problem" in df_all.columns:
            pairs = df_all[["domain", "problem"]].drop_duplicates()
            all_instances.update([tuple(x) for x in pairs.to_numpy()])
    except pd.errors.EmptyDataError:
        continue

# === Schritt 2: Pro Planner auswerten
summary_list = []
domain_summary = []

for file_path in csv_files:
    try:
        df = pd.read_csv(file_path)
    except pd.errors.EmptyDataError:
        print(f"Übersprungen (komplett leer): {file_path}")
        continue

    if "planner" in df.columns and not df.empty:
        planner_name = df["planner"].iloc[0]
        print(f"Bearbeite Planner '{planner_name}' in Datei {file_path}")
    else:
        print(f"Übersprungen (leer oder ohne planner): {file_path}")
        continue

    # === Globale Metriken
    solved_df = df[df["Status"] == "SUCCESS"]
    solved_pairs = set([tuple(x) for x in solved_df[["domain", "problem"]].to_numpy()])
    coverage = len(solved_pairs) / len(all_instances) if all_instances else 0

    ipc_score = 0
    if not solved_df.empty:
        best_costs = solved_df.groupby(["domain", "problem"])["PlanCost"].min().reset_index()
        best_costs = best_costs.rename(columns={"PlanCost": "BestCost"})
        merged = solved_df.merge(best_costs, on=["domain", "problem"])
        merged["IPC_score"] = merged["BestCost"] / merged["PlanCost"]
        ipc_score = merged["IPC_score"].sum()

    df["PAR10"] = df.apply(
        lambda row: row["Runtime_wall_s"] if row["Status"] == "SUCCESS" else 10 * CUTOFF,
        axis=1
    )
    par10 = df["PAR10"].mean()

    summary_list.append({
        "planner": planner_name,
        "Coverage": coverage,
        "IPC_Score": ipc_score,
        "PAR10": par10
    })

    # === Pro Domain
    for domain in df["domain"].unique():
        domain_df = df[df["domain"] == domain]
        solved_df = domain_df[domain_df["Status"] == "SUCCESS"]
        domain_problems = {(d, p) for (d, p) in all_instances if d == domain}
        solved_pairs = set([tuple(x) for x in solved_df[["domain", "problem"]].to_numpy()])
        coverage = len(solved_pairs) / len(domain_problems) if domain_problems else 0

        ipc_score = 0
        if not solved_df.empty:
            best_costs = solved_df.groupby(["domain", "problem"])["PlanCost"].min().reset_index()
            best_costs = best_costs.rename(columns={"PlanCost": "BestCost"})
            merged = solved_df.merge(best_costs, on=["domain", "problem"])
            merged["IPC_score"] = merged["BestCost"] / merged["PlanCost"]
            ipc_score = merged["IPC_score"].sum()

        domain_df["PAR10"] = domain_df.apply(
            lambda row: row["Runtime_wall_s"] if row["Status"] == "SUCCESS" else 10 * CUTOFF,
            axis=1
        )
        par10 = domain_df["PAR10"].mean()

        domain_summary.append({
            "planner": planner_name,
            "domain": domain,
            "Coverage": coverage,
            "IPC_Score": ipc_score,
            "PAR10": par10
        })

# === 1. Globale Planner-Metriken
if summary_list:
    overall_df = pd.DataFrame(summary_list).set_index("planner")
    overall_df = smart_round(overall_df)
    print("\n=== Baseline-Metriken über alle Domains & Probleme ===")
    print(overall_df)
    overall_df.to_csv(os.path.join(script_dir, "summary_overall.csv"))
else:
    print("⚠️ Keine Planner-Daten verarbeitet.")
    exit(1)

# === 2. Pro-Domain & Planner
domain_planner_df = pd.DataFrame(domain_summary)
domain_planner_df = smart_round(domain_planner_df)
domain_planner_df.to_csv(os.path.join(script_dir, "summary_per_domain_planner.csv"), index=False)

# === 3. Mittelwerte pro Domain
domain_means = domain_planner_df.groupby("domain").agg({
    "Coverage": "mean",
    "IPC_Score": "mean",
    "PAR10": "mean"
}).reset_index()

# === 4. Streuungen pro Domain
domain_std = domain_planner_df.groupby("domain").agg({
    "Coverage": "std",
    "IPC_Score": "std",
    "PAR10": "std"
}).rename(columns={
    "Coverage": "Coverage_std",
    "IPC_Score": "IPC_Score_std",
    "PAR10": "PAR10_std"
}).reset_index()

# === 5. Kombinieren & Runden
domain_combined = pd.merge(domain_means, domain_std, on="domain")
domain_combined = smart_round(domain_combined)

print("\n=== Durchschnitt + Streuung pro Domain ===")
print(domain_combined)

domain_combined.to_csv(os.path.join(script_dir, "summary_domain_combined.csv"), index=False)
