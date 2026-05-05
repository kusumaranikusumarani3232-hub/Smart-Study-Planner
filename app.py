import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

st.title("📚 Smart Study Planner")

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

# ---------- GENERATE PLAN ----------
if st.button("🚀 Generate Study Plan"):

    start_date = datetime.today()
    plan = []

    for i in range(exam_days):
        study_day = start_date + timedelta(days=i)

        for subject in subjects_list:

            # Topic selection
            if subject in topics_dict:
                topic = random.choice(topics_dict[subject])
            else:
                topic = "General Study"

            # Hours logic
            if subject in weak_subjects:
                hours = 3
                suggestion = f"⚠ Focus more on {topic}"
            else:
                hours = 2
                suggestion = f"Revise {topic}"

            # Study type
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
                suggestion
            ])

    df = pd.DataFrame(plan, columns=["Date", "Subject", "Hours", "Topic", "Type", "Suggestion"])

    st.success("✅ Plan Generated")

    # Show total hours
    st.subheader("📊 Total Study Hours")
    st.write(df["Hours"].sum())

    # Show table
    st.dataframe(df)

    # Chart
    st.subheader("📈 Study Hours per Subject")
    st.bar_chart(df.groupby("Subject")["Hours"].sum())

    # Download
    st.download_button("📥 Download Plan", df.to_csv(index=False), "study_plan.csv")
