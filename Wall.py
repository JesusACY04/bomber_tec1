import pygame
from Object import Object
from PowerUp import PowerUp

IMAGES_NUMBER = 16


class Wall(Object):
    images = []
    destroyed_walls = []

    def __init__(self, game, level, position: list[int, int]):
        super().__init__(game, level,
                         [game.size * position[0], game.size * position[1]],
                         self.images[0])
        self.background = self.level.get_background(position)
        self.background.add_object(self)
        self.pos = position

        self.timer = 0
        self.state = 0
        self.state_timer = 0

        # Asegurar que el muro esté en walls_list al crearlo
        if self not in self.level.walls_list:
            self.level.walls_list.append(self)

    def change_timer(self, dt):
        self.timer -= dt
        if self.timer < 0:
            if self.state < IMAGES_NUMBER - 1:
                self.timer = self.state_timer
                self.state += 1
                self.image = self.images[self.state]
            elif self.state == IMAGES_NUMBER - 1:
                self.delete()

    def destroy(self, time=0):
        # Asegurar que no haya duplicados en destroyed_walls
        if self not in self.destroyed_walls:
            self.destroyed_walls.append(self)

        self.state_timer = time / (IMAGES_NUMBER - 1)
        self.timer = self.state_timer
        self.state = 1
        self.image = self.images[self.state]

        return True

    def delete(self):
        print(f"Eliminando muro: {self}")

        # Validar y eliminar de destroyed_walls
        if self in self.destroyed_walls:
            self.destroyed_walls.remove(self)
        else:
            print(f"Warning: {self} no está en destroyed_walls.")

        # Validar y eliminar de walls_list
        if self in self.level.walls_list:
            self.level.walls_list.remove(self)
        else:
            print(f"Warning: {self} no está en walls_list.")

        # Remover el objeto del fondo y dibujar nuevamente
        self.background.remove_object(self)
        self.background.draw()

        # Crear PowerUp después de eliminar el muro
        PowerUp.create(self.game, self.level, self.pos)

    @staticmethod
    def load_images(graphic_type):
        Wall.images = list(pygame.image.load(f'map/{graphic_type}/w{i}.bmp') for i in range(IMAGES_NUMBER))
