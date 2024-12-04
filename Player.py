import pygame
from MovableObject import MovableObject
from Bomb import Bomb
from Field import Field


# TODO somethings wrong when press 4 keys for one player (probably hardware)


class Player(MovableObject):
    key_player = [
        [pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_RCTRL],
        [pygame.K_a, pygame.K_w, pygame.K_d, pygame.K_s, pygame.K_LALT],
    ]

    def __init__(self, game, level, cords, number):
        self.id = number
        self.images = []
        self.load_images()
        self.insensitivity_timer = 0
        self.insensitivity = False

        super().__init__(game, level, cords, self.images[0], True, (9, 1), (25, 43))
        self.my_background[0].number_of_player += 1

        self.speed = 1.5
        self.key = Player.key_player[self.id]

        print(self.id)
        print(self.position, self.x, self.y, self.cords)

        self.bomb_counter = 0
        self.bomb_max = 1
        self.bomb_power = 1

        self.pressed_key = []

        self.lives = 1

        # TODO change name
        self.ability_to_kick = False

    def load_images(self):
        self.images = [
            [pygame.image.load(f"img\\player\\player_{self.id}_stay.png"),
             pygame.image.load(f"img\\player\\player_{self.id}_go.png")
             ],
            []
        ]
        for i in self.images[0]:
            temp = i.copy()
            temp.set_alpha(127, 0)
            self.images[1].append(temp)

    def draw(self):
        if 10 < self.distance_to_move < 35:
            self.image = self.images[self.insensitivity][1]
        else:
            self.image = self.images[self.insensitivity][0]
        super().draw()

    def press_key(self, key):
        if key in self.key:
            k_index = self.key.index(key)
            if k_index == 4:
                self.plant_bomb()
            else:
                if k_index in self.pressed_key: self.pressed_key.remove(k_index)
                self.pressed_key.append(self.key.index(key))
        print(self.pressed_key)

    def plant_bomb(self):
        if self.bomb_max > self.bomb_counter and self.background[self.position[0]][self.position[1]].can_entry():
            Bomb.list_.append(Bomb(self.game, self.level, self.position, self, self.bomb_power))
            self.bomb_counter += 1

    def release_key(self, key):
        if key in self.key and self.key.index(key) < 4:
            self.pressed_key.remove(self.key.index(key))
        print(self.pressed_key)

    def set_move_parameters(self, destination, next_background: Field, direction=0):
        self.direction = direction
        super().set_move_parameters(destination, next_background)

        self.my_background[-1].number_of_player += 1
        # print()
        # print(f"{self.my_background[0].cords} Num of player: {self.my_background[0].number_of_player}")
        # print(f"{self.my_background[1].cords} Num of player: {self.my_background[1].number_of_player}")

    def start_move(self):

        if self.movement == 0 and len(self.pressed_key):
            for key in self.pressed_key[::-1]:
                if self.reaction_for_key(key):
                    self.direction = (key + self.level.change_direction) % 4
                    break

    def reaction_for_key(self, key):
        x, y = self.position
        index = (key + self.level.change_direction) % 4
        if index == 0:
            x -= 1
        elif index == 1:
            y -= 1
        elif index == 2:
            x += 1
        elif index == 3:
            y += 1
        entry = self.background[x][y].can_entry()
        kick = self.ability_to_kick and self.background[x][y].can_kick()

        if entry:
            self.set_move_parameters((x * self.game.size, y * self.game.size), self.background[x][y], 0)
            return True
        elif kick and self.background[x][y].kick(index):
            return True
        return False

    def end_move(self):
        self.my_background[0].number_of_player -= 1
        # print(f"{self.my_background[0].cords} Num of player: {self.my_background[0].number_of_player}")
        # print(f"{self.my_background[1].cords} Num of player: {self.my_background[1].number_of_player}")
        super().end_move()

    def destroy(self, time=0):
        if not self.insensitivity:
            self.lives -= 1
            if self.lives == 0:
                self.level.remove_player(self)
                self.hide()
        return False

    def collect(self, powerup):
        powerup.collect(self)

    def insensitivity_on(self):
        self.insensitivity = True
        print(f"Player {self.id} insensitivity {self.insensitivity}")
        self.insensitivity_timer = 10000  # 10 second

    def change_timer(self, dt):
        self.insensitivity_timer -= dt
        if self.insensitivity_timer <= 0:
            self.insensitivity = False
