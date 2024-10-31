from sqlite3 import Connection, Cursor, DatabaseError, IntegrityError

from database import AFEDB
from models import ParentChild


class ParentChildRepository:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = Connection(db_path)

    def __del__(self):
        self.connection.close()

    def insert(self, parentchildren: list[ParentChild]) -> None:
        try:
            cursor = Cursor(self.connection)
            for parentchild in parentchildren:
                if not parentchild.parent_api and not parentchild.child_api:
                    raise ValueError("ParentChild parent and child cannot be null")
                try:
                    cursor.execute(
                        AFEDB.SQL.INSERT_PARENT_CHILD.value,
                        (
                            parentchild.parent_api,
                            parentchild.parent_name,
                            parentchild.child_api,
                            parentchild.child_name,
                            parentchild.sibling_api,
                            parentchild.sibling_name,
                            parentchild.adjacent,
                            parentchild.parent_interval,
                            parentchild.child_interval,
                            parentchild.sibling_interval
                        ),
                    )
                except IntegrityError as e:
                    raise e
            self.connection.commit()
        except IntegrityError as e:
            self.connection.rollback() 
            raise ValueError(f"Unable to insert parcent child into database: {e}")
        finally:
            cursor.close()

    def get_by_parent_api(self, parent_api: str) -> list[ParentChild]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_PARENTCHILD_BY_PARENT_API.value, (parent_api,))
            rows = cursor.fetchall()
            return [ParentChild(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Unable to get parent child by {parent_api}: {e}")
        finally:
            cursor.close()

    def get_by_child_api(self, child_api: str) -> list[ParentChild]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_PARENTCHILD_BY_CHILD_API.value, (child_api,))
            rows = cursor.fetchall()
            return [ParentChild(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Unable to get parent childres by child api {child_api}: {e}")
        finally:
            cursor.close()

    def get_by_child_api_adjacent(self, child_api: str, adjacent: str) -> ParentChild:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_PARENTCHILD_CHILD_API_ADJACENT.value, (child_api, adjacent,))
            row = cursor.fetchone()
            if row is None:
                return None
            return ParentChild(*row)
        except DatabaseError as e:
            raise ValueError(f"Unable to get parent child by adjacent {adjacent} and child api {child_api}: {e}")
        finally:
            cursor.close()

 