import cv2
import numpy
import mediapipe

mp_hands = mediapipe.solutions.hands
mp_drawing = mediapipe.solutions.drawing_utils
hands = mp_hands.Hands()
draw_color = (255, 255, 255)  # Color for drawing
erase_color = (0, 0, 0)       # Color for erasing

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1024)

canvas = numpy.zeros((1024, 1024, 3), dtype=numpy.uint8)

prev_left_x, prev_left_y = None, None

def draw_line(canvas, start, end, color, thickness=2):
    cv2.line(canvas, start, end, color, thickness)

def erase_area(canvas, center, radius, color):
    cv2.circle(canvas, center, radius, color, -1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            hand_label = results.multi_handedness[idx].classification[0].label

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                if hand_label == 'Left' and id == 8:
                    if prev_left_x is not None and prev_left_y is not None:
                        draw_line(canvas, (prev_left_x, prev_left_y), (cx, cy), draw_color)
                    prev_left_x, prev_left_y = cx, cy

                elif hand_label == 'Right' and id == 12:
                    erase_area(canvas, (cx, cy), 20, erase_color)
    else:
        prev_left_x, prev_left_y = None, None

    cv2.imshow('Frame', frame)
    cv2.imshow('Canvas', canvas)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
