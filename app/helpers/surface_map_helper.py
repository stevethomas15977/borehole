
from math import e
from folium import CircleMarker, Map, PolyLine, Element, GeoJson, Marker, DivIcon
from folium.plugins import BeautifyIcon
import json
import os
import geopandas as gpd

from context import Context

from helpers import adjust_coordinate

from models import (Analysis, Well, TexasLandSurveySystem)

from services import (WellService, SurveyService, StratigraphicService)
from services.analysis_service import AnalysisService

def well_tooltip(well: Well) -> str:
    html = ""
    html += f"<div style='text-align: left; font-size: 10px;'>"
    html += f" Name: {well.name}<br>"
    html += f" API: {well.api}<br>"
    html += f" Interval: {well.interval}<br>"
    html += f" 1st Prod Date: {well.first_production_date}<br>"
    html += f" Lateral Length: {well.lateral_length} ft.<br>"
    html += f" Direction: {well.direction}"
    html += f"</div>"
    return html

def determine_center_map(analyses: list[Analysis]) -> tuple[float, float]:
    total_latitude = sum(a.lateral_end_latitude for a in analyses if a.lateral_end_latitude is not None)
    total_longitude = sum(a.lateral_end_longitude for a in analyses if a.lateral_end_longitude is not None)
    count = sum(1 for a in analyses if a.lateral_end_latitude is not None and a.lateral_end_longitude is not None)
    
    if count == 0:
        raise ValueError("No valid coordinates found in the list of Analysis instances.")
    
    avg_latitude = total_latitude / count
    avg_longitude = total_longitude / count
    
    return avg_latitude, avg_longitude

def well_determine_center_map(wells: list[Well]) -> tuple[float, float]:
    total_latitude = sum(well.bottom_hole_latitude for well in wells if well.bottom_hole_latitude is not None)
    total_longitude = sum(well.bottom_hole_longitude for well in wells if well.bottom_hole_longitude is not None)
    count = sum(1 for well in wells if well.bottom_hole_latitude is not None and well.bottom_hole_longitude is not None)
    if count == 0:
        raise ValueError("Unable to fild center of map.")
    avg_latitude = total_latitude / count
    avg_longitude = total_longitude / count
    return avg_latitude, avg_longitude

def apply_geojson_overlay(geojson_file_path: str, name: str, label:str, map: Map) -> None:
    # Load the GeoJSON file for townships
    with open(geojson_file_path) as f:
        geojson_data = json.load(f)
    # Add the GeoJSON data for the townships
    GeoJson(
        geojson_data,
        name=name,
        style_function=lambda feature: {
            "color": "black",
            "weight": 0.5,
            "fillColor": "none",
            "opacity": 0.5,
        },
    ).add_to(map)

    # Add labels for the townships
    gdf = gpd.GeoDataFrame.from_features(geojson_data['features'])
    for _, row in gdf.iterrows():
        centroid = row['geometry'].centroid
        Marker(
            location=[centroid.y, centroid.x],
            icon=DivIcon(
                html = f"""<div style="font-size: 6pt; color: black; white-space: nowrap; opacity: 0.5;">{row[label]}</div>"""
            ),
        ).add_to(map)

def texas_plss_block_section_overlay(context: Context, fip_codes: list[str], map: Map) -> None:
    for fips_code in fip_codes:
        geojson_file_path = os.path.join(context.geojson_path, "texas", "block-section", f"surv{fips_code}p.geojson")
        # Load the GeoJSON file for abstracts
        with open(geojson_file_path) as f:
            township_geojson_data = json.load(f)
        # Add the GeoJSON data for the abstracts
        GeoJson(
            township_geojson_data,
            name="PLSS Block Sections",
            style_function=lambda feature: {
                "color": "black",
                "weight": 0.5,
                "fillColor": "none",
                "opacity": 0.5,
            },
        ).add_to(map)

        # Add labels for the block
        block_gdf = gpd.GeoDataFrame.from_features(township_geojson_data['features'])
        for _, row in block_gdf.iterrows():
            centroid = row['geometry'].centroid
            abstract = row['ABSTRACT_L']
            block = row['LEVEL2_BLO']
            section = row['LEVEL3_SUR']
            if section is not None:
                label = f'<span style="text-align: center; vertical-align: middle;">{abstract}<br>{block}<br>{section}</span>'
            marker = Marker(
                location=[centroid.y, centroid.x],
                popup=f"{label}",
                icon=DivIcon(
                    html = f"""<div style="font-size: 6pt; color: black; white-space: nowrap; opacity: 0.5;">{label}</div>"""
                ),
            )
            marker.add_to(map)

