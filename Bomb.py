import pygame
from MovableObject import MovableObject
from Field import Field
from Fire import Fire, TIME_TO_EXPAND_FIRE, TIME_TO_DISAPEAR

TIME_TO_EXPLODE = 4000


class Bomb(MovableObject):
    images = []
    list_ = []

    def __init__(self, game, level, position, player, power):
        # bomb, ready to explode, exploded, waiting, ending
        self.state = 0

        self.timer = TIME_TO_EXPLODE

        self.owner = player
        self.fires: list[Fire] = []

        super().__init__(game, level, [game.size * position[0], game.size * position[1]], self.images[0], False)

        self.my_background[0].add_object(self)

        self.moving = True

        self.speed = 1
        self.power = power

    @staticmethod
    def init():
        # TODO make rotate image
        Bomb.images = [pygame.image.load("img/bomb/bomb_0.png"),
                       pygame.image.load("img/bomb/bomb_1.png"),
                       pygame.image.load("img/bomb/bomb_2.png"),
                       pygame.image.load("img/bomb/bomb_3.png"),
                       pygame.image.load("img/bomb/bomb_4.png"),
                       ]

    def move_object(self):  # type: ()-> bool
        if self.state == 0:
            if super().move_object():
                self.kick(self.direction)
                return True
        elif self.state == 1:
            if self.movement == 0:
                self.explode()
            else:
                super().move_object()
        return False

    def can_kick(self):
        return self.state == 0

    def set_move_parameters(self, destination: tuple[int, int], next_background: Field):
        super().set_move_parameters(destination, next_background)
        next_background.add_object(self)
        print(f"Bomb added to {next_background.cords}")

    def kick(self, direction):
        if self.state == 0 and self.movement == 0:
            self.direction = direction
            x, y = self.position
            if self.direction == 0:
                x -= 1
            elif self.direction == 1:
                y -= 1
            elif self.direction == 2:
                x += 1
            elif self.direction == 3:
                y += 1

            if self.background[x][y].can_entry_bomb():
                self.set_move_parameters((x * self.game.size, y * self.game.size), self.background[x][y])
                return True
            else:
                return False

        elif self.state == 1:
            self.explode()
        return False

    def change_timer(self, dt):
        self.timer -= dt
        if self.timer < 0:
            if self.state == 0:
                self.state = 1
            elif self.state == 1:
                pass
            elif self.state == 2:
                self.power -= 1
                if self.power:
                    for f in self.fires:
                        f.next()
                    self.timer = TIME_TO_EXPAND_FIRE
                else:
                    self.timer = TIME_TO_DISAPEAR
                    self.state = 3
            elif self.state == 3:
                self.end()

    def explode(self):

        if self.state == 1:
            self.state = 2

            self.set_cords((self.position[0] * self.game.size, self.position[1] * self.game.size))
            self.owner.bomb_counter -= 1
            self.fires = [Fire(self.game, self.level, self, self.position, 4, self.power),
                          Fire(self.game, self.level, self, self.position, 0, self.power),
                          Fire(self.game, self.level, self, self.position, 1, self.power),
                          Fire(self.game, self.level, self, self.position, 2, self.power),
                          Fire(self.game, self.level, self, self.position, 3, self.power),
                          ]

            self.timer = TIME_TO_EXPAND_FIRE

    def draw(self):
        if self.state == 2 or self.state == 3:
            # self.image = self.images[1][0]
            for f in self.fires:
                f.draw()
            return  # if exploded don't draw self
        elif self.state == 1:
            self.image = self.images[4]
        elif self.state == 0:
            if self.timer > 3500:
                self.image = self.images[0]
            elif self.timer > 2500:
                self.image = self.images[1]
            elif self.timer > 1500:
                self.image = self.images[2]
            elif self.timer > 100:
                self.image = self.images[3]
            elif self.timer > 0:
                self.image = self.images[4]

        super().draw()

    def can_entry(self):
        return self.state >= 2

    def hide(self):
        for f in self.fires: f.hide()
        super().hide()

    def end(self):
        # print("END")
        for f in self.fires: f.delete()
        super().hide()
        for b in self.my_background:
            b.remove_object(self)
        self.list_.remove(self)

        self.fires = []

    def end_move(self):
        self.my_background[0].remove_object(self)
        super().end_move()

    def destroy(self, time=0):
        # print("DESTROY")
        if self.state < 2:
            self.state = 1
            self.set_cords((self.position[0] * self.game.size, self.position[1] * self.game.size))
            self.explode()
        else:
            return False
