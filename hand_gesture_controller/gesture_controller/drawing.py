import cv2
from gesture_controller.hand_tracker import HAND_CONNECTIONS


def draw_skeleton(frame, hand_landmarks, frame_width, frame_height):
    """Draws connecting lines first, then joints on top, matching the
    hand's 21-point skeleton onto the given frame (in place)."""

    for connection in HAND_CONNECTIONS:
        start = hand_landmarks[connection.start]
        end = hand_landmarks[connection.end]
        x1, y1 = int(start.x * frame_width), int(start.y * frame_height)
        x2, y2 = int(end.x * frame_width), int(end.y * frame_height)
        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    for landmark in hand_landmarks:
        px, py = int(landmark.x * frame_width), int(landmark.y * frame_height)
        cv2.circle(frame, (px, py), 5, (0, 255, 0), -1)
