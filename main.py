import sys
from canvas import Canvas
from webcam import Webcam
import cv2


def exit_listener():
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return True
    if cv2.getWindowProperty('Frame', cv2.WND_PROP_VISIBLE) < 1:
        Canvas.close_canvas()
        return True
    if cv2.getWindowProperty('Canvas', cv2.WND_PROP_VISIBLE) < 1:
        Webcam.close_webcam()
        return True
    return False


if __name__ == '__main__':
    Canvas = Canvas()
    Webcam = Webcam()

    prev_left_x, prev_left_y = None, None

    while True:
        Webcam.last_frame = Webcam.generate_frame()
        if not Webcam.is_camera_on:
            print(
                '\033[91m' + '\033[1m' + "\n\nKAMERKA NIE WYKRYTA!\nSprawdź czy nie jest wyłączona lub czy działa" + '\033[0m')
            break

        hand_detect_data = Webcam.detect_hands_in_frame(Webcam.last_frame)

        if hand_detect_data.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(hand_detect_data.multi_hand_landmarks):
                hand_label = hand_detect_data.multi_handedness[idx].classification[0].label

                Canvas.mp_drawing.draw_landmarks(Webcam.last_frame, hand_landmarks, Webcam.mp_hands.HAND_CONNECTIONS)

                for ID, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = Webcam.last_frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)

                    if hand_label == 'Left' and ID == 8:
                        if prev_left_x is not None and prev_left_y is not None:
                            Canvas.draw_line((prev_left_x, prev_left_y), (cx, cy), Canvas.colors["white"])
                        prev_left_x, prev_left_y = cx, cy

                    elif hand_label == 'Right' and ID == 12:
                        Canvas.erase_area((cx, cy), 20, Canvas.colors["black"])
        else:
            prev_left_x, prev_left_y = None, None

        Canvas.show_canvas()
        Webcam.show_webcam()
        if exit_listener():
            sys.exit(0)
