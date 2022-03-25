from server import loadClubs, loadCompetitions


def test_should_load_clubs():
    sut = loadClubs()
    expected_value = [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
        {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
    ]
    assert sut == expected_value


def test_should_load_competitions():
    sut = loadCompetitions()
    expected_value = [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25",
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13",
        },
    ]
    assert sut == expected_value
