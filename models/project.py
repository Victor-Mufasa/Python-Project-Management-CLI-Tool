from datetime import datetime
from models.task import Task

class Project:
    """Represents a project containing tasks."""
    _id_counter = 1  # Class attribute for ID generation

    def __init__(self, title, description="", due_date=None):
        self.id = Project._id_counter
        Project._id_counter += 1
        self.title = title
        self.description = description
        self._due_date = None
        self.due_date = due_date  # Triggers setter
        self.tasks = []  # One-to-many relationship

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, value):
        """Validates due date format."""
        if value:
            try:
                datetime.strptime(value, "%Y-%m-%d")
                self._due_date = value
            except ValueError:
                raise ValueError("Due date must be in YYYY-MM-DD format.")
        else:
            self._due_date = None

    def add_task(self, task):
        self.tasks.append(task)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "tasks": [t.to_dict() for t in self.tasks]
        }