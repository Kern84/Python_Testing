import pytest
import server
from server import app


@pytest.fixture
def client():
    """Create a test browser."""
    client = app.test_client()
    yield client


@pytest.fixture
def clubs_loaded():
    """Copy of a JSON file. Used for comparison."""
    clubs = [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
        {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
    ]
    return clubs


@pytest.fixture
def competitions_loaded():
    """Copy of a JSON file. Used for comparison."""
    competitions = [
        {
            "name": "Spring Festival",
            "date": "2023-03-27 10:00:00",
            "numberOfPlaces": "25",
        },
        {"name": "Fall Classic", "date": "2020-10-22 13:30:00", "numberOfPlaces": "13"},
    ]
    return competitions


def modified_competitions_date():
    """Copy of the original competitions, with a difference of date for the first."""
    competitions = [
        {
            "name": "Spring Festival",
            "date": "2023-03-27 10:00:00",
            "numberOfPlaces": "25",
        },
        {"name": "Fall Classic", "date": "2020-10-22 13:30:00", "numberOfPlaces": "13"},
    ]
    return competitions


def modified_full_competitions():
    """Copy of the original competitions, with no available places and a difference of date for the first."""
    competitions = [
        {
            "name": "Spring Festival",
            "date": "2023-03-27 10:00:00",
            "numberOfPlaces": "0",
        },
        {"name": "Fall Classic", "date": "2020-10-22 13:30:00", "numberOfPlaces": "13"},
    ]
    return competitions


def clubs_to_mock():
    clubs = [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
        {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
    ]
    return clubs


@pytest.fixture
def mock_modified_competitions_date(mocker):
    """Mocking the original variable with our changes. Here, the date."""
    mocker.patch.object(server, "competitions", modified_competitions_date())


@pytest.fixture
def mock_modified_full_competitions(mocker):
    """Mocking the original variable with our changes. Here, the number of available places and date."""
    mocker.patch.object(server, "competitions", modified_full_competitions())


@pytest.fixture
def mock_club(mocker):
    """Mocking the clubs to have the same number of points for each test."""
    mocker.patch.object(server, "clubs", clubs_to_mock())
