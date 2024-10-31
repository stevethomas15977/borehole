from tasks.task import Task
from tasks.task_enum import TASKS
from helpers import task_logger, HandlerWithText, calculate_angle
from services import (AnalysisService, 
                      TargetWellInformationService, 
                      WellService,
                      XYZDistanceService,
                      OverlapService)

from models import XYZDistance, Overlap
from traceback import format_exc
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import os
import numpy as np

BACKGROUND_COLOR = "white"

class CreateChildWellRiskGunBarrelPlotZoomed(Task):

    def execute(self):
        task = TASKS.CREATE_CHILD_WELL_RISK_GUN_BARREL_PLOT_ZOOMED.value
        logger = task_logger(task, self.context.logs_path)
        try:
            plot_name = "child-well-risk"
            analysis_service = AnalysisService(db_path=self.context.db_path)
            target_well_information_service = TargetWellInformationService(self.context.db_path)
            well_service = WellService(self.context.db_path)
            overlap_service = OverlapService(self.context.db_path)
            xyz_distance_service = XYZDistanceService(self.context.db_path)

            target_well = target_well_information_service.get_first_row()

            shallowest = target_well_information_service.get_shallowest() - self.context.depth_distance_threshold
            deepest = target_well_information_service.get_deepest() + self.context.depth_distance_threshold
            
            y_min = deepest * -1
            y_max = shallowest * -1
            x_min = -2640
            x_max = 2640

            fig, ax = plt.subplots(figsize=(15, 8), facecolor=BACKGROUND_COLOR)
            ax.set_facecolor(BACKGROUND_COLOR)
            ax.grid(True, which='both', color=BACKGROUND_COLOR, linestyle='--', linewidth=0.5)
            
            title = f"{self.context.project.capitalize()} child well risk (zoomed) "
            title += f"({target_well.state.capitalize()}/"
            title += f"{target_well.county.capitalize()}/"
            title += f"{target_well.tx_abstract_southwest_corner}/{target_well.tx_block_southwest_corner}/{target_well.nm_tx_section_southwest_corner}) "
            title += f"[{self.context.version}]"
            plt.title(title, fontsize=12, fontweight='bold')
            
            ax.set_xlim(x_min, x_max)
            ax.set_ylim(y_min, y_max)

            depths = np.arange(y_min, y_max, 100)
            for depth in depths:
                ax.axhline(depth, color='lightgrey', linewidth=0.5, linestyle='--', alpha=0.90, zorder=0)

            plt.xticks(np.arange(x_min, x_max + 1, 1320))

            widths = np.arange(x_min, x_max, 100)
            for width in widths:
                ax.axvline(width, color='lightgrey', linewidth=0.5, linestyle='--', alpha=0.90, zorder=0)  

            # Set axis labels
            ax.set_xlabel(f"Lateral endpoint spacing from west line of {target_well.tx_abstract_southwest_corner}/{target_well.tx_block_southwest_corner}/{target_well.nm_tx_section_southwest_corner}) in feet")
            ax.set_ylabel(f"Depth below bean sea level in feet")

            # Plot a single thin blue dashed line at x = 100
            specific_x = 0  # Change this value to the desired x-coordinate
            ax.axvline(specific_x, color='blue', linewidth=0.5, linestyle='--', alpha=0.75)
            label_y_position = y_min
            ax.text(specific_x, label_y_position, f"{target_well.tx_abstract_southwest_corner}/{target_well.tx_block_southwest_corner}/{target_well.nm_tx_section_southwest_corner})", color='black', fontsize=8, ha='center', va='bottom')

            offsets = analysis_service.select_where_target_well_spacing_gun_barrel_plot_flag_is_true_zoomed()
            legend_elements = []    
            api_to_index = {}
            for i, offset in enumerate(offsets):
                api_to_index[offset.api] = i
                if "11-111" in offset.api:
                    color = "orange"
                    text_color = "black"
                else:
                    well = well_service.get_by_api(offset.api)
                    if well is None:
                        color = "black"
                        text_color = "white"
                    else:
                        if "COMPLETED" == well.status:
                            color = "black"
                            text_color = "white"
                        elif "DRILLED" == well.status:
                            color = "magenta"
                            text_color = "black"
                        elif "DUC" == well.status:
                            color = "blue"
                            text_color = "black"
                        elif "INACTIVE PRODUCER" == well.status:
                            color = "yellow"
                            text_color = "black"
                        elif "PERMIT EXPIRED" == well.status:
                            color = "black"
                            text_color = "white"
                        elif "PERMITTED" == well.status:
                            color = "red"
                            text_color = "black"
                        elif "PRODUCING" == well.status:
                            color = "green"
                            text_color = "black"
                        else:
                            color = "black"
                            text_color = "white"

                ax.scatter(offset.gun_barrel_x, offset.subsurface_depth, facecolor=color, s=100, edgecolor=BACKGROUND_COLOR, linewidth=0.5, alpha=0.70, zorder=3)
                ax.annotate(str(i), (offset.gun_barrel_x, offset.subsurface_depth), color=text_color, fontsize=8, ha='center', va='center', weight='bold', zorder=6)
                
                y_offset = -85
                ax.annotate(str(offset.first_production_date), (offset.gun_barrel_x, offset.subsurface_depth + y_offset), color='black', fontsize=5, ha='center', va='center', alpha=0.70, zorder=6)

                # Annotate the perforation interval
                y_offset = 85
                ax.annotate(str(offset.lateral_length), (offset.gun_barrel_x, offset.subsurface_depth + y_offset), color='black', fontsize=5, ha='center', va='center', alpha=0.70, zorder=6)

                # Add legend elements
                legend_elements.append(Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markeredgecolor=BACKGROUND_COLOR, markersize=10, linestyle='None', alpha=0.70, zorder=5))

            #Add adjacent, opposite and hypotenuse lines and labels
            offset = 100 
            text = ""
            target_wells = analysis_service.get_simulated_target_wells()
            for target_well in target_wells:
                xyz_distances = xyz_distance_service.get_by_target_well(target_well.api)
                reference_analysis = analysis_service.get_by_api(target_well.api)
                if reference_analysis is None:
                    continue
                for xyz_distance in list[XYZDistance](xyz_distances):
                    target_analysis = analysis_service.get_by_api(xyz_distance.target_api)
                    # Calculate distances for end points
                    if reference_analysis.gun_barrel_x is None or target_analysis.gun_barrel_x is None:
                        continue
                    x_distance_end = abs(reference_analysis.gun_barrel_x - target_analysis.gun_barrel_x)
                    if reference_analysis.gun_barrel_y is None or target_analysis.gun_barrel_y is None:
                        continue
                    y_distance_end = abs(reference_analysis.subsurface_depth - target_analysis.subsurface_depth)
                    hyp_distance_end = int(np.sqrt(x_distance_end**2 + y_distance_end**2))

                    text += f"- {api_to_index[reference_analysis.api]}-({x_distance_end}, {y_distance_end}, {hyp_distance_end}, "

                    reference_parent = analysis_service.get_by_name(reference_analysis.parent_1)
                    if reference_parent is not None:
                        # print(f"Parent: {reference_parent.api}")
                        reference_parent_well = well_service.get_by_api(reference_parent.api)
                        # print(f"Cumulative oil production: {reference_parent_well.cumlative_oil}")
                        # print(f"Perferated interval: {reference_parent_well.perf_interval}")
                        overlap = overlap_service.get_by_reference_api_target_api(reference_api=reference_parent.api, target_api=reference_analysis.api)
                        if overlap is not None:
                            # print(f"Overlap: {overlap.overlap_percentage}")
                            parent_production_to_target_ratio = round((reference_parent_well.cumlative_oil / reference_parent_well.perf_interval) * (overlap.overlap_percentage / 100), 2)
                            # print(parent_production_to_target_ratio)
                    
                            text += f"{reference_parent_well.first_production_date}, {int(reference_parent_well.cumlative_oil/1000)}, {int(overlap.overlap_percentage)}, {parent_production_to_target_ratio}"

                    text += f")\n"

                    # Define the vertices of the triangle
                    A = (reference_analysis.gun_barrel_x, reference_analysis.subsurface_depth)
                    B = (reference_analysis.gun_barrel_x, target_analysis.subsurface_depth)
                    C = (target_analysis.gun_barrel_x, target_analysis.subsurface_depth)
                    
                    # Plot the triangle
                    # triangle = plt.Polygon([A, B, C], fill=None, linestyle='--', linewidth=0.5, edgecolor='black', alpha=0.30, zorder=0)
                    # ax.add_patch(triangle)

                    # Calculate the angles
                    angle_AB = calculate_angle(*A, *B)
                    angle_BC = calculate_angle(*B, *C)
                    angle_CA = calculate_angle(*C, *A)
                    if abs(angle_AB) >= 90:
                        angle_AB += 180
                    if abs(angle_BC) >= 90:
                        angle_BC += 180
                    if abs(angle_CA) >= 90:
                        angle_CA += 180

                    # print(f"angle_AB: {angle_AB}-{x_distance_end}, angle_BC: {angle_BC}-{y_distance_end}, angle_CA: {angle_CA}-{hyp_distance_end}")

                    # Annotate the sides
                    # ax.text((A[0] + B[0]) / 2, (A[1] + B[1]) / 2, x_distance_end, rotation=angle_AB, ha='center', va='center', alpha=0.90, fontsize=5, zorder=6)
                    # ax.text((B[0] + C[0]) / 2, (B[1] + C[1]) / 2, y_distance_end, rotation=angle_BC, ha='center', va='center', alpha=0.90, fontsize=5, zorder=6)
                    # ax.text((C[0] + A[0]) / 2, (C[1] + A[1]) / 2, hyp_distance_end, rotation=angle_CA, ha='center', va='center', alpha=0.90, fontsize=5, zorder=6)

            # Add custom legend
            handlers = {legend_elements[i]: HandlerWithText(str(i)) for i in range(len(legend_elements))}
            custom_legend = ax.legend(
                handles=legend_elements,
                labels=[f"{offset.name}" for offset in offsets],
                loc='upper center',
                fontsize=7,
                bbox_to_anchor=(0.5, -0.14),
                handler_map=handlers,
                borderaxespad=0.1,
                ncol=6)

            custom_legend.get_frame().set_facecolor(BACKGROUND_COLOR)
            ax.add_artist(custom_legend)

            # Add custom annotation text
            status_text = f"Status colors:\n"
            status_text += f"- targets:   orange\n"
            status_text += f"- proudcing: green\n"
            status_text += f"- completed: black\n"
            status_text += f"- drilled:   magenta\n"
            status_text += f"- DUC:       blue\n"
            status_text += f"- inactive:  yellow\n"
            status_text += f"- expired:   red\n"

            status_text += f"\nPerforation interval and first production date\n"
            status_text += f"are shown at the top and bottom of marker.\n"

            text = f"Distances between wells in ft. \nHytpoetunuse distances <= 2000 are annotated\nIndex from/to (adjacent(x),opposite(y),hypotenuse(z), \noffset first production date, cumulative barrels/1000s, \noverlap%, cumulative/perf interval ratio)\n" + text

            ax.annotate(f"{status_text}\n{text}", 
                         xy=(x_max - 2200, y_max - 100), 
                         xytext=(x_max - 2200, y_max - 100),
                         fontsize=6, 
                         color='black', 
                         ha='left', 
                         va='top')

            # plt.text(0.5, -0.12,
            #         'Index # and Well Names.',
            #         ha='center',
            #         va='center',
            #         transform=ax.transAxes,
            #         fontsize=8,
            #         color='black')

            # Save the plot
            output_file = os.path.join(self.context.project_path, f"{self.context.project}-{plot_name}-gun-barrel-plot-zoomed-{self.context.version}.png")
            plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor=BACKGROUND_COLOR)
            plt.close(fig)

            logger.info(f"{task}: {self.context.logs_path}")
        except Exception as e:
            logger.error(f"Error {task} workflow task: {e}\n{format_exc()}")
            raise ValueError(f"Error {task} workflow task: {e}")