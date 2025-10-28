class Settings:
    """Una clase para todos los settings de la aplicacion"""

    def __init__(self):
        # Pantalla
        self.screen_width = 1000
        self.screen_height = 700
        self.bg_color = (18, 21, 57)

        # Jugador Settings
        self.player_speed = 14.5

        # Bullet settings
        self.bullet_speed = 7.2
        self.bullet_width = 10
        self.bullet_height = 17
        self.bullet_color = (245, 73, 39)
        self.bullets_allowed= 10

        #Alien settings
        self.alien_speed=5.0
        self.fleet_drop_speed=15
        self.player_limit=3
        #Fleet direction 1 representa derecha -1 representa izq
        self.fleet_direction=1

        #Que tan rapido el juego avanza
        self.speedup_scale=1.1

        #Que tan rapido los puntos incrementan
        self.score_scale=1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.player_speed=10.0
        self.bullet_speed=6.5
        self.alien_speed=4.0

        self.alien_points=50

        self.fleet_direction=1

    def increase_speed(self):
        self.player_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
