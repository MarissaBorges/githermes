:   Execute a child program in a new process. On POSIX, the class uses
    [`os.execvpe()`](os.html#os.execvpe "os.execvpe")-like behavior to execute the child program. On Windows,
    the class uses the Windows `CreateProcess()` function. The arguments to
    [`Popen`](#subprocess.Popen "subprocess.Popen") are as follows.

    *args* should be a sequence of program arguments or else a single string
    or [path-like object](../glossary.html#term-path-like-object).
    By default, the program to execute is the first item in *args* if *args* is
    a sequence. If *args* is a string, the interpretation is
    platform-dependent and described below. See the *shell* and *executable*
    arguments for additional differences from the default behavior. Unless
    otherwise stated, it is recommended to pass *args* as a sequence.

    Warning

    For maximum reliability, use a fully qualified path for the executable.
    To search for an unqualified name on `PATH`, use
    [`shutil.which()`](shutil.html#shutil.which "shutil.which"). On all platforms, passing [`sys.executable`](sys.html#sys.executable "sys.executable")
    is the recommended way to launch the current Python interpreter again,
    and use the `-m` command-line format to launch an installed module.

    Resolving the path of *executable* (or the first item of *args*) is
    platform dependent. For POSIX, see [`os.execvpe()`](os.html#os.execvpe "os.execvpe"), and note that
    when resolving or searching for the executable path, *cwd* overrides the
    current working directory and *env* can override the `PATH`
    environment variable. For Windows, see the documentation of the
    `lpApplicationName` and `lpCommandLine` parameters of WinAPI
    `CreateProcess`, and note that when resolving or searching for the
    executable path with `shell=False`, *cwd* does not override the
    current working directory and *env* cannot override the `PATH`
    environment variable. Using a full path avoids all of these variations.

    An example of passing some arguments to an external program
    as a sequence is:

    Copy

    ```
    Popen(["/usr/bin/git", "commit", "-m", "Fixes a bug."])

    ```

    On POSIX, if *args* is a string, the string is interpreted as the name or
    path of the program to execute. However, this can only be done if not
    passing arguments to the program.

    Note

    It may not be obvious how to break a shell command into a sequence of arguments,
    especially in complex cases. [`shlex.split()`](shlex.html#shlex.split "shlex.split") can illustrate how to
    determine the correct tokenization for *args*:

    Copy

    ```
    >>> import shlex, subprocess
    >>> command_line = input()
    /bin/vikings -input eggs.txt -output "spam spam.txt" -cmd "echo '$MONEY'"
    >>> args = shlex.split(command_line)
    >>> print(args)
    ['/bin/vikings', '-input', 'eggs.txt', '-output', 'spam spam.txt', '-cmd', "echo '$MONEY'"]
    >>> p = subprocess.Popen(args) # Success!

    ```

    Note in particular that options (such as *-input*) and arguments (such
    as *eggs.txt*) that are separated by whitespace in the shell go in separate
    list elements, while arguments that need quoting or backslash escaping when
    used in the shell (such as filenames containing spaces or the *echo* command
    shown above) are single list elements.

    On Windows, if *args* is a sequence, it will be converted to a string in a
    manner described in [Converting an argument sequence to a string on Windows](#converting-argument-sequence). This is because
    the underlying `CreateProcess()` operates on strings.

    Changed in version 3.6: *args* parameter accepts a [path-like object](../glossary.html#term-path-like-object) if *shell* is
    `False` and a sequence containing path-like objects on POSIX.

    Changed in version 3.8: *args* parameter accepts a [path-like object](../glossary.html#term-path-like-object) if *shell* is
    `False` and a sequence containing bytes and path-like objects
    on Windows.

    The *shell* argument (which defaults to `False`) specifies whether to use
    the shell as the program to execute. If *shell* is `True`, it is
    recommended to pass *args* as a string rather than as a sequence.

    On POSIX with `shell=True`, the shell defaults to `/bin/sh`. If
    *args* is a string, the string specifies the command
    to execute through the shell. This means that the string must be
    formatted exactly as it would be when typed at the shell prompt. This
    includes, for example, quoting or backslash escaping filenames with spaces in
    them. If *args* is a sequence, the first item specifies the command string, and
    any additional items will be treated as additional arguments to the shell
    itself. That is to say, [`Popen`](#subprocess.Popen "subprocess.Popen") does the equivalent of:

    Copy

    ```
    Popen(['/bin/sh', '-c', args[0], args[1], ...])

    ```

    On Windows with `shell=True`, the `COMSPEC` environment variable
    specifies the default shell. The only time you need to specify
    `shell=True` on Windows is when the command you wish to execute is built
    into the shell (e.g. **dir** or **copy**). You do not need
    `shell=True` to run a batch file or console-based executable.

    *bufsize* will be supplied as the corresponding argument to the
    [`open()`](functions.html#open "open") function when creating the stdin/stdout/stderr pipe
    file objects:

    * `0` means unbuffered (read and write are one
      system call and can return short)
    * `1` means line buffered
      (only usable if `text=True` or `universal_newlines=True`)
    * any other positive value means use a buffer of approximately that
      size
    * negative bufsize (the default) means the system default of
      io.DEFAULT\_BUFFER\_SIZE will be used.

    Changed in version 3.3.1: *bufsize* now defaults to -1 to enable buffering by default to match the
    behavior that most code expects. In versions prior to Python 3.2.4 and
    3.3.1 it incorrectly defaulted to `0` which was unbuffered
    and allowed short reads. This was unintentional and did not match the
    behavior of Python 2 as most code expected.

    The *executable* argument specifies a replacement program to execute. It
    is very seldom needed. When `shell=False`, *executable* replaces the
    program to execute specified by *args*. However, the original *args* is
    still passed to the program. Most programs treat the program specified
    by *args* as the command name, which can then be different from the program
    actually executed. On POSIX, the *args* name
    becomes the display name for the executable in utilities such as
    **ps**. If `shell=True`, on POSIX the *executable* argument
    specifies a replacement shell for the default `/bin/sh`.

    Changed in version 3.6: *executable* parameter accepts a [path-like object](../glossary.html#term-path-like-object) on POSIX.

    Changed in version 3.8: *executable* parameter accepts a bytes and [path-like object](../glossary.html#term-path-like-object)
    on Windows.

    Changed in version 3.12: Changed Windows shell search order for `shell=True`. The current
    directory and `%PATH%` are replaced with `%COMSPEC%` and
    `%SystemRoot%\System32\cmd.exe`. As a result, dropping a
    malicious program named `cmd.exe` into a current directory no
    longer works.

    *stdin*, *stdout* and *stderr* specify the executed program’s standard input,
    standard output and standard error file handles, respectively. Valid values
    are `None`, [`PIPE`](#subprocess.PIPE "subprocess.PIPE"), [`DEVNULL`](#subprocess.DEVNULL "subprocess.DEVNULL"), an existing file descriptor (a
    positive integer), and an existing [file object](../glossary.html#term-file-object) with a valid file
    descriptor. With the default settings of `None`, no redirection will
    occur. [`PIPE`](#subprocess.PIPE "subprocess.PIPE") indicates that a new pipe to the child should be
    created. [`DEVNULL`](#subprocess.DEVNULL "subprocess.DEVNULL") indicates that the special file [`os.devnull`](os.html#os.devnull "os.devnull")
    will be used. Additionally, *stderr* can be [`STDOUT`](#subprocess.STDOUT "subprocess.STDOUT"), which indicates
    that the stderr data from the applications should be captured into the same
    file handle as for *stdout*.

    If *preexec\_fn* is set to a callable object, this object will be called in the
    child process just before the child is executed.
    (POSIX only)

    Warning

    The *preexec\_fn* parameter is NOT SAFE to use in the presence of threads
    in your application. The child process could deadlock before exec is
    called.

    Note

    If you need to modify the environment for the child use the *env*
    parameter rather than doing it in a *preexec\_fn*.
    The *start\_new\_session* and *process\_group* parameters should take the place of
    code using *preexec\_fn* to call [`os.setsid()`](os.html#os.setsid "os.setsid") or [`os.setpgid()`](os.html#os.setpgid "os.setpgid") in the child.

    Changed in version 3.8: The *preexec\_fn* parameter is no longer supported in subinterpreters.
    The use of the parameter in a subinterpreter raises
    [`RuntimeError`](exceptions.html#RuntimeError "RuntimeError"). The new restriction may affect applications that
    are deployed in mod\_wsgi, uWSGI, and other embedded environments.

    If *close\_fds* is true, all file descriptors except `0`, `1` and
    `2` will be closed before the child process is executed. Otherwise
    when *close\_fds* is false, file descriptors obey their inheritable flag
    as described in [Inheritance of File Descriptors](os.html#fd-inheritance).

    On Windows, if *close\_fds* is true then no handles will be inherited by the
    child process unless explicitly passed in the `handle_list` element of
    [`STARTUPINFO.lpAttributeList`](#subprocess.STARTUPINFO.lpAttributeList "subprocess.STARTUPINFO.lpAttributeList"), or by standard handle redirection.

    Changed in version 3.2: The default for *close\_fds* was changed from [`False`](constants.html#False "False") to
    what is described above.

    Changed in version 3.7: On Windows the default for *close\_fds* was changed from [`False`](constants.html#False "False") to
    [`True`](constants.html#True "True") when redirecting the standard handles. It’s now possible to
    set *close\_fds* to [`True`](constants.html#True "True") when redirecting the standard handles.

    *pass\_fds* is an optional sequence of file descriptors to keep open
    between the parent and child. Providing any *pass\_fds* forces
    *close\_fds* to be [`True`](constants.html#True "True"). (POSIX only)

    Changed in version 3.2: The *pass\_fds* parameter was added.

    If *cwd* is not `None`, the function changes the working directory to
    *cwd* before executing the child. *cwd* can be a string, bytes or
    [path-like](../glossary.html#term-path-like-object) object. On POSIX, the function
    looks for *executable* (or for the first item in *args*) relative to *cwd*
    if the executable path is a relative path.

    Changed in version 3.8: *cwd* parameter accepts a bytes object on Windows.

    If *restore\_signals* is true (the default) all signals that Python has set to
    SIG\_IGN are restored to SIG\_DFL in the child process before the exec.
    Currently this includes the SIGPIPE, SIGXFZ and SIGXFSZ signals.
    (POSIX only)

    Changed in version 3.2: *restore\_signals* was added.

    If *start\_new\_session* is true the `setsid()` system call will be made in the
    child process prior to the execution of the subprocess.

    Changed in version 3.2: *start\_new\_session* was added.

    If *process\_group* is a non-negative integer, the `setpgid(0, value)` system call will
    be made in the child process prior to the execution of the subprocess.

    Changed in version 3.11: *process\_group* was added.

    If *group* is not `None`, the setregid() system call will be made in the
    child process prior to the execution of the subprocess. If the provided
    value is a string, it will be looked up via [`grp.getgrnam()`](grp.html#grp.getgrnam "grp.getgrnam") and
    the value in `gr_gid` will be used. If the value is an integer, it
    will be passed verbatim. (POSIX only)

    If *extra\_groups* is not `None`, the setgroups() system call will be
    made in the child process prior to the execution of the subprocess.
    Strings provided in *extra\_groups* will be looked up via
    [`grp.getgrnam()`](grp.html#grp.getgrnam "grp.getgrnam") and the values in `gr_gid` will be used.
    Integer values will be passed verbatim. (POSIX only)

    If *user* is not `None`, the setreuid() system call will be made in the
    child process prior to the execution of the subprocess. If the provided
    value is a string, it will be looked up via [`pwd.getpwnam()`](pwd.html#pwd.getpwnam "pwd.getpwnam") and
    the value in `pw_uid` will be used. If the value is an integer, it will
    be passed verbatim. (POSIX only)

    If *umask* is not negative, the umask() system call will be made in the
    child process prior to the execution of the subprocess.

    If *env* is not `None`, it must be a mapping that defines the environment
    variables for the new process; these are used instead of the default
    behavior of inheriting the current process’ environment. This mapping can be
    str to str on any platform or bytes to bytes on POSIX platforms much like
    [`os.environ`](os.html#os.environ "os.environ") or [`os.environb`](os.html#os.environb "os.environb").

    Note

    If specified, *env* must provide any variables required for the program to
    execute. On Windows, in order to run a [side-by-side assembly](https://en.wikipedia.org/wiki/Side-by-Side_Assembly) the
    specified *env* **must** include a valid `SystemRoot`.

    If *encoding* or *errors* are specified, or *text* is true, the file objects
    *stdin*, *stdout* and *stderr* are opened in text mode with the specified
    *encoding* and *errors*, as described above in [Frequently Used Arguments](#frequently-used-arguments).
    The *universal\_newlines* argument is equivalent to *text* and is provided
    for backwards compatibility. By default, file objects are opened in binary mode.

    Added in version 3.6: *encoding* and *errors* were added.

    Added in version 3.7: *text* was added as a more readable alias for *universal\_newlines*.

    If given, *startupinfo* will be a [`STARTUPINFO`](#subprocess.STARTUPINFO "subprocess.STARTUPINFO") object, which is
    passed to the underlying `CreateProcess` function.

    If given, *creationflags*, can be one or more of the following flags:

    *pipesize* can be used to change the size of the pipe when
    [`PIPE`](#subprocess.PIPE "subprocess.PIPE") is used for *stdin*, *stdout* or *stderr*. The size of the pipe
    is only changed on platforms that support this (only Linux at this time of
    writing). Other platforms will ignore this parameter.

    Changed in version 3.10: Added the *pipesize* parameter.

    Popen objects are supported as context managers via the [`with`](../reference/compound_stmts.html#with) statement:
    on exit, standard file descriptors are closed, and the process is waited for.

    Copy

    ```
    with Popen(["ifconfig"], stdout=PIPE) as proc:
        log.write(proc.stdout.read())

    ```

    Popen and the other functions in this module that use it raise an
    [auditing event](sys.html#auditing) `subprocess.Popen` with arguments
    `executable`, `args`, `cwd`, and `env`. The value for `args`
    may be a single string or a list of strings, depending on platform.

    Changed in version 3.2: Added context manager support.

    Changed in version 3.6: Popen destructor now emits a [`ResourceWarning`](exceptions.html#ResourceWarning "ResourceWarning") warning if the child
    process is still running.

    Changed in version 3.8: Popen can use [`os.posix_spawn()`](os.html#os.posix_spawn "os.posix_spawn") in some cases for better
    performance. On Windows Subsystem for Linux and QEMU User Emulation,
    Popen constructor using [`os.posix_spawn()`](os.html#os.posix_spawn "os.posix_spawn") no longer raise an
    exception on errors like missing program, but the child process fails
    with a non-zero [`returncode`](#subprocess.Popen.returncode "subprocess.Popen.returncode").