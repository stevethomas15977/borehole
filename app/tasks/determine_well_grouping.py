from tasks.task import Task
from tasks.task_enum import TASKS
from helpers import task_logger
from traceback import format_exc

from helpers import (identify_codevelopment_clusters, 
                     assign_colors_to_groups,
                     wordcloud_groupname)
from models import (WellGroup, 
                    WellGroupMember)
from services import (CodevelopmentService,
                      WellGroupMemberService, 
                      WellGroupService, 
                      WellService, 
                      AnalysisService)

class DetermineWellGrouping(Task):

    def execute(self):
        task = TASKS.DETERMINE_WELL_GROUPING.value
        logger = task_logger(task, self.context.logs_path)
        try:
            codevelopment_service = CodevelopmentService(db_path=self.context.db_path)
            well_service = WellService(db_path=self.context.db_path)
            analysis_service = AnalysisService(db_path=self.context.db_path)
            wellgroup_service = WellGroupService(db_path=self.context.db_path)
            wellgroupmember_service = WellGroupMemberService(db_path=self.context.db_path)
            codevelopments = codevelopment_service.get_all()
            codevelopment_api_groups = identify_codevelopment_clusters(codevelopments)
            colors = assign_colors_to_groups(codevelopment_api_groups)
            for index, group in enumerate(codevelopment_api_groups):
                leases = []
                for api in group:
                    well = well_service.get_by_api(api)
                    if well is None:
                        continue
                    leases.append(well.lease)
                group_name = f"{wordcloud_groupname(leases)} {index+1}"
                wellgroup = WellGroup(name=group_name, color=colors[index])
                wellgroup_lookup = wellgroup_service.get_by_name(group_name)
                if wellgroup_lookup is None:
                    wellgroup_service.add(wellgroup)
                for api in group:
                    well = well_service.get_by_api(api)
                    if well is None:
                        continue
                    wellgroupmember = WellGroupMember(group_name=group_name, 
                                                      well_api=well.api,
                                                      well_name=well.name)
                    if wellgroupmember_service.get_by_group_name_well_api(group_name, well.api) is None:
                        wellgroupmember_service.add(wellgroupmember)
                    analysis = analysis_service.get_by_api(api)
                    analysis.group_id = group_name
                    analysis_service.update(analysis)
            logger.info(f"{task}: {self.context.logs_path}")
        except Exception as e:
            logger.error(f"Error {task} workflow task: {e}\n{format_exc()}")
            raise ValueError(f"Error {task} workflow task: {e}")