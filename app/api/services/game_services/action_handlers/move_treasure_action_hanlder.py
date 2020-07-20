from app.schemas.game_schema import Positions, TreasureHoldTeams, Action, \
    MoveTreasureActionData
from .action_handler import ActionHandler


class MoveTreasureActionHandler(ActionHandler):
    @property
    def activity_text(self):
        return f"{self.player} moved loot from " \
               f"{self.payload.from_hold.lower()} to" \
               f"{self.where_is_treasure_going().lower()}"

    def execute(self):
        player_position = self.game.players_position[self.player]
        assert player_position in self.game.cabin_boy_slots
        if player_position in Positions.jr_positions():
            if self.payload.from_hold == TreasureHoldTeams.britain:
                if self.game.chests_position.jr_en <= 0:
                    raise AssertionError("no chests here")
                self.game.chests_position.jr_en -= 1
                self.game.chests_position.jr_fr += 1
            else:
                if self.game.chests_position.jr_fr <= 0:
                    raise AssertionError("no chests here")
                self.game.chests_position.jr_fr -= 1
                self.game.chests_position.jr_en += 1
        elif player_position in Positions.fd_positions():
            if self.payload.from_hold == TreasureHoldTeams.britain:
                if self.game.chests_position.fd_en <= 0:
                    raise AssertionError("no chests here")
                self.game.chests_position.fd_en -= 1
                self.game.chests_position.fd_fr += 1
            else:
                if self.game.chests_position.fd_fr <= 0:
                    raise AssertionError("no chests here")
                self.game.chests_position.fd_fr -= 1
                self.game.chests_position.fd_en += 1
        else:
            raise AssertionError("You are not a cabin boy.")

        self.game.last_action = Action(
            action_type=Action.ActionType.MOVE_TREASURE,
            action_data=MoveTreasureActionData(
                cabin_boy=self.player,
                from_hold=self.payload.from_hold,
                to_hold=self.where_is_treasure_going()
            )
        )
        self.game.next_turn()

    def where_is_treasure_going(self):
        if self.payload.from_hold == TreasureHoldTeams.france:
            to_hold = TreasureHoldTeams.britain
        else:
            to_hold = TreasureHoldTeams.france
        return to_hold
