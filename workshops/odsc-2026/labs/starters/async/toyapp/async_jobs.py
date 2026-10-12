from __future__ import annotations

import asyncio

WORK_DELAY_SECONDS = 0.005


class AsyncCounter:
    def __init__(self) -> None:
        self.value = 0

    async def increment(self) -> None:
        await asyncio.sleep(WORK_DELAY_SECONDS)
        current = self.value
        await asyncio.sleep(0)
        self.value = current + 1


async def run_batch(size: int) -> int:
    counter = AsyncCounter()
    await asyncio.gather(*(counter.increment() for _ in range(size)))
    return counter.value


def run_batch_sync(size: int) -> int:
    return asyncio.run(run_batch(size))
