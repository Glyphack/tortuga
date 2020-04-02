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
from .call_for_mutiny_action_handler import CallForMutinyActionHandler
from .view_two_event_cards import ViewTwoEventCardsActionHandler
from .reveal_event_card_action_handler import RevealEventCardActionHandler
from .keep_event_card_action_handler import KeepEventCardActionHandler
from .see_event_card_options import SeeEventCardOptions
from .use_event_card import UseEventCardActionHandler

handlers: Dict[Action.ActionType, Type[ActionHandler]] = {
    Action.ActionType.CALL_FOR_AN_ATTACK: CallForAnAttackActionHandler,
    Action.ActionType.VOTE: VoteActionHandler,
    Action.ActionType.PUT_CHEST: PutChestActionHandler,
    Action.ActionType.MAROON_ANY_CREW_MATE_TO_TORTUGA: MaroonCrewActionHandler,
    Action.ActionType.MOVE: MoveActionHandler,
    Action.ActionType.MOVE_TREASURE: MoveTreasureActionHandler,
    Action.ActionType.CALL_FOR_BRAWL: CallForBrawlActionHandler,
    Action.ActionType.CALL_FOR_A_MUTINY: CallForMutinyActionHandler,
    Action.ActionType.VIEW_TWO_EVENT_CARDS: ViewTwoEventCardsActionHandler,
    Action.ActionType.REVEAL_EVENT_CARD: RevealEventCardActionHandler,
    Action.ActionType.KEEP_EVENT_CARD: KeepEventCardActionHandler,
    Action.ActionType.SEE_EVENT_CARD_OPTIONS: SeeEventCardOptions,
    Action.ActionType.USE_EVENT_CARD: UseEventCardActionHandler
}
