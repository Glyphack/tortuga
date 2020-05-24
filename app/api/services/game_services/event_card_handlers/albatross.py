from typing import List

from .event_card_handler import EventCardHandler


class Albatross(EventCardHandler):
    def reveal(self) -> None:
        pass

    @property
    def options(self) -> List:
        return []

    @property
    def options_operations(self) -> List:
        return []

    @property
    def can_keep(self) -> bool:
        return True

    @property
    def can_use(self) -> bool:
        return False
