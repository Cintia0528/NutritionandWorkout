import streamlit as st
import pandas as pd
from datetime import date, timedelta

st.set_page_config(page_title="Gym & Nutrition Tracker", layout="wide")

# --------- Helper functions ----------
def generate_dates(start_date, weeks=4):
    return [start_date + timedelta(days=i*7) for i in range(weeks)]

def make_workout_table(exercises, dates):
    columns = ["Exercise"] + [d.strftime("%Y-%m-%d") for d in dates]
    data = {col: ["" for _ in exercises] for col in columns}
    data["Exercise"] = exercises
    return pd.DataFrame(data)

# --------- Data ----------
start_date = date(2025, 9, 22)   # Sept 22
weeks = 4
dates = generate_dates(start_date, weeks)

workout_plan = {
    "Day 1 – Back + Shoulders": [
        "Pull-Ups (weighted)", "Overhead Press", "Single-Arm Dumbbell Row",
        "Arnold Press", "Face Pulls", "Lateral Raises"
    ],
    "Day 2 – Legs + Glutes (Hip Hinge)": [
        "Deadlift / RDL", "Bulgarian Split Squat", "Hip Thrust",
        "Step-Ups", "Hamstring Curl", "Glute Kickbacks"
    ],
    "Day 3 – Chest + Arms": [
        "Barbell Bench Press", "Incline Dumbbell Press", "Chest Fly",
        "Barbell Curl", "Hammer Curl", "Overhead Dumbbell Extension"
    ],
    "Day 4 – Legs + Glutes (Squat Focus)": [
        "Back/Front Squat", "Walking Lunges", "Romanian Deadlift",
        "Hip Thrust", "Leg Extension", "Calf Raises"
    ],
    "Day 5 – Back + Triceps": [
        "Barbell Row", "Seated Cable Row", "Rear Delt Fly",
        "Skull Crushers", "Rope Pushdowns", "Close Grip Bench Press"
    ]
}

# --------- Tabs ----------
tab1, tab2 = st.tabs(["Nutrition", "Gym Plan"])

# --------- Nutrition Tab ----------
with tab1:
    st.header("Nutrition Tracker")
    today = st.date_input("Select Date", date.today())
    
    if "nutrition" not in st.session_state:
        st.session_state["nutrition"] = {}
    
    if today not in st.session_state["nutrition"]:
        st.session_state["nutrition"][today] = {"Calories": 0, "Protein": 0}
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Calories 2000–2200", key="cal_btn"):
            st.session_state["nutrition"][today]["Calories"] = 2100
    with c2:
        if st.button("Protein 150g", key="prot_btn"):
            st.session_state["nutrition"][today]["Protein"] = 150
    
    st.write("### Daily Log")
    st.write(st.session_state["nutrition"])

# --------- Gym Plan Tab ----------
with tab2:
    st.header("Gym Plan Progression")
    
    if "workouts" not in st.session_state:
        st.session_state["workouts"] = {}
        for day, exercises in workout_plan.items():
            st.session_state["workouts"][day] = make_workout_table(exercises, dates)
    
    for day, df in st.session_state["workouts"].items():
        st.subheader(day)
        edited_df = st.data_editor(df, num_rows="dynamic", key=day)
        st.session_state["workouts"][day] = edited_df