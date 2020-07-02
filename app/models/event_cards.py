import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict


@dataclass
class EventCard:
    slug: str
    title: str
    description: str
    image_url: str


class EventCardsManager:
    event_cards: Dict[str, EventCard] = {}

    @classmethod
    def get(cls, slug: str) -> EventCard:
        if not cls.event_cards:
            cls.load_event_cards()
        return cls.event_cards[slug]

    @classmethod
    def get_all_slugs(cls) -> List[str]:
        if not cls.event_cards:
            cls.load_event_cards()
        return list(cls.event_cards.keys())

    @classmethod
    def load_event_cards(cls):
        base_path = Path(__file__).parent
        file_path = (base_path / "../data/event_cards.json").resolve()
        with file_path.open() as f:
            event_cards_info = json.load(f)["event_cards"]
        for event_card_name, event_card in event_cards_info.items():
            for i in range(event_card["count"]):
                cls.event_cards[event_card_name] = EventCard(
                    slug=event_card_name,
                    title=event_card["title"],
                    description=event_card["description"],
                    image_url=event_card["image_url"]
                )
