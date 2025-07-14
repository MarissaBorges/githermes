This article explains the new features in Python 3.10, compared to 3.9.
Python 3.10 was released on October 4, 2021.
For full details, see the [changelog](changelog.html#changelog).

Improved Modules
----------------

### asyncio

Add missing `connect_accepted_socket()`
method.
(Contributed by Alex Grönholm in [bpo-41332](https://bugs.python.org/issue?@action=redirect&bpo=41332).)

### argparse

Misleading phrase “optional arguments” was replaced with “options” in argparse help. Some tests might require adaptation if they rely on exact output match.
(Contributed by Raymond Hettinger in [bpo-9694](https://bugs.python.org/issue?@action=redirect&bpo=9694).)

### array

The [`index()`](../library/array.html#array.array.index "array.array.index") method of [`array.array`](../library/array.html#array.array "array.array") now has
optional *start* and *stop* parameters.
(Contributed by Anders Lorentsen and Zackery Spytz in [bpo-31956](https://bugs.python.org/issue?@action=redirect&bpo=31956).)

### asynchat, asyncore, smtpd

These modules have been marked as deprecated in their module documentation
since Python 3.6. An import-time [`DeprecationWarning`](../library/exceptions.html#DeprecationWarning "DeprecationWarning") has now been
added to all three of these modules.

### bdb

Add `clearBreakpoints()` to reset all set breakpoints.
(Contributed by Irit Katriel in [bpo-24160](https://bugs.python.org/issue?@action=redirect&bpo=24160).)

### bisect

Added the possibility of providing a *key* function to the APIs in the [`bisect`](../library/bisect.html#module-bisect "bisect: Array bisection algorithms for binary searching.")
module. (Contributed by Raymond Hettinger in [bpo-4356](https://bugs.python.org/issue?@action=redirect&bpo=4356).)

### contextlib

Add a [`contextlib.aclosing()`](../library/contextlib.html#contextlib.aclosing "contextlib.aclosing") context manager to safely close async generators
and objects representing asynchronously released resources.
(Contributed by Joongi Kim and John Belmonte in [bpo-41229](https://bugs.python.org/issue?@action=redirect&bpo=41229).)

Add asynchronous context manager support to [`contextlib.nullcontext()`](../library/contextlib.html#contextlib.nullcontext "contextlib.nullcontext").
(Contributed by Tom Gringauz in [bpo-41543](https://bugs.python.org/issue?@action=redirect&bpo=41543).)

Add [`AsyncContextDecorator`](../library/contextlib.html#contextlib.AsyncContextDecorator "contextlib.AsyncContextDecorator"), for supporting usage of async
context managers as decorators.

### dataclasses

#### Keyword-only fields

dataclasses now supports fields that are keyword-only in the
generated \_\_init\_\_ method. There are a number of ways of specifying
keyword-only fields.

You can say that every field is keyword-only:

Copy

```
from dataclasses import dataclass

@dataclass(kw_only=True)
class Birthday:
    name: str
    birthday: datetime.date

```

Both `name` and `birthday` are keyword-only parameters to the
generated \_\_init\_\_ method.

You can specify keyword-only on a per-field basis:

Copy

```
from dataclasses import dataclass, field

@dataclass
class Birthday:
    name: str
    birthday: datetime.date = field(kw_only=True)

```

Here only `birthday` is keyword-only. If you set `kw_only` on
individual fields, be aware that there are rules about re-ordering
fields due to keyword-only fields needing to follow non-keyword-only
fields. See the full dataclasses documentation for details.

You can also specify that all fields following a KW\_ONLY marker are
keyword-only. This will probably be the most common usage:

Copy

```
from dataclasses import dataclass, KW_ONLY

@dataclass
class Point:
    x: float
    y: float
    _: KW_ONLY
    z: float = 0.0
    t: float = 0.0

```

Here, `z` and `t` are keyword-only parameters, while `x` and
`y` are not.
(Contributed by Eric V. Smith in [bpo-43532](https://bugs.python.org/issue?@action=redirect&bpo=43532).)

### distutils

The entire `distutils` package is deprecated, to be removed in Python
3.12. Its functionality for specifying package builds has already been
completely replaced by third-party packages `setuptools` and
`packaging`, and most other commonly used APIs are available elsewhere
in the standard library (such as [`platform`](../library/platform.html#module-platform "platform: Retrieves as much platform identifying data as possible."), [`shutil`](../library/shutil.html#module-shutil "shutil: High-level file operations, including copying."),
[`subprocess`](../library/subprocess.html#module-subprocess "subprocess: Subprocess management.") or [`sysconfig`](../library/sysconfig.html#module-sysconfig "sysconfig: Python's configuration information")). There are no plans to migrate
any other functionality from `distutils`, and applications that are
using other functions should plan to make private copies of the code.
Refer to [**PEP 632**](https://peps.python.org/pep-0632/) for discussion.

The `bdist_wininst` command deprecated in Python 3.8 has been removed.
The `bdist_wheel` command is now recommended to distribute binary packages
on Windows.
(Contributed by Victor Stinner in [bpo-42802](https://bugs.python.org/issue?@action=redirect&bpo=42802).)

### doctest

When a module does not define `__loader__`, fall back to `__spec__.loader`.
(Contributed by Brett Cannon in [bpo-42133](https://bugs.python.org/issue?@action=redirect&bpo=42133).)

### enum

[`Enum`](../library/enum.html#enum.Enum "enum.Enum") [`__repr__()`](../reference/datamodel.html#object.__repr__ "object.__repr__") now returns `enum_name.member_name` and
[`__str__()`](../reference/datamodel.html#object.__str__ "object.__str__") now returns `member_name`. Stdlib enums available as
module constants have a [`repr()`](../library/functions.html#repr "repr") of `module_name.member_name`.
(Contributed by Ethan Furman in [bpo-40066](https://bugs.python.org/issue?@action=redirect&bpo=40066).)

Add [`enum.StrEnum`](../library/enum.html#enum.StrEnum "enum.StrEnum") for enums where all members are strings.
(Contributed by Ethan Furman in [bpo-41816](https://bugs.python.org/issue?@action=redirect&bpo=41816).)

### faulthandler

The [`faulthandler`](../library/faulthandler.html#module-faulthandler "faulthandler: Dump the Python traceback.") module now detects if a fatal error occurs during a
garbage collector collection.
(Contributed by Victor Stinner in [bpo-44466](https://bugs.python.org/issue?@action=redirect&bpo=44466).)

### glob

Add the *root\_dir* and *dir\_fd* parameters in [`glob()`](../library/glob.html#glob.glob "glob.glob") and
[`iglob()`](../library/glob.html#glob.iglob "glob.iglob") which allow to specify the root directory for searching.
(Contributed by Serhiy Storchaka in [bpo-38144](https://bugs.python.org/issue?@action=redirect&bpo=38144).)

### hashlib

The hashlib module requires OpenSSL 1.1.1 or newer.
(Contributed by Christian Heimes in [**PEP 644**](https://peps.python.org/pep-0644/) and [bpo-43669](https://bugs.python.org/issue?@action=redirect&bpo=43669).)

The hashlib module has preliminary support for OpenSSL 3.0.0.
(Contributed by Christian Heimes in [bpo-38820](https://bugs.python.org/issue?@action=redirect&bpo=38820) and other issues.)

The pure-Python fallback of [`pbkdf2_hmac()`](../library/hashlib.html#hashlib.pbkdf2_hmac "hashlib.pbkdf2_hmac") is deprecated. In
the future PBKDF2-HMAC will only be available when Python has been built with
OpenSSL support.
(Contributed by Christian Heimes in [bpo-43880](https://bugs.python.org/issue?@action=redirect&bpo=43880).)

### hmac

The hmac module now uses OpenSSL’s HMAC implementation internally.
(Contributed by Christian Heimes in [bpo-40645](https://bugs.python.org/issue?@action=redirect&bpo=40645).)

### IDLE and idlelib

Make IDLE invoke [`sys.excepthook()`](../library/sys.html#sys.excepthook "sys.excepthook") (when started without ‘-n’).
User hooks were previously ignored. (Contributed by Ken Hilton in
[bpo-43008](https://bugs.python.org/issue?@action=redirect&bpo=43008).)

Rearrange the settings dialog. Split the General tab into Windows
and Shell/Ed tabs. Move help sources, which extend the Help menu, to the
Extensions tab. Make space for new options and shorten the dialog. The
latter makes the dialog better fit small screens. (Contributed by Terry Jan
Reedy in [bpo-40468](https://bugs.python.org/issue?@action=redirect&bpo=40468).) Move the indent space setting from the Font tab to
the new Windows tab. (Contributed by Mark Roseman and Terry Jan Reedy in
[bpo-33962](https://bugs.python.org/issue?@action=redirect&bpo=33962).)

The changes above were backported to a 3.9 maintenance release.

Add a Shell sidebar. Move the primary prompt (‘>>>’) to the sidebar.
Add secondary prompts (’…’) to the sidebar. Left click and optional
drag selects one or more lines of text, as with the editor
line number sidebar. Right click after selecting text lines displays
a context menu with ‘copy with prompts’. This zips together prompts
from the sidebar with lines from the selected text. This option also
appears on the context menu for the text. (Contributed by Tal Einat
in [bpo-37903](https://bugs.python.org/issue?@action=redirect&bpo=37903).)

Use spaces instead of tabs to indent interactive code. This makes
interactive code entries ‘look right’. Making this feasible was a
major motivation for adding the shell sidebar. (Contributed by
Terry Jan Reedy in [bpo-37892](https://bugs.python.org/issue?@action=redirect&bpo=37892).)

Highlight the new [soft keywords](../reference/lexical_analysis.html#soft-keywords) [`match`](../reference/compound_stmts.html#match),
[`case`](../reference/compound_stmts.html#match), and [`_`](../reference/compound_stmts.html#wildcard-patterns) in
pattern-matching statements. However, this highlighting is not perfect
and will be incorrect in some rare cases, including some `_`-s in
`case` patterns. (Contributed by Tal Einat in [bpo-44010](https://bugs.python.org/issue?@action=redirect&bpo=44010).)

New in 3.10 maintenance releases.

Apply syntax highlighting to `.pyi` files. (Contributed by Alex
Waygood and Terry Jan Reedy in [bpo-45447](https://bugs.python.org/issue?@action=redirect&bpo=45447).)

Include prompts when saving Shell with inputs and outputs.
(Contributed by Terry Jan Reedy in [gh-95191](https://github.com/python/cpython/issues/95191).)

### linecache

When a module does not define `__loader__`, fall back to `__spec__.loader`.
(Contributed by Brett Cannon in [bpo-42133](https://bugs.python.org/issue?@action=redirect&bpo=42133).)

### os

Add [`os.cpu_count()`](../library/os.html#os.cpu_count "os.cpu_count") support for VxWorks RTOS.
(Contributed by Peixing Xin in [bpo-41440](https://bugs.python.org/issue?@action=redirect&bpo=41440).)

Add a new function [`os.eventfd()`](../library/os.html#os.eventfd "os.eventfd") and related helpers to wrap the
`eventfd2` syscall on Linux.
(Contributed by Christian Heimes in [bpo-41001](https://bugs.python.org/issue?@action=redirect&bpo=41001).)

Add [`os.splice()`](../library/os.html#os.splice "os.splice") that allows to move data between two file
descriptors without copying between kernel address space and user
address space, where one of the file descriptors must refer to a
pipe. (Contributed by Pablo Galindo in [bpo-41625](https://bugs.python.org/issue?@action=redirect&bpo=41625).)

Add [`O_EVTONLY`](../library/os.html#os.O_EVTONLY "os.O_EVTONLY"), [`O_FSYNC`](../library/os.html#os.O_FSYNC "os.O_FSYNC"), [`O_SYMLINK`](../library/os.html#os.O_SYMLINK "os.O_SYMLINK")
and [`O_NOFOLLOW_ANY`](../library/os.html#os.O_NOFOLLOW_ANY "os.O_NOFOLLOW_ANY") for macOS.
(Contributed by Donghee Na in [bpo-43106](https://bugs.python.org/issue?@action=redirect&bpo=43106).)

### os.path

[`os.path.realpath()`](../library/os.path.html#os.path.realpath "os.path.realpath") now accepts a *strict* keyword-only argument. When set
to `True`, [`OSError`](../library/exceptions.html#OSError "OSError") is raised if a path doesn’t exist or a symlink loop
is encountered.
(Contributed by Barney Gale in [bpo-43757](https://bugs.python.org/issue?@action=redirect&bpo=43757).)

### py\_compile

Add `--quiet` option to command-line interface of [`py_compile`](../library/py_compile.html#module-py_compile "py_compile: Generate byte-code files from Python source files.").
(Contributed by Gregory Schevchenko in [bpo-38731](https://bugs.python.org/issue?@action=redirect&bpo=38731).)

### site

When a module does not define `__loader__`, fall back to `__spec__.loader`.
(Contributed by Brett Cannon in [bpo-42133](https://bugs.python.org/issue?@action=redirect&bpo=42133).)

### socket

The exception [`socket.timeout`](../library/socket.html#socket.timeout "socket.timeout") is now an alias of [`TimeoutError`](../library/exceptions.html#TimeoutError "TimeoutError").
(Contributed by Christian Heimes in [bpo-42413](https://bugs.python.org/issue?@action=redirect&bpo=42413).)

Add option to create MPTCP sockets with `IPPROTO_MPTCP`
(Contributed by Rui Cunha in [bpo-43571](https://bugs.python.org/issue?@action=redirect&bpo=43571).)

Add `IP_RECVTOS` option to receive the type of service (ToS) or DSCP/ECN fields
(Contributed by Georg Sauthoff in [bpo-44077](https://bugs.python.org/issue?@action=redirect&bpo=44077).)

### ssl

The ssl module requires OpenSSL 1.1.1 or newer.
(Contributed by Christian Heimes in [**PEP 644**](https://peps.python.org/pep-0644/) and [bpo-43669](https://bugs.python.org/issue?@action=redirect&bpo=43669).)

The ssl module has preliminary support for OpenSSL 3.0.0 and new option
[`OP_IGNORE_UNEXPECTED_EOF`](../library/ssl.html#ssl.OP_IGNORE_UNEXPECTED_EOF "ssl.OP_IGNORE_UNEXPECTED_EOF").
(Contributed by Christian Heimes in [bpo-38820](https://bugs.python.org/issue?@action=redirect&bpo=38820), [bpo-43794](https://bugs.python.org/issue?@action=redirect&bpo=43794),
[bpo-43788](https://bugs.python.org/issue?@action=redirect&bpo=43788), [bpo-43791](https://bugs.python.org/issue?@action=redirect&bpo=43791), [bpo-43799](https://bugs.python.org/issue?@action=redirect&bpo=43799), [bpo-43920](https://bugs.python.org/issue?@action=redirect&bpo=43920),
[bpo-43789](https://bugs.python.org/issue?@action=redirect&bpo=43789), and [bpo-43811](https://bugs.python.org/issue?@action=redirect&bpo=43811).)

Deprecated function and use of deprecated constants now result in
a [`DeprecationWarning`](../library/exceptions.html#DeprecationWarning "DeprecationWarning"). [`ssl.SSLContext.options`](../library/ssl.html#ssl.SSLContext.options "ssl.SSLContext.options") has
[`OP_NO_SSLv2`](../library/ssl.html#ssl.OP_NO_SSLv2 "ssl.OP_NO_SSLv2") and [`OP_NO_SSLv3`](../library/ssl.html#ssl.OP_NO_SSLv3 "ssl.OP_NO_SSLv3") set by default and
therefore cannot warn about setting the flag again. The
[deprecation section](#whatsnew310-deprecated) has a list of deprecated
features.
(Contributed by Christian Heimes in [bpo-43880](https://bugs.python.org/issue?@action=redirect&bpo=43880).)

The ssl module now has more secure default settings. Ciphers without forward
secrecy or SHA-1 MAC are disabled by default. Security level 2 prohibits
weak RSA, DH, and ECC keys with less than 112 bits of security.
[`SSLContext`](../library/ssl.html#ssl.SSLContext "ssl.SSLContext") defaults to minimum protocol version TLS 1.2.
Settings are based on Hynek Schlawack’s research.
(Contributed by Christian Heimes in [bpo-43998](https://bugs.python.org/issue?@action=redirect&bpo=43998).)

The deprecated protocols SSL 3.0, TLS 1.0, and TLS 1.1 are no longer
officially supported. Python does not block them actively. However
OpenSSL build options, distro configurations, vendor patches, and cipher
suites may prevent a successful handshake.

Add a *timeout* parameter to the [`ssl.get_server_certificate()`](../library/ssl.html#ssl.get_server_certificate "ssl.get_server_certificate") function.
(Contributed by Zackery Spytz in [bpo-31870](https://bugs.python.org/issue?@action=redirect&bpo=31870).)

The ssl module uses heap-types and multi-phase initialization.
(Contributed by Christian Heimes in [bpo-42333](https://bugs.python.org/issue?@action=redirect&bpo=42333).)

A new verify flag [`VERIFY_X509_PARTIAL_CHAIN`](../library/ssl.html#ssl.VERIFY_X509_PARTIAL_CHAIN "ssl.VERIFY_X509_PARTIAL_CHAIN") has been added.
(Contributed by l0x in [bpo-40849](https://bugs.python.org/issue?@action=redirect&bpo=40849).)

### sys

Add [`sys.orig_argv`](../library/sys.html#sys.orig_argv "sys.orig_argv") attribute: the list of the original command line
arguments passed to the Python executable.
(Contributed by Victor Stinner in [bpo-23427](https://bugs.python.org/issue?@action=redirect&bpo=23427).)

Add [`sys.stdlib_module_names`](../library/sys.html#sys.stdlib_module_names "sys.stdlib_module_names"), containing the list of the standard library
module names.
(Contributed by Victor Stinner in [bpo-42955](https://bugs.python.org/issue?@action=redirect&bpo=42955).)

### typing

For major changes, see [New Features Related to Type Hints](#new-feat-related-type-hints).

The behavior of [`typing.Literal`](../library/typing.html#typing.Literal "typing.Literal") was changed to conform with [**PEP 586**](https://peps.python.org/pep-0586/)
and to match the behavior of static type checkers specified in the PEP.

1. `Literal` now de-duplicates parameters.
2. Equality comparisons between `Literal` objects are now order independent.
3. `Literal` comparisons now respect types. For example,
   `Literal[0] == Literal[False]` previously evaluated to `True`. It is
   now `False`. To support this change, the internally used type cache now
   supports differentiating types.
4. `Literal` objects will now raise a [`TypeError`](../library/exceptions.html#TypeError "TypeError") exception during
   equality comparisons if any of their parameters are not [hashable](../glossary.html#term-hashable).
   Note that declaring `Literal` with unhashable parameters will not throw
   an error:

   Copy

   ```
   >>> from typing import Literal
   >>> Literal[{0}]
   >>> Literal[{0}] == Literal[{False}]
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: unhashable type: 'set'

   ```

(Contributed by Yurii Karabas in [bpo-42345](https://bugs.python.org/issue?@action=redirect&bpo=42345).)

Add new function [`typing.is_typeddict()`](../library/typing.html#typing.is_typeddict "typing.is_typeddict") to introspect if an annotation
is a [`typing.TypedDict`](../library/typing.html#typing.TypedDict "typing.TypedDict").
(Contributed by Patrick Reader in [bpo-41792](https://bugs.python.org/issue?@action=redirect&bpo=41792).)

Subclasses of `typing.Protocol` which only have data variables declared
will now raise a `TypeError` when checked with `isinstance` unless they
are decorated with [`runtime_checkable()`](../library/typing.html#typing.runtime_checkable "typing.runtime_checkable"). Previously, these checks
passed silently. Users should decorate their
subclasses with the `runtime_checkable()` decorator
if they want runtime protocols.
(Contributed by Yurii Karabas in [bpo-38908](https://bugs.python.org/issue?@action=redirect&bpo=38908).)

Importing from the `typing.io` and `typing.re` submodules will now emit
[`DeprecationWarning`](../library/exceptions.html#DeprecationWarning "DeprecationWarning"). These submodules have been deprecated since
Python 3.8 and will be removed in a future version of Python. Anything
belonging to those submodules should be imported directly from
[`typing`](../library/typing.html#module-typing "typing: Support for type hints (see :pep:`484`).") instead.
(Contributed by Sebastian Rittau in [bpo-38291](https://bugs.python.org/issue?@action=redirect&bpo=38291).)

### urllib.parse

Python versions earlier than Python 3.10 allowed using both `;` and `&` as
query parameter separators in [`urllib.parse.parse_qs()`](../library/urllib.parse.html#urllib.parse.parse_qs "urllib.parse.parse_qs") and
[`urllib.parse.parse_qsl()`](../library/urllib.parse.html#urllib.parse.parse_qsl "urllib.parse.parse_qsl"). Due to security concerns, and to conform with
newer W3C recommendations, this has been changed to allow only a single
separator key, with `&` as the default. This change also affects
`cgi.parse()` and `cgi.parse_multipart()` as they use the affected
functions internally. For more details, please see their respective
documentation.
(Contributed by Adam Goldschmidt, Senthil Kumaran and Ken Jin in [bpo-42967](https://bugs.python.org/issue?@action=redirect&bpo=42967).)

The presence of newline or tab characters in parts of a URL allows for some
forms of attacks. Following the WHATWG specification that updates [**RFC 3986**](https://datatracker.ietf.org/doc/html/rfc3986.html),
ASCII newline `\n`, `\r` and tab `\t` characters are stripped from the
URL by the parser in [`urllib.parse`](../library/urllib.parse.html#module-urllib.parse "urllib.parse: Parse URLs into or assemble them from components.") preventing such attacks. The removal
characters are controlled by a new module level variable
`urllib.parse._UNSAFE_URL_BYTES_TO_REMOVE`. (See [gh-88048](https://github.com/python/cpython/issues/88048))