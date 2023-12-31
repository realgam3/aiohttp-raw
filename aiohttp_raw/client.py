import functools
from .client_reqrep import ClientRequestRaw, ClientResponseRaw
from aiohttp.client import ClientSession


class ClientSessionRaw(ClientSession):
    @functools.wraps(ClientSession.__init__)
    def __init__(self, *args, **kwargs) -> None:
        if not kwargs.get("request_class"):
            kwargs["request_class"] = ClientRequestRaw

        if not kwargs.get("response_class"):
            kwargs["response_class"] = ClientResponseRaw

        super().__init__(*args, **kwargs)
