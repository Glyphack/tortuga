import pytest

from app.models.game import Game
from app.schemas.auth import User
from app.schemas.game_schema import Action, CaptainCallForAttackData, State
from .base import BaseGameTestCase


@pytest.fixture()
def game_success_full_attack(game: Game):
    game.last_action = Action(
        action_type=Action.ActionType.CALL_FOR_AN_ATTACK,
        action_data=CaptainCallForAttackData(
            which_captain=User(username=game.get_jr_caption()),
            state=State.Success,
        )
    )
    return game


class TestPutChestAction(BaseGameTestCase):
    def test_put_after_game_start(self):
        header = self.auth_header(self.game.get_jr_caption())
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
        france_chests_before = self.game.chests_position.jr_fr
        self.client.post(self.do_action_url, json=request, headers=header)

        assert france_chests_before + 1 == self.game.chests_position.jr_fr
