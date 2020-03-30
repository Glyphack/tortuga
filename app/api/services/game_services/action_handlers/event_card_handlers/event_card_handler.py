from app.models.game import Game
from app.schemas.game_schema import PayloadType


class EventCardHandler:
    def __init__(self, game: Game, player: str, payload: PayloadType):
        self.game = game
        self.player = player
        self.payload = payload

    def reveal_card(self):
        raise NotImplemented
