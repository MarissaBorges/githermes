Event Loop
==========

**Source code:** [Lib/asyncio/events.py](https://github.com/python/cpython/tree/3.13/Lib/asyncio/events.py),
[Lib/asyncio/base\_events.py](https://github.com/python/cpython/tree/3.13/Lib/asyncio/base_events.py)

---

Preface

The event loop is the core of every asyncio application.
Event loops run asynchronous tasks and callbacks, perform network
IO operations, and run subprocesses.

Application developers should typically use the high-level asyncio functions,
such as [`asyncio.run()`](asyncio-runner.html#asyncio.run "asyncio.run"), and should rarely need to reference the loop
object or call its methods. This section is intended mostly for authors
of lower-level code, libraries, and frameworks, who need finer control over
the event loop behavior.

Obtaining the Event Loop

The following low-level functions can be used to get, set, or create
an event loop:

asyncio.get\_running\_loop()
:   Return the running event loop in the current OS thread.

    Raise a [`RuntimeError`](exceptions.html#RuntimeError "RuntimeError") if there is no running event loop.

    This function can only be called from a coroutine or a callback.

asyncio.get\_event\_loop()
:   Get the current event loop.

    When called from a coroutine or a callback (e.g. scheduled with
    call\_soon or similar API), this function will always return the
    running event loop.

    If there is no running event loop set, the function will return
    the result of the `get_event_loop_policy().get_event_loop()` call.

    Because this function has rather complex behavior (especially
    when custom event loop policies are in use), using the
    [`get_running_loop()`](#asyncio.get_running_loop "asyncio.get_running_loop") function is preferred to [`get_event_loop()`](#asyncio.get_event_loop "asyncio.get_event_loop")
    in coroutines and callbacks.

    As noted above, consider using the higher-level [`asyncio.run()`](asyncio-runner.html#asyncio.run "asyncio.run") function,
    instead of using these lower level functions to manually create and close an
    event loop.

    Deprecated since version 3.12: Deprecation warning is emitted if there is no current event loop.
    In some future Python release this will become an error.

asyncio.set\_event\_loop(*loop*)
:   Set *loop* as the current event loop for the current OS thread.

asyncio.new\_event\_loop()
:   Create and return a new event loop object.

Note that the behaviour of [`get_event_loop()`](#asyncio.get_event_loop "asyncio.get_event_loop"), [`set_event_loop()`](#asyncio.set_event_loop "asyncio.set_event_loop"),
and [`new_event_loop()`](#asyncio.new_event_loop "asyncio.new_event_loop") functions can be altered by
[setting a custom event loop policy](asyncio-policy.html#asyncio-policies).

Contents

This documentation page contains the following sections:

Event Loop Methods
------------------

Event loops have **low-level** APIs for the following:



loop.run\_until\_complete(*future*)
:   Run until the *future* (an instance of [`Future`](asyncio-future.html#asyncio.Future "asyncio.Future")) has
    completed.

    If the argument is a [coroutine object](asyncio-task.html#coroutine) it
    is implicitly scheduled to run as a [`asyncio.Task`](asyncio-task.html#asyncio.Task "asyncio.Task").

    Return the Future’s result or raise its exception.

loop.run\_forever()
:   Run the event loop until [`stop()`](#asyncio.loop.stop "asyncio.loop.stop") is called.

    If [`stop()`](#asyncio.loop.stop "asyncio.loop.stop") is called before [`run_forever()`](#asyncio.loop.run_forever "asyncio.loop.run_forever") is called,
    the loop will poll the I/O selector once with a timeout of zero,
    run all callbacks scheduled in response to I/O events (and
    those that were already scheduled), and then exit.

    If [`stop()`](#asyncio.loop.stop "asyncio.loop.stop") is called while [`run_forever()`](#asyncio.loop.run_forever "asyncio.loop.run_forever") is running,
    the loop will run the current batch of callbacks and then exit.
    Note that new callbacks scheduled by callbacks will not run in this
    case; instead, they will run the next time [`run_forever()`](#asyncio.loop.run_forever "asyncio.loop.run_forever") or
    [`run_until_complete()`](#asyncio.loop.run_until_complete "asyncio.loop.run_until_complete") is called.

loop.stop()
:   Stop the event loop.

loop.is\_running()
:   Return `True` if the event loop is currently running.

loop.is\_closed()
:   Return `True` if the event loop was closed.

loop.close()
:   Close the event loop.

    The loop must not be running when this function is called.
    Any pending callbacks will be discarded.

    This method clears all queues and shuts down the executor, but does
    not wait for the executor to finish.

    This method is idempotent and irreversible. No other methods
    should be called after the event loop is closed.

*async* loop.shutdown\_asyncgens()
:   Schedule all currently open [asynchronous generator](../glossary.html#term-asynchronous-generator) objects to
    close with an [`aclose()`](../reference/expressions.html#agen.aclose "agen.aclose") call. After calling this method,
    the event loop will issue a warning if a new asynchronous generator
    is iterated. This should be used to reliably finalize all scheduled
    asynchronous generators.

    Note that there is no need to call this function when
    [`asyncio.run()`](asyncio-runner.html#asyncio.run "asyncio.run") is used.

    Example:

    Copy

    ```
    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()

    ```

*async* loop.shutdown\_default\_executor(*timeout=None*)
:   Schedule the closure of the default executor and wait for it to join all of
    the threads in the [`ThreadPoolExecutor`](concurrent.futures.html#concurrent.futures.ThreadPoolExecutor "concurrent.futures.ThreadPoolExecutor").
    Once this method has been called,
    using the default executor with [`loop.run_in_executor()`](#asyncio.loop.run_in_executor "asyncio.loop.run_in_executor")
    will raise a [`RuntimeError`](exceptions.html#RuntimeError "RuntimeError").

    The *timeout* parameter specifies the amount of time
    (in [`float`](functions.html#float "float") seconds) the executor will be given to finish joining.
    With the default, `None`,
    the executor is allowed an unlimited amount of time.

    If the *timeout* is reached, a [`RuntimeWarning`](exceptions.html#RuntimeWarning "RuntimeWarning") is emitted
    and the default executor is terminated
    without waiting for its threads to finish joining.

    Note

    Do not call this method when using [`asyncio.run()`](asyncio-runner.html#asyncio.run "asyncio.run"),
    as the latter handles default executor shutdown automatically.

    Changed in version 3.12: Added the *timeout* parameter.

loop.call\_soon(*callback*, *\*args*, *context=None*)
:   Schedule the *callback* [callback](../glossary.html#term-callback) to be called with
    *args* arguments at the next iteration of the event loop.

    Return an instance of [`asyncio.Handle`](#asyncio.Handle "asyncio.Handle"),
    which can be used later to cancel the callback.

    Callbacks are called in the order in which they are registered.
    Each callback will be called exactly once.

    The optional keyword-only *context* argument specifies a
    custom [`contextvars.Context`](contextvars.html#contextvars.Context "contextvars.Context") for the *callback* to run in.
    Callbacks use the current context when no *context* is provided.

    Unlike [`call_soon_threadsafe()`](#asyncio.loop.call_soon_threadsafe "asyncio.loop.call_soon_threadsafe"), this method is not thread-safe.

loop.call\_soon\_threadsafe(*callback*, *\*args*, *context=None*)
:   A thread-safe variant of [`call_soon()`](#asyncio.loop.call_soon "asyncio.loop.call_soon"). When scheduling callbacks from
    another thread, this function *must* be used, since [`call_soon()`](#asyncio.loop.call_soon "asyncio.loop.call_soon") is not
    thread-safe.

    This function is safe to be called from a reentrant context or signal handler,
    however, it is not safe or fruitful to use the returned handle in such contexts.

    Raises [`RuntimeError`](exceptions.html#RuntimeError "RuntimeError") if called on a loop that’s been closed.
    This can happen on a secondary thread when the main application is
    shutting down.

    See the [concurrency and multithreading](asyncio-dev.html#asyncio-multithreading)
    section of the documentation.

    Changed in version 3.7: The *context* keyword-only parameter was added. See [**PEP 567**](https://peps.python.org/pep-0567/)
    for more details.

Note

Most [`asyncio`](asyncio.html#module-asyncio "asyncio: Asynchronous I/O.") scheduling functions don’t allow passing
keyword arguments. To do that, use [`functools.partial()`](functools.html#functools.partial "functools.partial"):

Copy

```
# will schedule "print("Hello", flush=True)"
loop.call_soon(
    functools.partial(print, "Hello", flush=True))

```

Using partial objects is usually more convenient than using lambdas,
as asyncio can render partial objects better in debug and error
messages.

Event loop provides mechanisms to schedule callback functions
to be called at some point in the future. Event loop uses monotonic
clocks to track time.

loop.call\_later(*delay*, *callback*, *\*args*, *context=None*)
:   Schedule *callback* to be called after the given *delay*
    number of seconds (can be either an int or a float).

    An instance of [`asyncio.TimerHandle`](#asyncio.TimerHandle "asyncio.TimerHandle") is returned which can
    be used to cancel the callback.

    *callback* will be called exactly once. If two callbacks are
    scheduled for exactly the same time, the order in which they
    are called is undefined.

    The optional positional *args* will be passed to the callback when
    it is called. If you want the callback to be called with keyword
    arguments use [`functools.partial()`](functools.html#functools.partial "functools.partial").

    An optional keyword-only *context* argument allows specifying a
    custom [`contextvars.Context`](contextvars.html#contextvars.Context "contextvars.Context") for the *callback* to run in.
    The current context is used when no *context* is provided.

    Changed in version 3.7: The *context* keyword-only parameter was added. See [**PEP 567**](https://peps.python.org/pep-0567/)
    for more details.

    Changed in version 3.8: In Python 3.7 and earlier with the default event loop implementation,
    the *delay* could not exceed one day.
    This has been fixed in Python 3.8.

loop.call\_at(*when*, *callback*, *\*args*, *context=None*)
:   Schedule *callback* to be called at the given absolute timestamp
    *when* (an int or a float), using the same time reference as
    [`loop.time()`](#asyncio.loop.time "asyncio.loop.time").

    This method’s behavior is the same as [`call_later()`](#asyncio.loop.call_later "asyncio.loop.call_later").

    An instance of [`asyncio.TimerHandle`](#asyncio.TimerHandle "asyncio.TimerHandle") is returned which can
    be used to cancel the callback.

    Changed in version 3.7: The *context* keyword-only parameter was added. See [**PEP 567**](https://peps.python.org/pep-0567/)
    for more details.

    Changed in version 3.8: In Python 3.7 and earlier with the default event loop implementation,
    the difference between *when* and the current time could not exceed
    one day. This has been fixed in Python 3.8.

loop.time()
:   Return the current time, as a [`float`](functions.html#float "float") value, according to
    the event loop’s internal monotonic clock.

Note

Changed in version 3.8: In Python 3.7 and earlier timeouts (relative *delay* or absolute *when*)
should not exceed one day. This has been fixed in Python 3.8.

loop.create\_future()
:   Create an [`asyncio.Future`](asyncio-future.html#asyncio.Future "asyncio.Future") object attached to the event loop.

    This is the preferred way to create Futures in asyncio. This lets
    third-party event loops provide alternative implementations of
    the Future object (with better performance or instrumentation).

loop.create\_task(*coro*, *\**, *name=None*, *context=None*, *\*\*kwargs*)
:   Schedule the execution of [coroutine](asyncio-task.html#coroutine) *coro*.
    Return a [`Task`](asyncio-task.html#asyncio.Task "asyncio.Task") object.

    Third-party event loops can use their own subclass of [`Task`](asyncio-task.html#asyncio.Task "asyncio.Task")
    for interoperability. In this case, the result type is a subclass
    of [`Task`](asyncio-task.html#asyncio.Task "asyncio.Task").

    The full function signature is largely the same as that of the
    [`Task`](asyncio-task.html#asyncio.Task "asyncio.Task") constructor (or factory) - all of the keyword arguments to
    this function are passed through to that interface, except *name*,
    or *context* if it is `None`.

    If the *name* argument is provided and not `None`, it is set as
    the name of the task using [`Task.set_name()`](asyncio-task.html#asyncio.Task.set_name "asyncio.Task.set_name").

    An optional keyword-only *context* argument allows specifying a
    custom [`contextvars.Context`](contextvars.html#contextvars.Context "contextvars.Context") for the *coro* to run in.
    The current context copy is created when no *context* is provided.

    Changed in version 3.8: Added the *name* parameter.

    Changed in version 3.11: Added the *context* parameter.

    Changed in version 3.13.3: Added `kwargs` which passes on arbitrary extra parameters, including `name` and `context`.

    Changed in version 3.13.4: Rolled back the change that passes on *name* and *context* (if it is None),
    while still passing on other arbitrary keyword arguments (to avoid breaking backwards compatibility with 3.13.3).

loop.set\_task\_factory(*factory*)
:   Set a task factory that will be used by
    [`loop.create_task()`](#asyncio.loop.create_task "asyncio.loop.create_task").

    If *factory* is `None` the default task factory will be set.
    Otherwise, *factory* must be a *callable* with the signature matching
    `(loop, coro, **kwargs)`, where *loop* is a reference to the active
    event loop, and *coro* is a coroutine object. The callable
    must pass on all *kwargs*, and return a [`asyncio.Task`](asyncio-task.html#asyncio.Task "asyncio.Task")-compatible object.

    Changed in version 3.13.3: Required that all *kwargs* are passed on to [`asyncio.Task`](asyncio-task.html#asyncio.Task "asyncio.Task").

    Changed in version 3.13.4: *name* is no longer passed to task factories. *context* is no longer passed
    to task factories if it is `None`.

loop.get\_task\_factory()
:   Return a task factory or `None` if the default one is in use.

*async* loop.create\_connection(*protocol\_factory*, *host=None*, *port=None*, *\**, *ssl=None*, *family=0*, *proto=0*, *flags=0*, *sock=None*, *local\_addr=None*, *server\_hostname=None*, *ssl\_handshake\_timeout=None*, *ssl\_shutdown\_timeout=None*, *happy\_eyeballs\_delay=None*, *interleave=None*, *all\_errors=False*)
:   Open a streaming transport connection to a given
    address specified by *host* and *port*.

    The socket family can be either [`AF_INET`](socket.html#socket.AF_INET "socket.AF_INET") or
    [`AF_INET6`](socket.html#socket.AF_INET6 "socket.AF_INET6") depending on *host* (or the *family*
    argument, if provided).

    The socket type will be [`SOCK_STREAM`](socket.html#socket.SOCK_STREAM "socket.SOCK_STREAM").

    *protocol\_factory* must be a callable returning an
    [asyncio protocol](asyncio-protocol.html#asyncio-protocol) implementation.

    This method will try to establish the connection in the background.
    When successful, it returns a `(transport, protocol)` pair.

    The chronological synopsis of the underlying operation is as follows:

    1. The connection is established and a [transport](asyncio-protocol.html#asyncio-transport)
       is created for it.
    2. *protocol\_factory* is called without arguments and is expected to
       return a [protocol](asyncio-protocol.html#asyncio-protocol) instance.
    3. The protocol instance is coupled with the transport by calling its
       [`connection_made()`](asyncio-protocol.html#asyncio.BaseProtocol.connection_made "asyncio.BaseProtocol.connection_made") method.
    4. A `(transport, protocol)` tuple is returned on success.

    The created transport is an implementation-dependent bidirectional
    stream.

    Other arguments:

    * *ssl*: if given and not false, a SSL/TLS transport is created
      (by default a plain TCP transport is created). If *ssl* is
      a [`ssl.SSLContext`](ssl.html#ssl.SSLContext "ssl.SSLContext") object, this context is used to create
      the transport; if *ssl* is [`True`](constants.html#True "True"), a default context returned
      from [`ssl.create_default_context()`](ssl.html#ssl.create_default_context "ssl.create_default_context") is used.
    * *server\_hostname* sets or overrides the hostname that the target
      server’s certificate will be matched against. Should only be passed
      if *ssl* is not `None`. By default the value of the *host* argument
      is used. If *host* is empty, there is no default and you must pass a
      value for *server\_hostname*. If *server\_hostname* is an empty
      string, hostname matching is disabled (which is a serious security
      risk, allowing for potential man-in-the-middle attacks).
    * *family*, *proto*, *flags* are the optional address family, protocol
      and flags to be passed through to getaddrinfo() for *host* resolution.
      If given, these should all be integers from the corresponding
      [`socket`](socket.html#module-socket "socket: Low-level networking interface.") module constants.
    * *happy\_eyeballs\_delay*, if given, enables Happy Eyeballs for this
      connection. It should
      be a floating-point number representing the amount of time in seconds
      to wait for a connection attempt to complete, before starting the next
      attempt in parallel. This is the “Connection Attempt Delay” as defined
      in [**RFC 8305**](https://datatracker.ietf.org/doc/html/rfc8305.html). A sensible default value recommended by the RFC is `0.25`
      (250 milliseconds).
    * *interleave* controls address reordering when a host name resolves to
      multiple IP addresses.
      If `0` or unspecified, no reordering is done, and addresses are
      tried in the order returned by [`getaddrinfo()`](#asyncio.loop.getaddrinfo "asyncio.loop.getaddrinfo"). If a positive integer
      is specified, the addresses are interleaved by address family, and the
      given integer is interpreted as “First Address Family Count” as defined
      in [**RFC 8305**](https://datatracker.ietf.org/doc/html/rfc8305.html). The default is `0` if *happy\_eyeballs\_delay* is not
      specified, and `1` if it is.
    * *sock*, if given, should be an existing, already connected
      [`socket.socket`](socket.html#socket.socket "socket.socket") object to be used by the transport.
      If *sock* is given, none of *host*, *port*, *family*, *proto*, *flags*,
      *happy\_eyeballs\_delay*, *interleave*
      and *local\_addr* should be specified.

      Note

      The *sock* argument transfers ownership of the socket to the
      transport created. To close the socket, call the transport’s
      [`close()`](asyncio-protocol.html#asyncio.BaseTransport.close "asyncio.BaseTransport.close") method.
    * *local\_addr*, if given, is a `(local_host, local_port)` tuple used
      to bind the socket locally. The *local\_host* and *local\_port*
      are looked up using `getaddrinfo()`, similarly to *host* and *port*.
    * *ssl\_handshake\_timeout* is (for a TLS connection) the time in seconds
      to wait for the TLS handshake to complete before aborting the connection.
      `60.0` seconds if `None` (default).
    * *ssl\_shutdown\_timeout* is the time in seconds to wait for the SSL shutdown
      to complete before aborting the connection. `30.0` seconds if `None`
      (default).
    * *all\_errors* determines what exceptions are raised when a connection cannot
      be created. By default, only a single `Exception` is raised: the first
      exception if there is only one or all errors have same message, or a single
      `OSError` with the error messages combined. When `all_errors` is `True`,
      an `ExceptionGroup` will be raised containing all exceptions (even if there
      is only one).

    Changed in version 3.6: The socket option [socket.TCP\_NODELAY](socket.html#socket-unix-constants) is set by default
    for all TCP connections.

    Changed in version 3.7: Added the *ssl\_handshake\_timeout* parameter.

    Changed in version 3.8: Added the *happy\_eyeballs\_delay* and *interleave* parameters.

    Happy Eyeballs Algorithm: Success with Dual-Stack Hosts.
    When a server’s IPv4 path and protocol are working, but the server’s
    IPv6 path and protocol are not working, a dual-stack client
    application experiences significant connection delay compared to an
    IPv4-only client. This is undesirable because it causes the
    dual-stack client to have a worse user experience. This document
    specifies requirements for algorithms that reduce this user-visible
    delay and provides an algorithm.

    For more information: <https://datatracker.ietf.org/doc/html/rfc6555>

    Changed in version 3.11: Added the *ssl\_shutdown\_timeout* parameter.

    Changed in version 3.12: *all\_errors* was added.

*async* loop.create\_datagram\_endpoint(*protocol\_factory*, *local\_addr=None*, *remote\_addr=None*, *\**, *family=0*, *proto=0*, *flags=0*, *reuse\_port=None*, *allow\_broadcast=None*, *sock=None*)
:   Create a datagram connection.

    The socket family can be either [`AF_INET`](socket.html#socket.AF_INET "socket.AF_INET"),
    [`AF_INET6`](socket.html#socket.AF_INET6 "socket.AF_INET6"), or [`AF_UNIX`](socket.html#socket.AF_UNIX "socket.AF_UNIX"),
    depending on *host* (or the *family* argument, if provided).

    The socket type will be [`SOCK_DGRAM`](socket.html#socket.SOCK_DGRAM "socket.SOCK_DGRAM").

    *protocol\_factory* must be a callable returning a
    [protocol](asyncio-protocol.html#asyncio-protocol) implementation.

    A tuple of `(transport, protocol)` is returned on success.

    Other arguments:

    * *local\_addr*, if given, is a `(local_host, local_port)` tuple used
      to bind the socket locally. The *local\_host* and *local\_port*
      are looked up using [`getaddrinfo()`](#asyncio.loop.getaddrinfo "asyncio.loop.getaddrinfo").
    * *remote\_addr*, if given, is a `(remote_host, remote_port)` tuple used
      to connect the socket to a remote address. The *remote\_host* and
      *remote\_port* are looked up using [`getaddrinfo()`](#asyncio.loop.getaddrinfo "asyncio.loop.getaddrinfo").
    * *family*, *proto*, *flags* are the optional address family, protocol
      and flags to be passed through to [`getaddrinfo()`](#asyncio.loop.getaddrinfo "asyncio.loop.getaddrinfo") for *host*
      resolution. If given, these should all be integers from the
      corresponding [`socket`](socket.html#module-socket "socket: Low-level networking interface.") module constants.
    * *reuse\_port* tells the kernel to allow this endpoint to be bound to the
      same port as other existing endpoints are bound to, so long as they all
      set this flag when being created. This option is not supported on Windows
      and some Unixes. If the [socket.SO\_REUSEPORT](socket.html#socket-unix-constants) constant is not
      defined then this capability is unsupported.
    * *allow\_broadcast* tells the kernel to allow this endpoint to send
      messages to the broadcast address.
    * *sock* can optionally be specified in order to use a preexisting,
      already connected, [`socket.socket`](socket.html#socket.socket "socket.socket") object to be used by the
      transport. If specified, *local\_addr* and *remote\_addr* should be omitted
      (must be [`None`](constants.html#None "None")).

      Note

      The *sock* argument transfers ownership of the socket to the
      transport created. To close the socket, call the transport’s
      [`close()`](asyncio-protocol.html#asyncio.BaseTransport.close "asyncio.BaseTransport.close") method.

    See [UDP echo client protocol](asyncio-protocol.html#asyncio-udp-echo-client-protocol) and
    [UDP echo server protocol](asyncio-protocol.html#asyncio-udp-echo-server-protocol) examples.

    Changed in version 3.4.4: The *family*, *proto*, *flags*, *reuse\_address*, *reuse\_port*,
    *allow\_broadcast*, and *sock* parameters were added.

    Changed in version 3.8: Added support for Windows.

    Changed in version 3.8.1: The *reuse\_address* parameter is no longer supported, as using
    [socket.SO\_REUSEADDR](socket.html#socket-unix-constants)
    poses a significant security concern for
    UDP. Explicitly passing `reuse_address=True` will raise an exception.

    When multiple processes with differing UIDs assign sockets to an
    identical UDP socket address with `SO_REUSEADDR`, incoming packets can
    become randomly distributed among the sockets.

    For supported platforms, *reuse\_port* can be used as a replacement for
    similar functionality. With *reuse\_port*,
    [socket.SO\_REUSEPORT](socket.html#socket-unix-constants)
    is used instead, which specifically
    prevents processes with differing UIDs from assigning sockets to the same
    socket address.

    Changed in version 3.11: The *reuse\_address* parameter, disabled since Python 3.8.1,
    3.7.6 and 3.6.10, has been entirely removed.

*async* loop.create\_unix\_connection(*protocol\_factory*, *path=None*, *\**, *ssl=None*, *sock=None*, *server\_hostname=None*, *ssl\_handshake\_timeout=None*, *ssl\_shutdown\_timeout=None*)
:   Create a Unix connection.

    The socket family will be [`AF_UNIX`](socket.html#socket.AF_UNIX "socket.AF_UNIX"); socket
    type will be [`SOCK_STREAM`](socket.html#socket.SOCK_STREAM "socket.SOCK_STREAM").

    A tuple of `(transport, protocol)` is returned on success.

    *path* is the name of a Unix domain socket and is required,
    unless a *sock* parameter is specified. Abstract Unix sockets,
    [`str`](stdtypes.html#str "str"), [`bytes`](stdtypes.html#bytes "bytes"), and [`Path`](pathlib.html#pathlib.Path "pathlib.Path") paths are
    supported.

    See the documentation of the [`loop.create_connection()`](#asyncio.loop.create_connection "asyncio.loop.create_connection") method
    for information about arguments to this method.

    Changed in version 3.7: Added the *ssl\_handshake\_timeout* parameter.
    The *path* parameter can now be a [path-like object](../glossary.html#term-path-like-object).

    Changed in version 3.11: Added the *ssl\_shutdown\_timeout* parameter.

*async* loop.create\_server(*protocol\_factory*, *host=None*, *port=None*, *\**, *family=socket.AF\_UNSPEC*, *flags=socket.AI\_PASSIVE*, *sock=None*, *backlog=100*, *ssl=None*, *reuse\_address=None*, *reuse\_port=None*, *keep\_alive=None*, *ssl\_handshake\_timeout=None*, *ssl\_shutdown\_timeout=None*, *start\_serving=True*)
:   Create a TCP server (socket type [`SOCK_STREAM`](socket.html#socket.SOCK_STREAM "socket.SOCK_STREAM")) listening
    on *port* of the *host* address.

    Returns a [`Server`](#asyncio.Server "asyncio.Server") object.

    Arguments:

    * *protocol\_factory* must be a callable returning a
      [protocol](asyncio-protocol.html#asyncio-protocol) implementation.
    * The *host* parameter can be set to several types which determine where
      the server would be listening:

      + If *host* is a string, the TCP server is bound to a single network
        interface specified by *host*.
      + If *host* is a sequence of strings, the TCP server is bound to all
        network interfaces specified by the sequence.
      + If *host* is an empty string or `None`, all interfaces are
        assumed and a list of multiple sockets will be returned (most likely
        one for IPv4 and another one for IPv6).
    * The *port* parameter can be set to specify which port the server should
      listen on. If `0` or `None` (the default), a random unused port will
      be selected (note that if *host* resolves to multiple network interfaces,
      a different random port will be selected for each interface).
    * *family* can be set to either [`socket.AF_INET`](socket.html#socket.AF_INET "socket.AF_INET") or
      [`AF_INET6`](socket.html#socket.AF_INET6 "socket.AF_INET6") to force the socket to use IPv4 or IPv6.
      If not set, the *family* will be determined from host name
      (defaults to [`AF_UNSPEC`](socket.html#socket.AF_UNSPEC "socket.AF_UNSPEC")).
    * *flags* is a bitmask for [`getaddrinfo()`](#asyncio.loop.getaddrinfo "asyncio.loop.getaddrinfo").
    * *sock* can optionally be specified in order to use a preexisting
      socket object. If specified, *host* and *port* must not be specified.

      Note

      The *sock* argument transfers ownership of the socket to the
      server created. To close the socket, call the server’s
      [`close()`](#asyncio.Server.close "asyncio.Server.close") method.
    * *backlog* is the maximum number of queued connections passed to
      [`listen()`](socket.html#socket.socket.listen "socket.socket.listen") (defaults to 100).
    * *ssl* can be set to an [`SSLContext`](ssl.html#ssl.SSLContext "ssl.SSLContext") instance to enable
      TLS over the accepted connections.
    * *reuse\_address* tells the kernel to reuse a local socket in
      `TIME_WAIT` state, without waiting for its natural timeout to
      expire. If not specified will automatically be set to `True` on
      Unix.
    * *reuse\_port* tells the kernel to allow this endpoint to be bound to the
      same port as other existing endpoints are bound to, so long as they all
      set this flag when being created. This option is not supported on
      Windows.
    * *keep\_alive* set to `True` keeps connections active by enabling the
      periodic transmission of messages.

    Changed in version 3.13: Added the *keep\_alive* parameter.

    * *ssl\_handshake\_timeout* is (for a TLS server) the time in seconds to wait
      for the TLS handshake to complete before aborting the connection.
      `60.0` seconds if `None` (default).
    * *ssl\_shutdown\_timeout* is the time in seconds to wait for the SSL shutdown
      to complete before aborting the connection. `30.0` seconds if `None`
      (default).
    * *start\_serving* set to `True` (the default) causes the created server
      to start accepting connections immediately. When set to `False`,
      the user should await on [`Server.start_serving()`](#asyncio.Server.start_serving "asyncio.Server.start_serving") or
      [`Server.serve_forever()`](#asyncio.Server.serve_forever "asyncio.Server.serve_forever") to make the server to start accepting
      connections.

    Changed in version 3.5.1: The *host* parameter can be a sequence of strings.

    Changed in version 3.6: Added *ssl\_handshake\_timeout* and *start\_serving* parameters.
    The socket option [socket.TCP\_NODELAY](socket.html#socket-unix-constants) is set by default
    for all TCP connections.

    Changed in version 3.11: Added the *ssl\_shutdown\_timeout* parameter.

*async* loop.create\_unix\_server(*protocol\_factory*, *path=None*, *\**, *sock=None*, *backlog=100*, *ssl=None*, *ssl\_handshake\_timeout=None*, *ssl\_shutdown\_timeout=None*, *start\_serving=True*, *cleanup\_socket=True*)
:   Similar to [`loop.create_server()`](#asyncio.loop.create_server "asyncio.loop.create_server") but works with the
    [`AF_UNIX`](socket.html#socket.AF_UNIX "socket.AF_UNIX") socket family.

    *path* is the name of a Unix domain socket, and is required,
    unless a *sock* argument is provided. Abstract Unix sockets,
    [`str`](stdtypes.html#str "str"), [`bytes`](stdtypes.html#bytes "bytes"), and [`Path`](pathlib.html#pathlib.Path "pathlib.Path") paths
    are supported.

    If *cleanup\_socket* is true then the Unix socket will automatically
    be removed from the filesystem when the server is closed, unless the
    socket has been replaced after the server has been created.

    See the documentation of the [`loop.create_server()`](#asyncio.loop.create_server "asyncio.loop.create_server") method
    for information about arguments to this method.

    Changed in version 3.7: Added the *ssl\_handshake\_timeout* and *start\_serving* parameters.
    The *path* parameter can now be a [`Path`](pathlib.html#pathlib.Path "pathlib.Path") object.

    Changed in version 3.11: Added the *ssl\_shutdown\_timeout* parameter.

    Changed in version 3.13: Added the *cleanup\_socket* parameter.

*async* loop.connect\_accepted\_socket(*protocol\_factory*, *sock*, *\**, *ssl=None*, *ssl\_handshake\_timeout=None*, *ssl\_shutdown\_timeout=None*)
:   Wrap an already accepted connection into a transport/protocol pair.

    This method can be used by servers that accept connections outside
    of asyncio but that use asyncio to handle them.

    Parameters:

    * *protocol\_factory* must be a callable returning a
      [protocol](asyncio-protocol.html#asyncio-protocol) implementation.
    * *sock* is a preexisting socket object returned from
      [`socket.accept`](socket.html#socket.socket.accept "socket.socket.accept").

      Note

      The *sock* argument transfers ownership of the socket to the
      transport created. To close the socket, call the transport’s
      [`close()`](asyncio-protocol.html#asyncio.BaseTransport.close "asyncio.BaseTransport.close") method.
    * *ssl* can be set to an [`SSLContext`](ssl.html#ssl.SSLContext "ssl.SSLContext") to enable SSL over
      the accepted connections.
    * *ssl\_handshake\_timeout* is (for an SSL connection) the time in seconds to
      wait for the SSL handshake to complete before aborting the connection.
      `60.0` seconds if `None` (default).
    * *ssl\_shutdown\_timeout* is the time in seconds to wait for the SSL shutdown
      to complete before aborting the connection. `30.0` seconds if `None`
      (default).

    Returns a `(transport, protocol)` pair.

    Changed in version 3.7: Added the *ssl\_handshake\_timeout* parameter.

    Changed in version 3.11: Added the *ssl\_shutdown\_timeout* parameter.

*async* loop.sendfile(*transport*, *file*, *offset=0*, *count=None*, *\**, *fallback=True*)
:   Send a *file* over a *transport*. Return the total number of bytes
    sent.

    The method uses high-performance [`os.sendfile()`](os.html#os.sendfile "os.sendfile") if available.

    *file* must be a regular file object opened in binary mode.

    *offset* tells from where to start reading the file. If specified,
    *count* is the total number of bytes to transmit as opposed to
    sending the file until EOF is reached. File position is always updated,
    even when this method raises an error, and
    [`file.tell()`](io.html#io.IOBase.tell "io.IOBase.tell") can be used to obtain the actual
    number of bytes sent.

    *fallback* set to `True` makes asyncio to manually read and send
    the file when the platform does not support the sendfile system call
    (e.g. Windows or SSL socket on Unix).

    Raise [`SendfileNotAvailableError`](asyncio-exceptions.html#asyncio.SendfileNotAvailableError "asyncio.SendfileNotAvailableError") if the system does not support
    the *sendfile* syscall and *fallback* is `False`.

*async* loop.start\_tls(*transport*, *protocol*, *sslcontext*, *\**, *server\_side=False*, *server\_hostname=None*, *ssl\_handshake\_timeout=None*, *ssl\_shutdown\_timeout=None*)
:   Upgrade an existing transport-based connection to TLS.

    Create a TLS coder/decoder instance and insert it between the *transport*
    and the *protocol*. The coder/decoder implements both *transport*-facing
    protocol and *protocol*-facing transport.

    Return the created two-interface instance. After *await*, the *protocol*
    must stop using the original *transport* and communicate with the returned
    object only because the coder caches *protocol*-side data and sporadically
    exchanges extra TLS session packets with *transport*.

    In some situations (e.g. when the passed transport is already closing) this
    may return `None`.

    Parameters:

    * *transport* and *protocol* instances that methods like
      [`create_server()`](#asyncio.loop.create_server "asyncio.loop.create_server") and
      [`create_connection()`](#asyncio.loop.create_connection "asyncio.loop.create_connection") return.
    * *sslcontext*: a configured instance of [`SSLContext`](ssl.html#ssl.SSLContext "ssl.SSLContext").
    * *server\_side* pass `True` when a server-side connection is being
      upgraded (like the one created by [`create_server()`](#asyncio.loop.create_server "asyncio.loop.create_server")).
    * *server\_hostname*: sets or overrides the host name that the target
      server’s certificate will be matched against.
    * *ssl\_handshake\_timeout* is (for a TLS connection) the time in seconds to
      wait for the TLS handshake to complete before aborting the connection.
      `60.0` seconds if `None` (default).
    * *ssl\_shutdown\_timeout* is the time in seconds to wait for the SSL shutdown
      to complete before aborting the connection. `30.0` seconds if `None`
      (default).

    Changed in version 3.11: Added the *ssl\_shutdown\_timeout* parameter.

loop.add\_reader(*fd*, *callback*, *\*args*)
:   Start monitoring the *fd* file descriptor for read availability and
    invoke *callback* with the specified arguments once *fd* is available for
    reading.

    Any preexisting callback registered for *fd* is cancelled and replaced by
    *callback*.

loop.remove\_reader(*fd*)
:   Stop monitoring the *fd* file descriptor for read availability. Returns
    `True` if *fd* was previously being monitored for reads.

loop.add\_writer(*fd*, *callback*, *\*args*)
:   Start monitoring the *fd* file descriptor for write availability and
    invoke *callback* with the specified arguments once *fd* is available for
    writing.

    Any preexisting callback registered for *fd* is cancelled and replaced by
    *callback*.

    Use [`functools.partial()`](functools.html#functools.partial "functools.partial") [to pass keyword arguments](#asyncio-pass-keywords) to *callback*.

loop.remove\_writer(*fd*)
:   Stop monitoring the *fd* file descriptor for write availability. Returns
    `True` if *fd* was previously being monitored for writes.

See also [Platform Support](asyncio-platforms.html#asyncio-platform-support) section
for some limitations of these methods.

In general, protocol implementations that use transport-based APIs
such as [`loop.create_connection()`](#asyncio.loop.create_connection "asyncio.loop.create_connection") and [`loop.create_server()`](#asyncio.loop.create_server "asyncio.loop.create_server")
are faster than implementations that work with sockets directly.
However, there are some use cases when performance is not critical, and
working with [`socket`](socket.html#socket.socket "socket.socket") objects directly is more
convenient.

*async* loop.sock\_recv(*sock*, *nbytes*)
:   Receive up to *nbytes* from *sock*. Asynchronous version of
    [`socket.recv()`](socket.html#socket.socket.recv "socket.socket.recv").

    Return the received data as a bytes object.

    *sock* must be a non-blocking socket.

    Changed in version 3.7: Even though this method was always documented as a coroutine
    method, releases before Python 3.7 returned a [`Future`](asyncio-future.html#asyncio.Future "asyncio.Future").
    Since Python 3.7 this is an `async def` method.

*async* loop.sock\_recv\_into(*sock*, *buf*)
:   Receive data from *sock* into the *buf* buffer. Modeled after the blocking
    [`socket.recv_into()`](socket.html#socket.socket.recv_into "socket.socket.recv_into") method.

    Return the number of bytes written to the buffer.

    *sock* must be a non-blocking socket.

*async* loop.sock\_recvfrom(*sock*, *bufsize*)
:   Receive a datagram of up to *bufsize* from *sock*. Asynchronous version of
    [`socket.recvfrom()`](socket.html#socket.socket.recvfrom "socket.socket.recvfrom").

    Return a tuple of (received data, remote address).

    *sock* must be a non-blocking socket.

*async* loop.sock\_recvfrom\_into(*sock*, *buf*, *nbytes=0*)
:   Receive a datagram of up to *nbytes* from *sock* into *buf*.
    Asynchronous version of
    [`socket.recvfrom_into()`](socket.html#socket.socket.recvfrom_into "socket.socket.recvfrom_into").

    Return a tuple of (number of bytes received, remote address).

    *sock* must be a non-blocking socket.

*async* loop.sock\_sendall(*sock*, *data*)
:   Send *data* to the *sock* socket. Asynchronous version of
    [`socket.sendall()`](socket.html#socket.socket.sendall "socket.socket.sendall").

    This method continues to send to the socket until either all data
    in *data* has been sent or an error occurs. `None` is returned
    on success. On error, an exception is raised. Additionally, there is no way
    to determine how much data, if any, was successfully processed by the
    receiving end of the connection.

    *sock* must be a non-blocking socket.

    Changed in version 3.7: Even though the method was always documented as a coroutine
    method, before Python 3.7 it returned a [`Future`](asyncio-future.html#asyncio.Future "asyncio.Future").
    Since Python 3.7, this is an `async def` method.

*async* loop.sock\_sendto(*sock*, *data*, *address*)
:   Send a datagram from *sock* to *address*.
    Asynchronous version of
    [`socket.sendto()`](socket.html#socket.socket.sendto "socket.socket.sendto").

    Return the number of bytes sent.

    *sock* must be a non-blocking socket.

*async* loop.sock\_connect(*sock*, *address*)
:   Connect *sock* to a remote socket at *address*.

    Asynchronous version of [`socket.connect()`](socket.html#socket.socket.connect "socket.socket.connect").

    *sock* must be a non-blocking socket.

    Changed in version 3.5.2: `address` no longer needs to be resolved. `sock_connect`
    will try to check if the *address* is already resolved by calling
    [`socket.inet_pton()`](socket.html#socket.inet_pton "socket.inet_pton"). If not,
    [`loop.getaddrinfo()`](#asyncio.loop.getaddrinfo "asyncio.loop.getaddrinfo") will be used to resolve the
    *address*.

*async* loop.sock\_accept(*sock*)
:   Accept a connection. Modeled after the blocking
    [`socket.accept()`](socket.html#socket.socket.accept "socket.socket.accept") method.

    The socket must be bound to an address and listening
    for connections. The return value is a pair `(conn, address)` where *conn*
    is a *new* socket object usable to send and receive data on the connection,
    and *address* is the address bound to the socket on the other end of the
    connection.

    *sock* must be a non-blocking socket.

    Changed in version 3.7: Even though the method was always documented as a coroutine
    method, before Python 3.7 it returned a [`Future`](asyncio-future.html#asyncio.Future "asyncio.Future").
    Since Python 3.7, this is an `async def` method.

*async* loop.sock\_sendfile(*sock*, *file*, *offset=0*, *count=None*, *\**, *fallback=True*)
:   Send a file using high-performance [`os.sendfile`](os.html#os.sendfile "os.sendfile") if possible.
    Return the total number of bytes sent.

    Asynchronous version of [`socket.sendfile()`](socket.html#socket.socket.sendfile "socket.socket.sendfile").

    *sock* must be a non-blocking [`socket.SOCK_STREAM`](socket.html#socket.SOCK_STREAM "socket.SOCK_STREAM")
    [`socket`](socket.html#socket.socket "socket.socket").

    *file* must be a regular file object open in binary mode.

    *offset* tells from where to start reading the file. If specified,
    *count* is the total number of bytes to transmit as opposed to
    sending the file until EOF is reached. File position is always updated,
    even when this method raises an error, and
    [`file.tell()`](io.html#io.IOBase.tell "io.IOBase.tell") can be used to obtain the actual
    number of bytes sent.

    *fallback*, when set to `True`, makes asyncio manually read and send
    the file when the platform does not support the sendfile syscall
    (e.g. Windows or SSL socket on Unix).

    Raise [`SendfileNotAvailableError`](asyncio-exceptions.html#asyncio.SendfileNotAvailableError "asyncio.SendfileNotAvailableError") if the system does not support
    *sendfile* syscall and *fallback* is `False`.

    *sock* must be a non-blocking socket.

*async* loop.getaddrinfo(*host*, *port*, *\**, *family=0*, *type=0*, *proto=0*, *flags=0*)
:   Asynchronous version of [`socket.getaddrinfo()`](socket.html#socket.getaddrinfo "socket.getaddrinfo").

*async* loop.getnameinfo(*sockaddr*, *flags=0*)
:   Asynchronous version of [`socket.getnameinfo()`](socket.html#socket.getnameinfo "socket.getnameinfo").

Note

Both *getaddrinfo* and *getnameinfo* internally utilize their synchronous
versions through the loop’s default thread pool executor.
When this executor is saturated, these methods may experience delays,
which higher-level networking libraries may report as increased timeouts.
To mitigate this, consider using a custom executor for other user tasks,
or setting a default executor with a larger number of workers.

Changed in version 3.7: Both *getaddrinfo* and *getnameinfo* methods were always documented
to return a coroutine, but prior to Python 3.7 they were, in fact,
returning [`asyncio.Future`](asyncio-future.html#asyncio.Future "asyncio.Future") objects. Starting with Python 3.7
both methods are coroutines.

*async* loop.connect\_read\_pipe(*protocol\_factory*, *pipe*)
:   Register the read end of *pipe* in the event loop.

    *protocol\_factory* must be a callable returning an
    [asyncio protocol](asyncio-protocol.html#asyncio-protocol) implementation.

    *pipe* is a [file-like object](../glossary.html#term-file-object).

    Return pair `(transport, protocol)`, where *transport* supports
    the [`ReadTransport`](asyncio-protocol.html#asyncio.ReadTransport "asyncio.ReadTransport") interface and *protocol* is an object
    instantiated by the *protocol\_factory*.

    With [`SelectorEventLoop`](#asyncio.SelectorEventLoop "asyncio.SelectorEventLoop") event loop, the *pipe* is set to
    non-blocking mode.

*async* loop.connect\_write\_pipe(*protocol\_factory*, *pipe*)
:   Register the write end of *pipe* in the event loop.

    *protocol\_factory* must be a callable returning an
    [asyncio protocol](asyncio-protocol.html#asyncio-protocol) implementation.

    *pipe* is [file-like object](../glossary.html#term-file-object).

    Return pair `(transport, protocol)`, where *transport* supports
    [`WriteTransport`](asyncio-protocol.html#asyncio.WriteTransport "asyncio.WriteTransport") interface and *protocol* is an object
    instantiated by the *protocol\_factory*.

    With [`SelectorEventLoop`](#asyncio.SelectorEventLoop "asyncio.SelectorEventLoop") event loop, the *pipe* is set to
    non-blocking mode.

loop.add\_signal\_handler(*signum*, *callback*, *\*args*)
:   Set *callback* as the handler for the *signum* signal.

    The callback will be invoked by *loop*, along with other queued callbacks
    and runnable coroutines of that event loop. Unlike signal handlers
    registered using [`signal.signal()`](signal.html#signal.signal "signal.signal"), a callback registered with this
    function is allowed to interact with the event loop.

    Raise [`ValueError`](exceptions.html#ValueError "ValueError") if the signal number is invalid or uncatchable.
    Raise [`RuntimeError`](exceptions.html#RuntimeError "RuntimeError") if there is a problem setting up the handler.

    Use [`functools.partial()`](functools.html#functools.partial "functools.partial") [to pass keyword arguments](#asyncio-pass-keywords) to *callback*.

    Like [`signal.signal()`](signal.html#signal.signal "signal.signal"), this function must be invoked in the main
    thread.

loop.remove\_signal\_handler(*sig*)
:   Remove the handler for the *sig* signal.

    Return `True` if the signal handler was removed, or `False` if
    no handler was set for the given signal.

*awaitable* loop.run\_in\_executor(*executor*, *func*, *\*args*)
:   Arrange for *func* to be called in the specified executor.

    The *executor* argument should be an [`concurrent.futures.Executor`](concurrent.futures.html#concurrent.futures.Executor "concurrent.futures.Executor")
    instance. The default executor is used if *executor* is `None`.
    The default executor can be set by [`loop.set_default_executor()`](#asyncio.loop.set_default_executor "asyncio.loop.set_default_executor"),
    otherwise, a [`concurrent.futures.ThreadPoolExecutor`](concurrent.futures.html#concurrent.futures.ThreadPoolExecutor "concurrent.futures.ThreadPoolExecutor") will be
    lazy-initialized and used by [`run_in_executor()`](#asyncio.loop.run_in_executor "asyncio.loop.run_in_executor") if needed.

    Example:

    Copy

    ```
    import asyncio
    import concurrent.futures

    def blocking_io():
        # File operations (such as logging) can block the
        # event loop: run them in a thread pool.
        with open('/dev/urandom', 'rb') as f:
            return f.read(100)

    def cpu_bound():
        # CPU-bound operations will block the event loop:
        # in general it is preferable to run them in a
        # process pool.
        return sum(i * i for i in range(10 ** 7))

    async def main():
        loop = asyncio.get_running_loop()

        ## Options:

        # 1. Run in the default loop's executor:
        result = await loop.run_in_executor(
            None, blocking_io)
        print('default thread pool', result)

        # 2. Run in a custom thread pool:
        with concurrent.futures.ThreadPoolExecutor() as pool:
            result = await loop.run_in_executor(
                pool, blocking_io)
            print('custom thread pool', result)

        # 3. Run in a custom process pool:
        with concurrent.futures.ProcessPoolExecutor() as pool:
            result = await loop.run_in_executor(
                pool, cpu_bound)
            print('custom process pool', result)

    if __name__ == '__main__':
        asyncio.run(main())

    ```

    Note that the entry point guard (`if __name__ == '__main__'`)
    is required for option 3 due to the peculiarities of [`multiprocessing`](multiprocessing.html#module-multiprocessing "multiprocessing: Process-based parallelism."),
    which is used by [`ProcessPoolExecutor`](concurrent.futures.html#concurrent.futures.ProcessPoolExecutor "concurrent.futures.ProcessPoolExecutor").
    See [Safe importing of main module](multiprocessing.html#multiprocessing-safe-main-import).

    This method returns a [`asyncio.Future`](asyncio-future.html#asyncio.Future "asyncio.Future") object.

    Use [`functools.partial()`](functools.html#functools.partial "functools.partial") [to pass keyword arguments](#asyncio-pass-keywords) to *func*.

    Changed in version 3.5.3: [`loop.run_in_executor()`](#asyncio.loop.run_in_executor "asyncio.loop.run_in_executor") no longer configures the
    `max_workers` of the thread pool executor it creates, instead
    leaving it up to the thread pool executor
    ([`ThreadPoolExecutor`](concurrent.futures.html#concurrent.futures.ThreadPoolExecutor "concurrent.futures.ThreadPoolExecutor")) to set the
    default.

loop.set\_default\_executor(*executor*)
:   Set *executor* as the default executor used by [`run_in_executor()`](#asyncio.loop.run_in_executor "asyncio.loop.run_in_executor").
    *executor* must be an instance of
    [`ThreadPoolExecutor`](concurrent.futures.html#concurrent.futures.ThreadPoolExecutor "concurrent.futures.ThreadPoolExecutor").

Allows customizing how exceptions are handled in the event loop.

loop.set\_exception\_handler(*handler*)
:   Set *handler* as the new event loop exception handler.

    If *handler* is `None`, the default exception handler will
    be set. Otherwise, *handler* must be a callable with the signature
    matching `(loop, context)`, where `loop`
    is a reference to the active event loop, and `context`
    is a `dict` object containing the details of the exception
    (see [`call_exception_handler()`](#asyncio.loop.call_exception_handler "asyncio.loop.call_exception_handler") documentation for details
    about context).

    If the handler is called on behalf of a [`Task`](asyncio-task.html#asyncio.Task "asyncio.Task") or
    [`Handle`](#asyncio.Handle "asyncio.Handle"), it is run in the
    [`contextvars.Context`](contextvars.html#contextvars.Context "contextvars.Context") of that task or callback handle.

    Changed in version 3.12: The handler may be called in the [`Context`](contextvars.html#contextvars.Context "contextvars.Context")
    of the task or handle where the exception originated.

loop.get\_exception\_handler()
:   Return the current exception handler, or `None` if no custom
    exception handler was set.

loop.default\_exception\_handler(*context*)
:   Default exception handler.

    This is called when an exception occurs and no exception
    handler is set. This can be called by a custom exception
    handler that wants to defer to the default handler behavior.

    *context* parameter has the same meaning as in
    [`call_exception_handler()`](#asyncio.loop.call_exception_handler "asyncio.loop.call_exception_handler").

loop.call\_exception\_handler(*context*)
:   Call the current event loop exception handler.

    *context* is a `dict` object containing the following keys
    (new keys may be introduced in future Python versions):

    * ‘message’: Error message;
    * ‘exception’ (optional): Exception object;
    * ‘future’ (optional): [`asyncio.Future`](asyncio-future.html#asyncio.Future "asyncio.Future") instance;
    * ‘task’ (optional): [`asyncio.Task`](asyncio-task.html#asyncio.Task "asyncio.Task") instance;
    * ‘handle’ (optional): [`asyncio.Handle`](#asyncio.Handle "asyncio.Handle") instance;
    * ‘protocol’ (optional): [Protocol](asyncio-protocol.html#asyncio-protocol) instance;
    * ‘transport’ (optional): [Transport](asyncio-protocol.html#asyncio-transport) instance;
    * ‘socket’ (optional): [`socket.socket`](socket.html#socket.socket "socket.socket") instance;
    * ‘source\_traceback’ (optional): Traceback of the source;
    * ‘handle\_traceback’ (optional): Traceback of the handle;
    * ‘asyncgen’ (optional): Asynchronous generator that caused
      :   the exception.

    Note

    This method should not be overloaded in subclassed
    event loops. For custom exception handling, use
    the [`set_exception_handler()`](#asyncio.loop.set_exception_handler "asyncio.loop.set_exception_handler") method.

loop.get\_debug()
:   Get the debug mode ([`bool`](functions.html#bool "bool")) of the event loop.

    The default value is `True` if the environment variable
    [`PYTHONASYNCIODEBUG`](../using/cmdline.html#envvar-PYTHONASYNCIODEBUG) is set to a non-empty string, `False`
    otherwise.

loop.set\_debug(*enabled: [bool](functions.html#bool "bool")*)
:   Set the debug mode of the event loop.

loop.slow\_callback\_duration
:   This attribute can be used to set the
    minimum execution duration in seconds that is considered “slow”.
    When debug mode is enabled, “slow” callbacks are logged.

    Default value is 100 milliseconds.

Methods described in this subsections are low-level. In regular
async/await code consider using the high-level
[`asyncio.create_subprocess_shell()`](asyncio-subprocess.html#asyncio.create_subprocess_shell "asyncio.create_subprocess_shell") and
[`asyncio.create_subprocess_exec()`](asyncio-subprocess.html#asyncio.create_subprocess_exec "asyncio.create_subprocess_exec") convenience functions instead.

*async* loop.subprocess\_exec(*protocol\_factory*, *\*args*, *stdin=subprocess.PIPE*, *stdout=subprocess.PIPE*, *stderr=subprocess.PIPE*, *\*\*kwargs*)
:   Create a subprocess from one or more string arguments specified by
    *args*.

    *args* must be a list of strings represented by:

    The first string specifies the program executable,
    and the remaining strings specify the arguments. Together, string
    arguments form the `argv` of the program.

    This is similar to the standard library [`subprocess.Popen`](subprocess.html#subprocess.Popen "subprocess.Popen")
    class called with `shell=False` and the list of strings passed as
    the first argument; however, where [`Popen`](subprocess.html#subprocess.Popen "subprocess.Popen") takes
    a single argument which is list of strings, *subprocess\_exec*
    takes multiple string arguments.

    The *protocol\_factory* must be a callable returning a subclass of the
    [`asyncio.SubprocessProtocol`](asyncio-protocol.html#asyncio.SubprocessProtocol "asyncio.SubprocessProtocol") class.

    Other parameters:

    * *stdin* can be any of these:

      + a file-like object
      + an existing file descriptor (a positive integer), for example those created with [`os.pipe()`](os.html#os.pipe "os.pipe")
      + the [`subprocess.PIPE`](subprocess.html#subprocess.PIPE "subprocess.PIPE") constant (default) which will create a new
        pipe and connect it,
      + the value `None` which will make the subprocess inherit the file
        descriptor from this process
      + the [`subprocess.DEVNULL`](subprocess.html#subprocess.DEVNULL "subprocess.DEVNULL") constant which indicates that the
        special [`os.devnull`](os.html#os.devnull "os.devnull") file will be used
    * *stdout* can be any of these:

      + a file-like object
      + the [`subprocess.PIPE`](subprocess.html#subprocess.PIPE "subprocess.PIPE") constant (default) which will create a new
        pipe and connect it,
      + the value `None` which will make the subprocess inherit the file
        descriptor from this process
      + the [`subprocess.DEVNULL`](subprocess.html#subprocess.DEVNULL "subprocess.DEVNULL") constant which indicates that the
        special [`os.devnull`](os.html#os.devnull "os.devnull") file will be used
    * *stderr* can be any of these:

      + a file-like object
      + the [`subprocess.PIPE`](subprocess.html#subprocess.PIPE "subprocess.PIPE") constant (default) which will create a new
        pipe and connect it,
      + the value `None` which will make the subprocess inherit the file
        descriptor from this process
      + the [`subprocess.DEVNULL`](subprocess.html#subprocess.DEVNULL "subprocess.DEVNULL") constant which indicates that the
        special [`os.devnull`](os.html#os.devnull "os.devnull") file will be used
      + the [`subprocess.STDOUT`](subprocess.html#subprocess.STDOUT "subprocess.STDOUT") constant which will connect the standard
        error stream to the process’ standard output stream
    * All other keyword arguments are passed to [`subprocess.Popen`](subprocess.html#subprocess.Popen "subprocess.Popen")
      without interpretation, except for *bufsize*, *universal\_newlines*,
      *shell*, *text*, *encoding* and *errors*, which should not be specified
      at all.

      The `asyncio` subprocess API does not support decoding the streams
      as text. [`bytes.decode()`](stdtypes.html#bytes.decode "bytes.decode") can be used to convert the bytes returned
      from the stream to text.

    If a file-like object passed as *stdin*, *stdout* or *stderr* represents a
    pipe, then the other side of this pipe should be registered with
    [`connect_write_pipe()`](#asyncio.loop.connect_write_pipe "asyncio.loop.connect_write_pipe") or [`connect_read_pipe()`](#asyncio.loop.connect_read_pipe "asyncio.loop.connect_read_pipe") for use
    with the event loop.

    See the constructor of the [`subprocess.Popen`](subprocess.html#subprocess.Popen "subprocess.Popen") class
    for documentation on other arguments.

    Returns a pair of `(transport, protocol)`, where *transport*
    conforms to the [`asyncio.SubprocessTransport`](asyncio-protocol.html#asyncio.SubprocessTransport "asyncio.SubprocessTransport") base class and
    *protocol* is an object instantiated by the *protocol\_factory*.

*async* loop.subprocess\_shell(*protocol\_factory*, *cmd*, *\**, *stdin=subprocess.PIPE*, *stdout=subprocess.PIPE*, *stderr=subprocess.PIPE*, *\*\*kwargs*)
:   Create a subprocess from *cmd*, which can be a [`str`](stdtypes.html#str "str") or a
    [`bytes`](stdtypes.html#bytes "bytes") string encoded to the
    [filesystem encoding](os.html#filesystem-encoding),
    using the platform’s “shell” syntax.

    This is similar to the standard library [`subprocess.Popen`](subprocess.html#subprocess.Popen "subprocess.Popen")
    class called with `shell=True`.

    The *protocol\_factory* must be a callable returning a subclass of the
    [`SubprocessProtocol`](asyncio-protocol.html#asyncio.SubprocessProtocol "asyncio.SubprocessProtocol") class.

    See [`subprocess_exec()`](#asyncio.loop.subprocess_exec "asyncio.loop.subprocess_exec") for more details about
    the remaining arguments.

    Returns a pair of `(transport, protocol)`, where *transport*
    conforms to the [`SubprocessTransport`](asyncio-protocol.html#asyncio.SubprocessTransport "asyncio.SubprocessTransport") base class and
    *protocol* is an object instantiated by the *protocol\_factory*.

Note

It is the application’s responsibility to ensure that all whitespace
and special characters are quoted appropriately to avoid [shell injection](https://en.wikipedia.org/wiki/Shell_injection#Shell_injection)
vulnerabilities. The [`shlex.quote()`](shlex.html#shlex.quote "shlex.quote") function can be used to
properly escape whitespace and special characters in strings that
are going to be used to construct shell commands.

Callback Handles
----------------

*class* asyncio.Handle
:   A callback wrapper object returned by [`loop.call_soon()`](#asyncio.loop.call_soon "asyncio.loop.call_soon"),
    [`loop.call_soon_threadsafe()`](#asyncio.loop.call_soon_threadsafe "asyncio.loop.call_soon_threadsafe").

    get\_context()
    :   Return the [`contextvars.Context`](contextvars.html#contextvars.Context "contextvars.Context") object
        associated with the handle.

    cancel()
    :   Cancel the callback. If the callback has already been canceled
        or executed, this method has no effect.

    cancelled()
    :   Return `True` if the callback was cancelled.

*class* asyncio.TimerHandle
:   A callback wrapper object returned by [`loop.call_later()`](#asyncio.loop.call_later "asyncio.loop.call_later"),
    and [`loop.call_at()`](#asyncio.loop.call_at "asyncio.loop.call_at").

    This class is a subclass of [`Handle`](#asyncio.Handle "asyncio.Handle").

    when()
    :   Return a scheduled callback time as [`float`](functions.html#float "float") seconds.

        The time is an absolute timestamp, using the same time
        reference as [`loop.time()`](#asyncio.loop.time "asyncio.loop.time").

Server Objects
--------------

Server objects are created by [`loop.create_server()`](#asyncio.loop.create_server "asyncio.loop.create_server"),
[`loop.create_unix_server()`](#asyncio.loop.create_unix_server "asyncio.loop.create_unix_server"), [`start_server()`](asyncio-stream.html#asyncio.start_server "asyncio.start_server"),
and [`start_unix_server()`](asyncio-stream.html#asyncio.start_unix_server "asyncio.start_unix_server") functions.

Do not instantiate the [`Server`](#asyncio.Server "asyncio.Server") class directly.

*class* asyncio.Server
:   *Server* objects are asynchronous context managers. When used in an
    `async with` statement, it’s guaranteed that the Server object is
    closed and not accepting new connections when the `async with`
    statement is completed:

    Copy

    ```
    srv = await loop.create_server(...)

    async with srv:
        # some code

    # At this point, srv is closed and no longer accepts new connections.

    ```

    Changed in version 3.7: Server object is an asynchronous context manager since Python 3.7.

    Changed in version 3.11: This class was exposed publicly as `asyncio.Server` in Python 3.9.11, 3.10.3 and 3.11.

    close()
    :   Stop serving: close listening sockets and set the [`sockets`](#asyncio.Server.sockets "asyncio.Server.sockets")
        attribute to `None`.

        The sockets that represent existing incoming client connections
        are left open.

        The server is closed asynchronously; use the [`wait_closed()`](#asyncio.Server.wait_closed "asyncio.Server.wait_closed")
        coroutine to wait until the server is closed (and no more
        connections are active).

    close\_clients()
    :   Close all existing incoming client connections.

        Calls [`close()`](asyncio-protocol.html#asyncio.BaseTransport.close "asyncio.BaseTransport.close") on all associated
        transports.

        [`close()`](#asyncio.Server.close "asyncio.Server.close") should be called before [`close_clients()`](#asyncio.Server.close_clients "asyncio.Server.close_clients") when
        closing the server to avoid races with new clients connecting.

    abort\_clients()
    :   Close all existing incoming client connections immediately,
        without waiting for pending operations to complete.

        Calls [`abort()`](asyncio-protocol.html#asyncio.WriteTransport.abort "asyncio.WriteTransport.abort") on all associated
        transports.

        [`close()`](#asyncio.Server.close "asyncio.Server.close") should be called before [`abort_clients()`](#asyncio.Server.abort_clients "asyncio.Server.abort_clients") when
        closing the server to avoid races with new clients connecting.

    get\_loop()
    :   Return the event loop associated with the server object.

    *async* start\_serving()
    :   Start accepting connections.

        This method is idempotent, so it can be called when
        the server is already serving.

        The *start\_serving* keyword-only parameter to
        [`loop.create_server()`](#asyncio.loop.create_server "asyncio.loop.create_server") and
        [`asyncio.start_server()`](asyncio-stream.html#asyncio.start_server "asyncio.start_server") allows creating a Server object
        that is not accepting connections initially. In this case
        `Server.start_serving()`, or [`Server.serve_forever()`](#asyncio.Server.serve_forever "asyncio.Server.serve_forever") can be used
        to make the Server start accepting connections.

    *async* serve\_forever()
    :   Start accepting connections until the coroutine is cancelled.
        Cancellation of `serve_forever` task causes the server
        to be closed.

        This method can be called if the server is already accepting
        connections. Only one `serve_forever` task can exist per
        one *Server* object.

        Example:

        Copy

        ```
        async def client_connected(reader, writer):
            # Communicate with the client with
            # reader/writer streams.  For example:
            await reader.readline()

        async def main(host, port):
            srv = await asyncio.start_server(
                client_connected, host, port)
            await srv.serve_forever()

        asyncio.run(main('127.0.0.1', 0))

        ```

    is\_serving()
    :   Return `True` if the server is accepting new connections.

    *async* wait\_closed()
    :   Wait until the [`close()`](#asyncio.Server.close "asyncio.Server.close") method completes and all active
        connections have finished.

    sockets
    :   List of socket-like objects, `asyncio.trsock.TransportSocket`, which
        the server is listening on.

        Changed in version 3.7: Prior to Python 3.7 `Server.sockets` used to return an
        internal list of server sockets directly. In 3.7 a copy
        of that list is returned.

Event Loop Implementations
--------------------------

asyncio ships with two different event loop implementations:
[`SelectorEventLoop`](#asyncio.SelectorEventLoop "asyncio.SelectorEventLoop") and [`ProactorEventLoop`](#asyncio.ProactorEventLoop "asyncio.ProactorEventLoop").

By default asyncio is configured to use [`EventLoop`](#asyncio.EventLoop "asyncio.EventLoop").

*class* asyncio.SelectorEventLoop
:   A subclass of [`AbstractEventLoop`](#asyncio.AbstractEventLoop "asyncio.AbstractEventLoop") based on the
    [`selectors`](selectors.html#module-selectors "selectors: High-level I/O multiplexing.") module.

    Uses the most efficient *selector* available for the given
    platform. It is also possible to manually configure the
    exact selector implementation to be used:

    Copy

    ```
    import asyncio
    import selectors

    class MyPolicy(asyncio.DefaultEventLoopPolicy):
       def new_event_loop(self):
          selector = selectors.SelectSelector()
          return asyncio.SelectorEventLoop(selector)

    asyncio.set_event_loop_policy(MyPolicy())

    ```

*class* asyncio.ProactorEventLoop
:   A subclass of [`AbstractEventLoop`](#asyncio.AbstractEventLoop "asyncio.AbstractEventLoop") for Windows that uses “I/O Completion Ports” (IOCP).

*class* asyncio.EventLoop

*class* asyncio.AbstractEventLoop
:   Abstract base class for asyncio-compliant event loops.

    The [Event Loop Methods](#asyncio-event-loop-methods) section lists all
    methods that an alternative implementation of `AbstractEventLoop`
    should have defined.

Examples
--------

Note that all examples in this section **purposefully** show how
to use the low-level event loop APIs, such as [`loop.run_forever()`](#asyncio.loop.run_forever "asyncio.loop.run_forever")
and [`loop.call_soon()`](#asyncio.loop.call_soon "asyncio.loop.call_soon"). Modern asyncio applications rarely
need to be written this way; consider using the high-level functions
like [`asyncio.run()`](asyncio-runner.html#asyncio.run "asyncio.run").

### Hello World with call\_soon()

An example using the [`loop.call_soon()`](#asyncio.loop.call_soon "asyncio.loop.call_soon") method to schedule a
callback. The callback displays `"Hello World"` and then stops the
event loop:

Copy

```
import asyncio

def hello_world(loop):
    """A callback to print 'Hello World' and stop the event loop"""
    print('Hello World')
    loop.stop()

loop = asyncio.new_event_loop()

# Schedule a call to hello_world()
loop.call_soon(hello_world, loop)

# Blocking call interrupted by loop.stop()
try:
    loop.run_forever()
finally:
    loop.close()

```

See also

A similar [Hello World](asyncio-task.html#coroutine)
example created with a coroutine and the [`run()`](asyncio-runner.html#asyncio.run "asyncio.run") function.

### Display the current date with call\_later()

An example of a callback displaying the current date every second. The
callback uses the [`loop.call_later()`](#asyncio.loop.call_later "asyncio.loop.call_later") method to reschedule itself
after 5 seconds, and then stops the event loop:

Copy

```
import asyncio
import datetime

def display_date(end_time, loop):
    print(datetime.datetime.now())
    if (loop.time() + 1.0) < end_time:
        loop.call_later(1, display_date, end_time, loop)
    else:
        loop.stop()

loop = asyncio.new_event_loop()

# Schedule the first call to display_date()
end_time = loop.time() + 5.0
loop.call_soon(display_date, end_time, loop)

# Blocking call interrupted by loop.stop()
try:
    loop.run_forever()
finally:
    loop.close()

```

See also

A similar [current date](asyncio-task.html#asyncio-example-sleep) example
created with a coroutine and the [`run()`](asyncio-runner.html#asyncio.run "asyncio.run") function.

### Watch a file descriptor for read events

Wait until a file descriptor received some data using the
[`loop.add_reader()`](#asyncio.loop.add_reader "asyncio.loop.add_reader") method and then close the event loop:

Copy

```
import asyncio
from socket import socketpair

# Create a pair of connected file descriptors
rsock, wsock = socketpair()

loop = asyncio.new_event_loop()

def reader():
    data = rsock.recv(100)
    print("Received:", data.decode())

    # We are done: unregister the file descriptor
    loop.remove_reader(rsock)

    # Stop the event loop
    loop.stop()

# Register the file descriptor for read event
loop.add_reader(rsock, reader)

# Simulate the reception of data from the network
loop.call_soon(wsock.send, 'abc'.encode())

try:
    # Run the event loop
    loop.run_forever()
finally:
    # We are done. Close sockets and the event loop.
    rsock.close()
    wsock.close()
    loop.close()

```

### Set signal handlers for SIGINT and SIGTERM

(This `signals` example only works on Unix.)

Register handlers for signals [`SIGINT`](signal.html#signal.SIGINT "signal.SIGINT") and [`SIGTERM`](signal.html#signal.SIGTERM "signal.SIGTERM")
using the [`loop.add_signal_handler()`](#asyncio.loop.add_signal_handler "asyncio.loop.add_signal_handler") method:

Copy

```
import asyncio
import functools
import os
import signal

def ask_exit(signame, loop):
    print("got signal %s: exit" % signame)
    loop.stop()

async def main():
    loop = asyncio.get_running_loop()

    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(
            getattr(signal, signame),
            functools.partial(ask_exit, signame, loop))

    await asyncio.sleep(3600)

print("Event loop running for 1 hour, press Ctrl+C to interrupt.")
print(f"pid {os.getpid()}: send SIGINT or SIGTERM to exit.")

asyncio.run(main())

```