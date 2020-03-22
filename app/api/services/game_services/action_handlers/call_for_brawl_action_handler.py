from app.schemas import game_schema
from .action_handler import ActionHandler


class CallForBrawlActionHandler(ActionHandler):
    def execute(self):
        assert (
                self.game.players_position[self.player] ==
                game_schema.Positions.TR1
        )
        participating_players = self.get_attack_call_participating_players()

        action = game_schema.Action(
            action_type=game_schema.Action.ActionType.CALL_FOR_BRAWL,
            action_data=game_schema.CallForBrawlActionData(
                governer=self.player,
                participating_players=participating_players,
                state=game_schema.State.InProgress
            )
        )
        self.game.last_action = action

    def get_attack_call_participating_players(self):
        participating_players = []
        for player, position in self.game.players_position.items():
            if position in game_schema.Positions.tr_positions():
                participating_players.append(player)
        return participating_players
