from fastapi import APIRouter, Query, status

from app.mapper import ITEM_TYPE_TO_NO_USER_PROBLEM
from app.schemas import CheckResponse, CheckResponseItem
from app.schemas.check import Problem
from app.validators import ItemIdValidator, RightsValidator
from database import views

api_router = APIRouter(tags=['Check'])


@api_router.get(
    '/check',
    response_model=list,
    status_code=status.HTTP_200_OK,
)
async def check(
    user_id: int, items: list[str] = Query(..., alias='item_id')
) -> list[CheckResponseItem]:
    response = CheckResponse()
    account, account_type = await views.get_user(user_id)
    no_user = account is None or account_type is None
    for item_id in items:
        problem, item_id, (item_type, _id) = await ItemIdValidator.validate(
            item_id
        )
        if problem != Problem.OK or item_type is None or _id is None:
            response.items.append(
                CheckResponseItem(item_id=item_id, problem=problem)
            )
            continue
        item = await item_type.value['proxy'].get(id=_id)
        if item is None:
            response.items.append(
                CheckResponseItem(
                    item_id=item_id, problem=Problem.ITEM_NOT_FOUND
                )
            )
            continue
        if no_user:
            response.items.append(
                CheckResponseItem(
                    item_id=item_id,
                    problem=ITEM_TYPE_TO_NO_USER_PROBLEM[item_type],
                )
            )
            continue
        problem = await RightsValidator.validate(
            account, account_type, item, item_type  # type: ignore
        )
        if problem != Problem.OK:
            response.items.append(
                CheckResponseItem(item_id=item_id, problem=problem)
            )
    return response.items
