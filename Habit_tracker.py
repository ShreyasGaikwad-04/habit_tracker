# ----------------------------------------------------------------------
# importing 
# ----------------------------------------------------------------------
import streamlit as st
from datetime import date, datetime, timedelta
import os
import mysql.connector
import plotly.graph_objects as go

st.set_page_config(
    page_title="Daily Tracker",
    page_icon="📅",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={"Get Help": None, "Report a bug": None, "About": None},
)

if not st.user.is_logged_in:
    st.title("📅 Daily Tracker")
    st.write("Sign in with Google to continue.")
    st.button(
        "Continue with Google",
        on_click=st.login,
        args=("google",),
    )
    st.stop()

allowed_emails = {
    "shreyasgaikwad004@gmail.com": True,
    # "another@gmail.com": True,
}
user_email = (st.user.email or "").strip().lower()

if user_email not in allowed_emails:
    st.error("This Google account is not authorized to use this app.")
    st.logout()
    st.stop()

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
        padding-top: 2rem;
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

    .analytics-summary {
        display: grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        gap: 0.6rem;
        margin: 0.35rem 0 0.7rem;
    }

    .analytics-stat {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        min-width: 0;
        min-height: 86px;
        padding: 0.75rem 0.85rem;
        border: 1px solid var(--line);
        border-radius: 10px;
        background: linear-gradient(145deg, rgba(32, 53, 58, 0.95), rgba(24, 40, 44, 0.95));
    }

    .analytics-stat > span {
        flex: 0 1 auto;
        color: var(--muted);
        font-size: 0.74rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }

    .analytics-stat > strong {
        flex: 0 1 auto;
        overflow-wrap: anywhere;
        margin-left: auto;
        color: var(--accent);
        font-size: 1.25rem;
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
            padding: 3rem 0.75rem 1.5rem;
        }

        h1 {
            font-size: 1.8rem !important;
        }

        h2 {
            font-size: 1.2rem !important;
        }

        .analytics-summary {
            grid-template-columns: repeat(2, minmax(0, 1fr));
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


def ensure_activities_category_id_column():
    column = execute("SHOW COLUMNS FROM activities LIKE 'category_id'").fetchone()
    if column is None:
        execute("ALTER TABLE activities ADD COLUMN category_id INT NULL")
        conn.commit()

    legacy_rows = execute(
        """
        SELECT id, user_id, category
        FROM activities
        WHERE category_id IS NULL AND category IS NOT NULL
        """
    ).fetchall()

    for activity_id, activity_user_id, legacy_category_name in legacy_rows:
        category_row = execute(
            """
            SELECT id
            FROM categories
            WHERE user_id = %s AND name = %s
            LIMIT 1
            """,
            (activity_user_id, legacy_category_name),
        ).fetchone()

        if category_row is not None:
            execute(
                "UPDATE activities SET category_id = %s WHERE id = %s",
                (category_row[0], activity_id),
            )

    conn.commit()


ensure_activities_category_id_column()

google_subject = st.user.sub
user_name = getattr(st.user, "name", "")

user_record = execute(
    "SELECT id FROM users WHERE google_subject = %s",
    (google_subject,),
).fetchone()

if user_record is None:
    execute(
        """
        INSERT INTO users (google_subject, email, name)
        VALUES (%s, %s, %s)
        """,
        (google_subject, user_email, user_name),
    )
    conn.commit()
    user_record = execute(
        "SELECT id FROM users WHERE google_subject = %s",
        (google_subject,),
    ).fetchone()
else:
    execute(
        """
        UPDATE users
        SET email = %s, name = %s
        WHERE id = %s
        """,
        (user_email, user_name, user_record[0]),
    )
    conn.commit()

user_id = user_record[0]


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

# Add default categories only if this user has no categories yet
cursor = execute(
    "SELECT COUNT(*) FROM categories WHERE user_id = %s",
    (user_id,),
)
category_count = cursor.fetchone()[0]

if category_count == 0:
    executemany(
        "INSERT INTO categories (user_id, name, emoji) VALUES (%s, %s, %s)",
        [(user_id, name, emoji) for name, emoji in default_categories],
    )
    conn.commit()


# ----------------------------------------------------------------------
# side bar
# ----------------------------------------------------------------------
st.sidebar.title("Daily Tracker")
st.sidebar.caption(f"Signed in as {st.user.email}")

if st.sidebar.button("Log out"):
    st.logout()

page = st.sidebar.radio(
    "Go to",
    ["📝 Activities", "✅ To-Do List", "📜 History", "📊 Analytics"]
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

if page != "📊 Analytics":
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

if page == "📊 Analytics":

    st.title("📊 Analytics")
    period_type = st.pills(
        "View by", ["Weekly", "Monthly"], default="Weekly",
        key="analytics_period_type", label_visibility="collapsed", width="stretch",
    )
    chosen_date = st.date_input(
        "Choose a date in the period", value=today,
        key=f"analytics_{period_type.lower()}_date", label_visibility="collapsed",
    )

    if period_type == "Weekly":
        period_start = chosen_date - timedelta(days=chosen_date.weekday())
        period_end = period_start + timedelta(days=6)
        period_label = f"{period_start.strftime('%d %b')} - {period_end.strftime('%d %b %Y')}"
        chart_dates = [period_start + timedelta(days=index) for index in range(7)]
    else:
        period_start = chosen_date.replace(day=1)
        next_period = date(period_start.year + 1, 1, 1) if period_start.month == 12 else date(period_start.year, period_start.month + 1, 1)
        period_end = next_period - timedelta(days=1)
        period_label = period_start.strftime("%B %Y")
        chart_dates = [period_start + timedelta(days=index) for index in range((period_end - period_start).days + 1)]

    st.caption(period_label)

    activity_rows = execute(
        """
        SELECT a.date, c.name, a.time
        FROM activities a
        LEFT JOIN categories c ON c.id = a.category_id
        WHERE a.user_id = %s AND a.date BETWEEN %s AND %s
        ORDER BY a.date
        """,
        (user_id, period_start.isoformat(), period_end.isoformat()),
    ).fetchall()

    if not activity_rows:
        st.info(f"No time logged for {period_label}. Add an activity in this period to see your analytics.")
    else:
        daily_totals = {activity_date: 0.0 for activity_date in chart_dates}
        category_totals = {}
        daily_category_totals = {activity_date: {} for activity_date in chart_dates}

        for activity_date, category_name, logged_time in activity_rows:
            activity_date = activity_date.date() if isinstance(activity_date, datetime) else activity_date
            category_name = category_name or "Unknown"
            logged_time = float(logged_time or 0)
            daily_totals[activity_date] += logged_time
            category_totals[category_name] = category_totals.get(category_name, 0.0) + logged_time
            daily_category_totals[activity_date][category_name] = daily_category_totals[activity_date].get(category_name, 0.0) + logged_time

        total_logged = sum(daily_totals.values())
        average_per_day = total_logged / len(chart_dates)
        top_categories = sorted(category_totals.items(), key=lambda item: item[1], reverse=True)
        visible_categories = [category for category, _ in top_categories[:4]]
        if len(top_categories) > 4:
            visible_categories.append("Others")

        colors = ["#55d6c2", "#ff9c73", "#8fb8ff", "#f3c969", "#ad8de2"]
        top_category, top_category_hours = top_categories[0]
        peak_date, peak_hours = max(daily_totals.items(), key=lambda item: item[1])
        st.markdown(
            f'''<div class="analytics-summary">
                <div class="analytics-stat"><span>Total logged</span><strong>{total_logged:.1f} h</strong></div>
                <div class="analytics-stat"><span>Average per day</span><strong>{average_per_day:.1f} h</strong></div>
                <div class="analytics-stat"><span>Top category</span><strong>{top_category} · {top_category_hours:.1f} h</strong></div>
                <div class="analytics-stat"><span>Peak day</span><strong>{peak_date.strftime('%a')} · {peak_hours:.1f} h</strong></div>
            </div>''', unsafe_allow_html=True,
        )

        bar_figure = go.Figure()
        for color_index, category in enumerate(visible_categories):
            values = []
            for activity_date in chart_dates:
                if category == "Others":
                    value = sum(daily_category_totals[activity_date].get(name, 0.0) for name, _ in top_categories[4:])
                else:
                    value = daily_category_totals[activity_date].get(category, 0.0)
                values.append(value)
            bar_figure.add_trace(go.Bar(
                name=category, x=[activity_date.strftime("%a %d") for activity_date in chart_dates], y=values,
                marker_color=colors[color_index], hoverinfo="skip",
            ))
        bar_figure.update_layout(
            barmode="stack", height=300, margin=dict(l=0, r=0, t=10, b=70),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f4f7f5"),
            legend=dict(
                orientation="h",
                y=-0.18,
                yanchor="top",
                x=0.5,
                xanchor="center",
                itemsizing="constant",
            ),
            xaxis=dict(showgrid=False),
            yaxis=dict(title="Hours", gridcolor="#344d51"),
        )
        st.plotly_chart(bar_figure, width="stretch", config={"staticPlot": True, "displayModeBar": False})

        donut_labels = [category for category, _ in top_categories[:4]]
        donut_values = [hours for _, hours in top_categories[:4]]
        if len(top_categories) > 4:
            donut_labels.append("Others")
            donut_values.append(sum(hours for _, hours in top_categories[4:]))
        donut_figure = go.Figure(go.Pie(
            labels=donut_labels, values=donut_values, hole=0.62,
            marker=dict(colors=colors[:len(donut_labels)]), textinfo="percent", hoverinfo="skip",
        ))
        donut_figure.update_layout(
            height=330, margin=dict(l=0, r=0, t=12, b=0), paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f4f7f5"), legend=dict(orientation="h", y=-0.05), showlegend=True,
        )
        st.plotly_chart(donut_figure, width="stretch", config={"staticPlot": True, "displayModeBar": False})

        if len(top_categories) > 4:
            other_category_names = [name for name, _ in top_categories[4:]]
            st.caption(f"Other categories: {', '.join(other_category_names)}")

elif page == "📝 Activities":
    
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

        with st.form("add_category_form"):
            new_category_name = st.text_input(
                "Category name",
                placeholder="e.g. Music"
            )
            new_category_emoji = st.text_input(
                "Emoji",
                placeholder="e.g. 🎵"
            )
            add_category = st.form_submit_button("Add Category")

        if add_category:

            if new_category_name.strip() and new_category_emoji.strip():

                execute(
                    """
                    INSERT INTO categories (user_id, name, emoji)
                    VALUES (%s, %s, %s)
                    """,
                    (user_id, new_category_name.strip(), new_category_emoji.strip())
                )

                conn.commit()

                st.success(
                    f"{new_category_emoji} {new_category_name} added!"
                )

                st.rerun()

            else:

                st.warning("Please enter both a name and an emoji.")

    categories = execute(
        "SELECT id, name, emoji FROM categories WHERE user_id = %s",
        (user_id,)
    ).fetchall()

    with st.expander("⚙️ Manage Existing Categories"):
        for category_id, name, emoji in categories:
            category_col, rename_col, delete_col = st.columns([5, 1, 1])

            with category_col:
                st.write(f"{emoji} {name}")

            with rename_col:
                if st.button("Rename", key=f"rename_category_{category_id}"):
                    st.session_state["rename_category_id"] = category_id
                    st.rerun()

            with delete_col:
                if st.button("Delete", key=f"delete_category_{category_id}"):
                    st.session_state["delete_category_id"] = category_id
                    st.rerun()

            if st.session_state.get("rename_category_id") == category_id:
                with st.form(key=f"rename_category_form_{category_id}"):
                    renamed_category_name = st.text_input(
                        "New category name",
                        value=name,
                    )
                    save_rename, cancel_rename = st.columns(2)
                    with save_rename:
                        rename_submitted = st.form_submit_button("Save Name")
                    with cancel_rename:
                        rename_cancelled = st.form_submit_button("Cancel")

                if rename_submitted:
                    if renamed_category_name.strip():
                        execute(
                            """
                            UPDATE categories
                            SET name = %s
                            WHERE id = %s AND user_id = %s
                            """,
                            (renamed_category_name.strip(), category_id, user_id)
                        )
                        conn.commit()
                        st.session_state.pop("rename_category_id", None)
                        st.rerun()
                    else:
                        st.warning("Please enter a category name.")

                if rename_cancelled:
                    st.session_state.pop("rename_category_id", None)
                    st.rerun()

            if st.session_state.get("delete_category_id") == category_id:
                st.warning(
                    f"Delete {emoji} {name}? Previous activity history will remain."
                )
                confirm_delete, cancel_delete = st.columns(2)
                with confirm_delete:
                    delete_confirmed = st.button(
                        "Yes, Delete",
                        key=f"confirm_delete_category_{category_id}",
                    )
                with cancel_delete:
                    delete_cancelled = st.button(
                        "Cancel",
                        key=f"cancel_delete_category_{category_id}",
                    )

                if delete_confirmed:
                    execute(
                        "DELETE FROM categories WHERE id = %s AND user_id = %s",
                        (category_id, user_id)
                    )
                    conn.commit()
                    st.session_state.pop("delete_category_id", None)
                    st.rerun()

                if delete_cancelled:
                    st.session_state.pop("delete_category_id", None)
                    st.rerun()

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
            "category_id": category_id,
            "category_name": name,
            "time": time_spent,
            "description": description
        })


    if st.button("💾 Save Activities"):

        for activity in activity_data:

            execute(
                """
                INSERT INTO activities
                (user_id, date, category, category_id, time, description)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    user_id,
                    selected_date.isoformat(),
                    activity["category_name"],
                    activity["category_id"],
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
        ["📌 Flexible", "⏰ Deadline", "📅 Scheduled"],
        default="📌 Flexible"
    )

    # ===================================
    # 📅 SCHEDULED TASKS
    # ===================================

    if todo_type == "📅 Scheduled":

        st.caption("Tasks that need to be done on a specific date and time.")

        st.subheader(
            f"Tasks for {selected_date.strftime('%d %B %Y')}"
        )

        scheduled_tasks = execute(
            """
            SELECT id, task, scheduled_time
            FROM tasks
            WHERE user_id = %s
            AND type = 'scheduled'
            AND scheduled_date = %s
            AND completed = 0
            ORDER BY scheduled_time
            """,
            (user_id, selected_date.isoformat())
        ).fetchall()

        if scheduled_tasks:
            for task_id, task_name, task_time in scheduled_tasks:
                col1, col2 = st.columns([5, 1])

                with col1:
                    st.write(f"✅ **{task_name}** — {task_time}")

                with col2:
                    if st.button("Done", key=f"done_scheduled_{task_id}"):
                        execute(
                            """
                            UPDATE tasks
                            SET completed = 1, completed_at = %s
                            WHERE id = %s AND user_id = %s
                            """,
                            (datetime.now().isoformat(), task_id, user_id)
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
            scheduled_time = st.time_input("Time", key="scheduled_time")

            if st.button("Save Task", key="save_scheduled_task"):
                if task.strip():
                    execute(
                        """
                        INSERT INTO tasks
                        (user_id, task, type, scheduled_date, scheduled_time)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            user_id,
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

    elif todo_type == "⏰ Deadline":

        st.caption("Tasks that can be done anytime but have a deadline.")

        st.subheader("Active Deadlines")

        # Today's date
        today_date = date.today().isoformat()


        # Get active deadline tasks
        deadline_tasks = execute(
            """
            SELECT id, task, deadline
            FROM tasks
            WHERE user_id = %s
            AND type = 'deadline'
            AND completed = 0
            AND deadline >= %s
            ORDER BY deadline
            """,
            (user_id, today_date)
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
                                AND user_id = %s
                            """,
                            (
                                datetime.now().isoformat(),
                                task_id,
                                user_id
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
                        (user_id, task, type, deadline)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (
                            user_id,
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

        st.caption("Tasks without a specific date or deadline.")

        st.subheader("Your Flexible Tasks")

        flexible_tasks = execute(
            """
            SELECT id, task
            FROM tasks
            WHERE user_id = %s
            AND type = 'flexible'
            AND completed = 0
            ORDER BY id
            """,
            (user_id,)
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
                                AND user_id = %s
                            """,
                            (
                                datetime.now().isoformat(),
                                task_id,
                                user_id
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
                        (user_id, task, type)
                        VALUES (%s, %s, %s)
                        """,
                        (
                            user_id,
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
    SELECT a.id, c.name, a.time, a.description
    FROM activities a
    LEFT JOIN categories c ON c.id = a.category_id
    WHERE a.user_id = %s
    AND a.date = %s
    ORDER BY a.id DESC
    """,
    (user_id, selected_date.isoformat())
    )

    activities = cursor.fetchall()

    if activities:

        st.subheader(
            f"Activities on {selected_date.strftime('%d %B %Y')}"
        )

        total_time = 0

        for activity_id, category_name, time, description in activities:
            category_label = category_name or "Unknown"

            activity_col, delete_col = st.columns([5, 1])

            with activity_col:
                st.write(f"### {category_label}")
                st.write(f"⏱️ {time} hours")
                if description:
                    st.write(description)

            with delete_col:
                if st.button(
                    "Delete",
                    key=f"delete_activity_{activity_id}"
                ):
                    st.session_state["confirm_activity_delete_id"] = activity_id
                    st.rerun()

            if st.session_state.get("confirm_activity_delete_id") == activity_id:
                st.warning("Delete this activity from history?")
                confirm_col, cancel_col = st.columns(2)

                with confirm_col:
                    if st.button(
                        "Yes, Delete",
                        key=f"confirm_delete_activity_{activity_id}"
                    ):
                        execute(
                            "DELETE FROM activities WHERE id = %s AND user_id = %s",
                            (activity_id, user_id)
                        )
                        conn.commit()
                        st.session_state.pop("confirm_activity_delete_id", None)
                        st.rerun()

                with cancel_col:
                    if st.button(
                        "Cancel",
                        key=f"cancel_delete_activity_{activity_id}"
                    ):
                        st.session_state.pop("confirm_activity_delete_id", None)
                        st.rerun()

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
        WHERE user_id = %s
        AND completed = 1
        AND completed_at >= %s
        AND completed_at < %s
        ORDER BY completed_at
        """,
        (
            user_id,
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