from typing import Dict, Type

from .albatross import Albatross
from .atlantis import Atlantis
from .black_spot import BlackSpot
from .eight_bells import EightBells
from .el_dorado import ElDorado
from .event_card_handler import EventCardHandler
from .fountain_of_youth import FountainOfYouth
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
    "fountain-of-youth": FountainOfYouth,
    "el-dorado": ElDorado,
    "albatross": Albatross
}
