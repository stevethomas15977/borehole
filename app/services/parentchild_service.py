from models import ParentChild, ParentChildRepository


class ParentChildService:
    def __init__(self, db_path=None):
        self.repository = ParentChildRepository(db_path=db_path)

    def add(self, parrentchildren: list[ParentChild]) -> None:
        self.repository.insert(parrentchildren)

    def get_by_parent_api(self, parent_api: str) -> list[ParentChild]:
        return self.repository.get_by_parent_api(parent_api=parent_api)
    
    def get_by_child_api(self, child_api: str) -> list[ParentChild]:
        return self.repository.get_by_child_api(child_api=child_api)

    def get_by_child_api_adjacent(self, child_api: str, adjacent: str) -> list[ParentChild]:
        return self.repository.get_by_child_api_adjacent(child_api=child_api, adjacent=adjacent)

    