async def test_health_check(client):
    response = await client.get(f'/health_check/ping')
    assert response.status_code == 200
    assert response.json() == {'message': 'Pong!'}
