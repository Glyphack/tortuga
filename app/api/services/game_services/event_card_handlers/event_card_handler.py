import abc
from typing import List

from app.models.game import Game
from app.schemas.game_schema import PayloadType


class EventCardHandler:
    def __init__(self, game: Game, player: str, payload: PayloadType):
        self.game = game
        self.player = player
        self.payload = payload
        self._chosen_option = None

    @abc.abstractmethod
    def reveal(self):
        raise NotImplemented

    @property
    def chosen_option(self):
        return self._chosen_option

    @chosen_option.setter
    def chosen_option(self, value):
        self._chosen_option = value

    @property
    @abc.abstractmethod
    def options(self) -> List:
        raise NotImplemented

    @property
    @abc.abstractmethod
    def options_operations(self) -> List:
        raise NotImplemented

    @property
    @abc.abstractmethod
    def can_keep(self):
        return False

    @property
    @abc.abstractmethod
    def can_use(self):
        raise NotImplemented
