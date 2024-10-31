from models import Attribute, AttributeRepository


class AttributeService:
    def __init__(self, db_path=None):
        self.repository = AttributeRepository(db_path=db_path)

    def add(self, codevelopment: list[Attribute]):
        self.repository.insert(codevelopment)
    
    def get_by_name(self, name: str) -> list[Attribute]:
        return self.repository.get_by_name(name=name)

    def get_distinct_groups(self) -> list[int]:
        return self.repository.get_distinct_groups()

    def get_names_by_group(self, group: str) -> list[str]:
        return self.repository.get_names_by_group(group=group)  