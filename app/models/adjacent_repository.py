from sqlite3 import Connection, Cursor, DatabaseError, IntegrityError

from database import AFEDB
from models import Adjacent


class AdjacentRepository:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = Connection(db_path)

    def __del__(self):
        # Close the database connection when the object is about to be destroyed
        self.connection.close()

    def insert(self, adjacent_list: list[Adjacent]):
        try:
            cursor = Cursor(self.connection)
            for adjacent in adjacent_list:
                if not adjacent.reference_api or not adjacent.target_api:
                    raise ValueError("Adjacent reference_api or target_api cannot be null")
                try:
                    cursor.execute(
                        AFEDB.SQL.INSERT_ADJACENT.value,
                        (
                            adjacent.reference_api,
                            adjacent.reference_name,
                            adjacent.target_api,
                            adjacent.target_name,
                            adjacent.north,
                            adjacent.south,
                            adjacent.east,
                            adjacent.west,
                            adjacent.hypotenuse
                        ),
                    )
                except IntegrityError as e:
                    raise e
            self.connection.commit()  
        except IntegrityError as e:
            self.connection.rollback()
            raise ValueError(f"Unable to insert adjacent into database: {e}")
        finally:
            cursor.close()

    def insert_one(self, adjacent: Adjacent):
        cursor = None
        try:
            if adjacent is not None:
                if not adjacent.reference_api or not adjacent.target_api:
                    raise ValueError("Adjacent reference_api or target_api cannot be null")
                try:
                    cursor = Cursor(self.connection)
                    cursor.execute(
                        AFEDB.SQL.INSERT_ADJACENT.value,
                        (
                            adjacent.reference_api,
                            adjacent.reference_name,
                            adjacent.target_api,
                            adjacent.target_name,
                            adjacent.north,
                            adjacent.south,
                            adjacent.east,
                            adjacent.west,
                            adjacent.hypotenuse
                        ),
                    )
                except IntegrityError as e:
                    raise e
            self.connection.commit()  
        except IntegrityError as e:
            self.connection.rollback()
            raise ValueError(f"Unable to insert adjacent into database: {e}")
        finally:
            if cursor:
                cursor.close()

    def get_all(self) -> list[Adjacent]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_ALL_ADJACENTS.value)
            rows = cursor.fetchall()
            return [Adjacent(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Unable to get all adjacents: {e}")
        finally:
            cursor.close()   

    def get_by_reference_api_west(self, reference_api: str) -> list[Adjacent]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_ADJACENT_BY_REFERENCE_API_WEST.value, (reference_api,))
            rows = cursor.fetchall()
            return [Adjacent(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Unable to get adjacent for reference_api {reference_api}: {e}")
        finally:
            cursor.close()          

    def get_by_reference_api_east(self, reference_api: str) -> list[Adjacent]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_ADJACENT_BY_REFERENCE_API_EAST.value, (reference_api,))
            rows = cursor.fetchall()
            return [Adjacent(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Unable to get adjacent for reference_api {reference_api}: {e}")
        finally:
            cursor.close()   

    def get_by_reference_api_north(self, reference_api: str) -> list[Adjacent]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_ADJACENT_BY_REFERENCE_API_NORTH.value, (reference_api,))
            rows = cursor.fetchall()
            return [Adjacent(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Unable to get adjacent for reference_api {reference_api}: {e}")
        finally:
            cursor.close()          

    def get_by_reference_api_south(self, reference_api: str) -> list[Adjacent]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_ADJACENT_BY_REFERENCE_API_SOUTH.value, (reference_api,))
            rows = cursor.fetchall()
            return [Adjacent(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Unable to get adjacent for reference_api {reference_api}: {e}")
        finally:
            cursor.close()   

    def get_by_apis(self, reference_api: str, target_api: str) -> Adjacent:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_ADJACENT_BY_REFERENCE_TARGET_APIS.value, (reference_api, target_api,))
            row = cursor.fetchone()
            if row is None:
                return None
            return Adjacent(*row)
        except DatabaseError as e:
            raise ValueError(f"Unable to get adjacent: {e}")
        finally:
            cursor.close()

    def get_list_by_reference_apis(self, reference_apis: list[str]) -> list[Adjacent]:
        try:
            placeholders = ', '.join('?' for api in reference_apis)
            query = f'SELECT * FROM adjacent WHERE reference_api IN ({placeholders}) ORDER BY reference_name ASC, target_name ASC'
            cursor = Cursor(self.connection)
            cursor.execute(query, tuple(reference_apis))
            rows = cursor.fetchall()
            return [Adjacent(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Unable to get all adjacents by list of reference_apis: {e}")
        finally:
            cursor.close()


    def delete(self, reference_api: str, target_api: str):
        if not reference_api or not target_api:
            raise ValueError("Adjacent reference_api or target_api cannot be null")
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.DELETE_ADJACENT.value, (reference_api, target_api))
            self.connection.commit()  
        except DatabaseError as e:
            raise ValueError(f"Unable to delete adjacent for reference_api {reference_api} and target_api {target_api}: {e}")
        finally:
            cursor.close()