
from tasks.task import Task
from tasks.task_enum import TASKS
from helpers import task_logger, load_wells
from traceback import format_exc

class LoadWellData(Task):

    def execute(self):
        task = TASKS.LOAD_WELL_DATA.value
        logger = task_logger(task, self.context.logs_path)
        try:
            load_wells(self.context.db_path, self.context.well_file)
            logger.info(f"{task}: {self.context.logs_path}")
        except Exception as e:
            logger.error(f"Error {task} workflow task: {e}\n{format_exc()}")
            raise ValueError(f"Error {task} workflow task: {e}")