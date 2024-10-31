from models import Analysis
from tasks.task import Task
from tasks.task_enum import TASKS
from helpers import (task_logger, 
                     compass_direction, 
                     calculate_bearing, 
                     adjust_coordinate, 
                     latlon_to_utm_feet, 
                     swope_direction,
                     spc_feet_to_latlon)
from services import (TargetWellInformationService, 
                        TexasLandSurveySystemService, 
                        NewMexicoLandSurveySystemService,
                        AnalysisService)
from traceback import format_exc
from datetime import datetime, timedelta

class CreateSimulatedWell(Task):

    def execute(self):
        task = TASKS.CREATE_SIMULATED_WELL.value
        logger = task_logger(task, self.context.logs_path)
        try:
            tlss_service = TexasLandSurveySystemService(self.context._texas_land_survey_system_database_path)
            nmlss_service = NewMexicoLandSurveySystemService(self.context._new_mexico_land_survey_system_database_path)
            target_well_information_service = TargetWellInformationService(db_path=self.context.db_path)            
            analysis_service = AnalysisService(db_path=self.context.db_path)

            target_well = target_well_information_service.get_first_row()
            target_well_analysis = analysis_service.get_by_name(target_well.name)

            if target_well.state == "TX":
                tlss = tlss_service.get_by_county_abstract(county=target_well.county, abstract=target_well.tx_abstract_southwest_corner)
                if tlss is None:
                    logger.error(f"PLSS not found for {target_well.county}, {target_well.tx_block_southwest_corner}, {target_well.nm_tx_section_southwest_corner}")
                    raise ValueError(f"PLSS not found for {target_well.county}, {target_well.tx_block_southwest_corner}, {target_well.nm_tx_section_southwest_corner}")    
                else:
                    southwest_latitude = tlss.southwest_latitude
                    southwest_longitude = tlss.southwest_longitude
                simulated_well_name = f"Simulated-Well-{target_well.state}-{target_well.county}-{target_well.tx_abstract_southwest_corner}-{target_well.tx_block_southwest_corner}-{target_well.nm_tx_section_southwest_corner}"
            elif target_well.state == "NM":
                township = int(target_well.nw_township_southwest_corner[:-1])
                township_direction = target_well.nw_township_southwest_corner[-1]
                range = int(target_well.nm_range_southwest_corner[:-1])
                range_direction = target_well.nm_range_southwest_corner[-1]
                section = int(target_well.nm_tx_section_southwest_corner)
                nmlss = nmlss_service.get_by_township_range_section(township=township, township_direction=township_direction, range=range, range_direction=range_direction, section=section)
                if nmlss is None:
                    logger.error(f"PLSS not found for {target_well.nw_township_southwest_corner}, {target_well.nm_range_southwest_corner}, {target_well.nm_tx_section_southwest_corner}")
                    raise ValueError(f"PLSS not found for {target_well.nw_township_southwest_corner}, {target_well.nm_range_southwest_corner}, {target_well.nm_tx_section_southwest_corner}")
                else:
                    southwest_latitude = nmlss.southwest_latitude
                    southwest_longitude = nmlss.southwest_longitude
                simulated_well_name = f"Simulated-Well-{target_well.state}-{target_well.nw_township_southwest_corner}-{target_well.nm_range_southwest_corner}-{target_well.nm_tx_section_southwest_corner}"
            else:
                logger.error(f"We do not currently support the state {target_well.state}")
                raise ValueError(f"We do not currently support the state {target_well.state}")
            
            # Create simulated well from PLSS and Target Well Information
            simulated_well = Analysis()
            # Set the lateral length to max lateral length of target wells

            simulated_well.lateral_length = target_well_information_service.get_max_lateral_length()
            # TODO: Implement strategy if target wells have a material difference in lateral lengths

            simulated_well.dominant_direction = target_well_analysis.dominant_direction

            # Set the lateral start, midpoint and end latitude and longitude locations
            if simulated_well.dominant_direction == "N":
                simulated_well.lateral_start_latitude = target_well_analysis.lateral_start_latitude
                simulated_well.lateral_start_longitude = southwest_longitude
                simulated_well.lateral_midpoint_latitude, simulated_well.lateral_midpoint_longitude = adjust_coordinate(simulated_well.lateral_start_latitude , simulated_well.lateral_start_longitude , int(simulated_well.lateral_length/2), simulated_well.dominant_direction)
                simulated_well.lateral_end_latitude, simulated_well.lateral_end_longitude = adjust_coordinate(simulated_well.lateral_start_latitude , simulated_well.lateral_start_longitude , simulated_well.lateral_length, simulated_well.dominant_direction)
            elif simulated_well.dominant_direction == "S":
                simulated_well.lateral_start_latitude = target_well_analysis.lateral_start_latitude
                simulated_well.lateral_start_longitude = southwest_longitude
                simulated_well.lateral_midpoint_latitude, simulated_well.lateral_midpoint_longitude = adjust_coordinate(simulated_well.lateral_start_latitude , simulated_well.lateral_start_longitude , int(simulated_well.lateral_length/2), simulated_well.dominant_direction)
                simulated_well.lateral_end_latitude, simulated_well.lateral_end_longitude = adjust_coordinate(simulated_well.lateral_start_latitude , simulated_well.lateral_start_longitude , simulated_well.lateral_length, simulated_well.dominant_direction)
            elif simulated_well.dominant_direction == "W":
                simulated_well.lateral_start_latitude = southwest_latitude
                simulated_well.lateral_start_longitude = target_well_analysis.lateral_start_longitude
                simulated_well.lateral_midpoint_latitude, simulated_well.lateral_midpoint_longitude = adjust_coordinate(simulated_well.lateral_start_latitude , simulated_well.lateral_start_longitude , int(simulated_well.lateral_length/2), simulated_well.dominant_direction)
                simulated_well.lateral_end_latitude, simulated_well.lateral_end_longitude = adjust_coordinate(simulated_well.lateral_start_latitude , simulated_well.lateral_start_longitude , simulated_well.lateral_length, simulated_well.dominant_direction)
            elif simulated_well.dominant_direction == "E":
                simulated_well.lateral_start_latitude = southwest_latitude
                simulated_well.lateral_start_longitude = target_well_analysis.lateral_start_longitude
                simulated_well.lateral_midpoint_latitude, simulated_well.lateral_midpoint_longitude = adjust_coordinate(simulated_well.lateral_start_latitude , simulated_well.lateral_start_longitude , int(simulated_well.lateral_length/2), simulated_well.dominant_direction)
                simulated_well.lateral_end_latitude, simulated_well.lateral_end_longitude = adjust_coordinate(simulated_well.lateral_start_latitude , simulated_well.lateral_start_longitude , simulated_well.lateral_length, simulated_well.dominant_direction)

            # Set the subsurface depth
            simulated_well.subsurface_depth = target_well.bhl_tvd_ss_ft

            # Set first production date
            future_date = datetime.now() + timedelta(days=180)
            formatted_future_date = future_date.strftime("%Y-%m-%d")
            simulated_well.first_production_date = formatted_future_date

            # Set the simulated well name
            simulated_well.api = "00-000-00000"
            simulated_well.name = simulated_well_name
            simulated_well.interval = target_well.logs_landing_zone

            # 6 Set the X, Y, Z coordinates
            simulated_well.lateral_start_grid_x, simulated_well.lateral_start_grid_y = latlon_to_utm_feet(simulated_well.lateral_start_latitude, simulated_well.lateral_start_longitude)
            simulated_well.lateral_start_subsurface_depth = simulated_well.subsurface_depth
            simulated_well.lateral_midpoint_grid_x, simulated_well.lateral_midpoint_grid_y = latlon_to_utm_feet(simulated_well.lateral_midpoint_latitude, simulated_well.lateral_midpoint_longitude)
            simulated_well.lateral_midpoint_subsurface_depth = simulated_well.subsurface_depth
            simulated_well.lateral_end_grid_x, simulated_well.lateral_end_grid_y = latlon_to_utm_feet(simulated_well.lateral_end_latitude, simulated_well.lateral_end_longitude)
            simulated_well.lateral_end_subsurface_depth = simulated_well.subsurface_depth

            # 7. Save the simulated well
            analysis_service.add(simulated_well)

            logger.info(f"{task}: {self.context.logs_path}")
        except Exception as e:
            logger.error(f"Error {task} workflow task: {e}\n{format_exc()}")
            raise ValueError(f"Error {task} workflow task: {e}")