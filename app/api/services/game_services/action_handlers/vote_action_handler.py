from app.api.services.game_services.action_handlers.action_handler import (
    ActionHandler
)
from app.schemas import game_schema


class VoteActionHandler(ActionHandler):
    def execute(self):
        assert (
                self.game.last_action.action_type == game_schema.Action.ActionType.CALL_FOR_AN_ATTACK and
                self.game.last_action.action_data.state == game_schema.State.InProgress
        )
        vote_card = self.game.players_info.get(self.player).vote_cards.pop(
            self.payload.vote_card_index - 1
        )
        self.game.votes.fire += vote_card.fire
        self.game.votes.water += vote_card.water
        self.game.last_action.action_data.participating_players.remove(
            self.player
        )
        if len(self.game.last_action.action_data.participating_players) == 0:
            if self.game.votes.fire < self.game.votes.water:
                self.game.last_action.action_data.state = game_schema.State.Success
            else:
                self.game.last_action.action_data.state = game_schema.State.Failed


