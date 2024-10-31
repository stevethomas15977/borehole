from tasks.task import Task
from tasks.task_enum import TASKS
from helpers import task_logger
from traceback import format_exc

from helpers import (is_within_latitude_range,
                     is_within_longitude_range)
from models import (LatitudeLongitudeDistance,
                    Adjacent)
from services import (LatitudeLongitudeDistanceService,
                     AnalysisService,
                     AdjacentService)
class DetermineAdjacentWells(Task):

    def execute(self):
        task = TASKS.DETERMINE_ADJACENT_WELLS.value
        logger = task_logger(task, self.context.logs_path)
        try:
            latitudelongitudedistance_service = LatitudeLongitudeDistanceService(self.context.db_path)
            analysis_service = AnalysisService(self.context.db_path)
            adjacent_service = AdjacentService(self.context.db_path)
            distances = latitudelongitudedistance_service.get()

            for distance in list[LatitudeLongitudeDistance](distances):

                if distance.reference_api == '00-000-00000' or distance.target_api == '00-000-00000':
                    continue

                reference_analysis = analysis_service.get_by_api(distance.reference_api)
                target_analysis = analysis_service.get_by_api(distance.target_api)
            
                # Determine is the reference and target wells are within the same latitude and longitude range
                target_in_range_of_reference_latitude = is_within_latitude_range(reference_analysis.lateral_start_latitude, 
                                                                        reference_analysis.lateral_end_latitude, 
                                                                        target_analysis.lateral_midpoint_latitude)
                
                reference_in_range_of_target_latitude = is_within_latitude_range(target_analysis.lateral_start_latitude, 
                                                                        target_analysis.lateral_end_latitude, 
                                                                        reference_analysis.lateral_midpoint_latitude)

                target_in_range_of_reference_longitude = is_within_longitude_range(reference_analysis.lateral_start_longitude, 
                                                                        reference_analysis.lateral_end_longitude, 
                                                                        target_analysis.lateral_midpoint_longitude)
                
                reference_in_range_of_target_longitude = is_within_longitude_range(target_analysis.lateral_start_longitude,
                                                                        target_analysis.lateral_end_longitude,
                                                                        reference_analysis.lateral_midpoint_longitude)
                
                if (target_in_range_of_reference_latitude == False and 
                    reference_in_range_of_target_latitude == False and
                    target_in_range_of_reference_longitude == False and 
                    reference_in_range_of_target_longitude == False):
                    continue

                # Determine is the start, mid and end lateral location distances 
                # are within the horizontal distance threshold, vertical distance threshold 
                # and hypotenuse distance threshold            

                if reference_analysis.dominant_direction in ["N", "S"] and target_analysis.dominant_direction in ["N", "S"]:
                    
                    # Determine if the longitude (X-axis) distances are within the horizontal distance threshold
                    if ((abs(distance.start_longitude) or 0) > int(self.context.horizontal_distance_threshold) and
                        (abs(distance.mid_longitude) or 0) > int(self.context.horizontal_distance_threshold) and
                        (abs(distance.end_longitude) or 0) > int(self.context.horizontal_distance_threshold)):
                        continue
                    
                    # Determine if the latitude (Y-axis) distances are within the vertical distance threshold
                    # if ((abs(distance.start_latitude) or 0) > int(self.context.vertical_distance_threshold) and
                    #     (abs(distance.mid_latitude) or 0) > int(self.context.vertical_distance_threshold) and
                    #     (abs(distance.end_latitude) or 0) > int(self.context.vertical_distance_threshold)):
                    #     continue
                    
                    # Determine if the hypotenuse distances are within the hypotenuse distance threshold
                    if ((distance.start_hypotenuse or 0) > int(self.context.hypotenuse_distance_threshold) and 
                        (distance.mid_hypotenuse or 0) > int(self.context.hypotenuse_distance_threshold) and 
                        (distance.end_hypotenuse or 0) > int(self.context.hypotenuse_distance_threshold)):
                        continue

                    # The east-west distance along a meridian would correspond to the X-axis 
                    # distance on a 2-dimensional grid where longitude represents the horizontal axis.
                    # Northward movements (higher latitude) will always result in positive delta_lat and thus be marked as "N".
                    # Southward movements (lower latitude) will always result in negative delta_lat and thus be marked as "S".
                    if distance.start_latitude >= 0:
                        north = distance.end_latitude
                        south = None
                    else:
                        north = None
                        south = abs(distance.end_latitude)

                    # Moving eastward (toward higher longitude values) will result in a positive difference.
                    # Moving westward (toward lower longitude values) will result in a negative difference.
                    if distance.end_longitude >= 0:
                        east = distance.end_longitude
                        west = None
                    else:
                        east = None
                        west = abs(distance.end_longitude)

                    new_adjacent = Adjacent(
                        reference_api=reference_analysis.api,
                        reference_name=reference_analysis.name, 
                        target_api=target_analysis.api,
                        target_name=target_analysis.name, 
                        north=north,
                        south=south, 
                        east=east, 
                        west=west,
                        hypotenuse=distance.end_hypotenuse)
                        
                    # Determine if the reference and target wells are adjacent, if so add to the adjacent table
                    if distance.end_longitude >= 0:
                        adjacents = adjacent_service.get_by_reference_api_east(reference_api=reference_analysis.api)
                        if len(adjacents) == 0:
                            adjacent_service.add_one(new_adjacent)
                            reference_analysis.adjacent_1 = target_analysis.name
                            reference_analysis.distance_1 = abs(distance.end_longitude)
                            reference_analysis.hypotenuse_1 = distance.end_hypotenuse
                            analysis_service.update(reference_analysis)
                        else:
                            for adjacent in adjacents:
                                if distance.end_longitude is not None and adjacent.east is not None:
                                    if (abs(distance.end_longitude) or 0) < (adjacent.east or 0):   
                                        adjacent_service.delete(reference_api=reference_analysis.api, target_api=adjacent.target_api)
                                        adjacent_service.add_one(new_adjacent)
                                        reference_analysis.adjacent_1 = target_analysis.name
                                        reference_analysis.distance_1 = abs(distance.end_longitude)
                                        reference_analysis.hypotenuse_1 = distance.end_hypotenuse
                                        analysis_service.update(reference_analysis)
                    else:
                        adjacents = adjacent_service.get_by_reference_api_west(reference_api=reference_analysis.api)
                        if len(adjacents) == 0:
                            adjacent_service.add_one(new_adjacent)  
                            reference_analysis.adjacent_2 = target_analysis.name
                            reference_analysis.distance_2 = abs(distance.end_longitude)
                            reference_analysis.hypotenuse_2 = distance.end_hypotenuse
                            analysis_service.update(reference_analysis)
                        else:
                            for adjacent in adjacents:       
                                if distance.end_longitude is not None and adjacent.west is not None:
                                    if (abs(distance.end_longitude) or 0) < (adjacent.west or 0):   
                                        adjacent_service.delete(reference_api=reference_analysis.api, target_api=adjacent.target_api)
                                        adjacent_service.add_one(new_adjacent)
                                        reference_analysis.adjacent_2 = target_analysis.name
                                        reference_analysis.distance_2 = abs(distance.end_longitude)
                                        reference_analysis.hypotenuse_2 = distance.end_hypotenuse
                                        analysis_service.update(reference_analysis)

                # The north-south distance along a meridian would correspond to the Y-axis 
                # distance on a 2-dimensional grid where latitude represents the vertical axis.
                elif reference_analysis.dominant_direction in ["E", "W"] and target_analysis.dominant_direction in ["E", "W"]:
                    
                    if ((abs(distance.start_latitude) or 0) > int(self.context.horizontal_distance_threshold) and
                        (abs(distance.mid_latitude) or 0) > int(self.context.horizontal_distance_threshold) and
                        (abs(distance.end_latitude) or 0) > int(self.context.horizontal_distance_threshold)):
                        continue
                    
                    # Determine if the hypotenuse distances are within the hypotenuse distance threshold
                    if ((distance.start_hypotenuse or 0) > int(self.context.hypotenuse_distance_threshold) and 
                        (distance.mid_hypotenuse or 0) > int(self.context.hypotenuse_distance_threshold) and 
                        (distance.end_hypotenuse or 0) > int(self.context.hypotenuse_distance_threshold)):
                        continue

                    # The east-west distance along a meridian would correspond to the X-axis 
                    # distance on a 2-dimensional grid where longitude represents the horizontal axis.
                    # Northward movements (higher latitude) will always result in positive delta_lat and thus be marked as "N".
                    # Southward movements (lower latitude) will always result in negative delta_lat and thus be marked as "S".
                    if distance.start_latitude >= 0:
                        north = distance.end_latitude
                        south = None
                    else:
                        north = None
                        south = abs(distance.end_latitude)

                    # Moving eastward (toward higher longitude values) will result in a positive difference.
                    # Moving westward (toward lower longitude values) will result in a negative difference.
                    if distance.end_longitude >= 0:
                        east = distance.end_longitude
                        west = None
                    else:
                        east = None
                        west = abs(distance.end_longitude)

                    new_adjacent = Adjacent(
                        reference_api=reference_analysis.api,
                        reference_name=reference_analysis.name, 
                        target_api=target_analysis.api,
                        target_name=target_analysis.name, 
                        north=north,
                        south=south, 
                        east=east, 
                        west=west,
                        hypotenuse=distance.end_hypotenuse)

                    # Determine if the reference and target wells are adjacent, if so add to the adjacent table
                    if distance.end_latitude >= 0:
                        adjacents = adjacent_service.get_by_reference_api_north(reference_api=reference_analysis.api)
                        if len(adjacents) == 0:
                            adjacent_service.add_one(new_adjacent)
                            reference_analysis.adjacent_1 = target_analysis.name
                            reference_analysis.distance_1 = abs(distance.end_latitude)
                            reference_analysis.hypotenuse_1 = distance.end_hypotenuse
                            analysis_service.update(reference_analysis)
                        else:
                            for adjacent in adjacents:
                                if distance.end_latitude is not None and adjacent.north is not None:
                                    if (abs(distance.end_latitude) or 0) < (adjacent.north or 0):   
                                        adjacent_service.delete(reference_api=reference_analysis.api, target_api=adjacent.target_api)
                                        adjacent_service.add_one(new_adjacent)
                                        reference_analysis.adjacent_1 = target_analysis.name
                                        reference_analysis.distance_1 = abs(distance.end_latitude)
                                        reference_analysis.hypotenuse_1 = distance.end_hypotenuse
                                        analysis_service.update(reference_analysis)
                    else:
                        adjacents = adjacent_service.get_by_reference_api_south(reference_api=reference_analysis.api)
                        if len(adjacents) == 0:
                            adjacent_service.add_one(new_adjacent)  
                            reference_analysis.adjacent_2 = target_analysis.name
                            reference_analysis.distance_2 = abs(distance.end_latitude)
                            reference_analysis.hypotenuse_2 = distance.end_hypotenuse
                            analysis_service.update(reference_analysis)
                        else:
                            for adjacent in adjacents:       
                                if distance.end_latitude is not None and adjacent.south is not None:
                                    if (abs(distance.end_latitude) or 0) < (adjacent.south or 0):   
                                        adjacent_service.delete(reference_api=reference_analysis.api, target_api=adjacent.target_api)
                                        adjacent_service.add_one(new_adjacent)
                                        reference_analysis.adjacent_2 = target_analysis.name
                                        reference_analysis.distance_2 = abs(distance.end_latitude)
                                        reference_analysis.hypotenuse_2 = distance.end_hypotenuse
                                        analysis_service.update(reference_analysis)

            logger.info(f"{task}: {self.context.logs_path}")
        except Exception as e:
            logger.error(f"Error {task} workflow task: {e}\n{format_exc()}")
            raise ValueError(f"Error {task} workflow task: {e}")