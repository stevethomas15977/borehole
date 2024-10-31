from models import LatitudeLongitudeDistance
from models import LatitudeLongitudeDistanceRepository

class LatitudeLongitudeDistanceService:
    def __init__(self, db_path):
        self.db_path = db_path
        self.respository = LatitudeLongitudeDistanceRepository(db_path)

    def add_many(self, latitudelongitudedistance_list: list[LatitudeLongitudeDistance]):
        self.respository.inserts(latitudelongitudedistance_list)

    def get(self):
        return self.respository.get()
    
    def get_by_reference_api(self, reference_api: str) -> list[LatitudeLongitudeDistance]:
        return self.respository.get_by_reference_api(reference_api)
    
    def get_by_reference_target_apis(self, reference_api: str, target_api: str) -> LatitudeLongitudeDistance:
        return self.respository.get_by_reference_target_apis(reference_api, target_api)