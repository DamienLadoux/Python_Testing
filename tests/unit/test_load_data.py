import server
from unittest.mock import mock_open, patch
import pytest

def test_load_clubs():
    clubs = server.loadClubs()

    assert isinstance(clubs, list)
    assert len(clubs) > 0

    for club in clubs:
        assert 'name' in club
        assert 'email' in club
        assert 'points' in club


def test_load_clubs_file_not_found():
    with patch(
        'builtins.open',
        side_effect=FileNotFoundError
    ):
        with pytest.raises(FileNotFoundError):
            server.loadClubs()

def test_load_clubs_contains_iron_temple():
    clubs = server.loadClubs()

    iron_temple = [
        club for club in clubs
        if club['name'] == 'Iron Temple'
    ]

    assert len(iron_temple) == 1
    assert iron_temple[0]['email'] == 'admin@irontemple.com'
    assert iron_temple[0]['points'] == '4'


def test_load_clubs_raises_error_when_clubs_key_is_missing():
    json_content = '{"something_else": []}'

    with patch(
        'builtins.open',
        mock_open(read_data=json_content)
    ):
        with pytest.raises(KeyError):
            server.loadClubs()


def test_load_competitions():
    competitions = server.loadCompetitions()

    assert isinstance(competitions, list)
    assert len(competitions) > 0

    for competition in competitions:
        assert 'name' in competition
        assert 'date' in competition
        assert 'numberOfPlaces' in competition


def test_load_competitions_file_not_found():
    with patch(
        'builtins.open',
        side_effect=FileNotFoundError
    ):
        with pytest.raises(FileNotFoundError):
            server.loadCompetitions()


def test_load_competitions_contains_spring_festival():
    competitions = server.loadCompetitions()

    spring_festival = [
        competition
        for competition in competitions
        if competition['name'] == 'Spring Festival'
    ]

    assert len(spring_festival) == 1
    assert spring_festival[0]['date'] == '2020-03-27 10:00:00'
    assert spring_festival[0]['numberOfPlaces'] == '25'


def test_load_clubs_reads_clubs_json():
    json_content = '{"clubs": [{"name": "Test Club"}]}'

    with patch(
        'builtins.open',
        mock_open(read_data=json_content)
    ):
        clubs = server.loadClubs()

    assert clubs == [{'name': 'Test Club'}]


def test_load_competitions_reads_competitions_json():
    json_content = (
        '{"competitions": [{"name": "Test Competition"}]}'
    )

    with patch(
        'builtins.open',
        mock_open(read_data=json_content)
    ):
        competitions = server.loadCompetitions()

    assert competitions == [{'name': 'Test Competition'}]


def test_load_competitions_raises_error_when_competitions_key_is_missing():
    json_content = '{"something_else": []}'

    with patch(
        'builtins.open',
        mock_open(read_data=json_content)
    ):
        with pytest.raises(KeyError):
            server.loadCompetitions()
