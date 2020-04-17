from typing import Dict, Type

from .black_spot import BlackSpot
from .event_card_handler import EventCardHandler
from .pistol_handler import Pistol
from .spanish_armada import SpanishArmadaCard
from .letter_of_marque_handler import LetterOfMarque

event_card_handler: Dict[str, Type[EventCardHandler]] = {
    "spanish-armada": SpanishArmadaCard,
    "letter-of-marque": LetterOfMarque,
    "pistol": Pistol,
    "black-spot": BlackSpot
}
