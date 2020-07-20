from app.api.services.game_services.action_handlers import action_handler
from app.schemas import game_schema


class ForceAnotherPlayerToChooseCard(action_handler.ActionHandler):
    @property
    def activity_text(self):
        return f"player {self.player} forced {self.payload.forced_player}" \
               f"t' reveal a event card from event cards " \
               f"{self.payload.event_cards_indexes}"

    def execute(self):
        self.game.last_action = game_schema.Action(
            action_type=game_schema.Action.ActionType.FORCE_ANOTHER_PLAYER_TO_CHOOSE_CARD,
            action_data=game_schema.ForceAnotherPlayerToChooseCardActionData(
                player=self.player,
                forced_player=self.payload.forced_player,
                event_cards_indexes=self.payload.event_cards_indexes
            )
        )
