from sqlite3 import Connection, Cursor, DatabaseError, IntegrityError

from sqlalchemy import Over

from database import AFEDB
from models import Overlap


class OverlapRepository:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = Connection(db_path)

    def insert(self, overlap: Overlap):
        cursor = None
        try:
            if overlap is not None:
                if not overlap.reference_api or not overlap.target_api:
                    raise ValueError("Overlap reference_api or target_api cannot be null")
                try:
                    cursor = Cursor(self.connection)
                    cursor.execute(
                        AFEDB.SQL.INSERT_OVERLAP.value,
                        (
                            overlap.reference_api,
                            overlap.reference_name,
                            overlap.target_api,
                            overlap.target_name,
                            overlap.overlap_feet,
                            overlap.overlap_percentage
                        ),
                    )
                except IntegrityError as e:
                    raise e
            self.connection.commit()  
        except IntegrityError as e:
            self.connection.rollback()
            raise ValueError(f"Unable to insert overlap into database: {e}")
        finally:
            if cursor:
                cursor.close()  

    def get_by_reference_api_target_api(self, reference_api: str, target_api: str) -> Overlap:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_OVERLAP_BY_REFERENCE_API_TARGET_API.value, (reference_api, target_api,))
            row = cursor.fetchone()
            if row is None:
                return None
            return Overlap(*row)
        except DatabaseError as e:
            raise ValueError(f"Unable to get overlap by {reference_api} and {target_api}: {e}")
        finally:
            cursor.close()