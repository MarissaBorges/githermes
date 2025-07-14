:   Spawn a process, and connect its controlling terminal with the current
    process’s standard io. This is often used to baffle programs which insist on
    reading from the controlling terminal. It is expected that the process
    spawned behind the pty will eventually terminate, and when it does *spawn*
    will return.

    A loop copies STDIN of the current process to the child and data received
    from the child to STDOUT of the current process. It is not signaled to the
    child if STDIN of the current process closes down.

    The functions *master\_read* and *stdin\_read* are passed a file descriptor
    which they should read from, and they should always return a byte string. In
    order to force spawn to return before the child process exits an
    empty byte array should be returned to signal end of file.

    The default implementation for both functions will read and return up to 1024
    bytes each time the function is called. The *master\_read* callback is passed
    the pseudoterminal’s master file descriptor to read output from the child
    process, and *stdin\_read* is passed file descriptor 0, to read from the
    parent process’s standard input.

    Returning an empty byte string from either callback is interpreted as an
    end-of-file (EOF) condition, and that callback will not be called after
    that. If *stdin\_read* signals EOF the controlling terminal can no longer
    communicate with the parent process OR the child process. Unless the child
    process will quit without any input, *spawn* will then loop forever. If
    *master\_read* signals EOF the same behavior results (on linux at least).

    Return the exit status value from [`os.waitpid()`](os.html#os.waitpid "os.waitpid") on the child process.

    [`os.waitstatus_to_exitcode()`](os.html#os.waitstatus_to_exitcode "os.waitstatus_to_exitcode") can be used to convert the exit status into
    an exit code.

    Raises an [auditing event](sys.html#auditing) `pty.spawn` with argument `argv`.

    Changed in version 3.4: [`spawn()`](#pty.spawn "pty.spawn") now returns the status value from [`os.waitpid()`](os.html#os.waitpid "os.waitpid")
    on the child process.