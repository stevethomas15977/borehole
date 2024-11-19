from tasks.task import Task
from tasks.task_enum import TASKS
from traceback import format_exc
import os
from xlsxwriter import Workbook, worksheet

from helpers import (task_logger, 
                    is_within_range,
                    wells_to_plot,
                    create_well_data_worksheet,
                    create_plot_data_worksheet,
                    create_plot_support_data,
                    create_line_series_data_worksheet,
                    create_plot,
                    create_section_line_label,
                    create_calulated_data_worksheet,
                    calculate_overlap,
                    months_between_dates)

from services import (AnalysisService, 
                      TargetWellInformationService, 
                      WellService,
                      XYZDistanceService,
                      OverlapService)

from models import (Analysis,
                    XYZDistance, 
                    Overlap, 
                    TargetWellInformation)

class CreateExcelNativeGunBarrelPlot(Task):

    def __init__(self, context):
        super().__init__(context)
    
    def execute(self):
        task = TASKS.CREATE_EXCEL_NATIVE_GUN_BARREL_PLOT.value
        logger = task_logger(task, self.context.logs_path)
        try:
            analysis_service = AnalysisService(db_path=self.context.db_path)
            target_well_information_service = TargetWellInformationService(self.context.db_path)
            well_service = WellService(self.context.db_path)
            overlap_service = OverlapService(self.context.db_path)
            xyz_distance_service = XYZDistanceService(self.context.db_path)

            shallowest = round((target_well_information_service.get_shallowest() - self.context.depth_distance_threshold) * -1, -3)
            deepest = round((target_well_information_service.get_deepest() + self.context.depth_distance_threshold) * -1, -3)

            target_wells, other_wells = wells_to_plot(analysis_service, xyz_distance_service, shallowest, deepest)

            plot_title = f"{self.context.project.capitalize()} Barrel Plot ({self.context.version})"
            section_line_label = create_section_line_label(target_well_information_service.get_first_row())
            
            output_file = os.path.join(self.context.project_path, f"{self.context.project}-excel-native-gun-barrel-plot-{self.context.version}.xlsx")

            # Main script
            workbook = Workbook(output_file)

            plot_worksheet = workbook.add_worksheet("Plot")
            well_data_worksheet = workbook.add_worksheet("Well Data")
            plot_data_worksheet = workbook.add_worksheet("Plot Data")
            calculated_data_worksheet = workbook.add_worksheet("Calculated Data")
            line_series_data_worksheet = workbook.add_worksheet("Line Series")

            ref_index, target_well_series_1, target_well_series_2, other_well_series_1, other_well_series_2 = create_plot_data_worksheet(workbook, plot_data_worksheet, target_wells, other_wells)

            create_well_data_worksheet(workbook, well_data_worksheet, well_service, ref_index, other_wells)

            line_series, pairs = create_line_series_data_worksheet(self.context, workbook, line_series_data_worksheet, ref_index, target_wells, other_wells)    
            
            create_plot(workbook, 
                        plot_worksheet,
                        plot_title, 
                        section_line_label, 
                        target_well_series_1, 
                        target_well_series_2, 
                        other_well_series_1,
                        other_well_series_2,
                        line_series,
                        shallowest,
                        deepest)

            create_calulated_data_worksheet(workbook, 
                                            calculated_data_worksheet, 
                                            pairs, 
                                            ref_index, 
                                            analysis_service,
                                            target_well_information_service,
                                            well_service)

            # Close the workbook
            workbook.close()
            print("Oil barrel plot with dynamic and static data created.")

            logger.info(f"{task}: {self.context.logs_path}")
        except Exception as e:
            logger.error(f"Error {task} workflow task: {e}\n{format_exc()}")
            raise ValueError(f"Error {task} workflow task: {e}")