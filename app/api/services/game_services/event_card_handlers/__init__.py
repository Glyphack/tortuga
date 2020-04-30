from typing import Dict, Type

from .atlantis import Atlantis
from .black_spot import BlackSpot
from .eight_bells import EightBells
from .event_card_handlers import EventCardHandler
from .pistol_handler import Pistol
from .spanish_armada import SpanishArmadaCard
from .letter_of_marque_handler import LetterOfMarque
from .stormy_seas import StormySeas

event_card_handlers: Dict[str, Type[EventCardHandler]] = {
    "spanish-armada": SpanishArmadaCard,
    "letter-of-marque": LetterOfMarque,
    "pistol": Pistol,
    "black-spot": BlackSpot,
    "atlantis": Atlantis,
    "stormy-seas": StormySeas,
    "eight-bells": EightBells,
}
