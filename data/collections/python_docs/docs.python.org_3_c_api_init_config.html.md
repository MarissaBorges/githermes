Python Initialization Configuration
===================================

Python can be initialized with [`Py_InitializeFromConfig()`](init.html#c.Py_InitializeFromConfig "Py_InitializeFromConfig") and the
[`PyConfig`](#c.PyConfig "PyConfig") structure. It can be preinitialized with
[`Py_PreInitialize()`](#c.Py_PreInitialize "Py_PreInitialize") and the [`PyPreConfig`](#c.PyPreConfig "PyPreConfig") structure.

There are two kinds of configuration:

* The [Python Configuration](#init-python-config) can be used to build a
  customized Python which behaves as the regular Python. For example,
  environment variables and command line arguments are used to configure
  Python.
* The [Isolated Configuration](#init-isolated-conf) can be used to embed
  Python into an application. It isolates Python from the system. For example,
  environment variables are ignored, the LC\_CTYPE locale is left unchanged and
  no signal handler is registered.

The [`Py_RunMain()`](init.html#c.Py_RunMain "Py_RunMain") function can be used to write a customized Python
program.

See also [Initialization, Finalization, and Threads](init.html#initialization).

See also

[**PEP 587**](https://peps.python.org/pep-0587/) “Python Initialization Configuration”.

Example
-------

Example of customized Python always running in isolated mode:

```
int main(int argc, char **argv)
{
    PyStatus status;

    PyConfig config;
    PyConfig_InitPythonConfig(&config);
    config.isolated = 1;

    /* Decode command line arguments.
       Implicitly preinitialize Python (in isolated mode). */
    status = PyConfig_SetBytesArgv(&config, argc, argv);
    if (PyStatus_Exception(status)) {
        goto exception;
    }

    status = Py_InitializeFromConfig(&config);
    if (PyStatus_Exception(status)) {
        goto exception;
    }
    PyConfig_Clear(&config);

    return Py_RunMain();

exception:
    PyConfig_Clear(&config);
    if (PyStatus_IsExit(status)) {
        return status.exitcode;
    }
    /* Display the error message and exit the process with
       non-zero exit code */
    Py_ExitStatusException(status);
}

```

PyWideStringList
----------------

type PyWideStringList
:   List of `wchar_t*` strings.

    If *length* is non-zero, *items* must be non-`NULL` and all strings must be
    non-`NULL`.

    Methods:

    [PyStatus](#c.PyStatus "PyStatus") PyWideStringList\_Append([PyWideStringList](#c.PyWideStringList "PyWideStringList") \*list, const wchar\_t \*item)
    :   Append *item* to *list*.

        Python must be preinitialized to call this function.

    [PyStatus](#c.PyStatus "PyStatus") PyWideStringList\_Insert([PyWideStringList](#c.PyWideStringList "PyWideStringList") \*list, [Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") index, const wchar\_t \*item)
    :   Insert *item* into *list* at *index*.

        If *index* is greater than or equal to *list* length, append *item* to
        *list*.

        *index* must be greater than or equal to `0`.

        Python must be preinitialized to call this function.

    Structure fields:

    [Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") length
    :   List length.

    wchar\_t \*\*items
    :   List items.

PyStatus
--------

type PyStatus
:   Structure to store an initialization function status: success, error
    or exit.

    For an error, it can store the C function name which created the error.

    Structure fields:

    int exitcode
    :   Exit code. Argument passed to `exit()`.

    const char \*err\_msg
    :   Error message.

    const char \*func
    :   Name of the function which created an error, can be `NULL`.

    Functions to create a status:

    [PyStatus](#c.PyStatus "PyStatus") PyStatus\_Ok(void)
    :   Success.

    [PyStatus](#c.PyStatus "PyStatus") PyStatus\_Error(const char \*err\_msg)
    :   Initialization error with a message.

        *err\_msg* must not be `NULL`.

    [PyStatus](#c.PyStatus "PyStatus") PyStatus\_NoMemory(void)
    :   Memory allocation failure (out of memory).

    [PyStatus](#c.PyStatus "PyStatus") PyStatus\_Exit(int exitcode)
    :   Exit Python with the specified exit code.

    Functions to handle a status:

    int PyStatus\_Exception([PyStatus](#c.PyStatus "PyStatus") status)
    :   Is the status an error or an exit? If true, the exception must be
        handled; by calling [`Py_ExitStatusException()`](#c.Py_ExitStatusException "Py_ExitStatusException") for example.

    int PyStatus\_IsError([PyStatus](#c.PyStatus "PyStatus") status)
    :   Is the result an error?

    int PyStatus\_IsExit([PyStatus](#c.PyStatus "PyStatus") status)
    :   Is the result an exit?

    void Py\_ExitStatusException([PyStatus](#c.PyStatus "PyStatus") status)
    :   Call `exit(exitcode)` if *status* is an exit. Print the error
        message and exit with a non-zero exit code if *status* is an error. Must
        only be called if `PyStatus_Exception(status)` is non-zero.

Note

Internally, Python uses macros which set `PyStatus.func`,
whereas functions to create a status set `func` to `NULL`.

Example:

```
PyStatus alloc(void **ptr, size_t size)
{
    *ptr = PyMem_RawMalloc(size);
    if (*ptr == NULL) {
        return PyStatus_NoMemory();
    }
    return PyStatus_Ok();
}

int main(int argc, char **argv)
{
    void *ptr;
    PyStatus status = alloc(&ptr, 16);
    if (PyStatus_Exception(status)) {
        Py_ExitStatusException(status);
    }
    PyMem_Free(ptr);
    return 0;
}

```

PyPreConfig
-----------

type PyPreConfig
:   Structure used to preinitialize Python.

    Function to initialize a preconfiguration:

    void PyPreConfig\_InitPythonConfig([PyPreConfig](#c.PyPreConfig "PyPreConfig") \*preconfig)
    :   Initialize the preconfiguration with [Python Configuration](#init-python-config).

    void PyPreConfig\_InitIsolatedConfig([PyPreConfig](#c.PyPreConfig "PyPreConfig") \*preconfig)
    :   Initialize the preconfiguration with [Isolated Configuration](#init-isolated-conf).

    Structure fields:

    int allocator
    :   Name of the Python memory allocators:

        `PYMEM_ALLOCATOR_PYMALLOC` and `PYMEM_ALLOCATOR_PYMALLOC_DEBUG` are
        not supported if Python is [`configured using --without-pymalloc`](../using/configure.html#cmdoption-without-pymalloc).

        `PYMEM_ALLOCATOR_MIMALLOC` and `PYMEM_ALLOCATOR_MIMALLOC_DEBUG` are
        not supported if Python is [`configured using --without-mimalloc`](../using/configure.html#cmdoption-without-mimalloc) or if the underlying atomic support isn’t
        available.

        See [Memory Management](memory.html#memory).

        Default: `PYMEM_ALLOCATOR_NOT_SET`.

    int configure\_locale
    :   Set the LC\_CTYPE locale to the user preferred locale.

        If equals to `0`, set [`coerce_c_locale`](#c.PyPreConfig.coerce_c_locale "PyPreConfig.coerce_c_locale") and
        [`coerce_c_locale_warn`](#c.PyPreConfig.coerce_c_locale_warn "PyPreConfig.coerce_c_locale_warn") members to `0`.

        See the [locale encoding](../glossary.html#term-locale-encoding).

        Default: `1` in Python config, `0` in isolated config.

    int coerce\_c\_locale
    :   If equals to `2`, coerce the C locale.

        If equals to `1`, read the LC\_CTYPE locale to decide if it should be
        coerced.

        See the [locale encoding](../glossary.html#term-locale-encoding).

        Default: `-1` in Python config, `0` in isolated config.

    int coerce\_c\_locale\_warn
    :   If non-zero, emit a warning if the C locale is coerced.

        Default: `-1` in Python config, `0` in isolated config.

    int dev\_mode
    :   [Python Development Mode](../library/devmode.html#devmode): see
        [`PyConfig.dev_mode`](#c.PyConfig.dev_mode "PyConfig.dev_mode").

        Default: `-1` in Python mode, `0` in isolated mode.

    int isolated
    :   Isolated mode: see [`PyConfig.isolated`](#c.PyConfig.isolated "PyConfig.isolated").

        Default: `0` in Python mode, `1` in isolated mode.

    int legacy\_windows\_fs\_encoding
    :   If non-zero:

        Initialized from the [`PYTHONLEGACYWINDOWSFSENCODING`](../using/cmdline.html#envvar-PYTHONLEGACYWINDOWSFSENCODING) environment
        variable value.

        Only available on Windows. `#ifdef MS_WINDOWS` macro can be used for
        Windows specific code.

        Default: `0`.

    int parse\_argv
    :   If non-zero, [`Py_PreInitializeFromArgs()`](#c.Py_PreInitializeFromArgs "Py_PreInitializeFromArgs") and
        [`Py_PreInitializeFromBytesArgs()`](#c.Py_PreInitializeFromBytesArgs "Py_PreInitializeFromBytesArgs") parse their `argv` argument the
        same way the regular Python parses command line arguments: see
        [Command Line Arguments](../using/cmdline.html#using-on-cmdline).

        Default: `1` in Python config, `0` in isolated config.

    int use\_environment
    :   Use [environment variables](../using/cmdline.html#using-on-envvars)? See
        [`PyConfig.use_environment`](#c.PyConfig.use_environment "PyConfig.use_environment").

        Default: `1` in Python config and `0` in isolated config.

    int utf8\_mode
    :   If non-zero, enable the [Python UTF-8 Mode](../library/os.html#utf8-mode).

        Set to `0` or `1` by the [`-X utf8`](../using/cmdline.html#cmdoption-X) command line option
        and the [`PYTHONUTF8`](../using/cmdline.html#envvar-PYTHONUTF8) environment variable.

        Also set to `1` if the `LC_CTYPE` locale is `C` or `POSIX`.

        Default: `-1` in Python config and `0` in isolated config.

Preinitialize Python with PyPreConfig
-------------------------------------

The preinitialization of Python:

The current preconfiguration (`PyPreConfig` type) is stored in
`_PyRuntime.preconfig`.

Functions to preinitialize Python:

[PyStatus](#c.PyStatus "PyStatus") Py\_PreInitialize(const [PyPreConfig](#c.PyPreConfig "PyPreConfig") \*preconfig)
:   Preinitialize Python from *preconfig* preconfiguration.

    *preconfig* must not be `NULL`.

[PyStatus](#c.PyStatus "PyStatus") Py\_PreInitializeFromBytesArgs(const [PyPreConfig](#c.PyPreConfig "PyPreConfig") \*preconfig, int argc, char \*const \*argv)
:   Preinitialize Python from *preconfig* preconfiguration.

    Parse *argv* command line arguments (bytes strings) if
    [`parse_argv`](#c.PyPreConfig.parse_argv "PyPreConfig.parse_argv") of *preconfig* is non-zero.

    *preconfig* must not be `NULL`.

[PyStatus](#c.PyStatus "PyStatus") Py\_PreInitializeFromArgs(const [PyPreConfig](#c.PyPreConfig "PyPreConfig") \*preconfig, int argc, wchar\_t \*const \*argv)
:   Preinitialize Python from *preconfig* preconfiguration.

    Parse *argv* command line arguments (wide strings) if
    [`parse_argv`](#c.PyPreConfig.parse_argv "PyPreConfig.parse_argv") of *preconfig* is non-zero.

    *preconfig* must not be `NULL`.

The caller is responsible to handle exceptions (error or exit) using
[`PyStatus_Exception()`](#c.PyStatus_Exception "PyStatus_Exception") and [`Py_ExitStatusException()`](#c.Py_ExitStatusException "Py_ExitStatusException").

For [Python Configuration](#init-python-config)
([`PyPreConfig_InitPythonConfig()`](#c.PyPreConfig_InitPythonConfig "PyPreConfig_InitPythonConfig")), if Python is initialized with
command line arguments, the command line arguments must also be passed to
preinitialize Python, since they have an effect on the pre-configuration
like encodings. For example, the [`-X utf8`](../using/cmdline.html#cmdoption-X) command line option
enables the [Python UTF-8 Mode](../library/os.html#utf8-mode).

`PyMem_SetAllocator()` can be called after [`Py_PreInitialize()`](#c.Py_PreInitialize "Py_PreInitialize") and
before [`Py_InitializeFromConfig()`](init.html#c.Py_InitializeFromConfig "Py_InitializeFromConfig") to install a custom memory allocator.
It can be called before [`Py_PreInitialize()`](#c.Py_PreInitialize "Py_PreInitialize") if
[`PyPreConfig.allocator`](#c.PyPreConfig.allocator "PyPreConfig.allocator") is set to `PYMEM_ALLOCATOR_NOT_SET`.

Python memory allocation functions like [`PyMem_RawMalloc()`](memory.html#c.PyMem_RawMalloc "PyMem_RawMalloc") must not be
used before the Python preinitialization, whereas calling directly `malloc()`
and `free()` is always safe. [`Py_DecodeLocale()`](sys.html#c.Py_DecodeLocale "Py_DecodeLocale") must not be called
before the Python preinitialization.

Example using the preinitialization to enable
the [Python UTF-8 Mode](../library/os.html#utf8-mode):

```
PyStatus status;
PyPreConfig preconfig;
PyPreConfig_InitPythonConfig(&preconfig);

preconfig.utf8_mode = 1;

status = Py_PreInitialize(&preconfig);
if (PyStatus_Exception(status)) {
    Py_ExitStatusException(status);
}

/* at this point, Python speaks UTF-8 */

Py_Initialize();
/* ... use Python API here ... */
Py_Finalize();

```

PyConfig
--------

type PyConfig
:   Structure containing most parameters to configure Python.

    When done, the [`PyConfig_Clear()`](#c.PyConfig_Clear "PyConfig_Clear") function must be used to release the
    configuration memory.

    Structure methods:

    void PyConfig\_InitPythonConfig([PyConfig](#c.PyConfig "PyConfig") \*config)
    :   Initialize configuration with the [Python Configuration](#init-python-config).

    void PyConfig\_InitIsolatedConfig([PyConfig](#c.PyConfig "PyConfig") \*config)
    :   Initialize configuration with the [Isolated Configuration](#init-isolated-conf).

    [PyStatus](#c.PyStatus "PyStatus") PyConfig\_SetString([PyConfig](#c.PyConfig "PyConfig") \*config, wchar\_t \*const \*config\_str, const wchar\_t \*str)
    :   Copy the wide character string *str* into `*config_str`.

        [Preinitialize Python](#c-preinit) if needed.

    [PyStatus](#c.PyStatus "PyStatus") PyConfig\_SetBytesString([PyConfig](#c.PyConfig "PyConfig") \*config, wchar\_t \*const \*config\_str, const char \*str)
    :   Decode *str* using [`Py_DecodeLocale()`](sys.html#c.Py_DecodeLocale "Py_DecodeLocale") and set the result into
        `*config_str`.

        [Preinitialize Python](#c-preinit) if needed.

    [PyStatus](#c.PyStatus "PyStatus") PyConfig\_SetArgv([PyConfig](#c.PyConfig "PyConfig") \*config, int argc, wchar\_t \*const \*argv)
    :   Set command line arguments ([`argv`](#c.PyConfig.argv "PyConfig.argv") member of
        *config*) from the *argv* list of wide character strings.

        [Preinitialize Python](#c-preinit) if needed.

    [PyStatus](#c.PyStatus "PyStatus") PyConfig\_SetBytesArgv([PyConfig](#c.PyConfig "PyConfig") \*config, int argc, char \*const \*argv)
    :   Set command line arguments ([`argv`](#c.PyConfig.argv "PyConfig.argv") member of
        *config*) from the *argv* list of bytes strings. Decode bytes using
        [`Py_DecodeLocale()`](sys.html#c.Py_DecodeLocale "Py_DecodeLocale").

        [Preinitialize Python](#c-preinit) if needed.

    [PyStatus](#c.PyStatus "PyStatus") PyConfig\_SetWideStringList([PyConfig](#c.PyConfig "PyConfig") \*config, [PyWideStringList](#c.PyWideStringList "PyWideStringList") \*list, [Py\_ssize\_t](intro.html#c.Py_ssize_t "Py_ssize_t") length, wchar\_t \*\*items)
    :   Set the list of wide strings *list* to *length* and *items*.

        [Preinitialize Python](#c-preinit) if needed.

    [PyStatus](#c.PyStatus "PyStatus") PyConfig\_Read([PyConfig](#c.PyConfig "PyConfig") \*config)
    :   Read all Python configuration.

        Fields which are already initialized are left unchanged.

        Fields for [path configuration](#init-path-config) are no longer
        calculated or modified when calling this function, as of Python 3.11.

        The [`PyConfig_Read()`](#c.PyConfig_Read "PyConfig_Read") function only parses
        [`PyConfig.argv`](#c.PyConfig.argv "PyConfig.argv") arguments once: [`PyConfig.parse_argv`](#c.PyConfig.parse_argv "PyConfig.parse_argv")
        is set to `2` after arguments are parsed. Since Python arguments are
        stripped from [`PyConfig.argv`](#c.PyConfig.argv "PyConfig.argv"), parsing arguments twice would
        parse the application options as Python options.

        [Preinitialize Python](#c-preinit) if needed.

    void PyConfig\_Clear([PyConfig](#c.PyConfig "PyConfig") \*config)
    :   Release configuration memory.

    Most `PyConfig` methods [preinitialize Python](#c-preinit) if needed.
    In that case, the Python preinitialization configuration
    ([`PyPreConfig`](#c.PyPreConfig "PyPreConfig")) in based on the [`PyConfig`](#c.PyConfig "PyConfig"). If configuration
    fields which are in common with [`PyPreConfig`](#c.PyPreConfig "PyPreConfig") are tuned, they must
    be set before calling a [`PyConfig`](#c.PyConfig "PyConfig") method:

    Moreover, if [`PyConfig_SetArgv()`](#c.PyConfig_SetArgv "PyConfig_SetArgv") or [`PyConfig_SetBytesArgv()`](#c.PyConfig_SetBytesArgv "PyConfig_SetBytesArgv")
    is used, this method must be called before other methods, since the
    preinitialization configuration depends on command line arguments (if
    [`parse_argv`](#c.PyConfig.parse_argv "PyConfig.parse_argv") is non-zero).

    The caller of these methods is responsible to handle exceptions (error or
    exit) using `PyStatus_Exception()` and `Py_ExitStatusException()`.

    Structure fields:

    [PyWideStringList](#c.PyWideStringList "PyWideStringList") argv
    :   Set [`sys.argv`](../library/sys.html#sys.argv "sys.argv") command line arguments based on
        [`argv`](#c.PyConfig.argv "PyConfig.argv"). These parameters are similar to those passed
        to the program’s `main()` function with the difference that the
        first entry should refer to the script file to be executed rather than
        the executable hosting the Python interpreter. If there isn’t a script
        that will be run, the first entry in [`argv`](#c.PyConfig.argv "PyConfig.argv") can be an
        empty string.

        Set [`parse_argv`](#c.PyConfig.parse_argv "PyConfig.parse_argv") to `1` to parse
        [`argv`](#c.PyConfig.argv "PyConfig.argv") the same way the regular Python parses Python
        command line arguments and then to strip Python arguments from
        [`argv`](#c.PyConfig.argv "PyConfig.argv").

        If [`argv`](#c.PyConfig.argv "PyConfig.argv") is empty, an empty string is added to
        ensure that [`sys.argv`](../library/sys.html#sys.argv "sys.argv") always exists and is never empty.

        Default: `NULL`.

        See also the [`orig_argv`](#c.PyConfig.orig_argv "PyConfig.orig_argv") member.

    int safe\_path
    :   If equals to zero, `Py_RunMain()` prepends a potentially unsafe path to
        [`sys.path`](../library/sys.html#sys.path "sys.path") at startup:

        * If [`argv[0]`](#c.PyConfig.argv "PyConfig.argv") is equal to `L"-m"`
          (`python -m module`), prepend the current working directory.
        * If running a script (`python script.py`), prepend the script’s
          directory. If it’s a symbolic link, resolve symbolic links.
        * Otherwise (`python -c code` and `python`), prepend an empty string,
          which means the current working directory.

        Set to `1` by the [`-P`](../using/cmdline.html#cmdoption-P) command line option and the
        [`PYTHONSAFEPATH`](../using/cmdline.html#envvar-PYTHONSAFEPATH) environment variable.

        Default: `0` in Python config, `1` in isolated config.

    wchar\_t \*base\_exec\_prefix
    :   [`sys.base_exec_prefix`](../library/sys.html#sys.base_exec_prefix "sys.base_exec_prefix").

        Default: `NULL`.

        Part of the [Python Path Configuration](#init-path-config) output.

        See also [`PyConfig.exec_prefix`](#c.PyConfig.exec_prefix "PyConfig.exec_prefix").

    wchar\_t \*base\_executable
    :   Python base executable: `sys._base_executable`.

        Set by the `__PYVENV_LAUNCHER__` environment variable.

        Set from [`PyConfig.executable`](#c.PyConfig.executable "PyConfig.executable") if `NULL`.

        Default: `NULL`.

        Part of the [Python Path Configuration](#init-path-config) output.

        See also [`PyConfig.executable`](#c.PyConfig.executable "PyConfig.executable").

    wchar\_t \*base\_prefix
    :   [`sys.base_prefix`](../library/sys.html#sys.base_prefix "sys.base_prefix").

        Default: `NULL`.

        Part of the [Python Path Configuration](#init-path-config) output.

        See also [`PyConfig.prefix`](#c.PyConfig.prefix "PyConfig.prefix").

    int buffered\_stdio
    :   If equals to `0` and [`configure_c_stdio`](#c.PyConfig.configure_c_stdio "PyConfig.configure_c_stdio") is non-zero,
        disable buffering on the C streams stdout and stderr.

        Set to `0` by the [`-u`](../using/cmdline.html#cmdoption-u) command line option and the
        [`PYTHONUNBUFFERED`](../using/cmdline.html#envvar-PYTHONUNBUFFERED) environment variable.

        stdin is always opened in buffered mode.

        Default: `1`.

    int bytes\_warning
    :   If equals to `1`, issue a warning when comparing [`bytes`](../library/stdtypes.html#bytes "bytes") or
        [`bytearray`](../library/stdtypes.html#bytearray "bytearray") with [`str`](../library/stdtypes.html#str "str"), or comparing [`bytes`](../library/stdtypes.html#bytes "bytes") with
        [`int`](../library/functions.html#int "int").

        If equal or greater to `2`, raise a [`BytesWarning`](../library/exceptions.html#BytesWarning "BytesWarning") exception in these
        cases.

        Incremented by the [`-b`](../using/cmdline.html#cmdoption-b) command line option.

        Default: `0`.

    int warn\_default\_encoding
    :   If non-zero, emit a [`EncodingWarning`](../library/exceptions.html#EncodingWarning "EncodingWarning") warning when [`io.TextIOWrapper`](../library/io.html#io.TextIOWrapper "io.TextIOWrapper")
        uses its default encoding. See [Opt-in EncodingWarning](../library/io.html#io-encoding-warning) for details.

        Default: `0`.

    int code\_debug\_ranges
    :   If equals to `0`, disables the inclusion of the end line and column
        mappings in code objects. Also disables traceback printing carets to
        specific error locations.

        Set to `0` by the [`PYTHONNODEBUGRANGES`](../using/cmdline.html#envvar-PYTHONNODEBUGRANGES) environment variable
        and by the [`-X no_debug_ranges`](../using/cmdline.html#cmdoption-X) command line option.

        Default: `1`.

    wchar\_t \*check\_hash\_pycs\_mode
    :   Control the validation behavior of hash-based `.pyc` files:
        value of the [`--check-hash-based-pycs`](../using/cmdline.html#cmdoption-check-hash-based-pycs) command line option.

        Valid values:

        * `L"always"`: Hash the source file for invalidation regardless of
          value of the ‘check\_source’ flag.
        * `L"never"`: Assume that hash-based pycs always are valid.
        * `L"default"`: The ‘check\_source’ flag in hash-based pycs
          determines invalidation.

        Default: `L"default"`.

        See also [**PEP 552**](https://peps.python.org/pep-0552/) “Deterministic pycs”.

    int configure\_c\_stdio
    :   If non-zero, configure C standard streams:

        * On Windows, set the binary mode (`O_BINARY`) on stdin, stdout and
          stderr.
        * If [`buffered_stdio`](#c.PyConfig.buffered_stdio "PyConfig.buffered_stdio") equals zero, disable buffering
          of stdin, stdout and stderr streams.
        * If [`interactive`](#c.PyConfig.interactive "PyConfig.interactive") is non-zero, enable stream
          buffering on stdin and stdout (only stdout on Windows).

        Default: `1` in Python config, `0` in isolated config.

    int dev\_mode
    :   If non-zero, enable the [Python Development Mode](../library/devmode.html#devmode).

        Set to `1` by the [`-X dev`](../using/cmdline.html#cmdoption-X) option and the
        [`PYTHONDEVMODE`](../using/cmdline.html#envvar-PYTHONDEVMODE) environment variable.

        Default: `-1` in Python mode, `0` in isolated mode.

    int dump\_refs
    :   Dump Python references?

        If non-zero, dump all objects which are still alive at exit.

        Set to `1` by the [`PYTHONDUMPREFS`](../using/cmdline.html#envvar-PYTHONDUMPREFS) environment variable.

        Needs a special build of Python with the `Py_TRACE_REFS` macro defined:
        see the [`configure --with-trace-refs option`](../using/configure.html#cmdoption-with-trace-refs).

        Default: `0`.

    wchar\_t \*exec\_prefix
    :   The site-specific directory prefix where the platform-dependent Python
        files are installed: [`sys.exec_prefix`](../library/sys.html#sys.exec_prefix "sys.exec_prefix").

        Default: `NULL`.

        Part of the [Python Path Configuration](#init-path-config) output.

        See also [`PyConfig.base_exec_prefix`](#c.PyConfig.base_exec_prefix "PyConfig.base_exec_prefix").

    wchar\_t \*executable
    :   The absolute path of the executable binary for the Python interpreter:
        [`sys.executable`](../library/sys.html#sys.executable "sys.executable").

        Default: `NULL`.

        Part of the [Python Path Configuration](#init-path-config) output.

        See also [`PyConfig.base_executable`](#c.PyConfig.base_executable "PyConfig.base_executable").

    int faulthandler
    :   Enable faulthandler?

        If non-zero, call [`faulthandler.enable()`](../library/faulthandler.html#faulthandler.enable "faulthandler.enable") at startup.

        Set to `1` by [`-X faulthandler`](../using/cmdline.html#cmdoption-X) and the
        [`PYTHONFAULTHANDLER`](../using/cmdline.html#envvar-PYTHONFAULTHANDLER) environment variable.

        Default: `-1` in Python mode, `0` in isolated mode.

    wchar\_t \*filesystem\_encoding
    :   [Filesystem encoding](../glossary.html#term-filesystem-encoding-and-error-handler):
        [`sys.getfilesystemencoding()`](../library/sys.html#sys.getfilesystemencoding "sys.getfilesystemencoding").

        On macOS, Android and VxWorks: use `"utf-8"` by default.

        On Windows: use `"utf-8"` by default, or `"mbcs"` if
        [`legacy_windows_fs_encoding`](#c.PyPreConfig.legacy_windows_fs_encoding "PyPreConfig.legacy_windows_fs_encoding") of
        [`PyPreConfig`](#c.PyPreConfig "PyPreConfig") is non-zero.

        Default encoding on other platforms:

        * `"utf-8"` if [`PyPreConfig.utf8_mode`](#c.PyPreConfig.utf8_mode "PyPreConfig.utf8_mode") is non-zero.
        * `"ascii"` if Python detects that `nl_langinfo(CODESET)` announces
          the ASCII encoding, whereas the `mbstowcs()` function
          decodes from a different encoding (usually Latin1).
        * `"utf-8"` if `nl_langinfo(CODESET)` returns an empty string.
        * Otherwise, use the [locale encoding](../glossary.html#term-locale-encoding):
          `nl_langinfo(CODESET)` result.

        At Python startup, the encoding name is normalized to the Python codec
        name. For example, `"ANSI_X3.4-1968"` is replaced with `"ascii"`.

        See also the [`filesystem_errors`](#c.PyConfig.filesystem_errors "PyConfig.filesystem_errors") member.

    wchar\_t \*filesystem\_errors
    :   [Filesystem error handler](../glossary.html#term-filesystem-encoding-and-error-handler):
        [`sys.getfilesystemencodeerrors()`](../library/sys.html#sys.getfilesystemencodeerrors "sys.getfilesystemencodeerrors").

        On Windows: use `"surrogatepass"` by default, or `"replace"` if
        [`legacy_windows_fs_encoding`](#c.PyPreConfig.legacy_windows_fs_encoding "PyPreConfig.legacy_windows_fs_encoding") of
        [`PyPreConfig`](#c.PyPreConfig "PyPreConfig") is non-zero.

        On other platforms: use `"surrogateescape"` by default.

        Supported error handlers:

        See also the [`filesystem_encoding`](#c.PyConfig.filesystem_encoding "PyConfig.filesystem_encoding") member.

    unsigned long hash\_seed

    int use\_hash\_seed
    :   Randomized hash function seed.

        If [`use_hash_seed`](#c.PyConfig.use_hash_seed "PyConfig.use_hash_seed") is zero, a seed is chosen randomly
        at Python startup, and [`hash_seed`](#c.PyConfig.hash_seed "PyConfig.hash_seed") is ignored.

        Set by the [`PYTHONHASHSEED`](../using/cmdline.html#envvar-PYTHONHASHSEED) environment variable.

        Default *use\_hash\_seed* value: `-1` in Python mode, `0` in isolated
        mode.

    wchar\_t \*home
    :   Set the default Python “home” directory, that is, the location of the
        standard Python libraries (see [`PYTHONHOME`](../using/cmdline.html#envvar-PYTHONHOME)).

        Set by the [`PYTHONHOME`](../using/cmdline.html#envvar-PYTHONHOME) environment variable.

        Default: `NULL`.

        Part of the [Python Path Configuration](#init-path-config) input.

    int import\_time
    :   If non-zero, profile import time.

        Set the `1` by the [`-X importtime`](../using/cmdline.html#cmdoption-X) option and the
        [`PYTHONPROFILEIMPORTTIME`](../using/cmdline.html#envvar-PYTHONPROFILEIMPORTTIME) environment variable.

        Default: `0`.

    int inspect
    :   Enter interactive mode after executing a script or a command.

        If greater than `0`, enable inspect: when a script is passed as first
        argument or the -c option is used, enter interactive mode after executing
        the script or the command, even when [`sys.stdin`](../library/sys.html#sys.stdin "sys.stdin") does not appear to
        be a terminal.

        Incremented by the [`-i`](../using/cmdline.html#cmdoption-i) command line option. Set to `1` if the
        [`PYTHONINSPECT`](../using/cmdline.html#envvar-PYTHONINSPECT) environment variable is non-empty.

        Default: `0`.

    int install\_signal\_handlers
    :   Install Python signal handlers?

        Default: `1` in Python mode, `0` in isolated mode.

    int interactive
    :   If greater than `0`, enable the interactive mode (REPL).

        Incremented by the [`-i`](../using/cmdline.html#cmdoption-i) command line option.

        Default: `0`.

    int int\_max\_str\_digits
    :   Configures the [integer string conversion length limitation](../library/stdtypes.html#int-max-str-digits). An initial value of `-1` means the value will
        be taken from the command line or environment or otherwise default to
        4300 ([`sys.int_info.default_max_str_digits`](../library/sys.html#sys.int_info.default_max_str_digits "sys.int_info.default_max_str_digits")). A value of `0`
        disables the limitation. Values greater than zero but less than 640
        ([`sys.int_info.str_digits_check_threshold`](../library/sys.html#sys.int_info.str_digits_check_threshold "sys.int_info.str_digits_check_threshold")) are unsupported and
        will produce an error.

        Configured by the [`-X int_max_str_digits`](../using/cmdline.html#cmdoption-X) command line
        flag or the [`PYTHONINTMAXSTRDIGITS`](../using/cmdline.html#envvar-PYTHONINTMAXSTRDIGITS) environment variable.

        Default: `-1` in Python mode. 4300
        ([`sys.int_info.default_max_str_digits`](../library/sys.html#sys.int_info.default_max_str_digits "sys.int_info.default_max_str_digits")) in isolated mode.

    int cpu\_count
    :   If the value of [`cpu_count`](#c.PyConfig.cpu_count "PyConfig.cpu_count") is not `-1` then it will
        override the return values of [`os.cpu_count()`](../library/os.html#os.cpu_count "os.cpu_count"),
        [`os.process_cpu_count()`](../library/os.html#os.process_cpu_count "os.process_cpu_count"), and [`multiprocessing.cpu_count()`](../library/multiprocessing.html#multiprocessing.cpu_count "multiprocessing.cpu_count").

        Configured by the `-X cpu_count=n|default` command line
        flag or the [`PYTHON_CPU_COUNT`](../using/cmdline.html#envvar-PYTHON_CPU_COUNT) environment variable.

        Default: `-1`.

    int isolated
    :   If greater than `0`, enable isolated mode:

        * Set [`safe_path`](#c.PyConfig.safe_path "PyConfig.safe_path") to `1`:
          don’t prepend a potentially unsafe path to [`sys.path`](../library/sys.html#sys.path "sys.path") at Python
          startup, such as the current directory, the script’s directory or an
          empty string.
        * Set [`use_environment`](#c.PyConfig.use_environment "PyConfig.use_environment") to `0`: ignore `PYTHON`
          environment variables.
        * Set [`user_site_directory`](#c.PyConfig.user_site_directory "PyConfig.user_site_directory") to `0`: don’t add the user
          site directory to [`sys.path`](../library/sys.html#sys.path "sys.path").
        * Python REPL doesn’t import [`readline`](../library/readline.html#module-readline "readline: GNU readline support for Python. (Unix)") nor enable default readline
          configuration on interactive prompts.

        Set to `1` by the [`-I`](../using/cmdline.html#cmdoption-I) command line option.

        Default: `0` in Python mode, `1` in isolated mode.

        See also the [Isolated Configuration](#init-isolated-conf) and
        [`PyPreConfig.isolated`](#c.PyPreConfig.isolated "PyPreConfig.isolated").

    int legacy\_windows\_stdio
    :   If non-zero, use [`io.FileIO`](../library/io.html#io.FileIO "io.FileIO") instead of
        `io._WindowsConsoleIO` for [`sys.stdin`](../library/sys.html#sys.stdin "sys.stdin"), [`sys.stdout`](../library/sys.html#sys.stdout "sys.stdout")
        and [`sys.stderr`](../library/sys.html#sys.stderr "sys.stderr").

        Set to `1` if the [`PYTHONLEGACYWINDOWSSTDIO`](../using/cmdline.html#envvar-PYTHONLEGACYWINDOWSSTDIO) environment
        variable is set to a non-empty string.

        Only available on Windows. `#ifdef MS_WINDOWS` macro can be used for
        Windows specific code.

        Default: `0`.

        See also the [**PEP 528**](https://peps.python.org/pep-0528/) (Change Windows console encoding to UTF-8).

    int malloc\_stats
    :   If non-zero, dump statistics on [Python pymalloc memory allocator](memory.html#pymalloc) at exit.

        Set to `1` by the [`PYTHONMALLOCSTATS`](../using/cmdline.html#envvar-PYTHONMALLOCSTATS) environment variable.

        The option is ignored if Python is [`configured using
        the --without-pymalloc option`](../using/configure.html#cmdoption-without-pymalloc).

        Default: `0`.

    wchar\_t \*platlibdir
    :   Platform library directory name: [`sys.platlibdir`](../library/sys.html#sys.platlibdir "sys.platlibdir").

        Set by the [`PYTHONPLATLIBDIR`](../using/cmdline.html#envvar-PYTHONPLATLIBDIR) environment variable.

        Default: value of the `PLATLIBDIR` macro which is set by the
        [`configure --with-platlibdir option`](../using/configure.html#cmdoption-with-platlibdir)
        (default: `"lib"`, or `"DLLs"` on Windows).

        Part of the [Python Path Configuration](#init-path-config) input.

        Changed in version 3.11: This macro is now used on Windows to locate the standard
        library extension modules, typically under `DLLs`. However,
        for compatibility, note that this value is ignored for any
        non-standard layouts, including in-tree builds and virtual
        environments.

    wchar\_t \*pythonpath\_env
    :   Module search paths ([`sys.path`](../library/sys.html#sys.path "sys.path")) as a string separated by `DELIM`
        ([`os.pathsep`](../library/os.html#os.pathsep "os.pathsep")).

        Set by the [`PYTHONPATH`](../using/cmdline.html#envvar-PYTHONPATH) environment variable.

        Default: `NULL`.

        Part of the [Python Path Configuration](#init-path-config) input.

    [PyWideStringList](#c.PyWideStringList "PyWideStringList") module\_search\_paths

    int module\_search\_paths\_set
    :   Module search paths: [`sys.path`](../library/sys.html#sys.path "sys.path").

        If [`module_search_paths_set`](#c.PyConfig.module_search_paths_set "PyConfig.module_search_paths_set") is equal to `0`,
        [`Py_InitializeFromConfig()`](init.html#c.Py_InitializeFromConfig "Py_InitializeFromConfig") will replace
        [`module_search_paths`](#c.PyConfig.module_search_paths "PyConfig.module_search_paths") and sets
        [`module_search_paths_set`](#c.PyConfig.module_search_paths_set "PyConfig.module_search_paths_set") to `1`.

        Default: empty list (`module_search_paths`) and `0`
        (`module_search_paths_set`).

        Part of the [Python Path Configuration](#init-path-config) output.

    int optimization\_level
    :   Compilation optimization level:

        * `0`: Peephole optimizer, set `__debug__` to `True`.
        * `1`: Level 0, remove assertions, set `__debug__` to `False`.
        * `2`: Level 1, strip docstrings.

        Incremented by the [`-O`](../using/cmdline.html#cmdoption-O) command line option. Set to the
        [`PYTHONOPTIMIZE`](../using/cmdline.html#envvar-PYTHONOPTIMIZE) environment variable value.

        Default: `0`.

    [PyWideStringList](#c.PyWideStringList "PyWideStringList") orig\_argv
    :   The list of the original command line arguments passed to the Python
        executable: [`sys.orig_argv`](../library/sys.html#sys.orig_argv "sys.orig_argv").

        If [`orig_argv`](#c.PyConfig.orig_argv "PyConfig.orig_argv") list is empty and
        [`argv`](#c.PyConfig.argv "PyConfig.argv") is not a list only containing an empty
        string, [`PyConfig_Read()`](#c.PyConfig_Read "PyConfig_Read") copies [`argv`](#c.PyConfig.argv "PyConfig.argv") into
        [`orig_argv`](#c.PyConfig.orig_argv "PyConfig.orig_argv") before modifying
        [`argv`](#c.PyConfig.argv "PyConfig.argv") (if [`parse_argv`](#c.PyConfig.parse_argv "PyConfig.parse_argv") is
        non-zero).

        See also the [`argv`](#c.PyConfig.argv "PyConfig.argv") member and the
        [`Py_GetArgcArgv()`](#c.Py_GetArgcArgv "Py_GetArgcArgv") function.

        Default: empty list.

    int parse\_argv
    :   Parse command line arguments?

        If equals to `1`, parse [`argv`](#c.PyConfig.argv "PyConfig.argv") the same way the regular
        Python parses [command line arguments](../using/cmdline.html#using-on-cmdline), and strip
        Python arguments from [`argv`](#c.PyConfig.argv "PyConfig.argv").

        The [`PyConfig_Read()`](#c.PyConfig_Read "PyConfig_Read") function only parses
        [`PyConfig.argv`](#c.PyConfig.argv "PyConfig.argv") arguments once: [`PyConfig.parse_argv`](#c.PyConfig.parse_argv "PyConfig.parse_argv")
        is set to `2` after arguments are parsed. Since Python arguments are
        stripped from [`PyConfig.argv`](#c.PyConfig.argv "PyConfig.argv"), parsing arguments twice would
        parse the application options as Python options.

        Default: `1` in Python mode, `0` in isolated mode.

    int parser\_debug
    :   Parser debug mode. If greater than `0`, turn on parser debugging output (for expert only, depending
        on compilation options).

        Incremented by the [`-d`](../using/cmdline.html#cmdoption-d) command line option. Set to the
        [`PYTHONDEBUG`](../using/cmdline.html#envvar-PYTHONDEBUG) environment variable value.

        Needs a [debug build of Python](../using/configure.html#debug-build) (the `Py_DEBUG` macro
        must be defined).

        Default: `0`.

    int pathconfig\_warnings
    :   If non-zero, calculation of path configuration is allowed to log
        warnings into `stderr`. If equals to `0`, suppress these warnings.

        Default: `1` in Python mode, `0` in isolated mode.

        Part of the [Python Path Configuration](#init-path-config) input.

        Changed in version 3.11: Now also applies on Windows.

    wchar\_t \*prefix
    :   The site-specific directory prefix where the platform independent Python
        files are installed: [`sys.prefix`](../library/sys.html#sys.prefix "sys.prefix").

        Default: `NULL`.

        Part of the [Python Path Configuration](#init-path-config) output.

        See also [`PyConfig.base_prefix`](#c.PyConfig.base_prefix "PyConfig.base_prefix").

    wchar\_t \*program\_name
    :   Program name used to initialize [`executable`](#c.PyConfig.executable "PyConfig.executable") and in
        early error messages during Python initialization.

        * On macOS, use [`PYTHONEXECUTABLE`](../using/cmdline.html#envvar-PYTHONEXECUTABLE) environment variable if set.
        * If the `WITH_NEXT_FRAMEWORK` macro is defined, use
          `__PYVENV_LAUNCHER__` environment variable if set.
        * Use `argv[0]` of [`argv`](#c.PyConfig.argv "PyConfig.argv") if available and
          non-empty.
        * Otherwise, use `L"python"` on Windows, or `L"python3"` on other
          platforms.

        Default: `NULL`.

        Part of the [Python Path Configuration](#init-path-config) input.

    wchar\_t \*pycache\_prefix
    :   Directory where cached `.pyc` files are written:
        [`sys.pycache_prefix`](../library/sys.html#sys.pycache_prefix "sys.pycache_prefix").

        Set by the [`-X pycache_prefix=PATH`](../using/cmdline.html#cmdoption-X) command line option and
        the [`PYTHONPYCACHEPREFIX`](../using/cmdline.html#envvar-PYTHONPYCACHEPREFIX) environment variable.
        The command-line option takes precedence.

        If `NULL`, [`sys.pycache_prefix`](../library/sys.html#sys.pycache_prefix "sys.pycache_prefix") is set to `None`.

        Default: `NULL`.

    int quiet
    :   Quiet mode. If greater than `0`, don’t display the copyright and version at
        Python startup in interactive mode.

        Incremented by the [`-q`](../using/cmdline.html#cmdoption-q) command line option.

        Default: `0`.

    wchar\_t \*run\_command
    :   Value of the [`-c`](../using/cmdline.html#cmdoption-c) command line option.

        Used by [`Py_RunMain()`](init.html#c.Py_RunMain "Py_RunMain").

        Default: `NULL`.

    wchar\_t \*run\_filename
    :   Filename passed on the command line: trailing command line argument
        without [`-c`](../using/cmdline.html#cmdoption-c) or [`-m`](../using/cmdline.html#cmdoption-m). It is used by the
        [`Py_RunMain()`](init.html#c.Py_RunMain "Py_RunMain") function.

        For example, it is set to `script.py` by the `python3 script.py arg`
        command line.

        See also the [`PyConfig.skip_source_first_line`](#c.PyConfig.skip_source_first_line "PyConfig.skip_source_first_line") option.

        Default: `NULL`.

    wchar\_t \*run\_module
    :   Value of the [`-m`](../using/cmdline.html#cmdoption-m) command line option.

        Used by [`Py_RunMain()`](init.html#c.Py_RunMain "Py_RunMain").

        Default: `NULL`.

    wchar\_t \*run\_presite
    :   `package.module` path to module that should be imported before
        `site.py` is run.

        Set by the [`-X presite=package.module`](../using/cmdline.html#cmdoption-X) command-line
        option and the [`PYTHON_PRESITE`](../using/cmdline.html#envvar-PYTHON_PRESITE) environment variable.
        The command-line option takes precedence.

        Needs a [debug build of Python](../using/configure.html#debug-build) (the `Py_DEBUG` macro
        must be defined).

        Default: `NULL`.

    int show\_ref\_count
    :   Show total reference count at exit (excluding [immortal](../glossary.html#term-immortal) objects)?

        Set to `1` by [`-X showrefcount`](../using/cmdline.html#cmdoption-X) command line option.

        Needs a [debug build of Python](../using/configure.html#debug-build) (the `Py_REF_DEBUG`
        macro must be defined).

        Default: `0`.

    int site\_import
    :   Import the [`site`](../library/site.html#module-site "site: Module responsible for site-specific configuration.") module at startup?

        If equal to zero, disable the import of the module site and the
        site-dependent manipulations of [`sys.path`](../library/sys.html#sys.path "sys.path") that it entails.

        Also disable these manipulations if the [`site`](../library/site.html#module-site "site: Module responsible for site-specific configuration.") module is explicitly
        imported later (call [`site.main()`](../library/site.html#site.main "site.main") if you want them to be triggered).

        Set to `0` by the [`-S`](../using/cmdline.html#cmdoption-S) command line option.

        [`sys.flags.no_site`](../library/sys.html#sys.flags "sys.flags") is set to the inverted value of
        [`site_import`](#c.PyConfig.site_import "PyConfig.site_import").

        Default: `1`.

    int skip\_source\_first\_line
    :   If non-zero, skip the first line of the [`PyConfig.run_filename`](#c.PyConfig.run_filename "PyConfig.run_filename")
        source.

        It allows the usage of non-Unix forms of `#!cmd`. This is intended for
        a DOS specific hack only.

        Set to `1` by the [`-x`](../using/cmdline.html#cmdoption-x) command line option.

        Default: `0`.

    wchar\_t \*stdio\_encoding

    wchar\_t \*stdio\_errors
    :   Encoding and encoding errors of [`sys.stdin`](../library/sys.html#sys.stdin "sys.stdin"), [`sys.stdout`](../library/sys.html#sys.stdout "sys.stdout") and
        [`sys.stderr`](../library/sys.html#sys.stderr "sys.stderr") (but [`sys.stderr`](../library/sys.html#sys.stderr "sys.stderr") always uses
        `"backslashreplace"` error handler).

        Use the [`PYTHONIOENCODING`](../using/cmdline.html#envvar-PYTHONIOENCODING) environment variable if it is
        non-empty.

        Default encoding:

        Default error handler:

        * On Windows: use `"surrogateescape"`.
        * `"surrogateescape"` if [`PyPreConfig.utf8_mode`](#c.PyPreConfig.utf8_mode "PyPreConfig.utf8_mode") is non-zero,
          or if the LC\_CTYPE locale is “C” or “POSIX”.
        * `"strict"` otherwise.

        See also [`PyConfig.legacy_windows_stdio`](#c.PyConfig.legacy_windows_stdio "PyConfig.legacy_windows_stdio").

    int tracemalloc
    :   Enable tracemalloc?

        If non-zero, call [`tracemalloc.start()`](../library/tracemalloc.html#tracemalloc.start "tracemalloc.start") at startup.

        Set by [`-X tracemalloc=N`](../using/cmdline.html#cmdoption-X) command line option and by the
        [`PYTHONTRACEMALLOC`](../using/cmdline.html#envvar-PYTHONTRACEMALLOC) environment variable.

        Default: `-1` in Python mode, `0` in isolated mode.

    int perf\_profiling
    :   Enable compatibility mode with the perf profiler?

        If non-zero, initialize the perf trampoline. See [Python support for the Linux perf profiler](../howto/perf_profiling.html#perf-profiling)
        for more information.

        Set by [`-X perf`](../using/cmdline.html#cmdoption-X) command-line option and by the
        [`PYTHON_PERF_JIT_SUPPORT`](../using/cmdline.html#envvar-PYTHON_PERF_JIT_SUPPORT) environment variable for perf support
        with stack pointers and [`-X perf_jit`](../using/cmdline.html#cmdoption-X) command-line option
        and by the [`PYTHON_PERF_JIT_SUPPORT`](../using/cmdline.html#envvar-PYTHON_PERF_JIT_SUPPORT) environment variable for perf
        support with DWARF JIT information.

        Default: `-1`.

    int use\_environment
    :   Use [environment variables](../using/cmdline.html#using-on-envvars)?

        If equals to zero, ignore the [environment variables](../using/cmdline.html#using-on-envvars).

        Set to `0` by the [`-E`](../using/cmdline.html#cmdoption-E) environment variable.

        Default: `1` in Python config and `0` in isolated config.

    int user\_site\_directory
    :   If non-zero, add the user site directory to [`sys.path`](../library/sys.html#sys.path "sys.path").

        Set to `0` by the [`-s`](../using/cmdline.html#cmdoption-s) and [`-I`](../using/cmdline.html#cmdoption-I) command line options.

        Set to `0` by the [`PYTHONNOUSERSITE`](../using/cmdline.html#envvar-PYTHONNOUSERSITE) environment variable.

        Default: `1` in Python mode, `0` in isolated mode.

    int verbose
    :   Verbose mode. If greater than `0`, print a message each time a module is
        imported, showing the place (filename or built-in module) from which
        it is loaded.

        If greater than or equal to `2`, print a message for each file that is
        checked for when searching for a module. Also provides information on
        module cleanup at exit.

        Incremented by the [`-v`](../using/cmdline.html#cmdoption-v) command line option.

        Set by the [`PYTHONVERBOSE`](../using/cmdline.html#envvar-PYTHONVERBOSE) environment variable value.

        Default: `0`.

    [PyWideStringList](#c.PyWideStringList "PyWideStringList") warnoptions
    :   Options of the [`warnings`](../library/warnings.html#module-warnings "warnings: Issue warning messages and control their disposition.") module to build warnings filters, lowest
        to highest priority: [`sys.warnoptions`](../library/sys.html#sys.warnoptions "sys.warnoptions").

        The [`warnings`](../library/warnings.html#module-warnings "warnings: Issue warning messages and control their disposition.") module adds [`sys.warnoptions`](../library/sys.html#sys.warnoptions "sys.warnoptions") in the reverse
        order: the last [`PyConfig.warnoptions`](#c.PyConfig.warnoptions "PyConfig.warnoptions") item becomes the first
        item of `warnings.filters` which is checked first (highest
        priority).

        The [`-W`](../using/cmdline.html#cmdoption-W) command line options adds its value to
        [`warnoptions`](#c.PyConfig.warnoptions "PyConfig.warnoptions"), it can be used multiple times.

        The [`PYTHONWARNINGS`](../using/cmdline.html#envvar-PYTHONWARNINGS) environment variable can also be used to add
        warning options. Multiple options can be specified, separated by commas
        (`,`).

        Default: empty list.

    int write\_bytecode
    :   If equal to `0`, Python won’t try to write `.pyc` files on the import of
        source modules.

        Set to `0` by the [`-B`](../using/cmdline.html#cmdoption-B) command line option and the
        [`PYTHONDONTWRITEBYTECODE`](../using/cmdline.html#envvar-PYTHONDONTWRITEBYTECODE) environment variable.

        [`sys.dont_write_bytecode`](../library/sys.html#sys.dont_write_bytecode "sys.dont_write_bytecode") is initialized to the inverted value of
        [`write_bytecode`](#c.PyConfig.write_bytecode "PyConfig.write_bytecode").

        Default: `1`.

    [PyWideStringList](#c.PyWideStringList "PyWideStringList") xoptions
    :   Values of the [`-X`](../using/cmdline.html#cmdoption-X) command line options: [`sys._xoptions`](../library/sys.html#sys._xoptions "sys._xoptions").

        Default: empty list.

If [`parse_argv`](#c.PyConfig.parse_argv "PyConfig.parse_argv") is non-zero, [`argv`](#c.PyConfig.argv "PyConfig.argv")
arguments are parsed the same way the regular Python parses [command line
arguments](../using/cmdline.html#using-on-cmdline), and Python arguments are stripped from
[`argv`](#c.PyConfig.argv "PyConfig.argv").

The [`xoptions`](#c.PyConfig.xoptions "PyConfig.xoptions") options are parsed to set other options: see
the [`-X`](../using/cmdline.html#cmdoption-X) command line option.

Changed in version 3.9: The `show_alloc_count` field has been removed.

Initialization with PyConfig
----------------------------

Initializing the interpreter from a populated configuration struct is handled
by calling [`Py_InitializeFromConfig()`](init.html#c.Py_InitializeFromConfig "Py_InitializeFromConfig").

The caller is responsible to handle exceptions (error or exit) using
[`PyStatus_Exception()`](#c.PyStatus_Exception "PyStatus_Exception") and [`Py_ExitStatusException()`](#c.Py_ExitStatusException "Py_ExitStatusException").

If [`PyImport_FrozenModules()`](import.html#c.PyImport_FrozenModules "PyImport_FrozenModules"), [`PyImport_AppendInittab()`](import.html#c.PyImport_AppendInittab "PyImport_AppendInittab") or
[`PyImport_ExtendInittab()`](import.html#c.PyImport_ExtendInittab "PyImport_ExtendInittab") are used, they must be set or called after
Python preinitialization and before the Python initialization. If Python is
initialized multiple times, [`PyImport_AppendInittab()`](import.html#c.PyImport_AppendInittab "PyImport_AppendInittab") or
[`PyImport_ExtendInittab()`](import.html#c.PyImport_ExtendInittab "PyImport_ExtendInittab") must be called before each Python
initialization.

The current configuration (`PyConfig` type) is stored in
`PyInterpreterState.config`.

Example setting the program name:

```
void init_python(void)
{
    PyStatus status;

    PyConfig config;
    PyConfig_InitPythonConfig(&config);

    /* Set the program name. Implicitly preinitialize Python. */
    status = PyConfig_SetString(&config, &config.program_name,
                                L"/path/to/my_program");
    if (PyStatus_Exception(status)) {
        goto exception;
    }

    status = Py_InitializeFromConfig(&config);
    if (PyStatus_Exception(status)) {
        goto exception;
    }
    PyConfig_Clear(&config);
    return;

exception:
    PyConfig_Clear(&config);
    Py_ExitStatusException(status);
}

```

More complete example modifying the default configuration, read the
configuration, and then override some parameters. Note that since
3.11, many parameters are not calculated until initialization, and
so values cannot be read from the configuration structure. Any values
set before initialize is called will be left unchanged by
initialization:

```
PyStatus init_python(const char *program_name)
{
    PyStatus status;

    PyConfig config;
    PyConfig_InitPythonConfig(&config);

    /* Set the program name before reading the configuration
       (decode byte string from the locale encoding).

       Implicitly preinitialize Python. */
    status = PyConfig_SetBytesString(&config, &config.program_name,
                                     program_name);
    if (PyStatus_Exception(status)) {
        goto done;
    }

    /* Read all configuration at once */
    status = PyConfig_Read(&config);
    if (PyStatus_Exception(status)) {
        goto done;
    }

    /* Specify sys.path explicitly */
    /* If you want to modify the default set of paths, finish
       initialization first and then use PySys_GetObject("path") */
    config.module_search_paths_set = 1;
    status = PyWideStringList_Append(&config.module_search_paths,
                                     L"/path/to/stdlib");
    if (PyStatus_Exception(status)) {
        goto done;
    }
    status = PyWideStringList_Append(&config.module_search_paths,
                                     L"/path/to/more/modules");
    if (PyStatus_Exception(status)) {
        goto done;
    }

    /* Override executable computed by PyConfig_Read() */
    status = PyConfig_SetString(&config, &config.executable,
                                L"/path/to/my_executable");
    if (PyStatus_Exception(status)) {
        goto done;
    }

    status = Py_InitializeFromConfig(&config);

done:
    PyConfig_Clear(&config);
    return status;
}

```

Isolated Configuration
----------------------

[`PyPreConfig_InitIsolatedConfig()`](#c.PyPreConfig_InitIsolatedConfig "PyPreConfig_InitIsolatedConfig") and
[`PyConfig_InitIsolatedConfig()`](#c.PyConfig_InitIsolatedConfig "PyConfig_InitIsolatedConfig") functions create a configuration to
isolate Python from the system. For example, to embed Python into an
application.

This configuration ignores global configuration variables, environment
variables, command line arguments ([`PyConfig.argv`](#c.PyConfig.argv "PyConfig.argv") is not parsed)
and user site directory. The C standard streams (ex: `stdout`) and the
LC\_CTYPE locale are left unchanged. Signal handlers are not installed.

Configuration files are still used with this configuration to determine
paths that are unspecified. Ensure [`PyConfig.home`](#c.PyConfig.home "PyConfig.home") is specified
to avoid computing the default path configuration.

Python Path Configuration
-------------------------

[`PyConfig`](#c.PyConfig "PyConfig") contains multiple fields for the path configuration:

If at least one “output field” is not set, Python calculates the path
configuration to fill unset fields. If
[`module_search_paths_set`](#c.PyConfig.module_search_paths_set "PyConfig.module_search_paths_set") is equal to `0`,
[`module_search_paths`](#c.PyConfig.module_search_paths "PyConfig.module_search_paths") is overridden and
[`module_search_paths_set`](#c.PyConfig.module_search_paths_set "PyConfig.module_search_paths_set") is set to `1`.

It is possible to completely ignore the function calculating the default
path configuration by setting explicitly all path configuration output
fields listed above. A string is considered as set even if it is non-empty.
`module_search_paths` is considered as set if
`module_search_paths_set` is set to `1`. In this case,
`module_search_paths` will be used without modification.

Set [`pathconfig_warnings`](#c.PyConfig.pathconfig_warnings "PyConfig.pathconfig_warnings") to `0` to suppress warnings when
calculating the path configuration (Unix only, Windows does not log any warning).

If [`base_prefix`](#c.PyConfig.base_prefix "PyConfig.base_prefix") or [`base_exec_prefix`](#c.PyConfig.base_exec_prefix "PyConfig.base_exec_prefix")
fields are not set, they inherit their value from [`prefix`](#c.PyConfig.prefix "PyConfig.prefix")
and [`exec_prefix`](#c.PyConfig.exec_prefix "PyConfig.exec_prefix") respectively.

[`Py_RunMain()`](init.html#c.Py_RunMain "Py_RunMain") and [`Py_Main()`](init.html#c.Py_Main "Py_Main") modify [`sys.path`](../library/sys.html#sys.path "sys.path"):

If [`site_import`](#c.PyConfig.site_import "PyConfig.site_import") is non-zero, [`sys.path`](../library/sys.html#sys.path "sys.path") can be
modified by the [`site`](../library/site.html#module-site "site: Module responsible for site-specific configuration.") module. If
[`user_site_directory`](#c.PyConfig.user_site_directory "PyConfig.user_site_directory") is non-zero and the user’s
site-package directory exists, the [`site`](../library/site.html#module-site "site: Module responsible for site-specific configuration.") module appends the user’s
site-package directory to [`sys.path`](../library/sys.html#sys.path "sys.path").

The following configuration files are used by the path configuration:

If a `._pth` file is present:

The `__PYVENV_LAUNCHER__` environment variable is used to set
[`PyConfig.base_executable`](#c.PyConfig.base_executable "PyConfig.base_executable").

Py\_GetArgcArgv()
-----------------

void Py\_GetArgcArgv(int \*argc, wchar\_t \*\*\*argv)
:   Get the original command line arguments, before Python modified them.

    See also [`PyConfig.orig_argv`](#c.PyConfig.orig_argv "PyConfig.orig_argv") member.

Multi-Phase Initialization Private Provisional API
--------------------------------------------------

This section is a private provisional API introducing multi-phase
initialization, the core feature of [**PEP 432**](https://peps.python.org/pep-0432/):

* “Core” initialization phase, “bare minimum Python”:
* “Main” initialization phase, Python is fully initialized:

Private provisional API:

[PyStatus](#c.PyStatus "PyStatus") \_Py\_InitializeMain(void)
:   Move to the “Main” initialization phase, finish the Python initialization.

No module is imported during the “Core” phase and the `importlib` module is
not configured: the [Path Configuration](#init-path-config) is only
applied during the “Main” phase. It may allow to customize Python in Python to
override or tune the [Path Configuration](#init-path-config), maybe
install a custom [`sys.meta_path`](../library/sys.html#sys.meta_path "sys.meta_path") importer or an import hook, etc.

It may become possible to calculate the [Path Configuration](#init-path-config) in Python, after the Core phase and before the Main phase,
which is one of the [**PEP 432**](https://peps.python.org/pep-0432/) motivation.

The “Core” phase is not properly defined: what should be and what should
not be available at this phase is not specified yet. The API is marked
as private and provisional: the API can be modified or even be removed
anytime until a proper public API is designed.

Example running Python code between “Core” and “Main” initialization
phases:

```
void init_python(void)
{
    PyStatus status;

    PyConfig config;
    PyConfig_InitPythonConfig(&config);
    config._init_main = 0;

    /* ... customize 'config' configuration ... */

    status = Py_InitializeFromConfig(&config);
    PyConfig_Clear(&config);
    if (PyStatus_Exception(status)) {
        Py_ExitStatusException(status);
    }

    /* Use sys.stderr because sys.stdout is only created
       by _Py_InitializeMain() */
    int res = PyRun_SimpleString(
        "import sys; "
        "print('Run Python code before _Py_InitializeMain', "
               "file=sys.stderr)");
    if (res < 0) {
        exit(1);
    }

    /* ... put more configuration code here ... */

    status = _Py_InitializeMain();
    if (PyStatus_Exception(status)) {
        Py_ExitStatusException(status);
    }
}

```