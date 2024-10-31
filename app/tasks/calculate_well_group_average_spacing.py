from tasks.task import Task
from tasks.task_enum import TASKS
from helpers import task_logger
from traceback import format_exc
import math

from services import (WellGroupService, 
                      WellGroupMemberService, 
                      AnalysisService, 
                      AdjacentService)
from models import Adjacent
class CalculateWellGroupAverageSpacing(Task):

    def execute(self):
        task = TASKS.CALCULATE_WELL_GROUP_AVERAGE_SPACING.value
        logger = task_logger(task, self.context.logs_path)
        try:
            wellgroup_service = WellGroupService(self.context.db_path)
            wellgroupmember_service = WellGroupMemberService(self.context.db_path) 
            analysis_service = AnalysisService(self.context.db_path)
            adjacent_service = AdjacentService(self.context.db_path)
            
            for group in wellgroup_service.get_all():
                group_members = wellgroupmember_service.get_all_group_name(group_name=group.name)
                reference_apis = [member.well_api for member in group_members]
                adjacent_list = list[Adjacent](adjacent_service.get_list_by_reference_apis(reference_apis=reference_apis))
                horizontal_numerator = 0
                horizontal_denominator = 0
                hypotenuse_numerator = 0
                hypotenuse_denominator = 0
                for adjacent in adjacent_list:
                    if adjacent.east is not None:
                        horizontal_numerator += adjacent.east
                        horizontal_denominator += 1
                    if adjacent.west is not None:
                        horizontal_numerator += adjacent.west
                        horizontal_denominator += 1
                    if adjacent.hypotenuse is not None:
                        hypotenuse_numerator += adjacent.hypotenuse
                        hypotenuse_denominator += 1

                for adjacent in adjacent_list:
                    analysis = analysis_service.get_by_api(api=adjacent.reference_api)
                    analysis.group_average_horizontal_spacing = math.ceil(horizontal_numerator/horizontal_denominator)
                    analysis.group_average_hypotenuse_spacing = math.ceil(hypotenuse_numerator/hypotenuse_denominator)
                    analysis_service.update(analysis=analysis)

            logger.info(f"{task}: {self.context.logs_path}")
        except Exception as e:
            logger.error(f"Error {task} workflow task: {e}\n{format_exc()}")
            raise ValueError(f"Error {task} workflow task: {e}")