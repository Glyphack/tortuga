import random
from dataclasses import dataclass

from app.models.player import Player
from app.models.votes import Votes, generate_vote_card
from app.schemas import game_schema
from app.schemas.game_schema import (
    Action, VoteCard, Positions, Team
)
from typing import List, Dict, Optional


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
    winner: Optional[Team] = None

    def get_jr_caption(self) -> Optional[str]:
        for player, position in self.players_position.items():
            if position == Positions.JR1:
                return player
        return None

    def get_fd_caption(self) -> Optional[str]:
        for player, position in self.players_position.items():
            if position == Positions.FD1:
                return player
        return None

    def get_player_info(self, username) -> Player:
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

    def has_unfinished_voting(self):
        last_action = self.last_action
        if last_action is None:
            return False
        is_voting_started = (
            last_action.action_type in [
                Action.ActionType.CALL_FOR_AN_ATTACK,
                Action.ActionType.CALL_FOR_BRAWL,
                Action.ActionType.CALL_FOR_A_MUTINY
            ]
        )
        return (
                is_voting_started and
                last_action.action_data.state == game_schema.State.InProgress
        )

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
        current_position = self.get_position(player)
        if position == Positions.JR:
            position = self.jr_ship_first_empty_slot
        elif position == Positions.FD:
            position = self.fd_ship_first_empty_slot
        elif position == Positions.TR:
            position = self.tortuga_first_empty_slot
        self.players_position[player] = position
        self.fill_empty_position(current_position)

    def fill_empty_position(self, position: Positions):
        if position in Positions.jr_positions():
            positions = Positions.jr_positions()
            move_to = Positions.JR
        elif position in Positions.fd_positions():
            positions = Positions.fd_positions()
            move_to = Positions.FD
        elif position in Positions.tr_positions():
            positions = Positions.tr_positions()
            move_to = Positions.TR
        else:
            return

        move_from = None
        for front, back in zip(positions[0:], positions[1:]):
            if (
                    front not in self.players_position.values() and
                    back in self.players_position.values()
            ):
                move_from = back
                break
        if move_from:
            for player, position in self.players_position.items():
                if position == move_from:
                    self.set_position(player, move_to)

    def get_position(self, player: str) -> Positions:
        return self.players_position[player]

    def give_vote_cards_back_after_vote(self):
        random.shuffle(self.votes.vote_cards)
        for player in self.votes.participated_players:
            self.get_player_info(player).vote_cards.append(
                self.votes.vote_cards.pop()
            )

    def end_voting(self):
        self.give_vote_cards_back_after_vote()
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

    def maroon_player(self, player) -> bool:
        if self.get_player_info(player).has_event_card("fountain-of-youth"):
            self.get_player_info(player).remove_event_card(
                "fountain-of-youth"
            )
            return False
        self.set_position(
            player,
            Positions.TR
        )
        return True

    def check_albatross(self):
        """
        after every move we check that if two players on one part
        has albatross cards we maroon all the players on that
        part to tortuga
        """
        positions_with_albatross = []
        for player_name, position in self.players_position.items():
            if self.get_player_info(player_name).has_event_card("albatross"):
                positions_with_albatross.append(position)

        for positions in game_schema.Positions.all_sections():
            result = list(filter(
                lambda pos: pos in positions, positions_with_albatross
            ))
            if len(result) >= 2:
                players = filter(
                    lambda x: self.players_position[x] in positions,
                    self.players
                )
                for player in players:
                    self.maroon_player(player)
                return
