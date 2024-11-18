from tasks.task import Task
from tasks.task_enum import TASKS
from traceback import format_exc
import math, os
from xlsxwriter import Workbook

from helpers import (task_logger, is_within_y_range)
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

    def is_within_range(self, start: float, end: float, test: float) -> bool:
        lower_bound = min(start, end)
        upper_bound = max(start, end)
        return lower_bound <= test <= upper_bound

    def wells_to_plot(self, 
                      analysis_service: AnalysisService,
                      xyz_distance_service: XYZDistanceService):
        try:
            target_wells = []
            other_wells = []
            first_count = 0
            second_count = 0
            third_count = 0
            simulated_well = analysis_service.get_simluated_well()
            offset_wells = xyz_distance_service.get_by_simulated_well()
            for offset_well in offset_wells:
                offset_well_analysis = analysis_service.get_by_name(offset_well.target_name)
                if simulated_well.dominant_direction in ["N", "S"] and offset_well_analysis.dominant_direction in ["N", "S"]:
                    if offset_well.end_x < 7920 and offset_well.end_x > -2640:
                        first_count += 1
                        if ((self.is_within_range(simulated_well.lateral_start_grid_y, simulated_well.lateral_end_grid_y, offset_well_analysis.lateral_start_grid_y) == True) or
                            (self.is_within_range(simulated_well.lateral_start_grid_y, simulated_well.lateral_end_grid_y, offset_well_analysis.lateral_midpoint_grid_y) == True) or
                            (self.is_within_range(simulated_well.lateral_start_grid_y, simulated_well.lateral_end_grid_y, offset_well_analysis.lateral_end_grid_y)) == True):
                                second_count += 1
                                if offset_well_analysis.subsurface_depth < -6000 and offset_well_analysis.subsurface_depth > -8500:
                                    third_count += 1
                                    if offset_well_analysis.gun_barrel_x is None:
                                        offset_well_analysis.gun_barrel_x = offset_well.end_x
                                    if "11-111" in offset_well_analysis.api:
                                        target_wells.append(offset_well_analysis)
                                    else:
                                        other_wells.append(offset_well_analysis)
                                    # print(f"Offset well: {offset_well.target_name} at {offset_well.end_x} ft")
                elif simulated_well.dominant_direction in ["E", "W"] and offset_well_analysis.dominant_direction in ["E", "W"]:
                    if offset_well.end_y < 7920 and offset_well.end_y > -2640:
                        first_count += 1
                        if ((self.is_within_range(simulated_well.lateral_start_grid_x, simulated_well.lateral_end_grid_x, offset_well_analysis.lateral_start_grid_x) == True) or
                            (self.is_within_range(simulated_well.lateral_start_grid_x, simulated_well.lateral_end_grid_x, offset_well_analysis.lateral_midpoint_grid_x) == True) or
                            (self.is_within_range(simulated_well.lateral_start_grid_x, simulated_well.lateral_end_grid_x, offset_well_analysis.lateral_end_grid_x)) == True):
                                second_count += 1
                                if offset_well_analysis.subsurface_depth < -6000 and offset_well_analysis.subsurface_depth > -8500:
                                    third_count += 1
                                    if "11-111" in offset_well_analysis.api:
                                        target_wells.append(offset_well_analysis)
                                    else:
                                        other_wells.append(offset_well_analysis)
                                    # print(f"Offset well: {offset_well.target_name} at {offset_well.end_x} ft")
            # print(f"First count: {first_count}")
            # print(f"Second count: {second_count}")
            # print(f"Third count: {third_count}")
            return target_wells, other_wells
        except Exception as e:
            raise e

    def create_plot_data_worksheet(self, 
                                   workbook: Workbook, 
                                   target_wells: list[Analysis], 
                                   other_wells: list[Analysis]):

        worksheet = workbook.add_worksheet("Plot Data")
        worksheet.write(0, 0, "Ref #")
        worksheet.write(0, 1, "API")
        worksheet.write(0, 2, "Name")
        worksheet.write(0, 3, "X")
        worksheet.write(0, 4, "Y")

        first_row = 2
        row = 1
        last_row = 0
        refs = []
        lzs = []

        # Plot target wells
        for well in target_wells:
            worksheet.write(row, 0, row)
            refs.append(row)
            lzs.append(well.interval)
            worksheet.write(row, 1, "")
            worksheet.write(row, 2, well.name)
            worksheet.write(row, 3, well.gun_barrel_x)
            worksheet.write(row, 4, well.subsurface_depth)
            row = row + 1
        last_row = row
        target_well_series_1 = {
            "categories": f"='Plot Data'!$D${first_row}:$D${last_row}",         # Dynamic X-values
            "values": f"='Plot Data'!$E${first_row}:$E${last_row}",             # Dynamic Y-values
            "marker": {"type": "triangle", "size": 12, "fill": {"color": "orange"}},
            "data_labels": {
                "value": True,
                "position": "center",
                "custom": [{"value": ref, "index": ref} for ref in refs],
            }   
        }
        target_well_series_2 = {
            "categories": f"='Plot Data'!$D${first_row}:$D${last_row}",         # Dynamic X-values
            "values": f"='Plot Data'!$E${first_row}:$E${last_row}",             # Dynamic Y-values
            "marker": {"type": "none"},
            "data_labels": {
                "value": True,
                "position": "above",
                "custom": [{"value": lz, "index": lz} for lz in lzs],
            }   
        }

        # Plot other wells
        refs = []
        lzs = []
        first_row, row = last_row + 1, last_row
        for well in other_wells:
            worksheet.write(row, 0, row)
            refs.append(row)
            lzs.append(well.interval)
            worksheet.write(row, 1, well.api)
            worksheet.write(row, 2, well.name)
            worksheet.write(row, 3, well.gun_barrel_x)
            worksheet.write(row, 4, well.subsurface_depth)
            row = row + 1
        last_row = row
        other_well_series_1 = {
            "categories": f"='Plot Data'!$D${first_row}:$D${last_row}",         # Dynamic X-values
            "values": f"='Plot Data'!$E${first_row}:$E${last_row}",             # Dynamic Y-values
            "marker": {"type": "circle", "size": 12, "fill": {"color": "green"}},
            "data_labels": {"value": True,"position": "center","custom": [{"value": ref, "index": ref} for ref in refs],}
        }
        other_well_series_2 = {
            "categories": f"='Plot Data'!$D${first_row}:$D${last_row}",         # Dynamic X-values
            "values": f"='Plot Data'!$E${first_row}:$E${last_row}",             # Dynamic Y-values
            "marker": {"type": "none"},
            "data_labels": {
                "value": True,
                "position": "above",
                "custom": [{"value": lz, "index": lz} for lz in lzs],
            }   
        }

        return target_well_series_1, target_well_series_2, other_well_series_1, other_well_series_2

    def section_line_label(self, target_well: TargetWellInformation):
        try:
            if "TX" in target_well.state :
                return f"{target_well.tx_abstract_southwest_corner}/{target_well.tx_block_southwest_corner}/{int(float(target_well.nm_tx_section_southwest_corner))}"
            elif "NM" in target_well.state :
                return f"{target_well.nw_township_southwest_corner}/{target_well.nm_range_southwest_corner}/{int(float(target_well.nm_tx_section_southwest_corner))}"
        except Exception as e:
            raise e

    def create_plot_support_data(self, workbook: Workbook):
        """
        Creates a 'Support Data' worksheet with static data for vertical lines and annotations.
        """
        worksheet = workbook.add_worksheet("Support Data")

        # Static data for vertical lines
        vertical_line_x = [0, 0]  # Static X-values for vertical line
        vertical_line_y = [-8500, -6000]  # Static Y-values for vertical line

        # Static data for annotations
        annotation_x = [0]  # Static X-value for annotation
        annotation_y = [-8490]  # Static Y-value for annotation

        # Write vertical line data
        worksheet.write(0, 0, "Vertical Line X")
        worksheet.write(0, 1, "Vertical Line Y")
        for i, (x, y) in enumerate(zip(vertical_line_x, vertical_line_y), start=1):
            worksheet.write(i, 0, x)
            worksheet.write(i, 1, y)

        # Write annotation data
        worksheet.write(0, 3, "Annotation X")
        worksheet.write(0, 4, "Annotation Y")
        for i, (x, y) in enumerate(zip(annotation_x, annotation_y), start=1):
            worksheet.write(i, 3, x)
            worksheet.write(i, 4, y)

        # Return ranges for the chart
        vertical_line_categories = "='Support Data'!$A$2:$A$3"
        vertical_line_values = "='Support Data'!$B$2:$B$3"
        annotation_categories = "='Support Data'!$D$2:$D$2"
        annotation_values = "='Support Data'!$E$2:$E$2"

        return vertical_line_categories, vertical_line_values, annotation_categories, annotation_values

    def create_plot(self, 
                    workbook: Workbook, 
                    title: str, 
                    section_line_label: str, 
                    target_well_series_1: dict,
                    target_well_series_2: dict,
                    other_well_series_1: dict,
                    other_well_series_2: dict):
        try:
            # Create a scatter chart
            plot = workbook.add_chart({"type": "scatter"})
            # Add chart title
            plot.set_title({"name": title}) 
            # Adjust plot area and chart area to create space for the annotation
            plot.set_plotarea({"x": 0.1, "y": 0.2, "width": 0.7, "height": 0.6})
            plot.set_chartarea({"x": 0.1, "y": 0.05, "width": 0.7, "height": 0.9})  # Increase bottom margin
            # Set chart size and layout
            plot.set_size({"width": 1100, "height": 550})  # ~11.5" x 8"
            plot.set_legend({"none": True})  # Disable legend
            plot.set_x_axis({
                "name": "Lateral Bottom Hole Spacing (ft)",
                "min": -2640,
                "max": 7920,
                "major_unit": 1320,
                "minor_unit": 100,
                "minor_gridlines": {
                    "visible": True,
                    "line": {"color": "#D3D3D3", "width": 0.25},
                },
                "name_font": {"bold": True},
                "label_position": "low",
                "crossing": "min",
            })
            plot.set_y_axis({
                "name": "Depth Below MSL (ft)",
                "min": -8500,
                "max": -6000,
                "major_unit": 500,
                "minor_unit": 100,
                "minor_gridlines": {
                    "visible": True,
                    "line": {"color": "#D3D3D3", "width": 0.25},
                },
                "name_font": {"bold": True},
            })
            # Add static series for the vertical line
            vertical_line_categories, vertical_line_values, annotation_categories, annotation_values = self.create_plot_support_data(workbook)
            plot.add_series({
                "categories": vertical_line_categories,  # Static X-values for the vertical line
                "values": vertical_line_values,          # Static Y-values for the vertical line
                "line": {
                    "color": "blue",
                    "width": 1,
                    "dash_type": "dash",
                },
                "marker": {"type": "none"},  # No markers for the line
            })

            # Add static series for the annotation
            plot.add_series({
                "categories": annotation_categories,  # Static X-value for annotation
                "values": annotation_values,          # Static Y-value for annotation
                "name": section_line_label,           # Annotation label
                "marker": {"type": "none"},           # Hide marker
                "data_labels": {
                    "series_name": True,              # Display series name
                    "value": False,                   # Do not display Y-value
                    "position": "above",
                },
            })

            plot.add_series(target_well_series_1)
            plot.add_series(target_well_series_2)
            plot.add_series(other_well_series_1)
            plot.add_series(other_well_series_2)

            plot_worksheet = workbook.add_worksheet("Plot")
            plot_worksheet.insert_chart("B4", plot)

            return None
        except Exception as e:
            raise e
        
    def execute(self):
        task = TASKS.CREATE_EXCEL_NATIVE_GUN_BARREL_PLOT.value
        logger = task_logger(task, self.context.logs_path)
        try:
            analysis_service = AnalysisService(db_path=self.context.db_path)
            target_well_information_service = TargetWellInformationService(self.context.db_path)
            well_service = WellService(self.context.db_path)
            overlap_service = OverlapService(self.context.db_path)
            xyz_distance_service = XYZDistanceService(self.context.db_path)

            target_wells, other_wells = self.wells_to_plot(analysis_service, xyz_distance_service)

            plot_title = f"{self.context.project.capitalize()} Barrel Plot ({self.context.version})"
            section_line_label = self.section_line_label( target_well_information_service.get_first_row())
            
            output_file = os.path.join(self.context.project_path, f"{self.context.project}-excel-native-gun-barrel-plot-{self.context.version}.xlsx")

            # Main script
            workbook = Workbook(output_file)

            target_well_series_1, target_well_series_2, other_well_series_1, other_well_series_2 = self.create_plot_data_worksheet(workbook, target_wells, other_wells)

            self.create_plot(workbook, 
                             plot_title, 
                             section_line_label, 
                             target_well_series_1, 
                             target_well_series_2, 
                             other_well_series_1,
                             other_well_series_2)   

            # Close the workbook
            workbook.close()
            print("Oil barrel plot with dynamic and static data created.")

            logger.info(f"{task}: {self.context.logs_path}")
        except Exception as e:
            logger.error(f"Error {task} workflow task: {e}\n{format_exc()}")
            raise ValueError(f"Error {task} workflow task: {e}")