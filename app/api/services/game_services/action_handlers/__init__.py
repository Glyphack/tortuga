from typing import Dict, Type

from app.schemas.game_schema import Action
from .action_handler import ActionHandler
from .call_for_an_attack_action_handler import CallForAnAttackActionHandler
from .put_chest_action_handler import PutChestActionHandler
from .vote_action_handler import VoteActionHandler
from .maroon_crew_to_tortuga import MaroonCrewActionHandler
from .move_action_handler import MoveActionHandler
from .move_treasure_action_hanlder import MoveTreasureActionHandler
from .call_for_brawl_action_handler import CallForBrawlActionHandler

handlers: Dict[Action.ActionType, Type[ActionHandler]] = {
    Action.ActionType.CALL_FOR_AN_ATTACK: CallForAnAttackActionHandler,
    Action.ActionType.VOTE: VoteActionHandler,
    Action.ActionType.PUT_CHEST: PutChestActionHandler,
    Action.ActionType.MAROON_ANY_CREW_MATE_TO_TORTUGA: MaroonCrewActionHandler,
    Action.ActionType.MOVE: MoveActionHandler,
    Action.ActionType.MOVE_TREASURE: MoveTreasureActionHandler,
    Action.ActionType.CALL_FOR_BRAWL: CallForBrawlActionHandler
}
