import datetime
import asana
from asana.rest import ApiException
from config import ASANA_PAT, user_gid, assignee_gid, workspace_gid
import argparse


class AsanaTasks:
    """
    A class to fetch my Asana tasks.
    """

    def __init__(self, access_token) -> None:
        """
        Initialize the Asana client.

        Args:
            access_token (str): The Asana personal access token.
        """
        configuration = asana.Configuration()
        configuration.access_token = access_token
        self.api_client = asana.ApiClient(configuration)

    def get_user_info(self, user_gid):
        """
        Retrieves user information from Asana.

        Args:
            user_gid (str): The user's GID in Asana.

        Returns:
            dict: The user information dictionary

        Raises:
            ApiException: If an error occurs during API call
        """
        users_api_instance = asana.UsersApi(self.api_client)
        opts = {}
        try:
            user = users_api_instance.get_user(user_gid, opts)
            return user
        except ApiException as e:
            print(f"Exception when calling UsersApi->get_user:\n {e}")
            return None

    def get_tasks(self, assignee_gid, workspace_gid):
        """
        Fetches tasks assigned to  a specific user within a workspace
        Args:
            assignee_gid (str): The GID of the assignee (user) for the tasks.
            workspace_gid (str): The GID of the workspace where tasks reside.
            completed_since (datetime.datetime, optional):
            Datetime object representing the minimum completion time
            for tasks (defaults to None).
        Returns:
            list: A list of task dictionaries
        Raises:
            ApiException: If an error occurs during API call.
        """
        tasks_api_instance = asana.TasksApi(self.api_client)
        tasks_opts = {
            "assignee": assignee_gid,
            "workspace": workspace_gid,
            "completed_since": datetime.datetime.now(),
            "opt_fields": (
                "assignee,assignee.name,assignee_section,assignee_section.name,"
                "assignee_status,due_on,completed,gid,user.name,name,notes,permalink_url"
            ),
        }

        try:
            api_response = tasks_api_instance.get_tasks(tasks_opts)
            return [task for task in api_response]
        except ApiException as e:
            print(f"Exception when calling UsersApi->get_user:\n {e}")
            return []

    def get_current_tasks(self, assignee_gid, workspace_gid):
        """
        Fetches current tasks assigned to a specific user within a workspace.

        Args:
            assignee_gid (str): The GID of the assignee (user) for the tasks.
            workspace_gid (str): The GID of the workspace where tasks reside.

        Returns:
            list: A list of current task dictionaries.
        """
        tasks = self.get_tasks(assignee_gid, workspace_gid)
        current_tasks = [task for task in tasks if self._is_current_task(task)]
        return current_tasks

    def get_overdue_tasks(self, assignee_gid, workspace_gid):
        """
        Fetches overdue tasks assigned to a specific user within a workspace.

        Args:
            assignee_gid (str): The GID of the assignee (user) for the tasks.
            workspace_gid (str): The GID of the workspace where tasks reside.

        Returns:
            list: A list of overdue task dictionaries.
        """
        tasks = self.get_tasks(assignee_gid, workspace_gid)
        overdue_tasks = [task for task in tasks if self._is_overdue_task(task)]
        return overdue_tasks

    def _is_current_task(self, task):
        """
        Checks if a task is current.

        Args:
            task (dict): The task dictionary.

        Returns:
            bool: True if the task is current, False otherwise.
        """
        due_date = task.get("due_on")
        return (
            due_date is None
            or datetime.date.fromisoformat(due_date) >= datetime.date.today()
        )

    def _is_overdue_task(self, task):
        """
        Checks if a task is overdue.

        Args:
            task (dict): The task dictionary.

        Returns:
            bool: True if the task is overdue, False otherwise.
        """
        due_date = task.get("due_on")
        return (
            due_date is not None
            and datetime.date.fromisoformat(due_date) < datetime.date.today()
        )

    def create_task(self, assignee_gid, workspace_gid, name, due_on, html_notes):
        """
        Create a task in a workspace.

        Args:
            assignee_gid (str): GID of the assignee for the task.
            workspace_gid (str): GID of the workspace where the task will be created.
            name (str): Name of the task.
            due_on (str): Date when the task is due (YYYY-MM-DD format).
            html_notes (str): HTML formatted notes for the task.

        Returns:
            dict: A dictionary of the created tasks
        Raises:
            ApiException: If an error occurs during API call.
        """
        tasks_api_instance = asana.TasksApi(self.api_client)

        body = {
            "data": {
                "name": name,
                "assignee": assignee_gid,
                "workspace": workspace_gid,
                "due_on": due_on,
                "html_notes": html_notes,
            }
        }  # dict | The task to create.
        opts = {
            "opt_fields": "approval_status,assignee,assignee.name,html_notes",
        }

        try:
            # Create a task
            api_response = tasks_api_instance.create_task(body, opts)
            return api_response
        except ApiException as e:
            print(f"Exception when calling UsersApi->get_user:\n {e}")
            return []


def main():
    parser = argparse.ArgumentParser(description="Asana task management CLI")
    parser.add_argument(
        "action", choices=["current", "overdue"], help="Action to perform"
    )
    args = parser.parse_args()

    asana_client = AsanaTasks(ASANA_PAT)

    if args.action == "current":
        tasks = asana_client.get_current_tasks(assignee_gid, workspace_gid)
        print("Current tasks:")
        for task in tasks:
            print(f" - {task['name']}")
            print(f" - {task['notes']}")
            print(f" - {task['permalink_url']}")
    elif args.action == "overdue":
        tasks = asana_client.get_overdue_tasks(assignee_gid, workspace_gid)
        print("Overdue tasks:")
        for task in tasks:
            print(f" - {task['name']}")
            print(f" - {task['notes']}")
            print(f" - {task['permalink_url']}")

    else:
        print("Invalid action. Please specify 'current' or 'overdue'.")


if __name__ == "__main__":
    main()
