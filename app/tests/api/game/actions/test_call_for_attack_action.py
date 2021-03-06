from app.tests.api.game.base import BaseGameTestCase


class TestCallForAnAttackAction(BaseGameTestCase):
    def test_call_for_an_attack(self):
        player = self.game.get_jr_caption()
        self._call_for_an_attack(player)
        headers = self.auth_header(player)
        response = self.client.get(
            self.my_game_url, headers=headers
        )

        expected_response = {
            'actionType': 'call for an attack',
            'actionData': {
                'state': 'in_progress',
                'participatingPlayers': self.game.last_action
                    .action_data.participating_players,
                "whichCaptain": {"username": self.game.get_jr_caption()},
                'fromOtherShip': False,
                "voteResults": []
            },

        }

        assert response.json()["gameStatus"]["lastAction"] == expected_response

    def test_after_call_for_an_attack_player_can_vote(self):
        player = self.game.get_jr_caption()
        self._call_for_an_attack(player)
        assert (self.game.can_vote(player) is True)
