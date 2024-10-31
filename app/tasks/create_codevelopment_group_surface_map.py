from tasks.task import Task
from tasks.task_enum import TASKS
from helpers import task_logger
from traceback import format_exc
from folium import LayerControl, Element 
import os

from helpers import (determine_center_map, create_map, 
                     new_mexico_plss_overlay, 
                     texas_plss_abstracts_overlay, 
                     draw_codeveopment_wells, 
                     codevelopment_legend)
from services import (AnalysisService, 
                      WellService,
                      CodevelopmentService,
                      LatitudeLongitudeDistanceService,
                      WellGroupService,
                      WellGroupMemberService,
                      SurveyService,
                      ParentChildService)

class CreateCodevelopmentGroupSurfaceMap(Task):

    def execute(self):
        task = TASKS.CREATE_CODEVELOPMENT_GROUP_SURFACE_MAP.value
        logger = task_logger(task, self.context.logs_path)
        try:
            analysis_service = AnalysisService(db_path=self.context.db_path)
            well_service = WellService(db_path=self.context.db_path)
            codedevelopment_service = CodevelopmentService(db_path=self.context.db_path)
            distance_service = LatitudeLongitudeDistanceService(db_path=self.context.db_path)
            wellgroup_service = WellGroupService(db_path=self.context.db_path)
            wellgroupmember_service = WellGroupMemberService(db_path=self.context.db_path)
            survey_service = SurveyService(db_path=self.context.db_path)
            parentchild_service = ParentChildService(db_path=self.context.db_path)
            analyses = analysis_service.get()

            # Create the map
            avg_lat, avg_long = determine_center_map(analyses)
            map = create_map(context=self.context, avg_lat=avg_lat, avg_long=avg_long)   

            # Apply the GeoJSON overlays
            new_mexico_plss_overlay(context=self.context, file_prefixes=["23S", "24S", "25S", "26S"], map=map)
            texas_plss_abstracts_overlay(context=self.context, counties=['loving', 'winkler', 'ward', 'reeves'], map=map) 
            LayerControl().add_to(map)

            # Draw the well lines
            draw_codeveopment_wells(self.context, 
                                    analyses, 
                                    codedevelopment_service, 
                                    wellgroup_service, 
                                    distance_service,
                                    analysis_service, 
                                    parentchild_service, 
                                    survey_service, 
                                    map)
            
            # Apply the legend
            legend = codevelopment_legend(context=self.context, 
                                        analysis_service=analysis_service, 
                                        well_service=well_service,
                                        wellgroup_service=wellgroup_service,
                                        wellgroupmember_service=wellgroupmember_service)
            map.get_root().html.add_child(Element(legend))

            # Save the map
            output_file = os.path.join(self.context.logs_path, f"{self.context.project}-codevelopment-group-surface-map-{self.context.version}.html")
            map.save(output_file) 
            
            logger.info(f"{task}: {self.context.logs_path}")
        except Exception as e:
            logger.error(f"Error {task} workflow task: {e}\n{format_exc()}")
            raise ValueError(f"Error {task} workflow task: {e}")