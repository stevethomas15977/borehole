from models import Codevelopment, CodevelopmentRepository


class CodevelopmentService:
    def __init__(self, db_path=None):
        self.repository = CodevelopmentRepository(db_path=db_path)

    def add(self, codevelopment: list[Codevelopment]):
        self.repository.insert(codevelopment)

    def get_all(self) -> list[Codevelopment]:
        return self.repository.get_all()
    
    def get_by_reference_api(self, reference_api: str) -> list[Codevelopment]:
        return self.repository.get_by_reference_api(reference_api=reference_api)