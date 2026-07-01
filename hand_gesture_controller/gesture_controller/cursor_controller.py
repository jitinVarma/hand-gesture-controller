import pyautogui
from gesture_controller.geometry import (
    clamp_and_normalize,
    map_to_screen,
    smooth,
    distance,
    is_pinching,
)

pyautogui.FAILSAFE = True   # slam cursor to a screen corner to emergency-stop
pyautogui.PAUSE = 0          # remove default delay, we call this ~30x/sec

# landmark indices used for control
INDEX_TIP = 8
THUMB_TIP = 4
MIDDLE_TIP = 12


class CursorController:
    """Maps a hand's index fingertip to the OS cursor, with jitter smoothing,
    an active zone for easier reachability, and thumb+middle pinch-to-click/drag."""

    def __init__(self,
                 zone_x=(0.2, 0.8),
                 zone_y=(0.2, 0.8),
                 smoothing_factor=0.4,
                 pinch_threshold=0.05):
        self.screen_width, self.screen_height = pyautogui.size()

        self.zone_x_min, self.zone_x_max = zone_x
        self.zone_y_min, self.zone_y_max = zone_y
        self.smoothing_factor = smoothing_factor
        self.pinch_threshold = pinch_threshold

        self.smooth_x = self.screen_width // 2
        self.smooth_y = self.screen_height // 2
        self.was_pinching = False

    def update(self, hand_landmarks):
        """Call once per frame with the 21 detected landmarks. Moves the
        cursor and fires mouseDown/mouseUp on pinch transitions."""
        index_tip = hand_landmarks[INDEX_TIP]
        thumb_tip = hand_landmarks[THUMB_TIP]
        middle_tip = hand_landmarks[MIDDLE_TIP]

        # --- cursor position: clamp to active zone, normalize, map to screen ---
        normalized_x = clamp_and_normalize(index_tip.x, self.zone_x_min, self.zone_x_max)
        normalized_y = clamp_and_normalize(index_tip.y, self.zone_y_min, self.zone_y_max)
        screen_x = map_to_screen(normalized_x, self.screen_width)
        screen_y = map_to_screen(normalized_y, self.screen_height)

        # --- exponential smoothing to remove jitter ---
        self.smooth_x = smooth(self.smooth_x, screen_x, self.smoothing_factor)
        self.smooth_y = smooth(self.smooth_y, screen_y, self.smoothing_factor)

        pyautogui.moveTo(int(self.smooth_x), int(self.smooth_y))

        # --- pinch detection (thumb + middle) with debounced click/drag ---
        pinch_distance = distance(
            (thumb_tip.x, thumb_tip.y),
            (middle_tip.x, middle_tip.y)
        )
        pinching_now = is_pinching(pinch_distance, self.pinch_threshold)

        if pinching_now and not self.was_pinching:
            pyautogui.mouseDown()
            self.was_pinching = True
        elif not pinching_now and self.was_pinching:
            pyautogui.mouseUp()
            self.was_pinching = False
