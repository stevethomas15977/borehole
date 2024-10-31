from models import Survey, SurveyRepository


class SurveyService:

    def __init__(self, db_path=None):
        self.repository = SurveyRepository(db_path=db_path)

    def add(self, surveys: list[Survey]):
        self.repository.insert(surveys)

    def get_by_api(self, api: str) -> list[Survey]:
        return self.repository.get_by_api(api)
    
    def get_unique_api_values(self) -> list[str]:
        return self.repository.get_unique_api_values()   
