
from tasks.task import Task
from tasks.task_enum import TASKS
from helpers import task_logger
from database import AFEDB
from traceback import format_exc
from sqlite3 import connect
from database import AFEDB

from pandas import read_excel

class LoadLookupTables(Task):

    def _load_stratigrpahic(self):
        try:
            afe_db = AFEDB(self.context.db_path)
            afe_db.execute_ddl(AFEDB.SQL.DROP_STRATIGRAPHIC_TABLE.value)
            afe_db.execute_ddl(AFEDB.SQL.CREATE_STRATIGRAPHIC_TABLE.value)
            stratigraphic = read_excel(self.context.stratigraphic_file_path)
            connection = connect(self.context.db_path)
            stratigraphic.to_sql('stratigraphic', 
                                 connection, 
                                 if_exists='replace', 
                                 index=False, 
                                 dtype={"period":"TEXT", 
                                        "epoch": "TEXT", 
                                        "basin": "TEXT", 
                                        "formation": "TEXT", 
                                        "union_code": "TEXT", 
                                        "prism_code": "TEXT", 
                                        "position": "INTEGER",
                                        'color': 'TEXT'})
        except Exception as e:
            raise ValueError(f"Error loading stratigraphic: {e}")
        
    def _load_stratigraphic_command_tanks(self):
        try:
            afe_db = AFEDB(self.context.db_path)
            afe_db.execute_ddl(AFEDB.SQL.DROP_STRATIGRAPHIC_COMMON_TANKS_TABLE.value)
            afe_db.execute_ddl(AFEDB.SQL.CREATE_STRATIGRAPHIC_COMMON_TANKS_TABLE.value)
            stratigraphic_common_tanks = read_excel(self.context.stratigraphic_common_tanks_file_path)
            connection = connect(self.context.db_path)
            stratigraphic_common_tanks.to_sql('stratigraphic_common_tanks', 
                                              connection, 
                                              if_exists='replace', 
                                              index=False, 
                                              dtype={"union_code":"TEXT", 
                                                     "common_tank": "TEXT"})
        except Exception as e:
            raise ValueError(f"Error loading stratigraphic common tanks: {e}")
    def execute(self):
        task = TASKS.LOAD_LOOKUP_TABLES.value
        logger = task_logger(task, self.context.logs_path)
        try:
            self._load_stratigrpahic()
            self._load_stratigraphic_command_tanks()

            logger.info(f"{task}: {self.context.logs_path}")
        except Exception as e:
            logger.error(f"Error {task} workflow task: {e}\n{format_exc()}")
            raise ValueError(f"Error {task} workflow task: {e}")