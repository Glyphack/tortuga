import pytest
import requests

from app.models.game import Game


class BaseGameTestCase:
    @pytest.fixture(autouse=True)
    def _setup(self, client, game: Game, auth_header_generator):
        self.client = client
        self.game = game
        self.auth_header = auth_header_generator

    @property
    def do_action_url(self):
        return "api/v1/game/action"

    @property
    def game_status_url(self):
        return "api/v1/game/my-game"

    def _start_call_for_action(self):
        request = {
            "game_id": "1",
            "action": {
                "actionType": "call for an attack",
                "actionData": None
            },
            "payload": None
        }
        headers = self.auth_header(self.game.get_jr_caption())
        self.client.post(
            self.do_action_url, json=request, headers=headers
        )

    def _vote(self, player: str) -> requests.Response:
        request = {
            "gameId": self.game.id,
            "action": {
                "actionType": "vote",
            },
            "payload": {
                "voteCardIndex": 1
            }
        }
        headers = self.auth_header(player)
        response = self.client.post(
            self.do_action_url, headers=headers, json=request
        )
        return response

    def _call_for_an_attack(self, player: str):
        request = {
            "game_id": "1",
            "action": {
                "actionType": "call for an attack",
                "actionData": None
            },
            "payload": None
        }

        headers = self.auth_header(player)
        self.client.post(
            self.do_action_url, json=request, headers=headers
        )
