from app.schemas.game_schema import Positions, PutChestPayload
from .action_handler import ActionHandler


class PutChestActionHandler(ActionHandler):
    def execute(self):
        assert (
                self.game.players_info.get(self.player).chests > 0
        )
        team: PutChestPayload.Team = self.payload.which_team
        player_pos: Positions = self.game.players_position.get(
            self.player
        )
        if team == PutChestPayload.Team.britain:
            if player_pos in Positions.fd_positions():
                self.game.chests_position.fd_en += 1
            elif player_pos in Positions.jr_positions():
                self.game.chests_position.jr_en += 1
        elif team == PutChestPayload.Team.france:
            if player_pos in Positions.fd_positions():
                self.game.chests_position.fd_fr += 1
            elif player_pos in Positions.jr_positions():
                self.game.chests_position.jr_fr += 1
        self.game.players_info.get(self.player).chests -= 1
