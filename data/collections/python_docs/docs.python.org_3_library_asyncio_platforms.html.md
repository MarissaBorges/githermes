Platform Support
================

The [`asyncio`](asyncio.html#module-asyncio "asyncio: Asynchronous I/O.") module is designed to be portable,
but some platforms have subtle differences and limitations
due to the platforms’ underlying architecture and capabilities.

macOS
-----

Modern macOS versions are fully supported.

macOS <= 10.8

On macOS 10.6, 10.7 and 10.8, the default event loop
uses [`selectors.KqueueSelector`](selectors.html#selectors.KqueueSelector "selectors.KqueueSelector"), which does not support
character devices on these versions. The [`SelectorEventLoop`](asyncio-eventloop.html#asyncio.SelectorEventLoop "asyncio.SelectorEventLoop")
can be manually configured to use [`SelectSelector`](selectors.html#selectors.SelectSelector "selectors.SelectSelector")
or [`PollSelector`](selectors.html#selectors.PollSelector "selectors.PollSelector") to support character devices on
these older versions of macOS. Example:

Copy

```
import asyncio
import selectors

selector = selectors.SelectSelector()
loop = asyncio.SelectorEventLoop(selector)
asyncio.set_event_loop(loop)

```