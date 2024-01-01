# aiohttp-raw
[![PyPI version](https://img.shields.io/pypi/v/aiohttp-raw)](https://pypi.org/project/aiohttp-raw/)
[![Downloads](https://pepy.tech/badge/aiohttp-raw)](https://pepy.tech/project/aiohttp-raw)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aiohttp-raw)  

Use [aiohttp](https://docs.aiohttp.org/en/stable/) to send HTTP raw sockets (To Test RFC Compliance)

![Logo](https://raw.githubusercontent.com/realgam3/aiohttp-raw/main/assets/img/aiohttp-raw-logo.png)

## Usage
```python
import asyncio
import aiohttp_raw


async def main():
    req = b"GET /get HTTP/1.1\r\nHost: httpbin.org\r\n\r\n"
    async with aiohttp_raw.ClientSession() as session:
        async with session.raw("http://httpbin.org/get", data=req) as response:
            print(await response.text())

loop = asyncio.new_event_loop()
loop.run_until_complete(main())
```

## Installation
### Prerequisites
* Python 3.8+

```shell
pip3 install aiohttp-raw
```

```shell
# speedups
pip install aiohttp[speedups]
````

```shell
# socks
pip install aiohttp[socks]
```

```shell
# speedups-socks
pip install aiohttp[speedups-socks]
```
