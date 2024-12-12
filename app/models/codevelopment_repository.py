from sqlite3 import Connection, Cursor, DatabaseError, IntegrityError

from database import AFEDB
from models import Codevelopment

class CodevelopmentRepository:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = Connection(db_path)

    def __del__(self):
        # Close the database connection when the object is about to be destroyed
        self.connection.close()

    def insert(self, codevelopment_list: list[Codevelopment]):
        try:
            cursor = Cursor(self.connection)
            for codevelopment in codevelopment_list:
                if not codevelopment.reference_api or not codevelopment.target_api:
                    raise ValueError("Codevelopment reference api or target api cannot be null")
                try:
                    cursor.execute(
                        AFEDB.SQL.INSERT_CODEV.value,
                        (
                            codevelopment.reference_api,
                            codevelopment.target_api,
                            codevelopment.reference_name,
                            codevelopment.target_name
                        ),
                    )
                except IntegrityError as e:
                    raise e
            self.connection.commit()
        except IntegrityError as e:
            self.connection.rollback() 
            raise ValueError(f"Unable to insert codevelopment_list into database: {e}")
        finally:
            cursor.close()

    def get_all(self) -> list[Codevelopment]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_ALL_CODEVELOPMENTS.value)
            rows = cursor.fetchall()
            return [Codevelopment(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Unable to get codevelopments: {e}")
        finally:
            cursor.close()

    def get_by_reference_api(self, reference_api: str) -> list[Codevelopment]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_CODEVELOPMENTS_BY_REFERENCE_API.value, (reference_api,))
            rows = cursor.fetchall()
            return [Codevelopment(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Unable to get codevelopments by {reference_api}: {e}")
        finally:
            cursor.close()

 