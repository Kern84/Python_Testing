from flask import request
from server import app


dict_correct_email = {"email": "john@simplylift.co"}
dict_wrong_email = {"email": "wrong@email.fr"}
dict_wrong_input = {"email": "1"}
correct_competition = "Spring Festival"
correct_club = "Simply Lift"


class TestIndex:
    def test_index_should_return_200(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert response.status_code != 404
        assert response.status_code != 500

    def test_index_should_be_get(self):
        with app.test_request_context("/", method="GET"):
            assert request.method == "GET"
            assert request.method != "POST"
            assert request.path == "/"


class TestShowSummary:
    def test_login_sucess(self, client, list_club_email):
        response = client.post("/showSummary", data=dict(dict_correct_email))
        data = response.data.decode()
        assert response.status_code == 200
        assert dict_correct_email["email"] in list_club_email
        assert "Welcome, {}".format(dict_correct_email["email"]) in data

    def test_login_fail(self, client):
        response = client.post("/showSummary", data=dict(dict_wrong_email))
        data = response.data.decode()
        assert response.status_code == 500  # should not crash, 200
        # assert "Sorry, that email wasn't found." in data

    def test_login_wrong_input(self, client):
        response = client.post("/showSummary", data=dict(dict_wrong_input))
        data = response.data.decode()
        assert response.status_code == 500  # should not crash, 200
        # assert "Sorry, that email wasn't found." in data

    def test_login_no_input(self, client):
        response = client.post("/showSummary", data={"email": ""})
        data = response.data.decode()
        assert response.status_code == 500  # should not crash, 200
        # assert "Sorry, that email wasn't found." in data

    def test_get_show_summary_should_fail(self, client):
        response = client.get("/showSummary")
        assert response.status_code == 405  # method should be POST


class TestBook:
    def test_book_path_success(self, client, mock_modified_competitions_date):
        response = client.get("/book/Spring%20Festival/Simply%20Lift")
        data = response.data.decode()
        assert response.status_code == 200
        assert correct_competition in data
        assert correct_club in data

    def test_book_full_wrong_path_fail(self, client):
        response = client.get("/book/WrongComp/WrongClub")
        data = response.data.decode()
        assert response.status_code == 500
        # assert "Something went wrong-please try again" in data

    def test_book_wrong_competition_path_fail(
        self, client, mock_modified_competitions_date
    ):
        response = client.get("/book/WrongComp/Simply%20Lift")
        data = response.data.decode()
        assert response.status_code == 500
        # assert "Something went wrong-please try again" in data

    def test_book_wrong_club_path_fail(self, client, mock_modified_competitions_date):
        response = client.get("/book/Spring%20Festival/WrongClub")
        data = response.data.decode()
        assert response.status_code == 500
        # assert "Something went wrong-please try again" in data

    def test_book_root_path(self, client):
        response = client.get("/book/")
        assert response.status_code == 404  # useful ?

    def test_post_book_should_fail(self, client, mock_modified_competitions_date):
        response = client.post("/book/Spring%20Festival/Simply%20Lift")
        assert response.status_code == 405  # method should be GET

    def test_book_past_competition_should_fail(self, client):
        response = client.get("/book/Fall%20Classic/Simply%20Lift")
        data = response.data.decode()
        assert response.status_code == 200  # should be 403
        # assert "MESSAGE PAST COMPETITION" in data


class TestPurchasePlaces:
    def test_purchase_places_route_fail(self, client):
        response = client.get("/purchasePlaces")
        assert response.status_code == 405  # because the method should be POST

    def test_purchase_two_places(self, client):
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": correct_competition,
                "club": correct_club,
                "places": 2,
            },
        )
        assert response.status_code == 200

    def test_purchase_not_logged_in(self, client):
        response = client.get("/purchasePlaces")
        assert response.status_code == 405  # because the method should be POST


# TODO purchase after booking 0 < x < 13 places; booking 0 places; booking -x places; booking +12 places; more points than club has;


class TestLogout:
    def test_should_redirect_sucess(self, client):
        with client:
            response = client.get("/logout", follow_redirects=True)
            assert response.request.path == "/"

    def test_logout_redirect(self, client):
        response = client.get("/logout")
        assert response.status_code == 302


# TODO display points ???
