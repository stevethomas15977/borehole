
from context import Context
from tasks import TaskFactory
from helpers import write_to_file
import os
import traceback

class WorkflowGroup:

    def __init__(self, name: str, context: Context, task_factory: TaskFactory):
        self.name = name
        self.context = context
        self.task_factory = task_factory
        self.tasks = []

    def add_task(self, task_type: str):
        self.tasks.append(self.task_factory.create_task(task_type))

    def run(self):
        print(f"Running workflow group: {self.name}")
        for task in self.tasks:
            try:
                print(f"Starting {task.__class__.__name__}...")
                task.execute()
                print(f"{task.__class__.__name__} completed successfully.")
            except Exception as e:
                print(f"{task.__class__.__name__} failed with error: {e}")
                exception_message = f"{task.__class__.__name__}\n\n{traceback.format_exception(None, e, e.__traceback__)}"
                write_to_file(os.path.join(self.context.project_path, f"ERROR"), exception_message)
                running_file = os.path.join(self.context.project_path, f"RUNNING")
                if os.path.exists(running_file):
                    os.remove(running_file)
                raise e