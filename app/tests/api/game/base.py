from typing import List

import pytest
import requests
from requests import Response

from app.models.game import Game
from app.schemas import game_schema
from app.schemas.game_schema import Action, DoActionRequest, \
    SeeEventCardOptionsPayload, UseEventCardPayload


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
    def my_game_url(self):
        return "api/v1/game/my-game"

    def _start_call_for_action(self):
        request = {
            "game_id": "1",
            "action": {
                "actionType": "call for an attack",
                "actionData": None
            },
            "payload": None
        }
        headers = self.auth_header(self.game.get_jr_caption())
        self.client.post(
            self.do_action_url, json=request, headers=headers
        )

    def _vote(self, player: str) -> requests.Response:
        request = {
            "gameId": self.game.id,
            "action": {
                "actionType": "vote",
            },
            "payload": {
                "voteCardIndex": 1
            }
        }
        headers = self.auth_header(player)
        response = self.client.post(
            self.do_action_url, headers=headers, json=request
        )
        return response

    def _call_for_an_attack(self, player: str):
        request = {
            "game_id": "1",
            "action": {
                "actionType": "call for an attack",
                "actionData": None
            },
            "payload": None
        }

        headers = self.auth_header(player)
        response = self.client.post(
            self.do_action_url, json=request, headers=headers
        )
        return response

    def _maroon_crew(self, captain: str, player: str) -> Response:
        request = {
            "gameId": "1",
            "action": {
                "actionType": "maroon any crew mate to tortuga",
            },
            "payload": {
                "crewToMaroon": player
            }
        }
        headers = self.auth_header(captain)
        response = self.client.post(
            self.do_action_url, json=request, headers=headers
        )
        return response

    def _move_action(self, player_to_move: str,
                     position: game_schema.Positions) -> Response:
        request = {
            "gameId": 1,
            "action": {
                "actionType": "move",
            },
            "payload": {
                "move_where": position
            }
        }

        headers = self.auth_header(player_to_move)
        return self.client.post(url=self.do_action_url, json=request,
                                headers=headers)

    def _move_treasure_action(self,
                              player: str,
                              from_hold: game_schema.TreasureHoldTeams):
        json = {
            "gameId": "1",
            "action": {
                "actionType": "move treasure",
            },
            "payload": {
                "from_hold": from_hold
            }
        }

        headers = self.auth_header(player)
        return self.client.post(url=self.do_action_url, json=json,
                                headers=headers)

    def _call_brawl_action(self, player: str) -> Response:
        request = {
            "gameId": "1",
            "action": {
                "actionType": "call for brawl"
            }
        }

        headers = self.auth_header(player)
        return self.client.post(url=self.do_action_url, json=request,
                                headers=headers)

    def _call_for_mutiny_action(self, player: str) -> Response:
        request = {
            "gameId": "1",
            "action": {
                "actionType": "call for a mutiny"
            },
        }
        headers = self.auth_header(player)
        return self.client.post(url=self.do_action_url, json=request,
                                headers=headers)

    def _view_two_event_cards_action(self, player, event_cards: List[int]):
        request = {
            "gameId": 1,
            "action": {
                "actionType": "view two event cards"
            },
            "payload": {
                "eventCardsIndexes": event_cards
            }
        }
        headers = self.auth_header(player)
        return self.client.post(url=self.do_action_url, json=request,
                                headers=headers)

    def _reveal_event_card_action(self, player, index):
        request = {
            "gameId": 1,
            "action": {
                "actionType": "reveal one event card",
            },
            "payload": {
                "event_card_index": index
            }
        }
        headers = self.auth_header(player)
        return self.client.post(url=self.do_action_url, json=request,
                                headers=headers)

    def _keep_event_card_action(self, player):
        request = DoActionRequest(
            action=Action(
                action_type=Action.ActionType.KEEP_EVENT_CARD,
            ),
            game_id="1",
        )
        headers = self.auth_header(player)
        return self.client.post(url=self.do_action_url, data=request.json(),
                                headers=headers)

    def see_event_card_options(self, player, slug):
        request = DoActionRequest(
            action=Action(
                action_type=Action.ActionType.SEE_EVENT_CARD_OPTIONS,
            ),
            game_id="1",
            payload=SeeEventCardOptionsPayload(
                event_card_to_see_slug=slug
            )
        )
        headers = self.auth_header(player)
        return self.client.post(url=self.do_action_url, data=request.json(),
                                headers=headers)

    def use_event_card_action(self, player, slug: str, option):
        request = DoActionRequest(
            action=Action(
                action_type=Action.ActionType.USE_EVENT_CARD
            ),
            game_id="1",
            payload=UseEventCardPayload(
                event_card_option_index=option,
                event_card_to_use=slug,
            )
        )
        headers = self.auth_header(player)
        self.client.post(self.do_action_url, data=request.json(),
                         headers=headers)

    def _get_my_game(self, player) -> Response:
        headers = self.auth_header(player)
        response = self.client.get(self.my_game_url, headers=headers)
        return response
