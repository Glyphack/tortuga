from typing import Dict, Type

from .event_card_handler import EventCardHandler
from .spanish_armada import SpanishArmadaCard

event_card_handler: Dict[str, Type[EventCardHandler]] = {
    "spanish-armada": SpanishArmadaCard
}
