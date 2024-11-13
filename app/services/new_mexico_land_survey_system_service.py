from models import NewMexicoLandSurveySystem, NewMexicoLandSurveySystemRepository


class NewMexicoLandSurveySystemService:
    def __init__(self, db_path=None):
        self.repository = NewMexicoLandSurveySystemRepository(db_path=db_path)

    def get_by_township_range_section(self, township: int, township_direction: str, range: int, range_direction, section: int) -> NewMexicoLandSurveySystem:
        return self.repository.get_by_township_range_section(township=township, township_direction=township_direction, range=range, range_direction=range_direction, section=section)


    