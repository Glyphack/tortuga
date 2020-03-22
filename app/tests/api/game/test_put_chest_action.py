import pytest

from app.models.game import Game
from app.schemas.auth import User
from app.schemas.game_schema import Action, CaptainCallForAttackData, State
from .base import BaseGameTestCase


class TestPutChestAction(BaseGameTestCase):
    def test_put_chest_from_tortuga(self, game_success_full_attack):
        game = game_success_full_attack
        header = self.auth_header(self.game.get_jr_caption())
        game.players_info.get(game.get_jr_caption())
        request = {
            "game_id": "1",
            "action": {
                "actionType": "put chest",
                "actionData": None
            },
            "payload": {
                "whichTeam": "FRANCE"
            }
        }
        france_chests_before = game.chests_position.jr_fr
        self.client.post(self.do_action_url, json=request, headers=header)

        assert france_chests_before + 1 == game.chests_position.jr_fr
        assert game.players_info.get(self.game.get_jr_caption()).chests == 0

    def test_available_action_put_chest(self):
        response = self._get_my_game(self.game.get_jr_caption()).json()
        assert response["gameStatus"]["playerGameInfo"][
                   "availableActions"] == ["put chest"]


@pytest.fixture()
def game_success_full_attack(game: Game):
    game.last_action = Action(
        action_type=Action.ActionType.CALL_FOR_AN_ATTACK,
        action_data=CaptainCallForAttackData(
            which_captain=User(username=game.get_jr_caption()),
            state=State.Success,
            from_other_ship=False
        )
    )
    return game
