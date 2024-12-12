from enum import Enum

class TASKS(Enum):

    # AFE Project Initiation Workflow Group Tasks
    CREATE_DATABASE = 'create_database'
    LOAD_LOOKUP_TABLES = 'load_lookup_tables'
    LOAD_TARGET_WELL_INFORMATION = 'load_target_well_information'
    LOAD_WELL_DATA = 'load_well_data'
    LOAD_SURVEY_DATA = 'load_survey_data'
    VALIDATE_TARGET_WELL_INFORMATION = 'validate_target_well_information'
    
    # AFE Base Workflow Group Tasks
    ETL_WELL = 'etl_well'
    ETL_TARGET_WELL_INFORMATION = 'etl_target_well_information'
    CREATE_TARGET_WELL_ANALYSIS = 'create_target_well_analysis'
    CREATE_SIMULATED_WELL = 'create_simulated_well'
    CREATE_SIMULATED_WELL_MAP = 'create_simulated_well_map'
    CALCULATE_XYZ_DISTANCE = 'calculate_xyz_distance'
    CALCULATE_LATITUDE_LONGITUDE_DISTANCE = 'calculate_latitudelongitudedistance'

    # Offset Well Identification Workflow Group Tasks
    OFFSET_WELL_IDENTIFICATION_WORKFLOW_DATABASE_MANAGEMENT = 'offset_well_identification_workflow_database_management'
    DETERMINE_ADJACENT_WELLS = 'determine_adjacent_wells' 
    DETERMINE_CODEVELOPMENT_WELLS = 'determine_codevelopment_wells'
    DETERMINE_WELL_GROUPING = 'determine_well_grouping'
    CALCULATE_WELL_AVERAGE_SPACING = 'calculate_well_average_spacing'
    CALCULATE_WELL_GROUP_AVERAGE_SPACING = 'calculate_well_group_average_spacing'
    DETERMINE_PARENT_CHILD_WELLS = 'determine_parent_child_wells'
    DETERMINE_BOUNDED_WELLS = 'determine_bounded_wells'
    CREATE_OFFSET_WELL_IDENTIFICATION_EXCEL = 'create_offset_well_identification_excel'
    CREATE_SURFACE_MAP = 'create_surface_map'
    CREATE_CODEVELOPMENT_GROUP_SURFACE_MAP = 'create_codevelopment_group_surface_map'
    DETERMINE_WELL_GROUPING_AVG_CUM_OIL_BBL_PER_FT = 'determine_well_grouping_avg_cum_oil_bbl_per_ft'

    # Well Spacing Gun Barrel Plot Workflow Group Tasks
    GUN_BARREL_PLOT_WORKFLOW_DATABASE_MANAGEMENT = 'gun_barrel_plot_workflow_database_management'
    CALCULATE_WELL_OVERLAP_PERCENTAGE = 'calculate_well_overlap_percentage'
    DETERMINE_WELL_SPACING_GUN_BARREL_PLOT_WELLS = 'detemine_well_spacing_gun_barrel_plot_wells'
    ENRICH_GUN_BARREL = 'enrich_gun_barrel'
    CREATE_GUN_BARREL_SURFACE_MAP = 'create_gun_barrel_surface_map'
    CREATE_GUN_BARREL_EXCEL = 'create_gun_barrel_excel'

    CREATE_CHILD_WELL_RISK_GUN_BARREL_PLOT = 'create_child_well_risk_gun_barrel_plot'
    CREATE_CHILD_WELL_RISK_GUN_BARREL_PLOT_ZOOMED = 'create_child_well_risk_gun_barrel_plot_zoomed'
    CREATE_CHILD_WELL_RISK_GUN_BARREL_PLOT_3D = 'create_child_well_risk_run_barrel_plot_3d'
    CREATE_CHILD_WELL_RISK_GUN_BARREL_PLOT_DATA_SPREADSHEET = 'create_child_well_risk_gun_barrel_plot_data_spreadsheet'
    CREATE_GUN_BARREL_PLOT = 'create_gun_barrel_plot'
    CREATE_CROSS_PLOT = 'create_cross_plot'
    CREATE_EXCEL_NATIVE_GUN_BARREL_PLOT = 'create_excel_native_gun_barrel_plot'
    
    # Public Land Survey System Workflow Group Tasks
    LOAD_TEXAS_LAND_SURVEY_SYSTEM = 'load_texas_land_survey_system'