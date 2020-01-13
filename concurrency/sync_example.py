"""
Example from https://realpython.com/python-concurrency/
"""

import requests
import time


def download_site(url, session):
    with session.get(url) as response:
        # print(f"Read {len(response.content)} from {url}")
        pass


def download_all_sites(sites):
    with requests.Session() as session:
        for url in sites:
            download_site(url, session)


if __name__ == "__main__":
    sites = ["https://www.jython.org", "http://olympus.realpython.org/dice"] * 80
    start = time.perf_counter()
    download_all_sites(sites)
    duration = time.perf_counter() - start
    print(f"Downloaded {len(sites)} in {duration} seconds")
