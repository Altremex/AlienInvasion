import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, ai_game):
        """Creamos una bala en la posicion actual del jugador"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Creamos una bala rect enn 0,0 y luego ponemos la posicion correcta
        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height
        )
        self.rect.midtop = ai_game.player.rect.midtop

        # Guardamos la posicion de la bala en un float
        self.y = float(self.rect.y)

    def update(self):
        """Mover la bala en la pantalla"""
        # Actualizar la posicion de la bala
        self.y -= self.settings.bullet_speed
        # Actualizamos la posicion rect
        self.rect.y = int(self.y)

    def draw_bullet(self):
        """Dibujar la bala en la pantalla"""
        pygame.draw.rect(self.screen, self.color, self.rect)