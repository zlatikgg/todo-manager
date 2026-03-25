from datetime import datetime
from app import db


class Task(db.Model):
    """Модель одной задачи."""

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default='')
    priority    = db.Column(db.String(10), default='medium')   # low / medium / high
    completed   = db.Column(db.Boolean, default=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.id}: {self.title}>'