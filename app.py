import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# -------- PAGE CONFIG --------
st.set_page_config(page_title="Smart Study Planner", layout="wide")

# -------- TITLE --------
st.title("📚 Smart Study Planner")
st.markdown("### Plan smarter, not harder 💡")

# -------- SIDEBAR INPUT --------
st.sidebar.header("Enter Details")

subjects_input = st.sidebar.text_input("Subjects (comma separated)", "Math,Physics,CS")
days = st.sidebar.number_input("Days until exam", min_value=1, value=10)
weak_input = st.sidebar.text_input("Weak Subjects", "Math")

subjects = [s.strip() for s in subjects_input.split(",") if s.strip()]
weak_subjects = [s.strip() for s in weak_input.split(",") if s.strip()]

# -------- DIFFICULTY --------
difficulty = {}
st.sidebar.subheader("Set Difficulty (1–3)")

for sub in subjects:
    difficulty[sub] = st.sidebar.slider(sub, 1, 3, 2)

# -------- TOPICS --------
topics = {
    "Math": ["Algebra", "Calculus", "Trigonometry"],
    "Physics": ["Mechanics", "Optics"],
    "CS": ["Python", "Data Structures"]
}

# -------- AI-LIKE SUGGESTION --------
def get_suggestion(subject, topic, hours, is_weak):
    if is_weak:
        return f"⚠️ Focus more on {topic}. Spend extra time understanding basics and solving problems."

    if subject == "Math":
        return f"Practice problems on {topic} and revise formulas."
    elif subject == "Physics":
        return f"Understand concepts of {topic} and solve numericals."
    elif subject == "CS":
        return f"Write code for {topic} and practice problems."

    return f"Study {topic} consistently."

# -------- GENERATE PLAN --------
if st.button("Generate Study Plan"):

    plan = []
    start = datetime.today()

    for i in range(days):
        date = start + timedelta(days=i)

        for subject in subjects:
            base = difficulty[subject]

            # Hours logic
            if subject in weak_subjects:
                hours = base * 3
            else:
                hours = base * 2

            # Study type
            if i % 3 == 0:
                study_type = "Revision"
            elif i % 3 == 1:
                study_type = "Practice"
            else:
                study_type = "Concept Learning"

            topic = random.choice(topics.get(subject, ["General"]))

            suggestion = get_suggestion(subject, topic, hours, subject in weak_subjects)

            plan.append({
                "Date": date.strftime("%Y-%m-%d"),
                "Subject": subject,
                "Hours": hours,
                "Topic": topic,
                "Study_Type": study_type,
                "Suggestion": suggestion
            })

    df = pd.DataFrame(plan)

    # -------- OUTPUT --------
    st.success("✅ Study Plan Generated!")
    st.dataframe(df, use_container_width=True)

    # -------- CHART --------
    st.subheader("📊 Study Hours Distribution")
    chart_data = df.groupby("Subject")["Hours"].sum()
    st.bar_chart(chart_data)

    # -------- DOWNLOAD --------
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇ Download CSV", csv, "study_plan.csv", "text/csv")
