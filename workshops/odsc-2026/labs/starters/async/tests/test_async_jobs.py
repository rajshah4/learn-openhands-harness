import asyncio
import time

from toyapp.async_jobs import run_batch


async def _run_batch_with_elapsed(size: int) -> tuple[int, float]:
    started = time.perf_counter()
    result = await run_batch(size)
    return result, time.perf_counter() - started


def test_run_batch_counts_every_increment() -> None:
    assert asyncio.run(run_batch(50)) == 50


def test_run_batch_keeps_work_concurrent() -> None:
    result, elapsed = asyncio.run(_run_batch_with_elapsed(30))
    assert result == 30
    assert elapsed < 0.08
