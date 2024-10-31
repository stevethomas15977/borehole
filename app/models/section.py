import os
from typing import Tuple

import geopandas as gpd

from context import Context

class Section:
    def __init__(self, file_path: str, column: str):
        if not file_path:
            raise ValueError("File path cannot be null")
        if not column:
            raise ValueError("Column cannot be null")
        
        self._file_path = file_path
        self._column = column
        self._gdf = None

        try:
            self._gdf = gpd.read_file(self._file_path)
        except Exception as e:
            raise Exception(f"Error loading geojson from {self._file_path}: {e}")

    def get_section_west_line_coordinates(self, name: str) -> Tuple[float, float]:
        try:
            if not name:
                raise ValueError("Name cannot be null")
            if self._gdf is None:
                self._gdf = gpd.read_file(self._file_path)
            section = self._gdf[self._gdf[self._column] == name]
            if section.empty:
                raise ValueError(f"Section {name} not found in {self._file_path}")
            coordinates = list(section.geometry.iloc[0].boundary.coords)
            south_west_coordinate = self.__find_most_south_and_west(coordinates)
            return south_west_coordinate
        except Exception as e:
            raise Exception(f"Error getting coordinates for section {name}: {e}")

    def __find_most_south_and_west(self, coordinates: list[Tuple[float, float]]) -> Tuple[float, float]:
        west_line_coords = [coord for coord in coordinates if coord[0] == min(coord[0] for coord in coordinates)]
        for coords in west_line_coords:
            longitude = coords[0]
            latitude = coords[1]
        return latitude, longitude 
    
    @staticmethod
    def texas_abstract_west_line_coordinates(context: Context, county: str, abstract: str) -> Tuple[float, float]:
        try:
            if context.tx_abstract_column is None:
                raise ValueError("TX_ABSTRACT_COLUMN environment variable not set.")
            if not county:
                raise ValueError("County cannot be null")
            if not abstract:
                raise ValueError("Abstract cannot be null")
            texas_geojson_abstract_path = os.path.join(context.geojson_path, "texas", "abstract")
            geojson_file_path = os.path.join(texas_geojson_abstract_path, f"{county.lower()}.geojson")
            section = Section(geojson_file_path, context.tx_abstract_column)
            latitude, longitude = section.get_section_west_line_coordinates(abstract)
            return latitude, longitude
        except Exception as e:
            raise Exception(f"Error getting coordinates for Texas county {county} abstract {abstract}: {e}")
        
    @staticmethod
    def new_mexico_section_west_line_coordinates(context: Context, township: str, range: str, section_name: str) -> Tuple[float, float]:  
        try:
            if context.nm_section_column is None:
                raise ValueError("NM_SECTION_COLUMN environment variable not set.")
            if not township:
                raise ValueError("Township cannot be null")
            if not range:
                raise ValueError("Range cannot be null")
            if not section_name:
                raise ValueError("Section cannot be null")
            new_mexico_section_geojson_path = os.path.join(context.geojson_path, "new_mexico", "section")
            geojson_file_path = os.path.join(new_mexico_section_geojson_path, f"{township}-{range}.geojson")
            section = Section(geojson_file_path, context.nm_section_column)
            latitude, longitude = section.get_section_west_line_coordinates(section_name)
            return latitude, longitude
        except Exception as e:
            raise Exception(f"Error getting coordinates for section {section_name}: {e}")
