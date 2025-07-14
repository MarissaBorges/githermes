Runners
=======

**Source code:** [Lib/asyncio/runners.py](https://github.com/python/cpython/tree/3.13/Lib/asyncio/runners.py)

This section outlines high-level asyncio primitives to run asyncio code.

They are built on top of an [event loop](asyncio-eventloop.html#asyncio-event-loop) with the aim
to simplify async code usage for common wide-spread scenarios.



asyncio.run(*coro*, *\**, *debug=None*, *loop\_factory=None*)
:   Execute the [coroutine](../glossary.html#term-coroutine) *coro* and return the result.

    This function runs the passed coroutine, taking care of
    managing the asyncio event loop, *finalizing asynchronous
    generators*, and closing the executor.

    This function cannot be called when another asyncio event loop is
    running in the same thread.

    If *debug* is `True`, the event loop will be run in debug mode. `False` disables
    debug mode explicitly. `None` is used to respect the global
    [Debug Mode](asyncio-dev.html#asyncio-debug-mode) settings.

    If *loop\_factory* is not `None`, it is used to create a new event loop;
    otherwise [`asyncio.new_event_loop()`](asyncio-eventloop.html#asyncio.new_event_loop "asyncio.new_event_loop") is used. The loop is closed at the end.
    This function should be used as a main entry point for asyncio programs,
    and should ideally only be called once. It is recommended to use
    *loop\_factory* to configure the event loop instead of policies.
    Passing [`asyncio.EventLoop`](asyncio-eventloop.html#asyncio.EventLoop "asyncio.EventLoop") allows running asyncio without the
    policy system.

    The executor is given a timeout duration of 5 minutes to shutdown.
    If the executor hasn’t finished within that duration, a warning is
    emitted and the executor is closed.

    Example:

    Copy

    ```
    async def main():
        await asyncio.sleep(1)
        print('hello')

    asyncio.run(main())

    ```

    Changed in version 3.10: *debug* is `None` by default to respect the global debug mode settings.

    Changed in version 3.12: Added *loop\_factory* parameter.

*class* asyncio.Runner(*\**, *debug=None*, *loop\_factory=None*)
:   A context manager that simplifies *multiple* async function calls in the same
    context.

    Sometimes several top-level async functions should be called in the same [event
    loop](asyncio-eventloop.html#asyncio-event-loop) and [`contextvars.Context`](contextvars.html#contextvars.Context "contextvars.Context").

    If *debug* is `True`, the event loop will be run in debug mode. `False` disables
    debug mode explicitly. `None` is used to respect the global
    [Debug Mode](asyncio-dev.html#asyncio-debug-mode) settings.

    *loop\_factory* could be used for overriding the loop creation.
    It is the responsibility of the *loop\_factory* to set the created loop as the
    current one. By default [`asyncio.new_event_loop()`](asyncio-eventloop.html#asyncio.new_event_loop "asyncio.new_event_loop") is used and set as
    current event loop with [`asyncio.set_event_loop()`](asyncio-eventloop.html#asyncio.set_event_loop "asyncio.set_event_loop") if *loop\_factory* is `None`.

    Basically, [`asyncio.run()`](#asyncio.run "asyncio.run") example can be rewritten with the runner usage:

    Copy

    ```
    async def main():
        await asyncio.sleep(1)
        print('hello')

    with asyncio.Runner() as runner:
        runner.run(main())

    ```

    run(*coro*, *\**, *context=None*)
    :   Run a [coroutine](../glossary.html#term-coroutine) *coro* in the embedded loop.

        Return the coroutine’s result or raise its exception.

        An optional keyword-only *context* argument allows specifying a
        custom [`contextvars.Context`](contextvars.html#contextvars.Context "contextvars.Context") for the *coro* to run in.
        The runner’s default context is used if `None`.

        This function cannot be called when another asyncio event loop is
        running in the same thread.

    close()
    :   Close the runner.

        Finalize asynchronous generators, shutdown default executor, close the event loop
        and release embedded [`contextvars.Context`](contextvars.html#contextvars.Context "contextvars.Context").

    get\_loop()
    :   Return the event loop associated with the runner instance.

    Note

    [`Runner`](#asyncio.Runner "asyncio.Runner") uses the lazy initialization strategy, its constructor doesn’t
    initialize underlying low-level structures.

    Embedded *loop* and *context* are created at the [`with`](../reference/compound_stmts.html#with) body entering
    or the first call of [`run()`](#asyncio.run "asyncio.run") or [`get_loop()`](#asyncio.Runner.get_loop "asyncio.Runner.get_loop").