# import cv2
# import mediapipe
# import numpy as np
#

# cap = cv2.VideoCapture(1)
# drawingModule = mediapipe.solutions.drawing_utils
# handsModule = mediapipe.solutions.hands
#
# while True:
#
#   _, frame = cap.read()
#   x , y, c = frame.shape
#   frame = cv2.flip(frame, 1)
#   cv2.imshow("Output", frame)
#   if cv2.waitKey(1) == ord('q'):
#             break
#
#
# cap.release()
# cv2.destroyAllWindows()

import cv2
import numpy
import mediapipe

# Initialize MediaPipe Hands
mp_hands = mediapipe.solutions.hands
hands = mp_hands.Hands()
draw_color = (255, 255, 255)  # Color for drawing
erase_color = (0, 0, 0)        # Color for erasing

# Initialize webcam
cap = cv2.VideoCapture(1)

# Create a blank canvas to draw
canvas = numpy.zeros((480, 640, 3), dtype=numpy.uint8)

# Initialize previous position variables
prev_x, prev_y = 0, 0

# Function to draw lines on canvas
def draw_line(canvas, start, end, color, thickness=2):
    cv2.line(canvas, start, end, color, thickness)

# Function to erase drawn areas on canvas
def erase_area(canvas, center, radius, color):
    cv2.circle(canvas, center, radius, color, -1)

# Main loop
while True:
    # Read frame from webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally
    frame = cv2.flip(frame, 1)

    # Convert frame to RGB for MediaPipe
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hand landmarks
    results = hands.process(frame_rgb)

    # Draw landmarks and get hand positions
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for id, lm in enumerate(hand_landmarks.landmark):
                # Get x, y coordinates of each landmark
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                if id == 8:  # Index finger tip (Left hand)
                    # Use index finger to draw
                    if prev_x != 0 and prev_y != 0:
                        draw_line(canvas, (prev_x, prev_y), (cx, cy), draw_color)
                    prev_x, prev_y = cx, cy

                elif id == 12:  # Index finger tip (Right hand)
                    # Use middle finger to erase
                    erase_area(canvas, (cx, cy), 20, erase_color)

    # Display frame and canvas
    cv2.imshow('Frame', frame)
    cv2.imshow('Canvas', canvas)

    # Check for key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()