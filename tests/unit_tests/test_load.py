from server import loadClubs, loadCompetitions


def test_should_load_clubs(clubs_loaded):
    """Test if the JSON file that contains the clubs and their information is correctly loaded."""
    sut = loadClubs()
    expected_value = clubs_loaded
    assert sut == expected_value


def test_should_load_competitions(competitions_loaded):
    """Test if the JSON file that contains the competitions and their information is correctly loaded."""
    sut = loadCompetitions()
    expected_value = competitions_loaded
    assert sut == expected_value
