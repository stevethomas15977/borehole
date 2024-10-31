from sqlite3 import Connection, Cursor, DatabaseError, IntegrityError

from database import AFEDB
from models import GunBarrel

class GunBarrelRepository:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = Connection(db_path)

    def __del__(self):
        self.connection.close()

    def insert(self, gun_barrel: GunBarrel):
        cursor = None
        try:
            if gun_barrel is not None:
                if not gun_barrel.target_well_api or not gun_barrel.offset_well_api:
                    raise ValueError("GunBarrel Target or Offset API cannot be null")
                try:
                    cursor = Cursor(self.connection)
                    cursor.execute(
                        AFEDB.SQL.INSERT_GUN_BARREL_PLOT.value,
                        (
                            gun_barrel.target_well_api,
                            gun_barrel.offset_well_api,
                            gun_barrel.overlap_feet,
                            gun_barrel.overlap_percentage,
                            gun_barrel.cumulative_oil_per_ft,
                            gun_barrel.overlap_cumulative_oil_ft,
                            gun_barrel.months_from_first_production
                        ),
                    )
                except IntegrityError as e:
                    raise e
            self.connection.commit()  
        except IntegrityError as e:
            self.connection.rollback()
            raise ValueError(f"Unable to insert gun barrel into database: {e}")
        finally:
            if cursor:
                cursor.close()

    def select_all(self) -> list[GunBarrel]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_ALL_GUN_BARREL.value)
            rows = cursor.fetchall()
            return [GunBarrel(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Database error during select of gun barrels: {e}") from e
        finally:
            if cursor:
                cursor.close()

    def select_by_target_well_api(self, target_well_api: str) -> list[GunBarrel]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_GUN_BARREL_PLOT_BY_TARGET_WELL_API.value, (target_well_api,))
            rows = cursor.fetchall()
            return [GunBarrel(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Database error during select of gun barrel target wells: {e}") from e
        finally:
            cursor.close()

    def select_by_target_offset_well_api(self, target_well_api: str, offset_well_api: str) -> GunBarrel:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_GUN_BARREL_PLOT_BY_TARGET_OFFSET_WELL_API.value, (target_well_api, offset_well_api,))
            rows = cursor.fetchone()
            return GunBarrel(*rows)
        except DatabaseError as e:
            raise ValueError(f"Database error during select of gun barrel by target well {target_well_api} offset well {offset_well_api}: {e}") from e
        finally:
            cursor.close()

    def update(self, gun_barrel: GunBarrel):
        try:
            cursor = Cursor(self.connection)
            cursor.execute(
                AFEDB.SQL.UPDATE_GUN_BARREL.value,
                (
                    gun_barrel.overlap_feet,
                    gun_barrel.overlap_percentage,
                    gun_barrel.cumulative_oil_per_ft,
                    gun_barrel.overlap_cumulative_oil_ft,
                    gun_barrel.months_from_first_production,
                    gun_barrel.target_well_api,
                    gun_barrel.offset_well_api,
                ),
            )
            self.connection.commit()
        except IntegrityError as e:
            self.connection.rollback() 
            raise ValueError(
                f"Integrity constraint violation for gun barrel {gun_barrel.target_well_api} and {gun_barrel.offset_well_api}" 
            ) from e
        except DatabaseError as e:
            raise ValueError(f"Database error updating gun barrel: {e}") from e
        finally:
            cursor.close()

