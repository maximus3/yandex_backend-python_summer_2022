from fastapi import status

from app.schemas.check import Problem
from database.types import ItemType
from tests.utils import route_creator


async def test_no_items(client):
    response = await client.get(route_creator(user_id=1, items=[]))
    assert (
        response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    ), response.json()


async def test_wrong_category(client):
    response = await client.get(route_creator(user_id=1, items=['random_123']))
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json() == [
        {'item_id': 'random_123', 'problem': Problem.WRONG_CATEGORY}
    ]


async def test_incorrect_item_id(client):
    item_id = f'{ItemType.common.name}_a'
    response = await client.get(route_creator(user_id=1, items=[item_id]))
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json() == [
        {'item_id': item_id, 'problem': Problem.INCORRECT_ITEM_ID}
    ]


async def test_item_not_found(client):
    item_id = f'{ItemType.common.name}_9999'
    response = await client.get(route_creator(user_id=1, items=[item_id]))
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json() == [
        {'item_id': item_id, 'problem': Problem.ITEM_NOT_FOUND}
    ]


async def test_no_user(client):
    item_id = f'{ItemType.common.name}_1'
    response = await client.get(route_creator(user_id=9999, items=[item_id]))
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json() == [
        {'item_id': item_id, 'problem': Problem.NO_USER}
    ]


async def test_no_user_no_receipt(client):
    item_id = f'{ItemType.receipt.name}_1'
    response = await client.get(route_creator(user_id=9999, items=[item_id]))
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json() == [
        {'item_id': item_id, 'problem': Problem.NO_USER_NO_RECEIPT}
    ]


async def test_no_user_special_item(client):
    item_id = f'{ItemType.special.name}_1'
    response = await client.get(route_creator(user_id=9999, items=[item_id]))
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json() == [
        {'item_id': item_id, 'problem': Problem.NO_USER_SPECIAL_ITEM}
    ]


async def test_no_receipt(client):
    item_id = f'{ItemType.receipt.name}_1'
    response = await client.get(route_creator(user_id=1, items=[item_id]))
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json() == [
        {'item_id': item_id, 'problem': Problem.NO_RECEIPT}
    ]


async def test_item_is_special(client):
    item_id = f'{ItemType.special.name}_1'
    response = await client.get(route_creator(user_id=1, items=[item_id]))
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json() == [
        {'item_id': item_id, 'problem': Problem.ITEM_IS_SPECIAL}
    ]


async def test_item_special_wrong_specific(client):
    item_id = f'{ItemType.special.name}_1'
    response = await client.get(route_creator(user_id=61, items=[item_id]))
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json() == [
        {'item_id': item_id, 'problem': Problem.ITEM_SPECIAL_WRONG_SPECIFIC}
    ]


async def test_item_special_wrong_specific_to_lower(client):
    item_id = f'{ItemType.special.name.upper()}_1'
    response = await client.get(route_creator(user_id=61, items=[item_id]))
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json() == [
        {
            'item_id': item_id.lower(),
            'problem': Problem.ITEM_SPECIAL_WRONG_SPECIFIC,
        }
    ]


async def test_ok(client):
    item_id = f'{ItemType.common.name}_1'
    response = await client.get(route_creator(user_id=1, items=[item_id]))
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json() == []
