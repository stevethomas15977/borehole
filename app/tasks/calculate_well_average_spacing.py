from tasks.task import Task
from tasks.task_enum import TASKS
from helpers import task_logger
from traceback import format_exc
import math

from services import AnalysisService, AdjacentService
from models import Analysis, Adjacent

class CalculateWellAverageSpacing(Task):

    def execute(self):
        task = TASKS.CALCULATE_WELL_AVERAGE_SPACING.value
        logger = task_logger(task, self.context.logs_path)
        try:
            analysis_service = AnalysisService(self.context.db_path)
            adjacent_service = AdjacentService(self.context.db_path)

            analysis_list = list[Analysis](analysis_service.get_all())
            
            for analysis in analysis_list:
                if analysis.direction in ["N", "S"] and analysis.codevelopment == "Yes":
                    adjacent_easts = list[Adjacent](adjacent_service.get_by_reference_api_east(reference_api=analysis.api))
                    adjacent_wests = list[Adjacent](adjacent_service.get_by_reference_api_west(reference_api=analysis.api))
                    if adjacent_easts is None or adjacent_wests is None:
                        continue
                    if len(adjacent_easts) > 0 and len(adjacent_wests) > 0:
                        analysis.average_horizontal_spacing = math.ceil((adjacent_easts[0].east + adjacent_wests[0].west) / 2)
                    elif len(adjacent_easts) > 0 and len(adjacent_wests) == 0:
                        analysis.average_horizontal_spacing = adjacent_easts[0].east
                    elif len(adjacent_easts) == 0 and len(adjacent_wests) > 0:
                        analysis.average_horizontal_spacing = adjacent_wests[0].west
                    else:
                        continue
                elif analysis.direction in ["E", "W"]:
                    adjacent_norths = list[Adjacent](adjacent_service.get_by_reference_api_north(reference_api=analysis.api))
                    adjacent_souths = list[Adjacent](adjacent_service.get_by_reference_api_south(reference_api=analysis.api))
                    if adjacent_norths is None or adjacent_souths is None:
                        continue
                    if len(adjacent_norths) > 0 and len(adjacent_souths) > 0:
                        analysis.average_horizontal_spacing = math.ceil((adjacent_norths[0].north + adjacent_souths[0].south) / 2)
                    elif len(adjacent_norths) > 0 and len(adjacent_souths) == 0:
                        analysis.average_horizontal_spacing = adjacent_norths[0].north
                    elif len(adjacent_norths) == 0 and len(adjacent_souths) > 0:
                        analysis.average_horizontal_spacing = adjacent_souths[0].south
                    else:
                        continue
                analysis_service.update(analysis=analysis)
            logger.info(f"{task}: {self.context.logs_path}")
        except Exception as e:
            logger.error(f"Error {task} workflow task: {e}\n{format_exc()}")
            raise ValueError(f"Error {task} workflow task: {e}")