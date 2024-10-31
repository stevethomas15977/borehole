from tasks.task import Task
from tasks.task_enum import TASKS
from helpers import task_logger
from traceback import format_exc

from helpers import (compare_first_production_date_days)
from models import Codevelopment
from services import (CodevelopmentService, 
                      AdjacentService, 
                      AnalysisService)
class DetermineCodevelopmentWells(Task):

    def execute(self):
        task = TASKS.DETERMINE_CODEVELOPMENT_WELLS.value
        logger = task_logger(task, self.context.logs_path)
        try:
            adjacent_service = AdjacentService(db_path=self.context.db_path)
            analysis_service = AnalysisService(db_path=self.context.db_path)
            adjacents = adjacent_service.get_all()
            codevelopments = []
            for adjacent in adjacents:
                if "00-000" in adjacent.reference_api or "11-111" in adjacent.target_api:
                    continue
                reference_analysis = analysis_service.get_by_api(api=adjacent.reference_api)
                target_analysis = analysis_service.get_by_api(api=adjacent.target_api)

                if ((reference_analysis.first_production_date is None or reference_analysis.first_production_date == "None") or
                    (target_analysis.first_production_date is None or target_analysis.first_production_date == "None")):
                        logger.error(f"First production date is missing for {reference_analysis.name} or {target_analysis.name}")  
                        continue
                
                # Mark as codeveloopment, if the first production date of the target well is at least 6 months after the reference well
                if compare_first_production_date_days(date1=reference_analysis.first_production_date, 
                                                      date2=target_analysis.first_production_date,
                                                      threshold=int(self.context.codevelopment_first_production_date_days_threshold)):
                    codevelopment = Codevelopment(reference_api=reference_analysis.api,
                                                  target_api=target_analysis.api,
                                                  reference_name=reference_analysis.name, 
                                                  target_name=target_analysis.name)
                    codevelopments.append(codevelopment)
                    reference_analysis.codevelopment = "Yes"
                    analysis_service.update(reference_analysis)

            codevelopment_service = CodevelopmentService(db_path=self.context.db_path)
            codevelopment_service.add(codevelopments)
            logger.info(f"{task}: {self.context.logs_path}")
        except Exception as e:
            logger.error(f"Error {task} workflow task: {e}\n{format_exc()}")
            raise ValueError(f"Error {task} workflow task: {e}")