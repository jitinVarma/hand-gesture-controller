import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from gesture_controller.geometry import (
    clamp_and_normalize,
    map_to_screen,
    smooth,
    distance,
    is_pinching,
)


def test_clamp_and_normalize_middle_of_zone():
    # 0.5 is exactly halfway through the zone 0.2-0.8 -> should normalize to 0.5
    assert round(clamp_and_normalize(0.5, 0.2, 0.8), 4) == 0.5


def test_clamp_and_normalize_clamps_below_zone():
    # value below zone_min should clamp to zone_min -> normalized 0.0
    assert clamp_and_normalize(0.0, 0.2, 0.8) == 0.0


def test_clamp_and_normalize_clamps_above_zone():
    # value above zone_max should clamp to zone_max -> normalized 1.0
    assert clamp_and_normalize(1.0, 0.2, 0.8) == 1.0


def test_map_to_screen_scales_correctly():
    assert map_to_screen(0.5, 1920) == 960
    assert map_to_screen(0.0, 1920) == 0
    assert map_to_screen(1.0, 1920) == 1920


def test_smooth_moves_partway_toward_new_value():
    # previous=0, new=100, factor=0.5 -> should land exactly halfway
    assert smooth(0, 100, 0.5) == 50


def test_smooth_with_zero_factor_stays_at_previous():
    assert smooth(10, 999, 0.0) == 10


def test_smooth_with_full_factor_jumps_to_new():
    assert smooth(10, 999, 1.0) == 999


def test_distance_between_identical_points_is_zero():
    assert distance((0.5, 0.5), (0.5, 0.5)) == 0


def test_distance_matches_known_3_4_5_triangle():
    # classic 3-4-5 right triangle -> distance should be 5
    assert distance((0, 0), (3, 4)) == 5


def test_is_pinching_true_when_close():
    assert is_pinching(0.02, 0.05) is True


def test_is_pinching_false_when_far():
    assert is_pinching(0.2, 0.05) is False
