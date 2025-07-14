Subprocesses
============

**Source code:** [Lib/asyncio/subprocess.py](https://github.com/python/cpython/tree/3.13/Lib/asyncio/subprocess.py),
[Lib/asyncio/base\_subprocess.py](https://github.com/python/cpython/tree/3.13/Lib/asyncio/base_subprocess.py)

---

This section describes high-level async/await asyncio APIs to
create and manage subprocesses.

Here’s an example of how asyncio can run a shell command and
obtain its result:

Copy

```
import asyncio

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')

asyncio.run(run('ls /zzz'))

```

will print:

Copy

```
['ls /zzz' exited with 1]
[stderr]
ls: /zzz: No such file or directory

```

Because all asyncio subprocess functions are asynchronous and asyncio
provides many tools to work with such functions, it is easy to execute
and monitor multiple subprocesses in parallel. It is indeed trivial
to modify the above example to run several commands simultaneously:

Copy

```
async def main():
    await asyncio.gather(
        run('ls /zzz'),
        run('sleep 1; echo "hello"'))

asyncio.run(main())

```

See also the [Examples](#examples) subsection.

Creating Subprocesses
---------------------

*async* asyncio.create\_subprocess\_exec(*program*, *\*args*, *stdin=None*, *stdout=None*, *stderr=None*, *limit=None*, *\*\*kwds*)
:   Create a subprocess.

    The *limit* argument sets the buffer limit for [`StreamReader`](asyncio-stream.html#asyncio.StreamReader "asyncio.StreamReader")
    wrappers for [`stdout`](#asyncio.subprocess.Process.stdout "asyncio.subprocess.Process.stdout") and [`stderr`](#asyncio.subprocess.Process.stderr "asyncio.subprocess.Process.stderr")
    (if [`subprocess.PIPE`](subprocess.html#subprocess.PIPE "subprocess.PIPE") is passed to *stdout* and *stderr* arguments).

    Return a [`Process`](#asyncio.subprocess.Process "asyncio.subprocess.Process") instance.

    See the documentation of [`loop.subprocess_exec()`](asyncio-eventloop.html#asyncio.loop.subprocess_exec "asyncio.loop.subprocess_exec") for other
    parameters.

    Changed in version 3.10: Removed the *loop* parameter.

*async* asyncio.create\_subprocess\_shell(*cmd*, *stdin=None*, *stdout=None*, *stderr=None*, *limit=None*, *\*\*kwds*)
:   Run the *cmd* shell command.

    The *limit* argument sets the buffer limit for [`StreamReader`](asyncio-stream.html#asyncio.StreamReader "asyncio.StreamReader")
    wrappers for [`stdout`](#asyncio.subprocess.Process.stdout "asyncio.subprocess.Process.stdout") and [`stderr`](#asyncio.subprocess.Process.stderr "asyncio.subprocess.Process.stderr")
    (if [`subprocess.PIPE`](subprocess.html#subprocess.PIPE "subprocess.PIPE") is passed to *stdout* and *stderr* arguments).

    Return a [`Process`](#asyncio.subprocess.Process "asyncio.subprocess.Process") instance.

    See the documentation of [`loop.subprocess_shell()`](asyncio-eventloop.html#asyncio.loop.subprocess_shell "asyncio.loop.subprocess_shell") for other
    parameters.

    Important

    It is the application’s responsibility to ensure that all whitespace and
    special characters are quoted appropriately to avoid [shell injection](https://en.wikipedia.org/wiki/Shell_injection#Shell_injection)
    vulnerabilities. The [`shlex.quote()`](shlex.html#shlex.quote "shlex.quote") function can be used to properly
    escape whitespace and special shell characters in strings that are going
    to be used to construct shell commands.

    Changed in version 3.10: Removed the *loop* parameter.

Constants
---------

asyncio.subprocess.PIPE
:   Can be passed to the *stdin*, *stdout* or *stderr* parameters.

    If *PIPE* is passed to *stdin* argument, the
    [`Process.stdin`](#asyncio.subprocess.Process.stdin "asyncio.subprocess.Process.stdin") attribute
    will point to a [`StreamWriter`](asyncio-stream.html#asyncio.StreamWriter "asyncio.StreamWriter") instance.

    If *PIPE* is passed to *stdout* or *stderr* arguments, the
    [`Process.stdout`](#asyncio.subprocess.Process.stdout "asyncio.subprocess.Process.stdout") and
    [`Process.stderr`](#asyncio.subprocess.Process.stderr "asyncio.subprocess.Process.stderr")
    attributes will point to [`StreamReader`](asyncio-stream.html#asyncio.StreamReader "asyncio.StreamReader") instances.

asyncio.subprocess.STDOUT
:   Special value that can be used as the *stderr* argument and indicates
    that standard error should be redirected into standard output.

asyncio.subprocess.DEVNULL
:   Special value that can be used as the *stdin*, *stdout* or *stderr* argument
    to process creation functions. It indicates that the special file
    [`os.devnull`](os.html#os.devnull "os.devnull") will be used for the corresponding subprocess stream.

Interacting with Subprocesses
-----------------------------

Both [`create_subprocess_exec()`](#asyncio.create_subprocess_exec "asyncio.create_subprocess_exec") and [`create_subprocess_shell()`](#asyncio.create_subprocess_shell "asyncio.create_subprocess_shell")
functions return instances of the *Process* class. *Process* is a high-level
wrapper that allows communicating with subprocesses and watching for
their completion.

*class* asyncio.subprocess.Process
:   An object that wraps OS processes created by the
    [`create_subprocess_exec()`](#asyncio.create_subprocess_exec "asyncio.create_subprocess_exec") and [`create_subprocess_shell()`](#asyncio.create_subprocess_shell "asyncio.create_subprocess_shell")
    functions.

    This class is designed to have a similar API to the
    [`subprocess.Popen`](subprocess.html#subprocess.Popen "subprocess.Popen") class, but there are some
    notable differences:

    This class is [not thread safe](asyncio-dev.html#asyncio-multithreading).

    See also the [Subprocess and Threads](#asyncio-subprocess-threads)
    section.

    *async* wait()
    :   Wait for the child process to terminate.

        Set and return the [`returncode`](#asyncio.subprocess.Process.returncode "asyncio.subprocess.Process.returncode") attribute.

        Note

        This method can deadlock when using `stdout=PIPE` or
        `stderr=PIPE` and the child process generates so much output
        that it blocks waiting for the OS pipe buffer to accept
        more data. Use the [`communicate()`](#asyncio.subprocess.Process.communicate "asyncio.subprocess.Process.communicate") method when using pipes
        to avoid this condition.

    *async* communicate(*input=None*)
    :   Interact with process:

        1. send data to *stdin* (if *input* is not `None`);
        2. closes *stdin*;
        3. read data from *stdout* and *stderr*, until EOF is reached;
        4. wait for process to terminate.

        The optional *input* argument is the data ([`bytes`](stdtypes.html#bytes "bytes") object)
        that will be sent to the child process.

        Return a tuple `(stdout_data, stderr_data)`.

        If either [`BrokenPipeError`](exceptions.html#BrokenPipeError "BrokenPipeError") or [`ConnectionResetError`](exceptions.html#ConnectionResetError "ConnectionResetError")
        exception is raised when writing *input* into *stdin*, the
        exception is ignored. This condition occurs when the process
        exits before all data are written into *stdin*.

        If it is desired to send data to the process’ *stdin*,
        the process needs to be created with `stdin=PIPE`. Similarly,
        to get anything other than `None` in the result tuple, the
        process has to be created with `stdout=PIPE` and/or
        `stderr=PIPE` arguments.

        Note, that the data read is buffered in memory, so do not use
        this method if the data size is large or unlimited.

        Changed in version 3.12: *stdin* gets closed when `input=None` too.

    send\_signal(*signal*)
    :   Sends the signal *signal* to the child process.

        Note

        On Windows, [`SIGTERM`](signal.html#signal.SIGTERM "signal.SIGTERM") is an alias for [`terminate()`](#asyncio.subprocess.Process.terminate "asyncio.subprocess.Process.terminate").
        `CTRL_C_EVENT` and `CTRL_BREAK_EVENT` can be sent to processes
        started with a *creationflags* parameter which includes
        `CREATE_NEW_PROCESS_GROUP`.

    terminate()
    :   Stop the child process.

        On POSIX systems this method sends [`SIGTERM`](signal.html#signal.SIGTERM "signal.SIGTERM") to the
        child process.

        On Windows the Win32 API function `TerminateProcess()` is
        called to stop the child process.

    kill()
    :   Kill the child process.

        On POSIX systems this method sends [`SIGKILL`](signal.html#signal.SIGKILL "signal.SIGKILL") to the child
        process.

        On Windows this method is an alias for [`terminate()`](#asyncio.subprocess.Process.terminate "asyncio.subprocess.Process.terminate").

    stdin
    :   Standard input stream ([`StreamWriter`](asyncio-stream.html#asyncio.StreamWriter "asyncio.StreamWriter")) or `None`
        if the process was created with `stdin=None`.

    stdout
    :   Standard output stream ([`StreamReader`](asyncio-stream.html#asyncio.StreamReader "asyncio.StreamReader")) or `None`
        if the process was created with `stdout=None`.

    stderr
    :   Standard error stream ([`StreamReader`](asyncio-stream.html#asyncio.StreamReader "asyncio.StreamReader")) or `None`
        if the process was created with `stderr=None`.

    pid
    :   Process identification number (PID).

        Note that for processes created by the [`create_subprocess_shell()`](#asyncio.create_subprocess_shell "asyncio.create_subprocess_shell")
        function, this attribute is the PID of the spawned shell.

    returncode
    :   Return code of the process when it exits.

        A `None` value indicates that the process has not terminated yet.

        A negative value `-N` indicates that the child was terminated
        by signal `N` (POSIX only).

### Subprocess and Threads

Standard asyncio event loop supports running subprocesses from different threads by
default.

On Windows subprocesses are provided by [`ProactorEventLoop`](asyncio-eventloop.html#asyncio.ProactorEventLoop "asyncio.ProactorEventLoop") only (default),
[`SelectorEventLoop`](asyncio-eventloop.html#asyncio.SelectorEventLoop "asyncio.SelectorEventLoop") has no subprocess support.

On UNIX *child watchers* are used for subprocess finish waiting, see
[Process Watchers](asyncio-policy.html#asyncio-watchers) for more info.

Changed in version 3.8: UNIX switched to use [`ThreadedChildWatcher`](asyncio-policy.html#asyncio.ThreadedChildWatcher "asyncio.ThreadedChildWatcher") for spawning subprocesses from
different threads without any limitation.

Spawning a subprocess with *inactive* current child watcher raises
[`RuntimeError`](exceptions.html#RuntimeError "RuntimeError").

Note that alternative event loop implementations might have own limitations;
please refer to their documentation.

### Examples

An example using the [`Process`](#asyncio.subprocess.Process "asyncio.subprocess.Process") class to
control a subprocess and the [`StreamReader`](asyncio-stream.html#asyncio.StreamReader "asyncio.StreamReader") class to read from
its standard output.

The subprocess is created by the [`create_subprocess_exec()`](#asyncio.create_subprocess_exec "asyncio.create_subprocess_exec")
function:

Copy

```
import asyncio
import sys

async def get_date():
    code = 'import datetime; print(datetime.datetime.now())'

    # Create the subprocess; redirect the standard output
    # into a pipe.
    proc = await asyncio.create_subprocess_exec(
        sys.executable, '-c', code,
        stdout=asyncio.subprocess.PIPE)

    # Read one line of output.
    data = await proc.stdout.readline()
    line = data.decode('ascii').rstrip()

    # Wait for the subprocess exit.
    await proc.wait()
    return line

date = asyncio.run(get_date())
print(f"Current date: {date}")

```

See also the [same example](asyncio-protocol.html#asyncio-example-subprocess-proto)
written using low-level APIs.