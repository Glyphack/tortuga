from app.schemas.game_schema import (
    PlayerGameInfo, Action,
    MaroonAnyCrewMateToTortugaActionData
)
from .action_handler import ActionHandler


class MaroonCrewActionHandler(ActionHandler):
    def execute(self):
        player_to_maroon: str = self.payload.crew_to_maroon
        assert (
                self.game.players_info.get(
                    self.player).role == PlayerGameInfo.Role.CAPTAIN and
                self.game.on_same_ship(self.player, player_to_maroon)
        )

        self.game.players_position[player_to_maroon] = (
            self.game.first_empty_tortuga_slot
        )
        self.game.last_action = Action(
            action_type=Action.ActionType.MAROON_ANY_CREW_MATE_TO_TORTUGA,
            action_data=MaroonAnyCrewMateToTortugaActionData(
                marooned_crew=player_to_maroon
            )
        )
