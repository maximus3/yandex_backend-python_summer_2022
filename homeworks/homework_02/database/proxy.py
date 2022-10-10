from typing import Any, Type, TypeVar

from sqlalchemy.orm import Session as SessionType

from database.connection import create_session
from database.models import (
    Account,
    Base,
    CommonItem,
    DoctorAccount,
    Item,
    ReceiptItem,
    SpecialItem,
    UserAccount,
)

BaseProxyType = TypeVar('BaseProxyType', bound='BaseProxy')


class BaseProxy:
    BASE_MODEL: Type[Base] = Base

    def __init__(self, base_model: Base):
        self.id = base_model.id

    @classmethod
    async def get(
        cls: Type[BaseProxyType],
        session: SessionType = None,
        **kwargs: Any,
    ) -> BaseProxyType | None:
        if session is None:
            with create_session() as new_session:
                return await cls.get(new_session, **kwargs)
        model = session.query(cls.BASE_MODEL).filter_by(**kwargs).one_or_none()
        if model:
            return cls(model)
        return None


class AccountProxy(BaseProxy):
    BASE_MODEL = Account

    def __init__(self, account: Account):
        super().__init__(account)
        self.full_name = account.full_name
        self.phone = account.phone
        self.password_hash = account.password_hash


class UserAccountProxy(AccountProxy):
    BASE_MODEL = UserAccount

    def __init__(self, account: UserAccount):
        super().__init__(account)
        self.receipt = account.receipt


class DoctorAccountProxy(AccountProxy):
    BASE_MODEL = DoctorAccount

    def __init__(self, account: DoctorAccount):
        super().__init__(account)
        self.specialty_id = account.specialty_id


class ItemProxy(BaseProxy):
    BASE_MODEL = Item

    def __init__(self, item: Item):
        super().__init__(item)
        self.name = item.name
        self.amount = item.amount
        self.price = item.price
        self.dosage_form = item.dosage_form
        self.manufacturer = item.manufacturer
        self.barcode = item.barcode


class CommonItemProxy(ItemProxy):
    BASE_MODEL = CommonItem

    def __init__(self, item: CommonItem):
        super().__init__(item)


class ReceiptItemProxy(ItemProxy):
    BASE_MODEL = ReceiptItem

    def __init__(self, item: ReceiptItem):
        super().__init__(item)


class SpecialItemProxy(ItemProxy):
    BASE_MODEL = SpecialItem

    def __init__(self, item: SpecialItem):
        super().__init__(item)
        self.specialty_id = item.specialty_id


accounts = [
    {
        'model': UserAccount,
        'proxy': UserAccountProxy,
    },
    {
        'model': DoctorAccount,
        'proxy': DoctorAccountProxy,
    },
]

items = [
    {
        'model': CommonItem,
        'proxy': CommonItemProxy,
    },
    {
        'model': ReceiptItem,
        'proxy': ReceiptItemProxy,
    },
    {
        'model': SpecialItem,
        'proxy': SpecialItemProxy,
    },
]
