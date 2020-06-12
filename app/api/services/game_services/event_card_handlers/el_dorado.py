from typing import List

from .event_card_handler import EventCardHandler
from app.api.services.game_services.service import can_vote


class ElDorado(EventCardHandler):
    @property
    def slug(self):
        return "el-dorado"

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
        return (
                can_vote(self.game, self.player) and
                self.game.get_player_info(
                    self.player
                ).has_event_card(self.slug)
        )
