from models import XYZDistance
from models import XYZDistanceRepository

class XYZDistanceService:
    def __init__(self, db_path):
        self.db_path = db_path
        self.xyzdistance_repository = XYZDistanceRepository(db_path)

    def add_many(self, xyzdistance_list: list[XYZDistance]):
        self.xyzdistance_repository.inserts(xyzdistance_list)

    def get_by_simulated_well(self) -> list[XYZDistance]:
        return self.xyzdistance_repository.get_by_simulated_well()
    
    def get_by_reference_well(self, reference_well_api: str) -> list[XYZDistance]:
        return self.xyzdistance_repository.get_by_reference_well(reference_well_api=reference_well_api)
    
    def get_by_target_well(self, target_well_api: str) -> list[XYZDistance]:
        return self.xyzdistance_repository.get_by_target_well(target_well_api=target_well_api)
    
    def get_for_simulated_target_well(self, target_well_api: str) -> list[XYZDistance]:
        return self.xyzdistance_repository.get_for_simulated_target_well(target_well_api=target_well_api)  
    
    def get_by_reference_target_well(self, reference_well_api: str, target_well_api: str) -> XYZDistance:
        return self.xyzdistance_repository.get_by_reference_target_well(reference_well_api=reference_well_api, target_well_api=target_well_api)
    