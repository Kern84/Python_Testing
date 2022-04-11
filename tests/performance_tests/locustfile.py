from locust import HttpUser, task


class PerformanceTest(HttpUser):
    """Class to test all application paths with Locust."""

    @task
    def index(self):
        self.client.get("")

    @task
    def showSummary(self):
        self.client.post("showSummary", {"email": "john@simplylift.co"})

    @task
    def book(self):
        self.client.get("book/Spring%20Festival/Simply%20Lift")

    @task
    def purchasePlaces(self):
        self.client.post(
            "purchasePlaces",
            {
                "competition": "Spring Festival",
                "club": "Simply Lift",
                "places": 2,
            },
        )

    @task
    def logout(self):
        self.client.get("logout")

    @task
    def displayPoints(self):
        self.client.get("displayPoints")
