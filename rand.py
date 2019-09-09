import asyncio
import random

# ANSI colors
colors = (
    "\033[36m",  # Cyan
    "\033[91m",  # Red
    "\033[35m",  # Magenta
    "\033[0m",   # End of color
)

async def make_random(idx: int, threshold: int) -> int:
    print(colors[idx] + f"Initiated make_random({idx}).")
    j = random.randint(0, 10)
    while j <= threshold:
        print(colors[idx] + f"make_random({idx}) == {j} too low; retrying...")
        await asyncio.sleep(idx + 1)
        j = random.randint(0, 10)
    print(colors[idx] + f"--> Finished: make_random({idx}) => {j}" + colors[3])
    return j

async def main():
    res = await asyncio.gather(*(make_random(idx, 10 - idx - 2) for idx in range(3)))
    return res

if __name__ == '__main__':
    random.seed(444)
    r1, r2, r3 = asyncio.run(main())
    print(f"\nr1: {r1}, r2: {r2}, r3: {r3}")
