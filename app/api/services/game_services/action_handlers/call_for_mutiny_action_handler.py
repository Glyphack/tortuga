from app.schemas.game_schema import Positions, Action, CallForMutinyActionData, \
    State
from .action_handler import ActionHandler


class CallForMutinyActionHandler(ActionHandler):
    @property
    def activity_text(self):
        return f"player {self.player} called fer a mutiny," \
               f"waitin' fer vote: {self._get_participating_players()}"

    def execute(self):
        player_position = self.game.players_position[self.player]
        if player_position in Positions.jr_positions():
            assert player_position == Positions.JR2
            captain = self.game.get_jr_caption()
        elif player_position in Positions.fd_positions():
            assert player_position == Positions.FD2
            captain = self.game.get_fd_caption()
        else:
            raise AssertionError

        action = Action(
            action_type=Action.ActionType.CALL_FOR_A_MUTINY,
            action_data=CallForMutinyActionData(
                captain=captain,
                participating_players=self._get_participating_players(),
                state=State.InProgress
            )
        )

        self.game.last_action = action

    def _get_participating_players(self):
        player_position = self.game.players_position[self.player]
        if player_position in Positions.jr_positions():
            positions = Positions.jr_positions()
            positions.remove(Positions.JR1)
        else:
            positions = Positions.fd_positions()
            positions.remove(Positions.FD1)
        return [
            player
            for player, position in self.game.players_position.items()
            if position in positions
        ]
