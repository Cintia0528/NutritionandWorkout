import streamlit as st
import pandas as pd
from datetime import date, timedelta

st.set_page_config(page_title="Gym & Nutrition Tracker", layout="wide")

# --------- Helper functions ----------
def generate_weekdays(start_date, weeks=4):
    """Generate a list of workout dates (Mon-Fri) for given weeks."""
    all_dates = []
    for w in range(weeks):
        week_start = start_date + timedelta(weeks=w)
        for i in range(5):  # Mon-Fri
            all_dates.append(week_start + timedelta(days=i))
    return all_dates

def make_workout_table(exercises, workout_dates):
    """Create a workout progression table."""
    columns = ["Exercise"] + [d.strftime("%Y-%m-%d") for d in workout_dates]
    data = {col: ["" for _ in exercises] for col in columns}
    data["Exercise"] = exercises
    return pd.DataFrame(data)

# --------- Data ----------
start_date = date(2025, 9, 22)   # Monday, Sep 22
weeks = 4
all_dates = generate_weekdays(start_date, weeks)

# Map workout days to weekdays
weekday_mapping = {
    0: "Day 1 – Back + Shoulders",   # Monday
    1: "Day 2 – Legs + Glutes (Hip Hinge)",  # Tuesday
    2: "Day 3 – Chest + Arms",       # Wednesday
    3: "Day 4 – Legs + Glutes (Squat Focus)", # Thursday
    4: "Day 5 – Back + Triceps"      # Friday
}

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
        for weekday, day_name in weekday_mapping.items():
            # filter dates matching the weekday
            day_dates = [d for d in all_dates if d.weekday() == weekday]
            exercises = workout_plan[day_name]
            st.session_state["workouts"][day_name] = make_workout_table(exercises, day_dates)
    
    for day, df in st.session_state["workouts"].items():
        st.subheader(day)
        edited_df = st.data_editor(df, num_rows="dynamic", key=day)
        st.session_state["workouts"][day] = edited_df
