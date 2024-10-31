from sqlite3 import Connection, Cursor, DatabaseError, IntegrityError

from database import AFEDB
from models import GunBarrelTriangleDistances

class GunBarrelTriangleDistancesRepository:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = Connection(db_path)

    def __del__(self):
        self.connection.close()

    def insert(self, gun_barrel_triangle_distances: GunBarrelTriangleDistances):
        cursor = None
        try:
            if gun_barrel_triangle_distances is not None:
                if not gun_barrel_triangle_distances.target_well_api or not gun_barrel_triangle_distances.offset_well_api:
                    raise ValueError("Gun Barrel Triangle Distances Target or Offset API cannot be null")
                try:
                    cursor = Cursor(self.connection)
                    cursor.execute(
                        AFEDB.SQL.INSERT_GUN_BARREL_TRIANGLE_DISTANCES.value,
                        (
                            gun_barrel_triangle_distances.target_well_api,
                            gun_barrel_triangle_distances.offset_well_api,
                            gun_barrel_triangle_distances.adjacent,
                            gun_barrel_triangle_distances.opposite,
                            gun_barrel_triangle_distances.hypotenuse
                        ),
                    )
                except IntegrityError as e:
                    raise e
            self.connection.commit()  
        except IntegrityError as e:
            self.connection.rollback()
            raise ValueError(f"Unable to insert gun barrel triangle distances into database: {e}")
        finally:
            if cursor:
                cursor.close()

    def select_all(self) -> list[GunBarrelTriangleDistances]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_GUN_BARREL_TRIANGLE_DISTANCES.value)
            rows = cursor.fetchall()
            return [GunBarrelTriangleDistances(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Database error during select of gun barrel triangle distances: {e}") from e
        finally:
            if cursor:
                cursor.close()

    def select_by_target_api(self, target_well_api: str) -> list[GunBarrelTriangleDistances]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_GUN_BARREL_TRIANGLE_DISTANCES_By_TARGET_WELL_API.value, (target_well_api,))
            rows = cursor.fetchall()
            return [GunBarrelTriangleDistances(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(
                f"Database error during gun barrel triangle distances for APIs {target_well_api}: {e}"
            ) from e
        finally:
            cursor.close()

    def select_by_target_offset_api(self, target_well_api: str, offset_well_api: str) -> GunBarrelTriangleDistances:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_GUN_BARREL_TRIANGLE_DISTANCES_By_TARGET_WELL_OFFSET_WELL_API.value, (target_well_api,offset_well_api,))
            row = cursor.fetchone()
            if row:
                return GunBarrelTriangleDistances(*row)
            else:
                return None
        except DatabaseError as e:
            raise ValueError(
                f"Database error during gun barrel triangle distances for APIs {target_well_api}/{offset_well_api}: {e}"
            ) from e
        finally:
            cursor.close()

    

