from app.schemas.check import Problem
from database import views
from database.models import Account, Item, ReceiptItem, SpecialItem
from database.types import AccountType, ItemType


async def _validate_account_have_receipt(
    account: Account, item: ReceiptItem
) -> Problem:
    return (
        Problem.OK
        if await views.has_receipt(account.id, item.id)
        else Problem.NO_RECEIPT
    )


async def _validate_account_correct_specialty(
    account: Account, item: SpecialItem
) -> Problem:
    return (
        Problem.OK
        if account.specialty_id == item.specialty_id
        else Problem.ITEM_SPECIAL_WRONG_SPECIFIC
    )


async def _return_arg(arg: Problem) -> Problem:
    return arg


class Validator:
    _validators = {
        'user_account': {
            'common': lambda _, __: _return_arg(Problem.OK),
            'receipt': _validate_account_have_receipt,
            'special': lambda _, __: _return_arg(Problem.ITEM_IS_SPECIAL),
        },
        'doctor_account': {
            'common': lambda _, __: _return_arg(Problem.OK),
            'receipt': lambda _, __: _return_arg(Problem.OK),
            'special': _validate_account_correct_specialty,
        },
    }

    @classmethod
    async def validate(
        cls,
        account: Account,
        account_type: AccountType,
        item: Item,
        item_type: ItemType,
    ) -> Problem:
        return await cls._validators[account_type.name][item_type.name](
            account, item
        )
