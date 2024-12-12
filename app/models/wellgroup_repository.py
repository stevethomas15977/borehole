from sqlite3 import Connection, Cursor, DatabaseError, IntegrityError
from traceback import print_exc

from database import AFEDB
from models import WellGroup


class WellGroupRepository:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = Connection(db_path)

    def __del__(self):
        self.connection.close()

    def insert(self, wellgroup: WellGroup):
        try:
            cursor = Cursor(self.connection)
            if not wellgroup.name and not wellgroup.color:
                raise ValueError("wellgroup name and color cannot be null")
            try:
                cursor.execute(
                    AFEDB.SQL.INSERT_WELL_GROUP.value,
                    (
                        wellgroup.name,
                        wellgroup.color
                    ),
                )
            except IntegrityError as e:
                raise ValueError(f"Unable to insert WellGroup {wellgroup.name} into database: {e}  \n {print_exc()}") 
            self.connection.commit()
        except IntegrityError as e:
            self.connection.rollback() 
            raise ValueError(f"Unable to insert WellGroup {wellgroup.name} into database: {e} \n {print_exc()}")
        finally:
            cursor.close()

    def update(self, wellgroup: WellGroup):
        try:
            cursor = Cursor(self.connection)
            if not wellgroup.name and not wellgroup.color:
                raise ValueError("wellgroup name and color cannot be null")
            try:
                cursor.execute(
                    AFEDB.SQL.UPDATE_WELL_GROUP.value,
                    (
                        wellgroup.color,
                        wellgroup.avg_cumoil_per_ft,
                        wellgroup.name
                    ),
                )
            except IntegrityError as e:
                raise ValueError(f"Unable to update WellGroup {wellgroup.name} in database: {e}  \n {print_exc()}") 
            self.connection.commit()
        except IntegrityError as e:
            self.connection.rollback() 
            raise ValueError(f"Unable to update WellGroup {wellgroup.name} in database: {e} \n {print_exc()}")
        finally:
            cursor.close()

    def get_all(self) -> list[WellGroup]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_ALL_WELL_GROUPS.value)
            rows = cursor.fetchall()
            return [WellGroup(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Unable to get all WellGroups: {e}")
        finally:
            cursor.close()

    def get_by_name(self, name: str) -> WellGroup:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_WELL_GROUP_BY_NAME.value, (name,))
            row = cursor.fetchone()
            if row is None:
                return None
            return WellGroup(*row)
        except DatabaseError as e:
            raise ValueError(f"Unable to get WellGroup by {name}: {e} \n {print_exc()}")
        finally:
            cursor.close()


 