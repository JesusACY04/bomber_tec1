import pygame

EVENT_POWERUP_CHANGE_DIRECTION = pygame.USEREVENT + 1
EVENT_LAST_PLAYER = pygame.USEREVENT + 2
LEVEL_BACK_TO_MENU = pygame.USEREVENT + 3


def creat_event(event_id: int, _dict: dict = None):
    return pygame.event.Event(event_id, _dict)


def rise_event(event_id: int, delay: int = 0):
    pygame.time.set_timer(pygame.event.Event(event_id), delay)
