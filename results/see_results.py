import streamlit as st
import pandas as pd

st.title("CSV-Datei anzeigen")

# CSV-Datei hochladen
csv_file = st.file_uploader("Wähle eine CSV-Datei", type=["csv"])

if csv_file is not None:
    df = pd.read_csv(csv_file)

    # Vorschau der Daten
    st.subheader("Tabellarische Vorschau")
    st.dataframe(df)

    # Optional: Filterfunktion
    st.subheader("Spaltenfilter")
    spalten = st.multiselect("Wähle Spalten zum Anzeigen", df.columns.tolist(), default=df.columns.tolist())
    st.dataframe(df[spalten])

#run streamlit run /Users/daniel/Projects/llm_planner_project/results/see_results.py