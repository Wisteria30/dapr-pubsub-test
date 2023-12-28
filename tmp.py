import uvicorn

from dapr.ext.fastapi import DaprApp
from fastapi import Body, FastAPI
from pydantic import BaseModel


class RawEventModel(BaseModel):
    body: str


class User(BaseModel):
    id: int
    name = "Jane Doe"


class CloudEventModel(BaseModel):
    data: User
    datacontenttype: str
    id: str
    pubsubname: str
    source: str
    specversion: str
    topic: str
    traceid: str
    traceparent: str
    tracestate: str
    type: str


app = FastAPI()
dapr_app = DaprApp(app)


# Allow handling event with any structure (Easiest, but least robust)
# dapr publish --publish-app-id sample --topic any_topic --pubsub pubsub --data '{"id":"7", "desc": "good", "size":"small"}'
@dapr_app.subscribe(pubsub="pubsub", topic="any_topic")
def any_event_handler(event_data=Body()):
    print(event_data)


# For robustness choose one of the below based on if publisher is using CloudEvents


# Handle events sent with CloudEvents
# dapr publish --publish-app-id sample --topic cloud_topic --pubsub pubsub --data '{"id":"7", "name":"Bob Jones"}'
@dapr_app.subscribe(pubsub="pubsub", topic="cloud_topic")
def cloud_event_handler(event_data: CloudEventModel):
    print(event_data)


# Handle raw events sent without CloudEvents
# curl -X "POST" http://localhost:3500/v1.0/publish/pubsub/raw_topic?metadata.rawPayload=true -H "Content-Type: application/json" -d '{"body": "345"}'
@dapr_app.subscribe(pubsub="pubsub", topic="raw_topic")
def raw_event_handler(event_data: RawEventModel):
    print(event_data)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=30212)
