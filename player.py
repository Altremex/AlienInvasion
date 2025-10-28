import pygame
import os
from pygame.sprite import Sprite


class Player(Sprite):
    """Una clase para manejar al jugador"""

    def __init__(self, ai_game):
        super().__init__()
        # El jugador (Player) usará la misma pantalla (screen) que el juego principal (AlienInvasion)
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Carga todas las imagenes de la animacion de disparo
        self.image = pygame.image.load("images/GunGirl_shoot_02.png")  # 300*260
        self.image = pygame.transform.scale(
            self.image, (200, 160)
        )  # cambiamos el tamaño del personaje

        self.rect = self.image.get_rect()

        # Cargar al jugador en el centro de la pantalla
        self.rect.midbottom = self.screen_rect.midbottom

        # Guardar un float para la exacta posicion horizontal del jugador
        self.x = float(self.rect.x)


        self.moving_right = False
        self.moving_left = False

    def center_player(self):
        self.rect.midbottom=self.screen_rect.midbottom
        self.x=float(self.rect.x)

    def update(self):
        """Actualizamos la posicion del jugador basado en float"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.player_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.player_speed

        # Sincronizamos el rect(entero) con la posicion float
        self.rect.x = int(self.x)

    def blitme(self):
        """Dibuja al jugador en su posicion actual"""
        self.screen.blit(self.image, self.rect)