def texas_plss_abstracts_overlay(context: Context, counties: list[str], map: Map) -> None:
    for county in counties:
        geojson_file_path = os.path.join(context.geojson_path, "texas", "abstract", f"{county}.geojson")
        # Load the GeoJSON file for abstracts
        with open(geojson_file_path) as f:
            township_geojson_data = json.load(f)
        # Add the GeoJSON data for the abstracts
        GeoJson(
            township_geojson_data,
            name="PLSS Abstracts",
            style_function=lambda feature: {
                "color": "black",
                "weight": 0.5,
                "fillColor": "none",
                "opacity": 0.5,
            },
        ).add_to(map)

        # Add the modal HTML to the map
        map.get_root().html.add_child(Element(modal_html))

        # Add labels for the townships
        township_gdf = gpd.GeoDataFrame.from_features(township_geojson_data['features'])
        for _, row in township_gdf.iterrows():
            centroid = row['geometry'].centroid
            label = row['ABSTRACT_L']
            marker = Marker(
                location=[centroid.y, centroid.x],
                popup=f"{label}",
                icon=DivIcon(
                    html = f"""<div style="font-size: 6pt; color: black; white-space: nowrap; opacity: 0.5;">{label}</div>"""
                ),
            )
            marker.add_to(map)

        # Add the custom JavaScript to the map
        map.get_root().script.add_child(Element(click_event_js))

def create_map(context: Context, avg_lat: float, avg_long: float, zoom_level: float = 12.5) -> Map:
    zoom_level = zoom_level
    map = Map(location=[avg_lat, avg_long], 
            zoom_start=zoom_level, 
            # min_zoom=zoom_level, 
            # max_zoom=zoom_level, 
            # zoom_control=False,
            # scrollWheelZoom=False,
            tiles='OpenStreetMap')
    return map

def list_geojson_files(file_prefixes: list[str], target_directory: str) -> list[str]:
    matching_files = []
    for file in os.listdir(target_directory):
        for prefix in file_prefixes:
            if file.startswith(prefix) and file.endswith('.geojson'):
                matching_files.append(file)
                break
    return matching_files

def new_mexico_plss_overlay(context: Context, file_prefixes: list[str], map: Map):
    # New Mexico PLSS Township GeoJSON
    new_mexico_township_file_path = os.path.join(context.geojson_path, 'new_mexico', 'PLSSTownship.geojson')
    apply_geojson_overlay(new_mexico_township_file_path, name='PLSS Townships', label='TWNSHPLAB', map=map)
    # New Mexico PLSS Sections GeoJSON
    new_mexico_sections_file_path = os.path.join(context.geojson_path, 'new_mexico', 'sections')
    for geojson_file in list_geojson_files(file_prefixes=file_prefixes, target_directory=new_mexico_sections_file_path):
        apply_geojson_overlay(geojson_file_path=os.path.join(new_mexico_sections_file_path, geojson_file), name='PLSS Sections', label=context.nm_section_column, map=map)


def icon_square(color: str, border_width: int) -> BeautifyIcon:
    return BeautifyIcon(icon_shape='rectangle-dot', border_color=color, border_width=border_width)

def icon_circle(color: str, border_width: int) -> BeautifyIcon:
    return BeautifyIcon(icon_shape='circle-dot', border_color=color, border_width=border_width)

def icon_star(color: str, border_width: int) -> BeautifyIcon:
    return BeautifyIcon(icon_shape='star', border_color=color, border_width=border_width)

def draw_section_lines(coordinates: dict, tooltip: str, map: Map) -> None:
    # Marker for the southwest corner
    start = (coordinates['southwest_latitude'], coordinates['southwest_longitude'])
    CircleMarker(location=start, radius=5, color='red', fill=True, fill_color='red', fill_opacity=1.0, tooltip=tooltip).add_to(map)

    # Draw gun barrel slice
    start = adjust_coordinate(coordinates['southwest_latitude'], coordinates['southwest_longitude'], 2640, "W")
    end = adjust_coordinate(coordinates['southwest_latitude'], coordinates['southwest_longitude'], 7920, "E")
    PolyLine([start, end], color='red', weight=3.0, tooltip=f"Gun Barrel Slice").add_to(map)

    start = coordinates['northwest_latitude'], coordinates['northwest_longitude']
    end = adjust_coordinate(coordinates['northwest_latitude'], coordinates['northwest_longitude'], 5280, "W")
    PolyLine([start, end], color='green', weight=3.0, tooltip=f"Northwest Section Line").add_to(map)

