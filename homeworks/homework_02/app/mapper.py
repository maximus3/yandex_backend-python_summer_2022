from app.schemas.check import Problem
from database.types import ItemType

ITEM_TYPE_TO_NO_USER_PROBLEM = {
    ItemType.common: Problem.NO_USER,  # type: ignore
    ItemType.receipt: Problem.NO_USER_NO_RECEIPT,  # type: ignore
    ItemType.special: Problem.NO_USER_SPECIAL_ITEM,  # type: ignore
}
