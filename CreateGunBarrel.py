import xlsxwriter

def fetch_plot_data_from_db():
    """
    Simulate fetching plot data (grid_x and depth) from a database.
    Replace this with your actual database query logic.
    """
    grid_x = [1264, 1824, 1667, 2699, -273]
    depth = [-7122, -7352, -7159, -7401, -7100]
    labels = [f"{i}" for i in range(1, len(grid_x) + 1)] 

    return grid_x, depth, labels

def create_plot_data_worksheet(workbook, grid_x, depth, labels=None):
    """
    Create the 'Plot Data' worksheet and write grid_x, depth, and optional labels data.
    
    :param workbook: The Excel workbook object.
    :param grid_x: List of X-values (lateral bottom hole spacing).
    :param depth: List of Y-values (depth below MSL).
    :param labels: Optional list of labels to display on markers (e.g., well numbers or names).
    """
    worksheet = workbook.add_worksheet("Plot Data")
    worksheet.write(0, 0, "Grid X (ft)")
    worksheet.write(0, 1, "Depth (ft)")
    
    if labels:
        worksheet.write(0, 2, "Labels")  # Add a header for the labels column

    # Write data to the worksheet
    for i, (x, y) in enumerate(zip(grid_x, depth), start=1):
        worksheet.write(i, 0, x)
        worksheet.write(i, 1, y)
        if labels:
            worksheet.write(i, 2, labels[i - 1])  # Write corresponding label if provided

    # Return the dynamic range references
    categories_range = f"='Plot Data'!$A$2:$A${len(grid_x) + 1}"  # X-values
    values_range = f"='Plot Data'!$B$2:$B${len(depth) + 1}"       # Y-values
    labels_range = f"='Plot Data'!$C$2:$C${len(labels) + 1}" if labels else None  # Label range
    return categories_range, values_range, labels_range


def create_chart_support_data(workbook):
    """
    Creates a 'Support Data' worksheet with static data for vertical lines and annotations.
    """
    worksheet = workbook.add_worksheet("Support Data")

    # Static data for vertical lines
    vertical_line_x = [0, 0]  # Static X-values for vertical line
    vertical_line_y = [-8500, -6000]  # Static Y-values for vertical line

    # Static data for annotations
    annotation_x = [0]  # Static X-value for annotation
    annotation_y = [-8490]  # Static Y-value for annotation

    # Write vertical line data
    worksheet.write(0, 0, "Vertical Line X")
    worksheet.write(0, 1, "Vertical Line Y")
    for i, (x, y) in enumerate(zip(vertical_line_x, vertical_line_y), start=1):
        worksheet.write(i, 0, x)
        worksheet.write(i, 1, y)

    # Write annotation data
    worksheet.write(0, 3, "Annotation X")
    worksheet.write(0, 4, "Annotation Y")
    for i, (x, y) in enumerate(zip(annotation_x, annotation_y), start=1):
        worksheet.write(i, 3, x)
        worksheet.write(i, 4, y)

    # Return ranges for the chart
    vertical_line_categories = "='Support Data'!$A$2:$A$3"
    vertical_line_values = "='Support Data'!$B$2:$B$3"
    annotation_categories = "='Support Data'!$D$2:$D$2"
    annotation_values = "='Support Data'!$E$2:$E$2"

    return vertical_line_categories, vertical_line_values, annotation_categories, annotation_values

