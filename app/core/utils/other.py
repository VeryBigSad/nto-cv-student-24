import asyncio
from typing import Any


async def await_something(coroutine: asyncio.Future | asyncio.Task) -> Any:
    return await coroutine
