from enum import Enum
from poplib import CR
from sqlite3 import Connection, Cursor


class AFEDB:

    class SQL(Enum):

        ####### Stratigraphic Tables ########
        CREATE_STRATIGRAPHIC_TABLE = """
            CREATE TABLE IF NOT EXISTS stratigraphic
            (period TEXT,
             epoch TEXT,	
             basin TEXT,	
             formation TEXT,	
             union_code TEXT,	
             prism_code TEXT,
             position INTEGER,
             color TEXT,
             PRIMARY KEY (union_code)
            ); """

        DROP_STRATIGRAPHIC_TABLE = """DROP TABLE IF EXISTS stratigraphic"""
        
        SELECT_STRATIGRAPHIC_BY_UNION_CODE = """SELECT * FROM stratigraphic WHERE union_code = ? ORDER BY formation, period ASC"""

        SELECT_STRATIGRAPHIC_BY_PRISM_CODE = """SELECT * FROM stratigraphic WHERE prism_code = ? ORDER BY formation, period ASC"""

        CREATE_STRATIGRAPHIC_COMMON_TANKS_TABLE = """
            CREATE TABLE IF NOT EXISTS stratigraphic_common_tanks
            (union_code TEXT,
             common_tank TEXT,
             FOREIGN KEY(union_code) REFERENCES stratigraphic(union_code),
             FOREIGN KEY(common_tank) REFERENCES stratigraphic(union_code)
            ); """

        DROP_STRATIGRAPHIC_COMMON_TANKS_TABLE = """DROP TABLE IF EXISTS stratigraphic_common_tanks"""

        SELECT_STRATIGRAPHIC_COMMON_TANKS_BY_UNION_CODE = """SELECT * FROM stratigraphic_common_tanks WHERE union_code = ?"""

        ####### Target Well Information Table ########
        CREATE_TARGET_WELL_INFORMATION_TABLE = """
            CREATE TABLE IF NOT EXISTS target_well_information (
            id INTEGER, 
            name TEXT NOT NULL UNIQUE, 
            api TEXT, 
            afe_landing_zone TEXT,
            logs_landing_zone TEXT,
            enverus_status TEXT,
            afe_md_ft INTEGER,
            afe_bhl_tvd_ft INTEGER,
            surveys_preforated_interval_ft INTEGER,
            afe_gross_dollar REAL,
            well_cost REAL,
            seller_effective_gross_nri_percentage REAL,
            seller_net_nri_percentage REAL,
            seller_gross_for_sale_percentage REAL,
            afe_gwi_for_sale_net_capital_dollar REAL,
            enverus_rkb_elevation_ft INTEGER,
            bhl_tvd_ss_ft INTEGER,
            afe_in_landing_zone_hyp_spacing_ft INTEGER,
            state TEXT,
            county TEXT,
            tx_abstract_southwest_corner TEXT,
            tx_block_southwest_corner TEXT,
            nw_township_southwest_corner TEXT,
            nm_range_southwest_corner TEXT,
            nm_tx_section_southwest_corner TEXT,
            nad_system TEXT,
            nad_zone TEXT,
            x_surface_location REAL,
            y_surface_location REAL,
            x_first_take_point REAL,
            y_first_take_point REAL,
            x_last_take_point REAL,
            y_last_take_point REAL,
            x_bottom_hole REAL,
            y_bottom_hole REAL,
            latitude_surface_location TEXT,
            longitude_surface_location TEXT,
            latitude_first_take_point TEXT,
            longitude_first_take_point TEXT,
            latitude_last_take_point TEXT,
            longitude_last_take_point TEXT,
            latitude_bottom_hole TEXT,
            longitude_bottom_hole TEXT,
            legal_tx_abstract_surface_location TEXT,
            Legal_tx_block_surface_location TEXT,
            legal_nw_township_surface_location TEXT,
            legal_nw_range_surface_location TEXT,
            legal_nm_tx_section_surface_location TEXT,
            legal_fnl_surface_location TEXT,
            legal_fsl_surface_location TEXT,
            legal_fwl_surface_location TEXT,
            legal_fel_surface_location TEXT,
            legal_tx_abstract_first_take_point TEXT,
            Legal_tx_block_first_take_point TEXT,
            legal_nw_township_first_take_point TEXT,
            legal_nw_range_first_take_point TEXT,
            legal_nm_tx_section_first_take_point TEXT,
            legal_fnl_first_take_point TEXT,
            legal_fsl_first_take_point TEXT,
            legal_fwl_first_take_point TEXT,
            legal_fel_first_take_point TEXT,
            legal_tx_abstract_last_take_point TEXT,
            Legal_tx_block_last_take_point TEXT,
            legal_nw_township_last_take_point TEXT,
            legal_nw_range_last_take_point TEXT,
            legal_nm_tx_section_last_take_point TEXT,
            legal_fnl_last_take_point TEXT,
            legal_fsl_last_take_point TEXT,
            legal_fwl_last_take_point TEXT,
            legal_fel_last_take_point TEXT,
            legal_tx_abstract_bottom_hole TEXT,
            Legal_tx_block_bottom_hole TEXT,
            legal_nw_township_bottom_hole TEXT,
            legal_nw_range_bottom_hole TEXT,
            legal_nm_tx_section_bottom_hole TEXT,
            legal_fnl_bottom_hole TEXT,
            legal_fsl_bottom_hole TEXT,
            legal_fwl_bottom_hole TEXT,
            legal_fel_bottom_hole TEXT,
            perf_interval_ft INTEGER,
            PRIMARY KEY (id, name)
            ); """
        
        DROP_TARGET_WELL_INFORMATION_TABLE = """DROP TABLE IF EXISTS target_well_information"""

        UPDATE_TARGET_WELL_INFORMATION_LATITUDE_LONGITUDE_VALUES = """
            UPDATE target_well_information
            SET latitude_surface_location = ?,
                longitude_surface_location = ?,
                latitude_first_take_point = ?,
                longitude_first_take_point = ?,
                latitude_last_take_point = ?,
                longitude_last_take_point = ?,
                latitude_bottom_hole = ?,
                longitude_bottom_hole = ?
            WHERE name = ? """ 

        SELECT_TARGET_WELL_INFORMATION_FIRST_ROW = """SELECT * FROM target_well_information LIMIT 1"""

        SELECT_TARGET_WELL_INFORMATION = """SELECT * FROM target_well_information ORDER BY id ASC"""

        SELECT_TARGET_WELL_INFORMATION_BY_API = """SELECT * FROM target_well_information WHERE api = ?"""

        SELECT_TARGET_WELL_INFORMATION_BY_NAME = """SELECT * FROM target_well_information WHERE name = ?"""

        SELECT_TARGET_WELL_INFORMATION_DISTINCT_STATES = """SELECT DISTINCT state FROM target_well_information ORDER BY state DESC"""

        SELECT_TARGET_WELL_INFORMATION_TEXAS_DISTINCT_ABSTRACTS = """SELECT DISTINCT tx_abstract_southwest_corner FROM target_well_information WHERE state = "TX" ORDER BY tx_abstract_southwest_corner DESC"""
        
        SELECT_TARGET_WELL_INFORMATION_BY_TEXAS_ABSTRACT = """SELECT * FROM target_well_information WHERE tx_abstract_southwest_corner = ? ORDER BY name DESC"""
        
        SELECT_TARGEL_WELL_INFORMATION_SHALLOWEST = """SELECT MIN(ABS(bhl_tvd_ss_ft)) FROM target_well_information"""
        
        SELECT_TARGEL_WELL_INFORMATION_DEEPEST = """SELECT MAX(ABS(bhl_tvd_ss_ft)) FROM target_well_information"""

        SELECT_TARGEL_WELL_INFORMATION_MAX_LATERAL_LENGTH = """SELECT MAX(ABS(surveys_preforated_interval_ft)) FROM target_well_information"""

        ####### Gun Barrel Plot Table ########
        CREATE_GUN_BARREL_PLOT_TABLE = """
            CREATE TABLE IF NOT EXISTS gun_barrel_plot
            (
                target_well_api TEXT NOT NULL,
                offset_well_api TEXT NOT NULL,
                overlap_feet INTEGER,
                overlap_percentage INTEGER,
                cumulative_oil_per_ft INTEGER,
                overlap_cumulative_oil_ft INTEGER,
                months_from_first_production INTEGER,
                PRIMARY KEY (target_well_api, offset_well_api)
            ); """

        DROP_GUN_BARREL_PLOT_TABLE = """DROP TABLE IF EXISTS gun_barrel_plot"""

        INSERT_GUN_BARREL_PLOT = """
            INSERT INTO gun_barrel_plot (
                target_well_api,
                offset_well_api,
                overlap_feet,  
                overlap_percentage,
                cumulative_oil_per_ft,
                overlap_cumulative_oil_ft,
                months_from_first_production)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
        
        UPDATE_GUN_BARREL = """
            UPDATE gun_barrel_plot
            SET overlap_feet = ?,
                overlap_percentage = ?,
                cumulative_oil_per_ft = ?,
                overlap_cumulative_oil_ft = ?,
                months_from_first_production = ?
                WHERE target_well_api = ? AND offset_well_api = ?
                """
        SELECT_ALL_GUN_BARREL = """SELECT * FROM gun_barrel_plot ORDER BY target_well_api DESC"""
        
        SELECT_GUN_BARREL_PLOT_BY_TARGET_WELL_API = """SELECT * FROM gun_barrel_plot WHERE target_well_api = ?"""
        
        SELECT_GUN_BARREL_PLOT_BY_TARGET_OFFSET_WELL_API = """SELECT * FROM gun_barrel_plot WHERE target_well_api = ? AND offset_well_api = ?"""

        ####### GUN_BARREL_TRIANGLE_DISTANCES Table ########
        CREATE_GUN_BARREL_TRIANGLE_DISTANCES_TABLE = """
            CREATE TABLE IF NOT EXISTS gun_barrel_triangle_distances
            (
                target_well_api TEXT NOT NULL,
                offset_well_api TEXT NOT NULL,
                adjacent INTEGER,
                opposite INTEGER,
                hypotenuse INTEGER,
                PRIMARY KEY (target_well_api, offset_well_api)
            ); """
        
        DROP_GUN_BARREL_TRIANGLE_DISTANCES_TABLE = """DROP TABLE IF EXISTS gun_barrel_triangle_distances"""

        INSERT_GUN_BARREL_TRIANGLE_DISTANCES = """
            INSERT INTO gun_barrel_triangle_distances (
                target_well_api,
                offset_well_api,
                adjacent,
                opposite,
                hypotenuse)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(target_well_api, offset_well_api) DO NOTHING
            """

        SELECT_GUN_BARREL_TRIANGLE_DISTANCES = """SELECT * FROM gun_barrel_triangle_distances ORDER BY target_well_api DESC"""
        
        SELECT_GUN_BARREL_TRIANGLE_DISTANCES_By_TARGET_WELL_API = """SELECT * FROM gun_barrel_triangle_distances WHERE target_well_api = ?"""

        SELECT_GUN_BARREL_TRIANGLE_DISTANCES_By_TARGET_WELL_OFFSET_WELL_API = """SELECT * FROM gun_barrel_triangle_distances WHERE target_well_api = ? AND offset_well_api = ?"""
        
        ####### Well Table ########
        CREATE_WELL_TABLE = """
            CREATE TABLE IF NOT EXISTS well
            (
                api TEXT PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                direction TEXT,
                operator TEXT,
                status TEXT,
                lease TEXT,
                interval TEXT,
                formation TEXT,
                first_production_date TEXT,
                surface_latitude REAL,
                surface_longitude REAL,
                bottom_hole_latitude REAL,
                bottom_hole_longitude REAL,
                total_vertical_depth INTEGER,
                measured_depth INTEGER,
                kelly_bushing_elevation INTEGER,
                lateral_length INTEGER,
                perf_interval INTEGER,
                proppant_intensity INTEGER,
                state TEXT,
                county TEXT,
                abstract TEXT,
                township TEXT,
                "range" TEXT,
                section TEXT,
                cumlative_oil INTEGER
            ); """

        DROP_WELL_TABLE = """DROP TABLE IF EXISTS well"""

        INSERT_WELL = """
            INSERT INTO well (
            api,
            name,
            direction,
            operator,
            status,
            lease,
            interval,
            formation,
            first_production_date,
            surface_latitude,
            surface_longitude,
            bottom_hole_latitude,
            bottom_hole_longitude,
            total_vertical_depth,
            measured_depth,
            kelly_bushing_elevation,
            lateral_length,
            perf_interval,
            proppant_intensity,
            state,
            county,
            abstract,
            township,
            "range",
            section,
            cumlative_oil)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
            """

        SELECT_WELLS = """SELECT * FROM well ORDER BY name DESC"""

        SELECT_WELL_BY_API = """SELECT * FROM well WHERE api = ?"""

        SELECT_WELL_BY_NAME = """SELECT * FROM well WHERE name = ?"""

        SELECT_WELL_STATES = """SELECT DISTINCT state FROM well ORDER BY state DESC"""

        SELECT_WELL_TEXAS_ABSTRACTS = """SELECT DISTINCT abstract FROM well WHERE state = "TX" ORDER BY abstract DESC"""
        
        SELECT_WELLS_BY_TEXAS_ABSTRACT = """SELECT * FROM well WHERE abstract = ? ORDER BY name DESC"""
        
        ####### Survey Table ########

        CREATE_SURVEY_TABLE = """
            CREATE TABLE IF NOT EXISTS survey
            (
                api TEXT NOT NULL,
                station INTEGER NOT NULL,
                md INTEGER,
                inclination REAL,
                azimuth REAL,
                latitude REAL,
                longitude REAL,
                grid_x REAL,
                grid_y REAL,
                subsurface_depth INTEGER,
                PRIMARY KEY (api, station)
            ); """

        DROP_SURVEY_TABLE = """DROP TABLE IF EXISTS survey"""
        
        INSERT_SURVEY = """
            INSERT INTO survey (api, station, md, inclination, azimuth, latitude, longitude, grid_x, grid_y, subsurface_depth) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
        GET_SURVEYS_BY_API = (
            """SELECT * FROM survey WHERE api = ? ORDER BY station ASC"""
        )

        GET_SURVEY_UNIQUE_API_VALUES = """SELECT DISTINCT api FROM survey ORDER BY api DESC"""

        ####### Production Table ########

        ####### Analysis Table ########
        CREATE_ANALYSIS_TABLE = """
            CREATE TABLE IF NOT EXISTS analysis
            (
                api TEXT PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                direction TEXT,
                dominant_direction TEXT,
                interval TEXT,
                lateral_length INTEGER,
                lateral_start_latitude REAL,
                lateral_start_longitude REAL,
                lateral_midpoint_latitude REAL,
                lateral_midpoint_longitude REAL,
                lateral_end_latitude REAL,
                lateral_end_longitude REAL,
                lateral_start_grid_x REAL,
                lateral_start_grid_y REAL,
                lateral_start_subsurface_depth INTEGER,
                lateral_midpoint_grid_x REAL,
                lateral_midpoint_grid_y REAL,
                lateral_midpoint_subsurface_depth INTEGER,
                lateral_end_grid_x REAL,
                lateral_end_grid_y REAL,
                lateral_end_subsurface_depth INTEGER,
                subsurface_depth INTEGER,
                first_production_date TEXT,
                adjacent_1 TEXT,
                adjacent_2 TEXT,
                distance_1 INTEGER,
                distance_2 INTEGER,
                hypotenuse_1 INTEGER,
                hypotenuse_2 INTEGER,
                group_id TEXT,
                codevelopment TEXT,
                average_horizontal_spacing INTEGER,
                group_average_horizontal_spacing INTEGER,
                group_average_hypotenuse_spacing INTEGER,
                parents TEXT,
                parent_1 TEXT,
                parent_1_first_production_date TEXT,
                parent_1_delta_first_production_months TEXT,
                parent_1_interval TEXT,
                parent_2 TEXT,
                parent_2_first_production_date TEXT,
                parent_2_delta_first_production_months TEXT,
                parent_2_interval TEXT,
                child TEXT,
                adjacent_child TEXT,
                sibling TEXT,
                bound TEXT,
                gun_barrel_x INTEGER,
                gun_barrel_y INTEGER,
                gun_barrel_z INTEGER,
                target_well_spacing_gun_barrel_plot_flag TEXT,
                gun_barrel_index INTEGER
            ); """

        DROP_ANALYSIS_TABLE = """DROP TABLE IF EXISTS analysis"""

        INSERT_ANALYSIS = """
            INSERT INTO analysis (
            api, 
            name, 
            direction, 
            dominant_direction,
            interval,
            lateral_length, 
            lateral_start_latitude, 
            lateral_start_longitude, 
            lateral_midpoint_latitude, 
            lateral_midpoint_longitude, 
            lateral_end_latitude, 
            lateral_end_longitude, 
            lateral_start_grid_x,
            lateral_start_grid_y,
            lateral_start_subsurface_depth,
            lateral_midpoint_grid_x,
            lateral_midpoint_grid_y,
            lateral_midpoint_subsurface_depth,
            lateral_end_grid_x,
            lateral_end_grid_y,
            lateral_end_subsurface_depth,
            subsurface_depth,
            first_production_date,
            adjacent_1,
            adjacent_2,
            distance_1,
            distance_2,
            hypotenuse_1,
            hypotenuse_2,
            group_id,
            codevelopment,
            average_horizontal_spacing,
            group_average_horizontal_spacing,
            group_average_hypotenuse_spacing,
            parents,
            parent_1,
            parent_1_first_production_date,
            parent_1_delta_first_production_months,
            parent_1_interval,
            parent_2,
            parent_2_first_production_date,
            parent_2_delta_first_production_months,
            parent_2_interval,
            child,
            adjacent_child,
            sibling,
            bound,
            gun_barrel_x,
            gun_barrel_y,
            gun_barrel_z,
            target_well_spacing_gun_barrel_plot_flag,
            gun_barrel_index)
            VALUES (?, ?, ?, ?, ?, 
                    ?, ?, ?, ?, ?, 
                    ?, ?, ?, ?, ?, 
                    ?, ?, ?, ?, ?, 
                    ?, ?, ?, ?, ?, 
                    ?, ?, ?, ?, ?, 
                    ?, ?, ?, ?, ?, 
                    ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?,
                    ?, ?)
            """
        UPDATE_ANALYSIS = """
            UPDATE analysis
            SET name = ?, 
            direction = ?, 
            dominant_direction = ?,
            interval = ?,
            lateral_length = ?, 
            lateral_start_latitude = ?, 
            lateral_start_longitude = ?, 
            lateral_midpoint_latitude = ?, 
            lateral_midpoint_longitude = ?, 
            lateral_end_latitude = ?, 
            lateral_end_longitude = ?, 
            lateral_start_grid_x = ?,
            lateral_start_grid_y = ?,
            lateral_start_subsurface_depth = ?,
            lateral_midpoint_grid_x = ?,
            lateral_midpoint_grid_y = ?,
            lateral_midpoint_subsurface_depth = ?,
            lateral_end_grid_x = ?,
            lateral_end_grid_y = ?,
            lateral_end_subsurface_depth = ?,
            subsurface_depth = ?,
            first_production_date = ?,
            adjacent_1 = ?,
            adjacent_2 = ?,
            distance_1 = ?,
            distance_2 = ?,
            hypotenuse_1 = ?,
            hypotenuse_2 = ?,
            group_id = ?,
            codevelopment = ?,
            average_horizontal_spacing = ?,
            group_average_horizontal_spacing = ?,
            group_average_hypotenuse_spacing = ?,
            parents = ?,
            parent_1 = ?,
            parent_1_first_production_date = ?,
            parent_1_delta_first_production_months = ?,
            parent_1_interval = ?,
            parent_2 = ?,
            parent_2_first_production_date = ?,
            parent_2_delta_first_production_months = ?,
            parent_2_interval = ?,
            child = ?,
            adjacent_child = ?,
            sibling = ?,
            bound = ?,
            gun_barrel_x = ?,
            gun_barrel_y = ?,
            gun_barrel_z = ?,
            target_well_spacing_gun_barrel_plot_flag = ?,
            gun_barrel_index = ?
            WHERE api = ?
        """
        UPDATE_ANALYSIS_SET_TARGET_WELL_SPACING_GUN_BARREL_PLOT_FLAG_NULL = """ UPDATE analysis SET target_well_spacing_gun_barrel_plot_flag = NULL"""

        SELECT_ALL_ANALYSIS = """SELECT * FROM analysis ORDER BY name ASC"""

        SELECT_ANALYSIS_BY_API = """SELECT * FROM analysis WHERE api = ?"""

        SELECT_ANALYSIS_BY_NAME = """SELECT * FROM analysis WHERE name = ?"""

        SELECT_ANALYSIS_WHERE_TARGET_WELL_SPACING_GUN_BARREL_PLOT_FLAG_IS_TRUE = """SELECT * FROM analysis WHERE target_well_spacing_gun_barrel_plot_flag = "1" ORDER BY name ASC"""

        SELECT_ANALYSIS_WHERE_TARGET_WELL_SPACING_GUN_BARREL_PLOT_FLAG_IS_TRUE_ZOOMED = """SELECT * FROM analysis WHERE target_well_spacing_gun_barrel_plot_flag = "1" AND ABS(gun_barrel_x) <= 2640 ORDER BY name ASC"""

        SELECT_ANALYSIS_EXCLUDING_TARGET_WELLS = """SELECT * FROM analysis WHERE name NOT IN (SELECT name FROM target_well_information) AND name NOT LIKE 'Simulated-Well%' ORDER BY name ASC"""

        SELECT_ANALYSIS_BY_SIMULATED_WELL = """SELECT * FROM analysis WHERE name LIKE 'Simulated-Well%'"""
        
        SELECT_ANALYSIS_BY_SIMULATED_TARGET_WELLS = """SELECT * FROM analysis WHERE api LIKE '11-111-%'"""

        SELECT_ANALYSIS_SHALLOWEST = """SELECT MIN(ABS(subsurface_depth)) FROM analysis"""
        
        SELECT_ANALYSIS_DEEPEST = """SELECT MAX(ABS(subsurface_depth)) FROM analysis"""


        ####### Adjacent Table ########
        CREATE_ADJACENT_TABLE = """
            CREATE TABLE IF NOT EXISTS adjacent
            (
                reference_api TEXT NOT NULL,
                reference_name TEXT NOT NULL,
                target_api TEXT NOT NULL,
                target_name TEXT NOT NULL,
                north INTEGER,
                south INTEGER,
                east INTEGER,
                west INTEGER,
                hypotenuse INTEGER,
                PRIMARY KEY (reference_api, target_api)    
            ); """

        DROP_ADJACENT_TABLE = """DROP TABLE IF EXISTS adjacent"""

        INSERT_ADJACENT = """
            INSERT INTO adjacent (
            reference_api,
            reference_name,
            target_api,
            target_name,
            north,
            south,
            east,
            west,
            hypotenuse) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
        
        SELECT_ALL_ADJACENTS = """SELECT * FROM adjacent ORDER BY reference_name ASC"""
       
        SELECT_DISTINCT_ADJACENT_REFERENCE_APIS = """SELECT DISTINCT reference_api FROM adjacent ORDER BY reference_name ASC"""   
        
        SELECT_ADJACENT_BY_REFERENCE_API_WEST = """SELECT * FROM adjacent WHERE reference_api = ? AND west IS NOT NULL ORDER BY west ASC"""

        SELECT_ADJACENT_BY_REFERENCE_API_EAST = """SELECT * FROM adjacent WHERE reference_api = ? AND east IS NOT NULL ORDER BY east ASC"""

        SELECT_ADJACENT_BY_REFERENCE_API_NORTH = """SELECT * FROM adjacent WHERE reference_api = ? AND north IS NOT NULL ORDER BY north ASC"""

        SELECT_ADJACENT_BY_REFERENCE_API_SOUTH = """SELECT * FROM adjacent WHERE reference_api = ? AND south IS NOT NULL ORDER BY south ASC"""

        SELECT_ADJACENT_BY_REFERENCE_TARGET_APIS = """SELECT * FROM adjacent WHERE reference_api = ? AND target_api = ?"""

        SELECT_ADJACENT_BY_REFERENCE_APIS = """SELECT * FROM adjacent WHERE reference_api IN ({}) ORDER BY reference_name ASC, target_name ASC"""

        DELETE_ADJACENT = """DELETE FROM adjacent WHERE reference_api = ? AND target_api = ?"""   

        ####### Codevevlopment Table ########
        CREATE_CODEV_TABLE = """
            CREATE TABLE IF NOT EXISTS codevelopment
            (
                reference_api TEXT NOT NULL,
                target_api TEXT NOT NULL,
                reference_name TEXT NOT NULL,
                target_name TEXT NOT NULL,
                PRIMARY KEY (reference_name, target_name)    
            ); """

        DROP_CODEV_TABLE = """DROP TABLE IF EXISTS codevelopment"""

        INSERT_CODEV = """
            INSERT INTO codevelopment (
            reference_api,
            target_api,
            reference_name,
            target_name)
            VALUES (?, ?, ?, ?)
            """
        SELECT_ALL_CODEVELOPMENTS = """SELECT * FROM codevelopment ORDER BY reference_name DESC"""

        SELECT_CODEVELOPMENTS_BY_REFERENCE_API = """SELECT * FROM codevelopment WHERE reference_api = ?"""

        ####### Parent Child table ########
        CREATE_PARENT_CHILD_TABLE = """
            CREATE TABLE IF NOT EXISTS parentchild (
                parent_api TEXT NOT NULL,
                parent_name TEXT,
                child_api TEXT NOT NULL,
                child_name TEXT,
                sibling_api TEXT,
                sibling_name TEXT,
                adjacent TEXT,
                parent_interval TEXT,
                child_interval TEXT,
                sibling_interval TEXT,
                PRIMARY KEY (parent_api, child_api)
            ); """
                
        DROP_PARENT_CHILD_TABLE = """DROP TABLE IF EXISTS parentchild"""

        INSERT_PARENT_CHILD = """
            INSERT INTO parentchild (
                parent_api,
                parent_name,
                child_api,
                child_name,
                sibling_api,
                sibling_name,
                adjacent,
                parent_interval,
                child_interval,
                sibling_interval)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)    
            """
        SELECT_PARENTCHILD_BY_PARENT_API = """SELECT * FROM parentchild WHERE parent_api = ?"""

        SELECT_PARENTCHILD_BY_CHILD_API = """SELECT * FROM parentchild WHERE child_api = ?"""

        SELECT_PARENTCHILD_CHILD_API_ADJACENT = """SELECT * FROM parentchild WHERE child_api = ? AND adjacent = ?"""

        ####### Group Table ########
        CREATE_WELL_GROUP_TABLE = """
            CREATE TABLE IF NOT EXISTS wellgroup
            (
                name TEXT PRIMARY KEY,
                color TEXT NOT NULL   
            ); """
        
        DROP_WELL_GROUP_TABLE = """DROP TABLE IF EXISTS wellgroup"""

        INSERT_WELL_GROUP = """
            INSERT INTO wellgroup (
                name,
                color)
            VALUES (?, ?)    
            """
        SELECT_ALL_WELL_GROUPS = """SELECT * FROM wellgroup ORDER BY name ASC"""

        SELECT_WELL_GROUP_BY_NAME = """SELECT * FROM wellgroup WHERE name = ?"""

        ####### Well Group Member Table ########
        CREATE_WELL_GROUP_MEMBER_TABLE = """
            CREATE TABLE IF NOT EXISTS wellgroupmember
            (
                group_name TEXT NOT NULL,
                well_api TEXT NOT NULL,
                well_name TEXT NOT NULL,
                PRIMARY KEY (group_name, well_api)
            ); """
        
        DROP_WELL_GROUP_MEMBER_TABLE = """DROP TABLE IF EXISTS wellgroupmember"""
        
        INSERT_WELL_GROUP_MEMBER = """
            INSERT INTO wellgroupmember (
                group_name,
                well_api,
                well_name)
            VALUES (?, ?, ?)
            """
        SELECT_WELL_GROUP_MEMBERS = """SELECT * FROM wellgroupmember ORDER BY group_name ASC, well_name ASC"""

        SELECT_WELL_GROUP_MEMBERS_BY_GROUP_NAME = """SELECT * FROM wellgroupmember WHERE group_name = ? ORDER BY well_name ASC"""

        SELECT_WELL_GROUP_MEMBER_BY_GROUP_NAME_WELL_API = """SELECT * FROM wellgroupmember WHERE group_name = ? AND well_api = ? ORDER BY group_name ASC"""

        ####### XYZDistance Table ########
        CREATE_XYZ_DISTANCE_TABLE = """
            CREATE TABLE IF NOT EXISTS xyzdistance
            (
                reference_api TEXT NOT NULL,
                reference_name TEXT NOT NULL,
                target_api TEXT NOT NULL,
                target_name TEXT NOT NULL,
                start_x INTEGER,
                start_y INTEGER,
                start_z INTEGER,
                start_hypotenuse INTEGER,
                mid_x INTEGER,
                mid_y INTEGER,
                mid_z INTEGER,
                mid_hypotenuse INTEGER,
                end_x INTEGER,
                end_y INTEGER,
                end_z INTEGER,
                end_hypotenuse INTEGER,
                PRIMARY KEY (reference_api, target_api)    
            ); """
        
        # XYZDistance Table
        DROP_XYZ_DISTANCE_TABLE = """DROP TABLE IF EXISTS xyzdistance"""

        INSERT_XYZ_DISTANCE = """
            INSERT INTO xyzdistance (
                reference_api,
                reference_name,
                target_api,
                target_name,
                start_x,
                start_y,
                start_z,
                start_hypotenuse,
                mid_x,
                mid_y,
                mid_z,
                mid_hypotenuse,
                end_x,
                end_y,
                end_z,
                end_hypotenuse)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
        SELECT_XYZ_DISTANCES = """SELECT * FROM xyzdistance ORDER BY reference_name ASC"""

        SELECT_XYZDISTANCES_BY_REFERENCE_API = """SELECT * FROM xyzdistance WHERE reference_api = ?"""

        SELECT_XYZ_DISTANCE_BY_REFERENCE_API_TARGET_API = """SELECT * FROM xyzdistance WHERE reference_api = ? AND target_api = ? ORDER BY target_name DESC"""
        
        SELECT_XYZ_DISTANCE_BY_SIMULATED_WELL = """SELECT * FROM xyzdistance WHERE reference_api = ? ORDER BY target_name ASC"""

        SELECT_XYZ_DISTANCE_BY_REFERENCE_WELL = """SELECT * 
                                                FROM xyzdistance 
                                                WHERE reference_api = ? 
                                                AND target_api NOT LIKE "11-111-%"
                                                AND target_api NOT LIKE "00-000-%"
                                                ORDER BY end_hypotenuse ASC, target_api DESC"""
        
        SELECT_XYZ_DISTANCE_BY_TARGET_WELL = """SELECT * 
                                                FROM xyzdistance 
                                                WHERE reference_api = ? 
                                                AND target_api NOT LIKE "11-111-%"
                                                AND target_api NOT LIKE "00-000-%"
                                                AND end_hypotenuse <= 2000
                                                ORDER BY end_hypotenuse ASC, target_api DESC"""
        
        SELECT_XYZ_DISTANCE_FOR_SIMULATED_TARGET_WELL = """SELECT * 
                                                           FROM xyzdistance 
                                                           WHERE reference_api = '00-000-00000'
                                                           """
        
        SELECT_XYZ_DISTANCE_BY_REF_TARGET_WELLS = """SELECT * 
                                                FROM xyzdistance 
                                                WHERE reference_api = ? 
                                                AND target_api = ?"""
        
        # Latitude Longitude Distance Table
        CREATE_LATITUDE_LONGITUDE_DISTANCE_TABLE = """
            CREATE TABLE IF NOT EXISTS latitudelongitudedistance
            (
                reference_api TEXT NOT NULL,
                reference_name TEXT NOT NULL,
                target_api TEXT NOT NULL,
                target_name TEXT NOT NULL,
                start_latitude INTEGER,
                start_longitude INTEGER,
                start_z INTEGER,
                start_hypotenuse INTEGER,
                mid_latitude INTEGER,
                mid_longitude INTEGER,
                mid_z INTEGER,
                mid_hypotenuse INTEGER,
                end_latitude INTEGER,
                end_longitude INTEGER,
                end_z INTEGER,
                end_hypotenuse INTEGER,
                PRIMARY KEY (reference_api, target_api)  
            ); """

        DROP_LATITUDE_LONGITUDE_DISTANCE_TABLE = """DROP TABLE IF EXISTS latitudelongitudedistance"""
       
        INSERT_LATITUDE_LONGITUDE_DISTANCE = """
            INSERT INTO latitudelongitudedistance (
                reference_api,
                reference_name,
                target_api,
                target_name,
                start_latitude,
                start_longitude,
                start_z,
                start_hypotenuse,
                mid_latitude,
                mid_longitude,
                mid_z,
                mid_hypotenuse,
                end_latitude,
                end_longitude,
                end_z,
                end_hypotenuse)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(reference_api, target_api) DO NOTHING
            """
        
        SELECT_LATITUDE_LONGITUDE_DISTANCES = """SELECT * FROM latitudelongitudedistance ORDER BY reference_name ASC"""

        SELECT_LATITUDE_LONGITUDE_DISTANCES_BY_REFERENCE_API = """SELECT * FROM latitudelongitudedistance WHERE reference_api = ?"""

        SELECT_LATITUDE_LONGITUDE_DISTANCE_BY_REFERENCE_TARGET_APIS = """SELECT * FROM latitudelongitudedistance WHERE reference_api = ? AND target_api = ?"""
        
        ####### Well Overlap Table ########
        CREATE_OVERLAP_TABLE = """
            CREATE TABLE IF NOT EXISTS overlap
            (
                reference_api TEXT NOT NULL,
                reference_name TEXT NOT NULL,
                target_api TEXT NOT NULL,
                target_name TEXT NOT NULL,
                overlap_feet INTEGER,
                overlap_percentage REAL,
                PRIMARY KEY (reference_api, target_api)    
            ); """

        DROP_OVERLAP_TABLE = """DROP TABLE IF EXISTS overlap"""

        INSERT_OVERLAP = """
            INSERT INTO overlap (
            reference_api,
            reference_name,
            target_api,
            target_name,
            overlap_feet,
            overlap_percentage) 
            VALUES (?, ?, ?, ?, ?, ?)
            """
        
        SELECT_OVERLAP_BY_REFERENCE_API_TARGET_API = """SELECT * FROM overlap WHERE reference_api = ? AND target_api = ?"""

        ####### Texas Land Survey System Table ########
        CREATE_TEXAS_LAND_SURVEY_SYSTEM_TABLE = """
            CREATE TABLE IF NOT EXISTS texas_land_survey_system
            (
                county TEXT,
                fips_code TEXT,
                abstract TEXT,
                block TEXT,
                section TEXT,
                grantee TEXT,
                southwest_latitude REAL,
                southwest_longitude REAL,
                northwest_latitude REAL,
                northwest_longitude REAL,
                southeast_latitude REAL,
                southeast_longitude REAL,
                northeast_latitude REAL,
                northeast_longitude REAL,
                PRIMARY KEY (county, fips_code, abstract, block, section)
            ); """
        
        DROP_TEXAS_LAND_SURVEY_SYSTEM_TABLE = """DROP TABLE IF EXISTS texas_land_survey_system"""
        
        INSERT_TEXAS_LAND_SURVEY_SYSTEM = """
            INSERT INTO texas_land_survey_system (
                county,
                fips_code,
                abstract,
                block,
                section,
                grantee,
                southwest_latitude,
                southwest_longitude,
                northwest_latitude,
                northwest_longitude,
                southeast_latitude,
                southeast_longitude,
                northeast_latitude,
                northeast_longitude)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
        
        SELECT_TEXAS_LAND_SURVEY_SYSTEM_BY_COUNTY_ABSTRACT_BLOCK_SECTION = """
            SELECT * FROM texas_land_survey_system WHERE county = ? AND abstract = ? AND block = ? AND section = ?
        """

        SELECT_TEXAS_LAND_SURVEY_SYSTEM_BY_COUNTY_ABSTRACT = """
            SELECT * FROM texas_land_survey_system WHERE county = ? AND abstract = ?
        """

        ####### New Mexico Land Survey System Table ########
        SELECT_NEW_MEXICO_LAND_SURVEY_SYSTEM_BY_TOWNSHIP_RANGE_SECTION = """
            SELECT * FROM new_mexico_land_survey_system WHERE township = ? AND township_direction = ? AND range = ? AND range_direction = ? AND section = ?
        """
        
    def __init__(self, db_path=None):
        self.connection = Connection(db_path)

    def __del__(self):
        # Close the database connection when the object is about to be destroyed
        self.connection.close()

    def execute_ddl(self, sql):
        try:
            cursor = Cursor(self.connection)
            cursor.execute(sql)

        except Exception as e:
            raise Exception(f"Error occurred {sql}: {e}")
        finally:
            cursor.close()
