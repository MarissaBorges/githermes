`asyncio` — Asynchronous I/O
============================

---

asyncio is a library to write **concurrent** code using
the **async/await** syntax.

asyncio is used as a foundation for multiple Python asynchronous
frameworks that provide high-performance network and web-servers,
database connection libraries, distributed task queues, etc.

asyncio is often a perfect fit for IO-bound and high-level
**structured** network code.

asyncio provides a set of **high-level** APIs to:

Additionally, there are **low-level** APIs for
*library and framework developers* to:

asyncio REPL

You can experiment with an `asyncio` concurrent context in the [REPL](../glossary.html#term-REPL):

Copy

```
$ python -m asyncio
asyncio REPL ...
Use "await" directly instead of "asyncio.run()".
Type "help", "copyright", "credits" or "license" for more information.
>>> import asyncio
>>> await asyncio.sleep(10, result='hello')
'hello'

```

Raises an [auditing event](sys.html#auditing) `cpython.run_stdin` with no arguments.

Changed in version 3.12.5: (also 3.11.10, 3.10.15, 3.9.20, and 3.8.20)
Emits audit events.

Changed in version 3.13: Uses PyREPL if possible, in which case [`PYTHONSTARTUP`](../using/cmdline.html#envvar-PYTHONSTARTUP) is
also executed. Emits audit events.

Reference

Note

The source code for asyncio can be found in [Lib/asyncio/](https://github.com/python/cpython/tree/3.13/Lib/asyncio/).