# ----------------------------------------------------------------------
# importing 
# ----------------------------------------------------------------------
import streamlit as st
from datetime import date, datetime, timedelta
import os
import mysql.connector

st.set_page_config(
    page_title="Daily Tracker",
    page_icon="📅",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={"Get Help": None, "Report a bug": None, "About": None},
)

st.markdown(
    """
    <style>
    :root {
        --ink: #f4f7f5;
        --muted: #9eafad;
        --accent: #55d6c2;
        --accent-dark: #123a3b;
        --warm: #ff9c73;
        --surface: #18282c;
        --surface-alt: #20353a;
        --page: #0d181b;
        --line: #344d51;
    }

    .stApp {
        background: radial-gradient(circle at 100% 0%, rgba(85, 214, 194, 0.14), transparent 26rem),
            linear-gradient(135deg, #0d181b 0%, #102124 52%, #0d181b 100%);
        color: var(--ink);
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 820px;
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }

    h1 {
        color: var(--ink);
        font-family: Georgia, serif;
        font-size: 2.15rem !important;
        letter-spacing: 0;
        margin: 0 !important;
    }

    h2 {
        color: var(--ink);
        font-size: 1.25rem !important;
        margin-top: 1rem !important;
    }

    h3 {
        color: var(--ink);
        font-size: 1.05rem !important;
    }

    .date-badge {
        display: inline-block;
        margin: 0.2rem 0 0.5rem;
        padding: 0.25rem 0.7rem;
        border: 1px solid rgba(85, 214, 194, 0.35);
        border-radius: 999px;
        background: var(--accent-dark);
        color: var(--accent);
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.03em;
        animation: badge-in 420ms ease-out both;
    }

    @keyframes badge-in {
        from { opacity: 0; transform: translateY(-4px); }
        to { opacity: 1; transform: translateY(0); }
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
        gap: 0.55rem;
    }

    [data-testid="stDivider"] {
        margin: 0.75rem 0;
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
        min-height: 2.35rem;
        border: 1px solid var(--line);
        border-radius: 10px;
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
        min-height: 2.7rem;
        border: 1px solid var(--line) !important;
        border-radius: 999px;
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

    [data-testid="stDecoration"],
    footer {
        visibility: hidden;
        height: 0;
    }

    [data-testid="stSidebar"] {
        border-right: 1px solid var(--line);
    }

    .st-key-date-navigation [data-testid="stPills"] {
        width: 100%;
        min-width: 0;
        overflow: hidden;
    }

    .st-key-date-navigation [data-testid="stPills"] > div {
        flex-wrap: nowrap !important;
        width: 100%;
        justify-content: center;
    }

    .st-key-date-navigation [data-testid="stPills"] button {
        min-width: 0;
        min-height: 2.15rem;
        padding: 0.15rem 0.3rem;
        font-size: 0.73rem;
    }

    [data-testid="stSlider"] [role="slider"] {
        background: var(--warm);
        border-color: var(--warm);
        box-shadow: 0 0 0 5px rgba(255, 156, 115, 0.16);
    }

    [data-testid="stSlider"] [data-baseweb="slider"] > div > div:first-child {
        background: linear-gradient(90deg, var(--accent), var(--warm));
    }

    /* On small screens, let content use the full width and keep controls touchable. */
    @media (max-width: 640px) {
        [data-testid="stMainBlockContainer"] {
            padding: 1.5rem 0.75rem 1.5rem;
        }

        h1 {
            font-size: 1.8rem !important;
        }

        h2 {
            font-size: 1.2rem !important;
        }

        [data-testid="stHorizontalBlock"] {
            gap: 0.35rem;
        }

        [data-testid="stPills"] {
            width: 100%;
            overflow-x: auto;
            padding: 0.1rem 0 0.3rem;
            scrollbar-width: none;
        }

        [data-testid="stPills"] > div {
            flex-wrap: nowrap !important;
            width: 100%;
        }

        [data-testid="stPills"] button {
            flex: 0 0 auto;
            font-size: 0.82rem;
            padding: 0.35rem 0.7rem;
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

def get_database_setting(name):
    if name in st.secrets:
        return st.secrets[name]
    return os.environ[name]


conn = mysql.connector.connect(
    host=get_database_setting("MYSQLHOST"),
    port=int(st.secrets.get("MYSQLPORT", os.environ.get("MYSQLPORT", "3306"))),
    user=get_database_setting("MYSQLUSER"),
    password=get_database_setting("MYSQLPASSWORD"),
    database=get_database_setting("MYSQLDATABASE"),
    connection_timeout=10,
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
    for offset in range(3)
]

with st.container(key="date-navigation"):
    date_options = ["←"] + dates + ["→"]
    selected_option = st.pills(
        "Select a date",
        date_options,
        format_func=lambda value: (
            value if isinstance(value, str) else value.strftime("%a %d")
        ),
        default=st.session_state.selected_date,
        key=f"date_pills_{st.session_state.date_window_start}",
        label_visibility="collapsed",
        width="stretch",
    )

    if selected_option == "←":
        st.session_state.date_window_start -= timedelta(days=3)
        st.session_state.selected_date = (
            st.session_state.date_window_start + timedelta(days=1)
        )
        st.rerun()

    if selected_option == "→":
        st.session_state.date_window_start += timedelta(days=3)
        st.session_state.selected_date = (
            st.session_state.date_window_start + timedelta(days=1)
        )
        st.rerun()

    if isinstance(selected_option, date):
        st.session_state.selected_date = selected_option

selected_date = st.session_state.selected_date



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
    st.markdown(
        f'<div class="date-badge">{selected_date.strftime("%A, %d %B %Y")}</div>',
        unsafe_allow_html=True,
    )
    st.subheader("What did you do today?")
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

        time_spent = st.slider(
            "Time spent",
            min_value=0.0,
            max_value=24.0,
            value=0.0,
            step=0.5,
            format="%.1f h",
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