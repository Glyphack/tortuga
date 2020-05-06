from app.models.event_cards import EventCard
from app.schemas.game_schema import Action
from .action_handler import ActionHandler


class KeepEventCardActionHandler(ActionHandler):
    def execute(self):
        assert (
                self.game.last_action.action_type ==
                Action.ActionType.REVEAL_EVENT_CARD
        )
        assert (
                self.game.last_action.action_data.can_keep is True and
                self.game.last_action.action_data.player == self.player
        )
        event_card = self.game.last_action.action_data.event_card
        self.game.players_info[self.player].event_cards.append(
            event_card.slug
        )
        self.game.last_action = Action(
            action_type=Action.ActionType.KEEP_EVENT_CARD,
        )
        self.game.next_turn()
