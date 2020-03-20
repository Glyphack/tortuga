from app.tests.api.game.base import BaseGameTestCase


class TestVoteAction(BaseGameTestCase):
    def test_vote_on_call_for_action(self):
        self._start_call_for_action()
        participating_players_copy = (
            self.game.last_action.action_data.participating_players.copy()
        )
        for player in participating_players_copy:
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
            self.client.post(self.do_action_url, headers=headers, json=request)

        response = self.client.get(
            self.game_status_url,
            headers=self.auth_header(self.game.get_fd_caption())
        ).json()
        expected_response = {
            'actionType': 'call for an attack',
            'actionData': {
                'state': self.game.last_action.action_data.state.value,
                'participatingPlayers': []
            }
        }

        assert response["gameStatus"]["lastAction"] == expected_response

    def _start_call_for_action(self):
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
