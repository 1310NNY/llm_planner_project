import pandas as pd

# === Konfiguration ===
CSV_PATH = "../results/all_llm_combined.csv"
CUTOFF = 300  # Timeout in Sekunden für PAR10

# === Daten laden ===
df = pd.read_csv(CSV_PATH)

# === Instanz-ID erstellen
df["instance_id"] = df["domain"].astype(str) + "::" + df["problem"].astype(str)

# === Beste PlanCost pro Instanz (für IPC Score)
success_df = df[df["Status"] == "SUCCESS"]
best_costs = success_df.groupby("instance_id")["PlanCost"].min().reset_index()
best_costs = best_costs.rename(columns={"PlanCost": "BestCost"})

# === BestCost mergen
df = df.merge(best_costs, on="instance_id", how="left")
df["IPC_Score"] = df["BestCost"] / df["PlanCost"]

# === PAR10 berechnen
df["PAR10"] = df.apply(
    lambda row: row["Runtime_wall_s"] if row["Status"] == "SUCCESS" else 10 * CUTOFF,
    axis=1
)

# === Status-Indikatoren
df["Solved"] = df["Status"] == "SUCCESS"
df["Invalid"] = df["Status"] == "INVALID_DOMAIN"
df["Failure"] = df["Status"] == "FAILURE"
df["Timeout"] = df["Status"] == "TIMEOUT"
df["Attempted"] = ~df["Invalid"]  # Alles außer INVALID_DOMAIN

# === Gruppierung nach planner, domain, llm, prompt
group_cols = ["planner", "domain", "LLM_Model", "Prompt_ID"]

metrics = df.groupby(group_cols).agg(
    Coverage=("Solved", "mean"),
    Solved_Abs=("Solved", "sum"),
    IPC_Score_Sum=("IPC_Score", "sum"),
    PAR10_Avg=("PAR10", "mean"),
    Valid_Domain_Rate=("Valid_Domain", "mean"),
    Invalid_Domain_Rate=("Invalid", "mean"),
    Failure_Rate=("Failure", "mean"),
    Timeout_Rate=("Timeout", "mean"),
    Attempted_Rate=("Attempted", "mean"),
    LLM_API_Time_Avg=("LLM_API_Time_s", "mean"),
    Num_Instances=("instance_id", "nunique")
).reset_index()

# === Runden & Speichern
metrics = metrics.round(3)
#metrics.to_csv("../results/llm_metrics_summary.csv", index=False)
print(metrics)
print("\n✅ Analyse abgeschlossen. Ergebnisse gespeichert in 'llm_metrics_summary.csv'")
