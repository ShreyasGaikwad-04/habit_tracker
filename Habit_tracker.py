# ----------------------------------------------------------------------
# importing 
# ----------------------------------------------------------------------
import streamlit as st
from datetime import date, timedelta
import sqlite3 


# ----------------------------------------------------------------------
# Database setup
# ----------------------------------------------------------------------

conn = sqlite3.connect("habit_tracker.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    time REAL,
    description TEXT
)
""")

conn.commit()

# ----------------------------------------------------------------------
# side bar
# ----------------------------------------------------------------------
st.sidebar.title("Daily Tracker")

page = st.sidebar.radio(
    "Go to",
    ["📝 Activities", "✅ To-Do List", "📜 History"]
)

# ----------------------------------------------------------------------
# Date selection
# ----------------------------------------------------------------------

today = date.today()

dates = [
    today - timedelta(days=2),
    today - timedelta(days=1),
    today,
    today + timedelta(days=1),
    today + timedelta(days=2)
]

selected_date = st.pills(
    "Select a date",
    dates,
    format_func=lambda x: x.strftime("%a, %d %b"),
    default=today
)



# ----------------------------------------------------------------------
# Page Title
# ----------------------------------------------------------------------
# st.title("📅 Habit Tracker")
# st.write("Track how you spend your day.")


# ----------------------------------------------------------------------
# Categories page
# ----------------------------------------------------------------------
#categories
if page == "📝 Activities":
    
    st.title("📅 Daily Tracker")
    st.write(f"Track how you spent your day — {selected_date.strftime('%d %B %Y')}")

    st.subheader("What did you do today? 🤷")

    # Study
    study = st.checkbox("📚 Study")

    if study:
        st.write("### 📚 Study")

        study_time = st.number_input(
            "Time spent (hours)",
            min_value=0.0,
            step=0.5,
            key="study_time"
        )

        study_description = st.text_area(
            "What did you study?",
            key="study_description"
        )


    # Coding
    coding = st.checkbox("💻 Coding")

    if coding:
        st.write("### 💻 Coding")

        coding_time = st.number_input(
            "Time spent (hours)",
            min_value=0.0,
            step=0.5,
            key="coding_time"
        )

        coding_description = st.text_area(
            "What did you code?",
            key="coding_description"
        )


    # Exercise
    exercise = st.checkbox("🏃 Exercise")

    if exercise:
        st.write("### 🏃 Exercise")

        exercise_time = st.number_input(
            "Time spent (hours)",
            min_value=0.0,
            step=0.5,
            key="exercise_time"
        )

        exercise_description = st.text_area(
            "What exercise did you do?",
            key="exercise_description"
        )


    # Playing
    playing = st.checkbox("🎮 Playing")

    if playing:
        st.write("### 🎮 Playing")

        playing_time = st.number_input(
            "Time spent (hours)",
            min_value=0.0,
            step=0.5,
            key="playing_time"
        )

        playing_description = st.text_area(
            "What did you play?",
            key="playing_description"
        )


    # Entertainment
    entertainment = st.checkbox("🎬 Entertainment")

    if entertainment:
        st.write("### 🎬 Entertainment")

        entertainment_time = st.number_input(
            "Time spent (hours)",
            min_value=0.0,
            step=0.5,
            key="entertainment_time"
        )

        entertainment_description = st.text_area(
            "What did you watch/do?",
            key="entertainment_description"
        )


    # Social
    social = st.checkbox("👥 Social")

    if social:
        st.write("### 👥 Social")

        social_time = st.number_input(
            "Time spent (hours)",
            min_value=0.0,
            step=0.5,
            key="social_time"
        )

        social_description = st.text_area(
            "What did you do?",
            key="social_description"
        )


    # Reading
    reading = st.checkbox("📖 Reading")

    if reading:
        st.write("### 📖 Reading")

        reading_time = st.number_input(
            "Time spent (hours)",
            min_value=0.0,
            step=0.5,
            key="reading_time"
        )

        reading_description = st.text_area(
            "What did you read?",
            key="reading_description"
        )


    if st.button("💾 Save Activities"):

        activities = []

        if study:
            activities.append({
                "date": selected_date,
                "category": "Study",
                "time": study_time,
                "description": study_description
            })

        if coding:
            activities.append({
                "date": selected_date,
                "category": "Coding",
                "time": coding_time,
                "description": coding_description
            })

        if exercise:
            activities.append({
                "date": selected_date,
                "category": "Exercise",
                "time": exercise_time,
                "description": exercise_description
            })

        for activity in activities:

            conn.execute(
                """
                INSERT INTO activities (date, category, time, description)
                VALUES (?, ?, ?, ?)
                """,
                (
                    activity["date"].isoformat(),
                    activity["category"],
                    activity["time"],
                    activity["description"]
                )
            )

        conn.commit()

        st.success("Activities saved successfully! 🎉")





# ----------------------------------------------------------------------
# TODOLIST page
# ----------------------------------------------------------------------
elif page == "✅ To-Do List":

    st.title("✅ To-Do List")


# ----------------------------------------------------------------------
# History page
# ----------------------------------------------------------------------
elif page == "📜 History":

    st.title("📜 History")

    cursor = conn.execute(
    """
    SELECT category, time, description
    FROM activities
    WHERE date = ?
    """,
    (selected_date.isoformat(),)
    )

    activities = cursor.fetchall()

    if activities:

        st.subheader(
            f"Activities on {selected_date.strftime('%d %B %Y')}"
        )

        total_time = 0

        for category, time, description in activities:

            st.write(f"### {category}")
            st.write(f"⏱️ {time} hours")
            st.write(description)

            total_time += time

        st.divider()
        st.write(f"**⏱️ Total time: {total_time} hours**")

    else:

        st.info("No activities recorded for this date.")