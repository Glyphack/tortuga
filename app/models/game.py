import random
from dataclasses import dataclass

from fastapi_utils.enums import StrEnum

from app.models.votes import Votes, generate_vote_card

from app.models.event_cards import EventCard
from app.schemas.game_schema import (
    Action, VoteCard, Positions
)
from typing import List, Dict, Optional


class Team(StrEnum):
    BRITAIN = "britain"
    FRANCE = "france"
    DUTCH = "dutch"


@dataclass
class Player:
    id: str
    team: str
    vote_cards: List[VoteCard] = None
    event_cards: List[EventCard] = None
    seen_event_cards: List[EventCard] = None
    chests: int = 0


@dataclass
class Chests:
    fd_fr: int
    fd_en: int
    sg_nt: int
    jr_fr: int
    jr_en: int
    tr_fr: int
    tr_en: int

    def get_france_count(self):
        return self.fd_fr + self.jr_fr + self.tr_fr

    def get_britain_count(self):
        return self.fd_en + self.jr_en + self.tr_en


@dataclass
class Game:
    id: str
    players_info: Dict[str, Player]
    host: str
    players_position: Dict[str, Positions]
    chests_position: Chests
    event_cards: List[str]
    vote_deck: VoteCard = None
    votes: Optional[Votes] = Votes()
    turn: str = ""
    last_action: Optional[Action] = None
    last_votes: Optional[Votes] = None
    is_over: bool = False
    winner: Optional[str] = None

    def get_jr_caption(self) -> Optional[str]:
        for player, position in self.players_position.items():
            if position == Positions.JR1:
                return player
        return None

    def get_player_info(self, username):
        return self.players_info[username]

    @property
    def players(self):
        return list(self.players_position.keys())

    def next_turn(self):
        index = self.players.index(self.turn)
        index += 1
        if index == len(self.players):
            index = 0
        self.turn = self.players[index]

    def give_chest(self, player: str):
        self.players_info.get(player).chests += 1

    def on_same_ship(self, player1: str, player2: str):
        ship_slots_positions = [
            Positions.jr_positions(), Positions.fd_positions()
        ]
        return any(
            self.players_position.get(player1) in ship and
            self.players_position.get(player2) in ship
            for ship in ship_slots_positions
        )

    @property
    def tortuga_first_empty_slot(self):
        tg_positions = Positions.tr_positions().copy()
        return self.get_first_empty_slot(tg_positions)

    @property
    def jr_ship_first_empty_slot(self):
        jr_positions = Positions.jr_positions().copy()
        return self.get_first_empty_slot(jr_positions)

    @property
    def fd_ship_first_empty_slot(self):
        fd_positions = Positions.fd_positions().copy()
        return self.get_first_empty_slot(fd_positions)

    def get_first_empty_slot(self, position_list):
        for _, p in self.players_position.items():
            if p in position_list:
                position_list.remove(p)
        return position_list[0]

    def is_empty(self, position: Positions):
        for _, position_occupied in self.players_position.items():
            if position == position_occupied:
                return False
        return True

    def set_position(self, player: str, position: Positions):
        if position == Positions.JR:
            position = self.jr_ship_first_empty_slot
        elif position == Positions.FD:
            position = self.fd_ship_first_empty_slot
        elif position == Positions.TR:
            position = self.tortuga_first_empty_slot
        self.players_position[player] = position

    def give_vote_cards_back_after_vote(self):
        random.shuffle(self.votes.vote_cards)
        for player in self.votes.participated_players:
            self.get_player_info(player).vote_cards.append(
                self.votes.vote_cards.pop()
            )

    def end_voting(self):
        self.give_vote_cards_back_after_vote()
        self.next_turn()
        self.votes = Votes()
        self.vote_deck = generate_vote_card()

    def finish_game(self):
        if self.chests_position.get_britain_count() > self.chests_position.get_france_count():
            self.winner = Team.BRITAIN
        elif self.chests_position.get_france_count() == self.chests_position.get_britain_count():
            self.winner = Team.DUTCH
        else:
            self.winner = Team.FRANCE

        self.is_over = True

    def get_event_cards_deck_count(self):
        if len(self.event_cards) > 5:
            return 5
        else:
            return len(self.event_cards)

    @property
    def cabin_boy_slots(self) -> List[Positions]:
        jr_cabin_boy = None
        fd_cabin_boy = None
        for p in Positions.jr_positions():
            if p not in self.players_position.values():
                break
            jr_cabin_boy = p
        for p in Positions.fd_positions():
            if p not in self.players_position.values():
                break
            fd_cabin_boy = p
        return [jr_cabin_boy, fd_cabin_boy]
