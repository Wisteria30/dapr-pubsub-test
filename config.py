from pydantic import BaseSettings, Field


class Config(BaseSettings):
    """
    All Settings are here
    > dotenv ファイルを使用する場合でも、pydantic はdotenv ファイルだけでなく環境変数も読み取ります。
    環境変数は常に dotenv ファイルからロードされた値よりも優先されます。
    ref: https://docs.pydantic.dev/latest/usage/settings/
    """

    # app
    APP_NAME: str = "pubsub"
    HTTP_PORT: int
    GRPC_PORT: int
    DEBUG: bool = Field(env="DEBUG", default=True)
    LOG_LEVEL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
