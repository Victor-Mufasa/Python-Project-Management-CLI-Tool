import json
from models.user import User
from models.project import Project
from models.task import Task

DATA_FILE = "data/data.json"

def save_data(users):
    """Saves all users and their nested projects/tasks to JSON."""
    with open(DATA_FILE, "w") as f:
        json.dump([u.to_dict() for u in users], f, indent=4)

def load_data():
    """Loads data from JSON and reconstructs the object model."""
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            users = []
            for u_data in data:
                user = User(u_data["name"], u_data.get("email", ""))
                for p_data in u_data.get("projects", []):
                    project = Project(p_data["title"], p_data.get("description", ""), p_data.get("due_date"))
                    for t_data in p_data.get("tasks", []):
                        task = Task(t_data["title"], t_data["status"], t_data.get("assigned_to"))
                        project.add_task(task)
                    user.add_project(project)
                users.append(user)
            return users
    except FileNotFoundError:
        return []
    except json.decoder.JSONDecodeError:
        # If the file is empty or corrupted, start fresh
        print("Warning: Data file was empty or corrupted. Starting fresh.")
        return []