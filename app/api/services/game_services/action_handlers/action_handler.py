from abc import abstractmethod

from app.models.game import Game
from app.schemas.game_schema import Action, PayloadType


class ActionHandler:
    def __init__(
            self,
            game: Game,
            player: str,
            action: Action,
            payload: PayloadType):
        self.game = game
        self.action = action
        self.player = player
        self.payload = payload

    @abstractmethod
    def execute(self):
        raise NotImplemented
