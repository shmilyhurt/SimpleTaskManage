from sqlalchemy.orm import validates

from .. import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.Date, nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    is_delete = db.Column(db.String(25), nullable=False, default='f')

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Title cannot be empty")
        if len(title) > 255:
            raise ValueError("Title cannot exceed 255 characters")
        return title

    @validates('priority')
    def validate_priority(self, key, priority):
        if priority < 1 or priority > 5:
            raise ValueError("Priority must be between 1 and 5")
        return priority

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'priority': self.priority,
            'is_delete': self.is_delete
        }