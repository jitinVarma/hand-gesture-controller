import math


def clamp_and_normalize(value, zone_min, zone_max):
    """Clamp value to [zone_min, zone_max], then rescale to 0.0-1.0."""
    clamped = max(zone_min, min(value, zone_max))
    normalized = (clamped - zone_min) / (zone_max - zone_min)
    return normalized


def map_to_screen(normalized_value, screen_dimension):
    """Scale a 0.0-1.0 normalized value to a pixel coordinate."""
    return int(normalized_value * screen_dimension)


def smooth(previous_value, new_value, smoothing_factor):
    """Exponential smoothing: blend previous and new value."""
    return previous_value + (new_value - previous_value) * smoothing_factor


def distance(point_a, point_b):
    """Euclidean distance between two (x, y) tuples."""
    return math.sqrt((point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2)


def is_pinching(dist, threshold):
    """Is the measured distance below the pinch threshold?"""
    return dist < threshold
