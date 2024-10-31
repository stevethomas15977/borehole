from services import TexasLandSurveySystemService
from models import TexasLandSurveySystem
from tasks.task import Task
from tasks.task_enum import TASKS
from helpers import task_logger, county_fips, section_4_corners
from database import AFEDB
from traceback import format_exc
import os
import geopandas as gpd

class LoadTexasLandSurveySystem(Task):

    def execute(self):
        task = TASKS.LOAD_TEXAS_LAND_SURVEY_SYSTEM.value
        logger = task_logger(task, self.context.logs_path)
        try:
            afe_db = AFEDB(self.context._texas_land_survey_system_database_path)
            afe_db.execute_ddl(AFEDB.SQL.DROP_TEXAS_LAND_SURVEY_SYSTEM_TABLE.value)
            afe_db.execute_ddl(AFEDB.SQL.CREATE_TEXAS_LAND_SURVEY_SYSTEM_TABLE.value)

            texas_land_survey_system_service = TexasLandSurveySystemService(db_path=self.context._texas_land_survey_system_database_path)

            for county, fips_code in county_fips().items():
                if county not in ["Loving", "Ward", "Winkler"]:
                    continue    

                logger.info(f"Loading {county}")

                geojson_file = os.path.join(self.context.geojson_path, "texas", "block-section", f"surv{fips_code}p.geojson")
                                
                gdf = gpd.read_file(geojson_file)

                texas_land_survey_system_list = []

                for _, row in gdf.iterrows():
                    abstract = row.get('ABSTRACT_L')
                    block = row.get('LEVEL2_BLO')
                    section = row.get('LEVEL3_SUR')
                    grantee = row.get('LEVEL4_SUR')
                    geometry = row.get('geometry')
                    corners = section_4_corners(geometry=geometry)
                    if not corners:
                        continue
                    southwest_latitude = None
                    southwest_longitude = None
                    northwest_latitude = None
                    northwest_longitude = None
                    southeast_latitude = None
                    southeast_longitude = None
                    northeast_latitude = None
                    northeast_longitude = None
                    for corner, coords in corners.items():
                        longitude = coords[0]
                        latitude = coords[1]
                        if corner == 'southwest':
                            southwest_latitude = latitude
                            southwest_longitude = longitude
                        elif corner == 'northwest':
                            northwest_latitude = latitude
                            northwest_longitude = longitude
                        elif corner == 'southeast':
                            southeast_latitude = latitude
                            southeast_longitude = longitude
                        elif corner == 'northeast':
                            northeast_latitude = latitude
                            northeast_longitude = longitude
                        
                    texas_land_survey_system = TexasLandSurveySystem(county=county,
                                                                    fips_code=fips_code,
                                                                    abstract=abstract,
                                                                    block=block,
                                                                    section=section,
                                                                    grantee=grantee,
                                                                    southwest_latitude=southwest_latitude,
                                                                    southwest_longitude=southwest_longitude,
                                                                    northwest_latitude=northwest_latitude,
                                                                    northwest_longitude=northwest_longitude,
                                                                    southeast_latitude=southeast_latitude,
                                                                    southeast_longitude=southeast_longitude,
                                                                    northeast_latitude=northeast_latitude,
                                                                    northeast_longitude=northeast_longitude)
                    texas_land_survey_system_list.append(texas_land_survey_system)

                if len(texas_land_survey_system_list) > 0:
                    texas_land_survey_system_service.add(texas_land_survey_system_list)

            logger.info(f"{task}: {self.context.logs_path}")
        except Exception as e:
            logger.error(f"Error {task} workflow task: {e}\n{format_exc()}")
            raise ValueError(f"Error {task} workflow task: {e}")