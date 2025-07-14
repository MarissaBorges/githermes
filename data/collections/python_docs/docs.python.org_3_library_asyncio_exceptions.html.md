Exceptions
==========

**Source code:** [Lib/asyncio/exceptions.py](https://github.com/python/cpython/tree/3.13/Lib/asyncio/exceptions.py)

---

*exception* asyncio.TimeoutError
:   A deprecated alias of [`TimeoutError`](exceptions.html#TimeoutError "TimeoutError"),
    raised when the operation has exceeded the given deadline.

    Changed in version 3.11: This class was made an alias of [`TimeoutError`](exceptions.html#TimeoutError "TimeoutError").

*exception* asyncio.CancelledError
:   The operation has been cancelled.

    This exception can be caught to perform custom operations
    when asyncio Tasks are cancelled. In almost all situations the
    exception must be re-raised.

*exception* asyncio.InvalidStateError
:   Invalid internal state of [`Task`](asyncio-task.html#asyncio.Task "asyncio.Task") or [`Future`](asyncio-future.html#asyncio.Future "asyncio.Future").

    Can be raised in situations like setting a result value for a
    *Future* object that already has a result value set.

*exception* asyncio.SendfileNotAvailableError
:   The “sendfile” syscall is not available for the given
    socket or file type.

    A subclass of [`RuntimeError`](exceptions.html#RuntimeError "RuntimeError").

*exception* asyncio.IncompleteReadError
:   The requested read operation did not complete fully.

    Raised by the [asyncio stream APIs](asyncio-stream.html#asyncio-streams).

    This exception is a subclass of [`EOFError`](exceptions.html#EOFError "EOFError").

    expected
    :   The total number ([`int`](functions.html#int "int")) of expected bytes.

    partial
    :   A string of [`bytes`](stdtypes.html#bytes "bytes") read before the end of stream was reached.

*exception* asyncio.LimitOverrunError
:   Reached the buffer size limit while looking for a separator.

    Raised by the [asyncio stream APIs](asyncio-stream.html#asyncio-streams).

    consumed
    :   The total number of to be consumed bytes.