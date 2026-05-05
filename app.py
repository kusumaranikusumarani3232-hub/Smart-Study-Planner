import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import os

st.title("📚 Smart Study Planner")

# ---------- FILE NAME ----------
FILE_NAME = "saved_plan.csv"

# ---------- USER INPUT ----------
st.sidebar.header("Enter Details")

subjects_input = st.sidebar.text_input("Subjects (comma separated)", "Math,Physics,CS")
exam_days = st.sidebar.number_input("Days until exam", min_value=1, value=10)
weak_subjects_input = st.sidebar.text_input("Weak Subjects", "Math")

subjects_list = [s.strip() for s in subjects_input.split(",")]
weak_subjects = [s.strip() for s in weak_subjects_input.split(",")]

# ---------- TOPIC DATABASE ----------
topics_dict = {
    "Math": ["Algebra", "Calculus", "Trigonometry", "Probability"],
    "Physics": ["Mechanics", "Optics", "Thermodynamics", "Modern Physics"],
    "CS": ["Data Structures", "Algorithms", "DBMS", "Operating Systems"]
}

# ---------- LOAD SAVED DATA ----------
if "plan_df" not in st.session_state:
    if os.path.exists(FILE_NAME):
        st.session_state.plan_df = pd.read_csv(FILE_NAME)
    else:
        st.session_state.plan_df = None

# ---------- GENERATE PLAN ----------
if st.button("🚀 Generate Study Plan"):

    start_date = datetime.today()
    plan = []

    for i in range(exam_days):
        study_day = start_date + timedelta(days=i)

        for subject in subjects_list:

            topic = random.choice(topics_dict.get(subject, ["General Study"]))

            if subject in weak_subjects:
                hours = 3
                suggestion = f"⚠ Focus more on {topic}"
            else:
                hours = 2
                suggestion = f"Revise {topic}"

            if i % 3 == 0:
                study_type = "Revision"
            elif i % 3 == 1:
                study_type = "Practice"
            else:
                study_type = "Test"

            plan.append([
                study_day.strftime("%Y-%m-%d"),
                subject,
                hours,
                topic,
                study_type,
                suggestion,
                False
            ])

    df = pd.DataFrame(plan, columns=["Date", "Subject", "Hours", "Topic", "Type", "Suggestion", "Completed"])

    st.session_state.plan_df = df
    df.to_csv(FILE_NAME, index=False)  # ✅ Save immediately

# ---------- DISPLAY ----------
if st.session_state.plan_df is not None:

    df = st.session_state.plan_df

    st.success("✅ Plan Loaded")

    edited_df = st.data_editor(df, use_container_width=True)

    # Save updates automatically
    edited_df.to_csv(FILE_NAME, index=False)
    st.session_state.plan_df = edited_df

    # Progress
    total = len(edited_df)
    completed = edited_df["Completed"].sum()
    progress = completed / total if total > 0 else 0

    st.subheader("📊 Progress")
    st.progress(progress)
    st.write(f"✅ Completed: {completed} / {total}")

    # Chart
    st.subheader("📈 Study Hours per Subject")
    st.bar_chart(edited_df.groupby("Subject")["Hours"].sum())

    # Download
    st.download_button("📥 Download Plan", edited_df.to_csv(index=False), "study_plan.csv")

# ---------- RESET BUTTON ----------
if st.button("🗑 Reset Plan"):
    if os.path.exists(FILE_NAME):
        os.remove(FILE_NAME)
    st.session_state.plan_df = None
    st.success("Plan Reset! Refresh page.")
