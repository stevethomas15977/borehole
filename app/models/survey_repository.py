from sqlite3 import Connection, Cursor, IntegrityError

from database import AFEDB
from models import Survey


class SurveyRepository:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = Connection(db_path)

    def __del__(self):
        # Close the database connection when the object is about to be destroyed
        self.connection.close()

    def insert(self, surveys: list[Survey]):
        try:
            cursor = Cursor(self.connection)
            for survey in surveys:
                if not survey.api:
                    raise ValueError("Survey api or name cannot be null")
                try:
                    cursor.execute(
                        AFEDB.SQL.INSERT_SURVEY.value,
                        (
                            survey.api,
                            survey.station,
                            survey.md,
                            survey.inclination,
                            survey.azimuth,
                            survey.latitude,
                            survey.longitude,
                            survey.grid_x,
                            survey.grid_y,
                            survey.subsurface_depth
                        ),
                    )
                except IntegrityError as e:
                    raise Exception(f"Error inserting survey {survey.api}-{survey.station}: {e}")
            self.connection.commit()  # Commit the transaction after all inserts
        except IntegrityError as e:
            self.connection.rollback()  # Rollback in case of an error
            raise ValueError(f"Unable to insert surveys into database: {e}")
        finally:
            cursor.close()

    def get_by_api(self, api: str) -> list[Survey]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.GET_SURVEYS_BY_API.value, (api,))
            rows = cursor.fetchall()
            return [Survey(*row) for row in rows]
        except IntegrityError as e:
            raise ValueError(f"Unable to get surveys by api: {e}")
        finally:
            cursor.close()

    def get_unique_api_values(self) -> list[str]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.GET_SURVEY_UNIQUE_API_VALUES.value)
            rows = cursor.fetchall()
            return [row[0] for row in rows]
        except IntegrityError as e:
            raise ValueError(f"Unable to get survey unique api values: {e}")
        finally:
            cursor.close()

    
