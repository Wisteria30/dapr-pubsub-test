import time

from dapr.clients import DaprClient
from pydantic import BaseSettings

# import requests


class Message(BaseSettings):
    id: int
    message: str


# time.sleep(7)

with DaprClient() as d:
    id = 0
    while id < 3:
        id += 1
        # req_data = {"id": id, "message": "hello world"}
        req_data = Message(id=id, message="hello world")

        # Create a typed message with content type and body
        resp = d.publish_event(
            pubsub_name="pubsub",
            topic_name="a_hoge",
            data=req_data.json(),
            data_content_type="application/json",
        )

        # Print the request
        print(req_data, flush=True)

        time.sleep(1)

    # we can publish events to different topics but handle them with the same method
    # by disabling topic validation in the subscriber

    id = 3
    while id < 6:
        id += 1
        # req_data = {"id": id, "message": "hello world"}
        req_data = Message(id=id, message="hello world")
        resp = d.publish_event(
            pubsub_name="pubsub",
            topic_name=f"fuga/{id}",
            data=req_data.json(),
            data_content_type="application/json",
        )

        # Print the request
        print(req_data, flush=True)

        time.sleep(0.5)

    # This topic will fail - initiate a retry which gets routed to the dead letter topic
    req_data.id = 7
    resp = d.publish_event(
        pubsub_name="pubsub",
        topic_name="d_alive",
        data=req_data.json(),
        data_content_type="application/json",
        publish_metadata={"custommeta": "somevalue"},
    )

    # Print the request
    print(req_data, flush=True)

# health check
# resp = requests.get("http://localhost:8081/health")
# print(resp.json(), flush=True)
