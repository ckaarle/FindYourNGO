import time
from locust import task, between
from locust.contrib.fasthttp import FastHttpUser


class NgoUser(FastHttpUser):
    wait_time = between(0, 0)

    @task
    def hello_world(self):
        self.client.get("/ngoOverviewItems")

    def on_start(self):
        pass
        #self.client.post("/login", json={"username":"a", "password":"a"})
