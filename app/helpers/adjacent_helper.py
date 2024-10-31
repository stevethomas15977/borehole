


def are_lengths_close(length1: int, length2: int, threshold: float = 0.8):
    """
    Determines if two lengths are within the specified threshold of each other.

    :param length1: Length of the first oil well
    :param length2: Length of the second oil well
    :param threshold: The threshold for comparison (default is 0.8, meaning 80%)
    :return: True if the lengths are within the threshold, False otherwise
    """
    ratio = length1 / length2 if length1 < length2 else length2 / length1
    return ratio >= threshold

def is_within_latitude_range(start_latitude: float, end_latitude: float, test_latitude: float) -> bool:
    # Determine the lower and upper bounds
    lower_bound = min(start_latitude, end_latitude)
    upper_bound = max(start_latitude, end_latitude)

    # Check if the test_latitude is between the bounds
    return lower_bound <= test_latitude <= upper_bound

def is_within_longitude_range(start_longitude: float, end_longitude: float, test_longitude: float) -> bool:
    # Determine the lower and upper bounds
    lower_bound = min(start_longitude, end_longitude)
    upper_bound = max(start_longitude, end_longitude)

    # Check if the test_longitude is between the bounds
    return lower_bound <= test_longitude <= upper_bound

def is_within_x_range(start_x: float, end_x: float, target_x: float) -> bool:
    lower_bound = min(start_x, end_x)
    upper_bound = max(start_x, end_x)
    return lower_bound <= target_x <= upper_bound

def is_within_y_range(start_y: float, end_y: float, test_y: float) -> bool:
    lower_bound = min(start_y, end_y)
    upper_bound = max(start_y, end_y)
    return lower_bound <= test_y <= upper_bound