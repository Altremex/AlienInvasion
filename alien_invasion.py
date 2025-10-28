import sys
import pygame
from settings import Settings
from player import Player
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:

    def __init__(self):
        """Iniciamos el juego y creamos los recursos"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.game_active=False

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )

        pygame.display.set_caption("Alien Invasion")

        #Crear el boton de juego
        self.play_button= Button(self, "Play")

        #Creamos una instancia para guardar las estadisticas
        self.stats = GameStats(self)
        self.sb= Scoreboard(self)

        self.player = Player(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def _create_fleet(self):
        """Creamos una flota de aliens"""
        #Creamos un alien y seguimos añadiendo hasta que no tengamos espacio
        #El espacio entre cada alien en 1 alien width y 1 alien heigh
        alien=Alien(self)
        alien_width , alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y <(self.settings.screen_height - 4 * alien_height):
            while current_x < (self.settings.screen_width -2 *alien_width):
                self._create_alien(current_x, current_y)
                current_x+= 2* alien_width

            #Terminamos una fila, reset valor x e incrementamos y
            current_x=alien_width
            current_y+=2*alien_height



    def _create_alien(self, x_position, y_position):
        new_alien=Alien(self)
        new_alien.x=x_position
        new_alien.rect.x= x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """Responder de manera correcta si un alien choca con las esquinas"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *=-1


    def run_game(self):
        """Iniciamos el main loop del juego"""
        while True:
            self._check_events()
            if self.game_active:

                self.player.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screem()
            self.clock.tick(60)

    def _update_bullets(self):
        """Actualiza la posicion de la bala y elimina las viejas balas"""
        self.bullets.update()

        #Borrar las balas que ya no aparecen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):


        collisions= pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #Aumenta nivel
            self.stats.level += 1
            self.sb.prep_level()




    def _update_aliens(self):
        """Actualiza la posicion del alien en la flota"""
        self._check_fleet_edges()
        self.aliens.update()

        #Checar si hubo colisiones
        if pygame.sprite.spritecollideany(self.player, self.aliens):
            self._alien_hit()

        self._check_aliens_botttom()

    def _alien_hit(self):
        """Responder de manera correcta al chocar con un alien"""

        if self.stats.players_left > 0:
        #Decremento de naves restantes
            self.stats.players_left-=1
            self.sb.prep_players()

            #Eliminar cualquier bala y alien restante
            self.bullets.empty()
            self.aliens.empty()

            #Crear una nueva flota y centar el personaje
            self._create_fleet()
            self.player.center_player()
            #Pausar
            sleep(0.5)
        else:
            self.game_active=False
            pygame.mouse.set_visible(True)

    def _check_events(self):
        """Responde a keypresses y mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type== pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """Inicia el juego solo si el botón Play fue presionado y el juego está inactivo."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.settings.initialize_dynamic_settings()
            # Reiniciamos las estadísticas del juego
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_players()
            self.game_active = True
            #Escondemos el cursor
            pygame.mouse.set_visible(False)

            self.bullets.empty()
            self.aliens.empty()

            self._create_fleet()
            self.player.center_player()

    def _check_keydown_events(self, event):
        """Responde al presionar teclas"""
        if event.key == pygame.K_RIGHT:
            # Movemos al jugador a la derecha
            self.player.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.player.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.player.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.player.moving_left = False


    def _fire_bullet(self):
        """Creamos una nueva bala y la añadimos al grupo de balas"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet= Bullet(self)
            self.bullets.add(new_bullet)

    def _check_aliens_botttom(self):
        """Cehcar si aliens tocaron el hasta abajo de la pantalla"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._alien_hit()
                break



    def _update_screem(self):
        # Redibuja la pantalla durante cada pse del loop
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.player.blitme()
        self.aliens.draw(self.screen)

        self.sb.show_score()

        #Dibuja el boton de jugar
        if not self.game_active:
            self.play_button.draw_button()
        pygame.display.flip()




if __name__ == "__main__":

    # Haz una instancia del juego y corre el juego
    ai = AlienInvasion()
    ai.run_game()
