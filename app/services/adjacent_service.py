
from models import Adjacent, AdjacentRepository


class AdjacentService:
    def __init__(self, db_path=None):
        self.repository = AdjacentRepository(db_path=db_path)

    def add(self, adjacent_list: list[Adjacent]):
        self.repository.insert(adjacent_list=adjacent_list)

    def add_one(self, adjacent: Adjacent):
        self.repository.insert_one(adjacent=adjacent)

    def get_all(self) -> list[Adjacent]:
        return self.repository.get_all()
    
    def get_by_reference_api_west(self, reference_api: str) -> list[Adjacent]:
        return self.repository.get_by_reference_api_west(reference_api=reference_api)   
    
    def get_by_reference_api_east(self, reference_api: str) -> list[Adjacent]:
        return self.repository.get_by_reference_api_east(reference_api=reference_api)   
    
    def get_by_reference_api_north(self, reference_api: str) -> list[Adjacent]:
        return self.repository.get_by_reference_api_north(reference_api=reference_api)   
    
    def get_by_reference_api_south(self, reference_api: str) -> list[Adjacent]:
        return self.repository.get_by_reference_api_south(reference_api=reference_api)   

    def get_by_apis(self, reference_api: str, target_api: str) -> Adjacent:
        return self.repository.get_by_apis(reference_api=reference_api, target_api=target_api)   
    
    def get_list_by_reference_apis(self, reference_apis: list[str]) -> list[Adjacent]:
        return self.repository.get_list_by_reference_apis(reference_apis=reference_apis)   

    def delete(self, reference_api: str, target_api: str):
        return self.repository.delete(reference_api=reference_api, target_api=target_api)

    
