from models import GunBarrel, GunBarrelRepository


class GunBarrelService:
    def __init__(self, db_path=None):
        self.repository = GunBarrelRepository(db_path=db_path)

    def insert(self, gun_barrel: GunBarrel) -> None:    
        self.repository.insert(gun_barrel=gun_barrel)

    def select_all(self) -> list[GunBarrel]:
        return self.repository.select_all()
    
    def select_by_target_well_api(self, target_well_api: str) -> list[GunBarrel]:
        return self.repository.select_by_target_well_api(target_well_api=target_well_api)
    
    def select_by_target_offset_well_api(self, target_well_api: str, offset_well_api: str) -> GunBarrel:
        return self.repository.select_by_target_offset_well_api(target_well_api=target_well_api, offset_well_api=offset_well_api)

    def update(self, gun_barrel: GunBarrel) -> None:
        self.repository.update(gun_barrel)