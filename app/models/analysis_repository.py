from sqlite3 import Connection, Cursor, DatabaseError, IntegrityError

from database import AFEDB
from models import Analysis


class AnalysisRepository:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = Connection(db_path)

    def __del__(self):
        # Close the database connection when the object is about to be destroyed
        self.connection.close()

    def insert_list(self, analysis_list: list[Analysis]):
        try:
            cursor = Cursor(self.connection)
            for analysis in analysis_list:
                if not analysis.api:
                    raise ValueError("Analysis api or name cannot be null")
                try:
                    cursor.execute(
                        AFEDB.SQL.INSERT_ANALYSIS.value,
                        (
                            analysis.api,
                            analysis.name,
                            analysis.direction,
                            analysis.dominant_direction,
                            analysis.interval,
                            analysis.lateral_length,
                            analysis.lateral_start_latitude,
                            analysis.lateral_start_longitude,
                            analysis.lateral_midpoint_latitude,
                            analysis.lateral_midpoint_longitude,
                            analysis.lateral_end_latitude,
                            analysis.lateral_end_longitude,
                            analysis.lateral_start_grid_x,
                            analysis.lateral_start_grid_y,
                            analysis.lateral_start_subsurface_depth,
                            analysis.lateral_midpoint_grid_x,
                            analysis.lateral_midpoint_grid_y,
                            analysis.lateral_midpoint_subsurface_depth,
                            analysis.lateral_end_grid_x,
                            analysis.lateral_end_grid_y,
                            analysis.lateral_end_subsurface_depth,
                            analysis.subsurface_depth,
                            analysis.first_production_date,
                            analysis.adjacent_1,
                            analysis.adjacent_2,
                            analysis.distance_1,
                            analysis.distance_2,
                            analysis.hypotenuse_1,
                            analysis.hypotenuse_2,
                            analysis.group_id,
                            analysis.codevelopment,
                            analysis.average_horizontal_spacing,
                            analysis.group_average_horizontal_spacing,
                            analysis.group_average_hypotenuse_spacing,
                            analysis.parents,
                            analysis.parent_1,
                            analysis.parent_1_first_production_date,
                            analysis.parent_1_delta_first_production_months,
                            analysis.parent_1_interval,
                            analysis.parent_2,
                            analysis.parent_2_first_production_date,
                            analysis.parent_2_delta_first_production_months,
                            analysis.parent_2_interval,
                            analysis.child,
                            analysis.adjacent_child,
                            analysis.sibling,
                            analysis.bound,
                            analysis.gun_barrel_x,
                            analysis.gun_barrel_y,
                            analysis.gun_barrel_z,
                            analysis.target_well_spacing_gun_barrel_plot_flag,
                            analysis.gun_barrel_index,
                            analysis.cumoil_bblperft,
                            analysis.pct_of_group_cumoil_bblperft,
                            analysis.pct_of_group_cumoil_bblperft_greater_than
                        ),
                    )
                except IntegrityError as e:
                    raise e
            self.connection.commit()  
        except IntegrityError as e:
            self.connection.rollback()
            raise ValueError(f"Unable to insert analysis into database: {e}")
        finally:
            cursor.close()

    def insert(self, analysis: Analysis):
        try:
            cursor = Cursor(self.connection)
            cursor.execute(
                AFEDB.SQL.INSERT_ANALYSIS.value,
                (
                    analysis.api,
                    analysis.name,
                    analysis.direction,
                    analysis.dominant_direction,
                    analysis.interval,
                    analysis.lateral_length,
                    analysis.lateral_start_latitude,
                    analysis.lateral_start_longitude,
                    analysis.lateral_midpoint_latitude,
                    analysis.lateral_midpoint_longitude,
                    analysis.lateral_end_latitude,
                    analysis.lateral_end_longitude,
                    analysis.lateral_start_grid_x,
                    analysis.lateral_start_grid_y,
                    analysis.lateral_start_subsurface_depth,
                    analysis.lateral_midpoint_grid_x,
                    analysis.lateral_midpoint_grid_y,
                    analysis.lateral_midpoint_subsurface_depth,
                    analysis.lateral_end_grid_x,
                    analysis.lateral_end_grid_y,
                    analysis.lateral_end_subsurface_depth,
                    analysis.subsurface_depth,
                    analysis.first_production_date,
                    analysis.adjacent_1,
                    analysis.adjacent_2,
                    analysis.distance_1,
                    analysis.distance_2,
                    analysis.hypotenuse_1,
                    analysis.hypotenuse_2,
                    analysis.group_id,
                    analysis.codevelopment,
                    analysis.average_horizontal_spacing,
                    analysis.group_average_horizontal_spacing,
                    analysis.group_average_hypotenuse_spacing,
                    analysis.parents,
                    analysis.parent_1,
                    analysis.parent_1_first_production_date,
                    analysis.parent_1_delta_first_production_months,
                    analysis.parent_1_interval,
                    analysis.parent_2,
                    analysis.parent_2_first_production_date,
                    analysis.parent_2_delta_first_production_months,
                    analysis.parent_2_interval,
                    analysis.child,
                    analysis.adjacent_child,
                    analysis.sibling,
                    analysis.bound,
                    analysis.gun_barrel_x,
                    analysis.gun_barrel_y,
                    analysis.gun_barrel_z,
                    analysis.target_well_spacing_gun_barrel_plot_flag,
                    analysis.gun_barrel_index,
                    analysis.cumoil_bblperft,
                    analysis.pct_of_group_cumoil_bblperft,
                    analysis.pct_of_group_cumoil_bblperft_greater_than
                ),
            )
            self.connection.commit()
        except IntegrityError as e:
            self.connection.rollback()  # Rollback in case of an error
            raise ValueError(
                f"Integrity constraint violation for analysis {analysis.api}"
            ) from e
        except DatabaseError as e:
            raise ValueError(f"Database error inserting analysis: {e}") from e
        finally:
            cursor.close()


    def update(self, analysis: Analysis):
        try:
            cursor = Cursor(self.connection)
            cursor.execute(
                AFEDB.SQL.UPDATE_ANALYSIS.value,
                (
                    analysis.name,
                    analysis.direction,
                    analysis.dominant_direction,
                    analysis.interval,
                    analysis.lateral_length,
                    analysis.lateral_start_latitude,
                    analysis.lateral_start_longitude,
                    analysis.lateral_midpoint_latitude,
                    analysis.lateral_midpoint_longitude,
                    analysis.lateral_end_latitude,
                    analysis.lateral_end_longitude,
                    analysis.lateral_start_grid_x,
                    analysis.lateral_start_grid_y,
                    analysis.lateral_start_subsurface_depth,
                    analysis.lateral_midpoint_grid_x,
                    analysis.lateral_midpoint_grid_y,
                    analysis.lateral_midpoint_subsurface_depth,
                    analysis.lateral_end_grid_x,
                    analysis.lateral_end_grid_y,
                    analysis.lateral_end_subsurface_depth,
                    analysis.subsurface_depth,
                    analysis.first_production_date,
                    analysis.adjacent_1,
                    analysis.adjacent_2,
                    analysis.distance_1,
                    analysis.distance_2,
                    analysis.hypotenuse_1,
                    analysis.hypotenuse_2,
                    analysis.group_id,
                    analysis.codevelopment,
                    analysis.average_horizontal_spacing,
                    analysis.group_average_horizontal_spacing,
                    analysis.group_average_hypotenuse_spacing,
                    analysis.parents,
                    analysis.parent_1,
                    analysis.parent_1_first_production_date,
                    analysis.parent_1_delta_first_production_months,
                    analysis.parent_1_interval,
                    analysis.parent_2,
                    analysis.parent_2_first_production_date,
                    analysis.parent_2_delta_first_production_months,
                    analysis.parent_2_interval,
                    analysis.child,
                    analysis.adjacent_child,
                    analysis.sibling,
                    analysis.bound,
                    analysis.gun_barrel_x,
                    analysis.gun_barrel_y,
                    analysis.gun_barrel_z,
                    analysis.target_well_spacing_gun_barrel_plot_flag,
                    analysis.gun_barrel_index,
                    analysis.cumoil_bblperft,
                    analysis.pct_of_group_cumoil_bblperft,
                    analysis.pct_of_group_cumoil_bblperft_greater_than,
                    analysis.api
                ),
            )
            self.connection.commit()
        except IntegrityError as e:
            self.connection.rollback()  # Rollback in case of an error
            raise ValueError(
                f"Integrity constraint violation for analysis {analysis.api}"
            ) from e
        except DatabaseError as e:
            raise ValueError(f"Database error updating analysis: {e}") from e
        finally:
            cursor.close()

    def reset_target_well_spacing_gun_barrel_plot_flag(self):
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.UPDATE_ANALYSIS_SET_TARGET_WELL_SPACING_GUN_BARREL_PLOT_FLAG_NULL.value)
            self.connection.commit()
        except DatabaseError as e:
            self.connection.rollback()
            raise ValueError(f"Database error during reset_target_well_spacing_gun_barrel_plot_flag: {e}") from e
        finally:
            cursor.close()

    def select_all(self) -> list[Analysis]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_ALL_ANALYSIS.value)
            rows = cursor.fetchall()
            return [Analysis(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Database error during select_all: {e}") from e
        finally:
            cursor.close()

    def select_simulated_target_wells(self) -> list[Analysis]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_ANALYSIS_BY_SIMULATED_TARGET_WELLS.value)
            rows = cursor.fetchall()
            return [Analysis(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Database error during select of simulated target wells: {e}") from e
        finally:
            cursor.close()

    def select_all_excluding_target_wells(self) -> list[Analysis]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_ANALYSIS_EXCLUDING_TARGET_WELLS.value)
            rows = cursor.fetchall()
            return [Analysis(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Database error during select all excluing target wells: {e}") from e
        finally:
            cursor.close()

    def select_where_target_well_spacing_gun_barrel_plot_flag_is_true(self) -> list[Analysis]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_ANALYSIS_WHERE_TARGET_WELL_SPACING_GUN_BARREL_PLOT_FLAG_IS_TRUE.value)
            rows = cursor.fetchall()
            return [Analysis(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Database error during select where target well spacing gun barrel plot flag of true: {e}") from e
        finally:
            cursor.close()

    def select_where_target_well_spacing_gun_barrel_plot_flag_is_true_zoomed(self) -> list[Analysis]:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_ANALYSIS_WHERE_TARGET_WELL_SPACING_GUN_BARREL_PLOT_FLAG_IS_TRUE_ZOOMED.value)
            rows = cursor.fetchall()
            return [Analysis(*row) for row in rows]
        except DatabaseError as e:
            raise ValueError(f"Database error during select where target well spacing gun barrel plot flag of true: {e}") from e
        finally:
            cursor.close()

    def select_by_api(self, api: str) -> Analysis:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_ANALYSIS_BY_API.value, (api,))
            row = cursor.fetchone()
            if row:
                return Analysis(*row)
            else:
                return None
        except DatabaseError as e:
            raise ValueError(
                f"Database error during select_by_api for API {api}: {e}"
            ) from e
        finally:
            cursor.close()

    def select_simulated_well(self) -> Analysis:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_ANALYSIS_BY_SIMULATED_WELL.value)
            row = cursor.fetchone()
            if row:
                return Analysis(*row)
            else:
                return None
        except DatabaseError as e:
            raise ValueError(
                f"Database error during select simuated well: {e}"
            ) from e
        finally:
            cursor.close()

    def select_by_name(self, name: str) -> Analysis:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_ANALYSIS_BY_NAME.value, (name,))
            row = cursor.fetchone()
            if row:
                return Analysis(*row)
            else:
                return None
        except DatabaseError as e:
            raise ValueError(
                f"Database error during select_by_name for name {name}: {e}"
            ) from e
        finally:
            cursor.close()

    def get_shallowest(self) -> int:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_ANALYSIS_SHALLOWEST.value)
            row = cursor.fetchone()
            if row:
                return int(*row)
        except DatabaseError as e:
            raise ValueError(f"Unable to get analysis shallowest well{e}")
        finally:
            cursor.close()

    def get_deepest(self) -> int:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_ANALYSIS_DEEPEST.value)
            row = cursor.fetchone()
            if row:
                return int(*row)
        except DatabaseError as e:
            raise ValueError(f"Unable to get analysis deepest well{e}")
        finally:
            cursor.close()

    def get_group_avg_cumoil_bbl_per_ft(self, group_id: str) -> int:
        try:
            cursor = Cursor(self.connection)
            cursor.execute(AFEDB.SQL.SELECT_ANALYSIS_AVG_GROUP_CUMOIL_PER_FT.value, (group_id,))
            row = cursor.fetchone()
            if row:
                return int(*row)
        except DatabaseError as e:
            raise ValueError(f"Unable to get analysis group average cumoil bbl per ft{e}")
        finally:
            cursor.close()