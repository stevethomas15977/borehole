
from models import Overlap, OverlapRepository


class OverlapService:
    def __init__(self, db_path=None):
        self.repository = OverlapRepository(db_path=db_path)

    def insert(self, overlap: Overlap):
        self.repository.insert(overlap=overlap)

    def get_by_reference_api_target_api(self, reference_api: str, target_api: str) -> Overlap:
        return self.repository.get_by_reference_api_target_api(reference_api=reference_api, target_api=target_api)
