'''
Notes:
Getting Todoist Credentials
1.Go to Todoist
2.Log in to your account
3.Go to Settings -> Integrations
4.Copy your API token (it's a long string of characters)

Install the library using pip:
-pip install todoist-api-python
'''

from todoist_api_python.api import TodoistAPI
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the API
api = TodoistAPI(os.getenv("TODOIST_API_TOKEN"))

def show_all_projects():
    try:
        projects_iterator = api.get_projects()
        
        all_projects = []
        for project_list in projects_iterator:
            all_projects.extend(project_list)
        
        # Now you can work with all projects
        for project in all_projects:
            print(f"Project: {project.name} ID: {project.id}")
            
    except Exception as error:
        print(f"Error: {error}")

def show_project_by_id(project_id):
    try:
        project = api.get_project(project_id)
        print(f"Project: {project.name} ID: {project.id}")
    except Exception as error:
        print(f"Error: {error}")

def show_all_tasks_by_project(project_id):
    try:
        tasks_iter = api.get_tasks(project_id=project_id)
        
        tasks = []
        for task_list in tasks_iter:
            tasks.extend(task_list)

        for task in tasks:
            print(f"Task: {task.content} Description: {'None' if task.description=='' else task.description} ID: {task.id}")
    except Exception as error:
        print(error)

def add_task(content, description, project_id, due_string):
    try:
        task = api.add_task(content=content,
                            description=description,
                            project_id=project_id,
                            due_string=due_string)
        print(f"Created task: {task.content}")
    except Exception as error:
        print(error)

if __name__ == "__main__":
    PROJECT_ID = os.getenv("PROJECT_ID")
    show_all_projects()
    show_project_by_id(PROJECT_ID)
    show_all_tasks_by_project(PROJECT_ID)
    add_task("New Task from API", "This is a task added via the Todoist API", PROJECT_ID, "tomorrow on 11:00")