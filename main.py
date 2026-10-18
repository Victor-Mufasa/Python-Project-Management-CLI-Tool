#!/usr/bin/env python3
import argparse
from tabulate import tabulate
from models.user import User
from models.project import Project
from models.task import Task
from utils.storage import save_data, load_data

def find_user(users, user_name):
    """Finds a user by name (case-insensitive). Returns None if not found."""
    for user in users:
        if user.name.lower() == user_name.lower():
            return user
    return None

def find_project(users, project_title):
    """Searches all users' projects for a specific project title."""
    for user in users:
        for project in user.projects:
            if project.title.lower() == project_title.lower():
                return project
    return None

def handle_add_user(users, args):
    """Creates a new user and saves it."""
    new_user = User(args.name, args.email)
    users.append(new_user)
    save_data(users)
    print(f"User '{args.name}' created successfully.")

def handle_add_project(users, args):
    """Adds a project to a specific user and saves it."""
    user = find_user(users, args.user)
    if not user:
        print(f"Error: User '{args.user}' not found.")
        return
    
    try:
        new_project = Project(args.title, args.description, args.due_date)
        user.add_project(new_project)
        save_data(users)
        print(f"Project '{args.title}' added to {user.name}.")
    except ValueError as e:
        print(f"Error: {e}")

def handle_add_task(users, args):
    """Adds a task to a specific project and saves it."""
    project = find_project(users, args.project)
    if not project:
        print(f"Error: Project '{args.project}' not found.")
        return
        
    new_task = Task(args.title)
    project.add_task(new_task)
    save_data(users)
    print(f"Task '{args.title}' added to project '{project.title}'.")

def handle_list_projects(users, args):
    """Displays a nicely formatted table of a user's projects."""
    user = find_user(users, args.user)
    if not user or not user.projects:
        print(f"No projects found for '{args.user}'.")
        return

    # Build the table data
    table_data = []
    for project in user.projects:
        total_tasks = len(project.tasks)
        completed_tasks = sum(1 for task in project.tasks if task.status == "Completed")
        due_date = project.due_date or "N/A"
        
        table_data.append([project.title, due_date, f"{completed_tasks}/{total_tasks}"])

    # Print using the tabulate package
    print(f"\nProjects for {user.name}:")
    print(tabulate(table_data, headers=["Title", "Due Date", "Tasks (Done/Total)"], tablefmt="grid"))

def handle_complete_task(users, args):
    """Marks a specific task as complete and saves it."""
    project = find_project(users, args.project)
    if not project:
        print("Error: Project not found.")
        return

    # Look for the task inside the project
    task_found = False
    for task in project.tasks:
        if task.title.lower() == args.task.lower():
            task.complete()
            save_data(users)
            print(f"Task '{task.title}' marked as completed.")
            task_found = True
            break
            
    if not task_found:
        print("Error: Task not found in this project.")

# MAIN FUNCTION (The CLI Setup)

def main():
    # 1. Setup the Argument Parser
    parser = argparse.ArgumentParser(description="Project Management CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 2. Define the Subcommands
    # add-user
    user_parser = subparsers.add_parser("add-user", help="Add a new user")
    user_parser.add_argument("--name", required=True, help="User's name")
    user_parser.add_argument("--email", default="", help="User's email")

    # add-project
    proj_parser = subparsers.add_parser("add-project", help="Add a project to a user")
    proj_parser.add_argument("--user", required=True, help="Name of the user")
    proj_parser.add_argument("--title", required=True, help="Project title")
    proj_parser.add_argument("--description", default="", help="Project description")
    proj_parser.add_argument("--due-date", help="Due date (YYYY-MM-DD)")

    # add-task
    task_parser = subparsers.add_parser("add-task", help="Add a task to a project")
    task_parser.add_argument("--project", required=True, help="Project title")
    task_parser.add_argument("--title", required=True, help="Task title")

    # list-projects
    list_proj_parser = subparsers.add_parser("list-projects", help="List projects for a user")
    list_proj_parser.add_argument("--user", required=True, help="Name of the user")

    # complete-task
    complete_parser = subparsers.add_parser("complete-task", help="Mark a task as complete")
    complete_parser.add_argument("--project", required=True, help="Project title")
    complete_parser.add_argument("--task", required=True, help="Task title")

    # 3. Parse arguments
    args = parser.parse_args()
    users = load_data()

    # 4. Route the commands to the correct helper functions
    if args.command == "add-user":
        handle_add_user(users, args)
    elif args.command == "add-project":
        handle_add_project(users, args)
    elif args.command == "add-task":
        handle_add_task(users, args)
    elif args.command == "list-projects":
        handle_list_projects(users, args)
    elif args.command == "complete-task":
        handle_complete_task(users, args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()