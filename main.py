import sys
import cv2
from canvas import Canvas
from webcam import Webcam


def exit_listener(check_for_canvas=False, check_for_webcam=False):
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return True
    if cv2.getWindowProperty(Webcam.frame_name, cv2.WND_PROP_VISIBLE) < 1 and check_for_webcam:
        Canvas.close_canvas()
        return True
    if cv2.getWindowProperty(Canvas.frame_name, cv2.WND_PROP_VISIBLE) < 1 and check_for_canvas:
        Webcam.close_webcam()
        return True
    return False


if __name__ == '__main__':
    Canvas = Canvas("Canvas")
    Webcam = Webcam("Webcam")

    Canvas.add_circles(10)

    while True:
        Webcam.last_frame = Webcam.generate_frame()
        if not Webcam.is_camera_on:
            print(
                '\033[91m' + '\033[1m' + "\n\nKAMERKA NIE WYKRYTA!\nSprawdź czy nie jest wyłączona lub czy działa" + '\033[0m')
            sys.exit(1)

        hand_detect_data = Webcam.detect_hands_in_frame(Webcam.last_frame)

        if hand_detect_data.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(hand_detect_data.multi_hand_landmarks):
                hand_label = hand_detect_data.multi_handedness[idx].classification[0].label

                Canvas.mp_drawing.draw_landmarks(Webcam.last_frame, hand_landmarks, Webcam.mp_hands.HAND_CONNECTIONS)

                for ID, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = Webcam.last_frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)

                    if hand_label == 'Left':
                        Canvas.draw_circle((cx, cy), 5, Canvas.colors["blue"])
                    if hand_label == 'Right':
                        Canvas.draw_circle((cx, cy), 5, Canvas.colors["red"])
                    Canvas.check_for_collisions((cx, cy), ID)

        Canvas.draw_canvas_objects()
        Canvas.show_canvas()
        # Webcam.show_webcam()
        Canvas.erase((0, 0), (1000, 1000))
        if exit_listener(True, False):
            sys.exit(0)
