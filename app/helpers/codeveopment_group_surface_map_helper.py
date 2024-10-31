from folium import Map, PolyLine, Element, GeoJson, LayerControl, Marker, DivIcon, CircleMarker
from folium.plugins import BeautifyIcon
import json
import os
import geopandas as gpd

from context import Context

from models import (Analysis, Codevelopment, Well)

from services import (WellService, 
                      WellGroupService, 
                      WellGroupMemberService, 
                      CodevelopmentService, 
                      AnalysisService, 
                      ParentChildService, 
                      SurveyService,
                      LatitudeLongitudeDistanceService)

def codevelopment_tooltip(analysis: Analysis, 
                          codevelopment_list: list[Codevelopment], 
                          distance_service: LatitudeLongitudeDistanceService,
                          analysis_service: AnalysisService) -> str:
    
    html = f"<div style='text-align: left; font-size: 10px;'>"
    html += f"Name: {analysis.name}<br>"
    html += f"API: {analysis.api}<br>"
    html += f"1st Prod Date: {analysis.first_production_date}<br>"
    html += f"Lateral Length: {analysis.lateral_length} ft.<br>"
    html += f"Direction: {analysis.direction}<br>"
    
    for codevelopment in codevelopment_list:
        distance = distance_service.get_by_reference_target_apis(reference_api=analysis.api, target_api=codevelopment.target_api)
        codevelopment_analysis = analysis_service.get_by_api(api=codevelopment.target_api)
        html += f"Codevelopment: {codevelopment_analysis.name}<br>"
        if distance:
            if distance.end_latitude:
                if distance.end_latitude >= 0:
                    html += f"&nbspNorth: {distance.end_latitude} ft.<br>"
                else:
                    html += f"&nbspSouth: {abs(distance.end_latitude)} ft.<br>"
            if distance.end_longitude:
                if distance.end_longitude >= 0:
                    html += f"&nbspEast: {distance.end_longitude} ft.<br>"
                else:
                    html += f"&nbspWest: {abs(distance.end_longitude)} ft.<br>"
    html += f"</div>"
    return html

def codevelopment_legend(context: Context,
                         analysis_service: AnalysisService, 
                         well_service: WellService,
                         wellgroup_service: WellGroupService,
                         wellgroupmember_service: WellGroupMemberService) -> str:

    # Create the beginning of the HTML for the legend
    html = """
        <div style="position: fixed; 
                    top: 80px; 
                    left: 10px; 
                    width: 350px; 
                    border: 2px solid grey;
                    z-index: 9999; 
                    overflow-y: auto; 
                    overflow-x: auto;
                    max-height: 80%;
                    background-color: #D3D3D3; 
                    opacity: 0.9; 
                    padding: 5px;">
          """
    html += f""" <div style="text-align: center; font-size: 14px;"><b>{context.project.capitalize()}</b></div>"""
    html += f""" <div style="text-align: center; font-size: 12px;">Codevelopment Groups</div>"""
    html += f""" <div style="text-align: center; font-size: 10px;">Version {context.version}</div>"""
    html += f""" <div style="margin-right: 10px;">"""
    groups = wellgroup_service.get_all()
    for group in groups:
        html += f"""  <div style="margin-right: 5px;">"""
        html += f"   <span style='font-size:14px'><b>{group.name}</b></span><br>"
        for member in wellgroupmember_service.get_all_group_name(group_name=group.name):
            analysis = analysis_service.get_by_name(name=member.well_name)
            well = well_service.get_by_api(api=analysis.api)
            color = group.color
            if analysis.parents is not None:
                html += f"   &nbsp; <i class='fa fa-square' style='color:{color}'></i> &nbsp; <span style='font-size:12px'><b>{analysis.name}</b> (parent)</span>"
                html += f"""  <br>"""
                html += f"""  <div style="margin-right: 5px;">"""
                html += f"      &nbsp;&nbsp&nbsp;&nbsp&nbsp;&nbsp<span style='font-size:10px'>{well.interval}</span><br>"
                if well.state == "NM":
                    html += f"      &nbsp;&nbsp&nbsp;&nbsp&nbsp;&nbsp<span style='font-size:10px'>{well.county} {well.township} {well.section}</span>"
                elif well.state == "TX":
                    html += f"      &nbsp;&nbsp&nbsp;&nbsp&nbsp;&nbsp<span style='font-size:10px'>{well.county} {well.abstract}</span>"
                html += """   </div>"""            
            else:
                html += f"   &nbsp; <i class='fa fa-square' style='color:{color}'></i> &nbsp; <span style='font-size:12px'>{analysis.name}</span>"
                html += f"""  <br>"""
                html += f"""  <div style="margin-right: 5px;">"""
                html += f"      &nbsp;&nbsp&nbsp;&nbsp&nbsp;&nbsp<span style='font-size:10px'>{well.interval}</span><br>"
                if well.state == "NM":
                    html += f"      &nbsp;&nbsp&nbsp;&nbsp&nbsp;&nbsp<span style='font-size:10px'>{well.county} {well.township} {well.section}</span>"
                elif well.state == "TX":
                    html += f"      &nbsp;&nbsp&nbsp;&nbsp&nbsp;&nbsp<span style='font-size:10px'>{well.county} {well.abstract}</span>"
                html += """   </div>"""
        # html += f"""  <br>"""
        html += """  </div>"""
    html += """ </div>"""
    html += """</div>"""
    return html

