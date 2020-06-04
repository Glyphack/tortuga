from app.api.services.game_services.action_handlers import action_handler
from app.schemas import game_schema


class ForceAnotherPlayerToChooseCard(action_handler.ActionHandler):
    def execute(self):
        self.game.last_action = game_schema.Action(
            action_type=game_schema.Action.ActionType.REVEAL_EVENT_CARD,
            action_data=game_schema.ForceAnotherPlayerToChooseCardActionData(
                player=self.player,
                forced_player=self.payload.forced_player,
                event_cards_indexes=self.payload.event_cards_indexes
            )
        )
