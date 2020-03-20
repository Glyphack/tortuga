import pytest

from app.models.game import Game


class TestCallForAnAttackAction:
    @pytest.fixture(autouse=True)
    def _setup(self, client, game: Game):
        self.client = client
        self.game = game

    @property
    def do_action_url(self):
        return "api/v1/game/action"

    @property
    def game_status_url(self):
        return "api/v1/game/my-game"

    def test_call_for_an_attack(self, auth_header_generator):
        request = {
            "game_id": "1",
            "action": {
                "actionType": "call for an attack",
                "actionData": None
            },
            "payload": None
        }

        headers = auth_header_generator(self.game.get_fd_caption())
        self.client.post(
            self.do_action_url, json=request, headers=headers
        )

        response = self.client.get(
            self.game_status_url, headers=headers
        )

        print(response.json())
