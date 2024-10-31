
from tasks.task import Task
from tasks.task_enum import TASKS
from helpers import task_logger
from traceback import format_exc
from services import (GunBarrelService, AnalysisService, WellService,
                      GunBarrelTriangleDistancesService, XYZDistanceService)
from models import GunBarrelTriangleDistances
import math
from dateutil.relativedelta import relativedelta
from datetime import datetime

class EnrichGunBarrel(Task):

    def months_between_dates(self, start_date:str, end_date:str) -> int:
        # Convert string inputs to datetime objects if necessary
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Calculate the difference between the two dates
        delta = relativedelta(end_date, start_date)

        # Return the total number of months (years * 12 + months)
        return delta.years * 12 + delta.months

    def execute(self):
        task = TASKS.ENRICH_GUN_BARREL.value
        logger = task_logger(task, self.context.logs_path)
        try:
            gun_barrel_service = GunBarrelService(self.context.db_path)
            analysis_service = AnalysisService(self.context.db_path)
            well_service = WellService(self.context.db_path)
            gun_barrel_triangle_distances_service = GunBarrelTriangleDistancesService(self.context.db_path)
            xyz_distance_service = XYZDistanceService(self.context.db_path)

            # Get all gun barrels
            gun_barrels = gun_barrel_service.select_all()
            for gun_barrel in gun_barrels:
                target_well_analysis = analysis_service.get_by_api(gun_barrel.target_well_api)
                offset_well_analysis = analysis_service.get_by_api(gun_barrel.offset_well_api)
                offset_well = well_service.get_by_api(gun_barrel.offset_well_api)

                cumulative_oil = offset_well.cumlative_oil
                perf_interval = offset_well.lateral_length if offset_well.perf_interval is None else offset_well.perf_interval
                
                cumulative_oil_per_foot = math.ceil(cumulative_oil / perf_interval)

                if gun_barrel.overlap_percentage is not None:
                    overlap_cumulative_oil = math.ceil(gun_barrel.overlap_percentage * (cumulative_oil_per_foot/100))
                else:
                    overlap_cumulative_oil = 0
                months_from_first_production_data = self.months_between_dates(offset_well_analysis.first_production_date, target_well_analysis.first_production_date)

                gun_barrel.cumulative_oil_per_ft = cumulative_oil_per_foot
                gun_barrel.overlap_cumulative_oil_ft = overlap_cumulative_oil
                gun_barrel.months_from_first_production = months_from_first_production_data

                gun_barrel_service.update(gun_barrel)

                # Updata analysis gun_barrel_x values
                target_gun_barrel_x = xyz_distance_service.get_by_reference_target_well('00-000-00000', gun_barrel.target_well_api)
                offset_gun_barrel_x = xyz_distance_service.get_by_reference_target_well('00-000-00000', gun_barrel.offset_well_api)
                if offset_gun_barrel_x is None or target_gun_barrel_x is None:
                    continue
                target_well_analysis.gun_barrel_x = target_gun_barrel_x.end_x
                target_well_analysis.target_well_spacing_gun_barrel_plot_flag = True
                offset_well_analysis.gun_barrel_x = offset_gun_barrel_x.end_x
                offset_well_analysis.target_well_spacing_gun_barrel_plot_flag = True
                analysis_service.update(target_well_analysis)
                analysis_service.update(offset_well_analysis)

                # Calculate the triangle distances
                gun_barrel_triangle_distances = GunBarrelTriangleDistances()
                gun_barrel_triangle_distances.target_well_api = target_well_analysis.api
                gun_barrel_triangle_distances.offset_well_api = offset_well_analysis.api
                gun_barrel_triangle_distances.adjacent = int(abs(offset_well_analysis.gun_barrel_x - target_well_analysis.gun_barrel_x))
                gun_barrel_triangle_distances.opposite = int(abs(offset_well_analysis.subsurface_depth - target_well_analysis.subsurface_depth))
                gun_barrel_triangle_distances.hypotenuse = int(math.sqrt(gun_barrel_triangle_distances.adjacent**2 + gun_barrel_triangle_distances.opposite**2))
                gun_barrel_triangle_distances_service.insert(gun_barrel_triangle_distances)

            logger.info(f"{task}: {self.context.logs_path}")
        except Exception as e:
            logger.error(f"Error {task} workflow task: {e}\n{format_exc()}")
            raise ValueError(f"Error {task} workflow task: {e}")    