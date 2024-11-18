from tasks.task import Task
from tasks.task_enum import TASKS
from traceback import format_exc
import math, os
from xlsxwriter import Workbook, worksheet
from datetime import datetime
from dateutil.relativedelta import relativedelta
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

    def create_well_data_worksheet(self, 
                                   workbook: Workbook, 
                                   worksheet: worksheet,
                                   well_service: WellService, 
                                   ref_index: dict, 
                                   other_wells: list[Analysis]):
        try:

            data_format = workbook.add_format({
                'align': 'center',
                'border': 1,
                'text_wrap': True
            })

            header_format = workbook.add_format({
                'bold': True,
                'align': 'center',
                'bg_color': '#DDEBF7',
                'border': 1,
                'text_wrap': True
            })  
                
            headers = [
                "Well Ref Number",
                "API",	
                "Well Name",
                "Operator",	
                "Landing zone",	
                "First Production Date",	
                "TVD",	
                "Perf Interval",	
                "Lateral length",	
                "Proppant Intensity LBS/ft",
                "Type",	
                "Group by Radius",
            ]

            row = 0
            for i, header in enumerate(headers):
                worksheet.write(row, i, header, header_format)

            row = 1
            for analysis in other_wells:
                well = well_service.get_by_api(analysis.api)
                worksheet.write(row, 0, ref_index[well.name], data_format)
                worksheet.write(row, 1, well.api, data_format)
                worksheet.write(row, 2, well.name, data_format)
                worksheet.write(row, 3, well.operator, data_format)
                worksheet.write(row, 4, well.interval, data_format)
                worksheet.write(row, 5, well.first_production_date, data_format)
                worksheet.write(row, 6, well.total_vertical_depth, data_format)
                worksheet.write(row, 7, well.perf_interval, data_format)
                worksheet.write(row, 8, well.lateral_length, data_format)
                worksheet.write(row, 9, well.proppant_intensity, data_format)
                worksheet.write(row, 10, "TBD", data_format)
                worksheet.write(row, 11, "TBD", data_format)
                row = row + 1

            worksheet.autofit()

        except Exception as e:
            raise e
        
    def create_plot_data_worksheet(self, 
                                   workbook: Workbook, 
                                   worksheet: worksheet,
                                   target_wells: list[Analysis], 
                                   other_wells: list[Analysis]):

        data_format = workbook.add_format({
            'align': 'center',
            'border': 1,
            'text_wrap': True
        })

        header_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'bg_color': '#DDEBF7',
            'border': 1,
            'text_wrap': True
        })  
                
        worksheet.write(0, 0, "Well Ref Number", header_format)
        worksheet.write(0, 1, "API", header_format)
        worksheet.write(0, 2, "Target Well", header_format)
        worksheet.write(0, 3, "FNL Section (X)", header_format)
        worksheet.write(0, 4, "TVD Subsea depth (Y)", header_format)
        worksheet.write(0, 5, "FNL Section", header_format)

        first_row = 2
        row = 1
        last_row = 0
        refs = []
        lzs = []
        ref_index = {}

        # Plot target wells 
        for well in target_wells:
            worksheet.write(row, 0, row, data_format)
            refs.append(row)
            ref_index[well.name] = row
            lzs.append(well.interval)
            worksheet.write(row, 1, "", data_format)
            worksheet.write(row, 2, well.name, data_format)
            worksheet.write(row, 3, well.gun_barrel_x, data_format)
            worksheet.write(row, 4, well.subsurface_depth, data_format)
            worksheet.write(row, 5, "TBD", data_format)

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
                "font": {
                    "size": 12,
                    "bold": True,
                },   
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
            worksheet.write(row, 0, row, data_format)
            refs.append(row)
            ref_index[well.name] = row
            lzs.append(well.interval)
            worksheet.write(row, 1, well.api, data_format)
            worksheet.write(row, 2, well.name, data_format)
            worksheet.write(row, 3, well.gun_barrel_x, data_format)
            worksheet.write(row, 4, well.subsurface_depth, data_format)
            worksheet.write(row, 5, "TBD", data_format) 
            row = row + 1
        last_row = row
        other_well_series_1 = {
            "categories": f"='Plot Data'!$D${first_row}:$D${last_row}",         # Dynamic X-values
            "values": f"='Plot Data'!$E${first_row}:$E${last_row}",             # Dynamic Y-values
            "marker": {"type": "circle", "size": 12, "fill": {"color": "green"}},
            "data_labels": {
                "value": True,
                "position": "center","custom": 
                [{"value": ref, "index": ref} for ref in refs], 
                "font": {
                    "size": 12,
                    "bold": True,
                },
            }
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

        worksheet.autofit()

        return ref_index, target_well_series_1, target_well_series_2, other_well_series_1, other_well_series_2

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
        worksheet = workbook.add_worksheet("Annotation")

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
        vertical_line_categories = "='Annotation'!$A$2:$A$3"
        vertical_line_values = "='Annotation'!$B$2:$B$3"
        annotation_categories = "='Annotation'!$D$2:$D$2"
        annotation_values = "='Annotation'!$E$2:$E$2"

        return vertical_line_categories, vertical_line_values, annotation_categories, annotation_values

    def create_line_series_data_worksheet(self, 
                                         workbook: Workbook, 
                                         worksheet: worksheet,  
                                         ref_index: dict,
                                         target_wells: list[Analysis], 
                                         other_wells: list[Analysis]):
        try:
            results = []
            pairs = []

            data_format = workbook.add_format({
                'align': 'center',
                'border': 1,
                'text_wrap': True
            })

            header_format = workbook.add_format({
                'bold': True,
                'align': 'center',
                'bg_color': '#DDEBF7',
                'border': 1,
                'text_wrap': True
            })  

            worksheet.write(0, 0, "Target Ref #", header_format)
            worksheet.write(0, 1, "Offset Ref #", header_format)
            worksheet.write(0, 2, "Target X", header_format)
            worksheet.write(0, 3, "Offset X", header_format)   
            worksheet.write(0, 4, "Target Y", header_format)
            worksheet.write(0, 5, "Offset Y", header_format)
            worksheet.write(0, 6, "Distance", header_format)
            worksheet.write(0, 7, "Midpoint X", header_format)
            worksheet.write(0, 8, "Midpoint Y", header_format)

            row = 1
            for target_well in target_wells:
                for other_well in other_wells:
                    x_distance = abs(target_well.lateral_end_grid_x - other_well.lateral_end_grid_x)
                    y_distance = abs(target_well.subsurface_depth - other_well.subsurface_depth)
                    hypotenuse_distance = int(math.sqrt(x_distance**2 + y_distance**2))
                    worksheet.write(row, 0, ref_index[target_well.name], data_format)
                    worksheet.write(row, 1, ref_index[other_well.name], data_format)
                    worksheet.write(row, 2, target_well.gun_barrel_x, data_format)
                    worksheet.write(row, 3, other_well.gun_barrel_x, data_format)
                    worksheet.write(row, 4, target_well.subsurface_depth, data_format)
                    worksheet.write(row, 5, other_well.subsurface_depth, data_format)
                    worksheet.write(row, 6, hypotenuse_distance, data_format)
                    worksheet.write(row, 7, int((target_well.gun_barrel_x + other_well.gun_barrel_x) / 2), data_format)
                    worksheet.write(row, 8, int((target_well.subsurface_depth + other_well.subsurface_depth) / 2), data_format)
                    row = row + 1
                    if hypotenuse_distance < self.context.hypotenuse_distance_threshold:  
                        pairs.append((target_well.name, other_well.name))
                        results.append({
                            "categories": f"='Line Series'!$C${row}:$D${row}",
                            "values": f"='Line Series'!$E${row}:$F${row}",
                            "line": {
                                "color": "black",
                                "width": .5,
                                "dash_type": "dash",
                            },
                            "marker": {"type": "none"},
                        })

                        results.append({
                            "categories":  f"='Line Series'!$H${row}:$H${row}",
                            "values":  f"='Line Series'!$I${row}:$I${row}",
                            "marker": {"type": "none"}, 
                            "data_labels": {
                                "value": False,
                                "position": "center",
                                "custom": [{"value": f"='Line Series'!$G${row}", 
                                            "index": f"='Line Series'!$G${row}"}],
                                "font": {
                                    "size": 10 
                                },          
                            },
                        })
     
            worksheet.autofit()

            return results, pairs
        except Exception as e:
            raise e
        
    def create_plot(self, 
                    workbook: Workbook, 
                    worksheet: worksheet,
                    title: str, 
                    section_line_label: str, 
                    target_well_series_1: dict,
                    target_well_series_2: dict,
                    other_well_series_1: dict,
                    other_well_series_2: dict,
                    line_series: list[dict]):
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
                "name": "Bottom hole lateral distance from section line (100 ft intervals)",
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
                "name": "Bottom hole depth below MSL (100 ft intervals)",
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

            for series in line_series:
                plot.add_series(series)

            worksheet.insert_chart("B4", plot)

            return None
        except Exception as e:
            raise e

    def create_calulated_data_worksheet(self, 
                                        workbook, worksheet,
                                        pairs: list[tuple[str, str]],
                                        ref_index: dict,
                                        analysis_service: AnalysisService,
                                        target_well_information_service: TargetWellInformationService,
                                        well_service: WellService):
        try:
            headers = [
                'target_well_index',
                'offset_well_index',
                'Target Well Name',	
                'Offset Well Name',	
                'Targete Well First Prod Date',	
                'Offset Well First Prod Date',	
                'Months to First Production',	
                'Target Well Perf Interval',	
                'Offset Well Perf Interval',	
                'Offset Well Cum Oil Date',	
                'overlap_feet',	
                'overlap_percentage',
                'Cum Oil',	
                'cumulative_oil_per_ft',	
                'overlap_cumulative_oil_ft',	
                'months_from_first_production',	
                'horizontal_distance',	
                'vertical_distance',	
                'three_d_distance']
            
            data_format = workbook.add_format({
                'align': 'center',
                'border': 1,
                'text_wrap': True
            })

            header_format = workbook.add_format({
                'bold': True,
                'align': 'center',
                'bg_color': '#DDEBF7',
                'border': 1,
                'text_wrap': True
            })  

            row = 0
            for i, header in enumerate(headers):
                worksheet.write(row, i, header, header_format)

            row = 1
            for pair in pairs:
                target_well_analysis = analysis_service.get_by_name(pair[0])
                target_well_information = target_well_information_service.get_by_name(pair[0])
                offset_well_analysis = analysis_service.get_by_name(pair[1])
                offset_well = well_service.get_by_api(offset_well_analysis.api)
                overlap = self.calculate_overlap(target_well_analysis, offset_well_analysis)
                worksheet.write(row, 0, ref_index[target_well_analysis.name], data_format)
                worksheet.write(row, 1, ref_index[offset_well_analysis.name], data_format)
                worksheet.write(row, 2, target_well_analysis.name, data_format)
                worksheet.write(row, 3, offset_well_analysis.name, data_format)
                worksheet.write(row, 4, target_well_analysis.first_production_date, data_format)
                worksheet.write(row, 5, offset_well_analysis.first_production_date, data_format)
                worksheet.write(row, 6, "TBD", data_format)
                worksheet.write(row, 7, target_well_information.perf_interval_ft, data_format)
                perf_interval = offset_well.lateral_length if offset_well.perf_interval is None else offset_well.perf_interval
                worksheet.write(row, 8, perf_interval, data_format)
                worksheet.write(row, 9, offset_well.last_producing_month, data_format)
                worksheet.write(row, 10, overlap["overlap_feet"], data_format)
                worksheet.write(row, 11, overlap["overlap_percentage"], data_format)
                worksheet.write(row, 12, offset_well.cumlative_oil, data_format)
                cumulative_oil_per_ft = math.ceil(offset_well.cumlative_oil / perf_interval)
                worksheet.write(row, 13, cumulative_oil_per_ft, data_format)
                overlap_cumulative_oil_ft = math.ceil(overlap["overlap_percentage"] * (cumulative_oil_per_ft/100))
                worksheet.write(row, 14, overlap_cumulative_oil_ft, data_format)
                months_from_first_production_date = self.months_between_dates(offset_well_analysis.first_production_date, target_well_analysis.first_production_date)
                worksheet.write(row, 15, months_from_first_production_date, data_format)
                adjacent = int(abs(offset_well_analysis.gun_barrel_x - target_well_analysis.gun_barrel_x))
                opposite = int(abs(offset_well_analysis.subsurface_depth - target_well_analysis.subsurface_depth))
                hypotenuse = int(math.sqrt(adjacent**2 + opposite**2))
                worksheet.write(row, 16, adjacent, data_format)
                worksheet.write(row, 17, opposite, data_format)
                worksheet.write(row, 18, hypotenuse, data_format)
                row = row + 1

            worksheet.autofit()

        except Exception as e:
            raise e
        
    def calculate_overlap(self, target_well: Analysis, offset_well: Analysis) -> dict:
        try:
            results = {}

            if (target_well.dominant_direction == 'N' and offset_well.dominant_direction == 'S' or
               target_well.dominant_direction == 'S' and offset_well.dominant_direction == 'N'):
                    overlap = int(target_well.lateral_length)
                    if target_well.lateral_end_grid_y - offset_well.lateral_start_grid_y > 0:
                        overlap = overlap - int((target_well.lateral_end_grid_y - offset_well.lateral_start_grid_y))
                    if target_well.lateral_start_grid_y - offset_well.lateral_end_grid_y < 0:
                        overlap = overlap - int(abs(target_well.lateral_start_grid_y - offset_well.lateral_end_grid_y))
                    overlap_percentage = math.ceil((overlap/target_well.lateral_length)*100)
                    results["overlap_feet"] = overlap
                    results["overlap_percentage"] = overlap_percentage
            if (target_well.dominant_direction == 'N' and offset_well.dominant_direction == 'N' or 
               target_well.dominant_direction == 'S' and offset_well.dominant_direction == 'S'):
                overlap = int(target_well.lateral_length)
                if target_well.lateral_end_grid_y - offset_well.lateral_end_grid_y > 0:
                    overlap = overlap - int((target_well.lateral_end_grid_y - offset_well.lateral_end_grid_y))
                if target_well.lateral_start_grid_y - offset_well.lateral_start_grid_y < 0:
                    overlap = overlap - int(abs(target_well.lateral_start_grid_y - offset_well.lateral_start_grid_y))
                overlap_percentage = math.ceil((overlap/target_well.lateral_length)*100)
                results["overlap_feet"] = overlap
                results["overlap_percentage"] = overlap_percentage
            if (target_well.dominant_direction == 'E' and offset_well.dominant_direction == 'W' or
                target_well.dominant_direction == 'W' and offset_well.dominant_direction == 'E'):
                overlap = int(target_well.lateral_length)
                if target_well.lateral_end_grid_x - offset_well.lateral_start_grid_x > 0:
                    overlap = overlap - int((target_well.lateral_end_grid_x - offset_well.lateral_start_grid_x))
                if target_well.lateral_start_grid_x - offset_well.lateral_end_grid_x < 0:
                    overlap = overlap - int(abs(target_well.lateral_start_grid_x - offset_well.lateral_end_grid_x))
                overlap_percentage = math.ceil((overlap/target_well.lateral_length)*100)
                results["overlap_feet"] = overlap
                results["overlap_percentage"] = overlap_percentage
            if (target_well.dominant_direction == 'E' and offset_well.dominant_direction == 'E' or  
                target_well.dominant_direction == 'W' and offset_well.dominant_direction == 'W'):
                overlap = int(target_well.lateral_length)
                if target_well.lateral_end_grid_x - offset_well.lateral_end_grid_x > 0:
                    overlap = overlap - int((target_well.lateral_end_grid_x - offset_well.lateral_end_grid_x))
                if target_well.lateral_start_grid_x - offset_well.lateral_start_grid_x < 0:
                    overlap = overlap - int(abs(target_well.lateral_start_grid_x - offset_well.lateral_start_grid_x))
                overlap_percentage = math.ceil((overlap/target_well.lateral_length)*100)
                results["overlap_feet"] = overlap
                results["overlap_percentage"] = overlap_percentage

            return results
        except Exception as e:
            raise e

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

            plot_worksheet = workbook.add_worksheet("Plot")
            well_data_worksheet = workbook.add_worksheet("Well Data")
            plot_data_worksheet = workbook.add_worksheet("Plot Data")
            calculated_data_worksheet = workbook.add_worksheet("Calculated Data")
            line_series_data_worksheet = workbook.add_worksheet("Line Series")

            ref_index, target_well_series_1, target_well_series_2, other_well_series_1, other_well_series_2 = self.create_plot_data_worksheet(workbook, plot_data_worksheet, target_wells, other_wells)

            self.create_well_data_worksheet(workbook, well_data_worksheet, well_service, ref_index, other_wells)

            line_series, pairs = self.create_line_series_data_worksheet(workbook, line_series_data_worksheet, ref_index, target_wells, other_wells)    

            self.create_plot(workbook, 
                             plot_worksheet,
                             plot_title, 
                             section_line_label, 
                             target_well_series_1, 
                             target_well_series_2, 
                             other_well_series_1,
                             other_well_series_2,
                             line_series)   

            self.create_calulated_data_worksheet(workbook, 
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