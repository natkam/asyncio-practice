import asyncio
import time

async def count():
    print("one")
    await asyncio.sleep(1)
    print("two")


async def main():
    await asyncio.gather(count(), count(), count())


if __name__ == "__main__":
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")


async def f(x):
    y = await z(x)  # coroutine
    return y

async def g(x):
    yield x  # async generator
