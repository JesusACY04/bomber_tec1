import pygame
from Object import Object
from Field import Field
from PowerUp import PowerUp
from Fire import FireSegment


class MovableObject(Object):

    def __init__(self, game, level, cords, image, possibility_of_entry, rect_offset=(0, 0), rect_size=None):
        self.distance_to_move = 0

        super().__init__(game, level, cords, image, possibility_of_entry, rect_offset, rect_size)

        self.background: list[list[Field]] = self.level.background

        self.position = (0, 0)
        self.cords: list = [0, 0]
        self.set_cords(cords)

        self.movement = 0
        self.speed = 0

        self.direction = 0
        self.destination = (-1, -1)

        self.draw()
        self.my_background: list[Field] = [self.background[self.position[0]][self.position[1]]]

    def set_cords(self, cords):
        self.cords: list[float, float] = [cords[0], cords[1]]
        self.x, self.y = self.cords[0] + self.rect_offset[0], self.cords[1] + self.rect_offset[1]
        self.position = (self.calculate_position(self.x), self.calculate_position(self.y))

    def change_cords(self, dx, dy):
        self.cords[0] += dx
        self.cords[1] += dy
        self.x, self.y = self.cords[0] + self.rect_offset[0], self.cords[1] + self.rect_offset[1]
        self.position = (self.calculate_position(self.x), self.calculate_position(self.y))

    def calculate_position(self, x):
        return (x + self.game.size // 2) // self.game.size

    def hide(self):
        for b in self.my_background: b.draw()

    def draw(self):
        self.game.display.blit(self.image, (round(self.cords[0]), round(self.cords[1])))

    def set_move_parameters(self, destination, next_background: Field):
        self.movement = self.speed
        self.distance_to_move = self.game.size
        self.destination = destination
        self.my_background.append(next_background)

    def move_forward(self, distance):
        if self.direction == 0:
            self.change_cords(-distance, 0)
        elif self.direction == 1:
            self.change_cords(0, -distance)
        elif self.direction == 2:
            self.change_cords(distance, 0)
        else:
            self.change_cords(0, distance)
        self.distance_to_move -= distance

    #  Return True if object end moving
    def move_object(self):

        if self.movement != 0:
            self.move_forward(self.movement)
            if self.distance_to_move < 0:
                self.end_move()
                return True

        # check background in fire or powerup
        for back in self.my_background:
            for obj in back.object:
                if obj.__class__ == FireSegment and self.colliderect(obj):
                    self.destroy()
                elif obj.__class__ == PowerUp and self.colliderect(obj):
                    self.collect(obj)
        return False

    def end_move(self):
        print("End move")
        self.movement = 0
        self.distance_to_move = 0
        self.set_cords(self.destination)
        self.my_background = self.my_background[1:]
        # print(f"Cords: {self.cords} Rect_pos: ({self.x},{self.y}) Position: {self.position}")

    def collect(self, powerup):
        pass
