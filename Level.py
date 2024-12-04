import pygame
from Field import Field
from Player import Player
from Bomb import Bomb
from Events import *
from PowerUp import PowerUp
from Wall import Wall


class Level:

    def __init__(self, game, lvl_name):
        self.game=game

        # load lvl
        self.lvl_name = lvl_name
        self.background = []
        self.walls_list = []
        self.load_map(self.lvl_name)

        # player start position
        psc = [[1, 1], [17, 1], [1, 11], [17, 11]]

        # TODO add number of player settings
        # creating player
        number_player = 2
        self.all_players: list[Player] = list(
            Player(self.game,
                   self, [psc[i][0] * self.game.size, psc[i][1] * self.game.size],
                   i) for i in range(number_player)
        )
        self.alive_players: list[Player] = list(self.all_players)
        self.dead_players: list[Player] = []




        # game param
        self.change_direction = 0

        # ending
        self.ending_scane = None
        self.is_end = False

        # frames per second setting

        pygame.display.update()

        # 0 - normal play, 1 - last standing, 2 ending scene
        self.state = 0

    def load_map(self, lvl_name):
        self.background = []

        for i in range(self.game.fields_size[0]):
            self.background.append([])
            for j in range(self.game.fields_size[1]):
                self.background[i].append(0)

        # TODO make validation opened file
        file_map = open(f"map/{lvl_name}", "r")
        graphic_type = file_map.readline()[:-1]
        number_of_images = int(file_map.readline()[:-1])
        number_of_map_lines = int(file_map.readline()[:-1])

        Field.load_images(graphic_type, number_of_images)
        Wall.load_images(graphic_type)

        # TODO check if there is that folder
        for row in range(number_of_map_lines):
            line = file_map.readline()
            for column, field in enumerate(line.split()):
                self.background[column][row] = Field(self.game, self, int(field), [self.game.size * column, self.game.size * row])

        # load wall cords
        walls_cord = file_map.readline().split(";")
        for cords in walls_cord:
            self.walls_list.append(Wall(self.game, self, list(map(int, cords.split(",")))))

    def remove_player(self, player):
        self.alive_players.remove(player)
        self.dead_players.append(player)

    def end(self):
        f = pygame.font.SysFont("Arial", 60, True)
        if len(self.alive_players) == 1:
            text = f"JUGADOR {self.alive_players[0].id} GANÓ"
            img = f.render(text, True, (255, 215, 0))  # Color dorado
        else:
            text = f"EMPATE"
            img = f.render(text, False, (255, 0, 0))

        rect = pygame.Rect(0, 0, img.get_width() + 20, img.get_height() + 20)
        rect.center = (self.game.display_size[0] // 2, self.game.display_size[1] // 2)
        pygame.draw.rect(self.game.display, (0, 0, 0, 30), rect)  # Fondo negro semitransparente
        self.game.to_update.append(rect)
        self.game.display.blit(img, img.get_rect(center=rect.center))
        

        rise_event(LEVEL_BACK_TO_MENU, 5000)

    def next_frame(self, delta_time):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                print(event.key)
                for p in self.alive_players:
                    p.press_key(event.key)
            elif event.type == pygame.KEYUP:
                for p in self.alive_players:
                    p.release_key(event.key)


            elif event.type == EVENT_POWERUP_CHANGE_DIRECTION:
                print("Cambiar dirección restablecer")
                self.change_direction = 0
            elif event.type == EVENT_LAST_PLAYER and self.state == 1:
                self.end()
                self.state = 2
            elif event.type == LEVEL_BACK_TO_MENU and self.state == 2:
                self.game.end_lvl()
                return
        if not self.is_end:
            for p in self.alive_players: p.start_move()
            for p in self.alive_players: p.hide()
            for b in Bomb.list_: b.hide()

            for p in self.alive_players: p.move_object()
            for b in Bomb.list_: b.move_object()

            for b in Bomb.list_: b.change_timer(delta_time)
            for p in self.alive_players: p.change_timer(delta_time)
            for w in Wall.destroyed_walls: w.change_timer(delta_time)
            for w in Wall.destroyed_walls: w.draw()
            for u in PowerUp.list_: u.draw()
            for b in Bomb.list_: b.draw()
            for p in self.alive_players: p.draw()

            if len(self.alive_players) == 1 and self.state == 0:
                print("ÚLTIMO EN PIE")
                self.state = 1
                rise_event(EVENT_LAST_PLAYER, 2000)

    def get_background(self, position):  # type: (tuple[int, int])-> Field
        return self.background[position[0]][position[1]]