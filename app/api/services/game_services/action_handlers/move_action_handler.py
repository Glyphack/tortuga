from app.schemas.game_schema import Positions, Action
from .action_handler import ActionHandler


class MoveActionHandler(ActionHandler):
    def execute(self):
        move_where = self.payload.move_where
        player_position = self.game.players_position.get(self.player)
        assert self.game.is_empty(move_where)
        if player_position in Positions.jr_positions():
            assert move_where == Positions.JR_B
        elif player_position in Positions.fd_positions():
            assert move_where == Positions.FD_B
        elif player_position in Positions.tr_positions():
            assert move_where in [Positions.FD_B, Positions.JR_B]
        elif player_position == Positions.JR_B:
            assert move_where in [Positions.TR, Positions.JR]
        elif player_position == Positions.FD_B:
            assert move_where in [Positions.FD, Positions.TR]

        self.game.set_position(self.player, move_where)
        self.game.next_turn()
        self.game.last_action = Action(
            action_type=Action.ActionType.MOVE,
        )