def draw_codeveopment_wells(context: Context, 
                            analyses: list[Analysis], 
                            codedevelopment_service: CodevelopmentService,
                            wellgroup_service: WellGroupService,
                            distance_service: LatitudeLongitudeDistanceService,
                            analysis_service: AnalysisService,
                            parentchild_service: ParentChildService,
                            survey_service: SurveyService,
                            map: Map):
    
    for analysis in analyses:
        
        start = (analysis.lateral_start_latitude, analysis.lateral_start_longitude)
        end = (analysis.lateral_end_latitude, analysis.lateral_end_longitude)
        
        codevelopment_list = codedevelopment_service.get_by_reference_api(reference_api=analysis.api)
        
        group = wellgroup_service.get_by_name(name=analysis.group_id)
        
        if group is None:
            color = 'black'
        else:
            color = group.color
        
        tooltip_text = codevelopment_tooltip(analysis=analysis, 
                                             codevelopment_list=codevelopment_list, 
                                             distance_service=distance_service, 
                                             analysis_service=analysis_service)

        parentchild = parentchild_service.get_by_parent_api(parent_api=analysis.api)

        if parentchild is not None:
            weight = 2.5
        else:
            weight = 1.5

        surveys = survey_service.get_by_api(api=analysis.api)
        
        if surveys is None or len(surveys) <= 50 or color == 'black':
            # midpoint = [(start[0] + end[0]) / 2, (start[1] + end[1]) / 2]
            PolyLine([start, end], color=color, weight=1.5, tooltip=tooltip_text).add_to(map)
            # CircleMarker(
            #     location=midpoint,
            #     radius=3,
            #     color='red',
            #     fill=True,
            #     fill_color='red'
            # ).add_to(map)
        else:
            for index, survey in enumerate(surveys):
                if index == 0:
                    start = (survey.latitude, survey.longitude)
                    end = (survey.latitude, survey.longitude)
                    PolyLine([start, end], color=color, weight=weight, tooltip=tooltip_text).add_to(map)
                else:
                    start = (surveys[index - 1].latitude, surveys[index - 1].longitude)
                    end = (survey.latitude, survey.longitude)
                    PolyLine([start, end], color=color, weight=weight, tooltip=tooltip_text).add_to(map)

    # West line test
    # CircleMarker(location=[31.971144956097767, -103.66706244834383], radius=5, color='blue', fill=True, fill_color='blue').add_to(map)
 