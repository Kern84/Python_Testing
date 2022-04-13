dict_correct_email = {"email": "john@simplylift.co"}
dict_wrong_email = {"email": "wrong@email.fr"}
dict_wrong_input = {"email": "1"}
correct_competition = "Spring Festival"
correct_club = "Simply Lift"
not_enough_points_club = "Iron Temple"


class TestPurchasePlaces:
    """Class where the purchasePlaces function is tested."""

    def test_purchase_places_should_reduce_club_points_success(
        self, client, mock_modified_competitions_date
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
        print("BBBB", data)
        assert response.status_code == 200
        assert "Points available: {}".format(expected_value) in data

    def test_purchase_places_should_reduce_competition_points_success(
        self, client, mock_modified_competitions_date
    ):
        """
        Test the purchasePlaces path,
        with POST and a correct club, competition and places,
        it should return a 200 HTTP code (OK),
        the response should contain some text and the competition should have a reduction of it's available places.
        """
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": correct_competition,
                "club": correct_club,
                "places": 1,
            },
        )
        expected_value = 24
        data = response.data.decode()
        assert response.status_code == 200
        assert "Number of Places: {}".format(expected_value) in data

    def test_get_purchase_should_fail(self, client):
        """Test the purchasePlaces path, with GET, it should return a 405 HTTP code (Method Not Allowed)."""
        response = client.get("/purchasePlaces")
        assert response.status_code == 405
