class Circle:
    def __init__(self, c_id, center, radius, color):
        self.c_id = c_id
        self.center = center
        self.radius = radius
        self.color = color

    def check_for_collision(self, collision_position, hand_lm_id):
        if ((self.center[0] - self.radius <= collision_position[0] <= self.center[0] + self.radius) and
                (self.center[1] - self.radius <= collision_position[1] <= self.center[1] + self.radius)):
            print(f"Circle {self.c_id} on position {self.center} collides on {collision_position} with hand landmark id {hand_lm_id}")
            return True
        return False
