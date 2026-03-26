from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import Task

main = Blueprint('main', __name__)


# Главная страница 
@main.route('/')
def index():
    """Показать список задач с возможностью фильтрации."""
    filt = request.args.get('filter', 'all')

    if filt == 'active':
        tasks = Task.query.filter_by(completed=False)
    elif filt == 'completed':
        tasks = Task.query.filter_by(completed=True)
    else:
        tasks = Task.query

    tasks = tasks.order_by(Task.created_at.desc()).all()
    return render_template('index.html', tasks=tasks, current_filter=filt)


# Добавить задачу
@main.route('/add', methods=['POST'])
def add():
    title = request.form.get('title', '').strip()
    if not title:
        return redirect(url_for('main.index'))

    task = Task(
        title=title,
        description=request.form.get('description', '').strip(),
        priority=request.form.get('priority', 'medium'),
    )
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('main.index'))


# Переключить статус 
@main.route('/toggle/<int:task_id>')
def toggle(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for('main.index'))


# Удалить задачу 
@main.route('/delete/<int:task_id>')
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('main.index'))


# Редактировать задачу
@main.route('/edit/<int:task_id>', methods=['POST'])
def edit(task_id):
    task = Task.query.get_or_404(task_id)
    task.title       = request.form.get('title', task.title).strip()
    task.description = request.form.get('description', task.description).strip()
    task.priority    = request.form.get('priority', task.priority)
    db.session.commit()
    return redirect(url_for('main.index'))