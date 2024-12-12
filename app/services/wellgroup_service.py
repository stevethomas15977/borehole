from models import WellGroup, WellGroupRepository


class WellGroupService:
    def __init__(self, db_path=None):
        self.repository = WellGroupRepository(db_path=db_path)

    def add(self, wellgroup: WellGroup) -> None:
        self.repository.insert(wellgroup=wellgroup)

    def update(self, wellgroup: WellGroup) -> None:
        self.repository.update(wellgroup=wellgroup)
        
    def get_all(self) -> list[WellGroup]:
        return self.repository.get_all()

    def get_by_name(self, name: str) -> WellGroup:
        return self.repository.get_by_name(name=name)