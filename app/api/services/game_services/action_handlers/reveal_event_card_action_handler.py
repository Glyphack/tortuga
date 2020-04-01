from app.models.event_cards import EventCardsManager
from app.schemas.game_schema import Action, RevealOneEventCardActionData
from .action_handler import ActionHandler
from .event_card_handlers import event_card_handler


class RevealEventCardActionHandler(ActionHandler):
    def execute(self):
        event_card = EventCardsManager.get(
            self.game.event_cards[self.payload.event_card_index - 1]
        )
        event_card_class = event_card_handler[event_card.slug](
            self.game, self.player, self.payload
        )
        event_card_class.reveal()
        self.game.last_action = Action(
            action_type=Action.ActionType.REVEAL_EVENT_CARD,
            action_data=RevealOneEventCardActionData(
                who=self.player,
                event_card=event_card,
                options=event_card_class.options()
            )
        )
        self.game.event_cards.remove(event_card.slug)
        if not event_card_class.options():
            self.game.next_turn()
