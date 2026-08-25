# Daily Tracker

A focused, multi-user habit and activity tracker built with Streamlit, Google Sign-In, and MySQL. Record how you spend your time, manage personal categories, organize tasks, and review your history from one simple workspace.

<!-- Add your screenshots here when ready.

![Daily Tracker dashboard](docs/images/dashboard.png)
![Daily Tracker tasks](docs/images/tasks.png)
![Daily Tracker history](docs/images/history.png)

Suggested folder:
- docs/images/dashboard.png
- docs/images/tasks.png
- docs/images/history.png
-->

## Features

- Google Sign-In with no separate app password
- Separate data for every user
- Personal activity categories with custom emoji icons
- Activity tracking with time spent and descriptions
- Scheduled tasks with date and time
- Deadline tasks
- Flexible tasks without a fixed date
- Mark tasks as completed
- Date navigation for daily records
- History view for activities and completed tasks
- Responsive mobile-friendly interface
- MySQL storage for persistent cloud data

## Screenshots

Screenshots will be added here.

<!-- Replace this section with image links when your screenshots are ready. -->

| Activities | To-Do List | History |
| --- | --- | --- |
| Add screenshot | Add screenshot | Add screenshot |

## Technology

- Python 3.11+
- Streamlit
- MySQL
- Google OAuth 2.0 / OpenID Connect
- Authlib
- mysql-connector-python
- httpx

## Project Structure

```text
.
├── Habit_tracker.py              # Streamlit application
├── requirements.txt              # Python dependencies
├── .gitignore                    # Local files and secrets excluded from Git
├── .streamlit/
│   └── secrets.toml              # Local secrets, never commit this file
└── .devcontainer/
    └── devcontainer.json         # Optional Codespaces/Dev Containers setup
```

## Local Setup

### 1. Clone the repository

```powershell
git clone <your-repository-url>
cd habit_tracker
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use the virtual environment Python directly instead.

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure local secrets

Create this file:

```text
.streamlit/secrets.toml
```

Add your local values:

```toml
MYSQLHOST = "your-mysql-host"
MYSQLPORT = "your-mysql-port"
MYSQLUSER = "your-mysql-user"
MYSQLPASSWORD = "your-mysql-password"
MYSQLDATABASE = "your-mysql-database"

[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "generate-a-long-random-secret"

[auth.google]
client_id = "your-google-client-id"
client_secret = "your-google-client-secret"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
```

The MySQL values must be at the top level, before the `[auth]` section. Never commit `secrets.toml` to GitHub.

Generate a cookie secret with:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 5. Start the app

Run the command from the directory containing `Habit_tracker.py` and `.streamlit`:

```powershell
python -m streamlit run Habit_tracker.py
```

Open the local URL shown by Streamlit, normally:

```text
http://localhost:8501
```

## Google Sign-In Setup

1. Open the [Google Cloud Console](https://console.cloud.google.com/).
2. Create or select a project.
3. Configure the OAuth consent screen.
4. Choose `External` for users outside your organization.
5. Add the `openid`, `email`, and `profile` scopes.
6. Add your Google account under **Test users** while the app is in testing mode.
7. Create a **Web application** OAuth client.
8. Add this local redirect URI:

```text
http://localhost:8501/oauth2callback
```

For a deployed app, add the exact production callback URI instead:

```text
https://your-app-name.streamlit.app/oauth2callback
```

The redirect URI in the running app must exactly match an authorized redirect URI in Google Cloud.

## Database Setup

The application expects these MySQL tables:

- `users`
- `categories`
- `activities`
- `tasks`

The `users` table stores the Google identity. The other tables use `user_id` so each account sees and changes only its own data.

A basic `users` table is:

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    google_subject VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);
```

The `categories`, `activities`, and `tasks` tables must each contain a `user_id` column. Their queries should always filter by the authenticated user's ID.

## Streamlit Cloud Deployment

1. Push the project files to GitHub.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/).
3. Select the repository and branch.
4. Set the main file to:

```text
Habit_tracker.py
```

5. Open **App settings > Secrets**.
6. Add the production MySQL and Google OAuth values.
7. Set the production redirect URI:

```toml
[auth]
redirect_uri = "https://your-app-name.streamlit.app/oauth2callback"
cookie_secret = "your-production-cookie-secret"
```

8. Reboot the app after saving secrets.
9. Add the production callback URI to Google Cloud.
10. Test login with an approved Google test user.

Local and production environments can use different cookie secrets. Keep each environment's secret stable after deployment.

## Security Notes

- Never commit `.streamlit/secrets.toml`.
- Never place passwords, OAuth client secrets, or database credentials in Python code.
- Use a new Google client secret if an old one has been exposed.
- Use a separate MySQL user with only the permissions the app needs when possible.
- Keep `user_id` filters on every `SELECT`, `INSERT`, `UPDATE`, and `DELETE` operation.
- Test with two Google accounts to confirm that users cannot see or modify each other's data.

## Testing Checklist

- [ ] Google login works locally
- [ ] A user record is created after the first login
- [ ] Categories are private to each user
- [ ] Activities are private to each user
- [ ] Tasks are private to each user
- [ ] History is private to each user
- [ ] A second Google account cannot access the first user's data
- [ ] Production redirect URI is registered in Google Cloud
- [ ] Production secrets are configured in Streamlit Cloud

## License

Add your preferred license here.
