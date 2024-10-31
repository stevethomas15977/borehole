from tasks.task import Task
from tasks.task_enum import TASKS
from helpers import task_logger, calculate_xyz_distances
from models import XYZDistance
from services import XYZDistanceService, AnalysisService
from traceback import format_exc

class CalculateXYZDistance(Task):

    def execute(self):
        task = TASKS.CALCULATE_XYZ_DISTANCE.value
        logger = task_logger(task, self.context.logs_path)
        try:
            analysis_service = AnalysisService(db_path=self.context.db_path)

            reference_analysis = analysis_service.get()
            target_analysis = analysis_service.get()

            xyzdistance_list = []

            for reference in reference_analysis:

                # if reference.name not in ['AMPHITHEATER A3 15UA']:
                #     continue   

                for target in target_analysis:

                    # if target.name not in ['AMPHITHEATER A6 16UA']:
                    #     continue 

                    if reference.name == target.name:
                        continue

                    if (
                        (reference.dominant_direction == "N" and target.dominant_direction == "N")
                         or (reference.dominant_direction == "S" and target.dominant_direction == "S")
                         or (reference.dominant_direction == "E" and target.dominant_direction == "E")
                         or (reference.dominant_direction == "W" and target.dominant_direction == "W")
                        ):
                        xyzdistance = XYZDistance()
                        xyzdistance.reference_api = reference.api
                        xyzdistance.reference_name = reference.name
                        xyzdistance.target_api = target.api
                        xyzdistance.target_name = target.name
                        
                        start_distance_dict = calculate_xyz_distances(reference.lateral_start_grid_x, 
                                                                      reference.lateral_start_grid_y, 
                                                                      reference.subsurface_depth, 
                                                                      target.lateral_start_grid_x, 
                                                                      target.lateral_start_grid_y, 
                                                                      target.subsurface_depth)
                        xyzdistance.start_x = start_distance_dict["delta_x"]
                        xyzdistance.start_y = start_distance_dict["delta_y"]
                        xyzdistance.start_z = start_distance_dict["delta_z"]
                        xyzdistance.start_hypotenuse =  start_distance_dict["hypotenuse"]
                        
                        mid_distance_dict = calculate_xyz_distances(reference.lateral_midpoint_grid_x, 
                                                                    reference.lateral_midpoint_grid_y, 
                                                                    reference.subsurface_depth, 
                                                                    target.lateral_midpoint_grid_x, 
                                                                    target.lateral_midpoint_grid_y, 
                                                                    target.subsurface_depth)
                        xyzdistance.mid_x = mid_distance_dict["delta_x"]
                        xyzdistance.mid_y = mid_distance_dict["delta_y"]
                        xyzdistance.mid_z = mid_distance_dict["delta_z"]
                        xyzdistance.mid_hypotenuse =  mid_distance_dict["hypotenuse"]
                        
                        end_distance_dict = calculate_xyz_distances(reference.lateral_end_grid_x, 
                                                                    reference.lateral_end_grid_y, 
                                                                    reference.subsurface_depth, 
                                                                    target.lateral_end_grid_x, 
                                                                    target.lateral_end_grid_y, 
                                                                    target.subsurface_depth)
                        xyzdistance.end_x = end_distance_dict["delta_x"]
                        xyzdistance.end_y = end_distance_dict["delta_y"]
                        xyzdistance.end_z = end_distance_dict["delta_z"]
                        xyzdistance.end_hypotenuse =  end_distance_dict["hypotenuse"]

                        xyzdistance_list.append(xyzdistance)  
                    elif (
                        (reference.dominant_direction == "N" and target.dominant_direction == "S")
                         or (reference.dominant_direction == "S" and target.dominant_direction == "N")
                         or (reference.dominant_direction == "E" and target.dominant_direction == "E")
                         or (reference.dominant_direction == "W" and target.dominant_direction == "W")
                        ):
                        xyzdistance = XYZDistance()
                        xyzdistance.reference_api = reference.api
                        xyzdistance.reference_name = reference.name
                        xyzdistance.target_api = target.api
                        xyzdistance.target_name = target.name
                        
                        start_distance_dict = calculate_xyz_distances(reference.lateral_end_grid_x, 
                                                                      reference.lateral_end_grid_y, 
                                                                      reference.subsurface_depth, 
                                                                      target.lateral_start_grid_x, 
                                                                      target.lateral_start_grid_y, 
                                                                      target.subsurface_depth)
                        xyzdistance.start_x = start_distance_dict["delta_x"]
                        xyzdistance.start_y = start_distance_dict["delta_y"]
                        xyzdistance.start_z = start_distance_dict["delta_z"]
                        xyzdistance.start_hypotenuse =  start_distance_dict["hypotenuse"]
                        
                        mid_distance_dict = calculate_xyz_distances(reference.lateral_midpoint_grid_x, 
                                                                    reference.lateral_midpoint_grid_y, 
                                                                    reference.subsurface_depth, 
                                                                    target.lateral_midpoint_grid_x, 
                                                                    target.lateral_midpoint_grid_y, 
                                                                    target.subsurface_depth)
                        xyzdistance.mid_x = mid_distance_dict["delta_x"]
                        xyzdistance.mid_y = mid_distance_dict["delta_y"]
                        xyzdistance.mid_z = mid_distance_dict["delta_z"]
                        xyzdistance.mid_hypotenuse =  mid_distance_dict["hypotenuse"]
                        
                        end_distance_dict = calculate_xyz_distances(reference.lateral_start_grid_x, 
                                                                    reference.lateral_start_grid_y, 
                                                                    reference.subsurface_depth, 
                                                                    target.lateral_end_grid_x, 
                                                                    target.lateral_end_grid_y, 
                                                                    target.subsurface_depth)
                        xyzdistance.end_x = end_distance_dict["delta_x"]
                        xyzdistance.end_y = end_distance_dict["delta_y"]
                        xyzdistance.end_z = end_distance_dict["delta_z"]
                        xyzdistance.end_hypotenuse =  end_distance_dict["hypotenuse"]

                        xyzdistance_list.append(xyzdistance)  

            if len(xyzdistance_list) > 0:
                xyzdistance_service = XYZDistanceService(db_path=self.context.db_path)
                xyzdistance_service.add_many(xyzdistance_list)

            logger.info(f"{task}: {self.context.logs_path}")
        except Exception as e:
            logger.error(f"Error {task} workflow task: {e}\n{format_exc()}")
            raise ValueError(f"Error {task} workflow task: {e}")