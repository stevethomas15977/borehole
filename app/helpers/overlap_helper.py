

import numpy as np

def are_lengths_similar(well_lengths, threshold_percent) -> tuple[bool, float]:
    """
    Determine if a group of oil well lengths are considered similar.
    
    Parameters:
    well_lengths (list of float): A list containing the lengths of oil wells.
    threshold_percent (float): The threshold as a percentage of the mean length. 
                               If the standard deviation is below this percentage of the mean, 
                               the wells are considered similar.
    
    Returns:
    bool: True if the standard deviation is within the threshold percentage, False otherwise.
    float: The standard deviation of the well lengths.
    """
    if len(well_lengths) == 0:
        raise ValueError("The list of well lengths is empty.")
    
    # Calculate the mean and standard deviation
    mean_length = np.mean(well_lengths)
    std_dev = np.std(well_lengths)

    # Calculate the threshold in terms of absolute length
    threshold_value = (threshold_percent / 100) * mean_length
    
    # Return True if the standard deviation is less than or equal to the threshold value
    return std_dev <= threshold_value, std_dev
