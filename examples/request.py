#!/usr/bin/env python3

import asyncio
import aiohttp_raw


async def main():
    req = b"GET /get HTTP/1.1\r\nHost: httpbin.org\r\n\r\n"
    async with aiohttp_raw.ClientSession() as session:
        async with session.raw("http://httpbin.org/get", data=req) as response:
            print(await response.text())

loop = asyncio.new_event_loop()
loop.run_until_complete(main())
