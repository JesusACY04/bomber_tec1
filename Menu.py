from copy import copy
import pygame
from Button import *
from Player import Player
from Text import Text


class Menu:
    def __init__(self, game):
        self.game = game
        self.background = pygame.image.load("img/menu/background.png")
        self.background = pygame.transform.scale(self.background, (self.game.display_size[0], self.game.display_size[1]))
        self.background_rect = pygame.Rect((0, 0), (self.game.display_size[0], self.game.display_size[1]))

        # Configuración de fuentes con tamaños ajustados
        font_name = "forte" if "forte" in pygame.font.get_fonts() else None
        self.font = pygame.font.SysFont(font_name, 35, bold=True)  # Tamaño reducido para títulos
        self.font2 = pygame.font.SysFont(font_name, 20, bold=True)  # Tamaño reducido para botones de teclas
        self.key_listening = False
        self.key_cord = None

        # Estados de la pantalla: 0 - menú, 1 - configuración
        self.screen = 0

        # Listas de objetos de menú y configuración
        self.menu_object = []
        self.settings_object = []
        self.add_menu_object()
        self.add_settings_object()
        self.draw()

    def add_menu_object(self):
        # Botón de inicio
        img = pygame.image.load("img/menu/button_start.png")
        self.menu_object.append(
            Button(self.game, self, (427, 160), (84, 50), img,
                   self.game.start_lvl,
                   True
                   ))
        # Botón de configuración
        img = pygame.image.load("img/menu/button_settings.png")
        self.menu_object.append(
            Button(self.game, self, (427, 220), (153, 50), img,
                   self.go_to_settings,
                   True
                   ))

    def add_settings_object(self):
        # Mostrar nombres de jugadores con tamaño de fuente ajustado
        for i in range(2):
            img = self.font.render(f"Jugador {i + 1}", True, (0, 0, 255))  # Azul para los nombres de los jugadores
            self.settings_object.append(
                Text(self.game, self,
                     (30, 150 + i * 80), img.get_size(),
                     img
                     )
            )
        # Nombres de las teclas de control en español
        key_names = ["Izquierda", "Arriba", "Derecha", "Abajo", "Bomba"]
        for i, key_name in enumerate(key_names):
            img = self.font.render(key_name, True, (0, 0, 0))  # Negro para los nombres de las teclas
            self.settings_object.append(
                Text(self.game, self,
                     (230 + 135 * i, 100), img.get_size(),
                     img, True
                     )
            )
        # Botones de configuración de teclas con tamaño de fuente ajustado
        for i in range(2):
            for j in range(5):
                key = Player.key_player[i][j]
                img = self.font2.render(
                    self.key_to_str(key),
                    True,
                    (0, 0, 0)  # Negro para las teclas de control
                )
                self.settings_object.append(
                    Button1(self.game, self,
                            (230 + 135 * j, 175 + i * 80), img.get_size(),
                            img,
                            self.change_player_button_click,
                            [i, j], True
                            )
                )
        # Botón de regresar con tamaño de fuente ajustado
        try:
            img = pygame.image.load("img/menu/button_settings.png")
        except FileNotFoundError:
            print("Advertencia: No se encontró la imagen de 'button_settings.png'. Usando una imagen predeterminada.")
            img = pygame.Surface((153, 50))
            img.fill((200, 200, 200))  # Color de fondo de reemplazo
        self.settings_object.append(
            Button(self.game, self, (300, 500), (153, 50), img,
                   self.go_to_menu,
                   True
                   ))

    def change_player_button_click(self, params):
        """Inicia la escucha de una tecla para cambiar la asignación."""
        self.key_cord = params
        self.key_listening = True

    def change_player_button_button(self, key):
        """Cambia la tecla asignada a la posición actual si no está en uso."""
        if not any(key in pk for pk in Player.key_player):
            i, j = self.key_cord
            Player.key_player[i][j] = key
            img = self.font2.render(
                self.key_to_str(key),
                True,
                (0, 0, 0)
            )
            button = Button1(self.game, self,
                             (230 + 135 * j, 175 + i * 80), img.get_size(),
                             img,
                             self.change_player_button_click,
                             [i, j], True
                             )

            # Actualiza el botón en la lista de configuración
            self.settings_object[4 + 5 + i * 5 + j] = button
            self.key_listening = False
            self.draw()

    def draw(self):
        """Dibuja el fondo y los elementos del menú o configuración en la pantalla."""
        self.game.display.blit(self.background, (0, 0))
        self.game.to_update.append(self.background_rect)
        if self.screen == 0:
            for obj in self.menu_object:
                obj.draw()
        elif self.screen == 1:
            for obj in self.settings_object:
                obj.draw()

    def next_frame(self, delta_time):
        """Maneja los eventos de la pantalla actual."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.key_listening = False
                pos = pygame.mouse.get_pos()
                if self.screen == 0:
                    for obj in self.menu_object:
                        obj.click(pos)
                elif self.screen == 1:
                    for obj in self.settings_object:
                        obj.click(pos)

            if self.key_listening and event.type == pygame.KEYDOWN:
                key = event.key
                self.change_player_button_button(key)

    def go_to_settings(self):
        """Cambia la pantalla a la sección de configuración."""
        self.screen = 1
        self.draw()

    def go_to_menu(self):
        """Cambia la pantalla de regreso al menú principal."""
        self.screen = 0
        self.draw()

    @staticmethod
    def key_to_str(key):
        """
        Devuelve el nombre de la tecla en español.
        """
        key_names = {
            pygame.K_LEFT: "Left",
            pygame.K_UP: "Up",
            pygame.K_RIGHT: "Right",
            pygame.K_DOWN: "Down",
            pygame.K_LCTRL: "Ctrl",
            pygame.K_RCTRL: "Ctrl",
            pygame.K_LALT: "Alt",
            pygame.K_RALT: "Alt",
            pygame.K_a: "A",
            pygame.K_w: "W",
            pygame.K_d: "D",
            pygame.K_s: "S",
            pygame.K_SPACE: "Espacio",
            pygame.K_h: "H",
            pygame.K_u: "U",
            pygame.K_k: "K",
            pygame.K_j: "J"
        }
        return key_names.get(key, "Desconocido")
