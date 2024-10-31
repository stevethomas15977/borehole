from tasks.task import Task
from tasks.task_enum import TASKS
from helpers import task_logger
from traceback import format_exc
from services import (GunBarrelService, AnalysisService)
import math

class CalculateWellOverlapPercentage(Task):

    debug = False

    def execute(self):
        task = TASKS.CALCULATE_WELL_OVERLAP_PERCENTAGE.value
        logger = task_logger(task, self.context.logs_path)
        try:
            gun_barrel_service = GunBarrelService(self.context.db_path)
            analysis_service = AnalysisService(self.context.db_path)

            # Get all gun barrels
            gun_barrels = gun_barrel_service.select_all()
            for gun_barrel in gun_barrels:
                target_well = analysis_service.get_by_api(gun_barrel.target_well_api)
                offset_well = analysis_service.get_by_api(gun_barrel.offset_well_api)
                if target_well.dominant_direction == 'N' and offset_well.dominant_direction == 'S':
                    overlap = int(target_well.lateral_length)
                    if target_well.lateral_end_grid_y - offset_well.lateral_start_grid_y > 0:
                        overlap = overlap - int((target_well.lateral_end_grid_y - offset_well.lateral_start_grid_y))
                    if target_well.lateral_start_grid_y - offset_well.lateral_end_grid_y < 0:
                        overlap = overlap - int(abs(target_well.lateral_start_grid_y - offset_well.lateral_end_grid_y))
                    overlap_percentage = math.ceil((overlap/target_well.lateral_length)*100)
                    gun_barrel.overlap_feet = overlap
                    gun_barrel.overlap_percentage = overlap_percentage
                    gun_barrel_service.update(gun_barrel)
                if target_well.dominant_direction == 'N' and offset_well.dominant_direction == 'N':
                    overlap = int(target_well.lateral_length)
                    if target_well.lateral_end_grid_y - offset_well.lateral_end_grid_y > 0:
                        overlap = overlap - int((target_well.lateral_end_grid_y - offset_well.lateral_end_grid_y))
                    if target_well.lateral_start_grid_y - offset_well.lateral_start_grid_y < 0:
                        overlap = overlap - int(abs(target_well.lateral_start_grid_y - offset_well.lateral_start_grid_y))
                    overlap_percentage = math.ceil((overlap/target_well.lateral_length)*100)
                    gun_barrel.overlap_feet = overlap
                    gun_barrel.overlap_percentage = overlap_percentage
                    gun_barrel_service.update(gun_barrel)
            logger.info(f"{task}: {self.context.logs_path}")
        except Exception as e:
            logger.error(f"Error {task} workflow task: {e}\n{format_exc()}")
            raise ValueError(f"Error {task} workflow task: {e}")