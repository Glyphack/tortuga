from app.api.services.game_services.action_handlers.action_handler import (
    ActionHandler
)
from app.models.game import Votes
from app.schemas import game_schema
from app.schemas.game_schema import VoteCard, State, Positions


class VoteActionHandler(ActionHandler):
    def execute(self):
        last_action = self.game.last_action
        is_voting_active = (
                last_action.action_type ==
                game_schema.Action.ActionType.CALL_FOR_AN_ATTACK or
                last_action.action_type ==
                game_schema.Action.ActionType.CALL_FOR_BRAWL or
                last_action.action_type ==
                game_schema.Action.ActionType.CALL_FOR_A_MUTINY
        )
        assert (
                is_voting_active and
                last_action.action_data.state == game_schema.State.InProgress and
                self.player in last_action.action_data.participating_players
        )
        vote_card = self.game.players_info.get(self.player).vote_cards.pop(
            self.payload.vote_card_index - 1
        )
        self.game.votes.participated_players.append(self.player)
        self.game.votes.vote_cards.append(vote_card)

        if last_action.action_type == game_schema.Action.ActionType.CALL_FOR_AN_ATTACK:
            self.handle_call_for_attack_vote(vote_card)
        elif last_action.action_type == game_schema.Action.ActionType.CALL_FOR_BRAWL:
            self.handle_call_for_brawl_vote(vote_card)
        elif last_action.action_type == game_schema.Action.ActionType.CALL_FOR_A_MUTINY:
            self.handle_call_for_mutiny_vote(vote_card)

    def handle_call_for_attack_vote(self, vote_card: VoteCard):
        last_action = self.game.last_action
        self.game.votes.fire += vote_card.fire
        self.game.votes.water += vote_card.water
        last_action.action_data.participating_players.remove(
            self.player
        )
        if len(last_action.action_data.participating_players) == 0:
            if self.game.votes.fire < self.game.votes.water:
                last_action.action_data.state = game_schema.State.Success
                self.game.give_chest(
                    last_action.action_data.which_captain.username
                )
            else:
                last_action.action_data.state = game_schema.State.Failed
            self.game.end_voting()

    def handle_call_for_brawl_vote(self, vote_card):
        last_action = self.game.last_action
        self.game.votes.britain += vote_card.britain
        self.game.votes.france += vote_card.france
        last_action.action_data.participating_players.remove(
            self.player
        )
        if len(last_action.action_data.participating_players) == 0:
            last_action.action_data.state = game_schema.State.Failed
            if self.game.votes.britain > self.game.votes.france:
                self.game.chests_position.tr_fr -= 1
                self.game.chests_position.tr_en += 1
                last_action.action_data.state = game_schema.State.Success
            elif self.game.votes.britain < self.game.votes.france:
                self.game.chests_position.tr_en -= 1
                self.game.chests_position.tr_fr += 1
                last_action.action_data.state = game_schema.State.Success
            self.game.next_turn()
            self.game.end_voting()

    def handle_call_for_mutiny_vote(self, vote_card):
        last_action = self.game.last_action
        self.game.votes.wheel += vote_card.wheel
        self.game.votes.skull += vote_card.skull
        last_action.action_data.participating_players.remove(
            self.player
        )
        if len(last_action.action_data.participating_players) == 0:
            if self.game.votes.skull > self.game.votes.wheel:
                self.game.last_action.action_data.state = State.Success
                self.game.set_position(
                    last_action.action_data.captain, Positions.TR
                )
            else:
                self.game.last_action.action_data.state = State.Failed
            self.game.next_turn()
            self.game.end_voting()
