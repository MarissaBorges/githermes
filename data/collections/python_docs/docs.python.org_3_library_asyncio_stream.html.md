Streams
=======

**Source code:** [Lib/asyncio/streams.py](https://github.com/python/cpython/tree/3.13/Lib/asyncio/streams.py)

---

Streams are high-level async/await-ready primitives to work with
network connections. Streams allow sending and receiving data without
using callbacks or low-level protocols and transports.

Here is an example of a TCP echo client written using asyncio
streams:

Copy

```
import asyncio

async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888)

    print(f'Send: {message!r}')
    writer.write(message.encode())
    await writer.drain()

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    print('Close the connection')
    writer.close()
    await writer.wait_closed()

asyncio.run(tcp_echo_client('Hello World!'))

```

See also the [Examples](#examples) section below.

Stream Functions

The following top-level asyncio functions can be used to create
and work with streams:

*async* asyncio.open\_connection(*host=None*, *port=None*, *\**, *limit=None*, *ssl=None*, *family=0*, *proto=0*, *flags=0*, *sock=None*, *local\_addr=None*, *server\_hostname=None*, *ssl\_handshake\_timeout=None*, *ssl\_shutdown\_timeout=None*, *happy\_eyeballs\_delay=None*, *interleave=None*)
:   Establish a network connection and return a pair of
    `(reader, writer)` objects.

    The returned *reader* and *writer* objects are instances of
    [`StreamReader`](#asyncio.StreamReader "asyncio.StreamReader") and [`StreamWriter`](#asyncio.StreamWriter "asyncio.StreamWriter") classes.

    *limit* determines the buffer size limit used by the
    returned [`StreamReader`](#asyncio.StreamReader "asyncio.StreamReader") instance. By default the *limit*
    is set to 64 KiB.

    The rest of the arguments are passed directly to
    [`loop.create_connection()`](asyncio-eventloop.html#asyncio.loop.create_connection "asyncio.loop.create_connection").

    Note

    The *sock* argument transfers ownership of the socket to the
    [`StreamWriter`](#asyncio.StreamWriter "asyncio.StreamWriter") created. To close the socket, call its
    [`close()`](#asyncio.StreamWriter.close "asyncio.StreamWriter.close") method.

    Changed in version 3.7: Added the *ssl\_handshake\_timeout* parameter.

    Changed in version 3.8: Added the *happy\_eyeballs\_delay* and *interleave* parameters.

    Changed in version 3.10: Removed the *loop* parameter.

    Changed in version 3.11: Added the *ssl\_shutdown\_timeout* parameter.

*async* asyncio.start\_server(*client\_connected\_cb*, *host=None*, *port=None*, *\**, *limit=None*, *family=socket.AF\_UNSPEC*, *flags=socket.AI\_PASSIVE*, *sock=None*, *backlog=100*, *ssl=None*, *reuse\_address=None*, *reuse\_port=None*, *keep\_alive=None*, *ssl\_handshake\_timeout=None*, *ssl\_shutdown\_timeout=None*, *start\_serving=True*)
:   Start a socket server.

    The *client\_connected\_cb* callback is called whenever a new client
    connection is established. It receives a `(reader, writer)` pair
    as two arguments, instances of the [`StreamReader`](#asyncio.StreamReader "asyncio.StreamReader") and
    [`StreamWriter`](#asyncio.StreamWriter "asyncio.StreamWriter") classes.

    *client\_connected\_cb* can be a plain callable or a
    [coroutine function](asyncio-task.html#coroutine); if it is a coroutine function,
    it will be automatically scheduled as a [`Task`](asyncio-task.html#asyncio.Task "asyncio.Task").

    *limit* determines the buffer size limit used by the
    returned [`StreamReader`](#asyncio.StreamReader "asyncio.StreamReader") instance. By default the *limit*
    is set to 64 KiB.

    The rest of the arguments are passed directly to
    [`loop.create_server()`](asyncio-eventloop.html#asyncio.loop.create_server "asyncio.loop.create_server").

    Note

    The *sock* argument transfers ownership of the socket to the
    server created. To close the socket, call the server’s
    [`close()`](asyncio-eventloop.html#asyncio.Server.close "asyncio.Server.close") method.

    Changed in version 3.7: Added the *ssl\_handshake\_timeout* and *start\_serving* parameters.

    Changed in version 3.10: Removed the *loop* parameter.

    Changed in version 3.11: Added the *ssl\_shutdown\_timeout* parameter.

    Changed in version 3.13: Added the *keep\_alive* parameter.

Unix Sockets

*async* asyncio.open\_unix\_connection(*path=None*, *\**, *limit=None*, *ssl=None*, *sock=None*, *server\_hostname=None*, *ssl\_handshake\_timeout=None*, *ssl\_shutdown\_timeout=None*)
:   Establish a Unix socket connection and return a pair of
    `(reader, writer)`.

    Similar to [`open_connection()`](#asyncio.open_connection "asyncio.open_connection") but operates on Unix sockets.

    See also the documentation of [`loop.create_unix_connection()`](asyncio-eventloop.html#asyncio.loop.create_unix_connection "asyncio.loop.create_unix_connection").

    Note

    The *sock* argument transfers ownership of the socket to the
    [`StreamWriter`](#asyncio.StreamWriter "asyncio.StreamWriter") created. To close the socket, call its
    [`close()`](#asyncio.StreamWriter.close "asyncio.StreamWriter.close") method.

    Changed in version 3.7: Added the *ssl\_handshake\_timeout* parameter.
    The *path* parameter can now be a [path-like object](../glossary.html#term-path-like-object)

    Changed in version 3.10: Removed the *loop* parameter.

    Changed in version 3.11: Added the *ssl\_shutdown\_timeout* parameter.

*async* asyncio.start\_unix\_server(*client\_connected\_cb*, *path=None*, *\**, *limit=None*, *sock=None*, *backlog=100*, *ssl=None*, *ssl\_handshake\_timeout=None*, *ssl\_shutdown\_timeout=None*, *start\_serving=True*, *cleanup\_socket=True*)
:   Start a Unix socket server.

    Similar to [`start_server()`](#asyncio.start_server "asyncio.start_server") but works with Unix sockets.

    If *cleanup\_socket* is true then the Unix socket will automatically
    be removed from the filesystem when the server is closed, unless the
    socket has been replaced after the server has been created.

    See also the documentation of [`loop.create_unix_server()`](asyncio-eventloop.html#asyncio.loop.create_unix_server "asyncio.loop.create_unix_server").

    Note

    The *sock* argument transfers ownership of the socket to the
    server created. To close the socket, call the server’s
    [`close()`](asyncio-eventloop.html#asyncio.Server.close "asyncio.Server.close") method.

    Changed in version 3.7: Added the *ssl\_handshake\_timeout* and *start\_serving* parameters.
    The *path* parameter can now be a [path-like object](../glossary.html#term-path-like-object).

    Changed in version 3.10: Removed the *loop* parameter.

    Changed in version 3.11: Added the *ssl\_shutdown\_timeout* parameter.

    Changed in version 3.13: Added the *cleanup\_socket* parameter.

StreamReader
------------

*class* asyncio.StreamReader
:   Represents a reader object that provides APIs to read data
    from the IO stream. As an [asynchronous iterable](../glossary.html#term-asynchronous-iterable), the
    object supports the [`async for`](../reference/compound_stmts.html#async-for) statement.

    It is not recommended to instantiate *StreamReader* objects
    directly; use [`open_connection()`](#asyncio.open_connection "asyncio.open_connection") and [`start_server()`](#asyncio.start_server "asyncio.start_server")
    instead.

    feed\_eof()
    :   Acknowledge the EOF.

    *async* read(*n=-1*)
    :   Read up to *n* bytes from the stream.

        If *n* is not provided or set to `-1`,
        read until EOF, then return all read [`bytes`](stdtypes.html#bytes "bytes").
        If EOF was received and the internal buffer is empty,
        return an empty `bytes` object.

        If *n* is `0`, return an empty `bytes` object immediately.

        If *n* is positive, return at most *n* available `bytes`
        as soon as at least 1 byte is available in the internal buffer.
        If EOF is received before any byte is read, return an empty
        `bytes` object.

    *async* readline()
    :   Read one line, where “line” is a sequence of bytes
        ending with `\n`.

        If EOF is received and `\n` was not found, the method
        returns partially read data.

        If EOF is received and the internal buffer is empty,
        return an empty `bytes` object.

    *async* readexactly(*n*)
    :   Read exactly *n* bytes.

        Raise an [`IncompleteReadError`](asyncio-exceptions.html#asyncio.IncompleteReadError "asyncio.IncompleteReadError") if EOF is reached before *n*
        can be read. Use the [`IncompleteReadError.partial`](asyncio-exceptions.html#asyncio.IncompleteReadError.partial "asyncio.IncompleteReadError.partial")
        attribute to get the partially read data.

    *async* readuntil(*separator=b'\n'*)
    :   Read data from the stream until *separator* is found.

        On success, the data and separator will be removed from the
        internal buffer (consumed). Returned data will include the
        separator at the end.

        If the amount of data read exceeds the configured stream limit, a
        [`LimitOverrunError`](asyncio-exceptions.html#asyncio.LimitOverrunError "asyncio.LimitOverrunError") exception is raised, and the data
        is left in the internal buffer and can be read again.

        If EOF is reached before the complete separator is found,
        an [`IncompleteReadError`](asyncio-exceptions.html#asyncio.IncompleteReadError "asyncio.IncompleteReadError") exception is raised, and the internal
        buffer is reset. The [`IncompleteReadError.partial`](asyncio-exceptions.html#asyncio.IncompleteReadError.partial "asyncio.IncompleteReadError.partial") attribute
        may contain a portion of the separator.

        The *separator* may also be a tuple of separators. In this
        case the return value will be the shortest possible that has any
        separator as the suffix. For the purposes of [`LimitOverrunError`](asyncio-exceptions.html#asyncio.LimitOverrunError "asyncio.LimitOverrunError"),
        the shortest possible separator is considered to be the one that
        matched.

        Changed in version 3.13: The *separator* parameter may now be a [`tuple`](stdtypes.html#tuple "tuple") of
        separators.

    at\_eof()
    :   Return `True` if the buffer is empty and [`feed_eof()`](#asyncio.StreamReader.feed_eof "asyncio.StreamReader.feed_eof")
        was called.

StreamWriter
------------

*class* asyncio.StreamWriter
:   Represents a writer object that provides APIs to write data
    to the IO stream.

    It is not recommended to instantiate *StreamWriter* objects
    directly; use [`open_connection()`](#asyncio.open_connection "asyncio.open_connection") and [`start_server()`](#asyncio.start_server "asyncio.start_server")
    instead.

    write(*data*)
    :   The method attempts to write the *data* to the underlying socket immediately.
        If that fails, the data is queued in an internal write buffer until it can be
        sent.

        The method should be used along with the `drain()` method:

        Copy

        ```
        stream.write(data)
        await stream.drain()

        ```

    writelines(*data*)
    :   The method writes a list (or any iterable) of bytes to the underlying socket
        immediately.
        If that fails, the data is queued in an internal write buffer until it can be
        sent.

        The method should be used along with the `drain()` method:

        Copy

        ```
        stream.writelines(lines)
        await stream.drain()

        ```

    close()
    :   The method closes the stream and the underlying socket.

        The method should be used, though not mandatory,
        along with the `wait_closed()` method:

        Copy

        ```
        stream.close()
        await stream.wait_closed()

        ```

    can\_write\_eof()
    :   Return `True` if the underlying transport supports
        the [`write_eof()`](#asyncio.StreamWriter.write_eof "asyncio.StreamWriter.write_eof") method, `False` otherwise.

    write\_eof()
    :   Close the write end of the stream after the buffered write
        data is flushed.

    transport
    :   Return the underlying asyncio transport.

    :   Access optional transport information; see
        [`BaseTransport.get_extra_info()`](asyncio-protocol.html#asyncio.BaseTransport.get_extra_info "asyncio.BaseTransport.get_extra_info") for details.

    *async* drain()
    :   Wait until it is appropriate to resume writing to the stream.
        Example:

        Copy

        ```
        writer.write(data)
        await writer.drain()

        ```

        This is a flow control method that interacts with the underlying
        IO write buffer. When the size of the buffer reaches
        the high watermark, *drain()* blocks until the size of the
        buffer is drained down to the low watermark and writing can
        be resumed. When there is nothing to wait for, the [`drain()`](#asyncio.StreamWriter.drain "asyncio.StreamWriter.drain")
        returns immediately.

    *async* start\_tls(*sslcontext*, *\**, *server\_hostname=None*, *ssl\_handshake\_timeout=None*, *ssl\_shutdown\_timeout=None*)
    :   Upgrade an existing stream-based connection to TLS.

        Parameters:

        * *sslcontext*: a configured instance of [`SSLContext`](ssl.html#ssl.SSLContext "ssl.SSLContext").
        * *server\_hostname*: sets or overrides the host name that the target
          server’s certificate will be matched against.
        * *ssl\_handshake\_timeout* is the time in seconds to wait for the TLS
          handshake to complete before aborting the connection. `60.0` seconds
          if `None` (default).
        * *ssl\_shutdown\_timeout* is the time in seconds to wait for the SSL shutdown
          to complete before aborting the connection. `30.0` seconds if `None`
          (default).

        Changed in version 3.12: Added the *ssl\_shutdown\_timeout* parameter.

    is\_closing()
    :   Return `True` if the stream is closed or in the process of
        being closed.

    *async* wait\_closed()
    :   Wait until the stream is closed.

        Should be called after [`close()`](#asyncio.StreamWriter.close "asyncio.StreamWriter.close") to wait until the underlying
        connection is closed, ensuring that all data has been flushed
        before e.g. exiting the program.

Examples
--------

### TCP echo client using streams

TCP echo client using the [`asyncio.open_connection()`](#asyncio.open_connection "asyncio.open_connection") function:

Copy

```
import asyncio

async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888)

    print(f'Send: {message!r}')
    writer.write(message.encode())
    await writer.drain()

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    print('Close the connection')
    writer.close()
    await writer.wait_closed()

asyncio.run(tcp_echo_client('Hello World!'))

```

### TCP echo server using streams

TCP echo server using the [`asyncio.start_server()`](#asyncio.start_server "asyncio.start_server") function:

Copy

```
import asyncio

async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    print(f"Received {message!r} from {addr!r}")

    print(f"Send: {message!r}")
    writer.write(data)
    await writer.drain()

    print("Close the connection")
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 8888)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

asyncio.run(main())

```

### Register an open socket to wait for data using streams

Coroutine waiting until a socket receives data using the
[`open_connection()`](#asyncio.open_connection "asyncio.open_connection") function:

Copy

```
import asyncio
import socket

async def wait_for_data():
    # Get a reference to the current event loop because
    # we want to access low-level APIs.
    loop = asyncio.get_running_loop()

    # Create a pair of connected sockets.
    rsock, wsock = socket.socketpair()

    # Register the open socket to wait for data.
    reader, writer = await asyncio.open_connection(sock=rsock)

    # Simulate the reception of data from the network
    loop.call_soon(wsock.send, 'abc'.encode())

    # Wait for data
    data = await reader.read(100)

    # Got data, we are done: close the socket
    print("Received:", data.decode())
    writer.close()
    await writer.wait_closed()

    # Close the second socket
    wsock.close()

asyncio.run(wait_for_data())

```