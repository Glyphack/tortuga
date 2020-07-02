import abc
from typing import List, Optional

from app.schemas.game_schema import PayloadType


class EventCardHandler:
    def __init__(self, game: "Game", player: str,
                 payload: Optional[PayloadType] = None):
        self.game: "Game" = game
        self.player: str = player
        self.payload: PayloadType = payload
        self._chosen_option: Optional[int] = None

    @property
    def slug(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def reveal(self) -> None:
        raise NotImplementedError()

    @property
    def chosen_option(self) -> int:
        return self._chosen_option

    @chosen_option.setter
    def chosen_option(self, value) -> None:
        self._chosen_option = value

    @property
    @abc.abstractmethod
    def options(self) -> List:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def options_operations(self) -> List:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def can_keep(self) -> bool:
        return False

    @property
    @abc.abstractmethod
    def can_use(self) -> bool:
        raise NotImplementedError()
