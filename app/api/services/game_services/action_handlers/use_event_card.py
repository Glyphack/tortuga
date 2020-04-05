from app.schemas.game_schema import Action
from .action_handler import ActionHandler
from ..event_card_handlers import event_card_handler


class UseEventCardActionHandler(ActionHandler):
    def execute(self):
        event_card = event_card_handler[self.payload.event_card_to_use](
            self.game, self.player, self.payload,
        )
        if self.payload.event_card_option_index:
            event_card.chosen_option = self.payload.event_card_option_index - 1
        event_card.reveal()
        self.game.last_action = Action(
            action_type=Action.ActionType.USE_EVENT_CARD,
        )
        self.game.next_turn()
