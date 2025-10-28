class GameStats:
    """Lleva recuento del juego"""

    def __init__(self, ai_game):
        """Inicamos las estadisticas"""
        self.high_score=0
        self.settings= ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        self.players_left= self.settings.player_limit
        self.score=0
        self.level=1