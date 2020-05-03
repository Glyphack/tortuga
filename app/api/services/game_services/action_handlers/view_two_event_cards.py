from app.models.event_cards import EventCardsManager
from app.schemas.game_schema import Action, ViewTwoEventCardsActionData
from .action_handler import ActionHandler


class ViewTwoEventCardsActionHandler(ActionHandler):
    def execute(self):
        seen_event_cards = {}
        for event_card_index in self.payload.event_cards_indexes:
            seen_event_cards[event_card_index](
                EventCardsManager.get(
                    self.game.event_cards[event_card_index]
                )
            )

        self.game.last_action = Action(
            action_type=Action.ActionType.VIEW_TWO_EVENT_CARDS,
            action_data=ViewTwoEventCardsActionData(who_viewed=self.player)
        )
        self.game.players_info[self.player].seen_event_cards = seen_event_cards
        self.game.next_turn()
