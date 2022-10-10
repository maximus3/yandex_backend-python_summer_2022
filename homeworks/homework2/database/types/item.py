from enum import Enum

from database.proxy import items

ItemType = Enum(  # type: ignore
    'ItemType',
    {model_data['model'].name_for_enum: model_data for model_data in items},
)


item_types = list(ItemType)
