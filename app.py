"""
TalentTrack — Mini Recruitment CRM
A small Python project: track job candidates through a hiring pipeline.
Built with Streamlit + SQLite + Pandas.

Run it with:
    pip install streamlit pandas
    streamlit run app.py
"""

import sqlite3
from datetime import date

import pandas as pd
import streamlit as st

DB_PATH = "candidates.db"
STAGES = ["Applied", "Screening", "Interview", "Offer", "Hired", "Rejected"]


# ---------- Data layer (keep all SQL in one place so it's easy to extend) ----------

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role_applied TEXT NOT NULL,
            source TEXT,
            stage TEXT NOT NULL,
            notes TEXT,
            date_added TEXT
        )
        """
    )
    conn.commit()
    return conn


def add_candidate(conn, name, role, source, stage, notes):
    conn.execute(
        "INSERT INTO candidates (name, role_applied, source, stage, notes, date_added) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (name, role, source, stage, notes, str(date.today())),
    )
    conn.commit()


def update_stage(conn, candidate_id, new_stage):
    conn.execute("UPDATE candidates SET stage = ? WHERE id = ?", (new_stage, candidate_id))
    conn.commit()


def delete_candidate(conn, candidate_id):
    conn.execute("DELETE FROM candidates WHERE id = ?", (candidate_id,))
    conn.commit()


def fetch_candidates(conn):
    return pd.read_sql_query("SELECT * FROM candidates ORDER BY date_added DESC", conn)


# ---------- UI ----------

st.set_page_config(page_title="TalentTrack — Mini CRM", layout="wide")
st.title("🧑‍💼 TalentTrack — Mini Recruitment CRM")
st.caption("A lightweight candidate tracker: add, filter, and move candidates through a hiring pipeline.")

conn = get_connection()

# --- Add candidate ---
with st.expander("➕ Add a new candidate", expanded=False):
    with st.form("add_candidate_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        name = col1.text_input("Candidate name")
        role = col2.text_input("Role applied for")
        col3, col4 = st.columns(2)
        source = col3.selectbox("Source", ["LinkedIn", "Referral", "Job Portal", "College Placement", "Other"])
        stage = col4.selectbox("Starting stage", STAGES)
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Add candidate")
        if submitted:
            if name.strip() and role.strip():
                add_candidate(conn, name.strip(), role.strip(), source, stage, notes.strip())
                st.success(f"Added {name} to the pipeline.")
            else:
                st.error("Name and role are required.")

df = fetch_candidates(conn)

# --- Dashboard ---
st.subheader("📊 Pipeline overview")
if df.empty:
    st.info("No candidates yet — add one above to get started.")
else:
    counts = df["stage"].value_counts().reindex(STAGES, fill_value=0)
    cols = st.columns(len(STAGES))
    for c, stage_name in zip(cols, STAGES):
        c.metric(stage_name, int(counts[stage_name]))

    st.bar_chart(counts)

    # --- Filters ---
    st.subheader("🔍 Candidates")
    fcol1, fcol2, fcol3 = st.columns(3)
    stage_filter = fcol1.multiselect("Filter by stage", STAGES, default=STAGES)
    role_filter = fcol2.text_input("Filter by role (contains)")
    search = fcol3.text_input("Search by name")

    filtered = df[df["stage"].isin(stage_filter)]
    if role_filter:
        filtered = filtered[filtered["role_applied"].str.contains(role_filter, case=False, na=False)]
    if search:
        filtered = filtered[filtered["name"].str.contains(search, case=False, na=False)]

    st.dataframe(filtered, use_container_width=True, hide_index=True)

    # --- Update / delete a candidate ---
    st.subheader("✏️ Update a candidate")
    if not filtered.empty:
        options = {f'{row["id"]} — {row["name"]} ({row["role_applied"]})': row["id"] for _, row in filtered.iterrows()}
        choice = st.selectbox("Select candidate", list(options.keys()))
        selected_id = options[choice]
        new_stage = st.selectbox("Move to stage", STAGES, key="move_stage")
        b1, b2 = st.columns(2)
        if b1.button("Update stage"):
            update_stage(conn, selected_id, new_stage)
            st.rerun()
        if b2.button("Delete candidate", type="secondary"):
            delete_candidate(conn, selected_id)
            st.rerun()

    # --- Export ---
    st.download_button(
        "⬇️ Export all candidates as CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="candidates.csv",
        mime="text/csv",
    )
