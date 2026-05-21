# 📚 Smart Study Planner

A clean, modern Flask web application to help students track study tasks,
manage deadlines, and monitor their progress.

---

## ✨ Features

- **Dashboard** — view all tasks sorted by deadline & priority
- **Today's Tasks** — highlighted tasks due today
- **Overdue Detection** — tasks past deadline turn red automatically
- **Add Tasks** — subject, topic, deadline, and priority (Easy / Medium / Hard)
- **Complete & Delete** — mark tasks done or remove them
- **Progress Tracking** — total, completed, and % progress bar
- **SQLite Database** — persistent storage via Flask-SQLAlchemy
- **Responsive UI** — works on mobile and desktop

---

## 🗂 Project Structure

```
smart_study_planner/
├── app.py                  ← Flask app, routes, database model
├── requirements.txt        ← Python dependencies
├── README.md
├── templates/
│   ├── base.html           ← Shared layout (navbar, flash messages)
│   ├── index.html          ← Dashboard
│   └── add.html            ← Add task form
├── static/
│   ├── css/
│   │   └── style.css       ← All styles
│   └── js/
│       └── main.js         ← Delete confirm, animations
└── instance/
    └── study_planner.db    ← SQLite DB (auto-created on first run)
```

---

## 🚀 How to Run

### Step 1 — Create a virtual environment (recommended)
```bash
python -m venv venv
```

### Step 2 — Activate the virtual environment
```bash
# On Windows:
venv\Scripts\activate

# On macOS / Linux:
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Run the app
```bash
python app.py
```

### Step 5 — Open in your browser
```
http://127.0.0.1:5000
```

The SQLite database (`study_planner.db`) is created automatically inside
the `instance/` folder on first run.

---

## 📋 Routes

| Method | URL                    | Action                  |
|--------|------------------------|-------------------------|
| GET    | `/`                    | Dashboard               |
| GET    | `/add`                 | Show add-task form      |
| POST   | `/add`                 | Save new task           |
| GET    | `/complete/<id>`       | Mark task completed     |
| GET    | `/undo/<id>`           | Revert task to pending  |
| GET    | `/delete/<id>`         | Delete task             |

---

## 🎨 Tech Stack

- **Backend**: Python 3, Flask, Flask-SQLAlchemy
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, Vanilla JS
- **Fonts**: Syne + DM Sans (Google Fonts)
