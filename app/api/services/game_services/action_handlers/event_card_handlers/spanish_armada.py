from .event_card_handler import EventCardHandler


class SpanishArmadaCard(EventCardHandler):
    def reveal_card(self):
        self.game.finish_game()
