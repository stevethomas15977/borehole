
from tasks.task import Task
from tasks.task_enum import TASKS
from helpers import task_logger
from database import AFEDB
from traceback import format_exc

class OffsetWellIdenficationWorkflowDatabaseManagement(Task):

    def execute(self):
        task = TASKS.OFFSET_WELL_IDENTIFICATION_WORKFLOW_DATABASE_MANAGEMENT.value
        logger = task_logger(task, self.context.logs_path)
        try:
            afe_db = AFEDB(self.context.db_path)
            
            afe_db.execute_ddl(AFEDB.SQL.DROP_ADJACENT_TABLE.value)
            afe_db.execute_ddl(AFEDB.SQL.CREATE_ADJACENT_TABLE.value)
            
            afe_db.execute_ddl(AFEDB.SQL.DROP_CODEV_TABLE.value)
            afe_db.execute_ddl(AFEDB.SQL.CREATE_CODEV_TABLE.value)
            
            afe_db.execute_ddl(AFEDB.SQL.DROP_PARENT_CHILD_TABLE.value)
            afe_db.execute_ddl(AFEDB.SQL.CREATE_PARENT_CHILD_TABLE.value)
            
            afe_db.execute_ddl(AFEDB.SQL.DROP_WELL_GROUP_TABLE.value)
            afe_db.execute_ddl(AFEDB.SQL.CREATE_WELL_GROUP_TABLE.value)
            
            afe_db.execute_ddl(AFEDB.SQL.DROP_WELL_GROUP_MEMBER_TABLE.value)
            afe_db.execute_ddl(AFEDB.SQL.CREATE_WELL_GROUP_MEMBER_TABLE.value)

            logger.info(f"{task}: {self.context.logs_path}")
        except Exception as e:
            logger.error(f"Error {task} workflow task: {e}\n{format_exc()}")
            raise ValueError(f"Error {task} workflow task: {e}")