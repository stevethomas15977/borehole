import os
from dotenv import load_dotenv

class Context():
    def __init__(self):
        if load_dotenv() == False:
            raise ValueError("Failed to load .env file.")
        self._version = os.getenv("VERSION")
        self._projects_path = os.path.join(os.getenv("PROJECTS_PATH"))
        self._username = os.getenv("USERNAME")
        self._password = os.getenv("PASSWORD")

        self._project = None
        self._project_path = None
        self._db_path = None

        self._target_well_information_path = None
        self._well_data_path = None
        self._survey_data_path = None

        self._target_well_information_file = None
        self._well_file = None
        self._survey_file = None

        self._logs_path = None

        self._geojson_path = os.path.join(os.getenv("GEOJSON_PATH"))

        self._target_well_information_strategy = "XY"
        
        self._codevelopment_first_production_date_days_threshold: int = os.getenv("CODEVELOPMENT_FIRST_PRODUCTION_DATE_DAYS_THRESHOLD")
        self._horizontal_distance_threshold: int = os.getenv("HORIZONTAL_DISTANCE_THRESHOLD")
        self._vertical_distance_threshold: int = os.getenv("VERTICAL_DISTANCE_THRESHOLD")
        self._lateral_length_threshold: int = os.getenv("LATERAL_LENGTH_THRESHOLD")
        self._max_distance_threshold: int = os.getenv("MAX_DISTANCE_THRESHOLD")
        self._hypotenuse_distance_threshold: int = os.getenv("HYPOTENUSE_DISTANCE_THRESHOLD")
        self._depth_distance_threshold: int = int(os.getenv("DEPTH_DISTANCE_THRESHOLD"))
        self._pct_group_cum_oil_greater_than_threshold: float = float(os.getenv("PCT_GROUP_CUM_OIL_GREATER_THAN_THRESHOLD"))

        self._tx_abstract_column = os.getenv("TX_ABSTRACT_COLUMN")
        self._nm_section_column = os.getenv("NM_SECTION_COLUMN")
        self._texas_land_survey_system_database = os.getenv("TEXAS_LAND_SURVEY_SYSTEM_DATABASE")
        self._texas_land_survey_system_database_path = os.path.join(self._geojson_path, self._texas_land_survey_system_database)

        self._new_mexico_land_survey_system_database = os.getenv("NEW_MEXICO_LAND_SURVEY_SYSTEM_DATABASE")  
        self._new_mexico_land_survey_system_database_path = os.path.join(self._geojson_path, self._new_mexico_land_survey_system_database)  
        
        self._stratigraphic_file_path = os.path.join("database", "stratigraphic.xlsx")
        self._stratigraphic_common_tanks_file_path = os.path.join("database", "stratigraphic-common-tanks.xlsx")

    @property
    def version(self):
        return self._version
    
    @version.setter
    def version(self, version):
        if version == None:
            raise ValueError("VERSION environment variable not set.")
        self._version = version

    @property
    def project(self):
        return self._project
    
    @project.setter
    def project(self, project):
        self._project = project

    @property
    def projects_path(self):
        return self._projects_path
    
    @projects_path.setter
    def projects_path(self, projects_path):
        if projects_path == None:
            raise ValueError("WEB_ROOT environment variable not set.")
        self._projects_path = projects_path

    @property
    def project_path(self):
        return self._project_path
    
    @project_path.setter
    def project_path(self, project_path):
        self._project_path = project_path

    @property
    def db_path(self):
        return self._db_path
    
    @db_path.setter
    def db_path(self, db_path):
        self._db_path = db_path

    @property
    def target_well_information_path(self):
        return self._target_well_information_path
    
    @target_well_information_path.setter
    def target_well_information_path(self, target_well_information_path):
        self._target_well_information_path = target_well_information_path

    @property
    def well_data_path(self):
        return self._well_data_path
    
    @well_data_path.setter
    def well_data_path(self, well_data_path):
        self._well_data_path = well_data_path

    @property
    def survey_data_path(self):
        return self._survey_data_path
    
    @survey_data_path.setter
    def survey_data_path(self, survey_data_path):
        self._survey_data_path = survey_data_path

    @property
    def target_well_information_file(self):
        return self._target_well_information_file
    
    @target_well_information_file.setter
    def target_well_information_file(self, target_well_information_file):
        self._target_well_information_file = target_well_information_file
        
    @property
    def well_file(self):
        return self._well_file
    
    @well_file.setter
    def well_file(self, well_file):
        self._well_file = well_file

    @property
    def survey_file(self):
        return self._survey_file
    
    @survey_file.setter
    def survey_file(self, survey_file):
        self._survey_file = survey_file

    @property
    def logs_path(self):
        return self._logs_path
    
    @logs_path.setter
    def logs_path(self, logs_path):
        self._logs_path = logs_path

    @property
    def geojson_path(self):
        return self._geojson_path
    
    @geojson_path.setter
    def geojson_path(self, geojson_path):
        self._geojson_path = geojson_path

    @property
    def target_well_information_strategy(self):
        return self._target_well_information_strategy
    
    @target_well_information_strategy.setter
    def target_well_information_strategy(self, target_well_information_strategy):
        self._target_well_information_strategy = target_well_information_strategy
        
    @property
    def horizontal_distance_threshold(self):
        return self._horizontal_distance_threshold
    
    @horizontal_distance_threshold.setter
    def horizontal_distance_threshold(self, horizontal_distance_threshold):
        if horizontal_distance_threshold == None:
            raise ValueError("HORIZONTAL_DISTANCE_THRESHOLD environment variable not set.")
        self._horizontal_distance_threshold = horizontal_distance_threshold

    @property
    def codevelopment_first_production_date_days_threshold(self):
        return self._codevelopment_first_production_date_days_threshold
    
    @codevelopment_first_production_date_days_threshold.setter
    def codevelopment_first_production_date_days_threshold(self, codevelopment_first_production_date_days_threshold):
        if codevelopment_first_production_date_days_threshold == None:
            raise ValueError("CODEVELOPMENT_FIRST_PRODUCTION_DATE_DAYS_THRESHOLD environment variable not set.")
        self._codevelopment_first_production_date_days_threshold = codevelopment_first_production_date_days_threshold

    @property
    def vertical_distance_threshold(self):
        return self._vertical_distance_threshold
    
    @vertical_distance_threshold.setter
    def vertical_distance_threshold(self, vertical_distance_threshold):
        if vertical_distance_threshold == None:
            raise ValueError("VERTICAL_DISTANCE_THRESHOLD environment variable not set.")
        self._vertical_distance_threshold = vertical_distance_threshold

    @property
    def lateral_length_threshold(self):
        return self._lateral_length_threshold
    
    @lateral_length_threshold.setter
    def lateral_length_threshold(self, lateral_length_threshold):
        if lateral_length_threshold == None:
            raise ValueError("LATERAL_LENGTH_THRESHOLD environment variable not set.")
        self._lateral_length_threshold = lateral_length_threshold

    @property
    def max_distance_threshold(self):
        return self._max_distance_threshold
    
    @max_distance_threshold.setter  
    def max_distance_threshold(self, max_distance_threshold):
        if max_distance_threshold == None:
            raise ValueError("MAX_DISTANCE_THRESHOLD environment variable not set.")
        self._max_distance_threshold = max_distance_threshold

    @property
    def hypotenuse_distance_threshold(self):
        return int(self._hypotenuse_distance_threshold)
    
    @hypotenuse_distance_threshold.setter
    def hypotenuse_distance_threshold(self, hypotenuse_distance_threshold):
        if hypotenuse_distance_threshold == None:
            raise ValueError("HYPOTENUSE_DISTANCE_THRESHOLD environment variable not set.")
        self._hypotenuse_distance_threshold = hypotenuse_distance_threshold

    @property
    def depth_distance_threshold(self):
        return self._depth_distance_threshold
    
    @depth_distance_threshold.setter
    def depth_distance_threshold(self, depth_distance_threshold):
        if depth_distance_threshold == None:
            raise ValueError("DEPTH_DISTANCE_THRESHOLD environment variable not set.")
        self._depth_distance_threshold = depth_distance_threshold
        
    @property
    def pct_group_cum_oil_greater_than_threshold(self):
        return self._pct_group_cum_oil_greater_than_threshold
    
    @pct_group_cum_oil_greater_than_threshold.setter
    def pct_group_cum_oil_greater_than_threshold(self, pct_group_cum_oil_greater_than_threshold):
        if pct_group_cum_oil_greater_than_threshold == None:
            raise ValueError("PCT_GROUP_CUM_OIL_GREATER_THAN_THRESHOLD environment variable not set.")
        self._pct_group_cum_oil_greater_than_threshold = pct_group_cum_oil_greater_than_threshold
        
    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, username):
        if username == None:
            raise ValueError("USERNAME environment variable not set.")
        self._username = username

    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, password):
        if password == None:
            raise ValueError("PASSWORD environment variable not set.")
        self._password = password

    @property
    def tx_abstract_column(self):
        return self._tx_abstract_column
    
    @tx_abstract_column.setter
    def tx_abstract_column(self, tx_abstract_column):
        if tx_abstract_column == None:
            raise ValueError("TX_ABSTRACT_COLUMN environment variable not set.")
        self._tx_abstract_column = tx_abstract_column

    @property
    def nm_section_column(self):
        return self._nm_section_column
    
    @nm_section_column.setter
    def nm_section_column(self, nm_section_column):
        if nm_section_column == None:
            raise ValueError("NM_SECTION_COLUMN environment variable not set.")
        self._nm_section_column = nm_section_column

    @property
    def texas_land_survey_system_database(self):
        return self._texas_land_survey_system_database
    
    @texas_land_survey_system_database.setter
    def texas_land_survey_system_database(self, texas_land_survey_system_database):
        if texas_land_survey_system_database == None:
            raise ValueError("TEXAS_LAND_SURVEY_SYSTEM_DATABASE environment variable not set.")
        self._texas_land_survey_system_database = texas_land_survey_system_database

    @property
    def stratigraphic_file_path(self):
        return self._stratigraphic_file_path
    
    @property
    def stratigraphic_common_tanks_file_path(self):
        return self._stratigraphic_common_tanks_file_path
    
    @staticmethod
    def moosehorn_3_mile():
        context = Context()
        context.project = "Test"
        context.project_path = os.path.join(context.projects_path, context.project)
        
        context.target_well_information_path = os.path.join(context.project_path, 'target_well_information')
        context.well_data_path = os.path.join(context.project_path, 'well_data')
        context.survey_data_path = os.path.join(context.project_path, 'survey_data')
        context.logs_path = os.path.join(context.project_path, 'logs')

        context.db_path = os.path.join(context.logs_path, f"{context.project}-{context.version}.db")

        context.target_well_information_file = os.path.join(context.target_well_information_path, "moosehorn-3-mile-target-well-information.xlsx")
        context.well_file = os.path.join(context.well_data_path, "moosehorn-3-mile-well-data.xlsx")
        context.survey_file = os.path.join(context.survey_data_path, "moosehorn-3-mile-survey-data.xlsx")
        return context
    
    @staticmethod
    def atomic_5_mile():
        context = Context()
        context.project = "atomic-5-mile"
        context.project_path = os.path.join(context.projects_path, context.project)
        
        context.target_well_information_path = os.path.join(context.project_path, 'target_well_information')
        context.well_data_path = os.path.join(context.project_path, 'well_data')
        context.survey_data_path = os.path.join(context.project_path, 'survey_data')
        context.logs_path = os.path.join(context.project_path, 'logs')

        context.db_path = os.path.join(context.logs_path, f"{context.project}-{context.version}.db")

        context.target_well_information_file = os.path.join(context.target_well_information_path, "atomic-5-mile-target-well-information.xlsx")
        context.well_file = os.path.join(context.well_data_path, "Atomic_5-mile_WCXY_AU_Al_BU_well_data.xlsx")
        context.survey_file = os.path.join(context.survey_data_path, "Atomic_5-mile_WCXY_AU_AL_BU_Directional_Surveys.xlsx")
        return context
    
    @staticmethod
    def dragonfly_5_mile():
        context = Context()
        context.project = "dragonfly-5-mile"
        context.project_path = os.path.join(context.projects_path, context.project)
        
        context.target_well_information_path = os.path.join(context.project_path, 'target_well_information')
        context.well_data_path = os.path.join(context.project_path, 'well_data')
        context.survey_data_path = os.path.join(context.project_path, 'survey_data')
        context.logs_path = os.path.join(context.project_path, 'logs')

        context.db_path = os.path.join(context.logs_path, f"{context.project}-{context.version}.db")

        context.target_well_information_file = os.path.join(context.target_well_information_path, "dragonfly-5-mile-target-well-information.xlsx")
        context.well_file = os.path.join(context.well_data_path, "dragonfly_5-mile-well-data.xlsx")
        context.survey_file = os.path.join(context.survey_data_path, "dragonfly-survey-data.xlsx")
        return context
    
    @staticmethod
    def cobra_5_mile():
        context = Context()
        context.project = "cobra-5-mile"
        context.project_path = os.path.join(context.projects_path, context.project)
        
        context.target_well_information_path = os.path.join(context.project_path, 'target_well_information')
        context.well_data_path = os.path.join(context.project_path, 'well_data')
        context.survey_data_path = os.path.join(context.project_path, 'survey_data')
        context.logs_path = os.path.join(context.project_path, 'logs')

        context.db_path = os.path.join(context.logs_path, f"{context.project}-{context.version}.db")

        context.target_well_information_file = os.path.join(context.target_well_information_path, "cobra-5-mile-target-well-information.xlsx")
        context.well_file = os.path.join(context.well_data_path, "cobra-5-mile-well-data.xlsx")
        context.survey_file = os.path.join(context.survey_data_path, "corba-5-mile-survey-data.xlsx")
        return context
    
    @staticmethod
    def vjranch_5_mile():
        context = Context()
        context.project = "vjranch-5-mile"
        context.project_path = os.path.join(context.projects_path, context.project)
        
        context.target_well_information_path = os.path.join(context.project_path, 'target_well_information')
        context.well_data_path = os.path.join(context.project_path, 'well_data')
        context.survey_data_path = os.path.join(context.project_path, 'survey_data')
        context.logs_path = os.path.join(context.project_path, 'logs')

        context.db_path = os.path.join(context.logs_path, f"{context.project}-{context.version}.db")

        context.target_well_information_file = os.path.join(context.target_well_information_path, "vjranch-5-mile-target-well-information.xlsx")
        context.well_file = os.path.join(context.well_data_path, "vjranch-5-mile-well-data.xlsx")
        context.survey_file = os.path.join(context.survey_data_path, "vjranch-5-mile-survey-data.xlsx")
        return context
    
    @staticmethod
    def michelada_10_mile():
        context = Context()
        context.project = "michelada-10-mile"
        context.project_path = os.path.join(context.projects_path, context.project)
        
        context.target_well_information_path = os.path.join(context.project_path, 'target_well_information')
        context.well_data_path = os.path.join(context.project_path, 'well_data')
        context.survey_data_path = os.path.join(context.project_path, 'survey_data')
        context.logs_path = os.path.join(context.project_path, 'logs')

        context.db_path = os.path.join(context.logs_path, f"{context.project}-{context.version}.db")

        context.target_well_information_file = os.path.join(context.target_well_information_path, "michelada-10-mile-target-well-information.xlsx")
        context.well_file = os.path.join(context.well_data_path, "michelada-10-mile-well-data.xlsx")
        context.survey_file = os.path.join(context.survey_data_path, "michelada-10-mile-survey-data.xlsx")
        return context
    
    @staticmethod
    def popin_cork_10_mile():
        context = Context()
        context.project = "popin-cork-10-mile"
        context.project_path = os.path.join(context.projects_path, context.project)
        
        context.target_well_information_path = os.path.join(context.project_path, 'target_well_information')
        context.well_data_path = os.path.join(context.project_path, 'well_data')
        context.survey_data_path = os.path.join(context.project_path, 'survey_data')
        context.logs_path = os.path.join(context.project_path, 'logs')

        context.db_path = os.path.join(context.logs_path, f"{context.project}-{context.version}.db")

        context.well_file = os.path.join(context.well_data_path, "popin-cork-10-mile-well-data.xlsx")
        context.survey_file = os.path.join(context.survey_data_path, "popin-cork-10-survey-data.xlsx")
        return context
    
    @staticmethod
    def redhills():
        context = Context()
        context.project = "redhills"
        context.project_path = os.path.join(context.projects_path, context.project)
        
        context.target_well_information_path = os.path.join(context.project_path, 'target_well_information')
        context.well_data_path = os.path.join(context.project_path, 'well_data')
        context.survey_data_path = os.path.join(context.project_path, 'survey_data')
        context.logs_path = os.path.join(context.project_path, 'logs')

        context.db_path = os.path.join(context.logs_path, f"{context.project}-{context.version}.db")

        context.target_well_information_file = os.path.join(context.target_well_information_path, "redhills-target-well-information.xlsx")
        context.well_file = os.path.join(context.well_data_path, "redhills-well-data.xlsx")
        context.survey_file = os.path.join(context.survey_data_path, "redhills-survey-data.xlsx")
        return context
    
    @staticmethod
    def pokerlake_5_mile():
        context = Context()
        context.project = "pokerlake-5-mile"
        context.project_path = os.path.join(context.projects_path, context.project)
        
        context.target_well_information_path = os.path.join(context.project_path, 'target_well_information')
        context.well_data_path = os.path.join(context.project_path, 'well_data')
        context.survey_data_path = os.path.join(context.project_path, 'survey_data')
        context.logs_path = os.path.join(context.project_path, 'logs')

        context.db_path = os.path.join(context.logs_path, f"{context.project}-{context.version}.db")

        context.target_well_information_file = os.path.join(context.target_well_information_path, f"{context.project}-target-well-information.xlsx")
        context.well_file = os.path.join(context.well_data_path, f"{context.project}-well-data.xlsx")
        context.survey_file = os.path.join(context.survey_data_path, f"{context.project}-survey-data.xlsx")
        return context
    
    @staticmethod
    def doublestamp_10_mile():
        context = Context()
        context.project = "doublestamp-10-mile"
        context.project_path = os.path.join(context.projects_path, context.project)
        
        context.target_well_information_path = os.path.join(context.project_path, 'target_well_information')
        context.well_data_path = os.path.join(context.project_path, 'well_data')
        context.survey_data_path = os.path.join(context.project_path, 'survey_data')
        context.logs_path = os.path.join(context.project_path, 'logs')

        context.db_path = os.path.join(context.logs_path, f"{context.project}-{context.version}.db")

        context.target_well_information_file = os.path.join(context.target_well_information_path, f"{context.project}-target-well-information.xlsx")
        context.well_file = os.path.join(context.well_data_path, f"{context.project}-well-data.xlsx")
        context.survey_file = os.path.join(context.survey_data_path, f"{context.project}-survey-data.xlsx")
        return context
    
    @staticmethod
    def cop_oxy_ash():
        context = Context()
        context.project = "cop-oxy-ash"
        context.project_path = os.path.join(context.projects_path, context.project)
        
        context.target_well_information_path = os.path.join(context.project_path, 'target_well_information')
        context.well_data_path = os.path.join(context.project_path, 'well_data')
        context.survey_data_path = os.path.join(context.project_path, 'survey_data')
        context.logs_path = os.path.join(context.project_path, 'logs')

        context.db_path = os.path.join(context.logs_path, f"{context.project}-{context.version}.db")

        context.target_well_information_file = os.path.join(context.target_well_information_path, f"{context.project}-target-well-information.xlsx")
        context.well_file = os.path.join(context.well_data_path, f"{context.project}-well-data.xlsx")
        context.survey_file = os.path.join(context.survey_data_path, f"{context.project}-survey-data.xlsx")
        return context

    @staticmethod
    def olive_won_mwp():
        context = Context()
        context.project = "olive-won-mwp"
        context.project_path = os.path.join(context.projects_path, context.project)
        
        context.target_well_information_path = os.path.join(context.project_path, 'target_well_information')
        context.well_data_path = os.path.join(context.project_path, 'well_data')
        context.survey_data_path = os.path.join(context.project_path, 'survey_data')
        context.logs_path = os.path.join(context.project_path, 'logs')

        context.db_path = os.path.join(context.logs_path, f"{context.project}-{context.version}.db")

        context.target_well_information_file = os.path.join(context.target_well_information_path, f"{context.project}-target-well-information.xlsx")
        context.well_file = os.path.join(context.well_data_path, f"{context.project}-well-data.xlsx")
        context.survey_file = os.path.join(context.survey_data_path, f"{context.project}-survey-data.xlsx")
        return context