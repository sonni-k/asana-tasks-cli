Asana task CLI

This project provides a small Python script that connects to the Asana API and lists your assigned tasks.

Setup

1. Install dependencies:
   pip install -r requirements.txt

2. Create a config.py file from the example:
   cp CONFIG_EXAMPLE.py config.py

3. Fill in your Asana values in config.py:
   ASANA_PAT = "your_personal_access_token"
   user_gid = "your_user_gid"
   assignee_gid = "your_assignee_gid"
   workspace_gid = "your_workspace_gid"

Usage

Run the script with one of these actions:

- python main.py current
- python main.py overdue

The `current` command prints tasks that are due today or have no due date.
The `overdue` command prints tasks whose due date is before today.

Each task output includes the task name, notes, and Asana permalink.
