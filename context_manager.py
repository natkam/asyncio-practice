from __future__ import annotations

import asyncio
import typing

import aiohttp


GET_URL = "http://httpbin.org/get"
POST_URL = "http://httpbin.org/post"


class SomeApiException(Exception):
    pass


class SomeApiManager:
    def __init__(self, headers: typing.Optional[dict] = None):
        self.session = aiohttp.ClientSession(headers=headers)

    async def __aenter__(self) -> SomeApiManager:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def request(
        self,
        method: str,
        url: str,
        params: typing.Optional[dict] = None,
        payload: typing.Optional[dict] = None,
        **kwargs,
    ):
        async with self.session.request(
            method=method, url=url, params=params, json=payload, **kwargs
        ) as resp:
            if resp.reason.upper() != "OK":
                raise SomeApiException(resp.status, resp.reason)
            return await resp.json()

    async def get_page(self, params: typing.Optional[dict] = None, **kwargs):
        return await self.request("GET", GET_URL, params=params, **kwargs)

    async def post_something(self, payload: typing.Optional[dict] = None, **kwargs):
        return await self.request("POST", POST_URL, payload=payload, **kwargs)

    async def get_status_code(self, code: str):
        return await self.request("GET", f"http://httpbin.org/status/{code}")


async def api_call():
    async with SomeApiManager() as api:
        get_resp = await api.get_page(params={"key1": "val1", "key2": 314})
        print(get_resp)
        print("======")

        post_resp = await api.post_something(payload={"data": "asdf", "number": 42})
        print(post_resp)
        print("======")

        try:
            status_resp = await api.get_status_code("401")
            # ^ this will raise
        except SomeApiException as err:
            print("API ERROR!", err)


if __name__ == "__main__":
    asyncio.run(api_call())
