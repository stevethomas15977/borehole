from context import Context
from tasks.etl_target_well_information import ETLTargetWellInformation
from tasks.load_texas_land_survey_system import LoadTexasLandSurveySystem
from tasks.create_database import CreateDatabase
from tasks.load_target_well_information import LoadTargetWellInformation
from tasks.load_well_data import LoadWellData
from tasks.load_survey_data import LoadSurveyData
from tasks.etl_well import ETLWell
from tasks.calculate_xyzdistance import CalculateXYZDistance
from tasks.calculate_latitudelongitudedistance import CalculateLatitudeLongitudeDistance
from tasks.create_gun_barrel_plot import CreateGunBarrelPlot
from tasks.determine_adjacent_wells import DetermineAdjacentWells
from tasks.determine_codevelopment_wells import DetermineCodevelopmentWells
from tasks.determine_well_grouping import DetermineWellGrouping
from tasks.calculate_well_average_spacing import CalculateWellAverageSpacing
from tasks.calculate_well_group_average_spacing import CalculateWellGroupAverageSpacing
from tasks.determine_parent_child_wells import DetermineParentChildWells
from tasks.determine_bounded_wells import DetermineBoundedWells
from tasks.create_offset_well_identification_excel import CreateOffsetWellIdentificationExcel
from tasks.create_surface_map import CreateSurfaceMap
from tasks.create_codevelopment_group_surface_map import CreateCodevelopmentGroupSurfaceMap
from tasks.detemine_well_spacing_gun_barrel_plot_wells import DetermineWellSpacingGunBarrelPlotWells
from tasks.create_gun_barrel_surface_map import CreateGunBarrelSurfaceMap
from tasks.offset_well_identification_workflow_database_management import OffsetWellIdenficationWorkflowDatabaseManagement
from tasks.load_lookup_tables import LoadLookupTables
from tasks.create_child_well_risk_gun_barrel_plot import CreateChildWellRiskGunBarrelPlot
from tasks.calculate_well_overlap_percentage import CalculateWellOverlapPercentage
from tasks.gun_barrel_plot_workflow_database_management import GunBarrelPlotWorkflowDatabaseManagement
from tasks.create_simulated_well import CreateSimulatedWell
from tasks.create_target_well_analysis import CreateTargetWellAnalysis
from tasks.create_simulated_well_map import CreateSimulatedWellMap
from tasks.create_child_well_risk_gun_barrel_plot_3d import CreateChildWellRiskGunBarrelPlot3D
from tasks.validate_target_well_information import ValidateTargetWellInformation
from tasks.create_child_well_risk_gun_barrel_plot_data_spreadsheet import CreateChildWellRiskGunBarrelPlotDataSpreadsheet
from tasks.create_child_well_risk_gun_barrel_plot_zoomed import CreateChildWellRiskGunBarrelPlotZoomed
from tasks.create_cross_plot import CreateCrossPlot
from tasks.enrich_gun_barrel import EnrichGunBarrel
from tasks.create_gun_barrel_excel import CreateGunBarrelExcel
from tasks.create_excel_native_gun_barrel_plot import CreateExcelNativeGunBarrelPlot
from tasks.determine_well_grouping_avg_cum_oil_bbl_per_ft import DetermineWellGroupingAvgCumOilBblPerFT

from tasks.task import Task
from tasks.task_enum import TASKS

