from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def my_task(self):
        # Simulate normal requests to the root endpoint
        self.client.get("/")

    @task
    def health_check(self):
        # Simulate a health check request to the /health endpoint
        self.client.get("/health")
