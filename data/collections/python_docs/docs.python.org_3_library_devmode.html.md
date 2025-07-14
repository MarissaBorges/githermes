Python Development Mode
=======================

The Python Development Mode introduces additional runtime checks that are too
expensive to be enabled by default. It should not be more verbose than the
default if the code is correct; new warnings are only emitted when an issue is
detected.

It can be enabled using the [`-X dev`](../using/cmdline.html#cmdoption-X) command line option or by
setting the [`PYTHONDEVMODE`](../using/cmdline.html#envvar-PYTHONDEVMODE) environment variable to `1`.

See also [Python debug build](../using/configure.html#debug-build).

Effects of the Python Development Mode
--------------------------------------

Enabling the Python Development Mode is similar to the following command, but
with additional effects described below:

Copy

```
PYTHONMALLOC=debug PYTHONASYNCIODEBUG=1 python -W default -X faulthandler

```

Effects of the Python Development Mode:

* Add `default` [warning filter](warnings.html#describing-warning-filters). The
  following warnings are shown:

  Normally, the above warnings are filtered by the default [warning
  filters](warnings.html#describing-warning-filters).

  It behaves as if the [`-W default`](../using/cmdline.html#cmdoption-W) command line option is used.

  Use the [`-W error`](../using/cmdline.html#cmdoption-W) command line option or set the
  [`PYTHONWARNINGS`](../using/cmdline.html#envvar-PYTHONWARNINGS) environment variable to `error` to treat warnings
  as errors.
* Install debug hooks on memory allocators to check for:

  See the [`PyMem_SetupDebugHooks()`](../c-api/memory.html#c.PyMem_SetupDebugHooks "PyMem_SetupDebugHooks") C function.

  It behaves as if the [`PYTHONMALLOC`](../using/cmdline.html#envvar-PYTHONMALLOC) environment variable is set to
  `debug`.

  To enable the Python Development Mode without installing debug hooks on
  memory allocators, set the [`PYTHONMALLOC`](../using/cmdline.html#envvar-PYTHONMALLOC) environment variable to
  `default`.
* Call [`faulthandler.enable()`](faulthandler.html#faulthandler.enable "faulthandler.enable") at Python startup to install handlers for
  the [`SIGSEGV`](signal.html#signal.SIGSEGV "signal.SIGSEGV"), [`SIGFPE`](signal.html#signal.SIGFPE "signal.SIGFPE"),
  [`SIGABRT`](signal.html#signal.SIGABRT "signal.SIGABRT"), [`SIGBUS`](signal.html#signal.SIGBUS "signal.SIGBUS") and
  [`SIGILL`](signal.html#signal.SIGILL "signal.SIGILL") signals to dump the Python traceback on a crash.

  It behaves as if the [`-X faulthandler`](../using/cmdline.html#cmdoption-X) command line option is
  used or if the [`PYTHONFAULTHANDLER`](../using/cmdline.html#envvar-PYTHONFAULTHANDLER) environment variable is set to
  `1`.
* Enable [asyncio debug mode](asyncio-dev.html#asyncio-debug-mode). For example,
  [`asyncio`](asyncio.html#module-asyncio "asyncio: Asynchronous I/O.") checks for coroutines that were not awaited and logs them.

  It behaves as if the [`PYTHONASYNCIODEBUG`](../using/cmdline.html#envvar-PYTHONASYNCIODEBUG) environment variable is set
  to `1`.
* Check the *encoding* and *errors* arguments for string encoding and decoding
  operations. Examples: [`open()`](functions.html#open "open"), [`str.encode()`](stdtypes.html#str.encode "str.encode") and
  [`bytes.decode()`](stdtypes.html#bytes.decode "bytes.decode").

  By default, for best performance, the *errors* argument is only checked at
  the first encoding/decoding error and the *encoding* argument is sometimes
  ignored for empty strings.
* The [`io.IOBase`](io.html#io.IOBase "io.IOBase") destructor logs `close()` exceptions.
* Set the [`dev_mode`](sys.html#sys.flags.dev_mode "sys.flags.dev_mode") attribute of [`sys.flags`](sys.html#sys.flags "sys.flags") to
  `True`.

The Python Development Mode does not enable the [`tracemalloc`](tracemalloc.html#module-tracemalloc "tracemalloc: Trace memory allocations.") module by
default, because the overhead cost (to performance and memory) would be too
large. Enabling the [`tracemalloc`](tracemalloc.html#module-tracemalloc "tracemalloc: Trace memory allocations.") module provides additional information
on the origin of some errors. For example, [`ResourceWarning`](exceptions.html#ResourceWarning "ResourceWarning") logs the
traceback where the resource was allocated, and a buffer overflow error logs
the traceback where the memory block was allocated.

The Python Development Mode does not prevent the [`-O`](../using/cmdline.html#cmdoption-O) command line
option from removing [`assert`](../reference/simple_stmts.html#assert) statements nor from setting
[`__debug__`](constants.html#debug__ "__debug__") to `False`.

The Python Development Mode can only be enabled at the Python startup. Its
value can be read from [`sys.flags.dev_mode`](sys.html#sys.flags "sys.flags").

Changed in version 3.8: The [`io.IOBase`](io.html#io.IOBase "io.IOBase") destructor now logs `close()` exceptions.

Changed in version 3.9: The *encoding* and *errors* arguments are now checked for string encoding
and decoding operations.

ResourceWarning Example
-----------------------

Example of a script counting the number of lines of the text file specified in
the command line:

Copy

```
import sys

def main():
    fp = open(sys.argv[1])
    nlines = len(fp.readlines())
    print(nlines)
    # The file is closed implicitly

if __name__ == "__main__":
    main()

```

The script does not close the file explicitly. By default, Python does not emit
any warning. Example using README.txt, which has 269 lines:

```
$ python script.py README.txt
269

```

Enabling the Python Development Mode displays a [`ResourceWarning`](exceptions.html#ResourceWarning "ResourceWarning") warning:

```
$ python -X dev script.py README.txt
269
script.py:10: ResourceWarning: unclosed file <_io.TextIOWrapper name='README.rst' mode='r' encoding='UTF-8'>
  main()
ResourceWarning: Enable tracemalloc to get the object allocation traceback

```

In addition, enabling [`tracemalloc`](tracemalloc.html#module-tracemalloc "tracemalloc: Trace memory allocations.") shows the line where the file was
opened:

```
$ python -X dev -X tracemalloc=5 script.py README.rst
269
script.py:10: ResourceWarning: unclosed file <_io.TextIOWrapper name='README.rst' mode='r' encoding='UTF-8'>
  main()
Object allocated at (most recent call last):
  File "script.py", lineno 10
    main()
  File "script.py", lineno 4
    fp = open(sys.argv[1])

```

The fix is to close explicitly the file. Example using a context manager:

Copy

```
def main():
    # Close the file explicitly when exiting the with block
    with open(sys.argv[1]) as fp:
        nlines = len(fp.readlines())
    print(nlines)

```

Not closing a resource explicitly can leave a resource open for way longer than
expected; it can cause severe issues upon exiting Python. It is bad in
CPython, but it is even worse in PyPy. Closing resources explicitly makes an
application more deterministic and more reliable.

Bad file descriptor error example
---------------------------------

Script displaying the first line of itself:

Copy

```
import os

def main():
    fp = open(__file__)
    firstline = fp.readline()
    print(firstline.rstrip())
    os.close(fp.fileno())
    # The file is closed implicitly

main()

```

By default, Python does not emit any warning:

```
$ python script.py
import os

```

The Python Development Mode shows a [`ResourceWarning`](exceptions.html#ResourceWarning "ResourceWarning") and logs a “Bad file
descriptor” error when finalizing the file object:

```
$ python -X dev script.py
import os
script.py:10: ResourceWarning: unclosed file <_io.TextIOWrapper name='script.py' mode='r' encoding='UTF-8'>
  main()
ResourceWarning: Enable tracemalloc to get the object allocation traceback
Exception ignored in: <_io.TextIOWrapper name='script.py' mode='r' encoding='UTF-8'>
Traceback (most recent call last):
  File "script.py", line 10, in <module>
    main()
OSError: [Errno 9] Bad file descriptor

```

`os.close(fp.fileno())` closes the file descriptor. When the file object
finalizer tries to close the file descriptor again, it fails with the `Bad
file descriptor` error. A file descriptor must be closed only once. In the
worst case scenario, closing it twice can lead to a crash (see [bpo-18748](https://bugs.python.org/issue?@action=redirect&bpo=18748)
for an example).

The fix is to remove the `os.close(fp.fileno())` line, or open the file with
`closefd=False`.