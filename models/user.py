from .person import Person

class User(Person):
    """Represents a user who owns projects."""
    def __init__(self, name, email=""):
        super().__init__(name)
        self.email = email
        self.projects = []  # One-to-many relationship

    def add_project(self, project):
        self.projects.append(project)

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "projects": [p.to_dict() for p in self.projects]
        }