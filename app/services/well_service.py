from models import Well, WellRepository


class WellService:
    def __init__(self, db_path=None):
        self.repository = WellRepository(db_path=db_path)

    def add(self, wells: list[Well]):
        self.repository.insert(wells)

    def get_all(self) -> list[Well]:
        return self.repository.get()

    def get_by_api(self, api) -> Well:
        return self.repository.get_by_api(api)
    
    def get_by_name(self, name) -> Well:
        return self.repository.get_by_name(name)
    
    def get_distinct_states(self) -> list[str]:
        return self.repository.get_distinct_states()
    
    def get_distinct_texas_abstracts(self) -> list[str]:
        return self.repository.get_distinct_texas_abstracts()
    
    def get_wells_by_texas_abstract(self, texas_abstract) -> list[Well]:
        return self.repository.get_wells_by_texas_abstract(texas_abstract)
