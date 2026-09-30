from locust import HttpUser, task, between


class GUDLFTUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def home_page(self):
        self.client.get("/")

    @task
    def points_board(self):
        self.client.get("/points")

    @task
    def purchase_places(self):
        self.client.post(
            "/purchasePlaces",
            data={
                "competition": "Future event",
                "club": "Iron Temple",
                "places": "1"
            }
        )