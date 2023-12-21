from dependency_injector import containers, providers

import config


class Obj:
    def __init__(self, msg: str) -> None:
        self.msg = msg

    def __str__(self) -> str:
        return self.msg


class Container(containers.DeclarativeContainer):
    """Dependency Injection Container

    see https://github.com/ets-labs/python-dependency-injector for more details
    """

    conf = config.Config()

    __self__ = providers.Self()

    config = providers.Configuration(pydantic_settings=[conf])
    config.load()

    dummy_object = providers.Factory(Obj, msg="hello")
