from models import Analysis
from tasks.task import Task
from tasks.task_enum import TASKS
from helpers import (task_logger, 
                     compass_direction, 
                     dominant_direction,
                     calculate_bearing, 
                     adjust_coordinate, 
                     latlon_to_utm_feet, 
                     spc_feet_to_latlon)
from services import (TargetWellInformationService, TexasLandSurveySystemService, AnalysisService)
from traceback import format_exc
from datetime import datetime, timedelta
import random

class CreateTargetWellAnalysis(Task):

    def execute(self):
        task = TASKS.ETL_TARGET_WELL_INFORMATION.value
        logger = task_logger(task, self.context.logs_path)
        try:
            tlss_service = TexasLandSurveySystemService(self.context._texas_land_survey_system_database_path)
            target_well_information_service = TargetWellInformationService(db_path=self.context.db_path)            
            analysis_service = AnalysisService(db_path=self.context.db_path)

            # Create offset target well information
            for target_well in target_well_information_service.get_all():

                analysis = Analysis()
                analysis.api = f"11-111-{random.randint(10000, 99999)}"
                analysis.name = target_well.name
                analysis.interval = target_well.logs_landing_zone
                first_production_date = datetime.now() + timedelta(days=180)
                analysis.first_production_date = first_production_date.strftime("%Y-%m-%d")

                analysis.direction = compass_direction(calculate_bearing(float(target_well.latitude_surface_location), 
                                                        float(target_well.longitude_surface_location), 
                                                        float(target_well.latitude_bottom_hole), 
                                                        float(target_well.longitude_bottom_hole)))
                
                analysis.dominant_direction = dominant_direction(calculate_bearing(float(target_well.latitude_surface_location), 
                                                                                                     float(target_well.longitude_surface_location), 
                                                                                                     float(target_well.latitude_bottom_hole), 
                                                                                                     float(target_well.longitude_bottom_hole)))
                analysis.lateral_length = target_well.surveys_preforated_interval_ft
                analysis.lateral_start_latitude = float(target_well.latitude_first_take_point)
                analysis.lateral_start_longitude = float(target_well.longitude_first_take_point)
                analysis.lateral_midpoint_latitude, analysis.lateral_midpoint_longitude = adjust_coordinate(analysis.lateral_start_latitude , analysis.lateral_start_longitude , int(analysis.lateral_length/2), analysis.dominant_direction)
                analysis.lateral_end_latitude = float(target_well.latitude_last_take_point)
                analysis.lateral_end_longitude = float(target_well.longitude_first_take_point)
                analysis.subsurface_depth = target_well.bhl_tvd_ss_ft
                analysis.lateral_start_grid_x, analysis.lateral_start_grid_y = latlon_to_utm_feet(analysis.lateral_start_latitude, analysis.lateral_start_longitude)
                analysis.lateral_start_subsurface_depth = target_well.bhl_tvd_ss_ft
                analysis.lateral_midpoint_grid_x, analysis.lateral_midpoint_grid_y = latlon_to_utm_feet(analysis.lateral_midpoint_latitude, analysis.lateral_midpoint_longitude)
                analysis.lateral_midpoint_subsurface_depth = target_well.bhl_tvd_ss_ft
                analysis.lateral_end_grid_x, analysis.lateral_end_grid_y = latlon_to_utm_feet(analysis.lateral_end_latitude, analysis.lateral_end_longitude)
                analysis.lateral_end_subsurface_depth = target_well.bhl_tvd_ss_ft
                
                analysis_service.add(analysis)
                
            logger.info(f"{task}: {self.context.logs_path}")
        except Exception as e:
            logger.error(f"Error {task} workflow task: {e}\n{format_exc()}")
            raise ValueError(f"Error {task} workflow task: {e}")