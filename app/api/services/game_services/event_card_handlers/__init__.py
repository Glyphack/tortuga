from typing import Dict, Type

from .event_card_handler import EventCardHandler
from .spanish_armada import SpanishArmadaCard
from .letter_of_marque_handler import LetterOfMarque

event_card_handler: Dict[str, Type[EventCardHandler]] = {
    "spanish-armada": SpanishArmadaCard,
    "letter-of-marque": LetterOfMarque
}
