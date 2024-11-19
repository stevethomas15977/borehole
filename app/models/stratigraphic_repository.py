from sqlite3 import Connection, Cursor, DatabaseError

from database import AFEDB
from models import Stratigraphic

class StratigraphicRepository:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = Connection(db_path)

    def get_by_union_code(self, union_code: str) -> Stratigraphic:
        try:
            result = Stratigraphic()
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_STRATIGRAPHIC_BY_UNION_CODE.value, (union_code,))
            row = cursor.fetchone()
            if row:
                result = Stratigraphic(*row)
                result.common_tanks = self._get_common_tanks_by_union_code(result.union_code)
            return result
        except DatabaseError as e:
            raise ValueError(f"Unable to get stratigraphic by union code {union_code} {e}")
        finally:
            cursor.close()

    def get_by_union_code_list(self, union_code_list: list[str]) -> list[Stratigraphic]:
        try:
            cursor = Cursor(self.connection)
            placeholders = "("
            for union_code in union_code_list:
                placeholders += f"'{union_code}',"
            placeholders = placeholders[:-1] + ")"
            query = f"SELECT * FROM stratigraphic WHERE union_code IN {placeholders} ORDER BY position ASC"
            cursor.execute(query)
            rows = cursor.fetchall()
            return [Stratigraphic(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Unable to get stratigraphic by union code list {union_code_list} {e}")
        finally:
            cursor.close()

    def get_by_prism_code(self, prism_code: str) -> Stratigraphic:
        try:
            result = Stratigraphic()
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_STRATIGRAPHIC_BY_PRISM_CODE.value, (prism_code,))
            row = cursor.fetchone()
            if row:
                result = Stratigraphic(*row)
                commaon_tanks = self._get_common_tanks_by_union_code(result.union_code)
                if commaon_tanks:
                    result.common_tanks = commaon_tanks
            return result
        except DatabaseError as e:
            raise ValueError(f"Unable to get stratigraphic by prism code {prism_code} {e}")
        finally:
            cursor.close()

    def _get_common_tanks_by_union_code(self, union_code: str) -> list[str]:
        try:
            results = [str]
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_STRATIGRAPHIC_COMMON_TANKS_BY_UNION_CODE.value, (union_code,))
            rows = cursor.fetchall()
            for row in rows:
                results.append(row[1])
            return results
        except DatabaseError as e:
            raise ValueError(f"Unable to get target well information: {e}")
        finally:
            cursor.close()

    def get_union_codes(self) -> list[str]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_STRATIGRAPHIC_UNION_CODES.value)
            rows = cursor.fetchall()
            return [row[0] for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Unable to get union codes {e}")
        finally:
            cursor.close()