from models import Analysis, AnalysisRepository


class AnalysisService:
    def __init__(self, db_path=None):
        self.repository = AnalysisRepository(db_path=db_path)

    def add_list(self, analyses: list[Analysis]):
        self.repository.insert_list(analyses)

    def add(self, analysis: Analysis):
        self.repository.insert(analysis)

    def update(self, analysis: Analysis):
        self.repository.update(analysis)

    def get_all(self) -> list[Analysis]:
        return self.repository.select_all()
    
    def get_all_excluding_target_wells(self) -> list[Analysis]:
        return self.repository.select_all_excluding_target_wells()
    
    def get(self) -> list[Analysis]:
        return self.repository.select_all()
    
    def get_by_api(self, api: str) -> Analysis:
        return self.repository.select_by_api(api)
    
    def get_by_name(self, name: str) -> Analysis:
        return self.repository.select_by_name(name)
    
    def select_where_target_well_spacing_gun_barrel_plot_flag_is_true(self) -> list[Analysis]:
        return self.repository.select_where_target_well_spacing_gun_barrel_plot_flag_is_true()
    
    def select_where_target_well_spacing_gun_barrel_plot_flag_is_true_zoomed(self) -> list[Analysis]:
        return self.repository.select_where_target_well_spacing_gun_barrel_plot_flag_is_true_zoomed()

    def reset_target_well_spacing_gun_barrel_plot_flag(self):
        return self.repository.reset_target_well_spacing_gun_barrel_plot_flag()
    
    def get_simluated_well(self) -> Analysis:
        return self.repository.select_simulated_well()

    def get_simulated_target_wells(self) -> Analysis:
        return self.repository.select_simulated_target_wells()
    
    def get_shallowest(self) -> int:
        return self.repository.get_shallowest()
    
    def get_deepest(self) -> int:
        return self.repository.get_deepest()
    
    def get_group_avg_cumoil_bbl_per_ft(self, group_id: str) -> int:
        return self.repository.get_group_avg_cumoil_bbl_per_ft(group_id)