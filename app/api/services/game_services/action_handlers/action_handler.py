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

    def do_action(self):
        self.execute()
        if self.activity_text:
            self.game.add_activity(self.activity_text)

    @abstractmethod
    def execute(self):
        raise NotImplemented

    @property
    @abstractmethod
    def activity_text(self):
        raise NotImplementedError()
