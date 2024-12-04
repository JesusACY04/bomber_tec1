import pygame


class Object(pygame.Rect):

    def __init__(self, game, level, cords: list[float, float],
                 image: pygame.Surface,
                 possibility_of_entry: bool = False,
                 rect_offset: tuple[int, int] = (0, 0),
                 rect_size: tuple[int, int] = None):
        self.game = game
        self.level = level
        self.cords = cords
        self.rect_offset: tuple = rect_offset
        self.rect_size: tuple = (self.game.size, self.game.size) if rect_size is None else rect_size
        super().__init__((self.cords[0] + self.rect_offset[0], self.cords[1] + self.rect_offset[1]), self.rect_size)
        self.image = image  # type: pygame.Surface
        self.possibility_of_entry = possibility_of_entry
        self.draw()

    def can_entry(self): return self.possibility_of_entry

    def can_kick(self): return False

    def kick(self, direction: int): pass

    def get_image(self): return self.image

    def get_cords(self): return self.cords

    def draw(self):
        self.game.display.blit(self.image, self.cords)
        self.game.to_update.append(self)

    def set_image(self, image: pygame.Surface):
        self.image = image

    def destroy(self, time=0):
        return False

    def delete(self): pass

    def __str__(self):
        return f"{self.__class__}:{super().__str__()}"

    def __repr__(self):
        return f"{self.__class__}:{super().__repr__()}"
