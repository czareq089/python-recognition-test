import cv2
import mediapipe
import numpy
from random import randint
from circle import Circle


class Canvas:

    def __init__(self, frame_name, width=1000, height=700, min_rand=10, max_rand=700):
        self.frame_name = frame_name
        self.colors = {
            "white": (255, 255, 255),
            "black": (0, 0, 0),
            "blue": (255, 0, 0),
            "green": (0, 255, 0),
            "red": (0, 0, 255),
        }
        self.mp_drawing = mediapipe.solutions.drawing_utils
        self.canvas = numpy.zeros((height, width, 3), dtype=numpy.uint8)
        self.canvas_objects = []
        self.min_rand = min_rand
        self.max_rand = max_rand

    def draw_line(self, start, end, color, thickness=2):
        cv2.line(self.canvas, start, end, color, thickness)

    def draw_circle(self, center, radius, color):
        cv2.circle(self.canvas, center, radius, color, -1)

    def erase(self, start, end):
        cv2.rectangle(self.canvas, start, end, self.colors["black"], -1)

    def show_canvas(self):
        cv2.imshow(self.frame_name, self.canvas)

    def add_circle(self, id_c, center, radius, color):
        self.canvas_objects.append(Circle(id_c, center, radius, color))

    def add_circles(self, num_of_circles):
        for i in range(num_of_circles):
            Canvas.add_circle(self, i, (randint(self.min_rand, self.max_rand), randint(self.min_rand, self.max_rand)),
                              20, self.colors["green"])

    def remove_circle(self, index):
        self.canvas_objects.insert(index, None)
        self.canvas_objects.pop(index + 1)

    def draw_canvas_objects(self):
        for obj in self.canvas_objects:
            if type(obj) is Circle:
                obj: Circle = obj
                self.draw_circle(obj.center, obj.radius, obj.color)

    def check_for_collisions(self, collision_position, hand_lm_id):
        for obj in self.canvas_objects:
            if type(obj) is Circle:
                obj: Circle = obj
                if obj.check_for_collision(collision_position, hand_lm_id):
                    self.remove_circle(obj.c_id)

    def close_canvas(self):
        cv2.destroyWindow(self.frame_name)
