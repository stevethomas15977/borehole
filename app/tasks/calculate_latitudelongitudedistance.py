from tasks.task import Task
from tasks.task_enum import TASKS
from helpers import (task_logger, 
                     calculate_latitude_distance, 
                     calculate_longtitude_distance, 
                     latlon_to_utm_feet, 
                     calculate_3d_distance)
from services import AnalysisService, LatitudeLongitudeDistanceService
from models import LatitudeLongitudeDistance
from traceback import format_exc
import math

class CalculateLatitudeLongitudeDistance(Task):

    def execute(self):
        task = TASKS.CALCULATE_LATITUDE_LONGITUDE_DISTANCE.value
        logger = task_logger(task, self.context.logs_path)
        try:
            analysis_service = AnalysisService(db_path=self.context.db_path)

            reference_analysis = analysis_service.get()
            target_analysis = analysis_service.get()

            latitudelongitudedistance_list = []
            latitudelongitudedistance = None
            
            for reference in reference_analysis:

                # if reference.name not in ['CARR 34-125 UNIT 1H']:
                #     continue   

                for target in target_analysis:

                    # if target.name not in ['AMPHITHEATER A3 15UA']:
                    #     continue 

                    if reference.name == target.name:
                        continue

                   # Case 1 - All wells run north to south
                    if (
                        (reference.dominant_direction == "N" and target.dominant_direction == "N")
                         or (reference.dominant_direction == "S" and target.dominant_direction == "S")
                         or (reference.dominant_direction == "E" and target.dominant_direction == "E")
                         or (reference.dominant_direction == "W" and target.dominant_direction == "W")
                        ):

                        start_latitude_distance = calculate_latitude_distance(reference.lateral_start_latitude,target.lateral_start_latitude)
                        midpoint_latitude_distance = calculate_latitude_distance(reference.lateral_midpoint_latitude,target.lateral_midpoint_latitude)
                        end_latitude_distance = calculate_latitude_distance(reference.lateral_end_latitude,target.lateral_end_latitude)
                        
                        start_longitude_distance = calculate_longtitude_distance(reference.lateral_start_latitude, reference.lateral_start_longitude,target.lateral_start_longitude)
                        midpoint_longitude_distance = calculate_longtitude_distance(reference.lateral_midpoint_latitude, reference.lateral_midpoint_longitude,target.lateral_midpoint_longitude)
                        end_longitude_distance = calculate_longtitude_distance(reference.lateral_end_latitude, reference.lateral_end_longitude, target.lateral_end_longitude)
                                
                        latitudelongitudedistance = LatitudeLongitudeDistance(reference_api=reference.api,
                                                                              reference_name=reference.name,
                                                                              target_api=target.api,
                                                                              target_name=target.name)
                        
                        latitudelongitudedistance.start_latitude = start_latitude_distance
                        latitudelongitudedistance.mid_latitude= midpoint_latitude_distance
                        latitudelongitudedistance.end_latitude = end_latitude_distance
                        latitudelongitudedistance.start_longitude = start_longitude_distance
                        latitudelongitudedistance.mid_longitude = midpoint_longitude_distance
                        latitudelongitudedistance.end_longitude = end_longitude_distance
                        
                        latitudelongitudedistance.start_z = reference.subsurface_depth - target.subsurface_depth
                        latitudelongitudedistance.mid_z = reference.subsurface_depth - target.subsurface_depth
                        latitudelongitudedistance.end_z = reference.subsurface_depth - target.subsurface_depth

                        reference_lateral_start_grid_x, reference_lateral_start_grid_y = latlon_to_utm_feet(reference.lateral_start_latitude, reference.lateral_start_longitude)
                        reference_lateral_midpoint_grid_x, reference_lateral_midpoint_grid_y = latlon_to_utm_feet(reference.lateral_midpoint_latitude, reference.lateral_midpoint_longitude)
                        reference_lateral_end_grid_x, reference_lateral_end_grid_y = latlon_to_utm_feet(reference.lateral_end_latitude, reference.lateral_end_longitude)
                                                
                        target_lateral_start_grid_x, target_lateral_start_grid_y = latlon_to_utm_feet(target.lateral_start_latitude, target.lateral_start_longitude)
                        target_lateral_midpoint_grid_x, target_lateral_midpoint_grid_y = latlon_to_utm_feet(target.lateral_midpoint_latitude, target.lateral_midpoint_longitude)
                        target_lateral_end_grid_x, target_lateral_end_grid_y = latlon_to_utm_feet(target.lateral_end_latitude, target.lateral_end_longitude)
                        
                        latitudelongitudedistance.start_hypotenuse = math.ceil(calculate_3d_distance(reference_lateral_start_grid_x, 
                                                                                                     reference_lateral_start_grid_y, 
                                                                                                     reference.subsurface_depth, 
                                                                                                     target_lateral_start_grid_x, 
                                                                                                     target_lateral_start_grid_y,
                                                                                                     target.subsurface_depth))

                        latitudelongitudedistance.mid_hypotenuse = math.ceil(calculate_3d_distance(reference_lateral_midpoint_grid_x, 
                                                                                                     reference_lateral_midpoint_grid_y, 
                                                                                                     reference.subsurface_depth, 
                                                                                                     target_lateral_midpoint_grid_x, 
                                                                                                     target_lateral_midpoint_grid_y,
                                                                                                     target.subsurface_depth))
                        
                        latitudelongitudedistance.end_hypotenuse = math.ceil(calculate_3d_distance(reference_lateral_end_grid_x, 
                                                                                                     reference_lateral_end_grid_y, 
                                                                                                     reference.subsurface_depth, 
                                                                                                     target_lateral_end_grid_x, 
                                                                                                     target_lateral_end_grid_y,
                                                                                                     target.subsurface_depth))
                        


                    elif (
                        (reference.dominant_direction == "N" and target.dominant_direction == "S")
                         or (reference.dominant_direction == "S" and target.dominant_direction == "N")
                         or (reference.dominant_direction == "E" and target.dominant_direction == "W")
                         or (reference.dominant_direction == "W" and target.dominant_direction == "E")
                        ):

                        # Swope target.end_latitude for target.start_latitude
                        start_latitude_distance = calculate_latitude_distance(reference.lateral_start_latitude,target.lateral_end_latitude)
                        midpoint_latitude_distance = calculate_latitude_distance(reference.lateral_midpoint_latitude,target.lateral_midpoint_latitude)
                        # Swap target.start_latitude for target.end_latitude
                        end_latitude_distance = calculate_latitude_distance(reference.lateral_end_latitude,target.lateral_start_latitude)
                        
                        # Swope target.end_longitude for target.start_longitude
                        start_longitude_distance = calculate_longtitude_distance(reference.lateral_start_latitude, reference.lateral_start_longitude,target.lateral_end_longitude)
                        midpoint_longitude_distance = calculate_longtitude_distance(reference.lateral_midpoint_latitude, reference.lateral_midpoint_longitude,target.lateral_midpoint_longitude)
                        # Swap target.start_longitude for target.end_longitude
                        end_longitude_distance = calculate_longtitude_distance(reference.lateral_end_latitude, reference.lateral_end_longitude, target.lateral_start_longitude)
                        
                        latitudelongitudedistance = LatitudeLongitudeDistance(reference_api=reference.api,
                                                                              reference_name=reference.name,
                                                                              target_api=target.api,
                                                                              target_name=target.name)
                        
                        latitudelongitudedistance.start_latitude = start_latitude_distance
                        latitudelongitudedistance.mid_latitude = midpoint_latitude_distance
                        latitudelongitudedistance.end_latitude = end_latitude_distance
                        latitudelongitudedistance.start_longitude = start_longitude_distance
                        latitudelongitudedistance.mid_longitude = midpoint_longitude_distance
                        latitudelongitudedistance.end_longitude = end_longitude_distance
                        
                        latitudelongitudedistance.start_z = reference.subsurface_depth - target.subsurface_depth
                        latitudelongitudedistance.mid_z = reference.subsurface_depth - target.subsurface_depth
                        latitudelongitudedistance.end_z = reference.subsurface_depth - target.subsurface_depth

                        reference_lateral_start_grid_x, reference_lateral_start_grid_y = latlon_to_utm_feet(reference.lateral_start_latitude, reference.lateral_start_longitude)
                        reference_lateral_midpoint_grid_x, reference_lateral_midpoint_grid_y = latlon_to_utm_feet(reference.lateral_midpoint_latitude, reference.lateral_midpoint_longitude)
                        reference_lateral_end_grid_x, reference_lateral_end_grid_y = latlon_to_utm_feet(reference.lateral_end_latitude, reference.lateral_end_longitude)
                                                
                        target_lateral_start_grid_x, target_lateral_start_grid_y = latlon_to_utm_feet(target.lateral_start_latitude, target.lateral_start_longitude)
                        target_lateral_midpoint_grid_x, target_lateral_midpoint_grid_y = latlon_to_utm_feet(target.lateral_midpoint_latitude, target.lateral_midpoint_longitude)
                        target_lateral_end_grid_x, target_lateral_end_grid_y = latlon_to_utm_feet(target.lateral_end_latitude, target.lateral_end_longitude)
                        
                        # Swope target.end_grid_x and grid_y for target.start_grid_x and grid_y
                        latitudelongitudedistance.start_hypotenuse = math.ceil(calculate_3d_distance(reference_lateral_start_grid_x, 
                                                                                                     reference_lateral_start_grid_y, 
                                                                                                     reference.subsurface_depth, 
                                                                                                     target_lateral_end_grid_x, 
                                                                                                     target_lateral_end_grid_y,
                                                                                                     target.subsurface_depth))

                        latitudelongitudedistance.mid_hypotenuse = math.ceil(calculate_3d_distance(reference_lateral_midpoint_grid_x, 
                                                                                                     reference_lateral_midpoint_grid_y, 
                                                                                                     reference.subsurface_depth, 
                                                                                                     target_lateral_midpoint_grid_x, 
                                                                                                     target_lateral_midpoint_grid_y,
                                                                                                     target.subsurface_depth))
                        
                        # Swope target.start_grid_x and grid_y for target.end_grid_x and grid_y
                        latitudelongitudedistance.end_hypotenuse = math.ceil(calculate_3d_distance(reference_lateral_end_grid_x, 
                                                                                                     reference_lateral_end_grid_y, 
                                                                                                     reference.subsurface_depth, 
                                                                                                     target_lateral_start_grid_x, 
                                                                                                     target_lateral_start_grid_y,
                                                                                                     target.subsurface_depth))
                        
                    # else:
                    #     logger.info(f"{reference.dominant_direction}-{target.dominant_direction}")

                    if latitudelongitudedistance is not None:
                        latitudelongitudedistance_list.append(latitudelongitudedistance)

            latitudelongitudedistance_service = LatitudeLongitudeDistanceService(db_path=self.context.db_path)
            latitudelongitudedistance_service.add_many(latitudelongitudedistance_list)

            logger.info(f"{task}: {self.context.logs_path}")
        except Exception as e:
            logger.error(f"Error {task} workflow task: {e}\n{format_exc()}")
            raise ValueError(f"Error {task} workflow task: {e}")