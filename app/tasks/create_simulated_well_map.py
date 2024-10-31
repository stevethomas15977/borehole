from tasks.task import Task
from tasks.task_enum import TASKS
from helpers import task_logger
from traceback import format_exc
from folium import LayerControl, Element, PolyLine, CircleMarker, Map
import os

from services import (WellService, 
                      SurveyService, 
                      TexasLandSurveySystemService,
                      NewMexicoLandSurveySystemService,
                      TargetWellInformationService,
                      AnalysisService)

from helpers import (well_determine_center_map, 
                     create_map, 
                     new_mexico_plss_overlay, 
                     texas_plss_abstracts_overlay,
                     texas_plss_block_section_overlay, 
                     draw_wells, 
                     draw_well_legend,
                     draw_section_lines)

class CreateSimulatedWellMap(Task):

    def execute(self):
        task = TASKS.CREATE_SIMULATED_WELL_MAP.value
        logger = task_logger(task, self.context.logs_path)
        try:
            tlss_service = TexasLandSurveySystemService(self.context._texas_land_survey_system_database_path)
            nmlss_service = NewMexicoLandSurveySystemService(self.context._new_mexico_land_survey_system_database_path)
            target_well_information_service = TargetWellInformationService(self.context.db_path)
            analysis_service = AnalysisService(self.context.db_path)

            # Create the map
            target_well = target_well_information_service.get_first_row()
            map = Map(location=[target_well.latitude_surface_location, target_well.longitude_surface_location], zoom_start=12, tiles='OpenStreetMap')

            if target_well.state == "TX":
                # texas_plss_abstracts_overlay(context=self.context, counties=['loving', 'winkler', 'ward', 'reeves'], map=map) 
                tlss = tlss_service.get_by_county_abstract(county=target_well.county, abstract=target_well.tx_abstract_southwest_corner)
                fips_codes = []
                fips_codes.append(tlss.fips_code)
                texas_plss_block_section_overlay(context=self.context, fip_codes=fips_codes, map=map)
            elif target_well.state == "NM":
                # new_mexico_plss_overlay(context=self.context, file_prefixes=["23S", "24S", "25S", "26S"], map=map)
                township = int(target_well.nw_township_southwest_corner[:-1])
                township_direction = target_well.nw_township_southwest_corner[-1]
                range = int(target_well.nm_range_southwest_corner[:-1])
                range_direction = target_well.nm_range_southwest_corner[-1]
                section = int(target_well.nm_tx_section_southwest_corner)
                nmlss = nmlss_service.get_by_township_range_section(township=township, township_direction=township_direction, range=range, range_direction=range_direction, section=section)
                # new_mexico_plss_overlay(context=self.context, file_prefixes=["23S", "24S", "25S", "26S"], map=map)
                file_prefixes = []
                file_prefixes.append(target_well.nw_township_southwest_corner)
                file_prefixes.append(f"{int(township)-3}{township_direction}")
                file_prefixes.append(f"{int(township)-2}{township_direction}")
                file_prefixes.append(f"{int(township)-1}{township_direction}")
                file_prefixes.append(f"{int(township)+1}{township_direction}")
                file_prefixes.append(f"{int(township)+2}{township_direction}")
                file_prefixes.append(f"{int(township)+3}{township_direction}")
                new_mexico_plss_overlay(context=self.context, file_prefixes=file_prefixes, map=map)

            LayerControl().add_to(map)

            # Draw simulated well lines
            simulated_well = analysis_service.get_simluated_well()  
            start = (simulated_well.lateral_start_latitude, simulated_well.lateral_start_longitude)
            end = (simulated_well.lateral_end_latitude, simulated_well.lateral_end_longitude)
            PolyLine([start, end], color="blue", weight=3.0, tooltip=f"{simulated_well.name}").add_to(map)
           
            CircleMarker(location=start, radius=5, color='green', fill=True, fill_color='green', fill_opacity=1.0, tooltip=f"Start Lateral").add_to(map)
            CircleMarker(location=end, radius=5, color='black', fill=True, fill_color='black', fill_opacity=1.0, tooltip=f"End Lateral").add_to(map)

            #Draw the target wells
            target_wells = analysis_service.get_simulated_target_wells()
            for target_well in target_wells:
                start = (float(target_well.lateral_start_latitude), float(target_well.lateral_start_longitude))
                end = (float(target_well.lateral_end_latitude), float(target_well.lateral_end_longitude))
                PolyLine([start, end], color="orange", weight=2.0, tooltip=f"{target_well.name}").add_to(map)

            # Save the map
            output_file = os.path.join(self.context.logs_path, f"{self.context.project}-simulated-well-map-{self.context.version}.html")
            map.save(output_file) 
            
            logger.info(f"{task}: {self.context.logs_path}")
        except Exception as e:
            logger.error(f"Error {task} workflow task: {e}\n{format_exc()}")
            raise ValueError(f"Error {task} workflow task: {e}")