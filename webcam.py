import cv2
import mediapipe


class Webcam:
    def __init__(self, frame_name):
        self.frame_name = frame_name
        self.mp_hands = mediapipe.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1024)
        self.is_camera_on = False
        self.last_frame = None

    def generate_frame(self):
        self.is_camera_on, frame = self.cap.read()
        return cv2.flip(frame, 1)

    def detect_hands_in_frame(self, frame):
        return self.hands.process(frame)

    def show_webcam(self):
        cv2.imshow(self.frame_name, self.last_frame)

    def close_webcam(self):
        self.cap.release()
        cv2.destroyWindow(self.frame_name)
