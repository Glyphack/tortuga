from typing import List

from app.api.services.game_services.event_card_handlers import EventCardHandler
from app.api.services.game_services.service import can_vote


class ElDorado(EventCardHandler):
    def reveal(self) -> None:
        self.game.last_action.action_data.participating_players.append(
            self.player
        )

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
        return can_vote(self.game, self.player)
