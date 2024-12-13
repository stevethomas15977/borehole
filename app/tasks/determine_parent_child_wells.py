from tasks.task import Task
from tasks.task_enum import TASKS
from helpers import task_logger
from traceback import format_exc

from helpers import is_at_least_6_months_earlier, months_between_dates
from services import (AnalysisService, LatitudeLongitudeDistanceService, AdjacentService, WellGroupService)
from models import ParentChild

class DetermineParentChildWells(Task):

    def execute(self):
        task = TASKS.DETERMINE_PARENT_CHILD_WELLS.value
        logger = task_logger(task, self.context.logs_path)
        try:
            analysis_service = AnalysisService(db_path=self.context.db_path)
            distance_service = LatitudeLongitudeDistanceService(db_path=self.context.db_path)
            adjacent_service = AdjacentService(db_path=self.context.db_path)
            well_group_service = WellGroupService(db_path=self.context.db_path)

            analyses = analysis_service.get()

            parentchildren = []

            for analysis in analyses:
                distances = distance_service.get_by_reference_api(analysis.api)
                parents = []
                for distance in distances:
                    if distance.end_hypotenuse <= 1800:
                        parent_analysis = analysis_service.get_by_name(distance.target_name)
                        if ((parent_analysis.first_production_date is None or parent_analysis.first_production_date == "None") or
                            (analysis.first_production_date is None or analysis.first_production_date == "None")):
                            logger.error(f"First production date is missing for {parent_analysis.name} or {analysis.name}")  
                            continue
                        if is_at_least_6_months_earlier(parent_date=parent_analysis.first_production_date, 
                                                        child_date=analysis.first_production_date):
                            if parent_analysis.name not in parents:
                                parentchild = ParentChild(parent_api=parent_analysis.api, 
                                                          parent_name=parent_analysis.name,
                                                          child_api=analysis.api,
                                                          child_name=analysis.name,
                                                          parent_interval=parent_analysis.interval,
                                                          child_interval=analysis.interval)
                                parents.append(parent_analysis.name)
                                adjacent = adjacent_service.get_by_apis(reference_api=parent_analysis.api, 
                                                                        target_api=analysis.api)
                                analysis.child = "Yes"
                                if adjacent:
                                    parentchild.adjacent = "Yes"
                                    analysis.adjacent_child = "Yes"
                                else:
                                    analysis.adjacent_child = "No"
                                    analysis.sibling = analysis.name
                                    parentchild.adjacent = "No"
                                    parentchild.sibling_api = analysis.api
                                    parentchild.sibling_name = analysis.name

                                if analysis.group_id is not None:
                                    well_group = well_group_service.get_by_name(analysis.group_id)
                                    if well_group is not None and well_group.avg_cumoil_per_ft > 0:
                                        analysis.pct_of_group_cumoil_bblperft = round((analysis.cumoil_bblperft / well_group.avg_cumoil_per_ft) * 100, 2)
                                        if analysis.pct_of_group_cumoil_bblperft > self.context.pct_group_cum_oil_greater_than_threshold:
                                            analysis.pct_of_group_cumoil_bblperft_greater_than = "Yes"

                                parentchildren.append(parentchild)
                                analysis_service.update(analysis)
                if len(parents) > 0:
                    analysis.parents = len(parents)
                    if len(parents) == 1:
                        analysis.parent_1 = parents[0]
                        parent_analysis = analysis_service.get_by_name(parents[0])
                        analysis.parent_1_first_production_date = parent_analysis.first_production_date
                        analysis.parent_1_delta_first_production_months = months_between_dates(parent_analysis.first_production_date, analysis.first_production_date)
                    elif len(parents) == 2:
                        analysis.parent_1 = parents[0]
                        parent_analysis = analysis_service.get_by_name(parents[0])
                        analysis.parent_1_first_production_date = parent_analysis.first_production_date
                        analysis.parent_1_delta_first_production_months = months_between_dates(parent_analysis.first_production_date, analysis.first_production_date)
                        analysis.parent_1_interval = parent_analysis.interval
                        analysis.parent_2 = parents[1]
                        parent_analysis = analysis_service.get_by_name(parents[1])
                        analysis.parent_2_first_production_date = parent_analysis.first_production_date
                        analysis.parent_2_delta_first_production_months = months_between_dates(parent_analysis.first_production_date, analysis.first_production_date)
                        analysis.parent_2_interval = parent_analysis.interval
                    analysis_service.update(analysis)
                    
            logger.info(f"{task}: {self.context.logs_path}")
        except Exception as e:
            logger.error(f"Error {task} workflow task: {e}\n{format_exc()}")
            raise ValueError(f"Error {task} workflow task: {e}")