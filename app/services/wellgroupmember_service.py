from models import WellGroupMember, WellGroupMemberRepository


class WellGroupMemberService:
    def __init__(self, db_path=None):
        self.repository = WellGroupMemberRepository(db_path=db_path)

    def add(self, wellgroupmember: WellGroupMember) -> None:
        self.repository.insert(wellgroupmember=wellgroupmember)

    def get_all(self) -> list[WellGroupMember]:
        return self.repository.get_all()

    def get_all_group_name(self, group_name: str) -> list[WellGroupMember]:
        return self.repository.get_all_group_name(group_name)

    def get_by_group_name_well_api(self, group_name: str, well_api: str) -> WellGroupMember:
        return self.repository.get_by_group_name_well_api(group_name=group_name, well_api=well_api)