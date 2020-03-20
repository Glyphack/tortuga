from app.tests.api.game.base import BaseGameTestCase


class TestCallForAnAttackAction(BaseGameTestCase):
    def test_call_for_an_attack(self):
        request = {
            "game_id": "1",
            "action": {
                "actionType": "call for an attack",
                "actionData": None
            },
            "payload": None
        }

        headers = self.auth_header(self.game.get_fd_caption())
        self.client.post(
            self.do_action_url, json=request, headers=headers
        )

        response = self.client.get(
            self.game_status_url, headers=headers
        )

        expected_response = {
            'actionType': 'call for an attack',
            'actionData': {
                'state': 'in_progress',
                'participatingPlayers': self.game.last_action
                .action_data.participating_players
            }
        }

        assert response.json()["gameStatus"]["lastAction"] == expected_response
