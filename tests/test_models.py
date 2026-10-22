import pytest
from models.user import User
from models.project import Project
from models.task import Task

def test_user_creation():
    user = User("Alex", "alex@example.com")
    assert user.name == "Alex"
    assert user.email == "alex@example.com"
    assert len(user.projects) == 0

def test_add_project_to_user():
    user = User("Alex")
    project = Project("CLI Tool")
    user.add_project(project)
    assert len(user.projects) == 1
    assert user.projects[0].title == "CLI Tool"

def test_project_due_date_validation():
    with pytest.raises(ValueError):
        Project("Test", "Desc", "invalid-date")
    
    valid_project = Project("Test", "Desc", "2026-12-31")
    assert valid_project.due_date == "2026-12-31"

def test_task_completion():
    task = Task("Implement add-task")
    assert task.status == "Pending"
    task.complete()
    assert task.status == "Completed"