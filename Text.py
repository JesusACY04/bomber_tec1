import pygame


class Text(pygame.Rect):

    def __init__(self, game, menu, cords: tuple[int, int],
                 size: tuple[int, int],
                 image: pygame.Surface,
                 center=False):
        self.game = game
        self.menu = menu

        super().__init__(cords, size)
        self.image = image  # type: pygame.Surface
        if center: self.center = cords

        self.draw()

    def draw(self):
        self.game.display.blit(self.image, self.topleft)
        self.game.to_update.append(self)

    def set_image(self, image: pygame.Surface):
        self.image = image

    def click(self, temp):pass

    def __str__(self):
        return f"{self.__class__}:{super().__str__()}"

    def __repr__(self):
        return f"{self.__class__}:{super().__repr__()}"
