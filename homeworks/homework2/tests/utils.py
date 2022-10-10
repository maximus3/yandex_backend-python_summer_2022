def route_creator(user_id, items):
    return f'/check?user_id={user_id}' + ''.join(
        map(lambda item_id: f'&item_id={item_id}', items)
    )
