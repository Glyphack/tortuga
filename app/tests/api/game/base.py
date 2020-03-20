import pytest

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
