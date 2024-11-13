from services.analysis_service import AnalysisService
from tasks.task import Task
from tasks.task_enum import TASKS
from helpers import task_logger, spc_feet_to_latlon
from traceback import format_exc    
from folium import PolyLine, Element, LayerControl
import os

from services import (WellService, 
                      SurveyService, 
                      TexasLandSurveySystemService,
                      NewMexicoLandSurveySystemService,
                      TargetWellInformationService, 
                      WellService,
                      GunBarrelService)

from helpers import (create_map, 
                     new_mexico_plss_overlay, 
                     texas_plss_block_section_overlay, 
                     draw_wells, 
                     draw_well_legend,
                     draw_section_lines,
                     well_tooltip)

class CreateGunBarrelSurfaceMap(Task):

    def execute(self):
        task = TASKS.CREATE_GUN_BARREL_SURFACE_MAP.value
        logger = task_logger(task, self.context.logs_path)
        try:
            analysis_service = AnalysisService(db_path=self.context.db_path)
            well_service = WellService(db_path=self.context.db_path)
            survey_service = SurveyService(db_path=self.context.db_path)
            tlss_service = TexasLandSurveySystemService(self.context._texas_land_survey_system_database_path)
            nmlss_service = NewMexicoLandSurveySystemService(self.context._new_mexico_land_survey_system_database_path)
            target_well_information_service = TargetWellInformationService(self.context.db_path)
            gun_barrel_service = GunBarrelService(self.context.db_path)

            # Create the map
            map = None
            target_well = target_well_information_service.get_first_row()

            if target_well.state == "TX":
                # texas_plss_abstracts_overlay(context=self.context, counties=['loving', 'winkler', 'ward', 'reeves'], map=map) 
                tlss = tlss_service.get_by_county_abstract(county=target_well.county, abstract=target_well.tx_abstract_southwest_corner)
                fips_codes = []
                fips_codes.append(tlss.fips_code)
                map = create_map(context=self.context, avg_lat=tlss.southwest_latitude, avg_long=tlss.southwest_longitude, zoom_level=13.5)
                texas_plss_block_section_overlay(context=self.context, fip_codes=fips_codes, map=map)
            elif target_well.state == "NM":
                township = int(target_well.nw_township_southwest_corner[:-1])
                township_direction = target_well.nw_township_southwest_corner[-1]
                range = int(target_well.nm_range_southwest_corner[:-1])
                range_direction = target_well.nm_range_southwest_corner[-1]
                section = int(target_well.nm_tx_section_southwest_corner)
                nmlss = nmlss_service.get_by_township_range_section(township=township, township_direction=township_direction, range=range, range_direction=range_direction, section=section)
                map = create_map(context=self.context, avg_lat=nmlss.southwest_latitude, avg_long=nmlss.southwest_longitude, zoom_level=13.5)
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

            coordinates = {}
            # Draw the section lines
            if target_well.state == "TX":
                coordinates['southwest_latitude'] = tlss.southwest_latitude
                coordinates['southwest_longitude'] = tlss.southwest_longitude
                coordinates['northwest_latitude'] = tlss.northeast_latitude
                coordinates['northwest_longitude'] = tlss.northeast_longitude
                tooltip = f"SW Corner {tlss.abstract}-{tlss.block}-{str(int(tlss.section))}"
                draw_section_lines(coordinates=coordinates, tooltip=tooltip, map=map)
            elif target_well.state == "NM":
                coordinates['southwest_latitude'] = nmlss.southwest_latitude
                coordinates['southwest_longitude'] = nmlss.southwest_longitude
                coordinates['northwest_latitude'] = nmlss.northeast_latitude
                coordinates['northwest_longitude'] = nmlss.northeast_longitude
                tooltip = f"SW Corner {nmlss.township}-{nmlss.range}-{str(int(nmlss.section))}"
                draw_section_lines(coordinates=coordinates, tooltip=tooltip, map=map)

            #Draw the target wells
            target_wells = analysis_service.get_simulated_target_wells()
            for target_well in target_wells:
                start = (float(target_well.lateral_start_latitude), float(target_well.lateral_start_longitude))
                end = (float(target_well.lateral_end_latitude), float(target_well.lateral_end_longitude))
                PolyLine([start, end], color="orange", weight=2.0, tooltip=f"{target_well.name}").add_to(map)
            wells = target_wells

            # Draw simulated well lines
            simulated_well = analysis_service.get_simluated_well()  
            start = (simulated_well.lateral_start_latitude, simulated_well.lateral_start_longitude)
            end = (simulated_well.lateral_end_latitude, simulated_well.lateral_end_longitude)
            PolyLine([start, end], color="blue", weight=3.0, tooltip=f"{simulated_well.name}").add_to(map)

            # Draw the offset well lines
            for gun_barrel_well in gun_barrel_service.select_all():
                well = analysis_service.get_by_api(api=gun_barrel_well.offset_well_api)
                wells.append(well)
                tooltip_html = well_tooltip(well=well_service.get_by_api(api=well.api))
                surveys = survey_service.get_by_api(api=well.api)
                if len(surveys) == 0:
                    start = (well._lateral_start_latitude, well.lateral_start_longitude)
                    end = (well.lateral_end_latitude, well.lateral_end_longitude)
                    PolyLine([start, end], color="blue", weight=2.0, tooltip=f"{well.name}").add_to(map)
                    # Marker(location=start, icon=icon_circle(color='black', border_width=4)).add_to(map)
                else:
                    for index, survey in enumerate(surveys):
                        if index == 0:
                            start = (survey.latitude, survey.longitude)
                            end = (survey.latitude, survey.longitude)
                            PolyLine([start, end], color="green", weight=2.0, tooltip=tooltip_html).add_to(map)
                            # Marker(location=start, icon=icon_circle(color='black', border_width=4)).add_to(map)
                        else:
                            start = (surveys[index - 1].latitude, surveys[index - 1].longitude)
                            end = (survey.latitude, survey.longitude)
                            PolyLine([start, end], color="green", weight=2.0, tooltip=tooltip_html).add_to(map)
            
            # Draw the legend
            legend_html = ""
            legend_html += f"""<div style="position: fixed; top: 80px; left: 10px; width: 350px; border: 2px solid grey; z-index: 9999; overflow-y: auto; overflow-x: auto; max-height: 80%; background-color: #D3D3D3; opacity: 0.9; padding: 5px;">"""
            legend_html += f""" <div style="text-align: center; font-size: 14px;"><b>{self.context.project.capitalize()}</b></div>"""
            legend_html += f""" <div style="text-align: center; font-size: 12px;">Target Well Distances</div>"""
            legend_html += f""" <div style="text-align: center; font-size: 10px;">Version {self.context.version}</div>"""
            legend_html += f""" <div style="margin-right: 10px;">"""
            for offset in wells:
                if "11-111" in offset.api:
                    continue
                well = well_service.get_by_api(api=offset.api)
                legend_html += f"""  <div style="margin-right: 5px;">"""
                legend_html += f"""   <span style='font-size:12px'><b>{well.name}</b></span>"""
                legend_html += f"""   <br>"""
                legend_html += f"""   <div style="margin-right: 5px;">"""
                legend_html += f"""      &nbsp;&nbsp&nbsp;&nbsp&nbsp;&nbsp<span style='font-size:10px'>{well.interval}</span><br>"""
                if well.state == "NM":
                    legend_html += f"""      &nbsp;&nbsp&nbsp;&nbsp&nbsp;&nbsp<span style='font-size:10px'>{well.county} {well.township} {well.section}</span>"""
                elif well.state == "TX":
                    legend_html += f"""      &nbsp;&nbsp&nbsp;&nbsp&nbsp;&nbsp<span style='font-size:10px'>{well.county} {well.abstract}</span>"""
                legend_html += f"""   </div>"""  
                legend_html += f"""  </div>"""           
            legend_html += f""" </div>"""
            legend_html += f"""</div>"""
            
            map.get_root().html.add_child(Element(legend_html))

            # Save the map
            output_file = os.path.join(self.context.logs_path, f"{self.context.project}-gun-barrel-surface-map-{self.context.version}.html")
            map.save(output_file) 
            
            logger.info(f"{task}: {self.context.logs_path}")
        except Exception as e:
            logger.error(f"Error {task} workflow task: {e}\n{format_exc()}")
            raise ValueError(f"Error {task} workflow task: {e}")