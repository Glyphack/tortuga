import abc
from typing import List

from app.models.game import Game
from app.schemas.game_schema import PayloadType


class EventCardHandler:
    def __init__(self, game: Game, player: str, payload: PayloadType, option= None):
        self.game = game
        self.player = player
        self.payload = payload
        self.option = option

    @abc.abstractmethod
    def reveal(self):
        raise NotImplemented

    def set_option(self, option):
        self.option = self.options[option - 1]

    @property
    @abc.abstractmethod
    def options(self) -> List:
        raise NotImplemented

    @property
    @abc.abstractmethod
    def can_keep(self):
        return False
