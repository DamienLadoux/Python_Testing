import server


def test_get_clubs_points_returns_club_names(monkeypatch):
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

    result = server.get_clubs_points()

    assert result[0]['name'] == 'Iron Temple'
    assert result[1]['name'] == 'Blue Club'


def test_get_clubs_points_returns_current_points(monkeypatch):
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

    result = server.get_clubs_points()

    assert result[0]['points'] == '20'
    assert result[1]['points'] == '15'