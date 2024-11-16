import xlsxwriter

# Create a new workbook and add a worksheet
workbook = xlsxwriter.Workbook("OilBarrelPlot.xlsx")
worksheet = workbook.add_worksheet()

# Updated well data
grid_x = [-2640, -1320, 0, 1320, 2640, 3960, 5280, 6600, 7920]
depth = [-6000, -6500, -7000, -7500, -8000, -8500]

# Write data to the worksheet
worksheet.write(0, 0, "Grid X (ft)")
worksheet.write(0, 1, "Depth (ft)")
# for i, (x, y) in enumerate(zip(grid_x, depth), start=1):
#     worksheet.write(i, 0, x)
#     worksheet.write(i, 1, y)

# Create a scatter chart
chart = workbook.add_chart({"type": "scatter"})

# Configure the series
chart.add_series({
    "categories": f"=Sheet1!$A$2:$A${len(grid_x)+1}",  # X-values
    "values": f"=Sheet1!$B$2:$B${len(depth)+1}",        # Y-values
    "marker": {"type": "circle", "size": 7},           # Circle markers
})

# Set chart title and axis titles
chart.set_title({"name": "Oil Barrel Plot"})
chart.set_x_axis({
    "name": "Lateral Bottom Hole Spacing (ft)",
    "min": -2640,
    "max": 7920,
    "major_unit": 1320,
    "name_font": {"bold": True},
    "label_position": "low",
    "crossing": "min",
})

chart.set_y_axis({
    "name": "Depth Below MSL (ft)",
    "min": -8500,
    "max": -6000,
    "major_unit": 500,
    "name_font": {"bold": True},
    "label_position": "low",
})

chart.set_plotarea({'x': 0.1, 'y': 0.1, 'width': 0.7, 'height': 0.7}) 

chart.set_chartarea({'x': 0.1, 'y': 0.1, 'width': 0.7, 'height': 0.7})

# Set chart size and layout
chart.set_size({"width": 900, "height": 450})  # ~11.5" x 8"
chart.set_legend({"none": True})  # Disable legend

# Insert the chart into the worksheet
worksheet.insert_chart("E5", chart)

# Close the workbook
workbook.close()
print("Oil barrel plot with adjusted Y-axis created.")
