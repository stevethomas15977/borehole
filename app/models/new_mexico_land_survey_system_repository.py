from sqlite3 import Connection, Cursor, DatabaseError, IntegrityError

from database import AFEDB
from models import NewMexicoLandSurveySystem


class NewMexicoLandSurveySystemRepository:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = Connection(db_path)

    def __del__(self):
        self.connection.close()
    
    def get_by_township_range_section(self, township: int, township_direction: str, range:int, range_direction: str, section: str) -> NewMexicoLandSurveySystem:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_NEW_MEXICO_LAND_SURVEY_SYSTEM_BY_TOWNSHIP_RANGE_SECTION.value, (township, township_direction, range, range_direction, section,))
            row = cursor.fetchone()
            if row:
                return NewMexicoLandSurveySystem(*row)
        except DatabaseError as e:
            raise ValueError(f"Unable to get new mexico land survey system by {township} {township_direction} {range} {range_direction} {section}: {e}")
        finally:
            cursor.close()

 