def create_chart(
    workbook, categories_range, values_range, vertical_line_categories,
    vertical_line_values, annotation_categories, annotation_values, labels
):
    """
    Creates the oil barrel plot chart and inserts it into a new worksheet.

    :param workbook: The Excel workbook object.
    :param categories_range: Excel range for X-values of the main data.
    :param values_range: Excel range for Y-values of the main data.
    :param vertical_line_categories: Excel range for X-values of the vertical line.
    :param vertical_line_values: Excel range for Y-values of the vertical line.
    :param annotation_categories: Excel range for X-values of the annotation.
    :param annotation_values: Excel range for Y-values of the annotation.
    :param labels: Optional list of custom labels for the main data markers.
    """
    chart = workbook.add_chart({"type": "scatter"})

    # Add dynamic series for the main data with optional labels
    series_config = {
        "categories": categories_range,  # Dynamic X-values
        "values": values_range,          # Dynamic Y-values
        "marker": {"type": "circle", "size": 12},  # Circle markers
        'data_labels': {
            'value': True,
            'position': 'center',
        "custom": [{"value": lbl, "index": lbl} for lbl in labels],
        }
    }
    # if labels:
    #     series_config["data_labels"] = {
    #         "value": True,
    #         "position": "center",    
    #         "custom": [{"value": lbl, "index": lbl} for lbl in labels],
    #     }
    chart.add_series(series_config)

    # Add static series for the vertical line
    chart.add_series({
        "categories": vertical_line_categories,  # Static X-values for the vertical line
        "values": vertical_line_values,          # Static Y-values for the vertical line
        "line": {
            "color": "blue",
            "width": 1,
            "dash_type": "dash",
        },
        "marker": {"type": "none"},  # No markers for the line
    })

    # Add static series for the annotation
    chart.add_series({
        "categories": annotation_categories,  # Static X-value for annotation
        "values": annotation_values,          # Static Y-value for annotation
        "name": "Section Line",               # Annotation label
        "marker": {"type": "none"},           # Hide marker
        "data_labels": {
            "series_name": True,              # Display series name
            "value": False,                   # Do not display Y-value
            "position": "above",
        },
    })

    # Configure other chart properties
    chart.set_title({"name": "Oil Barrel Plot"})
    chart.set_x_axis({
        "name": "Lateral Bottom Hole Spacing (ft)",
        "min": -2640,
        "max": 7920,
        "major_unit": 1320,
        "minor_unit": 100,
        "minor_gridlines": {
            "visible": True,
            "line": {"color": "#D3D3D3", "width": 0.25},
        },
        "name_font": {"bold": True},
        "label_position": "low",
        "crossing": "min",
    })
    chart.set_y_axis({
        "name": "Depth Below MSL (ft)",
        "min": -8500,
        "max": -6000,
        "major_unit": 500,
        "minor_unit": 100,
        "minor_gridlines": {
            "visible": True,
            "line": {"color": "#D3D3D3", "width": 0.25},
        },
        "name_font": {"bold": True},
    })

    # Adjust plot area and chart area to create space for the annotation
    chart.set_plotarea({"x": 0.1, "y": 0.2, "width": 0.7, "height": 0.6})
    chart.set_chartarea({"x": 0.1, "y": 0.05, "width": 0.7, "height": 0.9})  # Increase bottom margin

    # Set chart size and layout
    chart.set_size({"width": 1100, "height": 550})  # ~11.5" x 8"
    chart.set_legend({"none": True})  # Disable legend

    # Insert the chart into a new worksheet
    chart_worksheet = workbook.add_worksheet("Chart")
    chart_worksheet.insert_chart("B4", chart)

# Main script
workbook = xlsxwriter.Workbook("OilBarrelPlot.xlsx")

# Fetch dynamic data for 'Plot Data'
grid_x, depth, labels = fetch_plot_data_from_db()

# Create the 'Plot Data' worksheet
categories_range, values_range, labels_range = create_plot_data_worksheet(workbook, grid_x, depth, labels)

# Create the 'Support Data' worksheet
vertical_line_categories, vertical_line_values, annotation_categories, annotation_values = create_chart_support_data(workbook)

# Create the chart
create_chart(workbook, categories_range, values_range, vertical_line_categories, vertical_line_values, annotation_categories, annotation_values, labels)

# Close the workbook
workbook.close()
print("Oil barrel plot with dynamic and static data created.")