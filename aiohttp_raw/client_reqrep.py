import functools

import re
from io import BytesIO
from ast import literal_eval
from urllib.parse import urlparse
from aiohttp.http import HttpVersion
from aiohttp.streams import EmptyStreamReader
from aiohttp.connector import Connection
from aiohttp.http_writer import StreamWriter
from aiohttp.client_exceptions import ClientResponseError
from aiohttp.typedefs import CIMultiDict, CIMultiDictProxy
from aiohttp.client_reqrep import ClientRequest, ClientResponse


class ClientRequestRaw(ClientRequest):
    async def send(self, conn: "Connection") -> "ClientResponse":
        if self.method != "AIOHTTP-RAW":
            return await super().send(conn)

        if self.proxy and not self.is_ssl():
            path = str(self.url)
        else:
            path = self.url.raw_path
            if self.url.raw_query_string:
                path += "?" + self.url.raw_query_string

        protocol = conn.protocol
        assert protocol is not None
        writer = StreamWriter(
            protocol,
            self.loop,
            on_chunk_sent=functools.partial(
                self._on_chunk_request_sent, self.method, self.url
            ),
            on_headers_sent=functools.partial(
                self._on_headers_request_sent, self.method, self.url
            ),
        )

        if not path.startswith("/"):
            _path = urlparse(path)
            _body = self.body._value.split(b"/", 1)
            self.body._value = b"".join([_body[0], f"{_path.scheme}://{_path.netloc}/".encode(), _body[1]])

        self._writer = self.loop.create_task(self.write_bytes(writer, conn))

        response_class = self.response_class
        assert response_class is not None
        self.response = response_class(
            self.method,
            self.original_url,
            writer=self._writer,
            continue100=self._continue,
            timer=self._timer,
            request_info=self.request_info,
            traces=self._traces,
            loop=self.loop,
            session=self._session,
        )
        return self.response


class StreamReaderRaw(EmptyStreamReader):
    def __init__(self, body):
        super().__init__()
        self._body = BytesIO(body)

    async def read(self, n: int = -1) -> bytes:
        return self._body.read(n)


class ClientResponseRaw(ClientResponse):
    async def start(self, connection: "Connection") -> "ClientResponse":
        try:
            return await super().start(connection)
        except ClientResponseError as exc:
            if exc.status != 400:
                raise exc

            res_re = re.search("Expected HTTP/:.*?(?P<res_raw>b'.*')", exc.message, flags=re.DOTALL)
            self.version = HttpVersion(0, 0)
            self.status = 0
            self.reason = "Non Standard"
            self._headers = CIMultiDictProxy(CIMultiDict())
            self._raw_headers = tuple()
            self.content = StreamReaderRaw(literal_eval(res_re.group("res_raw")))

            # print(res_re.group("res_raw"))
            # print(exc.status, exc.message)

        # """Start response processing."""
        # self._closed = False
        # self._protocol = connection.protocol
        # self._connection = connection
        #
        # with self._timer:
        #     while True:
        #         # read response
        #         try:
        #             protocol = self._protocol
        #             message, payload = await protocol.read()  # type: ignore[union-attr]
        #         except http.HttpProcessingError as exc:
        #             raise ClientResponseError(
        #                 self.request_info,
        #                 self.history,
        #                 status=exc.code,
        #                 message=exc.message,
        #                 headers=exc.headers,
        #             ) from exc
        #
        #         if message.code < 100 or message.code > 199 or message.code == 101:
        #             break
        #
        #         if self._continue is not None:
        #             set_result(self._continue, True)
        #             self._continue = None
        #
        # # payload eof handler
        # payload.on_eof(self._response_eof)
        #
        # # response status
        # self.version = message.version
        # self.status = message.code
        # self.reason = message.reason
        #
        # # headers
        # self._headers = message.headers  # type is CIMultiDictProxy
        # self._raw_headers = message.raw_headers  # type is Tuple[bytes, bytes]
        #
        # # payload
        # self.content = payload
        #
        # # cookies
        # for hdr in self.headers.getall(hdrs.SET_COOKIE, ()):
        #     try:
        #         self.cookies.load(hdr)
        #     except CookieError as exc:
        #         client_logger.warning("Can not load response cookies: %s", exc)
        # return self
