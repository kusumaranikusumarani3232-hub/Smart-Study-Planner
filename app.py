import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

st.title("📚 Smart Study Planner")

# -------- USER INPUT --------
st.sidebar.header("Enter Details")

subjects_input = st.sidebar.text_input("Subjects (comma separated)", "Math,Physics,CS")
exam_days = st.sidebar.number_input("Days until exam", min_value=1, value=10)

weak_subjects_input = st.sidebar.text_input("Weak Subjects", "Math")

subjects_list = [s.strip() for s in subjects_input.split(",")]
weak_subjects = [s.strip() for s in weak_subjects_input.split(",")]

# Topics
topics = {
    "Math": ["Algebra", "Calculus", "Trigonometry"],
    "Physics": ["Mechanics", "Optics"],
    "CS": ["Python", "Data Structures"]
}

# -------- AI-like function --------
def get_ai_suggestion(subject, topic, hours):
    if subject == "Math":
        return f"Practice {topic} problems and revise formulas."
    elif subject == "Physics":
        return f"Understand concepts of {topic} and solve numericals."
    elif subject == "CS":
        return f"Write code for {topic} and debug errors."
    else:
        return "Study regularly."

# -------- GENERATE PLAN --------
if st.button("Generate Study Plan"):

    plan = []
    start_date = datetime.today()

    for subject in subjects_list:
        difficulty = 3 if subject in weak_subjects else 2

        for i in range(exam_days):
            study_day = start_date + timedelta(days=i)

            if i % 3 == 0:
                study_type = "Revision"
            elif i % 3 == 1:
                study_type = "Practice"
            else:
                study_type = "Concept Learning"

            hours = difficulty * 2
            topic = random.choice(topics.get(subject, ["General"]))

            plan.append({
                "Date": study_day.strftime("%Y-%m-%d"),
                "Subject": subject,
                "Hours": hours,
                "Topic": topic,
                "Study_Type": study_type,
                "AI_Suggestion": get_ai_suggestion(subject, topic, hours)
            })

    df = pd.DataFrame(plan)

    st.success("✅ Study Plan Generated!")
    st.dataframe(df)

    # डाउनलोड option
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "study_plan.csv", "text/csv")