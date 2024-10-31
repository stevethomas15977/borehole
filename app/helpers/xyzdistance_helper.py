import math

# Function to calculate xyz distances
def calculate_xyz_distances(reference_well_x, reference_well_y, reference_well_z, target_well_x, target_well_y, target_well_z) -> dict: 
    delta_x = int(target_well_x - reference_well_x)
    delta_y = int(target_well_y - reference_well_y)
    delta_z = int(target_well_z - reference_well_z)
    hypotenuse = int(math.sqrt(delta_x**2 + delta_y**2 + delta_z**2))
    return {
        "delta_x": delta_x,
        "delta_y": delta_y,
        "delta_z": delta_z,
        "hypotenuse": hypotenuse
    }