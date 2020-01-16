"""
Example from https://realpython.com/python-concurrency/
"""

import threading
import time
from concurrent.futures import ThreadPoolExecutor

import requests

thread_local = threading.local()


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def download_site(url):
    session = get_session()
    with session.get(url) as resp:
        print(f"Read {len(resp.content)} from {url}")


def download_all_sites(sites):
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(download_site, sites)


if __name__ == "__main__":
    sites = ["https://www.jython.org", "http://olympus.realpython.org/dice"] * 80
    start = time.perf_counter()
    download_all_sites(sites)
    duration = time.perf_counter() - start
    print(f"Downloaded {len(sites)} in {duration} seconds")
