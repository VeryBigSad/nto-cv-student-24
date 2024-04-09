from contextlib import contextmanager
from contextvars import ContextVar
from typing import Optional, Union

from redis.asyncio import Redis as AsyncRedis
from redis import Redis as SyncRedis


class WI18NMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super(WI18NMeta, cls).__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class WI18N(metaclass=WI18NMeta):
    def __init__(
        self,
        redis: Union[SyncRedis, AsyncRedis],
        default_locale: str = "EN",
        domain: str = "messages",
        langs_domain: str = "langs",
        ab_default: str = "ab_default",
    ):
        self.redis = redis
        self.domain = domain
        self.default_locale = default_locale
        self.langs_domain = langs_domain
        self.ab_default = ab_default
        self.ctx_locale = ContextVar("wanna_ctx_locale", default=default_locale)

    @property
    def current_locale(self) -> str:
        return self.ctx_locale.get()

    @current_locale.setter
    def current_locale(self, value: str) -> None:
        self.ctx_locale.set(value)

    @contextmanager
    def use_locale(self, locale: str):
        ctx_token = self.ctx_locale.set(locale)
        try:
            yield
        finally:
            self.ctx_locale.reset(ctx_token)

    @contextmanager
    def context(self):
        yield self

    def get_request(self, locale: str, singular: str) -> str:
        return f"{self.domain}:{locale}:{self.ab_default}:{singular}"

    def gettext(self, singular: str, locale: Optional[str] = None):
        if locale is None:
            locale = self.current_locale
        value: Optional[bytes] = self.redis.get(self.get_request(locale, singular))
        if value is not None:
            return value.decode()
        return singular

    async def gettext_async(self, singular: str, locale: Optional[str] = None):
        if locale is None:
            locale = self.current_locale
        value = await self.redis.get(self.get_request(locale, singular))
        value: Optional[bytes]
        if value is not None:
            return value.decode()
        return singular

    async def check_locale(self, locale: str):
        return await self.redis.sismember(f"{self.langs_domain}", locale)

    def lazy_gettext(self, singular: str, locale: Optional[str] = None):
        pass
