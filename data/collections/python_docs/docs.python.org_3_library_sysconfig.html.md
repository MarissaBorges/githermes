`sysconfig` — Provide access to Python’s configuration information
==================================================================

**Source code:** [Lib/sysconfig](https://github.com/python/cpython/tree/3.13/Lib/sysconfig)

---

The [`sysconfig`](#module-sysconfig "sysconfig: Python's configuration information") module provides access to Python’s configuration
information like the list of installation paths and the configuration variables
relevant for the current platform.

Configuration variables
-----------------------

A Python distribution contains a `Makefile` and a `pyconfig.h`
header file that are necessary to build both the Python binary itself and
third-party C extensions compiled using `setuptools`.

[`sysconfig`](#module-sysconfig "sysconfig: Python's configuration information") puts all variables found in these files in a dictionary that
can be accessed using [`get_config_vars()`](#sysconfig.get_config_vars "sysconfig.get_config_vars") or [`get_config_var()`](#sysconfig.get_config_var "sysconfig.get_config_var").

Notice that on Windows, it’s a much smaller set.

sysconfig.get\_config\_vars(*\*args*)
:   With no arguments, return a dictionary of all configuration variables
    relevant for the current platform.

    With arguments, return a list of values that result from looking up each
    argument in the configuration variable dictionary.

    For each argument, if the value is not found, return `None`.

sysconfig.get\_config\_var(*name*)
:   Return the value of a single variable *name*. Equivalent to
    `get_config_vars().get(name)`.

    If *name* is not found, return `None`.

Example of usage:

Copy

```
>>> import sysconfig
>>> sysconfig.get_config_var('Py_ENABLE_SHARED')
0
>>> sysconfig.get_config_var('LIBDIR')
'/usr/local/lib'
>>> sysconfig.get_config_vars('AR', 'CXX')
['ar', 'g++']

```

Installation paths
------------------

Python uses an installation scheme that differs depending on the platform and on
the installation options. These schemes are stored in [`sysconfig`](#module-sysconfig "sysconfig: Python's configuration information") under
unique identifiers based on the value returned by [`os.name`](os.html#os.name "os.name").
The schemes are used by package installers to determine where to copy files to.

Python currently supports nine schemes:

* *posix\_prefix*: scheme for POSIX platforms like Linux or macOS. This is
  the default scheme used when Python or a component is installed.
* *posix\_home*: scheme for POSIX platforms, when the *home* option is used.
  This scheme defines paths located under a specific home prefix.
* *posix\_user*: scheme for POSIX platforms, when the *user* option is used.
  This scheme defines paths located under the user’s home directory
  ([`site.USER_BASE`](site.html#site.USER_BASE "site.USER_BASE")).
* *posix\_venv*: scheme for [`Python virtual environments`](venv.html#module-venv "venv: Creation of virtual environments.") on POSIX
  platforms; by default it is the same as *posix\_prefix*.
* *nt*: scheme for Windows.
  This is the default scheme used when Python or a component is installed.
* *nt\_user*: scheme for Windows, when the *user* option is used.
* *nt\_venv*: scheme for [`Python virtual environments`](venv.html#module-venv "venv: Creation of virtual environments.") on Windows;
  by default it is the same as *nt*.
* *venv*: a scheme with values from either *posix\_venv* or *nt\_venv* depending
  on the platform Python runs on.
* *osx\_framework\_user*: scheme for macOS, when the *user* option is used.

Each scheme is itself composed of a series of paths and each path has a unique
identifier. Python currently uses eight paths:

* *stdlib*: directory containing the standard Python library files that are not
  platform-specific.
* *platstdlib*: directory containing the standard Python library files that are
  platform-specific.
* *platlib*: directory for site-specific, platform-specific files.
* *purelib*: directory for site-specific, non-platform-specific files (‘pure’ Python).
* *include*: directory for non-platform-specific header files for
  the Python C-API.
* *platinclude*: directory for platform-specific header files for
  the Python C-API.
* *scripts*: directory for script files.
* *data*: directory for data files.

User scheme
-----------

This scheme is designed to be the most convenient solution for users that don’t
have write permission to the global site-packages directory or don’t want to
install into it.

Files will be installed into subdirectories of [`site.USER_BASE`](site.html#site.USER_BASE "site.USER_BASE") (written
as `userbase` hereafter). This scheme installs pure Python modules and
extension modules in the same location (also known as [`site.USER_SITE`](site.html#site.USER_SITE "site.USER_SITE")).

### `posix_user`

| Path | Installation directory |
| --- | --- |
| *stdlib* | `userbase/lib/pythonX.Y` |
| *platstdlib* | `userbase/lib/pythonX.Y` |
| *platlib* | `userbase/lib/pythonX.Y/site-packages` |
| *purelib* | `userbase/lib/pythonX.Y/site-packages` |
| *include* | `userbase/include/pythonX.Y` |
| *scripts* | `userbase/bin` |
| *data* | `userbase` |

### `nt_user`

| Path | Installation directory |
| --- | --- |
| *stdlib* | `userbase\PythonXY` |
| *platstdlib* | `userbase\PythonXY` |
| *platlib* | `userbase\PythonXY\site-packages` |
| *purelib* | `userbase\PythonXY\site-packages` |
| *include* | `userbase\PythonXY\Include` |
| *scripts* | `userbase\PythonXY\Scripts` |
| *data* | `userbase` |

### `osx_framework_user`

| Path | Installation directory |
| --- | --- |
| *stdlib* | `userbase/lib/python` |
| *platstdlib* | `userbase/lib/python` |
| *platlib* | `userbase/lib/python/site-packages` |
| *purelib* | `userbase/lib/python/site-packages` |
| *include* | `userbase/include/pythonX.Y` |
| *scripts* | `userbase/bin` |
| *data* | `userbase` |

Home scheme
-----------

The idea behind the “home scheme” is that you build and maintain a personal
stash of Python modules. This scheme’s name is derived from the idea of a
“home” directory on Unix, since it’s not unusual for a Unix user to make their
home directory have a layout similar to `/usr/` or `/usr/local/`.
This scheme can be used by anyone, regardless of the operating system they
are installing for.

### `posix_home`

| Path | Installation directory |
| --- | --- |
| *stdlib* | `home/lib/python` |
| *platstdlib* | `home/lib/python` |
| *platlib* | `home/lib/python` |
| *purelib* | `home/lib/python` |
| *include* | `home/include/python` |
| *platinclude* | `home/include/python` |
| *scripts* | `home/bin` |
| *data* | `home` |

Prefix scheme
-------------

The “prefix scheme” is useful when you wish to use one Python installation to
perform the build/install (i.e., to run the setup script), but install modules
into the third-party module directory of a different Python installation (or
something that looks like a different Python installation). If this sounds a
trifle unusual, it is—that’s why the user and home schemes come before. However,
there are at least two known cases where the prefix scheme will be useful.

First, consider that many Linux distributions put Python in `/usr`, rather
than the more traditional `/usr/local`. This is entirely appropriate,
since in those cases Python is part of “the system” rather than a local add-on.
However, if you are installing Python modules from source, you probably want
them to go in `/usr/local/lib/python2.X` rather than
`/usr/lib/python2.X`.

Another possibility is a network filesystem where the name used to write to a
remote directory is different from the name used to read it: for example, the
Python interpreter accessed as `/usr/local/bin/python` might search for
modules in `/usr/local/lib/python2.X`, but those modules would have to
be installed to, say, `/mnt/@server/export/lib/python2.X`.

### `posix_prefix`

| Path | Installation directory |
| --- | --- |
| *stdlib* | `prefix/lib/pythonX.Y` |
| *platstdlib* | `prefix/lib/pythonX.Y` |
| *platlib* | `prefix/lib/pythonX.Y/site-packages` |
| *purelib* | `prefix/lib/pythonX.Y/site-packages` |
| *include* | `prefix/include/pythonX.Y` |
| *platinclude* | `prefix/include/pythonX.Y` |
| *scripts* | `prefix/bin` |
| *data* | `prefix` |

### `nt`

| Path | Installation directory |
| --- | --- |
| *stdlib* | `prefix\Lib` |
| *platstdlib* | `prefix\Lib` |
| *platlib* | `prefix\Lib\site-packages` |
| *purelib* | `prefix\Lib\site-packages` |
| *include* | `prefix\Include` |
| *platinclude* | `prefix\Include` |
| *scripts* | `prefix\Scripts` |
| *data* | `prefix` |

Installation path functions
---------------------------

[`sysconfig`](#module-sysconfig "sysconfig: Python's configuration information") provides some functions to determine these installation paths.

sysconfig.get\_scheme\_names()
:   Return a tuple containing all schemes currently supported in
    [`sysconfig`](#module-sysconfig "sysconfig: Python's configuration information").

sysconfig.get\_default\_scheme()
:   Return the default scheme name for the current platform.

    Added in version 3.10: This function was previously named `_get_default_scheme()` and
    considered an implementation detail.

    Changed in version 3.11: When Python runs from a virtual environment,
    the *venv* scheme is returned.

sysconfig.get\_preferred\_scheme(*key*)
:   Return a preferred scheme name for an installation layout specified by *key*.

    *key* must be either `"prefix"`, `"home"`, or `"user"`.

    The return value is a scheme name listed in [`get_scheme_names()`](#sysconfig.get_scheme_names "sysconfig.get_scheme_names"). It
    can be passed to [`sysconfig`](#module-sysconfig "sysconfig: Python's configuration information") functions that take a *scheme* argument,
    such as [`get_paths()`](#sysconfig.get_paths "sysconfig.get_paths").

    Changed in version 3.11: When Python runs from a virtual environment and `key="prefix"`,
    the *venv* scheme is returned.

sysconfig.\_get\_preferred\_schemes()
:   Return a dict containing preferred scheme names on the current platform.
    Python implementers and redistributors may add their preferred schemes to
    the `_INSTALL_SCHEMES` module-level global value, and modify this function
    to return those scheme names, to e.g. provide different schemes for system
    and language package managers to use, so packages installed by either do not
    mix with those by the other.

    End users should not use this function, but [`get_default_scheme()`](#sysconfig.get_default_scheme "sysconfig.get_default_scheme") and
    [`get_preferred_scheme()`](#sysconfig.get_preferred_scheme "sysconfig.get_preferred_scheme") instead.

sysconfig.get\_path\_names()
:   Return a tuple containing all path names currently supported in
    [`sysconfig`](#module-sysconfig "sysconfig: Python's configuration information").

sysconfig.get\_path(*name*[, *scheme*[, *vars*[, *expand*]]])
:   Return an installation path corresponding to the path *name*, from the
    install scheme named *scheme*.

    *name* has to be a value from the list returned by [`get_path_names()`](#sysconfig.get_path_names "sysconfig.get_path_names").

    [`sysconfig`](#module-sysconfig "sysconfig: Python's configuration information") stores installation paths corresponding to each path name,
    for each platform, with variables to be expanded. For instance the *stdlib*
    path for the *nt* scheme is: `{base}/Lib`.

    [`get_path()`](#sysconfig.get_path "sysconfig.get_path") will use the variables returned by [`get_config_vars()`](#sysconfig.get_config_vars "sysconfig.get_config_vars")
    to expand the path. All variables have default values for each platform so
    one may call this function and get the default value.

    If *scheme* is provided, it must be a value from the list returned by
    [`get_scheme_names()`](#sysconfig.get_scheme_names "sysconfig.get_scheme_names"). Otherwise, the default scheme for the current
    platform is used.

    If *vars* is provided, it must be a dictionary of variables that will update
    the dictionary returned by [`get_config_vars()`](#sysconfig.get_config_vars "sysconfig.get_config_vars").

    If *expand* is set to `False`, the path will not be expanded using the
    variables.

    If *name* is not found, raise a [`KeyError`](exceptions.html#KeyError "KeyError").

sysconfig.get\_paths([*scheme*[, *vars*[, *expand*]]])
:   Return a dictionary containing all installation paths corresponding to an
    installation scheme. See [`get_path()`](#sysconfig.get_path "sysconfig.get_path") for more information.

    If *scheme* is not provided, will use the default scheme for the current
    platform.

    If *vars* is provided, it must be a dictionary of variables that will
    update the dictionary used to expand the paths.

    If *expand* is set to false, the paths will not be expanded.

    If *scheme* is not an existing scheme, [`get_paths()`](#sysconfig.get_paths "sysconfig.get_paths") will raise a
    [`KeyError`](exceptions.html#KeyError "KeyError").

Other functions
---------------

sysconfig.get\_python\_version()
:   Return the `MAJOR.MINOR` Python version number as a string. Similar to
    `'%d.%d' % sys.version_info[:2]`.

sysconfig.get\_platform()
:   Return a string that identifies the current platform.

    This is used mainly to distinguish platform-specific build directories and
    platform-specific built distributions. Typically includes the OS name and
    version and the architecture (as supplied by [`os.uname()`](os.html#os.uname "os.uname")), although the
    exact information included depends on the OS; e.g., on Linux, the kernel
    version isn’t particularly important.

    Examples of returned values:

    * linux-i586
    * linux-alpha (?)
    * solaris-2.6-sun4u

    Windows will return one of:

    * win-amd64 (64-bit Windows on AMD64, aka x86\_64, Intel64, and EM64T)
    * win-arm64 (64-bit Windows on ARM64, aka AArch64)
    * win32 (all others - specifically, sys.platform is returned)

    macOS can return:

    * macosx-10.6-ppc
    * macosx-10.4-ppc64
    * macosx-10.3-i386
    * macosx-10.4-fat

    For other non-POSIX platforms, currently just returns [`sys.platform`](sys.html#sys.platform "sys.platform").

sysconfig.is\_python\_build()
:   Return `True` if the running Python interpreter was built from source and
    is being run from its built location, and not from a location resulting from
    e.g. running `make install` or installing via a binary installer.

sysconfig.parse\_config\_h(*fp*[, *vars*])
:   Parse a `config.h`-style file.

    *fp* is a file-like object pointing to the `config.h`-like file.

    A dictionary containing name/value pairs is returned. If an optional
    dictionary is passed in as the second argument, it is used instead of a new
    dictionary, and updated with the values read in the file.

sysconfig.get\_config\_h\_filename()
:   Return the path of `pyconfig.h`.

sysconfig.get\_makefile\_filename()
:   Return the path of `Makefile`.

Command-line usage
------------------

You can use [`sysconfig`](#module-sysconfig "sysconfig: Python's configuration information") as a script with Python’s *-m* option:

```
$ python -m sysconfig
Platform: "macosx-10.4-i386"
Python version: "3.2"
Current installation scheme: "posix_prefix"

Paths:
        data = "/usr/local"
        include = "/Users/tarek/Dev/svn.python.org/py3k/Include"
        platinclude = "."
        platlib = "/usr/local/lib/python3.2/site-packages"
        platstdlib = "/usr/local/lib/python3.2"
        purelib = "/usr/local/lib/python3.2/site-packages"
        scripts = "/usr/local/bin"
        stdlib = "/usr/local/lib/python3.2"

Variables:
        AC_APPLE_UNIVERSAL_BUILD = "0"
        AIX_GENUINE_CPLUSPLUS = "0"
        AR = "ar"
        ARFLAGS = "rc"
        ...

```

This call will print in the standard output the information returned by
[`get_platform()`](#sysconfig.get_platform "sysconfig.get_platform"), [`get_python_version()`](#sysconfig.get_python_version "sysconfig.get_python_version"), [`get_path()`](#sysconfig.get_path "sysconfig.get_path") and
[`get_config_vars()`](#sysconfig.get_config_vars "sysconfig.get_config_vars").