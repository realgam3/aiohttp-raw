import functools
from typing import Any
from aiohttp.typedefs import StrOrURL
from aiohttp.client import ClientSession, _RequestContextManager

from .__version__ import __title__
from .client_reqrep import ClientRequestRaw, ClientResponseRaw


class ClientSessionRaw(ClientSession):
    @functools.wraps(ClientSession.__init__)
    def __init__(self, *args, **kwargs) -> None:
        if not kwargs.get("request_class"):
            kwargs["request_class"] = ClientRequestRaw

        if not kwargs.get("response_class"):
            kwargs["response_class"] = ClientResponseRaw

        super().__init__(*args, **kwargs)

    def raw(self, url: StrOrURL, **kwargs: Any) -> "_RequestContextManager":
        return self.request(__title__, url, **kwargs)
