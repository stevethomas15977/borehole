from collections import defaultdict

from randomcolor import RandomColor
from datetime import datetime

from models import Codevelopment

# The function essentially identifies clusters of codeveloped APIs by finding all 
# connected components in an undirected graph representation of the input codevelopment_list. 
# Each connected component represents a group of codeveloped APIs.
def identify_codevelopment_clusters(codevelopment_list: list[Codevelopment]) -> dict[str, list[Codevelopment]]:
    # Create an adjacency list
    adjacency_list = defaultdict(set)

    for codevelopment in codevelopment_list:
        adjacency_list[codevelopment.reference_api].add(codevelopment.target_api)
        adjacency_list[codevelopment.target_api].add(codevelopment.reference_api)

    # Function to perform DFS and find all connected components
    def dfs(node, visited, group):
        stack = [node]
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                group.append(current)
                stack.extend(adjacency_list[current])

    # Find all groups (connected components)
    visited = set()
    groups = []

    for well in adjacency_list:
        if well not in visited:
            group = []
            dfs(well, visited, group)
            groups.append(group)

    return groups

# Function to search for a particular well in the groups list
def find_well_in_groups(well_name: str, groups: list[list[str]]):
    for i, group in enumerate(groups):
        if well_name in group:
            return i, group
    return None, None

# Function to assign a color to each group
def assign_colors_to_groups(groups: list[list[str]]):
    rc = RandomColor()
    colors = rc.generate(luminosity='dark', count=len(groups))
    if "#000000" in colors:
        colors.remove("#000000") # Remove black color
        colors.append("#A9A9A9") # Add dark grey color
    return colors

def compare_first_production_date_days(date1:str, date2:str, threshold: int) -> bool:
    date_format = "%Y-%m-%d"
    try:
        date1 = datetime.strptime(date1, date_format).date()
        date2 = datetime.strptime(date2, date_format).date()
    except ValueError as e:
        print(f"Error parsing dates: {e}")
        return False
    difference = abs((date2 - date1).days)
    # Check if the difference is within the threshold
    return difference <= threshold
