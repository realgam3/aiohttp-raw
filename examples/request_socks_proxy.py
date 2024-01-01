#!/usr/bin/env python3

import asyncio
import aiohttp_raw
import aiohttp_socks


async def main():
    connector = aiohttp_socks.ProxyConnector.from_url("socks5://127.0.0.1:9050")
    req = b"GET /get HTTP/1.1\r\nHost: httpbin.org\r\n\r\n"
    async with aiohttp_raw.ClientSession(connector=connector) as session:
        async with session.raw("http://httpbin.org/get", data=req) as response:
            print(await response.text())

loop = asyncio.new_event_loop()
loop.run_until_complete(main())
