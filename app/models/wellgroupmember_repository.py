from sqlite3 import Connection, Cursor, DatabaseError, IntegrityError
from traceback import print_exc

from database import AFEDB
from models import WellGroupMember


class WellGroupMemberRepository:
    def __init__(self, db_path=None):
        self.connection = Connection(db_path)

    def __del__(self):
        self.connection.close()

    def insert(self, wellgroupmember: WellGroupMember):
        try:
            cursor = Cursor(self.connection)
            if not wellgroupmember.group_name or not wellgroupmember.well_api:
                raise ValueError("WellGroupMember group or well api cannot be null")
            try:
                cursor.execute(
                    AFEDB.SQL.INSERT_WELL_GROUP_MEMBER.value,
                    (
                        wellgroupmember.group_name,
                        wellgroupmember.well_api,
                        wellgroupmember.well_name
                    ),
                )
            except IntegrityError as e:
                self.connection.rollback()
                error_msg = f"Unable to insert well group member '{wellgroupmember.well_api}' into database: {e} \n {print_exc()}"
                raise(error_msg)
            self.connection.commit()
        finally:
            cursor.close()

    def get_all(self) -> list[WellGroupMember]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_WELL_GROUP_MEMBERS.value)
            rows = cursor.fetchall()
            return [WellGroupMember(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Unable to get all well group members: {e} \n {print_exc()}")
        finally:
            cursor.close()

    def get_all_group_name(self, group_name: str) -> list[WellGroupMember]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_WELL_GROUP_MEMBERS_BY_GROUP_NAME.value, (group_name,))
            rows = cursor.fetchall()
            return [WellGroupMember(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Unable to get all well group members by {group_name}: {e} \n {print_exc()}")
        finally:
            cursor.close()

    def get_by_group_name_well_api(self, group_name: str, well_api: str) -> WellGroupMember:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_WELL_GROUP_MEMBER_BY_GROUP_NAME_WELL_API.value, (group_name, well_api,))
            row = cursor.fetchone()
            if row is None:
                return None
            return WellGroupMember(*row)
        except DatabaseError as e:
            raise ValueError(f"Unable to get well group by {well_api}: {e} \n {print_exc()}")
        finally:
            cursor.close()

