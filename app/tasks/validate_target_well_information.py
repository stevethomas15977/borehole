
from tasks.task import Task
from tasks.task_enum import TASKS
from helpers import task_logger
from traceback import format_exc
from pandas import isna, read_excel
import openpyxl
openpyxl.reader.excel.warnings.simplefilter(action='ignore')

class ValidateTargetWellInformation(Task):

    headers = [
            "id", 
            "name", 
            "api", 
            "afe_landing_zone",
            "logs_landing_zone",
            "enverus_status",
            "afe_md_ft",
            "afe_bhl_tvd_ft",
            "surveys_preforated_interval_ft",
            "afe_gross_dollar",
            "well_cost",
            "seller_effective_gross_nri_percentage",
            "seller_net_nri_percentage",
            "seller_gross_for_sale_percentage",
            "afe_gwi_for_sale_net_capital_dollar",
            "enverus_rkb_elevation_ft",
            "bhl_tvd_ss_ft",
            "afe_in_landing_zone_hyp_spacing_ft",
            "state",
            "county",
            "tx_abstract_southwest_corner",
            "tx_block_southwest_corner",
            "nw_township_southwest_corner",
            "nm_range_southwest_corner",
            "nm_tx_section_southwest_corner",
            "nad_system",
            "nad_zone",
            "x_surface_location",
            "y_surface_location",
            "x_first_take_point",
            "y_first_take_point",
            "x_last_take_point",
            "y_last_take_point",
            "x_bottom_hole",
            "y_bottom_hole",
            "latitude_surface_location",
            "longitude_surface_location",
            "latitude_first_take_point",
            "longitude_first_take_point",
            "latitude_last_take_point",
            "longitude_last_take_point",
            "latitude_bottom_hole",
            "longitude_bottom_hole",
            "legal_tx_abstract_surface_location",
            "Legal_tx_block_surface_location",
            "legal_nw_township_surface_location",
            "legal_nm_tx_section_surface_location",
            "legal_fnl_surface_location",
            "legal_fsl_surface_location",
            "legal_fwl_surface_location",
            "legal_fel_surface_location",
            "legal_tx_abstract_first_take_point",
            "Legal_tx_block_first_take_point",
            "legal_nw_township_first_take_point",
            "legal_nm_tx_section_first_take_point",
            "legal_fnl_first_take_point",
            "legal_fsl_first_take_point",
            "legal_fwl_first_take_point",
            "legal_fel_first_take_point",
            "legal_tx_abstract_last_take_point",
            "Legal_tx_block_last_take_point",
            "legal_nw_township_last_take_point",
            "legal_nm_tx_section_last_take_point",
            "legal_fnl_last_take_point",
            "legal_fsl_last_take_point",
            "legal_fwl_last_take_point",
            "legal_fel_last_take_point",
            "legal_tx_abstract_bottom_hole",
            "Legal_tx_block_bottom_hole",
            "legal_nw_township_bottom_hole",
            "legal_nm_tx_section_bottom_hole",
            "legal_fnl_bottom_hole",
            "legal_fsl_bottom_hole",
            "legal_fwl_bottom_hole",
            "legal_fel_bottom_hole",
            "perf_interval_ft"
            ]

    def execute(self):
        task = TASKS.VALIDATE_TARGET_WELL_INFORMATION.value
        logger = task_logger(task, self.context.logs_path)
        try:
            # Load the Excel file
            df = read_excel(self.context.target_well_information_file, engine='openpyxl', header=None)

            # Find the row index where the first column has the text "No."
            start_row = df[df[0] == 'No.'].index[0]

            # Adjust to start reading from start_row + 2
            adjusted_start_row = start_row + 1

            # Read the Excel file starting from the adjusted row without headers
            wells = read_excel(
                self.context.target_well_information_file,
                skiprows=adjusted_start_row,
                header=None,  # No headers applied yet
                engine='openpyxl'
            )

            # Read the Excel file starting from the adjusted row with headers
            wells = read_excel(
                self.context.target_well_information_file,
                skiprows=adjusted_start_row,
                header=None,
                names=self.headers,
                engine='openpyxl'
            )

            # Identify the first row with NaN in the 'id' column
            nan_row_index = wells[wells['id'].isna()].index.min()

            # If a NaN value is found, slice the DataFrame up to that row
            if not isna(nan_row_index):
                wells = wells.iloc[:nan_row_index]

            for row in wells.itertuples(index=False):

                if isna(row.name):
                    raise Exception(f"Error - Well Name is missing")
                if isna(row.afe_landing_zone):
                    raise Exception(f"Error - AFE Landing Zone is missing")
                if isna(row.logs_landing_zone):
                    raise Exception(f"Error - Logs Landing Zone is missing")
                if isna(row.afe_md_ft):
                    raise Exception(f"Error - AFE MD FT is missing")
                # if isna(row.afe_bhl_tvd_ft):
                #     raise Exception(f"Error - AFE BHL TVD FT is missing")
                if isna(row.surveys_preforated_interval_ft):
                    raise Exception(f"Error - Surveys Preforated Interval FT is missing")
                # if isna(row.enverus_rkb_elevation_ft):
                #     raise Exception(f"Error - RBK Elevation FT is missing")
                if isna(row.bhl_tvd_ss_ft):
                    raise Exception(f"Error - BHL TVD SS FT is missing")
                if isna(row.state):
                    raise Exception(f"Error - State is missing")
                if isna(row.county):
                    raise Exception(f"Error - County is missing")
                if row.state not in ['TX', 'NM']:
                    raise Exception(f"Error - State is not TX or NM")
                if row.state == 'TX':
                    if isna(row.tx_abstract_southwest_corner):
                        raise Exception(f"Error - TX Abstract Southwest Corner is missing")
                    if isna(row.tx_block_southwest_corner):
                        raise Exception(f"Error - TX Block Southwest Corner is missing")
                    if isna(row.nm_tx_section_southwest_corner):
                        raise Exception(f"Error - NM TX Section Southwest Corner is missing")
                if row.state == 'NM':
                    if isna(row.nw_township_southwest_corner):
                        raise Exception(f"Error - NW Township Southwest Corner is missing")
                    if isna(row.nm_range_southwest_corner):
                        raise Exception(f"Error - NM Range Southwest Corner is missing")
                    if isna(row.nm_tx_section_southwest_corner):
                        raise Exception(f"Error - NM TX Section Southwest Corner is missing")
                if isna(row.x_surface_location):
                    raise Exception(f"Error - X Surface Location is missing")
                if isna(row.y_surface_location):
                    raise Exception(f"Error - Y Surface Location is missing")
                if isna(row.x_first_take_point):
                    raise Exception(f"Error - X First Take Point is missing")
                if isna(row.y_first_take_point):
                    raise Exception(f"Error - Y First Take Point is missing")
                if isna(row.x_last_take_point):
                    raise Exception(f"Error - X Last Take Point is missing")
                if isna(row.y_last_take_point):
                    raise Exception(f"Error - Y Last Take Point is missing")
                if isna(row.x_bottom_hole):
                    raise Exception(f"Error - X Bottom Hole is missing")
                if isna(row.y_bottom_hole):
                    raise Exception(f"Error - Y Bottom Hole is missing")
                
            logger.info(f"{task}: {self.context.logs_path}")
        except Exception as e:
            logger.error(f"Error {task} workflow task: {e}\n{format_exc()}")
            raise ValueError(f"Error {task} workflow task: {e}")