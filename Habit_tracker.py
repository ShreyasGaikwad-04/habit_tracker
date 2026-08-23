# ----------------------------------------------------------------------
# importing 
# ----------------------------------------------------------------------
import streamlit as st
from datetime import date, datetime, timedelta
import sqlite3 


# ----------------------------------------------------------------------
# Database setup
# ----------------------------------------------------------------------

conn = sqlite3.connect("habit_tracker.db")

# Activities table
conn.execute("""
CREATE TABLE IF NOT EXISTS activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    time REAL,
    description TEXT
)
""")

# Categories table
conn.execute("""
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    emoji TEXT NOT NULL
)
""")

conn.commit()


# Default categories
default_categories = [
    ("Study", "📚"),
    ("Coding", "💻"),
    ("Exercise", "🏃"),
    ("Playing", "🎮"),
    ("Entertainment", "🎬"),
    ("Social", "👥"),
    ("Reading", "📖")
]

# Add default categories only if there are no categories yet
cursor = conn.execute("SELECT COUNT(*) FROM categories")
category_count = cursor.fetchone()[0]

if category_count == 0:
    conn.executemany(
        "INSERT INTO categories (name, emoji) VALUES (?, ?)",
        default_categories
    )
    conn.commit()


# Tasks table
conn.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    type TEXT NOT NULL,
    scheduled_date TEXT,
    scheduled_time TEXT,
    deadline TEXT,
    completed INTEGER DEFAULT 0,
    completed_at TEXT
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

if "date_window_start" not in st.session_state:
    st.session_state.date_window_start = today - timedelta(days=2)

if "selected_date" not in st.session_state:
    st.session_state.selected_date = today

dates = [
    st.session_state.date_window_start + timedelta(days=offset)
    for offset in range(5)
]

previous_col, dates_col, next_col = st.columns([0.6, 10, 0.6])

with previous_col:
    if st.button("←", key="previous_dates"):
        st.session_state.date_window_start -= timedelta(days=5)
        st.session_state.selected_date = (
            st.session_state.date_window_start + timedelta(days=2)
        )
        st.rerun()

with dates_col:
    selected_date = st.pills(
        "Select a date",
        dates,
        format_func=lambda x: x.strftime("%a, %d %b"),
        default=st.session_state.selected_date,
        key=f"date_pills_{st.session_state.date_window_start}",
        label_visibility="collapsed",
        width="stretch"
    )

st.session_state.selected_date = selected_date

with next_col:
    if st.button("→", key="next_dates"):
        st.session_state.date_window_start += timedelta(days=5)
        st.session_state.selected_date = (
            st.session_state.date_window_start + timedelta(days=2)
        )
        st.rerun()



# ----------------------------------------------------------------------
# Page Title
# ----------------------------------------------------------------------
# st.title("📅 Habit Tracker")
# st.write("Track how you spend your day.")


# ----------------------------------------------------------------------
# Categories page
# ----------------------------------------------------------------------

