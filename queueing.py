import asyncio
import random
import time

item_counter = 0


async def make_sleep_item():
    global item_counter  # just for the sake of clarity of the `print`-ed logs
    sleep_for = random.randint(0, 5)
    await asyncio.sleep(sleep_for)
    print(f"item {item_counter}, slept for {sleep_for} s")
    item_counter += 1
    return (item_counter, sleep_for)


async def produce(name: int, q: asyncio.Queue) -> None:
    counter, sleep_for = await make_sleep_item()  # can take up to 5 seconds
    t = time.perf_counter()
    await q.put((t, item_counter, sleep_for))
    print(f"{t:0.2f}: Producer {name} produced item <{item_counter}, {sleep_for}> and put in the queue. "
          f"Queue size: {q.qsize()}")


async def consume(name: int, q: asyncio.Queue) -> None:
    while True:
        t, item_counter, sleep_for = await q.get()
        await asyncio.sleep(sleep_for)  # pretend to do something with the consumed item
        elapsed = time.perf_counter() - t
        print(f"{time.perf_counter():0.2f}: Consumer {name} consumed the item <{item_counter}, {sleep_for}> "
              f"added to queue {elapsed:0.2f} s ago. Queue size: {q.qsize()}.")
        q.task_done()


async def main(nprod: int, ncon: int):
    q = asyncio.Queue()
    # q = asyncio.Queue(maxsize=3)  # can also set the max number of items in the queue

    producers = [asyncio.create_task(produce(n, q)) for n in range(nprod)]
    consumers = [asyncio.create_task(consume(n, q)) for n in range(ncon)]

    await asyncio.gather(*producers)
    await q.join()  # no need to gather consumers

    for c in consumers:
        c.cancel()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--nprod", type=int, default=10)
    parser.add_argument("-c", "--ncon", type=int, default=3)
    ns = parser.parse_args()

    main_start = time.perf_counter()
    asyncio.run(main(**ns.__dict__))
    elapsed = time.perf_counter() - main_start
    print(f"Program completed in {elapsed:0.5f} seconds.")