def draw_wells(context: Context, 
               well_service: WellService, 
               survey_service: SurveyService, 
               stratigraphic_service: StratigraphicService,
                map: Map) -> None:
    apis = survey_service.get_unique_api_values()
    color = "black"
    for api in apis:
        well = well_service.get_by_api(api=api)
        if well is not None:
            tooltip_html = well_tooltip(well=well)
            stratigraphic = stratigraphic_service.get_by_prism_code(well.interval)
            if stratigraphic is not None:
                color = stratigraphic.color
        else:
            tooltip_html = f"<div style='text-align: left; font-size: 10px;'>API: {api}</div>"
        surveys = survey_service.get_by_api(api=api)
        if well is not None and len(surveys) == 0:
            start = (well.surface_latitude, well.surface_longitude)
            end = (well.bottom_hole_latitude, well.bottom_hole_longitude)
            PolyLine([start, end], color=color, weight=2.0, tooltip=tooltip_html).add_to(map)
            # Marker(location=start, icon=icon_circle(color='black', border_width=4)).add_to(map)
        else:
            for index, survey in enumerate(surveys):
                if index == 0:
                    start = (survey.latitude, survey.longitude)
                    end = (survey.latitude, survey.longitude)
                    PolyLine([start, end], color=color, weight=2.0, tooltip=tooltip_html).add_to(map)
                else:
                    start = (surveys[index - 1].latitude, surveys[index - 1].longitude)
                    end = (survey.latitude, survey.longitude)
                    PolyLine([start, end], color=color, weight=2.0, tooltip=tooltip_html).add_to(map)

def draw_well_legend(context: Context, well_service: WellService, stratigraphic_service: StratigraphicService) -> str:
    legend_html = ""
    legend_html += f"""<div style="position: fixed; top: 80px; left: 10px; width: 350px; border: 2px solid grey; z-index: 9999; overflow-y: auto; overflow-x: auto; max-height: 80%; background-color: #D3D3D3; opacity: 0.9; padding: 5px;">"""
    legend_html += f""" <div style="text-align: center; font-size: 14px;"><b>{context.project.capitalize()}</b></div>"""
    legend_html += f""" <div style="text-align: center; font-size: 10px;">Version {context.version}</div>"""
    legend_html += f""" <div style="margin-right: 10px;">"""
    wells = well_service.get_all()
    legend_html += f"""  <div style="margin-right: 5px;">"""
    legend_html += f"""<div style="margin-right: 5px;"><b style="width: 100px;height:20px;">Landing Zones</b></div>"""

    interval_set = {well.interval for well in wells}
    for interval in interval_set:
        stratigraphic = stratigraphic_service.get_by_prism_code(interval)
        if stratigraphic is not None:
            color = stratigraphic.color
            legend_html += f"""<div style="margin-right: 5px; width:20px;height:20px;background-color:{color};"><p style="margin-left: 25px; width: 100px;height:20px;">{stratigraphic.union_code}</p></div>"""
    legend_html += f""" </div>"""
    legend_html += f""" <br>"""

    legend_html += f"""<div style="margin-right: 5px;"><b style="width: 100px;height:20px;">Wells</b></div>"""
    for well in wells:
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
    return legend_html

# HTML for the modal window
modal_html = '''
<div id="modal" style="display:none; position:fixed; z-index:10000; background:rgba(0, 0, 0, 0.5); top:0; left:0; width:100%; height:100%; align-items:center; justify-content:center;">
    <div style="background:white; padding:20px; border-radius:5px; max-width:500px; margin:auto;">
        <h2>Marker Information</h2>
        <p>This is a modal window that appears when a marker is clicked.</p>
        <button onclick="document.getElementById('modal').style.display='none'">Close</button>
    </div>
</div>
<script>
function showModal() {
    document.getElementById('modal').style.display = 'flex';
}
</script>
'''

# JavaScript to add click event to marker
click_event_js = '''
function onEachFeature(feature, layer) {
    layer.on('click', function() {
        showModal();
    });
}
'''