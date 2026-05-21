from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'study-planner-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///study_planner.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Task(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    subject   = db.Column(db.String(100), nullable=False)
    topic     = db.Column(db.String(200), nullable=False)
    deadline  = db.Column(db.Date, nullable=False)
    priority  = db.Column(db.String(10), nullable=False)
    status    = db.Column(db.String(10), default='Pending')
    progress = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def is_overdue(self):
        return self.deadline < date.today() and self.status == 'Pending'

    def is_today(self):
        return self.deadline == date.today()

    def priority_order(self):
        return {'Hard': 1, 'Medium': 2, 'Easy': 3}.get(self.priority, 4)


@app.route('/')
def index():

    all_tasks = Task.query.order_by(Task.deadline.asc()).all()
    all_tasks.sort(key=lambda t: (t.status == 'Completed', t.deadline, t.priority_order()))

    today_tasks  = [t for t in all_tasks if t.is_today() and t.status == 'Pending']
    overdue_tasks = [t for t in all_tasks if t.is_overdue()]
    upcoming     = [t for t in all_tasks if not t.is_today() and not t.is_overdue()]

    total     = len(all_tasks)
    completed = sum(1 for t in all_tasks if t.status == 'Completed')
    progress  = round((completed / total * 100) if total > 0 else 0)

    # SUBJECT PROGRESS
    subject_progress = {}

    for task in all_tasks:
        subject = task.subject

        if subject not in subject_progress:
            subject_progress[subject] = {"total": 0, "completed": 0}

        subject_progress[subject]["total"] += 1

        subject_progress[subject]["completed"] += task.progress / 100

    for subject in subject_progress:
        total_s = subject_progress[subject]["total"]
        completed_s = subject_progress[subject]["completed"]

        if total_s > 0:
            percent = int((completed_s / total_s) * 100)
        else:
            percent = 0

        subject_progress[subject]["percent"] = percent

   # 🔥 MULTIPLE WEAK SUBJECTS
    weak_subjects = []

    for subject, data in subject_progress.items():

        has_hard = any(
            t.subject.strip().lower() == subject.strip().lower()
            and t.priority.strip().lower() == "hard"
            for t in all_tasks
        )

        if has_hard and data["percent"] < 99:
            weak_subjects.append({
                "name": subject,
                "percent": data["percent"]
            })

    # if nothing found → fallback (show weakest anyway)
    if not weak_subjects:
        weak_subjects = sorted(
            subject_progress.items(),
            key=lambda x: x[1]["percent"]
        )[:2]

        weak_subjects = [
            {"name": s[0], "percent": s[1]["percent"]}
            for s in weak_subjects
        ]

    # SMART STUDY PLAN
    study_plan = []

    for task in all_tasks:
        if task.status == "Pending":

            days_left = (task.deadline - date.today()).days
            total_hours = 10  # assumed total work

            if days_left > 0:
                remaining_work = (100 - task.progress) / 100
                daily_work = round((remaining_work * total_hours) / days_left, 1)
            else:
                daily_work = 0

            study_plan.append({
                "subject": task.subject,
                "topic": task.topic,
                "daily_work": daily_work,
                "days_left": days_left
            })

    # TODAY PROGRESS
    total_score = 0
    completed_score = 0

    for task in all_tasks:
        if task.is_today():

            if task.priority == "Easy":
                weight = 1
            elif task.priority == "Medium":
                weight = 2
            else:
                weight = 3

            total_score += weight

            if task.status == "Completed":
                completed_score += weight

    if total_score > 0:
        today_progress = int((completed_score / total_score) * 100)
    else:
        today_progress = 0

    return render_template(
        'index.html',
        all_tasks=all_tasks,
        today_tasks=today_tasks,
        overdue_tasks=overdue_tasks,
        upcoming=upcoming,
        total=total,
        completed=completed,
        progress=progress,
        today=date.today(),
        today_progress=today_progress,
        study_plan=study_plan,
        subject_progress=subject_progress,
        weak_subjects=weak_subjects        # ✅ STEP 2
              
    )


@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        subject  = request.form.get('subject', '').strip()
        topic    = request.form.get('topic', '').strip()
        deadline_str = request.form.get('deadline', '')
        priority = request.form.get('priority', 'Medium')
        progress = int(request.form.get('progress', 0))

        if not subject or not topic or not deadline_str:
            flash('Please fill in all fields.', 'error')
            return redirect(url_for('add_task'))

        deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()

        new_task = Task(
            subject=subject,
            topic=topic,
            deadline=deadline,
            priority=priority,
            status='Pending',
            progress=progress
        )

        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add.html', today=date.today().isoformat())


@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.status = 'Completed'
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)

    if request.method == 'POST':
        task.subject = request.form['subject']
        task.topic = request.form['topic']
        task.deadline = datetime.strptime(request.form['deadline'], '%Y-%m-%d').date()
        task.priority = request.form['priority']
        task.progress = int(request.form.get('progress', 0))

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit.html', task=task)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)