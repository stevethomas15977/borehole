from models import TexasLandSurveySystem, TexasLandSurveySystemRepository


class TexasLandSurveySystemService:
    def __init__(self, db_path=None):
        self.repository = TexasLandSurveySystemRepository(db_path=db_path)

    def add(self, texas_land_survey_system_list: list[TexasLandSurveySystem]) -> None:
        self.repository.insert(texas_land_survey_system_list)

    def get_by_county_abstract(self, county: str, abstract: str) -> TexasLandSurveySystem:
        return self.repository.get_by_county_abstract(county=county, abstract=abstract)

    def get_by_county_abstract_block_section(self, county: str, abstract: str, block: str, section: str) -> TexasLandSurveySystem:
        return self.repository.get_by_county_abstract_block_section(county=county, abstract=abstract, block=block, section=section)


    