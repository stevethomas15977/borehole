
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
from pydash import min_
import math
import numpy as np

class HandlerWithText(HandlerLine2D):
    def __init__(self, marker_text, **kw):
        super().__init__(**kw)
        self.marker_text = marker_text

    def create_artists(self, legend, orig_handle, xdescent, ydescent, width, height, fontsize, trans):
        markers = super().create_artists(legend, orig_handle, xdescent, ydescent, width, height, fontsize, trans)
        x = markers[0].get_xdata()[0]
        y = markers[0].get_ydata()[0]
        markers.append(plt.text(x + 7, y, self.marker_text, weight='bold', fontsize=fontsize, ha='center', va='center', transform=trans))
        return markers
    
def calculate_angle(x1, y1, x2, y2):
    angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
    return angle

def plot_hypothenuse(ax, target_well, well, well_hypotenuse_distance):
    va = 'bottom'
    ha = 'right'
    ax.plot([target_well["grid_x"], well["grid_x"]],
            [(target_well["grid_z"]), (well["grid_z"])],
            color='black', linestyle='--', linewidth=0.5)
    
    # Calculate midpoints for hypotenuse
    mid_x = (target_well["grid_x"] + well["grid_x"]) / 2
    mid_y = (target_well["grid_z"] + well["grid_z"]) / 2
    
    # Calculate the angle of the hypotenuse
    delta_x = target_well["grid_x"] - well["grid_x"]
    delta_y = target_well["grid_z"] - well["grid_z"]
    angle = math.degrees(math.atan2(delta_y, delta_x))
    
    # Normalize the angle to ensure readability
    if angle < -90:
        angle += 180
    elif angle > 90:
        angle -= 180
    
    if well_hypotenuse_distance["hypotenuse"] is not None:
        if va == 'bottom':
            va = 'top'
        else:
            va = 'bottom'

        if ha == 'right':
            ha = 'left'
        else:
            ha = 'right'
        
        # Add hypotenuse label
        ax.text(mid_x, mid_y, f"{well_hypotenuse_distance['hypotenuse']}", weight='bold', fontsize=6, ha=ha, va=va, rotation=angle)
    
def plot_adjacent(ax, target_well, well):
    delta_x = target_well["grid_x"] - well["grid_x"]
    mid_adj_x = (target_well["grid_x"] + well["grid_x"]) / 2
    mid_adj_y = well["grid_y"]
    adjacent_distance = abs(delta_x)
    ax.plot([well["grid_x"], target_well["grid_x"]],
            [well["grid_y"], well["grid_y"]],
            color='blue', linestyle='--', linewidth=3.5)
    ax.text(mid_adj_x, mid_adj_y, f"{adjacent_distance}", weight='bold', fontsize=6, ha='center', va='bottom', rotation=0)

def plot_opposite(ax, target_well, well):
    delta_y = target_well["grid_z"] - well["grid_z"]  
    mid_opp_x = target_well["grid_x"]
    mid_opp_y = (target_well["grid_z"] + well["grid_z"]) / 2
    opposite_distance = abs(delta_y)
    ax.plot([target_well["grid_x"], target_well["grid_x"]],
            [well["grid_z"], target_well["grid_z"]],
            color='red', linestyle='--', linewidth=0.5)
    ax.text(mid_opp_x, mid_opp_y, f"{opposite_distance}", weight='bold', fontsize=6, ha='center', va='center', rotation=0)

def are_adjacent(reference_well, target_well, well_data):
    for well in well_data:
        if well == reference_well or well == target_well:
            continue
        min_x = min_([reference_well["grid_x"], target_well["grid_x"]])
        max_x = max([reference_well["grid_x"], target_well["grid_x"]])
        min_y = min_([reference_well["grid_y"], target_well["grid_y"]])
        max_y = max([reference_well["grid_y"], target_well["grid_y"]])
        min_z = min_([reference_well["grid_z"], target_well["grid_z"]])
        max_z = max([reference_well["grid_z"], target_well["grid_z"]])
        if (min_x < well["grid_x"] < max_x and
            min_y < well["grid_y"] < max_y and
            min_z < well["grid_z"] < max_z):
            return False
    return True

def marker_colors(status: str) -> tuple[str, str]:
    if "COMPLETED" == status:
        color = "black"
        text_color = "white"
    elif "DRILLED" == status:
        color = "magenta"
        text_color = "black"
    elif "DUC" == status:
        color = "blue"
        text_color = "black"
    elif "INACTIVE PRODUCER" == status:
        color = "yellow"
        text_color = "black"
    elif "PERMIT EXPIRED" == status:
        color = "black"
        text_color = "white"
    elif "PERMITTED" == status:
        color = "red"
        text_color = "black"
    elif "PRODUCING" == status:
        color = "green"
        text_color = "black"
    else:
        color = "black"
        text_color = "white"
    return color, text_color
