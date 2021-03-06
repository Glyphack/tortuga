from app.api.services.game_services.action_handlers.action_handler import (
    ActionHandler
)
from app.schemas import game_schema
from app.schemas.game_schema import VoteCard, State, Positions


class VoteActionHandler(ActionHandler):
    @property
    def activity_text(self):
        return f"{self.player} voted"

    def execute(self):
        last_action = self.game.last_action
        assert self.game.can_vote(self.player)
        vote_card = self.game.players_info.get(self.player).vote_cards.pop(
            self.payload.vote_card_index
        )

        last_action.action_data.participating_players.remove(
            self.player
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
        self.game.votes.cannons += vote_card.cannon
        self.game.votes.fire += vote_card.fire
        self.game.votes.water += vote_card.water

        if len(last_action.action_data.participating_players) == 0:
            self.game.votes.cannons += vote_card.cannon
            self.game.votes.fire += vote_card.fire
            self.game.votes.water += vote_card.water
            if (
                    self.game.votes.fire > self.game.votes.water and
                    self.game.votes.cannons > 0
            ):
                last_action.action_data.state = game_schema.State.Success
                self.game.give_chest(
                    last_action.action_data.which_captain.username
                )
            else:
                last_action.action_data.state = game_schema.State.Failed
                self.game.next_turn()
            self.game.last_action.action_data.vote_results.extend(
                self.game.votes.vote_cards
            )
            self.game.end_voting()


    def handle_call_for_brawl_vote(self, vote_card):
        last_action = self.game.last_action
        self.game.votes.britain += vote_card.britain
        self.game.votes.france += vote_card.france

        if len(last_action.action_data.participating_players) == 0:
            self.game.votes.britain += self.game.vote_deck.britain
            self.game.votes.france += self.game.vote_deck.france
            last_action.action_data.state = game_schema.State.Failed
            if (
                    self.game.votes.britain > self.game.votes.france and
                    self.game.chests_position.tr_fr > 0
            ):
                self.game.chests_position.tr_fr -= 1
                self.game.chests_position.tr_en += 1
                last_action.action_data.state = game_schema.State.Success
            elif (
                    self.game.votes.britain < self.game.votes.france and
                    self.game.chests_position.tr_en > 0
            ):
                self.game.chests_position.tr_en -= 1
                self.game.chests_position.tr_fr += 1
                last_action.action_data.state = game_schema.State.Success
            self.game.last_action.action_data.vote_results.extend(
                self.game.votes.vote_cards
            )
            self.game.end_voting()
            self.game.next_turn()

    def handle_call_for_mutiny_vote(self, vote_card):
        last_action = self.game.last_action
        self.game.votes.wheel += vote_card.wheel
        self.game.votes.skull += vote_card.skull

        if len(last_action.action_data.participating_players) == 0:
            self.game.votes.wheel += self.game.vote_deck.wheel
            self.game.votes.skull += self.game.vote_deck.skull
            if self.game.votes.skull > self.game.votes.wheel:
                self.game.last_action.action_data.state = State.Success
                self.game.set_position(
                    last_action.action_data.captain, Positions.TR
                )
            else:
                self.game.last_action.action_data.state = State.Failed
            self.game.last_action.action_data.vote_results.extend(
                self.game.votes.vote_cards
            )
            self.game.end_voting()
            self.game.next_turn()
