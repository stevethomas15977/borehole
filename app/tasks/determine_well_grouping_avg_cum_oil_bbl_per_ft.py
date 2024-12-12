from tasks.task import Task
from tasks.task_enum import TASKS
from helpers import task_logger
from services import WellGroupService, AnalysisService
from traceback import format_exc

class DetermineWellGroupingAvgCumOilBblPerFT(Task):

    def execute(self):
        task = TASKS.DETERMINE_WELL_GROUPING_AVG_CUM_OIL_BBL_PER_FT.value
        logger = task_logger(task, self.context.logs_path)
        try:
            well_group_service = WellGroupService(db_path=self.context.db_path)
            analysis_service = AnalysisService(db_path=self.context.db_path)
            for well_group in well_group_service.get_all():
                avg_group_cumoil_per_ft = analysis_service.get_group_avg_cumoil_bbl_per_ft(group_id=well_group.name)
                well_group.avg_cumoil_per_ft = avg_group_cumoil_per_ft
                well_group_service.update(well_group)
            logger.info(f"{task}: {self.context.logs_path}")
        except Exception as e:
            logger.error(f"Error {task} workflow task: {e}\n{format_exc()}")
            raise ValueError(f"Error {task} workflow task: {e}")