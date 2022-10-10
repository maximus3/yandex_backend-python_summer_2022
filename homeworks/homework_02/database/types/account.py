from enum import Enum

from database.proxy import accounts

AccountType = Enum(  # type: ignore
    'AccountType',
    {model_data['model'].__tablename__: model_data for model_data in accounts},
)


account_types = list(AccountType)
