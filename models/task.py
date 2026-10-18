class Task:
    """Represents a task within a project."""
    def __init__(self, title, status="Pending", assigned_to=None):
        self.title = title
        self.status = status
        self.assigned_to = assigned_to  # Could be a list of User objects

    def complete(self):
        self.status = "Completed"

    def to_dict(self):
        return {
            "title": self.title,
            "status": self.status,
            "assigned_to": self.assigned_to
        }