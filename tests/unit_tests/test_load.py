from server import loadClubs, loadCompetitions


def test_should_load_clubs(clubs_loaded):
    sut = loadClubs()
    expected_value = clubs_loaded
    assert sut == expected_value


def test_should_load_competitions(competitions_loaded):
    sut = loadCompetitions()
    expected_value = competitions_loaded
    assert sut == expected_value
