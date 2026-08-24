# ----------------------------------------------------------------------
# importing 
# ----------------------------------------------------------------------
import streamlit as st
from datetime import date, datetime, timedelta
import os
import mysql.connector

# Keep the visual language compact on desktop and comfortable for touch on phones.
st.markdown(
    """
    <style>
    :root {
        --ink: #edf5f3;
        --muted: #b5c5c4;
        --accent: #39c6b5;
        --accent-soft: #183c3d;
        --warm: #f2a27b;
        --surface: #1c292d;
        --surface-alt: #223438;
        --page: #10191c;
        --line: #3d5658;
    }

    .stApp {
        background: var(--page);
        color: var(--ink);
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 940px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1 {
        color: var(--ink);
        font-family: "Trebuchet MS", sans-serif;
        font-size: 2rem !important;
        letter-spacing: 0;
        margin-bottom: 0.25rem !important;
    }

    h2 {
        color: var(--ink);
        font-size: 1.35rem !important;
        margin-top: 1.25rem !important;
    }

    h3 {
        color: var(--ink);
        font-size: 1.05rem !important;
    }

    [data-testid="stCaptionContainer"] {
        color: var(--muted);
    }

    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p,
    label,
    [data-testid="stWidgetLabel"] p {
        color: var(--ink);
    }

    [data-testid="stHorizontalBlock"] {
        gap: 0.75rem;
    }

    [data-testid="stDivider"] {
        margin: 1rem 0;
        border-color: var(--line);
    }

    [data-testid="stExpander"] {
        border: 1px solid var(--line);
        border-radius: 10px;
        background: var(--surface);
    }

    [data-testid="stExpander"] summary {
        color: var(--accent);
        font-weight: 600;
    }

    [data-testid="stExpander"] details {
        background: var(--surface);
    }

    .stButton > button {
        min-height: 2.5rem;
        border: 1px solid var(--line);
        border-radius: 8px;
        color: var(--ink);
        background: var(--surface-alt);
        font-weight: 600;
    }

    .stButton > button:hover {
        border-color: var(--accent);
        color: var(--accent);
    }

    [data-testid="stPills"] button[aria-checked="true"] {
        background: var(--accent) !important;
        border-color: var(--accent) !important;
        color: #071516 !important;
    }

    [data-testid="stPills"] button {
        min-height: 2.5rem;
        border: 1px solid var(--line) !important;
        border-radius: 8px;
        background: var(--surface-alt) !important;
        color: var(--ink) !important;
        white-space: nowrap;
    }

    [data-testid="stPills"] button:hover {
        border-color: var(--accent) !important;
        color: var(--accent) !important;
    }

    [data-baseweb="input"],
    [data-baseweb="select"],
    [data-baseweb="textarea"] {
        background: var(--surface-alt);
        border-color: var(--line);
    }

    input,
    textarea,
    [data-baseweb="select"] * {
        color: var(--ink) !important;
    }

    input::placeholder,
    textarea::placeholder {
        color: var(--muted) !important;
    }

    [data-testid="stSidebar"] {
        background: #172427;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        font-size: 1.25rem !important;
    }

    [data-testid="stSidebar"] [role="radiogroup"] label {
        color: var(--ink);
    }

    /* On small screens, let content use the full width and keep controls touchable. */
    @media (max-width: 640px) {
        [data-testid="stMainBlockContainer"] {
            padding: 1rem 0.85rem 2rem;
        }

        h1 {
            font-size: 1.65rem !important;
        }

        h2 {
            font-size: 1.2rem !important;
        }

        [data-testid="stHorizontalBlock"] {
            gap: 0.45rem;
        }

        [data-testid="stPills"] {
            overflow-x: auto;
            padding-bottom: 0.25rem;
        }

        [data-testid="stPills"] button {
            font-size: 0.8rem;
            padding: 0.35rem 0.55rem;
        }

        .stButton > button {
            min-height: 2.75rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ----------------------------------------------------------------------
# Database setup
# ----------------------------------------------------------------------

conn = mysql.connector.connect(
    host=os.environ["MYSQLHOST"],
    port=int(os.environ.get("MYSQLPORT", "3306")),
    user=os.environ["MYSQLUSER"],
    password=os.environ["MYSQLPASSWORD"],
    database=os.environ["MYSQLDATABASE"],
)


def execute(query, params=()):
    cursor = conn.cursor()
    cursor.execute(query, params)
    return cursor


def executemany(query, params):
    cursor = conn.cursor()
    cursor.executemany(query, params)
    return cursor


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
cursor = execute("SELECT COUNT(*) FROM categories")
category_count = cursor.fetchone()[0]

if category_count == 0:
    executemany(
        "INSERT INTO categories (name, emoji) VALUES (%s, %s)",
        default_categories
    )
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
    st.caption(f"Track how you spent your day — {selected_date.strftime('%d %B %Y')}")

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

                execute(
                    """
                    INSERT INTO categories (name, emoji)
                    VALUES (%s, %s)
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

        categories_to_delete = execute(
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

                    execute(
                        "DELETE FROM categories WHERE id = %s",
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

    cursor = execute(
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

            execute(
                """
                INSERT INTO activities
                (date, category, time, description)
                VALUES (%s, %s, %s, %s)
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

        st.caption("Tasks that need to be done on a specific date and time.")

        st.divider()

        st.subheader(
            f"Tasks for {selected_date.strftime('%d %B %Y')}"
        )

        # Get scheduled tasks for selected date
        scheduled_tasks = execute(
            """
            SELECT id, task, scheduled_time
            FROM tasks
            WHERE type = 'scheduled'
            AND scheduled_date = %s
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

                        execute(
                            """
                            UPDATE tasks
                            SET completed = 1,
                                completed_at = %s
                                WHERE id = %s
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
                    execute(
                        """
                        INSERT INTO tasks
                        (task, type, scheduled_date, scheduled_time)
                        VALUES (%s, %s, %s, %s)
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

        st.caption(
            "Tasks that can be done anytime but have a deadline."
        )

        st.divider()

        st.subheader("Active Deadlines")

        # Today's date
        today_date = date.today().isoformat()


        # Get active deadline tasks
        deadline_tasks = execute(
            """
            SELECT id, task, deadline
            FROM tasks
            WHERE type = 'deadline'
            AND completed = 0
            AND deadline >= %s
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

                        execute(
                            """
                            UPDATE tasks
                            SET completed = 1,
                                completed_at = %s
                                WHERE id = %s
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
                    execute(
                        """
                        INSERT INTO tasks
                        (task, type, deadline)
                        VALUES (%s, %s, %s)
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

        st.caption(
            "Tasks without a specific date or deadline."
        )

        st.divider()

        st.subheader("Your Flexible Tasks")

        flexible_tasks = execute(
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

                        execute(
                            """
                            UPDATE tasks
                            SET completed = 1,
                                completed_at = %s
                                WHERE id = %s
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
                    execute(
                        """
                        INSERT INTO tasks
                        (task, type)
                        VALUES (%s, %s)
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

    cursor = execute(
    """
    SELECT category, time, description
    FROM activities
    WHERE date = %s
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

    st.divider()
    st.subheader(
        f"Completed Tasks on {selected_date.strftime('%d %B %Y')}"
    )

    next_date = selected_date + timedelta(days=1)

    completed_tasks = execute(
        """
        SELECT task, type, scheduled_time, deadline, completed_at
        FROM tasks
        WHERE completed = 1
        AND completed_at >= %s
        AND completed_at < %s
        ORDER BY completed_at
        """,
        (
            selected_date.isoformat(),
            next_date.isoformat()
        )
    ).fetchall()

    if completed_tasks:

        for task_name, task_type, scheduled_time, deadline, completed_at in completed_tasks:

            completed_time = completed_at[11:16]
            task_details = ""

            if task_type == "scheduled" and scheduled_time:
                task_details = f" at {scheduled_time}"
            elif task_type == "deadline" and deadline:
                task_details = f" (due {deadline})"

            st.write(
                f"### ✅ {task_name}"
            )
            st.write(
                f"Completed at {completed_time}{task_details}"
            )

    else:

        st.info("No tasks completed on this date.")