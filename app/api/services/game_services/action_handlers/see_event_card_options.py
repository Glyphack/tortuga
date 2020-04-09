from app.schemas.game_schema import Action, SeeEventCardOptionsActionData
from .action_handler import ActionHandler
from ..event_card_handlers import event_card_handler


class SeeEventCardOptions(ActionHandler):
    def execute(self):
        event_card = event_card_handler[self.payload.event_card_to_see_slug](
            self.game, self.player, self.payload
        )
        action = Action(
            action_type=Action.ActionType.SEE_EVENT_CARD_OPTIONS,
            action_data=SeeEventCardOptionsActionData(
                options=event_card.options,
                can_use=event_card.can_use,
                player=self.player,
                event_card_slug=self.payload.event_card_to_see_slug
            )
        )
        self.game.last_action = action