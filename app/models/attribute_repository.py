from sqlite3 import Connection, Cursor, DatabaseError, IntegrityError

from database import AFEDB
from models import Attribute


class AttributeRepository:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = Connection(db_path)

    def __del__(self):
        self.connection.close()

    def insert(self, attributes: list[Attribute]):
        try:
            cursor = Cursor(self.connection)
            for attribute in attributes:
                if not attribute.name and not attribute.key:
                    raise ValueError("Attribute name and key cannot be null")
                try:
                    cursor.execute(
                        AFEDB.SQL.INSERT_ATTRIBUTE.value,
                        (
                            attribute.name,
                            attribute.key,
                            attribute.value
                        ),
                    )
                except IntegrityError as e:
                    raise e
            self.connection.commit()
        except IntegrityError as e:
            self.connection.rollback() 
            raise ValueError(f"Unable to insert attributes into database: {e}")
        finally:
            cursor.close()

    def get_by_name(self, name: str) -> list[Attribute]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_ATTRIBUTES_BY_NAME.value, (name,))
            rows = cursor.fetchall()
            return [Attribute(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Unable to get attributes: {e}")
        finally:
            cursor.close()

    def get_distinct_groups(self) -> list[str]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_DISTINCT_ATTRIBUTE_GROUPS.value)
            rows = cursor.fetchall()
            return [str(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Unable to get groups: {e}")
        finally:
            cursor.close()

    def get_names_by_group(self, group: str) -> list[str]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_NAMES_BY_GROUP.value, (group,))
            rows = cursor.fetchall()
            return [str(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Unable to get group names: {e}")
        finally:
            cursor.close()


 