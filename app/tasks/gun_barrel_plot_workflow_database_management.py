
from tasks.task import Task
from tasks.task_enum import TASKS
from helpers import task_logger
from database import AFEDB
from traceback import format_exc

class GunBarrelPlotWorkflowDatabaseManagement(Task):

    def execute(self):
        task = TASKS.GUN_BARREL_PLOT_WORKFLOW_DATABASE_MANAGEMENT.value
        logger = task_logger(task, self.context.logs_path)
        try:
            afe_db = AFEDB(self.context.db_path)
            
            afe_db.execute_ddl(AFEDB.SQL.DROP_OVERLAP_TABLE.value)
            afe_db.execute_ddl(AFEDB.SQL.CREATE_OVERLAP_TABLE.value)

            afe_db.execute_ddl(AFEDB.SQL.DROP_GUN_BARREL_PLOT_TABLE.value)
            afe_db.execute_ddl(AFEDB.SQL.CREATE_GUN_BARREL_PLOT_TABLE.value)

            afe_db.execute_ddl(AFEDB.SQL.DROP_GUN_BARREL_TRIANGLE_DISTANCES_TABLE.value)
            afe_db.execute_ddl(AFEDB.SQL.CREATE_GUN_BARREL_TRIANGLE_DISTANCES_TABLE.value)

            logger.info(f"{task}: {self.context.logs_path}")
        except Exception as e:
            logger.error(f"Error {task} workflow task: {e}\n{format_exc()}")
            raise ValueError(f"Error {task} workflow task: {e}")