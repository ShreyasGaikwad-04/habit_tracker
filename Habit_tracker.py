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