from app.models.event_cards import EventCardsManager
from app.schemas.game_schema import Action
from .action_handler import ActionHandler
from ..event_card_handlers import event_card_handlers


class UseEventCardActionHandler(ActionHandler):
    @property
    def activity_text(self):
        event_card = EventCardsManager.get(
            self.payload.event_card_to_use
        )
        return f"{self.player} used " \
               f"{event_card.title}"

    def execute(self):
        event_card = event_card_handlers[self.payload.event_card_to_use](
            self.game, self.player
        )
        assert event_card.can_use
        if self.payload.event_card_option_index is not None:
            event_card.chosen_option = self.payload.event_card_option_index
        event_card.reveal()
        player_info = self.game.get_player_info(self.player)
        event_card_slug = self.payload.event_card_to_use
        if player_info.has_event_card(event_card_slug):
            player_info.remove_event_card(event_card_slug)
        if not self.game.has_unfinished_voting():
            self.game.last_action = Action(
                action_type=Action.ActionType.USE_EVENT_CARD,
            )
        if self.payload.event_card_to_use in ["atlantis", "el-dorado"]:
            return
        self.game.next_turn()
