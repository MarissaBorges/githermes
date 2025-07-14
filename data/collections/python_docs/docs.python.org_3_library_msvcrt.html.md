`msvcrt` — Useful routines from the MS VC++ runtime
===================================================

---

These functions provide access to some useful capabilities on Windows platforms.
Some higher-level modules use these functions to build the Windows
implementations of their services. For example, the [`getpass`](getpass.html#module-getpass "getpass: Portable reading of passwords and retrieval of the userid.") module uses
this in the implementation of the [`getpass()`](getpass.html#module-getpass "getpass: Portable reading of passwords and retrieval of the userid.") function.

Further documentation on these functions can be found in the Platform API
documentation.

The module implements both the normal and wide char variants of the console I/O
api. The normal API deals only with ASCII characters and is of limited use
for internationalized applications. The wide char API should be used where
ever possible.

Changed in version 3.3: Operations in this module now raise [`OSError`](exceptions.html#OSError "OSError") where [`IOError`](exceptions.html#IOError "IOError")
was raised.

File Operations
---------------

msvcrt.locking(*fd*, *mode*, *nbytes*)
:   Lock part of a file based on file descriptor *fd* from the C runtime. Raises
    [`OSError`](exceptions.html#OSError "OSError") on failure. The locked region of the file extends from the
    current file position for *nbytes* bytes, and may continue beyond the end of the
    file. *mode* must be one of the `LK_*` constants listed below. Multiple
    regions in a file may be locked at the same time, but may not overlap. Adjacent
    regions are not merged; they must be unlocked individually.

    Raises an [auditing event](sys.html#auditing) `msvcrt.locking` with arguments `fd`, `mode`, `nbytes`.

msvcrt.LK\_LOCK

msvcrt.LK\_RLCK
:   Locks the specified bytes. If the bytes cannot be locked, the program
    immediately tries again after 1 second. If, after 10 attempts, the bytes cannot
    be locked, [`OSError`](exceptions.html#OSError "OSError") is raised.

msvcrt.LK\_NBLCK

msvcrt.LK\_NBRLCK
:   Locks the specified bytes. If the bytes cannot be locked, [`OSError`](exceptions.html#OSError "OSError") is
    raised.

msvcrt.LK\_UNLCK
:   Unlocks the specified bytes, which must have been previously locked.

msvcrt.setmode(*fd*, *flags*)
:   Set the line-end translation mode for the file descriptor *fd*. To set it to
    text mode, *flags* should be [`os.O_TEXT`](os.html#os.O_TEXT "os.O_TEXT"); for binary, it should be
    [`os.O_BINARY`](os.html#os.O_BINARY "os.O_BINARY").

msvcrt.open\_osfhandle(*handle*, *flags*)
:   Create a C runtime file descriptor from the file handle *handle*. The *flags*
    parameter should be a bitwise OR of [`os.O_APPEND`](os.html#os.O_APPEND "os.O_APPEND"),
    [`os.O_RDONLY`](os.html#os.O_RDONLY "os.O_RDONLY"), [`os.O_TEXT`](os.html#os.O_TEXT "os.O_TEXT") and [`os.O_NOINHERIT`](os.html#os.O_NOINHERIT "os.O_NOINHERIT").
    The returned file descriptor may be used as a parameter
    to [`os.fdopen()`](os.html#os.fdopen "os.fdopen") to create a file object.

    The file descriptor is inheritable by default. Pass [`os.O_NOINHERIT`](os.html#os.O_NOINHERIT "os.O_NOINHERIT")
    flag to make it non inheritable.

    Raises an [auditing event](sys.html#auditing) `msvcrt.open_osfhandle` with arguments `handle`, `flags`.

msvcrt.get\_osfhandle(*fd*)
:   Return the file handle for the file descriptor *fd*. Raises [`OSError`](exceptions.html#OSError "OSError") if
    *fd* is not recognized.

    Raises an [auditing event](sys.html#auditing) `msvcrt.get_osfhandle` with argument `fd`.

Console I/O
-----------

msvcrt.kbhit()
:   Returns a nonzero value if a keypress is waiting to be read. Otherwise,
    return 0.

msvcrt.getch()
:   Read a keypress and return the resulting character as a byte string.
    Nothing is echoed to the console. This call will block if a keypress
    is not already available, but will not wait for `Enter` to be
    pressed. If the pressed key was a special function key, this will
    return `'\000'` or `'\xe0'`; the next call will return the keycode.
    The `Control`-`C` keypress cannot be read with this function.

msvcrt.getwch()
:   Wide char variant of [`getch()`](#msvcrt.getch "msvcrt.getch"), returning a Unicode value.

msvcrt.getche()
:   Similar to [`getch()`](#msvcrt.getch "msvcrt.getch"), but the keypress will be echoed if it represents a
    printable character.

msvcrt.getwche()
:   Wide char variant of [`getche()`](#msvcrt.getche "msvcrt.getche"), returning a Unicode value.

msvcrt.putch(*char*)
:   Print the byte string *char* to the console without buffering.

msvcrt.putwch(*unicode\_char*)
:   Wide char variant of [`putch()`](#msvcrt.putch "msvcrt.putch"), accepting a Unicode value.

msvcrt.ungetch(*char*)
:   Cause the byte string *char* to be “pushed back” into the console buffer;
    it will be the next character read by [`getch()`](#msvcrt.getch "msvcrt.getch") or [`getche()`](#msvcrt.getche "msvcrt.getche").

msvcrt.ungetwch(*unicode\_char*)
:   Wide char variant of [`ungetch()`](#msvcrt.ungetch "msvcrt.ungetch"), accepting a Unicode value.

Other Functions
---------------

msvcrt.heapmin()
:   Force the `malloc()` heap to clean itself up and return unused blocks to
    the operating system. On failure, this raises [`OSError`](exceptions.html#OSError "OSError").

msvcrt.set\_error\_mode(*mode*)
:   Changes the location where the C runtime writes an error message for an error
    that might end the program. *mode* must be one of the `OUT_*`
    constants listed below or [`REPORT_ERRMODE`](#msvcrt.REPORT_ERRMODE "msvcrt.REPORT_ERRMODE"). Returns the old setting
    or -1 if an error occurs. Only available in
    [debug build of Python](../using/configure.html#debug-build).

msvcrt.OUT\_TO\_DEFAULT
:   Error sink is determined by the app’s type. Only available in
    [debug build of Python](../using/configure.html#debug-build).

msvcrt.OUT\_TO\_STDERR
:   Error sink is a standard error. Only available in
    [debug build of Python](../using/configure.html#debug-build).

msvcrt.OUT\_TO\_MSGBOX
:   Error sink is a message box. Only available in
    [debug build of Python](../using/configure.html#debug-build).

msvcrt.REPORT\_ERRMODE
:   Report the current error mode value. Only available in
    [debug build of Python](../using/configure.html#debug-build).

msvcrt.CrtSetReportMode(*type*, *mode*)
:   Specifies the destination or destinations for a specific report type
    generated by `_CrtDbgReport()` in the MS VC++ runtime. *type* must be
    one of the `CRT_*` constants listed below. *mode* must be one of the
    `CRTDBG_*` constants listed below. Only available in
    [debug build of Python](../using/configure.html#debug-build).

msvcrt.CrtSetReportFile(*type*, *file*)
:   After you use [`CrtSetReportMode()`](#msvcrt.CrtSetReportMode "msvcrt.CrtSetReportMode") to specify [`CRTDBG_MODE_FILE`](#msvcrt.CRTDBG_MODE_FILE "msvcrt.CRTDBG_MODE_FILE"),
    you can specify the file handle to receive the message text. *type* must be
    one of the `CRT_*` constants listed below. *file* should be the file
    handle your want specified. Only available in
    [debug build of Python](../using/configure.html#debug-build).

msvcrt.CRT\_WARN
:   Warnings, messages, and information that doesn’t need immediate attention.

msvcrt.CRT\_ERROR
:   Errors, unrecoverable problems, and issues that require immediate attention.

msvcrt.CRT\_ASSERT
:   Assertion failures.

msvcrt.CRTDBG\_MODE\_DEBUG
:   Writes the message to the debugger’s output window.

msvcrt.CRTDBG\_MODE\_FILE
:   Writes the message to a user-supplied file handle. [`CrtSetReportFile()`](#msvcrt.CrtSetReportFile "msvcrt.CrtSetReportFile")
    should be called to define the specific file or stream to use as
    the destination.

msvcrt.CRTDBG\_MODE\_WNDW
:   Creates a message box to display the message along with the `Abort`,
    `Retry`, and `Ignore` buttons.

msvcrt.CRTDBG\_REPORT\_MODE
:   Returns current *mode* for the specified *type*.

msvcrt.CRT\_ASSEMBLY\_VERSION
:   The CRT Assembly version, from the `crtassem.h` header file.

msvcrt.VC\_ASSEMBLY\_PUBLICKEYTOKEN
:   The VC Assembly public key token, from the `crtassem.h` header file.

msvcrt.LIBRARIES\_ASSEMBLY\_NAME\_PREFIX
:   The Libraries Assembly name prefix, from the `crtassem.h` header file.