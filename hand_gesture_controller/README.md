# Hand Gesture Controller

A real-time touchless mouse controller built with MediaPipe and OpenCV.
Your index fingertip drives the OS cursor; pinching your thumb and middle
finger together clicks and drags.

## Features

- Real-time hand tracking using MediaPipe's HandLandmarker (21 landmarks per hand)
- Live skeleton overlay drawn on the webcam feed
- Fingertip-to-cursor mapping with an active zone, so a comfortable hand
  range covers the full screen instead of requiring you to reach the edges
  of the camera frame
- Exponential smoothing to remove frame-to-frame jitter in cursor movement
- Thumb+middle pinch detection with debounced click/drag (press on pinch
  start, release on pinch end, so you can drag-and-drop, not just click)

## Setup

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

curl -o hand_landmarker.task https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task
```

On macOS, grant your terminal/IDE Accessibility permission the first time
you run it (System Settings → Privacy & Security → Accessibility), since
macOS blocks programmatic mouse control by default.

## Run

```bash
python main.py
```

Press `q` to quit.

## Architecture

The project separates pure math (testable without any hardware) from
code that depends on a camera, screen, or OS mouse:

```
gesture_controller/
├── geometry.py           # pure math: clamping, normalization, smoothing, distance
├── hand_tracker.py       # wraps MediaPipe's HandLandmarker
├── cursor_controller.py  # maps landmarks -> cursor movement + pinch clicks
└── drawing.py            # draws the skeleton overlay
main.py                   # ties it all together into the webcam loop
```

**Pipeline, once per frame:**

```
webcam frame -> flip (mirror) -> BGR to RGB -> HandTracker.detect()
    -> 21 landmarks -> CursorController.update() -> OS cursor moves
    -> draw_skeleton() -> shown in window
```

## Tests

The geometry functions are pure (take numbers in, return numbers out),
so they're unit tested directly with made-up coordinates - no camera
required:

```bash
pytest tests/
```

## How it works

MediaPipe's hand tracking is a two-stage pipeline: a lightweight palm
detector finds roughly where a hand is in the frame, then a second model
places 21 precise (x, y, z) landmarks on it, normalized to 0.0-1.0
regardless of camera resolution. Landmark 8 is the index fingertip;
landmark 4 is the thumb tip; landmark 12 is the middle fingertip.

Cursor position is computed by clamping the fingertip's normalized
position to a smaller "active zone" within the frame, rescaling that zone
to the full 0.0-1.0 range (min-max normalization), then scaling to actual
screen pixels. Exponential smoothing blends each new position with the
previous one to remove jitter.

Clicking works by measuring the Euclidean distance between the thumb tip
and middle fingertip. A pinch is detected the frame that distance first
drops below a threshold (not every frame it stays below it), which
triggers `mouseDown()`; releasing the pinch triggers `mouseUp()`.
