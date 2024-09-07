import cv2
import mediapipe
import numpy


class Canvas:

    def __init__(self, frame_name):
        self.frame_name = frame_name
        self.colors = {
            "white": (255, 255, 255),
            "black": (0, 0, 0),
            "blue": (255, 0, 0),
            "green": (0, 255, 0),
            "red": (0, 0, 255),
        }
        self.mp_drawing = mediapipe.solutions.drawing_utils
        self.canvas = numpy.zeros((1024, 1024, 3), dtype=numpy.uint8)

    def draw_line(self, start, end, color, thickness=2):
        cv2.line(self.canvas, start, end, color, thickness)

    def draw_circle(self, center, radius, color):
        cv2.circle(self.canvas, center, radius, color, -1)

    def erase(self, start, end):
        cv2.rectangle(self.canvas, start, end, self.colors["black"], -1)

    def show_canvas(self):
        cv2.imshow(self.frame_name, self.canvas)

    def close_canvas(self):
        cv2.destroyWindow(self.frame_name)
