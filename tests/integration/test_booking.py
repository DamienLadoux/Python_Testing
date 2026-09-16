import server


def test_cannot_book_more_places_than_available(monkeypatch):
    monkeypatch.setattr(
        server,
        'competitions',
        [
            {
                'name': 'Spring Festival',
                'date': '2020-03-27 10:00:00',
                'numberOfPlaces': '25'
            }
        ]
    )

    client = server.app.test_client()

    response = client.post(
        '/purchasePlaces',
        data={
            'competition': 'Spring Festival',
            'club': 'Iron Temple',
            'places': '26'
        }
    )

    assert response.status_code == 200

    assert server.competitions[0]['numberOfPlaces'] == '25'


def test_can_book_available_places(monkeypatch):
    monkeypatch.setattr(
        server,
        'competitions',
        [
            {
                'name': 'Spring Festival',
                'date': '2020-03-27 10:00:00',
                'numberOfPlaces': '25'
            }
        ]
    )

    client = server.app.test_client()

    response = client.post(
        '/purchasePlaces',
        data={
            'competition': 'Spring Festival',
            'club': 'Iron Temple',
            'places': '2'
        }
    )

    assert response.status_code == 200

    assert server.competitions[0]['numberOfPlaces'] == 23


def test_cannot_redeem_more_points_than_available(monkeypatch):
    monkeypatch.setattr(
        server,
        'competitions',
        [
            {
                'name': 'Spring Festival',
                'date': '2020-03-27 10:00:00',
                'numberOfPlaces': '25'
            }
        ]
    )

    monkeypatch.setattr(
        server,
        'clubs',
        [
            {
                'name': 'Iron Temple',
                'email': 'admin@irontemple.com',
                'points': '4'
            }
        ]
    )

    client = server.app.test_client()

    response = client.post(
        '/purchasePlaces',
        data={
            'competition': 'Spring Festival',
            'club': 'Iron Temple',
            'places': '5'
        }
    )

    assert response.status_code == 200
    assert server.clubs[0]['points'] == '4'
    assert server.competitions[0]['numberOfPlaces'] == '25'


def test_redeem_points_are_deducted(monkeypatch):
    monkeypatch.setattr(
        server,
        'competitions',
        [
            {
                'name': 'Spring Festival',
                'date': '2020-03-27 10:00:00',
                'numberOfPlaces': '25'
            }
        ]
    )

    monkeypatch.setattr(
        server,
        'clubs',
        [
            {
                'name': 'Iron Temple',
                'email': 'admin@irontemple.com',
                'points': '4'
            }
        ]
    )

    client = server.app.test_client()

    response = client.post(
        '/purchasePlaces',
        data={
            'competition': 'Spring Festival',
            'club': 'Iron Temple',
            'places': '2'
        }
    )

    assert response.status_code == 200
    assert server.clubs[0]['points'] == 2
    assert server.competitions[0]['numberOfPlaces'] == 23


def test_cannot_book_more_than_12_places(monkeypatch):
    monkeypatch.setattr(
        server,
        'competitions',
        [
            {
                'name': 'Spring Festival',
                'date': '2020-03-27 10:00:00',
                'numberOfPlaces': '25'
            }
        ]
    )

    monkeypatch.setattr(
        server,
        'clubs',
        [
            {
                'name': 'Iron Temple',
                'email': 'admin@irontemple.com',
                'points': '20'
            }
        ]
    )

    client = server.app.test_client()

    response = client.post(
        '/purchasePlaces',
        data={
            'competition': 'Spring Festival',
            'club': 'Iron Temple',
            'places': '13'
        }
    )

    assert response.status_code == 200
    assert server.competitions[0]['numberOfPlaces'] == '25'
    assert server.clubs[0]['points'] == '20'


def test_can_book_12_places(monkeypatch):
    monkeypatch.setattr(
        server,
        'competitions',
        [
            {
                'name': 'Spring Festival',
                'date': '2020-03-27 10:00:00',
                'numberOfPlaces': '25'
            }
        ]
    )

    monkeypatch.setattr(
        server,
        'clubs',
        [
            {
                'name': 'Iron Temple',
                'email': 'admin@irontemple.com',
                'points': '20'
            }
        ]
    )

    client = server.app.test_client()

    response = client.post(
        '/purchasePlaces',
        data={
            'competition': 'Spring Festival',
            'club': 'Iron Temple',
            'places': '12'
        }
    )

    assert response.status_code == 200
    assert server.competitions[0]['numberOfPlaces'] == 13
    assert server.clubs[0]['points'] == 8

def test_cannot_book_past_competition(monkeypatch):
    monkeypatch.setattr(
        server,
        'competitions',
        [
            {
                'name': 'Past Competition',
                'date': '2020-01-01 10:00:00',
                'numberOfPlaces': '25'
            }
        ]
    )

    monkeypatch.setattr(
        server,
        'clubs',
        [
            {
                'name': 'Iron Temple',
                'email': 'admin@irontemple.com',
                'points': '20'
            }
        ]
    )

    client = server.app.test_client()

    response = client.get(
        '/book/Past Competition/Iron Temple'
    )

    assert response.status_code == 200
    assert b'<form action="/purchasePlaces" method="post">' not in response.data


def test_can_book_future_competition(monkeypatch):
    monkeypatch.setattr(
        server,
        'competitions',
        [
            {
                'name': 'Future Competition',
                'date': '2099-01-01 10:00:00',
                'numberOfPlaces': '25'
            }
        ]
    )

    monkeypatch.setattr(
        server,
        'clubs',
        [
            {
                'name': 'Iron Temple',
                'email': 'admin@irontemple.com',
                'points': '20'
            }
        ]
    )

    client = server.app.test_client()

    response = client.get(
        '/book/Future Competition/Iron Temple'
    )

    assert response.status_code == 200
    assert b'Future Competition' in response.data
    assert b'<form action="/purchasePlaces" method="post">' in response.data


def test_points_are_updated_in_response(monkeypatch):
    monkeypatch.setattr(
        server,
        'competitions',
        [
            {
                'name': 'Spring Festival',
                'date': '2099-03-27 10:00:00',
                'numberOfPlaces': '25'
            }
        ]
    )

    monkeypatch.setattr(
        server,
        'clubs',
        [
            {
                'name': 'Iron Temple',
                'email': 'admin@irontemple.com',
                'points': '4'
            }
        ]
    )

    client = server.app.test_client()

    response = client.post(
        '/purchasePlaces',
        data={
            'competition': 'Spring Festival',
            'club': 'Iron Temple',
            'places': '2'
        }
    )

    assert response.status_code == 200
    assert b'Points available: 2' in response.data
