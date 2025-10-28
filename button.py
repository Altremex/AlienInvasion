import pygame.font

class Button:
    """Clase que crea un boton para jugar"""
    def __init__(self, ai_game, msg):
        """Atributos del boton"""
        self.screen=ai_game.screen
        self.screen_rect=ai_game.screen.get_rect()

        #Dimensiones y propiedades del boton
        self.width, self.height= 200,50
        self.buttton_color=(0,135,0)
        self.text_color=(255,255,255)
        self.font=pygame.font.SysFont('None',48)

        #Crear el boton y centrarlo
        self.rect= pygame.Rect(0,0,self.width,self.height)
        self.rect.center= self.screen_rect.center

        #El mensaje del boton solo aparece una vez
        self.prep_msg(msg)

    def prep_msg(self,msg):
        self.msg_image= self.font.render(msg, True, self.text_color, self.buttton_color)
        self.msg_image_rect= self.msg_image.get_rect()
        self.msg_image_rect.center= self.rect.center

    def draw_button(self):
        self.screen.fill(self.buttton_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)