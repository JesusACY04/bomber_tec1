import pygame

from Field import Field
from Object import Object

TIME_TO_EXPAND_FIRE = 80
TIME_TO_DISAPEAR = 700

FIRE_TYPE_CENTER = 0
FIRE_TYPE_HORIZONTAL = 1
FIRE_TYPE_VERTICAL = 2


class FireSegment(Object):

    def __init__(self, game, level, cords, image, possibility_of_entry, fire_type):
        rect_offset = (10 if fire_type == 2 else 0, 10 if fire_type == 1 else 0)
        rect_size = (game.size - (20 if fire_type == 2 else 0), game.size - (20 if fire_type == 1 else 0))
        super().__init__(game, level, cords, image, possibility_of_entry, rect_offset, rect_size)


class Fire:
    images = []

    def __init__(self, game, level, bomb, begin_position: list[int, int], direction: int = 0, power: int = 0):
        self.owner = bomb
        self.game = game
        self.level = level
        self.begin_position: list[int, int] = list(begin_position)
        self.power = power

        self.my_background: list[Field] = []

        self.type = FIRE_TYPE_CENTER if direction == 4 else (
            FIRE_TYPE_VERTICAL if direction == 0 or direction == 2 else FIRE_TYPE_HORIZONTAL)

        # center of fire
        if direction == 4:
            self.power=0
            pos = begin_position
            img = self.images[0]
            field = self.level.get_background(pos)
            self.my_background.append(field)
            self.fire_segments = [
                FireSegment(self.game, self.level, [self.game.size * pos[0], self.game.size * pos[1]], img, True,
                            self.type)]
            self.my_background.append(field)

            # destroy object under fire
            field.destroy(TIME_TO_DISAPEAR+TIME_TO_EXPAND_FIRE*(power+1))

            field.add_object(self.fire_segments[0])

        else:
            self.selected_images = [self.images[1][direction],
                           self.images[2][direction]]
            self.fire_segments: list[FireSegment] = []

        self.direction = direction

        self.type = [1, 2][direction % 2] if direction != 4 else 0

        self.next()

    @staticmethod
    def init():
        Fire.images = [pygame.image.load("img/bomb/explosion_0.png"),
                       [pygame.image.load("img/bomb/explosion_10.png"),
                        pygame.image.load("img/bomb/explosion_11.png"),
                        pygame.image.load("img/bomb/explosion_12.png"),
                        pygame.image.load("img/bomb/explosion_13.png")],
                       [pygame.image.load("img/bomb/explosion_20.png"),
                        pygame.image.load("img/bomb/explosion_21.png"),
                        pygame.image.load("img/bomb/explosion_22.png"),
                        pygame.image.load("img/bomb/explosion_23.png")]
                       ]

    def next(self):
        if self.power > 0:
            self.power -= 1
            if self.direction == 0:
                self.begin_position[0] -= 1
            elif self.direction == 1:
                self.begin_position[1] -= 1
            elif self.direction == 2:
                self.begin_position[0] += 1
            elif self.direction == 3:
                self.begin_position[1] += 1

            pos = self.begin_position
            if len(self.fire_segments): self.fire_segments[-1].set_image(self.selected_images[0])

            field = self.level.get_background(pos)

            is_destroyed = field.destroy(TIME_TO_DISAPEAR+TIME_TO_EXPAND_FIRE*(self.power+1))
            if is_destroyed: self.power = 0

            if field.can_entry() or is_destroyed:
                print("New segment:", pos)
                fire_segment = FireSegment(self.game, self.level, [self.game.size * pos[0], self.game.size * pos[1]],
                                           self.selected_images[1],
                                           True, self.type)
                self.fire_segments.append(fire_segment)
                self.my_background.append(field)
                field.add_object(fire_segment)
            else:
                self.power = 0

    def draw(self):
        for f in self.fire_segments: f.draw()

    def hide(self):
        for f in self.my_background: f.draw()

    def delete(self):
        self.hide()
        for fire, field in zip(self.fire_segments, self.my_background):
            field.remove_object(fire)

        self.fire_segments = []
        self.my_background = []
        self.owner = None
