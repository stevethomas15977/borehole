from tasks.task import Task
from tasks.task_enum import TASKS
from helpers import task_logger, is_within_y_range, is_within_x_range, are_lengths_similar
from traceback import format_exc

from services import (AnalysisService, TargetWellInformationService, GunBarrelService)
from models import (Analysis, XYZDistance, GunBarrel)

class DetermineWellSpacingGunBarrelPlotWells(Task):

    def execute(self):
        task = TASKS.DETERMINE_WELL_SPACING_GUN_BARREL_PLOT_WELLS.value
        logger = task_logger(task, self.context.logs_path)
        try:
            analysis_service = AnalysisService(self.context.db_path)
            target_well_information_service = TargetWellInformationService(self.context.db_path)
            gun_barrel_service = GunBarrelService(self.context.db_path)
            shallowest = target_well_information_service.get_shallowest() - self.context.depth_distance_threshold
            deepest = target_well_information_service.get_deepest() + self.context.depth_distance_threshold

            # Get all target wells analysis
            analyses = analysis_service.get_simulated_target_wells()

            # Determine the eastern, western, northern, and southern target wells
            eastern_target_well = None
            western_target_well = None
            northern_target_well = None
            southern_target_well = None
            additonal_western_target_wells = []
            additonal_eastern_target_wells = []
            additional_northern_target_wells = []
            additional_southern_target_wells = []
            for analysis in analyses:
                target_well = analysis
                if target_well.dominant_direction in ['N', 'S']:
                    if eastern_target_well is None:
                        eastern_target_well = target_well
                    else:
                        if target_well.lateral_end_grid_x > eastern_target_well.lateral_end_grid_x:
                            additonal_eastern_target_wells.append(eastern_target_well)
                            eastern_target_well = target_well
                        else:
                            additonal_eastern_target_wells.append(target_well)

                    if western_target_well is None:
                        western_target_well = target_well
                    else:
                        if target_well.lateral_end_grid_x < western_target_well.lateral_end_grid_x:
                            additonal_western_target_wells.append(western_target_well)
                            western_target_well = target_well
                        else:
                            additonal_western_target_wells.append(target_well)

                if target_well.dominant_direction in ['E', 'W']:
                    if northern_target_well is None:
                        northern_target_well = target_well
                    else:
                        if target_well.lateral_end_grid_y > northern_target_well.lateral_end_grid_y:
                            additional_northern_target_wells.append(northern_target_well)
                            northern_target_well = target_well
                        else:
                            additional_northern_target_wells.append(target_well)

                    if southern_target_well is None:
                        southern_target_well = target_well
                    else:
                        if target_well.lateral_end_grid_y < southern_target_well.lateral_end_grid_y:
                            additional_southern_target_wells.append(southern_target_well)
                            southern_target_well = target_well
                        else:
                            additional_southern_target_wells.append(target_well)

            if eastern_target_well:
                for offset_well in analysis_service.get_all():
                    x_in = False
                    y_in = False
                    z_in = False
                    if '00-000' in offset_well.api or '11-111' in offset_well.api:
                        continue
                    if ((offset_well.lateral_start_grid_x > eastern_target_well.lateral_start_grid_x) and
                        (offset_well.lateral_midpoint_grid_x > eastern_target_well.lateral_midpoint_grid_x) and
                        (offset_well.lateral_end_grid_x > eastern_target_well.lateral_end_grid_x)):
                        if ((offset_well.lateral_start_grid_x - eastern_target_well.lateral_start_grid_x <= 2640) and
                            (offset_well.lateral_midpoint_grid_x - eastern_target_well.lateral_midpoint_grid_x <= 2640) and
                            (offset_well.lateral_end_grid_x - eastern_target_well.lateral_end_grid_x <= 2640)):
                            x_in = True
                    if ((is_within_y_range(eastern_target_well.lateral_start_grid_y, eastern_target_well.lateral_end_grid_y, offset_well.lateral_start_grid_y) == True) or
                        (is_within_y_range(eastern_target_well.lateral_start_grid_y, eastern_target_well.lateral_end_grid_y, offset_well.lateral_midpoint_grid_y) == True) or
                        (is_within_y_range(eastern_target_well.lateral_start_grid_y, eastern_target_well.lateral_end_grid_y, offset_well.lateral_end_grid_y)) == True):
                        y_in = True
                    if (abs(offset_well.subsurface_depth) > shallowest or abs(offset_well.subsurface_depth) < deepest):
                        z_in = True
                    if x_in and y_in and z_in:
                        gun_barrel = GunBarrel(target_well_api=eastern_target_well.api, offset_well_api=offset_well.api)
                        gun_barrel_service.insert(gun_barrel)

            if western_target_well:
                for offset_well in analysis_service.get_all():
                    x_in = False
                    y_in = False
                    z_in = False
                    if '00-000' in offset_well.api or '11-111' in offset_well.api:
                        continue
                    if ((offset_well.lateral_start_grid_x < western_target_well.lateral_start_grid_x) and
                        (offset_well.lateral_midpoint_grid_x < western_target_well.lateral_midpoint_grid_x) and
                        (offset_well.lateral_end_grid_x < western_target_well.lateral_end_grid_x)):
                        if ((western_target_well.lateral_start_grid_x - offset_well.lateral_start_grid_x <= 2640) and
                            (western_target_well.lateral_midpoint_grid_x - offset_well.lateral_midpoint_grid_x <= 2640) and
                            (western_target_well.lateral_end_grid_x - offset_well.lateral_end_grid_x <= 2640)):
                            x_in = True
                    if ((is_within_y_range(western_target_well.lateral_start_grid_y, western_target_well.lateral_end_grid_y, offset_well.lateral_start_grid_y) == True) or
                        (is_within_y_range(western_target_well.lateral_start_grid_y, western_target_well.lateral_end_grid_y, offset_well.lateral_midpoint_grid_y) == True) or
                        (is_within_y_range(western_target_well.lateral_start_grid_y, western_target_well.lateral_end_grid_y, offset_well.lateral_end_grid_y)) == True):
                        y_in = True
                    if (abs(offset_well.subsurface_depth) > shallowest or abs(offset_well.subsurface_depth) < deepest):
                        z_in = True
                    if x_in and y_in and z_in:
                        gun_barrel = GunBarrel(target_well_api=western_target_well.api, offset_well_api=offset_well.api)
                        gun_barrel_service.insert(gun_barrel)

            # Add eastern additional target wells
            for eastern_target_well in additonal_eastern_target_wells:
                for offset_well in analysis_service.get_all():
                    x_in = False
                    y_in = False
                    z_in = False
                    if '00-000' in offset_well.api or '11-111' in offset_well.api:
                        continue
                    if ((offset_well.lateral_start_grid_x > eastern_target_well.lateral_start_grid_x) and
                        (offset_well.lateral_midpoint_grid_x > eastern_target_well.lateral_midpoint_grid_x) and
                        (offset_well.lateral_end_grid_x > eastern_target_well.lateral_end_grid_x)):
                        if ((offset_well.lateral_start_grid_x - eastern_target_well.lateral_start_grid_x <= 2640) and
                            (offset_well.lateral_midpoint_grid_x - eastern_target_well.lateral_midpoint_grid_x <= 2640) and
                            (offset_well.lateral_end_grid_x - eastern_target_well.lateral_end_grid_x <= 2640)):
                            x_in = True
                    if ((is_within_y_range(eastern_target_well.lateral_start_grid_y, eastern_target_well.lateral_end_grid_y, offset_well.lateral_start_grid_y) == True) or
                        (is_within_y_range(eastern_target_well.lateral_start_grid_y, eastern_target_well.lateral_end_grid_y, offset_well.lateral_midpoint_grid_y) == True) or
                        (is_within_y_range(eastern_target_well.lateral_start_grid_y, eastern_target_well.lateral_end_grid_y, offset_well.lateral_end_grid_y)) == True):
                        y_in = True
                    if (abs(offset_well.subsurface_depth) > shallowest or abs(offset_well.subsurface_depth) < deepest):
                        z_in = True
                    if x_in and y_in and z_in:
                        gun_barrel = GunBarrel(target_well_api=eastern_target_well.api, offset_well_api=offset_well.api)
                        gun_barrel_service.insert(gun_barrel)

            # Add western additional target wells
            for western_target_well in additonal_western_target_wells:
                for offset_well in analysis_service.get_all():
                    x_in = False
                    y_in = False
                    z_in = False
                    if '00-000' in offset_well.api or '11-111' in offset_well.api:
                        continue
                    if ((offset_well.lateral_start_grid_x < western_target_well.lateral_start_grid_x) and
                        (offset_well.lateral_midpoint_grid_x < western_target_well.lateral_midpoint_grid_x) and
                        (offset_well.lateral_end_grid_x < western_target_well.lateral_end_grid_x)):
                        if ((western_target_well.lateral_start_grid_x - offset_well.lateral_start_grid_x <= 2640) and
                            (western_target_well.lateral_midpoint_grid_x - offset_well.lateral_midpoint_grid_x <= 2640) and
                            (western_target_well.lateral_end_grid_x - offset_well.lateral_end_grid_x <= 2640)):
                            x_in = True
                    if ((is_within_y_range(western_target_well.lateral_start_grid_y, western_target_well.lateral_end_grid_y, offset_well.lateral_start_grid_y) == True) or
                        (is_within_y_range(western_target_well.lateral_start_grid_y, western_target_well.lateral_end_grid_y, offset_well.lateral_midpoint_grid_y) == True) or
                        (is_within_y_range(western_target_well.lateral_start_grid_y, western_target_well.lateral_end_grid_y, offset_well.lateral_end_grid_y)) == True):
                        y_in = True
                    if (abs(offset_well.subsurface_depth) > shallowest or abs(offset_well.subsurface_depth) < deepest):
                        z_in = True
                    if x_in and y_in and z_in:
                        gun_barrel = GunBarrel(target_well_api=western_target_well.api, offset_well_api=offset_well.api)
                        gun_barrel_service.insert(gun_barrel)

            # TODO Northern target well

            # TODO Southern target well

            logger.info(f"{task}: {self.context.logs_path}")
        except Exception as e:
            logger.error(f"Error {task} workflow task: {e}\n{format_exc()}")
            raise ValueError(f"Error {task} workflow task: {e}")