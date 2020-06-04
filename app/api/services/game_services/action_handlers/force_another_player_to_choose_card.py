from app.api.services.game_services.action_handlers import action_handler
from app.api.services.game_services.event_card_handlers import (
    event_card_handlers
)
from app.models.event_cards import EventCardsManager
from app.schemas import game_schema


class ForceAnotherPlayerToChooseCard(action_handler.ActionHandler):
    def execute(self):
        event_card = EventCardsManager.get(
            self.game.event_cards[self.payload.event_card_index]
        )
        event_card_class = event_card_handlers[event_card.slug](
            self.game, self.player, self.payload
        )
        self.game.last_action = game_schema.Action(
            action_type=game_schema.Action.ActionType.REVEAL_EVENT_CARD,
            action_data=game_schema.ForceAnotherPlayerToChooseCardActionData(
                player=self.player,
                forced_player=self.payload.forced_player,
                event_card_index=self.payload.event_card_index,
                event_card_options=event_card_class.options,
                can_keep=event_card_class.can_keep,
                can_use=event_card_class.can_use
            )
        )
        self.game.event_cards.remove(event_card.slug)
        if not event_card_class.can_keep and not event_card_class.can_use:
            self.game.next_turn()
            event_card_class.reveal()
