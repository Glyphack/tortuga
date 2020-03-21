from app.tests.api.game.base import BaseGameTestCase


class TestCallForAnAttackAction(BaseGameTestCase):
    def test_call_for_an_attack(self):
        player = self.game.get_fd_caption()
        self._call_for_an_attack(player)
        headers = self.auth_header(player)
        response = self.client.get(
            self.game_status_url, headers=headers
        )

        expected_response = {
            'actionType': 'call for an attack',
            'actionData': {
                'state': 'in_progress',
                'participatingPlayers': self.game.last_action
                    .action_data.participating_players,
                "whichCaptain": {"username": self.game.get_fd_caption()}
            },

        }

        assert response.json()["gameStatus"]["lastAction"] == expected_response
