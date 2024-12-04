import pygame


class Button(pygame.Rect):

    def __init__(self, game, menu, cords: tuple[int, int],
                 size: tuple[int, int],
                 image: pygame.Surface,
                 function, center=False):
        self.game = game
        self.menu = menu
        self.function = function

        super().__init__(cords, (size[0] if size[0]>20 else size[0]+20,size[1]))
        self.image = image  # type: pygame.Surface
        if center: self.center = cords

        self.draw()
        self.a = 15

    def draw(self):
        self.game.display.blit(self.image, self.topleft)
        self.game.to_update.append(self)

    def set_image(self, image: pygame.Surface):
        self.image = image

    def click(self, position) -> bool:
        if self.collidepoint(position) and self.function is not None:
            self.function()
            return True
        return False

    def __str__(self):
        return f"{self.__class__}:{super().__str__()}"

    def __repr__(self):
        return f"{self.__class__}:{super().__repr__()}"


class Button1(Button):
    def __init__(self, game, menu, cords: tuple[int, int],
                 size: tuple[int, int],
                 image: pygame.Surface,
                 function, params, center=False):
        super().__init__(game, menu, cords,
                         size, image,
                         function, center)
        self.params = params

    def click(self, position) -> bool:
        if self.collidepoint(position) and self.function is not None:
            self.function(self.params)
            return True
        return False