if page == "📝 Activities":
    
    st.title("📅 Daily Tracker")
    st.write(f"Track how you spent your day — {selected_date.strftime('%d %B %Y')}")

    st.subheader("What did you do today? 🤷")

    st.divider()

    st.subheader("⚙️ Manage Categories")

    # --------------------------------------------
    # add category
    # --------------------------------------------
    with st.expander("➕ Add Category"):

        new_category_name = st.text_input(
            "Category name",
            placeholder="e.g. Music"
        )

        new_category_emoji = st.text_input(
            "Emoji",
            placeholder="e.g. 🎵"
        )

        if st.button("Add Category"):

            if new_category_name and new_category_emoji:

                conn.execute(
                    """
                    INSERT INTO categories (name, emoji)
                    VALUES (?, ?)
                    """,
                    (new_category_name, new_category_emoji)
                )

                conn.commit()

                st.success(
                    f"{new_category_emoji} {new_category_name} added!"
                )

                st.rerun()

            else:

                st.warning("Please enter both a name and an emoji.")

    # --------------------------------------------
    # Delete category
    # --------------------------------------------
    with st.expander("🗑️ Delete Category"):

        categories_to_delete = conn.execute(
            "SELECT id, name, emoji FROM categories"
        ).fetchall()

        category_options = {
            category_id: f"{emoji} {name}"
            for category_id, name, emoji in categories_to_delete
        }

        category_id = st.selectbox(
            "Select category to delete",
            options=category_options.keys(),
            format_func=lambda x: category_options[x]
        )

        if st.button("Delete Category"):

            st.session_state["confirm_delete"] = True


        # Confirmation
        if st.session_state.get("confirm_delete", False):

            selected_name = category_options[category_id]

            st.warning(
                f"Are you sure you want to delete {selected_name}?\n\n"
                "This will remove it from future activities, "
                "but your previous activity history will remain."
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Yes, Delete"):

                    conn.execute(
                        "DELETE FROM categories WHERE id = ?",
                        (category_id,)
                    )

                    conn.commit()

                    st.session_state["confirm_delete"] = False

                    st.success(f"{selected_name} deleted!")

                    st.rerun()

            with col2:
                if st.button("Cancel"):

                    st.session_state["confirm_delete"] = False

                    st.rerun()

    # --------------------------------------------
    # Get categories from database
    # --------------------------------------------

    cursor = conn.execute(
        "SELECT id, name, emoji FROM categories"
    )

    categories = cursor.fetchall()


    
    # --------------------------------------------
    # Display categories
    # --------------------------------------------

    selected_categories = []

    for category_id, name, emoji in categories:

        selected = st.checkbox(
            f"{emoji} {name}",
            key=f"category_{category_id}"
        )

        if selected:
            selected_categories.append(
                (category_id, name, emoji)
            )


    
    # --------------------------------------------
    # Show inputs for selected categories
    # --------------------------------------------
    activity_data = []

    for category_id, name, emoji in selected_categories:

        st.write(f"### {emoji} {name}")

        time_spent = st.number_input(
            "Time spent (hours)",
            min_value=0.0,
            step=0.5,
            key=f"time_{category_id}"
        )

        description = st.text_area(
            f"What did you do in {name}?",
            key=f"description_{category_id}"
        )

        activity_data.append({
            "category": name,
            "time": time_spent,
            "description": description
        })


    if st.button("💾 Save Activities"):

        for activity in activity_data:

            conn.execute(
                """
                INSERT INTO activities
                (date, category, time, description)
                VALUES (?, ?, ?, ?)
                """,
                (
                    selected_date.isoformat(),
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

    # -----------------------------------
    # To-Do type pills
    # -----------------------------------

    todo_type = st.pills(
        "Task type",
        ["📅 Scheduled", "⏰ Deadline", "📌 Flexible"],
        default="📅 Scheduled"
    )


    # ===================================
    # 📅 SCHEDULED TASKS
    # ===================================

    if todo_type == "📅 Scheduled":

        st.subheader("📅 Scheduled Tasks")

        st.write("Tasks that need to be done on a specific date and time.")

        st.divider()

        st.subheader(
            f"Tasks for {selected_date.strftime('%d %B %Y')}"
        )

        # Get scheduled tasks for selected date
        scheduled_tasks = conn.execute(
            """
            SELECT id, task, scheduled_time
            FROM tasks
            WHERE type = 'scheduled'
            AND scheduled_date = ?
            AND completed = 0
            ORDER BY scheduled_time
            """,
            (selected_date.isoformat(),)
        ).fetchall()


        if scheduled_tasks:

            for task_id, task_name, task_time in scheduled_tasks:

                col1, col2 = st.columns([5, 1])

                with col1:

                    st.write(
                        f"☐ **{task_name}** — {task_time}"
                    )

                with col2:

                    if st.button(
                        "Done",
                        key=f"done_scheduled_{task_id}"
                    ):

                        conn.execute(
                            """
                            UPDATE tasks
                            SET completed = 1,
                                completed_at = ?
                            WHERE id = ?
                            """,
                            (
                                datetime.now().isoformat(),
                                task_id
                            )
                        )

                        conn.commit()

                        st.rerun()

        else:

            st.info("No scheduled tasks for this date.")

        with st.expander("➕ Add Task"):
            task = st.text_input(
                "Task",
                placeholder="e.g. Gym",
                key="scheduled_task"
            )

            scheduled_date = st.date_input(
                "Date",
                value=selected_date,
                key="scheduled_date"
            )

            scheduled_time = st.time_input(
                "Time",
                key="scheduled_time"
            )

            if st.button("Save Task", key="save_scheduled_task"):
                if task.strip():
                    conn.execute(
                        """
                        INSERT INTO tasks
                        (task, type, scheduled_date, scheduled_time)
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            task.strip(),
                            "scheduled",
                            scheduled_date.isoformat(),
                            scheduled_time.strftime("%H:%M")
                        )
                    )
                    conn.commit()
                    st.success("Scheduled task added! 🎉")
                    st.rerun()
                else:
                    st.warning("Please enter a task.")


    # ===================================
    # ⏰ DEADLINE TASKS
    # ===================================

    elif todo_type == "⏰ Deadline":

        st.subheader("⏰ Deadline Tasks")

        st.write(
            "Tasks that can be done anytime but have a deadline."
        )

        st.divider()

        st.subheader("Active Deadlines")

        # Today's date
        today_date = date.today().isoformat()


        # Get active deadline tasks
        deadline_tasks = conn.execute(
            """
            SELECT id, task, deadline
            FROM tasks
            WHERE type = 'deadline'
            AND completed = 0
            AND deadline >= ?
            ORDER BY deadline
            """,
            (today_date,)
        ).fetchall()


        if deadline_tasks:

            for task_id, task_name, task_deadline in deadline_tasks:

                col1, col2 = st.columns([5, 1])

                with col1:

                    st.write(
                        f"☐ **{task_name}** — "
                        f"Due {task_deadline}"
                    )

                with col2:

                    if st.button(
                        "Done",
                        key=f"done_deadline_{task_id}"
                    ):

                        conn.execute(
                            """
                            UPDATE tasks
                            SET completed = 1,
                                completed_at = ?
                            WHERE id = ?
                            """,
                            (
                                datetime.now().isoformat(),
                                task_id
                            )
                        )

                        conn.commit()

                        st.rerun()

        else:

            st.info("No active deadline tasks.")

        with st.expander("➕ Add Task"):
            task = st.text_input(
                "Task",
                placeholder="e.g. Submit assignment",
                key="deadline_task"
            )

            deadline = st.date_input(
                "Deadline",
                value=selected_date,
                key="deadline_date"
            )

            if st.button("Save Task", key="save_deadline_task"):
                if task.strip():
                    conn.execute(
                        """
                        INSERT INTO tasks
                        (task, type, deadline)
                        VALUES (?, ?, ?)
                        """,
                        (
                            task.strip(),
                            "deadline",
                            deadline.isoformat()
                        )
                    )
                    conn.commit()
                    st.success("Deadline task added! 🎉")
                    st.rerun()
                else:
                    st.warning("Please enter a task.")


    # ===================================
    # 📌 FLEXIBLE TASKS
    # ===================================

    elif todo_type == "📌 Flexible":

        st.subheader("📌 Flexible Tasks")

        st.write(
            "Tasks without a specific date or deadline."
        )

        st.divider()

        st.subheader("Your Flexible Tasks")

        flexible_tasks = conn.execute(
            """
            SELECT id, task
            FROM tasks
            WHERE type = 'flexible'
            AND completed = 0
            ORDER BY id
            """
        ).fetchall()


        if flexible_tasks:

            for task_id, task_name in flexible_tasks:

                col1, col2 = st.columns([5, 1])

                with col1:

                    st.write(
                        f"☐ **{task_name}**"
                    )

                with col2:

                    if st.button(
                        "Done",
                        key=f"done_flexible_{task_id}"
                    ):

                        conn.execute(
                            """
                            UPDATE tasks
                            SET completed = 1,
                                completed_at = ?
                            WHERE id = ?
                            """,
                            (
                                datetime.now().isoformat(),
                                task_id
                            )
                        )

                        conn.commit()

                        st.rerun()

        else:

            st.info("No flexible tasks.")

        with st.expander("➕ Add Task"):
            task = st.text_input(
                "Task",
                placeholder="e.g. Learn Docker",
                key="flexible_task"
            )

            if st.button("Save Task", key="save_flexible_task"):
                if task.strip():
                    conn.execute(
                        """
                        INSERT INTO tasks
                        (task, type)
                        VALUES (?, ?)
                        """,
                        (
                            task.strip(),
                            "flexible"
                        )
                    )
                    conn.commit()
                    st.success("Flexible task added! 🎉")
                    st.rerun()
                else:
                    st.warning("Please enter a task.")

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