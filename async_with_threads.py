"""
Example from https://pymotw.com/3/asyncio/executors.html
"""

import asyncio
import concurrent.futures
import logging
import sys
import time


def block(n):
    log = logging.getLogger(f"blocks({n})")
    log.info("[BLOCK] running")
    time.sleep(1)
    log.info("[BLOCK] done")
    return n ** 2


async def run_blocking_tasks(executor):
    log = logging.getLogger("run_blocking_tasks")
    log.info("[RUN] starting: creating executor tasks")
    loop = asyncio.get_event_loop()
    blocking_tasks = [loop.run_in_executor(executor, block, i) for i in range(6)]
    log.info("[RUN] waiting for executor tasks")
    completed, pending = await asyncio.wait(blocking_tasks)
    results = [t.result() for t in completed]
    log.info(f"[RUN] results: {results}")
    log.info("[RUN] exiting")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(threadName)10s %(name)18s: %(message)s",
        stream=sys.stderr,
    )

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(
            run_blocking_tasks(executor)
        )
    finally:
        event_loop.close()


