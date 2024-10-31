from sqlite3 import Connection, Cursor, DatabaseError, IntegrityError

from database import AFEDB
from models import XYZDistance


class XYZDistanceRepository:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = Connection(db_path)

    def __del__(self):
        self.connection.close()

    def inserts(self, xyzdistance_list: list[XYZDistance]):
        try:
            cursor = Cursor(self.connection)
            for xyzdistance in xyzdistance_list:
                if not xyzdistance.reference_api or not xyzdistance.target_api:
                    raise ValueError("XYZDistance reference_api and target_api cannot be null")
                try:
                    cursor.execute(
                        AFEDB.SQL.INSERT_XYZ_DISTANCE.value,
                        (
                            xyzdistance.reference_api,
                            xyzdistance.reference_name,
                            xyzdistance.target_api,
                            xyzdistance.target_name,
                            xyzdistance.start_x,
                            xyzdistance.start_y,
                            xyzdistance.start_z,
                            xyzdistance.start_hypotenuse,
                            xyzdistance.mid_x,
                            xyzdistance.mid_y,
                            xyzdistance.mid_z,
                            xyzdistance.mid_hypotenuse,
                            xyzdistance.end_x,
                            xyzdistance.end_y,
                            xyzdistance.end_z,
                            xyzdistance.end_hypotenuse
                        ),
                    )
                except IntegrityError as e:
                    raise e
            self.connection.commit()  
        except IntegrityError as e:
            self.connection.rollback()
            raise ValueError(f"Unable to insert XYZDistance into database: {e}")
        finally:
            cursor.close()

    def get_by_simulated_well(self) -> list[XYZDistance]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_XYZ_DISTANCE_BY_SIMULATED_WELL.value, ("00-000-00000",))
            rows = cursor.fetchall()
            return [XYZDistance(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Unable to get siumated well xyz distances: {e}")
        finally:
            cursor.close()

    def get_by_reference_well(self, reference_well_api: str) -> list[XYZDistance]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_XYZ_DISTANCE_BY_REFERENCE_WELL.value, (reference_well_api,))
            rows = cursor.fetchall()
            return [XYZDistance(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Unable to get reference well xyz distances: {e}")
        finally:
            cursor.close()

    def get_by_target_well(self, target_well_api: str) -> list[XYZDistance]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_XYZ_DISTANCE_BY_TARGET_WELL.value, (target_well_api,))
            rows = cursor.fetchall()
            return [XYZDistance(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Unable to get target well xyz distances: {e}")
        finally:
            cursor.close()

    def get_for_simulated_target_well(self, target_well_api: str) -> list[XYZDistance]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_XYZ_DISTANCE_FOR_SIMULATED_TARGET_WELL.value, (target_well_api,))
            rows = cursor.fetchall()
            return [XYZDistance(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Unable to get simulated target well xyz distances: {e}")
        finally:
            cursor.close()

    def get_by_reference_target_well(self, reference_well_api: str, target_well_api: str) -> XYZDistance:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_XYZ_DISTANCE_BY_REF_TARGET_WELLS.value, (reference_well_api, target_well_api))
            row = cursor.fetchone()
            if row:
                return XYZDistance(*row)
            else:
                return None
        except DatabaseError as e:
            raise ValueError(f"Unable to get reference target well xyz distance: {e}")
        finally:
            cursor.close()

            
