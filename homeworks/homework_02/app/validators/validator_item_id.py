from app.schemas.check import Problem
from database.types import ItemType, item_types


def _valid_category(item_id: str) -> Problem:
    category, _ = item_id.split('_')
    if category not in map(lambda item_type: item_type.name, item_types):
        return Problem.WRONG_CATEGORY
    return Problem.OK


def _valid_id(item_id: str) -> Problem:
    _, _id = item_id.split('_')
    if _id.isdigit():
        return Problem.OK
    return Problem.INCORRECT_ITEM_ID


class Validator:
    _validators = [_valid_category, _valid_id]

    @classmethod
    async def validate(
        cls, item_id: str
    ) -> tuple[Problem, str, tuple[ItemType | None, int | None]]:
        item_id = item_id.lower()
        for func in cls._validators:
            problem = func(item_id)
            if problem != Problem.OK:
                return problem, item_id, (None, None)
        return Problem.OK, item_id, cls.split_item_id(item_id)

    @staticmethod
    def split_item_id(item_id: str) -> tuple[ItemType, int]:
        category, _id = item_id.split('_')
        return ItemType[category], int(_id)
