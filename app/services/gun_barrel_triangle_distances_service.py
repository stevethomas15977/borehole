from models import GunBarrelTriangleDistances, GunBarrelTriangleDistancesRepository

class GunBarrelTriangleDistancesService:
    def __init__(self, db_path=None):
        self.repository = GunBarrelTriangleDistancesRepository(db_path=db_path)

    def insert(self, gun_barrel_triangle_distances: GunBarrelTriangleDistances) -> None:    
        self.repository.insert(gun_barrel_triangle_distances=gun_barrel_triangle_distances)

    def select_all(self) -> list[GunBarrelTriangleDistances]:
        return self.repository.select_all()

    def select_by_target_api(self, target_well_api: str) -> list[GunBarrelTriangleDistances]:
        return self.repository.select_by_target_api(target_well_api=target_well_api)

    def select_by_target_offset_api(self, target_well_api: str, offset_well_api: str) -> GunBarrelTriangleDistances:
        return self.repository.select_by_target_offset_api(target_well_api=target_well_api, offset_well_api=offset_well_api)
