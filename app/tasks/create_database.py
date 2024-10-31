
from tasks.task import Task
from tasks.task_enum import TASKS
from helpers import task_logger
from database import AFEDB
from traceback import format_exc

class CreateDatabase(Task):

    def execute(self):
        task = TASKS.CREATE_DATABASE.value
        logger = task_logger(task, self.context.logs_path)
        try:
            afe_db = AFEDB(self.context.db_path)

            afe_db.execute_ddl(AFEDB.SQL.DROP_TARGET_WELL_INFORMATION_TABLE.value)
            afe_db.execute_ddl(AFEDB.SQL.CREATE_TARGET_WELL_INFORMATION_TABLE.value)

            afe_db.execute_ddl(AFEDB.SQL.DROP_WELL_TABLE.value)
            afe_db.execute_ddl(AFEDB.SQL.CREATE_WELL_TABLE.value)

            afe_db.execute_ddl(AFEDB.SQL.DROP_SURVEY_TABLE.value)
            afe_db.execute_ddl(AFEDB.SQL.CREATE_SURVEY_TABLE.value)
            
            afe_db.execute_ddl(AFEDB.SQL.DROP_ANALYSIS_TABLE.value)
            afe_db.execute_ddl(AFEDB.SQL.CREATE_ANALYSIS_TABLE.value)

            afe_db.execute_ddl(AFEDB.SQL.DROP_XYZ_DISTANCE_TABLE.value)
            afe_db.execute_ddl(AFEDB.SQL.CREATE_XYZ_DISTANCE_TABLE.value)

            afe_db.execute_ddl(AFEDB.SQL.DROP_LATITUDE_LONGITUDE_DISTANCE_TABLE.value)
            afe_db.execute_ddl(AFEDB.SQL.CREATE_LATITUDE_LONGITUDE_DISTANCE_TABLE.value)

            logger.info(f"{task}: {self.context.logs_path}")
        except Exception as e:
            logger.error(f"Error {task} workflow task: {e}\n{format_exc()}")
            raise ValueError(f"Error {task} workflow task: {e}")