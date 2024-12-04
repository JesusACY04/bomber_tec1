import random

import pygame

import Player
from Object import Object
import Events


class PowerUp(Object):
    number_of_powerups = 8
    images = []
    list_ = []

    def __init__(self, game, level, position: list[int, int], type_):
        self.type = type_
        super().__init__(game, level,
                         [game.size * position[0], game.size * position[1]],
                         self.images[self.type],
                         True, (5, 5),
                         (game.size - 10, game.size - 10)
                         )
        print("Create powerup")
        self.list_.append(self)
        self.background = self.level.get_background(position)
        self.background.add_object(self)
        self.is_deleted = False

    @staticmethod
    def init():
        # load images
        for i in range(PowerUp.number_of_powerups):
            PowerUp.images.append(
                pygame.image.load(f"img/powerup/p{i}.png")
            )
        print("PowerUp loaded")
        print(PowerUp.images)

    @staticmethod
    def create(game, level, position: list[int, int]):
        # id [bomb +1, bomb -1, insensitivity,speed +, speed -, kick, change direction]
        # TODO balance drop rate
        if random.randint(1, 10) <= 6:
            type_ = random.randint(0, 7)
            return PowerUp(game, level, position, type_)

    def destroy(self, time=0):
        self.delete()
        return True

    def delete(self):
        if not self.is_deleted:
            self.is_deleted = True
            self.background.remove_object(self)
            self.list_.remove(self)
            self.background.draw()

    def collect(self, player: Player):
        self.is_deleted = True
        self.background.remove_object(self)
        self.list_.remove(self)
        self.background.draw()

        if self.type == 0:
            player.bomb_max += 1
            # TODO move check player max_bomb to setter
        elif self.type == 1 and player.bomb_max > 1:
            player.bomb_max -= 1
        elif self.type == 2:
            player.insensitivity_on()
        elif self.type == 3:
            player.speed *= 1.5
            print("Speed:", player.speed)
            # TODO move check player max_bomb to setter
        elif self.type == 4 and player.speed > 1.5:
            player.speed = player.speed / 150 * 100
            if player.speed < 1.5: player.speed = 1.5
            print("Speed:", player.speed)
        elif self.type == 5:
            player.ability_to_kick = True
        elif self.type == 6:
            self.level.change_direction = random.randint(1, 3)
            print(f"Direction changed by {self.level.change_direction}")
            Events.rise_event(Events.EVENT_POWERUP_CHANGE_DIRECTION, 8000)
        elif self.type == 7:
            player.bomb_power += 1
