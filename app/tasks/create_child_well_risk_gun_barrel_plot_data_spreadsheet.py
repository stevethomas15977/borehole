from tasks.task import Task
from tasks.task_enum import TASKS
from helpers import task_logger
from services import (AnalysisService, 
                      TargetWellInformationService, 
                      WellService,
                      StratigraphicService,
                      XYZDistanceService,
                      OverlapService)
from traceback import format_exc
import pandas as pd
import os
import openpyxl
from openpyxl.drawing.image import Image

class CreateChildWellRiskGunBarrelPlotDataSpreadsheet(Task):

    def determine_color(self, status) -> str:
        color = "white"
        if "COMPLETED" == status:
            color = "black"
        elif "DRILLED" == status:
            color = "magenta"
        elif "DUC" == status:
            color = "blue"
        elif "INACTIVE PRODUCER" == status:
            color = "yellow"
        elif "PERMIT EXPIRED" == status:
            color = "black"
        elif "PERMITTED" == status:
            color = "red"
        elif "PRODUCING" == status:
            color = "green"
        else:
            color = "white"
        return color

    def execute(self):
        task = TASKS.CREATE_CHILD_WELL_RISK_GUN_BARREL_PLOT_DATA_SPREADSHEET.value
        logger = task_logger(task, self.context.logs_path)
        try:
            analysis_service = AnalysisService(db_path=self.context.db_path)
            target_well_information_service = TargetWellInformationService(self.context.db_path)
            well_service = WellService(self.context.db_path)
            stratigraphic_service = StratigraphicService(self.context.db_path)
            xyz_distance_service = XYZDistanceService(self.context.db_path)
            overlap_service = OverlapService(self.context.db_path)
            
            summary_rows = []
            distances_rows = []
            overlap_rows = []

            offsets = analysis_service.select_where_target_well_spacing_gun_barrel_plot_flag_is_true()
            for i, offset in enumerate(offsets):
                api = offset.api
                well_name = offset.name
                if "11-111" in offset.api:
                    target_well = target_well_information_service.get_by_name(well_name)
                    status = "PERMITTED"
                    landing_zone = target_well.afe_landing_zone
                    production_date = f""
                    color = "orange"
                else:
                    well = well_service.get_by_api(api)
                    status = well.status
                    stratigraphic = stratigraphic_service.get_by_prism_code(well.interval)
                    if stratigraphic:
                        landing_zone = stratigraphic.union_code
                    else:
                        landing_zone = well.interval
                    production_date = offset.first_production_date

                    color = self.determine_color(well.status)

                summary_row = {
                    'No.': i,
                    'API': api,
                    'WellName': well_name,
                    'Status': status,
                    'LandingZone': landing_zone,
                    'FirstProductionDate': production_date,
                    'X from line (ft)': offset.gun_barrel_x,
                    'Z depth (ft)': offset.lateral_end_subsurface_depth,
                    'Lateral (ft)': int(offset.lateral_length),
                    'Color': color
                    }
                summary_rows.append(summary_row)

                distances = xyz_distance_service.get_by_target_well(api)
                for distance in distances:
                    distances_row = {
                        'A_API': distance.reference_api,
                        'A_Well_Name': distance.reference_name,
                        'B_API': distance.target_api,
                        'B_Well_Name': distance.target_name,
                        'Lateral Start X': distance.start_x,
                        'Lateral Start Y': distance.start_y,
                        'Lateral Start Z': distance.start_z,
                        'Lateral Start Hypotenuse': distance.start_hypotenuse,
                        'Lateral Midpoint X': distance.mid_x,
                        'Lateral Midpoint Y': distance.mid_y,
                        'Lateral Midpoint Z': distance.mid_z,
                        'Lateral Midpoint Hypotenuse': distance.mid_hypotenuse,
                        'Lateral End X': distance.end_x,
                        'Lateral End Y': distance.end_y,
                        'Lateral End Z': distance.end_z,
                        'Lateral End Hypotenuse': distance.end_hypotenuse
                    }
                    distances_rows.append(distances_row)

                    overlap = overlap_service.get_by_reference_api_target_api(distance.reference_api, distance.target_api)
                    if overlap:
                        overlap_row = {
                            'A_API': overlap.reference_api,
                            'A_Well_Name': overlap.reference_name,
                            'B_API': overlap.target_api,
                            'B_Well_Name': overlap.target_name,
                            'Overlap_FT': overlap.overlap_feet,
                            'Overlap_%': overlap.overlap_percentage
                        }
                        overlap_rows.append(overlap_row)

            plot_df = pd.DataFrame([])
            summary_df = pd.DataFrame(summary_rows)
            distances_df = pd.DataFrame(distances_rows)
            overlap_df = pd.DataFrame(overlap_rows)

            # Save to excel
            plot_name = "child-well-risk"
            excel_file = os.path.join(self.context.project_path, f"{self.context.project}-{plot_name}-gun-barrel-plot-{self.context.version}.xlsx")
            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                plot_df.to_excel(writer, sheet_name='plot', index=False)
                summary_df.to_excel(writer, sheet_name='summary', index=False)
                distances_df.to_excel(writer, sheet_name='distances', index=False)
                overlap_df.to_excel(writer, sheet_name='overlap', index=False)

            wb = openpyxl.load_workbook(excel_file)
            ws = wb['plot']
            image_path = os.path.join(self.context.project_path, f"{self.context.project}-child-well-risk-gun-barrel-plot-{self.context.version}.png")
            if os.path.exists(image_path):
                img = Image(image_path)
                original_width = img.width
                original_height = img.height
                scaled_width = int(original_width * 0.40)
                scaled_height = int(original_height * 0.40)
                img.width = scaled_width
                img.height = scaled_height                
                ws.add_image(img, 'A1')
                wb.save(excel_file)
            else:
                logger.error(f"Image file not found: {image_path}")
        except Exception as e:
            logger.error(f"Error in {task} workflow task: {e}\n{format_exc()}")
            raise ValueError(f"Error in {task} workflow task: {e}")
