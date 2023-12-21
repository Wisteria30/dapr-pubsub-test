import json

from time import sleep

from cloudevents.sdk.event import v1
from dapr.clients.grpc._response import TopicEventResponse
from dapr.ext.grpc import App
from dapr.proto import appcallback_v1
from dependency_injector.wiring import Provide, inject

import container

should_retry = True  # To control whether dapr should retry sending a message


@inject
def mytopic(
    event: v1.Event,
    dummy_object: container.Container = Provide[container.Container.dummy_object],
) -> TopicEventResponse:
    global should_retry
    print(f"{dummy_object=}")
    data = json.loads(event.Data())
    print(
        f'Subscriber received: id={data["id"]}, message="{data["message"]}", '
        f'content_type="{event.content_type}"',
        flush=True,
    )
    # event.Metadata() contains a dictionary of cloud event extensions and publish metadata
    if should_retry:
        should_retry = False  # we only retry once in this example
        sleep(0.5)  # add some delay to help with ordering of expected logs
        return TopicEventResponse("retry")
    return TopicEventResponse("success")
