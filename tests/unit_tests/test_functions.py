from server import app, clubs
import pytest


@pytest.fixture
def client():
    client = app.test_client()
    yield client


@pytest.fixture
def list_club_email():
    list_club_email = []
    for club in clubs:
        list_club_email.append(club["email"])
    return list_club_email


class TestShowSummary:
    correct_email = "john@simplylift.co"
    wrong_email = "wrong@email.com"

    def test_should_verify_email_with_success(self, list_club_email):
        assert self.correct_email in list_club_email

    def test_should_verify_email_fail(self, list_club_email):
        assert self.wrong_email not in list_club_email


class TestBook:
    correct_competition = "Spring Festival"
    correct_club = "Simply Lift"

    def test_book_path_success(self, client):
        response = client.get("/book/Spring%20Festival/Simply%20Lift")
        assert response.status_code == 200
        assert b"<h2>Spring Festival</h2>" in response.data

    def test_book_path_fail(self, client):
        response = client.get("/book/wrong/path")
        assert response.status_code == 500  # IndexError

    def test_book_path(self, client):
        response = client.get(
            "/book/{}/{}".format(self.correct_competition, self.correct_club)
        )
        assert response.status_code == 200
        assert "<h2>{}</h2>".format(self.correct_competition)


class TestPurchasePlaces:
    def test_purchase_places_route_fail(self, client):
        response = client.get("/purchasePlaces")
        assert response.status_code == 405
