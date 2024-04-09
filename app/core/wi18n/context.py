from typing import Any, Coroutine

from .core import WI18N


def gettext(*args: Any, **kwargs: Any) -> str:
    return WI18N().gettext(*args, **kwargs)


def gettext_async(*args: Any, **kwargs: Any) -> Coroutine[Any, Any, Any]:
    return WI18N().gettext_async(*args, **kwargs)
