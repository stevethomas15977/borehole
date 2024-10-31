from models import TargetWellInformation, TargetWellInformationRepository


class TargetWellInformationService:
    def __init__(self, db_path=None):
        self.repository = TargetWellInformationRepository(db_path=db_path)

    def update(self, target_well: TargetWellInformation):
        self.repository.update(target_well)
        
    def get_first_row(self) -> TargetWellInformation:
        return self.repository.get_first_row()
    
    def get_all(self) -> list[TargetWellInformation]:
        return self.repository.get()

    def get_by_api(self, api) -> TargetWellInformation:
        return self.repository.get_by_api(api)
    
    def get_by_name(self, name) -> TargetWellInformation:
        return self.repository.get_by_name(name)
    
    def get_distinct_states(self) -> list[str]:
        return self.repository.get_distinct_states()
    
    def get_distinct_texas_abstracts(self) -> list[str]:
        return self.repository.get_distinct_texas_abstracts()
    
    def get_by_texas_abstract(self, texas_abstract) -> list[TargetWellInformation]:
        return self.repository.get_by_texas_abstract(texas_abstract)
    
    def get_shallowest(self) -> int:
        return self.repository.get_shallowest()
    
    def get_deepest(self) -> int:
        return self.repository.get_deepest()
    
    def get_max_lateral_length(self) -> int:
        return self.repository.get_max_lateral_length()
