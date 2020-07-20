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
    all_slugs: List[str] = []

    @classmethod
    def get(cls, slug: str) -> EventCard:
        if not cls.event_cards:
            cls.load_event_cards()
        return cls.event_cards[slug]

    @classmethod
    def get_all_slugs(cls) -> List[str]:
        if not cls.all_slugs:
            cls.load_event_cards()
        return cls.all_slugs

    @classmethod
    def load_event_cards(cls):
        base_path = Path(__file__).parent
        file_path = (base_path / "../data/event_cards.json").resolve()
        with file_path.open() as f:
            event_cards = json.load(f)["event_cards"]
        for event_card_slug, event_card in event_cards.items():
            cls.event_cards[event_card_slug] = EventCard(
                slug=event_card_slug,
                title=event_card["title"],
                description=event_card["description"],
                image_url=event_card["image_url"]
            )
            for _ in range(int(event_card["count"])):
                cls.all_slugs.append(event_card_slug)
