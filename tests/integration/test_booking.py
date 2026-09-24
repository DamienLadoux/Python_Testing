import server


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
