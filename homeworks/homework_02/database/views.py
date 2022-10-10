from database.connection import create_session
from database.models import Receipt
from database.proxy import AccountProxy
from database.types import AccountType, account_types


async def get_user(
    user_id: int,
) -> tuple[AccountProxy | None, AccountType | None]:
    with create_session() as session:
        for account_type in account_types:
            account_proxy = account_type.value['proxy']
            user = await account_proxy.get(session=session, id=user_id)
            if user is None:
                continue
            return user, account_type
        return None, None


async def has_receipt(user_id: int, item_id: int) -> bool:
    with create_session() as session:
        receipt = (
            session.query(Receipt)
            .filter(Receipt.user_id == user_id, Receipt.item_id == item_id)
            .first()
        )
        return receipt is not None
