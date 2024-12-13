from logging import warning
from sqlite3 import Connection, Cursor, DatabaseError, IntegrityError

from database import AFEDB
from models import Well


class WellRepository:
    def __init__(self, db_path=None):
        self.connection = Connection(db_path)

    def __del__(self):
        self.connection.close()

    def insert(self, wells: list[Well]):
        try:
            cursor = Cursor(self.connection)
            for well in wells:
                if not well.api or not well.name:
                    raise ValueError("Well api or name cannot be null")
                try:
                    cursor.execute(
                        AFEDB.SQL.INSERT_WELL.value,
                        (
                            well.api,
                            well.name,
                            well.direction,
                            well.operator,
                            well.status,
                            well.lease,
                            well.interval,
                            well.formation,
                            well.first_production_date,
                            well.surface_latitude,
                            well.surface_longitude,
                            well.bottom_hole_latitude,
                            well.bottom_hole_longitude,
                            well.total_vertical_depth,
                            well.measured_depth,
                            well.kelly_bushing_elevation,
                            well.lateral_length,
                            well.perf_interval,
                            well.proppant_intensity,
                            well.state,
                            well.county,
                            well.abstract,
                            well.township,
                            well.range,
                            well.section,
                            well.cumlative_oil,
                            well.last_producing_month,
                            well.cumoil_bblper1000ft,
                            well.cumoil_bblperft
                        ),
                    )
                except IntegrityError as e:
                    # TODO Can not be guaranteed the data is unique, so we should log the error and continue
                    #self.connection.rollback()
                    error_msg = f"Unable to insert well '{well.name}' into database: {e}"
                    warning(error_msg)
                    #raise ValueError(error_msg) from e
                    continue
            self.connection.commit()
        finally:
            cursor.close()

    def get_by_api(self, api: str):
        if not api:
            raise ValueError("Well api cannot be null")
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_WELL_BY_API.value, (api,))
            row = cursor.fetchone()
            if row is None:
                return None
            return Well(*row)
        except DatabaseError as e:
            raise ValueError(f"Unable to get well by api: {e}")
        finally:
            cursor.close()

    def get_by_name(self, name: str):
        if not name:
            raise ValueError("Well name cannot be null")
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_WELL_BY_NAME.value, (name,))
            row = cursor.fetchone()
            if row is None:
                return None
            return Well(*row)
        except DatabaseError as e:
            raise ValueError(f"Unable to get well by name: {e}")
        finally:
            cursor.close()

    def get(self) -> list[Well]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_WELLS.value)
            rows = cursor.fetchall()
            return [Well(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Unable to get wells: {e}")
        finally:
            cursor.close()

    def get_distinct_states(self) -> list[str]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_WELL_STATES.value)
            rows = cursor.fetchall()
            return [str(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Unable to get distinct well states: {e}")
        finally:
            cursor.close()

    def get_distinct_texas_abstracts(self) -> list[str]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_WELL_TEXAS_ABSTRACTS.value)
            rows = cursor.fetchall()
            return [str(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Unable to get distinct texas abstracts: {e}")
        finally:
            cursor.close()

    def get_wells_by_texas_abstract(self, texas_abstract: str) -> list[Well]:
        if not texas_abstract:
            raise ValueError("Texas abstract cannot be null")
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_WELLS_BY_TEXAS_ABSTRACT.value, (texas_abstract,))
            rows = cursor.fetchall()
            return [Well(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Unable to get wells by texas abstract: {e}")
        finally:
            cursor.close()