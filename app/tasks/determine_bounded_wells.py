from tasks.task import Task
from tasks.task_enum import TASKS
from helpers import task_logger
from traceback import format_exc

from services import (AdjacentService, AnalysisService)

class DetermineBoundedWells(Task):

    def execute(self):
        task = TASKS.DETERMINE_BOUNDED_WELLS.value
        logger = task_logger(task, self.context.logs_path)
        try:
            adjacent_service = AdjacentService(db_path=self.context.db_path)
            analysis_service = AnalysisService(db_path=self.context.db_path)
            analyses = analysis_service.get()
            for analysis in analyses:
                adjacents = adjacent_service.get_list_by_reference_apis(reference_apis=[analysis.api]) 
                if adjacents is not None:
                    if len(adjacents) == 0:
                        analysis.bound = "Unbound"
                        analysis_service.update(analysis)  
                    if len(adjacents) == 1:
                        analysis.bound = "Half-Bound"
                        analysis_service.update(analysis)
                    elif len(adjacents) == 2:
                        analysis.bound = "Bound"
                        analysis_service.update(analysis)  
            logger.info(f"{task}: {self.context.logs_path}")
        except Exception as e:
            logger.error(f"Error {task} workflow task: {e}\n{format_exc()}")
            raise ValueError(f"Error {task} workflow task: {e}")