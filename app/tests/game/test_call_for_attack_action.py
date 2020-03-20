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

        expected_response = {
            'gameStatus': {
                'playersPosition': {'p2': 'jr_1', 'p3': 'fd_1', 'p1': 'jr_2',
                                    'p4': 'fd_2'},
                'chestsPosition': {'fdFr': 0, 'fdEn': 0, 'sgNt': 4, 'jrFr': 0,
                                   'jrEn': 0, 'trFr': 1, 'trEn': 1},
                'playerGameInfo': {'team': 'dutch', 'voteCards': None,
                                   'eventCards': None, 'role': None},
                'lastAction': {
                    'actionType': 'call for an attack',
                    'actionData': {
                        'state': 'in_progress',
                        'participatingPlayers': ['p2', 'p1']}
                },
                'isOver': False, 'turn': {'username': 'p1'}, 'winner': None},
            'hasGame': True
        }

        assert response.json() == expected_response
