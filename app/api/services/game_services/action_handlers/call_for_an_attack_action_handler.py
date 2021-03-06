from typing import Dict

from app.api.services.game_services.action_handlers.action_handler import (
    ActionHandler
)
from app.schemas import game_schema


class CallForAnAttackActionHandler(ActionHandler):
    @property
    def activity_text(self):
        return f"player {self.player} called fer an attack," \
               f"waitin' fer vote: " \
               f"{self.get_attack_call_participating_players()}"

    def execute(self):
        assert self.game.players_position.get(self.player) in [
            game_schema.Positions.JR1,
            game_schema.Positions.FD1,
        ]

        participating_players = self.get_attack_call_participating_players()
        from_other_ship = True
        if self.game.chests_position.sg_nt > 0:
            from_other_ship = False

        action = game_schema.Action(
            action_type=game_schema.Action.ActionType.CALL_FOR_AN_ATTACK,
            action_data=game_schema.CaptainCallForAttackData(
                state=game_schema.State.InProgress,
                participating_players=participating_players,
                which_captain=game_schema.User(username=self.player),
                from_other_ship=from_other_ship
            )
        )
        self.game.last_action = action

    def get_attack_call_participating_players(self):
        positions = []
        players_position = self.game.players_position
        captain = self.player
        if players_position.get(captain) == game_schema.Positions.JR1:
            positions = game_schema.Positions.jr_positions()
        elif players_position.get(captain) == game_schema.Positions.FD1:
            positions = game_schema.Positions.fd_positions()
        return [
            player
            for player, position in players_position.items()
            if position in positions
        ]
