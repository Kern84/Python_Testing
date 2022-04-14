correct_competition = "Spring Festival"
correct_club = "Simply Lift"


def test_purchase_places_should_reduce_club_points(
    client, mock_modified_competitions_date
):
    """
    Test the purchasePlaces path,
    with POST and a correct club, competition and places,
    it should return a 200 HTTP code (OK),
    the response should contain some text and the club should have a reduction of it's points.
    """
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": correct_competition,
            "club": correct_club,
            "places": 3,
        },
    )
    expected_value = 10
    data = response.data.decode()
    assert response.status_code == 200
    assert "Points available: {}".format(expected_value) in data
