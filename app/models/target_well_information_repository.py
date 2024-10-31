from sqlite3 import Connection, Cursor, DatabaseError

from database import AFEDB
from models import TargetWellInformation

class TargetWellInformationRepository:
    def __init__(self, db_path=None):
        self.connection = Connection(db_path)

    def __del__(self):
        self.connection.close()

    def update(self, target_well: TargetWellInformation):
        try:
            cursor = Cursor(self.connection)
            cursor.execute(
                AFEDB.SQL.UPDATE_TARGET_WELL_INFORMATION_LATITUDE_LONGITUDE_VALUES.value,
                (
                    target_well.latitude_surface_location,
                    target_well.longitude_surface_location,
                    target_well.latitude_first_take_point,
                    target_well.longitude_first_take_point,
                    target_well.latitude_last_take_point,
                    target_well.longitude_last_take_point,
                    target_well.latitude_bottom_hole,
                    target_well.longitude_bottom_hole,
                    target_well.name
                ),
            )
            self.connection.commit()
        except DatabaseError as e:
            raise ValueError(f"Database error updating target well information latitude/longitude values: {e}") from e
        finally:
            cursor.close()

    def get_first_row(self) -> TargetWellInformation:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_TARGET_WELL_INFORMATION_FIRST_ROW.value)
            row = cursor.fetchone()
            if row:
                return TargetWellInformation(*row)
        except DatabaseError as e:
            raise ValueError(f"Unable to get target well information {e}")
        finally:
            cursor.close()

    def get_shallowest(self) -> int:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_TARGEL_WELL_INFORMATION_SHALLOWEST.value)
            row = cursor.fetchone()
            if row:
                return int(*row)
        except DatabaseError as e:
            raise ValueError(f"Unable to get target well information shallowest well{e}")
        finally:
            cursor.close()

    def get_deepest(self) -> int:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_TARGEL_WELL_INFORMATION_DEEPEST.value)
            row = cursor.fetchone()
            if row:
                return int(*row)
        except DatabaseError as e:
            raise ValueError(f"Unable to get target well information deepest well{e}")
        finally:
            cursor.close()

    def get_max_lateral_length(self) -> int:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_TARGEL_WELL_INFORMATION_MAX_LATERAL_LENGTH.value)
            row = cursor.fetchone()
            if row:
                return int(*row)
        except DatabaseError as e:
            raise ValueError(f"Unable to get target well information max lateral length{e}")
        finally:
            cursor.close()
            
    def get_by_api(self, api: str) -> TargetWellInformation:
        if not api:
            raise ValueError("Target well information API cannot be null")
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_TARGET_WELL_INFORMATION_BY_API.value, (api,))
            row = cursor.fetchone()
            if row is None:
                return None
            return TargetWellInformation(*row)
        except DatabaseError as e:
            raise ValueError(f"Unable to get target well information by API {api}: {e}")
        finally:
            cursor.close()

    def get_by_name(self, name: str) -> TargetWellInformation:
        if not name:
            raise ValueError("Target well information name cannot be null")
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_TARGET_WELL_INFORMATION_BY_NAME.value, (name,))
            row = cursor.fetchone()
            if row is None:
                return None
            return TargetWellInformation(*row)
        except DatabaseError as e:
            raise ValueError(f"Unable to get target well information by name {name}: {e}")
        finally:
            cursor.close()

    def get(self) -> list[TargetWellInformation]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_TARGET_WELL_INFORMATION.value)
            rows = cursor.fetchall()
            return [TargetWellInformation(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Unable to get target well information: {e}")
        finally:
            cursor.close()

    def get_distinct_states(self) -> list[str]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_TARGET_WELL_INFORMATION_DISTINCT_STATES.value)
            rows = cursor.fetchall()
            return [str(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Unable to get distinct target well information states: {e}")
        finally:
            cursor.close()

    def get_distinct_texas_abstracts(self) -> list[str]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_TARGET_WELL_INFORMATION_TEXAS_DISTINCT_ABSTRACTS.value)
            rows = cursor.fetchall()
            return [str(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Unable to get distinct target well information texas abstracts: {e}")
        finally:
            cursor.close()

    def get_by_texas_abstract(self, texas_abstract: str) -> list[TargetWellInformation]:
        if not texas_abstract:
            raise ValueError("Target well information texas abstract cannot be null")
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_TARGET_WELL_INFORMATION_BY_TEXAS_ABSTRACT.value, (texas_abstract,))
            rows = cursor.fetchall()
            return [TargetWellInformation(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Unable to get target well information by texas abstract: {e}")
        finally:
            cursor.close()