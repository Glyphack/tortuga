from typing import Dict

from app.api.services.game_services.action_handlers.action_handler import (
    ActionHandler
)
from app.schemas import game_schema


class CallForAnAttackActionHandler(ActionHandler):
    def execute(self):
        assert (
                self.game.players_position.get(
                    self.player) == game_schema.Positions.JR1 or
                self.game.players_position.get(
                    self.player) == game_schema.Positions.FD1
        )
        participating_players = self.get_attack_call_participating_players(
            players_position=self.game.players_position,
            captain=self.player
        )
        action = game_schema.Action(
            action_type=game_schema.Action.ActionType.CALL_FOR_AN_ATTACK,
            action_data=game_schema.CaptainCallForAttackData(
                state=game_schema.State.InProgress,
                participating_players=participating_players
            )
        )
        self.game.last_action = action

    @staticmethod
    def get_attack_call_participating_players(
            players_position: Dict[str, game_schema.Positions],
            captain: str):
        positions = []

        participating = []
        if players_position.get(captain) == game_schema.Positions.JR1:
            positions = [
                game_schema.Positions.JR1,
                game_schema.Positions.JR2,
                game_schema.Positions.JR3,
                game_schema.Positions.JR4,
                game_schema.Positions.JR5
            ]
        elif players_position.get(captain) == game_schema.Positions.FD1:
            positions = [
                game_schema.Positions.FD1,
                game_schema.Positions.FD2,
                game_schema.Positions.FD3,
                game_schema.Positions.FD4,
                game_schema.Positions.FD5
            ]
        for player, position in players_position.items():
            if position in positions:
                participating.append(player)
        return participating