import server


def test_points_display_board(monkeypatch):
    monkeypatch.setattr(
        server,
        'clubs',
        [
            {
                'name': 'Iron Temple',
                'email': 'admin@irontemple.com',
                'points': '20'
            },
            {
                'name': 'Blue Club',
                'email': 'admin@blueclub.com',
                'points': '15'
            }
        ]
    )

    client = server.app.test_client()

    response = client.get('/points')

    assert response.status_code == 200
    assert b'Iron Temple: 20 points' in response.data
    assert b'Blue Club: 15 points' in response.data