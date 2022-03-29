import pytest
from server import app


@pytest.fixture
def client():
    client = app.test_client()
    yield client


@pytest.fixture
def list_club_email():
    list_club_email = [
        "john@simplylift.co",
        "admin@irontemple.com",
        "kate@shelifts.co.uk",
    ]
    return list_club_email


@pytest.fixture
def clubs_loaded():
    clubs = [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
        {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
    ]
    return clubs


@pytest.fixture
def competitions_loaded():
    competitions = [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25",
        },
        {"name": "Fall Classic", "date": "2020-10-22 13:30:00", "numberOfPlaces": "13"},
    ]
    return competitions
