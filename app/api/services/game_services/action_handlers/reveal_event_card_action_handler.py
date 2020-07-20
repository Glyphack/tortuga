from app.models.event_cards import EventCardsManager, EventCard
from app.models.game import Game
from app.schemas.game_schema import Action, RevealOneEventCardActionData, \
    PayloadType
from .action_handler import ActionHandler
from app.api.services.game_services.event_card_handlers import (
    event_card_handlers
)


class RevealEventCardActionHandler(ActionHandler):
    def __init__(
            self,
            game: Game,
            player: str,
            action: Action,
            payload: PayloadType):
        super().__init__(game, player, action, payload)
        self.event_card: EventCard = self.revealed_event_card()

    @property
    def activity_text(self):
        return f"{self.player} revealed " \
               f"{self.payload.event_card_index} event card" \
               f"'n 'twas {self.event_card.title}"

    def execute(self):
        assert (
                self.game.turn == self.player or
                (
                        self.game.last_action and
                        self.game.last_action.action_data.forced_player ==
                        self.player
                )
        )
        event_card_class = event_card_handlers[self.event_card.slug](
            self.game, self.player, self.payload
        )
        self.game.last_action = Action(
            action_type=Action.ActionType.REVEAL_EVENT_CARD,
            action_data=RevealOneEventCardActionData(
                player=self.player,
                event_card=self.event_card,
                can_keep=event_card_class.can_keep,
                event_card_options=event_card_class.options,
                can_use=event_card_class.can_use
            )
        )
        self.game.event_cards.remove(self.event_card.slug)
        if not event_card_class.can_keep and not event_card_class.can_use:
            self.game.next_turn()
            event_card_class.reveal()

    def get_index_when_forced(self):
        return self.game.last_action.action_data.event_cards_indexes[
            self.payload.event_card_index
        ]

    def revealed_event_card(self) -> EventCard:
        if self.game.last_action and self.game.last_action.action_type == (
                Action.ActionType.FORCE_ANOTHER_PLAYER_TO_CHOOSE_CARD
        ):
            index = self.get_index_when_forced()
        else:
            index = self.payload.event_card_index

        return EventCardsManager.get(
            self.game.event_cards[index]
        )
