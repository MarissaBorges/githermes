Operating System Utilities
==========================

[PyObject](structures.html#c.PyObject "PyObject") \*PyOS\_FSPath([PyObject](structures.html#c.PyObject "PyObject") \*path)
:   *Return value: New reference.* *Part of the [Stable ABI](stable.html#stable) since version 3.6.*

    Return the file system representation for *path*. If the object is a
    [`str`](../library/stdtypes.html#str "str") or [`bytes`](../library/stdtypes.html#bytes "bytes") object, then a new
    [strong reference](../glossary.html#term-strong-reference) is returned.
    If the object implements the [`os.PathLike`](../library/os.html#os.PathLike "os.PathLike") interface,
    then [`__fspath__()`](../library/os.html#os.PathLike.__fspath__ "os.PathLike.__fspath__") is returned as long as it is a
    [`str`](../library/stdtypes.html#str "str") or [`bytes`](../library/stdtypes.html#bytes "bytes") object. Otherwise [`TypeError`](../library/exceptions.html#TypeError "TypeError") is raised
    and `NULL` is returned.

int Py\_FdIsInteractive(FILE \*fp, const char \*filename)
:   Return true (nonzero) if the standard I/O file *fp* with name *filename* is
    deemed interactive. This is the case for files for which `isatty(fileno(fp))`
    is true. If the [`PyConfig.interactive`](init_config.html#c.PyConfig.interactive "PyConfig.interactive") is non-zero, this function
    also returns true if the *filename* pointer is `NULL` or if the name is equal to
    one of the strings `'<stdin>'` or `'???'`.

    This function must not be called before Python is initialized.

void PyOS\_BeforeFork()
:   *Part of the [Stable ABI](stable.html#stable) on platforms with fork() since version 3.7.*

    Function to prepare some internal state before a process fork. This
    should be called before calling `fork()` or any similar function
    that clones the current process.
    Only available on systems where `fork()` is defined.

void PyOS\_AfterFork\_Parent()
:   *Part of the [Stable ABI](stable.html#stable) on platforms with fork() since version 3.7.*

    Function to update some internal state after a process fork. This
    should be called from the parent process after calling `fork()`
    or any similar function that clones the current process, regardless
    of whether process cloning was successful.
    Only available on systems where `fork()` is defined.

void PyOS\_AfterFork\_Child()
:   *Part of the [Stable ABI](stable.html#stable) on platforms with fork() since version 3.7.*

    Function to update internal interpreter state after a process fork.
    This must be called from the child process after calling `fork()`,
    or any similar function that clones the current process, if there is
    any chance the process will call back into the Python interpreter.
    Only available on systems where `fork()` is defined.

void PyOS\_AfterFork()
:   *Part of the [Stable ABI](stable.html#stable) on platforms with fork().*

    Function to update some internal state after a process fork; this should be
    called in the new process if the Python interpreter will continue to be used.
    If a new executable is loaded into the new process, this function does not need
    to be called.

int PyOS\_CheckStack()
:   *Part of the [Stable ABI](stable.html#stable) on platforms with USE\_STACKCHECK since version 3.7.*

    Return true when the interpreter runs out of stack space. This is a reliable
    check, but is only available when `USE_STACKCHECK` is defined (currently
    on certain versions of Windows using the Microsoft Visual C++ compiler).
    `USE_STACKCHECK` will be defined automatically; you should never
    change the definition in your own code.

typedef void (\*PyOS\_sighandler\_t)(int)
:   *Part of the [Stable ABI](stable.html#stable).*

[PyOS\_sighandler\_t](#c.PyOS_sighandler_t "PyOS_sighandler_t") PyOS\_getsig(int i)
:   *Part of the [Stable ABI](stable.html#stable).*

    Return the current signal handler for signal *i*. This is a thin wrapper around
    either `sigaction()` or `signal()`. Do not call those functions
    directly!

[PyOS\_sighandler\_t](#c.PyOS_sighandler_t "PyOS_sighandler_t") PyOS\_setsig(int i, [PyOS\_sighandler\_t](#c.PyOS_sighandler_t "PyOS_sighandler_t") h)
:   *Part of the [Stable ABI](stable.html#stable).*

    Set the signal handler for signal *i* to be *h*; return the old signal handler.
    This is a thin wrapper around either `sigaction()` or `signal()`. Do
    not call those functions directly!

wchar\_t \*Py\_DecodeLocale(const char \*arg, size\_t \*size)
:   *Part of the [Stable ABI](stable.html#stable) since version 3.7.*

    Decode a byte string from the [filesystem encoding and error handler](../glossary.html#term-filesystem-encoding-and-error-handler).
    If the error handler is [surrogateescape error handler](../library/codecs.html#surrogateescape), undecodable bytes are decoded as characters in range
    U+DC80..U+DCFF; and if a byte sequence can be decoded as a surrogate
    character, the bytes are escaped using the surrogateescape error handler
    instead of decoding them.

    Return a pointer to a newly allocated wide character string, use
    [`PyMem_RawFree()`](memory.html#c.PyMem_RawFree "PyMem_RawFree") to free the memory. If size is not `NULL`, write
    the number of wide characters excluding the null character into `*size`

    Return `NULL` on decoding error or memory allocation error. If *size* is
    not `NULL`, `*size` is set to `(size_t)-1` on memory error or set to
    `(size_t)-2` on decoding error.

    The [filesystem encoding and error handler](../glossary.html#term-filesystem-encoding-and-error-handler) are selected by
    [`PyConfig_Read()`](init_config.html#c.PyConfig_Read "PyConfig_Read"): see [`filesystem_encoding`](init_config.html#c.PyConfig.filesystem_encoding "PyConfig.filesystem_encoding") and
    [`filesystem_errors`](init_config.html#c.PyConfig.filesystem_errors "PyConfig.filesystem_errors") members of [`PyConfig`](init_config.html#c.PyConfig "PyConfig").

    Decoding errors should never happen, unless there is a bug in the C
    library.

    Use the [`Py_EncodeLocale()`](#c.Py_EncodeLocale "Py_EncodeLocale") function to encode the character string
    back to a byte string.

    Changed in version 3.7: The function now uses the UTF-8 encoding in the [Python UTF-8 Mode](../library/os.html#utf8-mode).

char \*Py\_EncodeLocale(const wchar\_t \*text, size\_t \*error\_pos)
:   *Part of the [Stable ABI](stable.html#stable) since version 3.7.*

    Encode a wide character string to the [filesystem encoding and error
    handler](../glossary.html#term-filesystem-encoding-and-error-handler). If the error handler is [surrogateescape error handler](../library/codecs.html#surrogateescape), surrogate characters in the range U+DC80..U+DCFF are
    converted to bytes 0x80..0xFF.

    Return a pointer to a newly allocated byte string, use [`PyMem_Free()`](memory.html#c.PyMem_Free "PyMem_Free")
    to free the memory. Return `NULL` on encoding error or memory allocation
    error.

    If error\_pos is not `NULL`, `*error_pos` is set to `(size_t)-1` on
    success, or set to the index of the invalid character on encoding error.

    The [filesystem encoding and error handler](../glossary.html#term-filesystem-encoding-and-error-handler) are selected by
    [`PyConfig_Read()`](init_config.html#c.PyConfig_Read "PyConfig_Read"): see [`filesystem_encoding`](init_config.html#c.PyConfig.filesystem_encoding "PyConfig.filesystem_encoding") and
    [`filesystem_errors`](init_config.html#c.PyConfig.filesystem_errors "PyConfig.filesystem_errors") members of [`PyConfig`](init_config.html#c.PyConfig "PyConfig").

    Use the [`Py_DecodeLocale()`](#c.Py_DecodeLocale "Py_DecodeLocale") function to decode the bytes string back
    to a wide character string.

    Changed in version 3.7: The function now uses the UTF-8 encoding in the [Python UTF-8 Mode](../library/os.html#utf8-mode).

System Functions
================

These are utility functions that make functionality from the [`sys`](../library/sys.html#module-sys "sys: Access system-specific parameters and functions.") module
accessible to C code. They all work with the current interpreter thread’s
[`sys`](../library/sys.html#module-sys "sys: Access system-specific parameters and functions.") module’s dict, which is contained in the internal thread state structure.

[PyObject](structures.html#c.PyObject "PyObject") \*PySys\_GetObject(const char \*name)
:   *Return value: Borrowed reference.* *Part of the [Stable ABI](stable.html#stable).*

    Return the object *name* from the [`sys`](../library/sys.html#module-sys "sys: Access system-specific parameters and functions.") module or `NULL` if it does
    not exist, without setting an exception.

int PySys\_SetObject(const char \*name, [PyObject](structures.html#c.PyObject "PyObject") \*v)
:   *Part of the [Stable ABI](stable.html#stable).*

    Set *name* in the [`sys`](../library/sys.html#module-sys "sys: Access system-specific parameters and functions.") module to *v* unless *v* is `NULL`, in which
    case *name* is deleted from the sys module. Returns `0` on success, `-1`
    on error.

void PySys\_ResetWarnOptions()
:   *Part of the [Stable ABI](stable.html#stable).*

    Reset [`sys.warnoptions`](../library/sys.html#sys.warnoptions "sys.warnoptions") to an empty list. This function may be
    called prior to [`Py_Initialize()`](init.html#c.Py_Initialize "Py_Initialize").

    Deprecated since version 3.13, will be removed in version 3.15: Clear [`sys.warnoptions`](../library/sys.html#sys.warnoptions "sys.warnoptions") and `warnings.filters` instead.

void PySys\_WriteStdout(const char \*format, ...)
:   *Part of the [Stable ABI](stable.html#stable).*

    Write the output string described by *format* to [`sys.stdout`](../library/sys.html#sys.stdout "sys.stdout"). No
    exceptions are raised, even if truncation occurs (see below).

    *format* should limit the total size of the formatted output string to
    1000 bytes or less – after 1000 bytes, the output string is truncated.
    In particular, this means that no unrestricted “%s” formats should occur;
    these should be limited using “%.<N>s” where <N> is a decimal number
    calculated so that <N> plus the maximum size of other formatted text does not
    exceed 1000 bytes. Also watch out for “%f”, which can print hundreds of
    digits for very large numbers.

    If a problem occurs, or [`sys.stdout`](../library/sys.html#sys.stdout "sys.stdout") is unset, the formatted message
    is written to the real (C level) *stdout*.

void PySys\_WriteStderr(const char \*format, ...)
:   *Part of the [Stable ABI](stable.html#stable).*

    As [`PySys_WriteStdout()`](#c.PySys_WriteStdout "PySys_WriteStdout"), but write to [`sys.stderr`](../library/sys.html#sys.stderr "sys.stderr") or *stderr*
    instead.

void PySys\_FormatStdout(const char \*format, ...)
:   *Part of the [Stable ABI](stable.html#stable).*

    Function similar to PySys\_WriteStdout() but format the message using
    [`PyUnicode_FromFormatV()`](unicode.html#c.PyUnicode_FromFormatV "PyUnicode_FromFormatV") and don’t truncate the message to an
    arbitrary length.

void PySys\_FormatStderr(const char \*format, ...)
:   *Part of the [Stable ABI](stable.html#stable).*

    As [`PySys_FormatStdout()`](#c.PySys_FormatStdout "PySys_FormatStdout"), but write to [`sys.stderr`](../library/sys.html#sys.stderr "sys.stderr") or *stderr*
    instead.

[PyObject](structures.html#c.PyObject "PyObject") \*PySys\_GetXOptions()
:   *Return value: Borrowed reference.* *Part of the [Stable ABI](stable.html#stable) since version 3.7.*

    Return the current dictionary of [`-X`](../using/cmdline.html#cmdoption-X) options, similarly to
    [`sys._xoptions`](../library/sys.html#sys._xoptions "sys._xoptions"). On error, `NULL` is returned and an exception is
    set.

int PySys\_Audit(const char \*event, const char \*format, ...)
:   *Part of the [Stable ABI](stable.html#stable) since version 3.13.*

    Raise an auditing event with any active hooks. Return zero for success
    and non-zero with an exception set on failure.

    The *event* string argument must not be *NULL*.

    If any hooks have been added, *format* and other arguments will be used
    to construct a tuple to pass. Apart from `N`, the same format characters
    as used in [`Py_BuildValue()`](arg.html#c.Py_BuildValue "Py_BuildValue") are available. If the built value is not
    a tuple, it will be added into a single-element tuple.

    The `N` format option must not be used. It consumes a reference, but since
    there is no way to know whether arguments to this function will be consumed,
    using it may cause reference leaks.

    Note that `#` format characters should always be treated as
    [`Py_ssize_t`](intro.html#c.Py_ssize_t "Py_ssize_t"), regardless of whether `PY_SSIZE_T_CLEAN` was defined.

    [`sys.audit()`](../library/sys.html#sys.audit "sys.audit") performs the same function from Python code.

    See also [`PySys_AuditTuple()`](#c.PySys_AuditTuple "PySys_AuditTuple").

    Changed in version 3.8.2: Require [`Py_ssize_t`](intro.html#c.Py_ssize_t "Py_ssize_t") for `#` format characters. Previously, an
    unavoidable deprecation warning was raised.

int PySys\_AuditTuple(const char \*event, [PyObject](structures.html#c.PyObject "PyObject") \*args)
:   *Part of the [Stable ABI](stable.html#stable) since version 3.13.*

    Similar to [`PySys_Audit()`](#c.PySys_Audit "PySys_Audit"), but pass arguments as a Python object.
    *args* must be a [`tuple`](../library/stdtypes.html#tuple "tuple"). To pass no arguments, *args* can be *NULL*.

int PySys\_AddAuditHook([Py\_AuditHookFunction](#c.Py_AuditHookFunction "Py_AuditHookFunction") hook, void \*userData)
:   Append the callable *hook* to the list of active auditing hooks.
    Return zero on success
    and non-zero on failure. If the runtime has been initialized, also set an
    error on failure. Hooks added through this API are called for all
    interpreters created by the runtime.

    The *userData* pointer is passed into the hook function. Since hook
    functions may be called from different runtimes, this pointer should not
    refer directly to Python state.

    This function is safe to call before [`Py_Initialize()`](init.html#c.Py_Initialize "Py_Initialize"). When called
    after runtime initialization, existing audit hooks are notified and may
    silently abort the operation by raising an error subclassed from
    [`Exception`](../library/exceptions.html#Exception "Exception") (other errors will not be silenced).

    The hook function is always called with the GIL held by the Python
    interpreter that raised the event.

    See [**PEP 578**](https://peps.python.org/pep-0578/) for a detailed description of auditing. Functions in the
    runtime and standard library that raise events are listed in the
    [audit events table](../library/audit_events.html#audit-events).
    Details are in each function’s documentation.

    If the interpreter is initialized, this function raises an auditing event
    `sys.addaudithook` with no arguments. If any existing hooks raise an
    exception derived from [`Exception`](../library/exceptions.html#Exception "Exception"), the new hook will not be
    added and the exception is cleared. As a result, callers cannot assume
    that their hook has been added unless they control all existing hooks.

    typedef int (\*Py\_AuditHookFunction)(const char \*event, [PyObject](structures.html#c.PyObject "PyObject") \*args, void \*userData)
    :   The type of the hook function.
        *event* is the C string event argument passed to [`PySys_Audit()`](#c.PySys_Audit "PySys_Audit") or
        [`PySys_AuditTuple()`](#c.PySys_AuditTuple "PySys_AuditTuple").
        *args* is guaranteed to be a [`PyTupleObject`](tuple.html#c.PyTupleObject "PyTupleObject").
        *userData* is the argument passed to PySys\_AddAuditHook().

Process Control
===============

void Py\_FatalError(const char \*message)
:   *Part of the [Stable ABI](stable.html#stable).*

    Print a fatal error message and kill the process. No cleanup is performed.
    This function should only be invoked when a condition is detected that would
    make it dangerous to continue using the Python interpreter; e.g., when the
    object administration appears to be corrupted. On Unix, the standard C library
    function `abort()` is called which will attempt to produce a `core`
    file.

    The `Py_FatalError()` function is replaced with a macro which logs
    automatically the name of the current function, unless the
    `Py_LIMITED_API` macro is defined.

    Changed in version 3.9: Log the function name automatically.

void Py\_Exit(int status)
:   *Part of the [Stable ABI](stable.html#stable).*

    Exit the current process. This calls [`Py_FinalizeEx()`](init.html#c.Py_FinalizeEx "Py_FinalizeEx") and then calls the
    standard C library function `exit(status)`. If [`Py_FinalizeEx()`](init.html#c.Py_FinalizeEx "Py_FinalizeEx")
    indicates an error, the exit status is set to 120.

    Changed in version 3.6: Errors from finalization no longer ignored.

int Py\_AtExit(void (\*func)())
:   *Part of the [Stable ABI](stable.html#stable).*

    Register a cleanup function to be called by [`Py_FinalizeEx()`](init.html#c.Py_FinalizeEx "Py_FinalizeEx"). The cleanup
    function will be called with no arguments and should return no value. At most
    32 cleanup functions can be registered. When the registration is successful,
    [`Py_AtExit()`](#c.Py_AtExit "Py_AtExit") returns `0`; on failure, it returns `-1`. The cleanup
    function registered last is called first. Each cleanup function will be called
    at most once. Since Python’s internal finalization will have completed before
    the cleanup function, no Python APIs should be called by *func*.