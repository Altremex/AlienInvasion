import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Una clase que representa un alien"""

    def __init__(self, ai_game):
        super().__init__()
        self.screen= ai_game.screen
        self.settings=ai_game.settings

        #Cargamos la imagen de la nave espacial
        self.image=pygame.image.load('images/spaceship.png')
        self.image = pygame.transform.scale(
            self.image, (60, 60)
        )  # cambiamos el tamaño del personaje
        self.rect= self.image.get_rect()

        #Creamos un nuevo alien en la esquina izq
        self.rect.x=self.rect.width
        self.rect.y = self.rect.height

        #Guardamos la posicion horizontal
        self.x= float(self.rect.x)

    def check_edges(self):
        """Regresar True si el alien toco la esquina"""
        screen_rect= self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <=0)


    def update(self):
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x=int(self.x)