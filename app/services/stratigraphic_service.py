
from models import Stratigraphic, StratigraphicRepository


class StratigraphicService:
    def __init__(self, db_path=None):
        self.repository = StratigraphicRepository(db_path=db_path)

    def get_by_union_code(self, union_code) -> Stratigraphic:
        return self.repository.get_by_union_code(union_code=union_code)
    
    def get_by_union_code_list(self, union_code_list: str) -> list[Stratigraphic]:
        return self.repository.get_by_union_code_list(union_code_list=union_code_list)
    
    def get_by_prism_code(self, prism_code) -> Stratigraphic:
        return self.repository.get_by_prism_code(prism_code=prism_code)
    
    def get_union_codes(self) -> list[str]:
        return self.repository.get_union_codes()

