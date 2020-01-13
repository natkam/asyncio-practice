"""
Example from https://realpython.com/python-concurrency/
"""

import asyncio
import time

import aiohttp


async def download_site(url, session):
    async with session.get(url) as resp:
        # print(f"Read {resp.content} from {url}")
        pass


async def download_all_sites(sites):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in sites:
            task = asyncio.ensure_future(download_site(url, session))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    sites = ["https://www.jython.org", "http://olympus.realpython.org/dice"] * 80
    start = time.perf_counter()
    asyncio.run(download_all_sites(sites))
    duration = time.perf_counter() - start
    print(f"Downloaded {len(sites)} in {duration} seconds")
