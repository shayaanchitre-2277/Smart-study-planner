Smart Study Planner

A clean, modern Flask web application to help students track study tasks,
manage deadlines, and monitor their progress.

---

 Features

- **Dashboard** — view all tasks sorted by deadline & priority
- **Today's Tasks** — highlighted tasks due today
- **Overdue Detection** — tasks past deadline turn red automatically
- **Add Tasks** — subject, topic, deadline, and priority (Easy / Medium / Hard)
- **Complete & Delete** — mark tasks done or remove them
- **Progress Tracking** — total, completed, and % progress bar
- **SQLite Database** — persistent storage via Flask-SQLAlchemy
- **Responsive UI** — works on mobile and desktop

---

 Project Structure

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


 Routes

| Method | URL                    | Action                  

| GET    | `/`                    | Dashboard               |
| GET    | `/add`                 | Show add-task form      |
| POST   | `/add`                 | Save new task           |
| GET    | `/complete/<id>`       | Mark task completed     |
| GET    | `/undo/<id>`           | Revert task to pending  |
| GET    | `/delete/<id>`         | Delete task             |

---

 Tech Stack

- **Backend**: Python 3, Flask, Flask-SQLAlchemy
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, Vanilla JS
- **Fonts**: Syne + DM Sans (Google Fonts)
