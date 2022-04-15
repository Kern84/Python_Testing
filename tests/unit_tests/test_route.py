dict_correct_email = {"email": "john@simplylift.co"}
dict_wrong_email = {"email": "wrong@email.fr"}
dict_wrong_input = {"email": "1"}
correct_competition = "Spring Festival"
correct_club = "Simply Lift"
not_enough_points_club = "Iron Temple"


class TestIndex:
    """Class where the Index function is tested."""

    def test_index_success(self, client):
        """Test the index path, with GET, it should return a 200 HTTP code (OK)."""
        response = client.get("/")
        assert response.status_code == 200

    def test_post_index_should_fail(self, client):
        """Test the index path, with POST, it should return a 405 HTTP code (Method Not Allowed)."""
        response = client.post("/")
        assert response.status_code == 405


class TestShowSummary:
    """Class where the showSummary function is tested."""

    def test_login_sucess(self, client):
        """
        Test the showSummary path,
        with POST and a correct email,
        it should return a 200 HTTP code (OK) and the response should contain some text.
        """
        response = client.post("/showSummary", data=dict(dict_correct_email))
        data = response.data.decode()
        assert response.status_code == 200
        assert "Welcome, {}".format(dict_correct_email["email"]) in data

    def test_login_should_fail(self, client):
        """
        Test the showSummary path,
        with POST and a wrong email,
        it should return a 200 HTTP code (OK) and the response should return an error message.
        """
        response = client.post("/showSummary", data=dict(dict_wrong_email))
        data = response.data.decode()
        assert response.status_code == 200
        assert "Sorry, that email" in data

    def test_login_wrong_input_should_fail(self, client):
        """
        Test the showSummary path,
        with POST and a wrong input,
        it should return a 200 HTTP code (OK) and the response should return an error message.
        """
        response = client.post("/showSummary", data=dict(dict_wrong_input))
        data = response.data.decode()
        assert response.status_code == 200
        assert "Sorry, that email" in data

    def test_login_no_input_should_fail(self, client):
        """
        Test the showSummary path,
        with POST and no input,
        it should return a 200 HTTP code (OK) and the response should return an error message.
        """
        response = client.post("/showSummary", data={"email": ""})
        data = response.data.decode()
        assert response.status_code == 200
        assert "Sorry, that email" in data

    def test_get_show_summary_should_fail(self, client):
        """
        Test the showSummary path,
        with GET,
        it should return a 405 HTTP code (Method Not Allowed).
        """
        response = client.get("/showSummary")
        assert response.status_code == 405


class TestBook:
    """Class where the book function is tested."""

    def test_book_path_success(self, client, mock_modified_competitions_date):
        """
        Test the book path,
        with GET and a correct club and competition,
        it should return a 200 HTTP code (OK) and the response should contain some text.
        """
        response = client.get("/book/Spring%20Festival/Simply%20Lift")
        data = response.data.decode()
        assert response.status_code == 200
        assert correct_competition in data
        assert correct_club in data

    def test_book_wrong_path_should_fail(self, client):
        """
        Test the book path,
        with GET and a wrong club and competition,
        it should return a 302 HTTP code (Found) and the response should return an error message.
        """
        response = client.get("/book/WrongComp/WrongClub")
        assert response.status_code == 302

    def test_book_wrong_competition_path_should_fail(
        self, client, mock_modified_competitions_date
    ):
        """
        Test the book path,
        with GET and a wrong competition and a correct club,
        it should return a 200 HTTP code (OK) and the response should return an error message.
        """
        response = client.get("/book/WrongComp/Simply%20Lift")
        data = response.data.decode()
        assert response.status_code == 200
        assert "Something went wrong-please try again" in data

    def test_book_wrong_club_path_should_fail(
        self, client, mock_modified_competitions_date
    ):
        """
        Test the book path,
        with GET and a wrong club and a correct competition,
        it should return a 302 HTTP code (Found) and the response should return an error message.
        """
        response = client.get("/book/Spring%20Festival/WrongClub")
        assert response.status_code == 302

    def test_book_full_competition_should_fail(
        self, client, mock_modified_full_competitions
    ):
        """
        Test the book path,
        with GET and a correct club and competition but the competition is full,
        it should return a 200 HTTP code (OK) and the response should return an error message.
        """
        response = client.get("/book/Spring%20Festival/Simply%20Lift")
        data = response.data.decode()
        assert response.status_code == 200
        assert "Something went wrong-please try again" in data

    def test_book_root_path_should_fail(self, client):
        """
        Test the book path,
        with GET and no club or competition,
        it should return a 404 HTTP code because the page doesn't exist.
        """
        response = client.get("/book/")
        assert response.status_code == 404

    def test_post_book_should_fail(self, client, mock_modified_competitions_date):
        """Test the book path, with POST, it should return a 405 HTTP code (Method Not Allowed)."""
        response = client.post("/book/Spring%20Festival/Simply%20Lift")
        assert response.status_code == 405

    def test_book_past_competition_should_fail(self, client):
        """
        Test the book path,
        with GET and a correct club and competition but the competition has already passed,
        it should return a 200 HTTP code (OK) and the response should return an error message.
        """
        response = client.get("/book/Fall%20Classic/Simply%20Lift")
        data = response.data.decode()
        assert response.status_code == 200
        assert "You cannot book places for a past competition" in data


