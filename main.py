import aiohttp_raw
import asyncio


async def main():
    req = b"GET /get HTTP/1.1\r\nHost: httpbin.org\r\n\r\n"
    proxy = "http://192.168.1.214:8080"
    connector = aiohttp_raw.TCPConnector(ssl=False)

    # req = b"GET /get\r\n\r\n"
    # proxy = None
    # connector = aiohttp.TCPConnector(ssl=False)

    # from aiohttp_socks import ProxyConnector
    # proxy = None
    # connector = ProxyConnector.from_url("socks5://127.0.0.1:9050")

    # from aiosocks.connector import ProxyConnector, ProxyClientRequest
    # proxy = "socks5://127.0.0.1:9050"
    # connector = ProxyConnector(remote_resolve=True)

    async with aiohttp_raw.ClientSession(connector=connector) as session:
        async with session.request("AIOHTTP-RAW", "http://httpbin.org/get", data=req, proxy=proxy) as response:
            print(await response.text())

loop = asyncio.new_event_loop()
loop.run_until_complete(main())
