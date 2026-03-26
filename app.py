from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# ─── Создание приложения ──────────────────────────
app = Flask(__name__)
app.config['SECRET_KEY'] = 'any-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ─── Модель ───────────────────────────────────────
class Task(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default='')
    priority    = db.Column(db.String(10), default='medium')
    completed   = db.Column(db.Boolean, default=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)


# ─── Маршруты ─────────────────────────────────────
@app.route('/')
def index():
    filt = request.args.get('filter', 'all')

    if filt == 'active':
        tasks = Task.query.filter_by(completed=False)
    elif filt == 'completed':
        tasks = Task.query.filter_by(completed=True)
    else:
        tasks = Task.query

    tasks = tasks.order_by(Task.created_at.desc()).all()
    return render_template('index.html', tasks=tasks, current_filter=filt)


@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title', '').strip()
    if not title:
        return redirect(url_for('index'))

    task = Task(
        title=title,
        description=request.form.get('description', '').strip(),
        priority=request.form.get('priority', 'medium'),
    )
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/toggle/<int:task_id>')
def toggle(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/edit/<int:task_id>', methods=['POST'])
def edit(task_id):
    task = Task.query.get_or_404(task_id)
    task.title       = request.form.get('title', task.title).strip()
    task.description = request.form.get('description', task.description).strip()
    task.priority    = request.form.get('priority', task.priority)
    db.session.commit()
    return redirect(url_for('index'))


# ─── Запуск ───────────────────────────────────────
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)