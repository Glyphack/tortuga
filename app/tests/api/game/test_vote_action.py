import requests

from app.tests.api.game.base import BaseGameTestCase


class TestVoteAction(BaseGameTestCase):
    def test_vote_on_call_for_action(self):
        self._start_call_for_action()
        participating_players = (
            self.game.last_action.action_data.participating_players.copy()
        )
        for player in participating_players:
            self._vote(player)
        response = self._get_my_game(self.game.get_jr_caption()).json()
        expected_last_action = {
            'actionType': 'call for an attack',
            'actionData': {
                'state': self.game.last_action.action_data.state.value,
                'participatingPlayers': [],
                "whichCaptain": {"username": self.game.get_jr_caption()},
                'fromOtherShip': False
            }
        }

        assert response["gameStatus"]["lastAction"] == expected_last_action

    def test_voting_twice(self):
        self._start_call_for_action()
        player = self.game.last_action.action_data.participating_players[0]
        response = self._vote(player)
        assert response.status_code == 200
        response = self._vote(player)
        assert response.status_code == 400

    def test_player_should_not_vote(self):
        self._start_call_for_action()
        not_voting_players = list(
            set(self.game.players) -
            set(self.game.last_action.action_data.participating_players)
        )
        player = not_voting_players.pop()
        response = self._vote(player)
        assert response.status_code == 400

    def test_turn_not_change_un_complete_vote(self):
        self._start_call_for_action()
        player = self.game.last_action.action_data.participating_players[0]
        turn = self.game.turn
        self._vote(player)
        assert turn == self.game.turn

    def test_turn_change_after_successful_vote(self):
        self._start_call_for_action()
        participating_players_copy = (
            self.game.last_action.action_data.participating_players.copy()
        )
        turn = self.game.turn
        for player in participating_players_copy:
            self._vote(player)
        assert turn != self.game.turn

    def test_available_action_is_voting(self):
        self._start_call_for_action()
        participating_players_copy = (
            self.game.last_action.action_data.participating_players.copy()
        )
        for player in participating_players_copy:
            response = self._get_my_game(player).json()
            assert response["gameStatus"]["playerGameInfo"][
                       "availableActions"] == ["vote"]

    def test_vote_cards_return_to_players(self):
        self._start_call_for_action()
        participating_players_copy = (
            self.game.last_action.action_data.participating_players.copy()
        )
        vote_cards_before = len(self.game.players_info["p3"].vote_cards)
        for player in participating_players_copy:
            self._vote(player)
        vote_cards_after = len(self.game.players_info["p3"].vote_cards)
        assert vote_cards_after == vote_cards_before
