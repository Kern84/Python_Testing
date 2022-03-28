import pytest
from server import app
from flask import request


@pytest.fixture
def client():
    client = app.test_client()
    yield client


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


class TestLoginEmail:
    correct_email = {"email": "john@simplylift.co"}
    wrong_email = {"email": "wrong@email.fr"}
    wrong_input = {"email": "1"}

    def test_login_secretary_sucess(self, client):
        response = client.post("/showSummary", data=dict(self.correct_email))
        assert response.status_code == 200

    def test_login_secretary_fail(self, client):
        response = client.post("/showSummary", data=dict(self.wrong_email))
        assert response.status_code == 500

    def test_login_secretary_wrong_input(self, client):
        response = client.post("/showSummary", data=dict(self.wrong_input))
        assert response.status_code == 500


class TestNotLoggedIn:
    def test_show_summary_not_logged_in(self, client):
        response = client.get("/showSummary")
        assert response.status_code == 405

    def test_book_not_logged_in(self, client):
        response = client.get("/book/")
        assert response.status_code == 404

    def test_book_full_route_not_logged_in(self, client):
        response = client.get("/book/Spring%20Festival/Simply%20Lift")
        assert response.status_code == 200  # should not be possible

    def test_purchase_not_logged_in(self, client):
        response = client.get("/purchasePlaces")
        assert response.status_code == 405

    def test_logout_not_logged_in(self, client):
        response = client.get("/logout")
        assert response.status_code == 302  # because redirect to index
