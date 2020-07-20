from app.schemas.game_schema import (
    Action,
    MaroonAnyCrewMateToTortugaActionData,
    Positions)
from .action_handler import ActionHandler


class MaroonCrewActionHandler(ActionHandler):
    @property
    def activity_text(self):
        return f"{self.player} marooned {self.payload.crew_to_maroon}"

    def execute(self):
        player_to_maroon: str = self.payload.crew_to_maroon
        assert self.game.players_position[self.player] in [
            Positions.JR1,
            Positions.FD1,
        ] and self.game.on_same_ship(self.player, player_to_maroon)

        self.game.maroon_player(player_to_maroon)
        self.game.last_action = Action(
            action_type=Action.ActionType.MAROON_ANY_CREW_MATE_TO_TORTUGA,
            action_data=MaroonAnyCrewMateToTortugaActionData(
                marooned_crew=player_to_maroon
            )
        )
        self.game.next_turn()
