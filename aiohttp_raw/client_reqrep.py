import functools


from urllib.parse import urlparse
from aiohttp.connector import Connection
from aiohttp.http_writer import StreamWriter
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


class ClientResponseRaw(ClientResponse):
    pass