class TaskFactory:
    def __init__(self, context: Context):
        self.context = context

    def create_task(self, task_type: str) -> Task:
        if task_type == TASKS.CREATE_DATABASE.value:
            return CreateDatabase(self.context)
        elif task_type == TASKS.LOAD_LOOKUP_TABLES.value:
            return LoadLookupTables(self.context)
        elif task_type == TASKS.LOAD_TARGET_WELL_INFORMATION.value:
            return LoadTargetWellInformation(self.context)
        elif task_type == TASKS.LOAD_WELL_DATA.value:
            return LoadWellData(self.context)
        elif task_type == TASKS.LOAD_SURVEY_DATA.value:
            return LoadSurveyData(self.context)
        elif task_type == TASKS.ETL_WELL.value:
            return ETLWell(self.context)
        elif task_type == TASKS.ETL_TARGET_WELL_INFORMATION.value:
            return ETLTargetWellInformation(self.context)
        elif task_type == TASKS.CALCULATE_XYZ_DISTANCE.value:
            return CalculateXYZDistance(self.context)
        elif task_type == TASKS.CALCULATE_LATITUDE_LONGITUDE_DISTANCE.value:
            return CalculateLatitudeLongitudeDistance(self.context)
        elif task_type == TASKS.LOAD_TEXAS_LAND_SURVEY_SYSTEM.value:
            return LoadTexasLandSurveySystem(self.context)
        elif task_type == TASKS.CREATE_GUN_BARREL_PLOT.value:
            return CreateGunBarrelPlot(self.context)
        elif task_type == TASKS.DETERMINE_ADJACENT_WELLS.value:
            return DetermineAdjacentWells(self.context)
        elif task_type == TASKS.DETERMINE_CODEVELOPMENT_WELLS.value:
            return DetermineCodevelopmentWells(self.context)
        elif task_type == TASKS.DETERMINE_WELL_GROUPING.value:
            return DetermineWellGrouping(self.context)
        elif task_type == TASKS.CALCULATE_WELL_AVERAGE_SPACING.value:
            return CalculateWellAverageSpacing(self.context)
        elif task_type == TASKS.CALCULATE_WELL_GROUP_AVERAGE_SPACING.value:
            return CalculateWellGroupAverageSpacing(self.context)
        elif task_type == TASKS.DETERMINE_PARENT_CHILD_WELLS.value:
            return DetermineParentChildWells(self.context)
        elif task_type == TASKS.DETERMINE_BOUNDED_WELLS.value:
            return DetermineBoundedWells(self.context)
        elif task_type == TASKS.CREATE_OFFSET_WELL_IDENTIFICATION_EXCEL.value:
            return CreateOffsetWellIdentificationExcel(self.context)
        elif task_type == TASKS.CREATE_SURFACE_MAP.value:
            return CreateSurfaceMap(self.context)
        elif task_type == TASKS.CREATE_CODEVELOPMENT_GROUP_SURFACE_MAP.value:
            return CreateCodevelopmentGroupSurfaceMap(self.context)
        elif task_type == TASKS.DETERMINE_WELL_SPACING_GUN_BARREL_PLOT_WELLS.value:
            return DetermineWellSpacingGunBarrelPlotWells(self.context)
        elif task_type == TASKS.CREATE_GUN_BARREL_SURFACE_MAP.value:
            return CreateGunBarrelSurfaceMap(self.context)
        elif task_type == TASKS.OFFSET_WELL_IDENTIFICATION_WORKFLOW_DATABASE_MANAGEMENT.value:
            return OffsetWellIdenficationWorkflowDatabaseManagement(self.context)
        elif task_type == TASKS.CREATE_CHILD_WELL_RISK_GUN_BARREL_PLOT.value:
            return CreateChildWellRiskGunBarrelPlot(self.context)  
        elif task_type == TASKS.CALCULATE_WELL_OVERLAP_PERCENTAGE.value:
            return CalculateWellOverlapPercentage(self.context)
        elif task_type == TASKS.GUN_BARREL_PLOT_WORKFLOW_DATABASE_MANAGEMENT.value:
            return GunBarrelPlotWorkflowDatabaseManagement(self.context)
        elif task_type == TASKS.CREATE_SIMULATED_WELL.value:
            return CreateSimulatedWell(self.context)
        elif task_type == TASKS.CREATE_TARGET_WELL_ANALYSIS.value:
            return CreateTargetWellAnalysis(self.context)
        elif task_type == TASKS.CREATE_SIMULATED_WELL_MAP.value:
            return CreateSimulatedWellMap(self.context)
        elif task_type == TASKS.CREATE_CHILD_WELL_RISK_GUN_BARREL_PLOT_3D.value:
            return CreateChildWellRiskGunBarrelPlot3D(self.context)
        elif task_type == TASKS.VALIDATE_TARGET_WELL_INFORMATION.value:
            return ValidateTargetWellInformation(self.context)
        elif task_type == TASKS.CREATE_CHILD_WELL_RISK_GUN_BARREL_PLOT_DATA_SPREADSHEET.value:
            return CreateChildWellRiskGunBarrelPlotDataSpreadsheet(self.context)
        elif task_type == TASKS.CREATE_CHILD_WELL_RISK_GUN_BARREL_PLOT_ZOOMED.value:
            return CreateChildWellRiskGunBarrelPlotZoomed(self.context)
        elif task_type == TASKS.CREATE_CROSS_PLOT.value:
            return CreateCrossPlot(self.context)
        elif task_type == TASKS.ENRICH_GUN_BARREL.value:
            return EnrichGunBarrel(self.context)
        elif task_type == TASKS.CREATE_GUN_BARREL_EXCEL.value:
            return CreateGunBarrelExcel(self.context)
        elif task_type == TASKS.CREATE_EXCEL_NATIVE_GUN_BARREL_PLOT.value:
            return CreateExcelNativeGunBarrelPlot(self.context) 
        elif task_type == TASKS.DETERMINE_WELL_GROUPING_AVG_CUM_OIL_BBL_PER_FT.value:
            return DetermineWellGroupingAvgCumOilBblPerFT(self.context)
        else:
            raise ValueError(f"Unknown task type: {task_type}")