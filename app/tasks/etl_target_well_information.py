from tasks.task import Task
from tasks.task_enum import TASKS
from helpers import (task_logger, 
                     spc_feet_to_latlon)
from services import (TargetWellInformationService, 
                      TexasLandSurveySystemService, 
                      NewMexicoLandSurveySystemService)
from traceback import format_exc

class ETLTargetWellInformation(Task):

    def execute(self):
        task = TASKS.ETL_TARGET_WELL_INFORMATION.value
        logger = task_logger(task, self.context.logs_path)
        try:
            tlss_service = TexasLandSurveySystemService(self.context._texas_land_survey_system_database_path)
            nmlss_service = NewMexicoLandSurveySystemService(self.context._new_mexico_land_survey_system_database_path)
            target_well_information_service = TargetWellInformationService(db_path=self.context.db_path)            

            # Create offset target well information
            for target_well in target_well_information_service.get_all():
                # Validation

                # Ensure the XY coordinates are provided
                if (target_well.x_surface_location is None or
                    target_well.y_surface_location is None or
                    target_well.x_first_take_point is None or
                    target_well.y_first_take_point is None or
                    target_well.x_last_take_point is None or
                    target_well.y_last_take_point is None or
                    target_well.x_bottom_hole is None or
                    target_well.y_bottom_hole is None or
                    target_well.nad_system is None or
                    target_well.nad_zone is None):
                    message = f"Ensure the XY coordinates and NAD system and zone are provided"
                    raise ValueError(message)
                
                # Ensure state specific information is provided
                if target_well.state == "TX":

                    # Coorelate NAD System and Zone to Datum and SPC Zone
                    if "NAD27" == target_well.nad_system:
                        inDatum = "NAD27"
                        outDatum = "NAD27"
                    elif "NAD83" == target_well.nad_system:
                        inDatum = "NAD83(2011)"
                        outDatum = "NAD83(2011)"
                    else:
                        raise ValueError(f"NAD System {target_well.nad_system} is not supported")
                     
                    if "TX(C)" == target_well.nad_zone or "C" == target_well.nad_zone:
                        spcZone = 4203
                    else:
                        raise ValueError(f"NAD Zone {target_well.nad_zone} is not supported")
                    
                    if (target_well.tx_abstract_southwest_corner is None or 
                        target_well.tx_block_southwest_corner is None or 
                        target_well.nm_tx_section_southwest_corner is None):
                        message = f"TX Abstract, Block, and Section must be provided"
                        raise ValueError(message)
                    else:
                        tlss = tlss_service.get_by_county_abstract(county=target_well.county, abstract=target_well.tx_abstract_southwest_corner)
                        if tlss is None:
                            raise ValueError(f"PLSS not found for {target_well.state}, {target_well.county}, {target_well.tx_block_southwest_corner}, {target_well.nm_tx_section_southwest_corner}")    
                elif target_well.state == "NM":

                    # Coorelate NAD System and Zone to Datum and SPC Zone
                    if "NAD27" == target_well.nad_system:
                        inDatum = "NAD27"
                        outDatum = "NAD27"
                    elif "NAD83" == target_well.nad_system:
                        inDatum = "NAD83(2011)"
                        outDatum = "NAD83(2011)"
                    else:
                        raise ValueError(f"NAD System {target_well.nad_system} is not supported")
                     
                    if "E" == target_well.nad_zone or "East" == target_well.nad_zone:
                        spcZone = 3001
                    else:
                        raise ValueError(f"NAD Zone {target_well.nad_zone} is not supported")
                    
                    if (target_well.nw_township_southwest_corner is None or
                        target_well.nm_range_southwest_corner is None or 
                        target_well.nm_tx_section_southwest_corner is None):
                        message = f"NM Township, Range, and Section must be provided"
                        raise ValueError(message)
                    else:
                        township = int(target_well.nw_township_southwest_corner[:-1])
                        township_direction = target_well.nw_township_southwest_corner[-1]
                        range = int(target_well.nm_range_southwest_corner[:-1])
                        range_direction = target_well.nm_range_southwest_corner[-1]
                        section = int(target_well.nm_tx_section_southwest_corner)
                        nmlss = nmlss_service.get_by_township_range_section(township=township, township_direction=township_direction, range=range, range_direction=range_direction, section=section)
                        if nmlss is None:
                            raise ValueError(f"PLSS not found for {target_well.state}, {target_well.nw_township_southwest_corner}, {target_well.nm_range_southwest_corner}, {target_well.nm_tx_section_southwest_corner}")
                else:
                    raise ValueError(f"We do not currently support the state of {target_well.state}")

                # Ensure landing zone is provided
                if target_well.afe_landing_zone is None:
                    raise ValueError(f"Logs landing zone must be provided")
                
                # Ensure perforation interval is provided
                if target_well.surveys_preforated_interval_ft is None or target_well.surveys_preforated_interval_ft <= 0:
                    raise ValueError(f"Perforation interval must be provided")
                
                # Ensure subsurface depth is provided
                if target_well.bhl_tvd_ss_ft is None:
                    raise ValueError(f"Subsurface depth must be provided")
                
                # Convert XYs to Latitudes and Longitudes; using Firt Take and Last Take Points.
                target_well.latitude_surface_location, target_well.longitude_surface_location = spc_feet_to_latlon(northing=target_well.y_surface_location,
                                                                                                                easting=target_well.x_surface_location,
                                                                                                                spcZone=spcZone,
                                                                                                                inDatum=inDatum)
                
                target_well.latitude_first_take_point, target_well.longitude_first_take_point = spc_feet_to_latlon(northing=target_well.y_first_take_point,
                                                                                                                easting=target_well.x_first_take_point,
                                                                                                                spcZone=spcZone,
                                                                                                                inDatum=inDatum)

                target_well.latitude_last_take_point, target_well.longitude_last_take_point = spc_feet_to_latlon(northing=target_well.y_last_take_point,
                                                                                                                 easting=target_well.x_last_take_point,
                                                                                                                 spcZone=spcZone,
                                                                                                                 inDatum=inDatum)

                target_well.latitude_bottom_hole, target_well.longitude_bottom_hole = spc_feet_to_latlon(northing=target_well.y_bottom_hole,
                                                                                                         easting=target_well.x_bottom_hole,
                                                                                                         spcZone=spcZone,
                                                                                                         inDatum=inDatum)
                target_well_information_service.update(target_well)
                
            logger.info(f"{task}: {self.context.logs_path}")
        except Exception as e:
            logger.error(f"Error {task} workflow task: {e}\n{format_exc()}")
            raise ValueError(f"Error {task} workflow task: {e}")