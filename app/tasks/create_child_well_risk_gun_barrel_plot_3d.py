from tasks.task import Task
from tasks.task_enum import TASKS
from helpers import task_logger, adjust_coordinate, latlon_to_utm_feet
from services import (AnalysisService, 
                      SurveyService, 
                      TexasLandSurveySystemService,
                      NewMexicoLandSurveySystemService,
                      TargetWellInformationService)
from traceback import format_exc
import matplotlib.pyplot as plt
import numpy as np
import os

BACKGROUND_COLOR = "white"

class CreateChildWellRiskGunBarrelPlot3D(Task):

    def execute(self):
        task = TASKS.CREATE_CHILD_WELL_RISK_GUN_BARREL_PLOT_3D.value
        logger = task_logger(task, self.context.logs_path)
        try:
            analysis_service = AnalysisService(db_path=self.context.db_path)
            survey_service = SurveyService(db_path=self.context.db_path)
            texas_land_survey_system_service = TexasLandSurveySystemService(self.context._texas_land_survey_system_database_path)
            new_mexico_land_survey_system_service = NewMexicoLandSurveySystemService(self.context._new_mexico_land_survey_system_database_path)             
            target_well_information_service = TargetWellInformationService(self.context.db_path)

            # Create the 3D plot with different colors for each well
            fig = plt.figure(figsize=(16, 10), facecolor=BACKGROUND_COLOR)
            ax = fig.add_subplot(111, projection='3d')

            # Rotate the plot 45 degrees to the right along the X-axis
            ax.view_init(elev=30, azim=55)  # You can adjust the 'elev' as needed
            
            # Set the z-axis limits
            z_min = -8000
            z_max = 2000
            ax.set_zlim(z_min, z_max)

            # Define function to scale the coordinates within the plot limits
            def scale_values(values, min_limit, max_limit):
                min_val = min(values)
                max_val = max(values)
                return [(max_limit - min_limit) * (v - min_val) / (max_val - min_val) + min_limit for v in values]

            # Plot the tlss line
            target_well = target_well_information_service.get_first_row()

            # Set axis labels
            if target_well.state == "TX":
                section_label = f"{target_well.state}/{target_well.county}/{target_well.tx_abstract_southwest_corner}/{target_well.tx_block_southwest_corner}/{int(float(target_well.nm_tx_section_southwest_corner))}) (100 ft intervals)"
                plss = texas_land_survey_system_service.get_by_county_abstract_block_section(target_well.county, target_well.tx_abstract_southwest_corner, target_well.tx_block_southwest_corner, str(int(float(target_well.nm_tx_section_southwest_corner))))            
                if plss:
                    fnl_grid_x, fnl_grid_y = latlon_to_utm_feet(plss.northeast_latitude, plss.northeast_longitude)
            elif target_well.state == "NM":
                section_label = f"{target_well.state}/{target_well.county}/{target_well.nw_township_southwest_corner}/{target_well.nm_range_southwest_corner}/{int(float(target_well.nm_tx_section_southwest_corner))}) (100 ft intervals)"
                township = int(target_well.nw_township_southwest_corner[:-1])
                township_direction = target_well.nw_township_southwest_corner[-1]
                nm_range = int(target_well.nm_range_southwest_corner[:-1])
                range_direction = target_well.nm_range_southwest_corner[-1]
                section = int(target_well.nm_tx_section_southwest_corner)
                plss = new_mexico_land_survey_system_service.get_by_township_range_section(township=township, township_direction=township_direction, range=nm_range, range_direction=range_direction, section=section)            
                if plss:
                    fnl_grid_x, fnl_grid_y = latlon_to_utm_feet(plss.northeast_latitude, plss.northeast_longitude)

            start = adjust_coordinate(plss.southwest_latitude, plss.southwest_longitude, 2640, "W")
            end = adjust_coordinate(plss.southwest_latitude, plss.southwest_longitude, 7920, "E")

            plss_start_grid_x, plss_start_grid_y = latlon_to_utm_feet(start[0], start[1])
            plss_end_grid_x, plss_end_grid_y = latlon_to_utm_feet(end[0], end[1])

            plss_grid_x = np.array([plss_start_grid_x, plss_end_grid_x])
            plss_grid_y = np.array([plss_start_grid_y, plss_end_grid_y])
            plss_subsurface_depth = np.array([z_min, z_min])
            ax.plot(plss_grid_x, plss_grid_y, plss_subsurface_depth, color='r', label=section_label)

            # Labels and title
            ax.set_xlabel('2640 ft intervals from section line (red)')
            ax.set_xticklabels([])
            ax.set_ylabel('5000 ft intervals')
            ax.set_yticklabels([])
            ax.set_zlabel('Subsurface Depth 2000 ft intervals')

            title = f"{self.context.project.capitalize()} child well risk {section_label} 3D gun barrel plot {self.context.version}"
            ax.set_title(title, fontsize=12, fontweight='bold')
            
            # Plot the offset wells
            save_i = 0
            offsets = analysis_service.select_where_target_well_spacing_gun_barrel_plot_flag_is_true()
            for i, offset in enumerate(offsets, start=1):
                save_i = i
                surveys = survey_service.get_by_api(offset.api)
                
                # Ensure that surveys contain iterable data for plotting
                grid_x = [s.grid_x for s in surveys]
                grid_y = [s.grid_y for s in surveys]
                subsurface_depth = [s.subsurface_depth for s in surveys]

                # Plot the well trajectory with a unique color and label
                ax.plot(grid_x, grid_y, subsurface_depth, color='g', label=f'{i}-{offset.name}')

                # Annotate the last survey with the index   
                if surveys:
                    last_index = len(surveys) - 1
                    # Ensure the last survey has the necessary attributes
                    if hasattr(surveys[last_index], 'grid_x') and hasattr(surveys[last_index], 'grid_y') and hasattr(surveys[last_index], 'subsurface_depth'):
                        ax.text(surveys[last_index].grid_x, surveys[last_index].grid_y, surveys[last_index].subsurface_depth, f'{i}', color='black', weight='bold') 

            # Plot the target wells
            target_wells = analysis_service.get_simulated_target_wells()
            for i, target_well in enumerate(target_wells, start=save_i+1):
                lookup = target_well_information_service.get_by_name(target_well.name)
                surface_grid_x, surface_grid_y = latlon_to_utm_feet(lookup.latitude_surface_location, lookup.longitude_surface_location)
                target_well_grid_x = np.array([surface_grid_x, target_well.lateral_start_grid_x, target_well.lateral_end_grid_x])
                target_well_grid_y = np.array([surface_grid_y, target_well.lateral_start_grid_y, target_well.lateral_end_grid_y])
                target_well_subsurface_depth = np.array([lookup.enverus_rkb_elevation_ft, target_well.subsurface_depth, target_well.subsurface_depth])
                ax.plot(target_well_grid_x, target_well_grid_y, target_well_subsurface_depth, color='orange', label=f"{i}-{target_well.name}")
                ax.text(target_well.lateral_end_grid_x, target_well.lateral_end_grid_y, target_well.subsurface_depth, f'{i}', color='black', weight='bold') 

            # Show the legend with labels
            ax.legend(loc='center left', bbox_to_anchor=(-0.6, 0.5))

            # Save the plot
            plot_name = ""
            output_file = os.path.join(self.context.project_path, f"{self.context.project}-{plot_name}-3d-gun-barrel-plot-{self.context.version}.png")
            plt.savefig(output_file)

            logger.info(f"{task} completed successfully: {output_file}")
        except Exception as e:
            logger.error(f"Error in {task} workflow task: {e}\n{format_exc()}")
            raise ValueError(f"Error in {task} workflow task: {e}")

