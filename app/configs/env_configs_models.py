from typing import Optional

from pydantic import BaseModel


class BaseConfigsModel(BaseModel):
    PROD_MODE: Optional[bool] = True


class TelegramConfigsModel(BaseModel):
    TELEGRAM_BOT_TOKEN: str


class DataBaseConfigsModel(BaseModel):
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str


class RedisBaseConfigsModel(BaseModel):
    REDIS_DB_HOST: str
    REDIS_DB_PORT: int
    REDIS_DB_DATABASE: str


class EnvConfigsModel(
    BaseConfigsModel,
    TelegramConfigsModel,
    DataBaseConfigsModel,
    RedisBaseConfigsModel,
):
    pass
