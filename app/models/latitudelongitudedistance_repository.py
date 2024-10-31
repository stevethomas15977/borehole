from sqlite3 import Connection, Cursor, DatabaseError, IntegrityError

from database import AFEDB
from models import LatitudeLongitudeDistance


class LatitudeLongitudeDistanceRepository:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = Connection(db_path)

    def __del__(self):
        self.connection.close()

    def inserts(self, latitudelongitudedistance_list: list[LatitudeLongitudeDistance]):
        try:
            cursor = Cursor(self.connection)
            for latitudelongitudedistance in latitudelongitudedistance_list:
                if not latitudelongitudedistance.reference_api or not latitudelongitudedistance.target_api:
                    raise ValueError("LatitudeLongitudeDistance reference_api and target_api cannot be null")
                try:
                    cursor.execute(
                        AFEDB.SQL.INSERT_LATITUDE_LONGITUDE_DISTANCE.value,
                        (
                            latitudelongitudedistance.reference_api,
                            latitudelongitudedistance.reference_name,
                            latitudelongitudedistance.target_api,
                            latitudelongitudedistance.target_name,
                            latitudelongitudedistance.start_latitude,
                            latitudelongitudedistance.start_longitude,
                            latitudelongitudedistance.start_z,
                            latitudelongitudedistance.start_hypotenuse,
                            latitudelongitudedistance.mid_latitude,
                            latitudelongitudedistance.mid_longitude,
                            latitudelongitudedistance.mid_z,
                            latitudelongitudedistance.mid_hypotenuse,
                            latitudelongitudedistance.end_latitude,
                            latitudelongitudedistance.end_longitude,
                            latitudelongitudedistance.end_z,
                            latitudelongitudedistance.end_hypotenuse
                        ),
                    )
                except IntegrityError as e:
                    raise e
            self.connection.commit()  
        except IntegrityError as e:
            self.connection.rollback()
            raise ValueError(f"Unable to insert LatitudeLongitudeDistances into database: {e}")
        finally:
            cursor.close()

    def get(self) -> list[LatitudeLongitudeDistance]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_LATITUDE_LONGITUDE_DISTANCES.value)
            rows = cursor.fetchall()
            return [LatitudeLongitudeDistance(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Unable to get LatitudeLongitudeDistances: {e}")
        finally:
            cursor.close()

    def get_by_reference_api(self, reference_api: str) -> list[LatitudeLongitudeDistance]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_LATITUDE_LONGITUDE_DISTANCES_BY_REFERENCE_API.value, (reference_api,))
            rows = cursor.fetchall()
            return [LatitudeLongitudeDistance(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Unable to get LatitudeLongitudeDistance for {reference_api}: {e}")
        finally:
            cursor.close()

    def get_by_reference_target_apis(self, reference_api: str, target_api) -> LatitudeLongitudeDistance:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_LATITUDE_LONGITUDE_DISTANCE_BY_REFERENCE_TARGET_APIS.value, (reference_api, target_api))
            row = cursor.fetchone()
            return LatitudeLongitudeDistance(*row)
        except DatabaseError as e:
            raise ValueError(f"Unable to get LatitudeLongitudeDistance by {reference_api} and {target_api}: {e}")
        finally:
            cursor.close()