class TestPurchasePlaces:
    """Class where the purchasePlaces function is tested."""

    def test_purchase_correct_number_of_places_success(
        self, client, mock_modified_competitions_date, mock_club
    ):
        """
        Test the purchasePlaces path,
        with POST and a correct club, competition and places (between 1 and 12),
        it should return a 200 HTTP code (OK) and the response should contain some text.
        """
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": correct_competition,
                "club": correct_club,
                "places": "2",
            },
        )
        data = response.data.decode()
        assert response.status_code == 200
        assert "Great-booking complete!" in data

    def test_purchase_zero_place_should_fail(
        self, client, mock_modified_competitions_date, mock_club
    ):
        """
        Test the purchasePlaces path,
        with POST and a correct club, competition and zero places,
        it should return a 200 HTTP code (OK) and the response should return an error message.
        """
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": correct_competition,
                "club": correct_club,
                "places": "0",
            },
        )
        data = response.data.decode()
        assert response.status_code == 200
        assert (
            "You must register a positive number of places (between 1 and 12)" in data
        )

    def test_purchase_negative_number_of_places_should_fail(
        self, client, mock_modified_competitions_date, mock_club
    ):
        """
        Test the purchasePlaces path,
        with POST and a correct club, competition and a negative number of places,
        it should return a 200 HTTP code (OK) and the response should return an error message.
        """
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": correct_competition,
                "club": correct_club,
                "places": "-2",
            },
        )
        data = response.data.decode()
        assert response.status_code == 200
        assert (
            "You must register a positive number of places (between 1 and 12)" in data
        )

    def test_purchase_too_much_places_should_fail(
        self, client, mock_modified_competitions_date, mock_club
    ):
        """
        Test the purchasePlaces path,
        with POST and a correct club, competition and too much places,
        it should return a 200 HTTP code (OK) and the response should return an error message.
        """
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": correct_competition,
                "club": correct_club,
                "places": "15",
            },
        )
        data = response.data.decode()
        assert response.status_code == 200
        assert (
            "You must register a positive number of places (between 1 and 12)" in data
        )

    def test_purchase_places_with_not_enough_points_should_fail(
        self, client, mock_modified_competitions_date, mock_club
    ):
        """
        Test the purchasePlaces path,
        with POST and a correct club, competition and places but the club does not have enough points,
        it should return a 200 HTTP code (OK) and the response should return an error message.
        """
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": correct_competition,
                "club": not_enough_points_club,
                "places": "8",
            },
        )
        data = response.data.decode()
        assert response.status_code == 200
        assert "You do not have enough points to make this booking" in data

    def test_purchase_places_should_reduce_club_points(
        self, client, mock_modified_competitions_date, mock_club
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
                "places": "1",
            },
        )
        expected_value = "10"
        data = response.data.decode()
        assert response.status_code == 200
        assert "Points available: {}".format(expected_value) in data

    def test_purchase_places_should_reduce_competition_points_success(
        self, client, mock_modified_competitions_date, mock_club
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
                "places": "1",
            },
        )
        expected_value = "24"
        data = response.data.decode()
        assert response.status_code == 200
        assert "Number of Places: {}".format(expected_value) in data

    def test_get_purchase_should_fail(self, client):
        """Test the purchasePlaces path, with GET, it should return a 405 HTTP code (Method Not Allowed)."""
        response = client.get("/purchasePlaces")
        assert response.status_code == 405


class TestLogout:
    """Class where the logout function is tested."""

    def test_logout_path_sucess(self, client):
        """
        Test the logout path with redirect,
        with GET,
        it should return a 200 HTTP code (OK), the response should redirect to the index.
        """
        with client:
            response = client.get("/logout", follow_redirects=True)
            assert response.request.path == "/"
            assert response.status_code == 200

    def test_post_logout_should_fail(self, client):
        """Test the logout path, with POST, it should return a 405 HTTP code (Method Not Allowed)."""
        with client:
            response = client.post("/logout", follow_redirects=True)
            assert response.status_code == 405

    def test_logout_redirect_success(self, client):
        """
        Test the logout path,
        with GET,
        it should return a 302 HTTP code (Found).
        """
        response = client.get("/logout")
        assert response.status_code == 302


class TestDisplayPoints:
    """Class where the displayPoints function is tested."""

    def test_dispay_clubs_points_sucess(self, client):
        """
        Test the displayPoints path,
        with GET,
        it should return a 200 HTTP code (OK) and the response should contain some text.
        """
        response = client.get("/displayPoints")
        data = response.data.decode()
        assert response.status_code == 200
        assert "Club list" in data

    def test_post_display_clubs_points_should_fail(self, client):
        """Test the displayPopints path, with POST, it should return a 405 HTTP code (Method Not Allowed)."""
        response = client.post("/displayPoints")
        assert response.status_code == 405
