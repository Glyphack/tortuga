from abc import abstractmethod

from app.models.game import Game
from app.schemas.game_schema import Action


class ActionHandler:
    def __init__(self, game: Game, player: str, action: Action):
        self.game = game
        self.action = action
        self.player = player

    @abstractmethod
    def execute(self):
        raise NotImplemented


