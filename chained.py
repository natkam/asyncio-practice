import asyncio
import random
import time


async def get_first_number(i: int) -> int:
    # Let's say it has to retrieve the first number from somewhere, and it takes time.
    print(f"get_first_number({i}): sleeping for {i} seconds")
    await asyncio.sleep(i)
    result = random.randint(10, 20)
    print(f"get_first_number({i}): retrieved the number {result}.")
    return result


async def get_second_number(i: int, num_1: int) -> int:
    # Now this calculates something very complicated based on the first number, and it takes even more time.
    print(f"get_second_number({i}): sleeping for {2 * i} more sec")
    await asyncio.sleep(2 * i)
    result = num_1 ** 2
    print(f"get_second_number({i}): from {num_1} obtained the number {result}.")
    return result


async def calculate_sum(i: int) -> None:
    # This just puts both the results together.
    start = time.perf_counter()
    num_1 = await get_first_number(i)
    num_2 = await get_second_number(i, num_1)
    result = num_1 + num_2
    end = time.perf_counter() - start
    print(f"--> ({i}) Calculated the final result {result} from {num_1} and {num_2}; it took {end:0.2f} s.")


async def main(*args):
    await asyncio.gather(*(calculate_sum(i) for i in args))


if __name__ == '__main__':
    random.seed(444)
    waiting_times = [2, 5, 10]
    asyncio.run(main(*waiting_times))
    print("\nProgram finished")
