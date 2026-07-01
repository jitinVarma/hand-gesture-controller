import cv2

from gesture_controller.hand_tracker import HandTracker
from gesture_controller.cursor_controller import CursorController
from gesture_controller.drawing import draw_skeleton


def main():
    tracker = HandTracker(model_path="hand_landmarker.task")
    cursor = CursorController()

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # mirror so hand movement matches cursor movement
        frame_height, frame_width = frame.shape[:2]

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        hand_landmarks = tracker.detect(rgb)

        if hand_landmarks:
            cursor.update(hand_landmarks)
            draw_skeleton(frame, hand_landmarks, frame_width, frame_height)

        cv2.imshow("Hand Gesture Controller", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    tracker.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
