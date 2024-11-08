from context import Context
from tasks.task_enum import TASKS
from tasks.task_factory import TaskFactory
from tasks.workflow_group import WorkflowGroup
from helpers import write_to_file
import os

class WorkflowManager:
    def __init__(self, context: Context=None):
        self._context = context
        self._factory = TaskFactory(self._context)
        write_to_file(os.path.join(self.context.project_path, f"RUNNING"),f"Running")

    def __del__(self):
        running_file = os.path.join(self.context.project_path, f"RUNNING")
        if os.path.exists(running_file):
            os.remove(running_file)
        write_to_file(os.path.join(self.context.project_path, f"COMPLETED"),f"Completed")

    def project_initiation_workflow(self):
        workgroup = WorkflowGroup("AFE Project Initiation Workflow", self._context, self._factory)
        workgroup.add_task(TASKS.CREATE_DATABASE.value)
        workgroup.add_task(TASKS.LOAD_LOOKUP_TABLES.value)
        if self._context.target_well_information_file:
            workgroup.add_task(TASKS.VALIDATE_TARGET_WELL_INFORMATION.value)
            
        workgroup.run()

    def base_workflow(self):
        workgroup = WorkflowGroup("AFE Base Workflow", self._context, self._factory)
        workgroup.add_task(TASKS.LOAD_WELL_DATA.value)
        workgroup.add_task(TASKS.LOAD_SURVEY_DATA.value)
        workgroup.add_task(TASKS.ETL_WELL.value)
        if self._context.target_well_information_file:
            workgroup.add_task(TASKS.LOAD_TARGET_WELL_INFORMATION.value)
            workgroup.add_task(TASKS.ETL_TARGET_WELL_INFORMATION.value)
            workgroup.add_task(TASKS.CREATE_TARGET_WELL_ANALYSIS.value)
            workgroup.add_task(TASKS.CREATE_SIMULATED_WELL.value)
        workgroup.add_task(TASKS.CALCULATE_XYZ_DISTANCE.value)
        workgroup.add_task(TASKS.CALCULATE_LATITUDE_LONGITUDE_DISTANCE.value)
        workgroup.run()

    def offset_well_identification_workflow(self):
        workgroup = WorkflowGroup("Offset Well Identification Workflow", self._context, self._factory)
        workgroup.add_task(TASKS.OFFSET_WELL_IDENTIFICATION_WORKFLOW_DATABASE_MANAGEMENT.value)
        workgroup.add_task(TASKS.DETERMINE_ADJACENT_WELLS.value)
        workgroup.add_task(TASKS.DETERMINE_CODEVELOPMENT_WELLS.value)
        workgroup.add_task(TASKS.DETERMINE_WELL_GROUPING.value)
        workgroup.add_task(TASKS.CALCULATE_WELL_AVERAGE_SPACING.value)
        workgroup.add_task(TASKS.CALCULATE_WELL_GROUP_AVERAGE_SPACING.value)
        workgroup.add_task(TASKS.DETERMINE_PARENT_CHILD_WELLS.value)
        workgroup.add_task(TASKS.DETERMINE_BOUNDED_WELLS.value)
        workgroup.add_task(TASKS.CREATE_OFFSET_WELL_IDENTIFICATION_EXCEL.value)
        workgroup.run()

    def gun_barrel_workflow(self):
        workgroup = WorkflowGroup("Well Spacing Gun Barrel Plot Workflow", self._context, self._factory)
        workgroup.add_task(TASKS.GUN_BARREL_PLOT_WORKFLOW_DATABASE_MANAGEMENT.value)
        workgroup.add_task(TASKS.DETERMINE_WELL_SPACING_GUN_BARREL_PLOT_WELLS.value)
        workgroup.add_task(TASKS.CALCULATE_WELL_OVERLAP_PERCENTAGE.value)
        workgroup.add_task(TASKS.ENRICH_GUN_BARREL.value)
        workgroup.add_task(TASKS.CREATE_GUN_BARREL_PLOT.value)
        workgroup.add_task(TASKS.CREATE_CROSS_PLOT.value)

        # workgroup.add_task(TASKS.CREATE_CHILD_WELL_RISK_GUN_BARREL_PLOT_3D.value)
        
        if self._context.target_well_information_file:
            workgroup.run()

    @property
    def context(self):
        return self._context
    
    @context.setter
    def context(self, context: Context):
        self._context = context
        self._factory = TaskFactory(self._context)

if __name__ == "__main__":
    context = Context().dragonfly_5_mile()
    workflow_manager = WorkflowManager(context)
    workflow_manager.project_initiation_workflow()
    workflow_manager.base_workflow()
    workflow_manager.offset_well_identification_workflow()
    workflow_manager.gun_barrel_workflow()
