Low-level API Index
===================

This page lists all low-level asyncio APIs.

Obtaining the Event Loop
------------------------

Examples

Event Loop Methods
------------------

See also the main documentation section about the
[Event Loop Methods](asyncio-eventloop.html#asyncio-event-loop-methods).

Lifecycle

Debugging

Scheduling Callbacks

Thread/Process Pool

Tasks and Futures

DNS

Networking and IPC

Sockets

Unix Signals

Subprocesses

Error Handling

Examples

Transports
----------

All transports implement the following methods:

Transports that can receive data (TCP and Unix connections,
pipes, etc). Returned from methods like
[`loop.create_connection()`](asyncio-eventloop.html#asyncio.loop.create_connection "asyncio.loop.create_connection"), [`loop.create_unix_connection()`](asyncio-eventloop.html#asyncio.loop.create_unix_connection "asyncio.loop.create_unix_connection"),
[`loop.connect_read_pipe()`](asyncio-eventloop.html#asyncio.loop.connect_read_pipe "asyncio.loop.connect_read_pipe"), etc:

Read Transports

Transports that can Send data (TCP and Unix connections,
pipes, etc). Returned from methods like
[`loop.create_connection()`](asyncio-eventloop.html#asyncio.loop.create_connection "asyncio.loop.create_connection"), [`loop.create_unix_connection()`](asyncio-eventloop.html#asyncio.loop.create_unix_connection "asyncio.loop.create_unix_connection"),
[`loop.connect_write_pipe()`](asyncio-eventloop.html#asyncio.loop.connect_write_pipe "asyncio.loop.connect_write_pipe"), etc:

Write Transports

Transports returned by [`loop.create_datagram_endpoint()`](asyncio-eventloop.html#asyncio.loop.create_datagram_endpoint "asyncio.loop.create_datagram_endpoint"):

Datagram Transports

Low-level transport abstraction over subprocesses.
Returned by [`loop.subprocess_exec()`](asyncio-eventloop.html#asyncio.loop.subprocess_exec "asyncio.loop.subprocess_exec") and
[`loop.subprocess_shell()`](asyncio-eventloop.html#asyncio.loop.subprocess_shell "asyncio.loop.subprocess_shell"):

Subprocess Transports

Protocols
---------

Protocol classes can implement the following **callback methods**:

Streaming Protocols (TCP, Unix Sockets, Pipes)

Buffered Streaming Protocols

Datagram Protocols

Subprocess Protocols