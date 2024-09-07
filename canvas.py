import cv2
import mediapipe
import numpy


class Canvas:

    def __init__(self):
        self.colors = {
            "white": (255, 255, 255),
            "black": (0, 0, 0),
        }
        self.mp_drawing = mediapipe.solutions.drawing_utils
        self.canvas = numpy.zeros((1024, 1024, 3), dtype=numpy.uint8)

    def draw_line(self, start, end, color, thickness=2):
        cv2.line(self.canvas, start, end, color, thickness)

    def erase_area(self, center, radius, color):
        cv2.circle(self.canvas, center, radius, color, -1)

    def show_canvas(self):
        cv2.imshow('Canvas', self.canvas)

    def close_canvas(self):
        cv2.destroyWindow('Canvas')
