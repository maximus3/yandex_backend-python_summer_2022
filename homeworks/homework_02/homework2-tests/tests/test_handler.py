import pytest
import requests


ENDPOINT = 'http://localhost:8090/check'

PROBLEMS = [
    'WRONG_CATEGORY',
    'INCORRECT_ITEM_ID',
    'ITEM_NOT_FOUND',
    'NO_USER',
    'NO_USER_NO_RECEIPT',
    'NO_USER_SPECIAL_ITEM',
    'NO_RECEIPT',
    'ITEM_IS_SPECIAL',
    'ITEM_SPECIAL_WRONG_SPECIFIC',
]


def has_uppercase_letters(text: str) -> bool:
    for ch in text:
        if ch.isupper():
            return True
    return False


def problem_exists(problem: str) -> bool:
    return problem in PROBLEMS


@pytest.mark.parametrize(
    'user_id,items',
    [
        pytest.param(
            100500,  # absent user
            {
                'bad-category-id_1': 'WRONG_CATEGORY',
            },
            id='wrong-category',
        ),
        pytest.param(
            100500,  # absent user
            {
                'common_blah': 'INCORRECT_ITEM_ID',
            },
            id='good-category-bad-id',
        ),
        pytest.param(
            100500,  # absent user
            {
                'common_100500': 'ITEM_NOT_FOUND',
            },
            id='item-not-found',
        ),
        pytest.param(
            100500,  # absent user
            {
                'common_8': 'NO_USER',
            },
            id='user-not-found-but-we-can-sell-item',
        ),
        pytest.param(
            100500,  # absent user
            {
                'receipt_8': 'NO_USER_NO_RECEIPT',
            },
            id='user-not-found-item-by-receipt',
        ),
        pytest.param(
            100500,  # absent user
            {
                'special_8': 'NO_USER_SPECIAL_ITEM',
            },
            id='user-not-found-special-item',
        ),
        pytest.param(
            4,
            {
                'receipt_11': 'NO_RECEIPT',
            },
            id='user-found-by-no-receipt',
        ),
        pytest.param(
            5,
            {
                'special_8': 'ITEM_IS_SPECIAL',
            },
            id='user-try-to-buy-special-item',
        ),
        pytest.param(
            63,
            {
                'special_24': 'ITEM_SPECIAL_WRONG_SPECIFIC',
            },
            id='doctor-speciality-mismatch',
        ),
        pytest.param(
            63,
            {
                'special_52': None,
                'common_1234': 'ITEM_NOT_FOUND',
            },
            id='special-item-doctor-ok',
        ),
        pytest.param(
            4,
            {
                'common_5': None,
                'special_1234': 'ITEM_NOT_FOUND',
            },
            id='common-item-user-ok',
        ),
        pytest.param(
            4,
            {
                'receipt_68': None,
                'special_1234': 'ITEM_NOT_FOUND',
            },
            id='receipt-item-user-has-receipt-ok',
        ),
        pytest.param(
            63,
            {
                'common_5': None,
                'special_1234': 'ITEM_NOT_FOUND',
            },
            id='doctor-any-common-item-ok',
        ),
        pytest.param(
            63,
            {
                'receipt_68': None,
                'special_1234': 'ITEM_NOT_FOUND',
            },
            id='doctor-any-receipt-item-ok',
        ),
        pytest.param(
            63,
            {
                'common_5': None,
                'receipt_68': None,
                'special_52': None,
                'special_24': 'ITEM_SPECIAL_WRONG_SPECIFIC',
            },
            id='doctor-some-cases-in-one-request',
        ),
        pytest.param(
            4,
            {
                'common_5': None,
                'receipt_68': None,
                'receipt_11': 'NO_RECEIPT',
                'special_8': 'ITEM_IS_SPECIAL',
            },
            id='user-some-cases-in-one-request',
        ),
    ],
)
def test(user_id, items):
    got = requests.get(
        ENDPOINT, params={'user_id': user_id, 'item_id': list(items.keys())}
    )
    print(user_id, items, got.json())

    assert got.status_code == 200

    response_item_ids = set()

    for resp_item in got.json():
        resp_item_id = resp_item.get('item_id')
        resp_problem = resp_item.get('problem')
        assert resp_item_id, 'Response items has no "item_id" field'
        assert resp_problem, 'Response item has no "problems" field'
        assert not has_uppercase_letters(
            resp_item_id
        ), 'item_id in response has uppercase letters'
        assert problem_exists(resp_problem), (
            f'Unexpected problem code. '
            f'Got: {resp_problem} but [{PROBLEMS}] expected'
        )
        assert (
            resp_item_id in items
        ), f'Got item_id: "{resp_item_id}" that was not in the request'

        if items[resp_item_id] is not None:
            assert items[resp_item_id] == resp_problem, (
                f'Incorect problem for item_id: "{resp_item_id}". '
                f'Expected: "{items[resp_item_id]}", got: "{resp_problem}"'
            )

        response_item_ids.add(resp_item_id)

    expected_in_response = set(ii for ii in items if items[ii] is not None)
    missing_item_ids = expected_in_response - response_item_ids

    assert (
        not missing_item_ids
    ), f'Some item_ids is missing in response: [{missing_item_ids}]'

    expected_not_in_response = set(ii for ii in items if items[ii] is None)
    extra_item_ids = response_item_ids & expected_not_in_response

    assert (
        not extra_item_ids
    ), f'Got unexpected item_ids in response: [{extra_item_ids}]'
