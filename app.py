import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="Smart Study Planner", layout="wide")

# ---------- TITLE ----------
st.title("📚 Smart Study Planner")
st.markdown("### Plan smarter, not harder 💡")

# ---------- LAYOUT ----------
col1, col2 = st.columns([1,2])

with col1:
    st.header("Enter Details")

    subjects_input = st.text_input("Subjects (comma separated)", "Math,Physics,CS")
    days = st.number_input("Days until exam", min_value=1, value=10)
    weak_input = st.text_input("Weak Subjects", "Math")

    subjects = [s.strip() for s in subjects_input.split(",") if s.strip()]
    weak_subjects = [s.strip() for s in weak_input.split(",") if s.strip()]

    st.subheader("Difficulty (1–3)")
    difficulty = {}
    for sub in subjects:
        difficulty[sub] = st.slider(sub, 1, 3, 2)

# ---------- TOPICS ----------
topics = {
    "Math": ["Algebra", "Calculus", "Trigonometry"],
    "Physics": ["Mechanics", "Optics"],
    "CS": ["Python", "Data Structures"]
}

def get_suggestion(subject, topic, hours, is_weak):
    if is_weak:
        return f"⚠️ Focus more on {topic}. Strengthen basics + practice more."

    if subject == "Math":
        return f"Practice {topic} problems + revise formulas."
    elif subject == "Physics":
        return f"Understand {topic} + solve numericals."
    elif subject == "CS":
        return f"Code {topic} problems."
    
    return f"Study {topic}"

# ---------- GENERATE ----------
with col2:
    if st.button("🚀 Generate Study Plan"):

        plan = []
        start = datetime.today()

        for i in range(days):
            date = start + timedelta(days=i)

            for subject in subjects:
                base = difficulty[subject]
                hours = base * 3 if subject in weak_subjects else base * 2

                study_type = ["Revision", "Practice", "Concept"][i % 3]
                topic = random.choice(topics.get(subject, ["General"]))

                suggestion = get_suggestion(subject, topic, hours, subject in weak_subjects)

                plan.append({
                    "Date": date.strftime("%Y-%m-%d"),
                    "Subject": subject,
                    "Hours": hours,
                    "Topic": topic,
                    "Type": study_type,
                    "Suggestion": suggestion
                })

        df = pd.DataFrame(plan)

        # ---------- SUMMARY ----------
        st.success("✅ Plan Generated")

        total_hours = df["Hours"].sum()
        st.metric("📊 Total Study Hours", total_hours)

        # ---------- TABLE ----------
        st.dataframe(df, use_container_width=True)

        # ---------- CHART ----------
        st.subheader("📊 Hours per Subject")
        chart = df.groupby("Subject")["Hours"].sum()
        st.bar_chart(chart)

        # ---------- DOWNLOAD ----------
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Download CSV", csv, "study_plan.csv", "text/csv")


           
            
    
