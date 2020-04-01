from typing import List

from .event_card_handler import EventCardHandler


class SpanishArmadaCard(EventCardHandler):
    def reveal(self):
        self.game.finish_game()

    def options(self) -> List:
        return []
