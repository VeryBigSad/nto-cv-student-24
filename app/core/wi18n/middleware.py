from typing import Optional, Dict, Any

from aiogram.types import TelegramObject
from aiogram.utils.i18n import I18nMiddleware
from aiogram.types import User
from aiogram.fsm.context import FSMContext

TYPE_CHECKER = False
if TYPE_CHECKER:
    from . import WI18N


class RedisI18nMiddleware(I18nMiddleware):
    def __init__(
        self,
        i18n: "WI18N",
        fsm_key: Optional[str] = "locale",
        i18n_key: Optional[str] = "i18n",
        middleware_key: str = "i18n_middleware",
    ) -> None:
        self.key = fsm_key
        super().__init__(i18n=i18n, i18n_key=i18n_key, middleware_key=middleware_key)

    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        fsm_context: Optional[FSMContext] = data.get("state")
        locale = None
        if fsm_context:
            fsm_data = await fsm_context.get_data()
            locale = fsm_data.get(self.key, None)
        if not locale:
            locale = await self.get_locale_from_update(event=event, data=data)
            if fsm_context:
                await fsm_context.update_data(data={self.key: locale})
        return locale

    async def get_locale_from_update(
        self, event: TelegramObject, data: Dict[str, Any]
    ) -> str:
        event_from_user: Optional[User] = data.get("event_from_user", None)
        if event_from_user is None or event_from_user.language_code is None:
            return self.i18n.default_locale
        language = event_from_user.language_code
        if await self.i18n.check_locale(language):
            return language
        return self.i18n.default_locale

    async def set_locale(self, state: FSMContext, locale: str) -> None:
        """
        Write new locale to the storage

        :param state: instance of FSMContext
        :param locale: new locale
        """
        await state.update_data(data={self.key: locale})
        self.i18n.current_locale = locale
