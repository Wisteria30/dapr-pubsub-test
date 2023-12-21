# ------------------------------------------------------------
# Copyright 2022 The Dapr Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------

import json

from time import sleep

from cloudevents.sdk.event import v1
from dapr.clients.grpc._response import TopicEventResponse
from dapr.ext.grpc import App
from dapr.proto import appcallback_v1

import container
import topic

should_retry = True  # To control whether dapr should retry sending a message


# def mytopic(event: v1.Event) -> TopicEventResponse:
#     global should_retry
#     data = json.loads(event.Data())
#     print(
#         f'Subscriber received: id={data["id"]}, message="{data["message"]}", '
#         f'content_type="{event.content_type}"',
#         flush=True,
#     )
#     # event.Metadata() contains a dictionary of cloud event extensions and publish metadata
#     if should_retry:
#         should_retry = False  # we only retry once in this example
#         sleep(0.5)  # add some delay to help with ordering of expected logs
#         return TopicEventResponse("retry")
#     return TopicEventResponse("success")


# @app.subscribe(pubsub_name="pubsub", topic="TOPIC_D", dead_letter_topic="TOPIC_D_DEAD")
def fail_and_send_to_dead_topic(event: v1.Event) -> TopicEventResponse:
    return TopicEventResponse("retry")


# @app.subscribe(pubsub_name="pubsub", topic="TOPIC_D_DEAD")
def mytopic_dead(event: v1.Event) -> TopicEventResponse:
    data = json.loads(event.Data())
    print(
        f'Dead-Letter Subscriber received: id={data["id"]}, message="{data["message"]}", '
        f'content_type="{event.content_type}"',
        flush=True,
    )
    print("Dead-Letter Subscriber. Received via deadletter topic: " + event.Subject(), flush=True)
    print(
        "Dead-Letter Subscriber. Originally intended topic: " + event.Extensions()["topic"],
        flush=True,
    )
    return TopicEventResponse("success")


# this allows subscribing to all events sent to this app - useful for wildcard topics
# @app.subscribe(pubsub_name="pubsub", topic="topic/#", disable_topic_validation=True)
def mytopic_wildcard(event: v1.Event) -> TopicEventResponse:
    data = json.loads(event.Data())
    print(
        f'Wildcard-Subscriber received: id={data["id"]}, message="{data["message"]}", '
        f'content_type="{event.content_type}"',
        flush=True,
    )
    return TopicEventResponse("success")


def serve():
    di_modules = [topic]
    ctr = container.Container()
    ctr.wire(modules=di_modules)
    app = App()

    app.subscribe(pubsub_name="pubsub", topic="TOPIC_A")(topic.mytopic)
    app.subscribe(pubsub_name="pubsub", topic="TOPIC_D", dead_letter_topic="TOPIC_D_DEAD")(
        fail_and_send_to_dead_topic
    )
    app.subscribe(pubsub_name="pubsub", topic="TOPIC_D_DEAD")(mytopic_dead)

    # for id in range(4, 7):
    #     app._servicer._registered_topics.append(
    #         appcallback_v1.TopicSubscription(pubsub_name="pubsub", topic=f"topic/{id}")
    #     )
    # app.subscribe(pubsub_name="pubsub", topic="topic/#", disable_topic_validation=True)(
    #     mytopic_wildcard
    # )

    app.run(50051)
