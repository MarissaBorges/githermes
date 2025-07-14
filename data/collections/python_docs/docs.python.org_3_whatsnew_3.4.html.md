This article explains the new features in Python 3.4, compared to 3.3.
Python 3.4 was released on March 16, 2014. For full details, see the
[changelog](https://docs.python.org/3.4/whatsnew/changelog.html).

Improved Modules
----------------

### abc

New function [`abc.get_cache_token()`](../library/abc.html#abc.get_cache_token "abc.get_cache_token") can be used to know when to invalidate
caches that are affected by changes in the object graph. (Contributed
by Łukasz Langa in [bpo-16832](https://bugs.python.org/issue?@action=redirect&bpo=16832).)

New class [`ABC`](../library/abc.html#abc.ABC "abc.ABC") has [`ABCMeta`](../library/abc.html#abc.ABCMeta "abc.ABCMeta") as its meta class.
Using `ABC` as a base class has essentially the same effect as specifying
`metaclass=abc.ABCMeta`, but is simpler to type and easier to read.
(Contributed by Bruno Dupuis in [bpo-16049](https://bugs.python.org/issue?@action=redirect&bpo=16049).)

### aifc

The `getparams()` method now returns a namedtuple rather than a
plain tuple. (Contributed by Claudiu Popa in [bpo-17818](https://bugs.python.org/issue?@action=redirect&bpo=17818).)

`aifc.open()` now supports the context management protocol: when used in a
[`with`](../reference/compound_stmts.html#with) block, the `close()` method of the returned
object will be called automatically at the end of the block. (Contributed by
Serhiy Storchacha in [bpo-16486](https://bugs.python.org/issue?@action=redirect&bpo=16486).)

The `writeframesraw()` and `writeframes()`
methods now accept any [bytes-like object](../glossary.html#term-bytes-like-object). (Contributed by Serhiy
Storchaka in [bpo-8311](https://bugs.python.org/issue?@action=redirect&bpo=8311).)

### argparse

The [`FileType`](../library/argparse.html#argparse.FileType "argparse.FileType") class now accepts *encoding* and
*errors* arguments, which are passed through to [`open()`](../library/functions.html#open "open"). (Contributed
by Lucas Maystre in [bpo-11175](https://bugs.python.org/issue?@action=redirect&bpo=11175).)

### audioop

`audioop` now supports 24-bit samples. (Contributed by Serhiy Storchaka
in [bpo-12866](https://bugs.python.org/issue?@action=redirect&bpo=12866).)

New `byteswap()` function converts big-endian samples to
little-endian and vice versa. (Contributed by Serhiy Storchaka in
[bpo-19641](https://bugs.python.org/issue?@action=redirect&bpo=19641).)

All `audioop` functions now accept any [bytes-like object](../glossary.html#term-bytes-like-object). Strings
are not accepted: they didn’t work before, now they raise an error right away.
(Contributed by Serhiy Storchaka in [bpo-16685](https://bugs.python.org/issue?@action=redirect&bpo=16685).)

### base64

The encoding and decoding functions in [`base64`](../library/base64.html#module-base64 "base64: RFC 4648: Base16, Base32, Base64 Data Encodings; Base85 and Ascii85") now accept any
[bytes-like object](../glossary.html#term-bytes-like-object) in cases where it previously required a
[`bytes`](../library/stdtypes.html#bytes "bytes") or [`bytearray`](../library/stdtypes.html#bytearray "bytearray") instance. (Contributed by Nick Coghlan in
[bpo-17839](https://bugs.python.org/issue?@action=redirect&bpo=17839).)

New functions [`a85encode()`](../library/base64.html#base64.a85encode "base64.a85encode"), [`a85decode()`](../library/base64.html#base64.a85decode "base64.a85decode"),
[`b85encode()`](../library/base64.html#base64.b85encode "base64.b85encode"), and [`b85decode()`](../library/base64.html#base64.b85decode "base64.b85decode") provide the ability to
encode and decode binary data from and to `Ascii85` and the git/mercurial
`Base85` formats, respectively. The `a85` functions have options that can
be used to make them compatible with the variants of the `Ascii85` encoding,
including the Adobe variant. (Contributed by Martin Morrison, the Mercurial
project, Serhiy Storchaka, and Antoine Pitrou in [bpo-17618](https://bugs.python.org/issue?@action=redirect&bpo=17618).)

### collections

The [`ChainMap.new_child()`](../library/collections.html#collections.ChainMap.new_child "collections.ChainMap.new_child") method now accepts an *m* argument specifying
the child map to add to the chain. This allows an existing mapping and/or a
custom mapping type to be used for the child. (Contributed by Vinay Sajip in
[bpo-16613](https://bugs.python.org/issue?@action=redirect&bpo=16613).)

### colorsys

The number of digits in the coefficients for the RGB — YIQ conversions have
been expanded so that they match the FCC NTSC versions. The change in
results should be less than 1% and may better match results found elsewhere.
(Contributed by Brian Landers and Serhiy Storchaka in [bpo-14323](https://bugs.python.org/issue?@action=redirect&bpo=14323).)

### contextlib

The new [`contextlib.suppress`](../library/contextlib.html#contextlib.suppress "contextlib.suppress") context manager helps to clarify the
intent of code that deliberately suppresses exceptions from a single
statement. (Contributed by Raymond Hettinger in [bpo-15806](https://bugs.python.org/issue?@action=redirect&bpo=15806) and
Zero Piraeus in [bpo-19266](https://bugs.python.org/issue?@action=redirect&bpo=19266).)

The new [`contextlib.redirect_stdout()`](../library/contextlib.html#contextlib.redirect_stdout "contextlib.redirect_stdout") context manager makes it easier
for utility scripts to handle inflexible APIs that write their output to
[`sys.stdout`](../library/sys.html#sys.stdout "sys.stdout") and don’t provide any options to redirect it. Using the
context manager, the [`sys.stdout`](../library/sys.html#sys.stdout "sys.stdout") output can be redirected to any
other stream or, in conjunction with [`io.StringIO`](../library/io.html#io.StringIO "io.StringIO"), to a string.
The latter can be especially useful, for example, to capture output
from a function that was written to implement a command line interface.
It is recommended only for utility scripts because it affects the
global state of [`sys.stdout`](../library/sys.html#sys.stdout "sys.stdout"). (Contributed by Raymond Hettinger
in [bpo-15805](https://bugs.python.org/issue?@action=redirect&bpo=15805).)

The [`contextlib`](../library/contextlib.html#module-contextlib "contextlib: Utilities for with-statement contexts.") documentation has also been updated to include a
[discussion](../library/contextlib.html#single-use-reusable-and-reentrant-cms) of the
differences between single use, reusable and reentrant context managers.

### dbm

[`dbm.open()`](../library/dbm.html#dbm.open "dbm.open") objects now support the context management protocol. When
used in a [`with`](../reference/compound_stmts.html#with) statement, the `close` method of the database
object will be called automatically at the end of the block. (Contributed by
Claudiu Popa and Nick Coghlan in [bpo-19282](https://bugs.python.org/issue?@action=redirect&bpo=19282).)

### dis

Functions [`show_code()`](../library/dis.html#dis.show_code "dis.show_code"), [`dis()`](../library/dis.html#dis.dis "dis.dis"), `distb()`, and
[`disassemble()`](../library/dis.html#dis.disassemble "dis.disassemble") now accept a keyword-only *file* argument that
controls where they write their output.

The [`dis`](../library/dis.html#module-dis "dis: Disassembler for Python bytecode.") module is now built around an [`Instruction`](../library/dis.html#dis.Instruction "dis.Instruction") class
that provides object oriented access to the details of each individual bytecode
operation.

A new method, [`get_instructions()`](../library/dis.html#dis.get_instructions "dis.get_instructions"), provides an iterator that emits
the Instruction stream for a given piece of Python code. Thus it is now
possible to write a program that inspects and manipulates a bytecode
object in ways different from those provided by the [`dis`](../library/dis.html#module-dis "dis: Disassembler for Python bytecode.") module
itself. For example:

Copy

```
>>> import dis
>>> for instr in dis.get_instructions(lambda x: x + 1):
...     print(instr.opname)
LOAD_FAST
LOAD_CONST
BINARY_ADD
RETURN_VALUE

```

The various display tools in the [`dis`](../library/dis.html#module-dis "dis: Disassembler for Python bytecode.") module have been rewritten to use
these new components.

In addition, a new application-friendly class [`Bytecode`](../library/dis.html#dis.Bytecode "dis.Bytecode") provides
an object-oriented API for inspecting bytecode in both in human-readable form
and for iterating over instructions. The [`Bytecode`](../library/dis.html#dis.Bytecode "dis.Bytecode") constructor
takes the same arguments that `get_instruction()` does (plus an
optional *current\_offset*), and the resulting object can be iterated to produce
[`Instruction`](../library/dis.html#dis.Instruction "dis.Instruction") objects. But it also has a [`dis`](../library/dis.html#dis.Bytecode.dis "dis.Bytecode.dis")
method, equivalent to calling [`dis`](../library/dis.html#dis.dis "dis.dis") on the constructor argument, but
returned as a multi-line string:

Copy

```
>>> bytecode = dis.Bytecode(lambda x: x + 1, current_offset=3)
>>> for instr in bytecode:
...     print('{} ({})'.format(instr.opname, instr.opcode))
LOAD_FAST (124)
LOAD_CONST (100)
BINARY_ADD (23)
RETURN_VALUE (83)
>>> bytecode.dis().splitlines()
['  1           0 LOAD_FAST                0 (x)',
 '      -->     3 LOAD_CONST               1 (1)',
 '              6 BINARY_ADD',
 '              7 RETURN_VALUE']

```

[`Bytecode`](../library/dis.html#dis.Bytecode "dis.Bytecode") also has a class method,
[`from_traceback()`](../library/dis.html#dis.Bytecode.from_traceback "dis.Bytecode.from_traceback"), that provides the ability to manipulate a
traceback (that is, `print(Bytecode.from_traceback(tb).dis())` is equivalent
to `distb(tb)`).

(Contributed by Nick Coghlan, Ryan Kelly and Thomas Kluyver in [bpo-11816](https://bugs.python.org/issue?@action=redirect&bpo=11816)
and Claudiu Popa in [bpo-17916](https://bugs.python.org/issue?@action=redirect&bpo=17916).)

New function [`stack_effect()`](../library/dis.html#dis.stack_effect "dis.stack_effect") computes the effect on the Python stack
of a given opcode and argument, information that is not otherwise available.
(Contributed by Larry Hastings in [bpo-19722](https://bugs.python.org/issue?@action=redirect&bpo=19722).)

### doctest

A new [option flag](../library/doctest.html#doctest-options), [`FAIL_FAST`](../library/doctest.html#doctest.FAIL_FAST "doctest.FAIL_FAST"), halts
test running as soon as the first failure is detected. (Contributed by R.
David Murray and Daniel Urban in [bpo-16522](https://bugs.python.org/issue?@action=redirect&bpo=16522).)

The [`doctest`](../library/doctest.html#module-doctest "doctest: Test pieces of code within docstrings.") command line interface now uses [`argparse`](../library/argparse.html#module-argparse "argparse: Command-line option and argument parsing library."), and has two
new options, `-o` and `-f`. `-o` allows [doctest options](../library/doctest.html#doctest-options) to be specified on the command line, and `-f` is a
shorthand for `-o FAIL_FAST` (to parallel the similar option supported by the
[`unittest`](../library/unittest.html#module-unittest "unittest: Unit testing framework for Python.") CLI). (Contributed by R. David Murray in [bpo-11390](https://bugs.python.org/issue?@action=redirect&bpo=11390).)

[`doctest`](../library/doctest.html#module-doctest "doctest: Test pieces of code within docstrings.") will now find doctests in extension module `__doc__` strings.
(Contributed by Zachary Ware in [bpo-3158](https://bugs.python.org/issue?@action=redirect&bpo=3158).)

### email

[`as_string()`](../library/email.compat32-message.html#email.message.Message.as_string "email.message.Message.as_string") now accepts a *policy* argument to
override the default policy of the message when generating a string
representation of it. This means that `as_string` can now be used in more
circumstances, instead of having to create and use a [`generator`](../library/email.generator.html#module-email.generator "email.generator: Generate flat text email messages from a message structure.") in
order to pass formatting parameters to its `flatten` method. (Contributed by
R. David Murray in [bpo-18600](https://bugs.python.org/issue?@action=redirect&bpo=18600).)

New method [`as_bytes()`](../library/email.compat32-message.html#email.message.Message.as_bytes "email.message.Message.as_bytes") added to produce a bytes
representation of the message in a fashion similar to how `as_string`
produces a string representation. It does not accept the *maxheaderlen*
argument, but does accept the *unixfrom* and *policy* arguments. The
[`Message`](../library/email.compat32-message.html#email.message.Message "email.message.Message") [`__bytes__()`](../library/email.compat32-message.html#email.message.Message.__bytes__ "email.message.Message.__bytes__") method
calls it, meaning that `bytes(mymsg)` will now produce the intuitive
result: a bytes object containing the fully formatted message. (Contributed
by R. David Murray in [bpo-18600](https://bugs.python.org/issue?@action=redirect&bpo=18600).)

The [`Message.set_param()`](../library/email.compat32-message.html#email.message.Message.set_param "email.message.Message.set_param") message now accepts a *replace* keyword argument.
When specified, the associated header will be updated without changing
its location in the list of headers. For backward compatibility, the default
is `False`. (Contributed by R. David Murray in [bpo-18891](https://bugs.python.org/issue?@action=redirect&bpo=18891).)

A pair of new subclasses of [`Message`](../library/email.compat32-message.html#email.message.Message "email.message.Message") have been added
([`EmailMessage`](../library/email.message.html#email.message.EmailMessage "email.message.EmailMessage") and [`MIMEPart`](../library/email.message.html#email.message.MIMEPart "email.message.MIMEPart")), along with a new sub-module,
[`contentmanager`](../library/email.contentmanager.html#module-email.contentmanager "email.contentmanager: Storing and Retrieving Content from MIME Parts") and a new [`policy`](../library/email.policy.html#module-email.policy "email.policy: Controlling the parsing and generating of messages") attribute
[`content_manager`](../library/email.policy.html#email.policy.EmailPolicy.content_manager "email.policy.EmailPolicy.content_manager"). All documentation is
currently in the new module, which is being added as part of email’s new
[provisional API](../glossary.html#term-provisional-API). These classes provide a number of new methods that
make extracting content from and inserting content into email messages much
easier. For details, see the [`contentmanager`](../library/email.contentmanager.html#module-email.contentmanager "email.contentmanager: Storing and Retrieving Content from MIME Parts") documentation and
the [email: Examples](../library/email.examples.html#email-examples). These API additions complete the
bulk of the work that was planned as part of the email6 project. The currently
provisional API is scheduled to become final in Python 3.5 (possibly with a few
minor additions in the area of error handling). (Contributed by R. David
Murray in [bpo-18891](https://bugs.python.org/issue?@action=redirect&bpo=18891).)

### filecmp

A new [`clear_cache()`](../library/filecmp.html#filecmp.clear_cache "filecmp.clear_cache") function provides the ability to clear the
[`filecmp`](../library/filecmp.html#module-filecmp "filecmp: Compare files efficiently.") comparison cache, which uses [`os.stat()`](../library/os.html#os.stat "os.stat") information to
determine if the file has changed since the last compare. This can be used,
for example, if the file might have been changed and re-checked in less time
than the resolution of a particular filesystem’s file modification time field.
(Contributed by Mark Levitt in [bpo-18149](https://bugs.python.org/issue?@action=redirect&bpo=18149).)

New module attribute [`DEFAULT_IGNORES`](../library/filecmp.html#filecmp.DEFAULT_IGNORES "filecmp.DEFAULT_IGNORES") provides the list of
directories that are used as the default value for the *ignore* parameter of
the [`dircmp()`](../library/filecmp.html#filecmp.dircmp "filecmp.dircmp") function. (Contributed by Eli Bendersky in
[bpo-15442](https://bugs.python.org/issue?@action=redirect&bpo=15442).)

### gc

New function [`get_stats()`](../library/gc.html#gc.get_stats "gc.get_stats") returns a list of three per-generation
dictionaries containing the collections statistics since interpreter startup.
(Contributed by Antoine Pitrou in [bpo-16351](https://bugs.python.org/issue?@action=redirect&bpo=16351).)

### glob

A new function [`escape()`](../library/glob.html#glob.escape "glob.escape") provides a way to escape special characters
in a filename so that they do not become part of the globbing expansion but are
instead matched literally. (Contributed by Serhiy Storchaka in [bpo-8402](https://bugs.python.org/issue?@action=redirect&bpo=8402).)

### hmac

[`hmac`](../library/hmac.html#module-hmac "hmac: Keyed-Hashing for Message Authentication (HMAC) implementation") now accepts `bytearray` as well as `bytes` for the *key*
argument to the [`new()`](../library/hmac.html#hmac.new "hmac.new") function, and the *msg* parameter to both the
[`new()`](../library/hmac.html#hmac.new "hmac.new") function and the [`update()`](../library/hmac.html#hmac.HMAC.update "hmac.HMAC.update") method now
accepts any type supported by the [`hashlib`](../library/hashlib.html#module-hashlib "hashlib: Secure hash and message digest algorithms.") module. (Contributed
by Jonas Borgström in [bpo-18240](https://bugs.python.org/issue?@action=redirect&bpo=18240).)

The *digestmod* argument to the [`hmac.new()`](../library/hmac.html#hmac.new "hmac.new") function may now be any hash
digest name recognized by [`hashlib`](../library/hashlib.html#module-hashlib "hashlib: Secure hash and message digest algorithms."). In addition, the current behavior in
which the value of *digestmod* defaults to `MD5` is deprecated: in a
future version of Python there will be no default value. (Contributed by
Christian Heimes in [bpo-17276](https://bugs.python.org/issue?@action=redirect&bpo=17276).)

With the addition of [`block_size`](../library/hmac.html#hmac.HMAC.block_size "hmac.HMAC.block_size") and [`name`](../library/hmac.html#hmac.HMAC.name "hmac.HMAC.name")
attributes (and the formal documentation of the [`digest_size`](../library/hmac.html#hmac.HMAC.digest_size "hmac.HMAC.digest_size")
attribute), the [`hmac`](../library/hmac.html#module-hmac "hmac: Keyed-Hashing for Message Authentication (HMAC) implementation") module now conforms fully to the [**PEP 247**](https://peps.python.org/pep-0247/) API.
(Contributed by Christian Heimes in [bpo-18775](https://bugs.python.org/issue?@action=redirect&bpo=18775).)

### html

New function [`unescape()`](../library/html.html#html.unescape "html.unescape") function converts HTML5 character references to
the corresponding Unicode characters. (Contributed by Ezio Melotti in
[bpo-2927](https://bugs.python.org/issue?@action=redirect&bpo=2927).)

[`HTMLParser`](../library/html.parser.html#html.parser.HTMLParser "html.parser.HTMLParser") accepts a new keyword argument
*convert\_charrefs* that, when `True`, automatically converts all character
references. For backward-compatibility, its value defaults to `False`, but
it will change to `True` in a future version of Python, so you are invited to
set it explicitly and update your code to use this new feature. (Contributed
by Ezio Melotti in [bpo-13633](https://bugs.python.org/issue?@action=redirect&bpo=13633).)

The *strict* argument of [`HTMLParser`](../library/html.parser.html#html.parser.HTMLParser "html.parser.HTMLParser") is now deprecated.
(Contributed by Ezio Melotti in [bpo-15114](https://bugs.python.org/issue?@action=redirect&bpo=15114).)

### http

[`send_error()`](../library/http.server.html#http.server.BaseHTTPRequestHandler.send_error "http.server.BaseHTTPRequestHandler.send_error") now accepts an
optional additional *explain* parameter which can be used to provide an
extended error description, overriding the hardcoded default if there is one.
This extended error description will be formatted using the
`error_message_format` attribute and sent as the body
of the error response. (Contributed by Karl Cow in [bpo-12921](https://bugs.python.org/issue?@action=redirect&bpo=12921).)

The [`http.server`](../library/http.server.html#module-http.server "http.server: HTTP server and request handlers.") [command line interface](../library/http.server.html#http-server-cli) now has
a `-b/--bind` option that causes the server to listen on a specific address.
(Contributed by Malte Swart in [bpo-17764](https://bugs.python.org/issue?@action=redirect&bpo=17764).)

### idlelib and IDLE

Since idlelib implements the IDLE shell and editor and is not intended for
import by other programs, it gets improvements with every release. See
`Lib/idlelib/NEWS.txt` for a cumulative list of changes since 3.3.0,
as well as changes made in future 3.4.x releases. This file is also available
from the IDLE dialog.

### inspect

The [`inspect`](../library/inspect.html#module-inspect "inspect: Extract information and source code from live objects.") module now offers a basic [command line interface](../library/inspect.html#inspect-module-cli) to quickly display source code and other
information for modules, classes and functions. (Contributed by Claudiu Popa
and Nick Coghlan in [bpo-18626](https://bugs.python.org/issue?@action=redirect&bpo=18626).)

[`unwrap()`](../library/inspect.html#inspect.unwrap "inspect.unwrap") makes it easy to unravel wrapper function chains
created by [`functools.wraps()`](../library/functools.html#functools.wraps "functools.wraps") (and any other API that sets the
`__wrapped__` attribute on a wrapper function). (Contributed by
Daniel Urban, Aaron Iles and Nick Coghlan in [bpo-13266](https://bugs.python.org/issue?@action=redirect&bpo=13266).)

As part of the implementation of the new [`enum`](../library/enum.html#module-enum "enum: Implementation of an enumeration class.") module, the
[`inspect`](../library/inspect.html#module-inspect "inspect: Extract information and source code from live objects.") module now has substantially better support for custom
`__dir__` methods and dynamic class attributes provided through
metaclasses. (Contributed by Ethan Furman in [bpo-18929](https://bugs.python.org/issue?@action=redirect&bpo=18929) and
[bpo-19030](https://bugs.python.org/issue?@action=redirect&bpo=19030).)

[`getfullargspec()`](../library/inspect.html#inspect.getfullargspec "inspect.getfullargspec") and `getargspec()`
now use the [`signature()`](../library/inspect.html#inspect.signature "inspect.signature") API. This allows them to
support a much broader range of callables, including those with
`__signature__` attributes, those with metadata provided by argument
clinic, [`functools.partial()`](../library/functools.html#functools.partial "functools.partial") objects and more. Note that, unlike
[`signature()`](../library/inspect.html#inspect.signature "inspect.signature"), these functions still ignore `__wrapped__`
attributes, and report the already bound first argument for bound methods,
so it is still necessary to update your code to use
[`signature()`](../library/inspect.html#inspect.signature "inspect.signature") directly if those features are desired.
(Contributed by Yury Selivanov in [bpo-17481](https://bugs.python.org/issue?@action=redirect&bpo=17481).)

[`signature()`](../library/inspect.html#inspect.signature "inspect.signature") now supports duck types of CPython functions,
which adds support for functions compiled with Cython. (Contributed
by Stefan Behnel and Yury Selivanov in [bpo-17159](https://bugs.python.org/issue?@action=redirect&bpo=17159).)

### ipaddress

[`ipaddress`](../library/ipaddress.html#module-ipaddress "ipaddress: IPv4/IPv6 manipulation library.") was added to the standard library in Python 3.3 as a
[provisional API](../glossary.html#term-provisional-API). With the release of Python 3.4, this qualification
has been removed: [`ipaddress`](../library/ipaddress.html#module-ipaddress "ipaddress: IPv4/IPv6 manipulation library.") is now considered a stable API, covered
by the normal standard library requirements to maintain backwards
compatibility.

A new [`is_global`](../library/ipaddress.html#ipaddress.IPv4Address.is_global "ipaddress.IPv4Address.is_global") property is `True` if
an address is globally routeable. (Contributed by Peter Moody in
[bpo-17400](https://bugs.python.org/issue?@action=redirect&bpo=17400).)

### logging

The [`TimedRotatingFileHandler`](../library/logging.handlers.html#logging.handlers.TimedRotatingFileHandler "logging.handlers.TimedRotatingFileHandler") has a new *atTime*
parameter that can be used to specify the time of day when rollover should
happen. (Contributed by Ronald Oussoren in [bpo-9556](https://bugs.python.org/issue?@action=redirect&bpo=9556).)

[`SocketHandler`](../library/logging.handlers.html#logging.handlers.SocketHandler "logging.handlers.SocketHandler") and
[`DatagramHandler`](../library/logging.handlers.html#logging.handlers.DatagramHandler "logging.handlers.DatagramHandler") now support Unix domain sockets (by
setting *port* to `None`). (Contributed by Vinay Sajip in commit
ce46195b56a9.)

[`fileConfig()`](../library/logging.config.html#logging.config.fileConfig "logging.config.fileConfig") now accepts a
[`configparser.RawConfigParser`](../library/configparser.html#configparser.RawConfigParser "configparser.RawConfigParser") subclass instance for the *fname*
parameter. This facilitates using a configuration file when logging
configuration is just a part of the overall application configuration, or where
the application modifies the configuration before passing it to
[`fileConfig()`](../library/logging.config.html#logging.config.fileConfig "logging.config.fileConfig"). (Contributed by Vinay Sajip in
[bpo-16110](https://bugs.python.org/issue?@action=redirect&bpo=16110).)

Logging configuration data received from a socket via the
[`logging.config.listen()`](../library/logging.config.html#logging.config.listen "logging.config.listen") function can now be validated before being
processed by supplying a verification function as the argument to the new
*verify* keyword argument. (Contributed by Vinay Sajip in [bpo-15452](https://bugs.python.org/issue?@action=redirect&bpo=15452).)

### marshal

The default [`marshal`](../library/marshal.html#module-marshal "marshal: Convert Python objects to streams of bytes and back (with different constraints).") version has been bumped to 3. The code implementing
the new version restores the Python2 behavior of recording only one copy of
interned strings and preserving the interning on deserialization, and extends
this “one copy” ability to any object type (including handling recursive
references). This reduces both the size of `.pyc` files and the amount of
memory a module occupies in memory when it is loaded from a `.pyc` (or
`.pyo`) file. (Contributed by Kristján Valur Jónsson in [bpo-16475](https://bugs.python.org/issue?@action=redirect&bpo=16475),
with additional speedups by Antoine Pitrou in [bpo-19219](https://bugs.python.org/issue?@action=redirect&bpo=19219).)

### multiprocessing

On Unix two new [start methods](../library/multiprocessing.html#multiprocessing-start-methods),
`spawn` and `forkserver`, have been added for starting processes using
[`multiprocessing`](../library/multiprocessing.html#module-multiprocessing "multiprocessing: Process-based parallelism."). These make the mixing of processes with threads more
robust, and the `spawn` method matches the semantics that multiprocessing has
always used on Windows. New function
[`get_all_start_methods()`](../library/multiprocessing.html#multiprocessing.get_all_start_methods "multiprocessing.get_all_start_methods") reports all start methods
available on the platform, [`get_start_method()`](../library/multiprocessing.html#multiprocessing.get_start_method "multiprocessing.get_start_method") reports
the current start method, and [`set_start_method()`](../library/multiprocessing.html#multiprocessing.set_start_method "multiprocessing.set_start_method") sets
the start method. (Contributed by Richard Oudkerk in [bpo-8713](https://bugs.python.org/issue?@action=redirect&bpo=8713).)

[`multiprocessing`](../library/multiprocessing.html#module-multiprocessing "multiprocessing: Process-based parallelism.") also now has the concept of a `context`, which
determines how child processes are created. New function
[`get_context()`](../library/multiprocessing.html#multiprocessing.get_context "multiprocessing.get_context") returns a context that uses a specified
start method. It has the same API as the [`multiprocessing`](../library/multiprocessing.html#module-multiprocessing "multiprocessing: Process-based parallelism.") module itself,
so you can use it to create [`Pool`](../library/multiprocessing.html#multiprocessing.pool.Pool "multiprocessing.pool.Pool")s and other
objects that will operate within that context. This allows a framework and an
application or different parts of the same application to use multiprocessing
without interfering with each other. (Contributed by Richard Oudkerk in
[bpo-18999](https://bugs.python.org/issue?@action=redirect&bpo=18999).)

Except when using the old *fork* start method, child processes no longer
inherit unneeded handles/file descriptors from their parents (part of
[bpo-8713](https://bugs.python.org/issue?@action=redirect&bpo=8713)).

[`multiprocessing`](../library/multiprocessing.html#module-multiprocessing "multiprocessing: Process-based parallelism.") now relies on [`runpy`](../library/runpy.html#module-runpy "runpy: Locate and run Python modules without importing them first.") (which implements the
`-m` switch) to initialise `__main__` appropriately in child processes
when using the `spawn` or `forkserver` start methods. This resolves some
edge cases where combining multiprocessing, the `-m` command line switch,
and explicit relative imports could cause obscure failures in child
processes. (Contributed by Nick Coghlan in [bpo-19946](https://bugs.python.org/issue?@action=redirect&bpo=19946).)

### operator

New function [`length_hint()`](../library/operator.html#operator.length_hint "operator.length_hint") provides an implementation of the
specification for how the [`__length_hint__()`](../reference/datamodel.html#object.__length_hint__ "object.__length_hint__") special method should
be used, as part of the [**PEP 424**](https://peps.python.org/pep-0424/) formal specification of this language
feature. (Contributed by Armin Ronacher in [bpo-16148](https://bugs.python.org/issue?@action=redirect&bpo=16148).)

There is now a pure-python version of the [`operator`](../library/operator.html#module-operator "operator: Functions corresponding to the standard operators.") module available for
reference and for use by alternate implementations of Python. (Contributed by
Zachary Ware in [bpo-16694](https://bugs.python.org/issue?@action=redirect&bpo=16694).)

### pdb

[`pdb`](../library/pdb.html#module-pdb "pdb: The Python debugger for interactive interpreters.") has been enhanced to handle generators, [`yield`](../reference/simple_stmts.html#yield), and
`yield from` in a more useful fashion. This is especially helpful when
debugging [`asyncio`](../library/asyncio.html#module-asyncio "asyncio: Asynchronous I/O.") based programs. (Contributed by Andrew Svetlov and
Xavier de Gaye in [bpo-16596](https://bugs.python.org/issue?@action=redirect&bpo=16596).)

The `print` command has been removed from [`pdb`](../library/pdb.html#module-pdb "pdb: The Python debugger for interactive interpreters."), restoring access to the
Python [`print()`](../library/functions.html#print "print") function from the pdb command line. Python2’s `pdb` did
not have a `print` command; instead, entering `print` executed the
`print` statement. In Python3 `print` was mistakenly made an alias for the
pdb [`p`](../library/pdb.html#pdbcommand-p) command. `p`, however, prints the `repr` of its argument,
not the `str` like the Python2 `print` command did. Worse, the Python3
`pdb print` command shadowed the Python3 `print` function, making it
inaccessible at the `pdb` prompt. (Contributed by Connor Osborn in
[bpo-18764](https://bugs.python.org/issue?@action=redirect&bpo=18764).)

### pickle

[`pickle`](../library/pickle.html#module-pickle "pickle: Convert Python objects to streams of bytes and back.") now supports (but does not use by default) a new pickle protocol,
protocol 4. This new protocol addresses a number of issues that were present
in previous protocols, such as the serialization of nested classes, very large
strings and containers, and classes whose `__new__()` method takes
keyword-only arguments. It also provides some efficiency improvements.

See also

[**PEP 3154**](https://peps.python.org/pep-3154/) – Pickle protocol 4
:   PEP written by Antoine Pitrou and implemented by Alexandre Vassalotti.

### plistlib

[`plistlib`](../library/plistlib.html#module-plistlib "plistlib: Generate and parse Apple plist files.") now has an API that is similar to the standard pattern for
stdlib serialization protocols, with new [`load()`](../library/plistlib.html#plistlib.load "plistlib.load"),
[`dump()`](../library/plistlib.html#plistlib.dump "plistlib.dump"), [`loads()`](../library/plistlib.html#plistlib.loads "plistlib.loads"), and [`dumps()`](../library/plistlib.html#plistlib.dumps "plistlib.dumps")
functions. (The older API is now deprecated.) In addition to the already
supported XML plist format ([`FMT_XML`](../library/plistlib.html#plistlib.FMT_XML "plistlib.FMT_XML")), it also now supports
the binary plist format ([`FMT_BINARY`](../library/plistlib.html#plistlib.FMT_BINARY "plistlib.FMT_BINARY")). (Contributed by Ronald
Oussoren and others in [bpo-14455](https://bugs.python.org/issue?@action=redirect&bpo=14455).)

### poplib

Two new methods have been added to [`poplib`](../library/poplib.html#module-poplib "poplib: POP3 protocol client (requires sockets)."): [`capa()`](../library/poplib.html#poplib.POP3.capa "poplib.POP3.capa"),
which returns the list of capabilities advertised by the POP server, and
[`stls()`](../library/poplib.html#poplib.POP3.stls "poplib.POP3.stls"), which switches a clear-text POP3 session into an
encrypted POP3 session if the POP server supports it. (Contributed by Lorenzo
Catucci in [bpo-4473](https://bugs.python.org/issue?@action=redirect&bpo=4473).)

### pprint

The [`pprint`](../library/pprint.html#module-pprint "pprint: Data pretty printer.") module’s [`PrettyPrinter`](../library/pprint.html#pprint.PrettyPrinter "pprint.PrettyPrinter") class and its
[`pformat()`](../library/pprint.html#pprint.pformat "pprint.pformat"), and [`pprint()`](../library/pprint.html#pprint.pprint "pprint.pprint") functions have a new
option, *compact*, that controls how the output is formatted. Currently
setting *compact* to `True` means that sequences will be printed with as many
sequence elements as will fit within *width* on each (indented) line.
(Contributed by Serhiy Storchaka in [bpo-19132](https://bugs.python.org/issue?@action=redirect&bpo=19132).)

Long strings are now wrapped using Python’s normal line continuation
syntax. (Contributed by Antoine Pitrou in [bpo-17150](https://bugs.python.org/issue?@action=redirect&bpo=17150).)

### pty

[`pty.spawn()`](../library/pty.html#pty.spawn "pty.spawn") now returns the status value from [`os.waitpid()`](../library/os.html#os.waitpid "os.waitpid") on
the child process, instead of `None`. (Contributed by Gregory P. Smith.)

### pydoc

The [`pydoc`](../library/pydoc.html#module-pydoc "pydoc: Documentation generator and online help system.") module is now based directly on the [`inspect.signature()`](../library/inspect.html#inspect.signature "inspect.signature")
introspection API, allowing it to provide signature information for a wider
variety of callable objects. This change also means that `__wrapped__`
attributes are now taken into account when displaying help information.
(Contributed by Larry Hastings in [bpo-19674](https://bugs.python.org/issue?@action=redirect&bpo=19674).)

The [`pydoc`](../library/pydoc.html#module-pydoc "pydoc: Documentation generator and online help system.") module no longer displays the `self` parameter for
already bound methods. Instead, it aims to always display the exact current
signature of the supplied callable. (Contributed by Larry Hastings in
[bpo-20710](https://bugs.python.org/issue?@action=redirect&bpo=20710).)

In addition to the changes that have been made to [`pydoc`](../library/pydoc.html#module-pydoc "pydoc: Documentation generator and online help system.") directly,
its handling of custom `__dir__` methods and various descriptor
behaviours has also been improved substantially by the underlying changes in
the [`inspect`](../library/inspect.html#module-inspect "inspect: Extract information and source code from live objects.") module.

As the [`help()`](../library/functions.html#help "help") builtin is based on [`pydoc`](../library/pydoc.html#module-pydoc "pydoc: Documentation generator and online help system."), the above changes also
affect the behaviour of [`help()`](../library/functions.html#help "help").

### re

New [`fullmatch()`](../library/re.html#re.fullmatch "re.fullmatch") function and `regex.fullmatch()` method anchor
the pattern at both ends of the string to match. This provides a way to be
explicit about the goal of the match, which avoids a class of subtle bugs where
`$` characters get lost during code changes or the addition of alternatives
to an existing regular expression. (Contributed by Matthew Barnett in
[bpo-16203](https://bugs.python.org/issue?@action=redirect&bpo=16203).)

The repr of [regex objects](../library/re.html#re-objects) now includes the pattern
and the flags; the repr of [match objects](../library/re.html#match-objects) now
includes the start, end, and the part of the string that matched. (Contributed
by Hugo Lopes Tavares and Serhiy Storchaka in [bpo-13592](https://bugs.python.org/issue?@action=redirect&bpo=13592) and
[bpo-17087](https://bugs.python.org/issue?@action=redirect&bpo=17087).)

### resource

New [`prlimit()`](../library/resource.html#resource.prlimit "resource.prlimit") function, available on Linux platforms with a
kernel version of 2.6.36 or later and glibc of 2.13 or later, provides the
ability to query or set the resource limits for processes other than the one
making the call. (Contributed by Christian Heimes in [bpo-16595](https://bugs.python.org/issue?@action=redirect&bpo=16595).)

On Linux kernel version 2.6.36 or later, there are also some new
Linux specific constants: [`RLIMIT_MSGQUEUE`](../library/resource.html#resource.RLIMIT_MSGQUEUE "resource.RLIMIT_MSGQUEUE"),
[`RLIMIT_NICE`](../library/resource.html#resource.RLIMIT_NICE "resource.RLIMIT_NICE"), [`RLIMIT_RTPRIO`](../library/resource.html#resource.RLIMIT_RTPRIO "resource.RLIMIT_RTPRIO"),
[`RLIMIT_RTTIME`](../library/resource.html#resource.RLIMIT_RTTIME "resource.RLIMIT_RTTIME"), and [`RLIMIT_SIGPENDING`](../library/resource.html#resource.RLIMIT_SIGPENDING "resource.RLIMIT_SIGPENDING").
(Contributed by Christian Heimes in [bpo-19324](https://bugs.python.org/issue?@action=redirect&bpo=19324).)

On FreeBSD version 9 and later, there some new FreeBSD specific constants:
[`RLIMIT_SBSIZE`](../library/resource.html#resource.RLIMIT_SBSIZE "resource.RLIMIT_SBSIZE"), [`RLIMIT_SWAP`](../library/resource.html#resource.RLIMIT_SWAP "resource.RLIMIT_SWAP"), and
[`RLIMIT_NPTS`](../library/resource.html#resource.RLIMIT_NPTS "resource.RLIMIT_NPTS"). (Contributed by Claudiu Popa in
[bpo-19343](https://bugs.python.org/issue?@action=redirect&bpo=19343).)

### select

[`epoll`](../library/select.html#select.epoll "select.epoll") objects now support the context management protocol.
When used in a [`with`](../reference/compound_stmts.html#with) statement, the [`close()`](../library/select.html#select.epoll.close "select.epoll.close")
method will be called automatically at the end of the block. (Contributed
by Serhiy Storchaka in [bpo-16488](https://bugs.python.org/issue?@action=redirect&bpo=16488).)

[`devpoll`](../library/select.html#select.devpoll "select.devpoll") objects now have [`fileno()`](../library/select.html#select.devpoll.fileno "select.devpoll.fileno") and
[`close()`](../library/select.html#select.devpoll.close "select.devpoll.close") methods, as well as a new attribute
[`closed`](../library/select.html#select.devpoll.closed "select.devpoll.closed"). (Contributed by Victor Stinner in
[bpo-18794](https://bugs.python.org/issue?@action=redirect&bpo=18794).)

### shelve

[`Shelf`](../library/shelve.html#shelve.Shelf "shelve.Shelf") instances may now be used in [`with`](../reference/compound_stmts.html#with) statements,
and will be automatically closed at the end of the `with` block.
(Contributed by Filip Gruszczyński in [bpo-13896](https://bugs.python.org/issue?@action=redirect&bpo=13896).)

### shutil

[`copyfile()`](../library/shutil.html#shutil.copyfile "shutil.copyfile") now raises a specific [`Error`](../library/shutil.html#shutil.Error "shutil.Error") subclass,
[`SameFileError`](../library/shutil.html#shutil.SameFileError "shutil.SameFileError"), when the source and destination are the same
file, which allows an application to take appropriate action on this specific
error. (Contributed by Atsuo Ishimoto and Hynek Schlawack in
[bpo-1492704](https://bugs.python.org/issue?@action=redirect&bpo=1492704).)

### smtpd

The `SMTPServer` and `SMTPChannel` classes now
accept a *map* keyword argument which, if specified, is passed in to
`asynchat.async_chat` as its *map* argument. This allows an application
to avoid affecting the global socket map. (Contributed by Vinay Sajip in
[bpo-11959](https://bugs.python.org/issue?@action=redirect&bpo=11959).)

### smtplib

[`SMTPException`](../library/smtplib.html#smtplib.SMTPException "smtplib.SMTPException") is now a subclass of [`OSError`](../library/exceptions.html#OSError "OSError"), which allows
both socket level errors and SMTP protocol level errors to be caught in one
try/except statement by code that only cares whether or not an error occurred.
(Contributed by Ned Jackson Lovely in [bpo-2118](https://bugs.python.org/issue?@action=redirect&bpo=2118).)

### socket

The socket module now supports the [`CAN_BCM`](../library/socket.html#socket.CAN_BCM "socket.CAN_BCM") protocol on
platforms that support it. (Contributed by Brian Thorne in [bpo-15359](https://bugs.python.org/issue?@action=redirect&bpo=15359).)

Socket objects have new methods to get or set their [inheritable flag](../library/os.html#fd-inheritance), [`get_inheritable()`](../library/socket.html#socket.socket.get_inheritable "socket.socket.get_inheritable") and
[`set_inheritable()`](../library/socket.html#socket.socket.set_inheritable "socket.socket.set_inheritable").

The `socket.AF_*` and `socket.SOCK_*` constants are now enumeration values
using the new [`enum`](../library/enum.html#module-enum "enum: Implementation of an enumeration class.") module. This allows meaningful names to be printed
during debugging, instead of integer “magic numbers”.

The [`AF_LINK`](../library/socket.html#socket.AF_LINK "socket.AF_LINK") constant is now available on BSD and OSX.

[`inet_pton()`](../library/socket.html#socket.inet_pton "socket.inet_pton") and [`inet_ntop()`](../library/socket.html#socket.inet_ntop "socket.inet_ntop") are now supported
on Windows. (Contributed by Atsuo Ishimoto in [bpo-7171](https://bugs.python.org/issue?@action=redirect&bpo=7171).)

### ssl

[`PROTOCOL_TLSv1_1`](../library/ssl.html#ssl.PROTOCOL_TLSv1_1 "ssl.PROTOCOL_TLSv1_1") and [`PROTOCOL_TLSv1_2`](../library/ssl.html#ssl.PROTOCOL_TLSv1_2 "ssl.PROTOCOL_TLSv1_2") (TLSv1.1 and
TLSv1.2 support) have been added; support for these protocols is only available if
Python is linked with OpenSSL 1.0.1 or later. (Contributed by Michele Orrù and
Antoine Pitrou in [bpo-16692](https://bugs.python.org/issue?@action=redirect&bpo=16692).)

New function [`create_default_context()`](../library/ssl.html#ssl.create_default_context "ssl.create_default_context") provides a standard way to
obtain an [`SSLContext`](../library/ssl.html#ssl.SSLContext "ssl.SSLContext") whose settings are intended to be a
reasonable balance between compatibility and security. These settings are
more stringent than the defaults provided by the [`SSLContext`](../library/ssl.html#ssl.SSLContext "ssl.SSLContext")
constructor, and may be adjusted in the future, without prior deprecation, if
best-practice security requirements change. The new recommended best
practice for using stdlib libraries that support SSL is to use
[`create_default_context()`](../library/ssl.html#ssl.create_default_context "ssl.create_default_context") to obtain an [`SSLContext`](../library/ssl.html#ssl.SSLContext "ssl.SSLContext")
object, modify it if needed, and then pass it as the *context* argument
of the appropriate stdlib API. (Contributed by Christian Heimes
in [bpo-19689](https://bugs.python.org/issue?@action=redirect&bpo=19689).)

[`SSLContext`](../library/ssl.html#ssl.SSLContext "ssl.SSLContext") method [`load_verify_locations()`](../library/ssl.html#ssl.SSLContext.load_verify_locations "ssl.SSLContext.load_verify_locations")
accepts a new optional argument *cadata*, which can be used to provide PEM or
DER encoded certificates directly via strings or bytes, respectively.
(Contributed by Christian Heimes in [bpo-18138](https://bugs.python.org/issue?@action=redirect&bpo=18138).)

New function [`get_default_verify_paths()`](../library/ssl.html#ssl.get_default_verify_paths "ssl.get_default_verify_paths") returns
a named tuple of the paths and environment variables that the
[`set_default_verify_paths()`](../library/ssl.html#ssl.SSLContext.set_default_verify_paths "ssl.SSLContext.set_default_verify_paths") method uses to set
OpenSSL’s default `cafile` and `capath`. This can be an aid in
debugging default verification issues. (Contributed by Christian Heimes
in [bpo-18143](https://bugs.python.org/issue?@action=redirect&bpo=18143).)

[`SSLContext`](../library/ssl.html#ssl.SSLContext "ssl.SSLContext") has a new method,
[`cert_store_stats()`](../library/ssl.html#ssl.SSLContext.cert_store_stats "ssl.SSLContext.cert_store_stats"), that reports the number of loaded
`X.509` certs, `X.509 CA` certs, and certificate revocation lists
(`crl`s), as well as a [`get_ca_certs()`](../library/ssl.html#ssl.SSLContext.get_ca_certs "ssl.SSLContext.get_ca_certs") method that
returns a list of the loaded `CA` certificates. (Contributed by Christian
Heimes in [bpo-18147](https://bugs.python.org/issue?@action=redirect&bpo=18147).)

If OpenSSL 0.9.8 or later is available, [`SSLContext`](../library/ssl.html#ssl.SSLContext "ssl.SSLContext") has a new
attribute [`verify_flags`](../library/ssl.html#ssl.SSLContext.verify_flags "ssl.SSLContext.verify_flags") that can be used to control the
certificate verification process by setting it to some combination of the new
constants [`VERIFY_DEFAULT`](../library/ssl.html#ssl.VERIFY_DEFAULT "ssl.VERIFY_DEFAULT"), [`VERIFY_CRL_CHECK_LEAF`](../library/ssl.html#ssl.VERIFY_CRL_CHECK_LEAF "ssl.VERIFY_CRL_CHECK_LEAF"),
[`VERIFY_CRL_CHECK_CHAIN`](../library/ssl.html#ssl.VERIFY_CRL_CHECK_CHAIN "ssl.VERIFY_CRL_CHECK_CHAIN"), or [`VERIFY_X509_STRICT`](../library/ssl.html#ssl.VERIFY_X509_STRICT "ssl.VERIFY_X509_STRICT").
OpenSSL does not do any CRL verification by default. (Contributed by
Christien Heimes in [bpo-8813](https://bugs.python.org/issue?@action=redirect&bpo=8813).)

New [`SSLContext`](../library/ssl.html#ssl.SSLContext "ssl.SSLContext") method [`load_default_certs()`](../library/ssl.html#ssl.SSLContext.load_default_certs "ssl.SSLContext.load_default_certs")
loads a set of default “certificate authority” (CA) certificates from default
locations, which vary according to the platform. It can be used to load both
TLS web server authentication certificates
(`purpose=`[`SERVER_AUTH`](../library/ssl.html#ssl.Purpose.SERVER_AUTH "ssl.Purpose.SERVER_AUTH")) for a client to use to verify a
server, and certificates for a server to use in verifying client certificates
(`purpose=`[`CLIENT_AUTH`](../library/ssl.html#ssl.Purpose.CLIENT_AUTH "ssl.Purpose.CLIENT_AUTH")). (Contributed by Christian
Heimes in [bpo-19292](https://bugs.python.org/issue?@action=redirect&bpo=19292).)

Two new windows-only functions, [`enum_certificates()`](../library/ssl.html#ssl.enum_certificates "ssl.enum_certificates") and
[`enum_crls()`](../library/ssl.html#ssl.enum_crls "ssl.enum_crls") provide the ability to retrieve certificates,
certificate information, and CRLs from the Windows cert store. (Contributed
by Christian Heimes in [bpo-17134](https://bugs.python.org/issue?@action=redirect&bpo=17134).)

Support for server-side SNI (Server Name Indication) using the new
[`ssl.SSLContext.set_servername_callback()`](../library/ssl.html#ssl.SSLContext.set_servername_callback "ssl.SSLContext.set_servername_callback") method.
(Contributed by Daniel Black in [bpo-8109](https://bugs.python.org/issue?@action=redirect&bpo=8109).)

The dictionary returned by [`SSLSocket.getpeercert()`](../library/ssl.html#ssl.SSLSocket.getpeercert "ssl.SSLSocket.getpeercert") contains additional
`X509v3` extension items: `crlDistributionPoints`, `calIssuers`, and
`OCSP` URIs. (Contributed by Christian Heimes in [bpo-18379](https://bugs.python.org/issue?@action=redirect&bpo=18379).)

### stat

The [`stat`](../library/stat.html#module-stat "stat: Utilities for interpreting the results of os.stat(), os.lstat() and os.fstat().") module is now backed by a C implementation in `_stat`. A C
implementation is required as most of the values aren’t standardized and
are platform-dependent. (Contributed by Christian Heimes in [bpo-11016](https://bugs.python.org/issue?@action=redirect&bpo=11016).)

The module supports new [`ST_MODE`](../library/stat.html#stat.ST_MODE "stat.ST_MODE") flags, [`S_IFDOOR`](../library/stat.html#stat.S_IFDOOR "stat.S_IFDOOR"),
[`S_IFPORT`](../library/stat.html#stat.S_IFPORT "stat.S_IFPORT"), and [`S_IFWHT`](../library/stat.html#stat.S_IFWHT "stat.S_IFWHT"). (Contributed by
Christian Hiemes in [bpo-11016](https://bugs.python.org/issue?@action=redirect&bpo=11016).)

### struct

New function [`iter_unpack`](../library/struct.html#struct.iter_unpack "struct.iter_unpack") and a new
[`struct.Struct.iter_unpack()`](../library/struct.html#struct.Struct.iter_unpack "struct.Struct.iter_unpack") method on compiled formats provide streamed
unpacking of a buffer containing repeated instances of a given format of data.
(Contributed by Antoine Pitrou in [bpo-17804](https://bugs.python.org/issue?@action=redirect&bpo=17804).)

### subprocess

[`check_output()`](../library/subprocess.html#subprocess.check_output "subprocess.check_output") now accepts an *input* argument that can
be used to provide the contents of `stdin` for the command that is run.
(Contributed by Zack Weinberg in [bpo-16624](https://bugs.python.org/issue?@action=redirect&bpo=16624).)

`getstatus()` and [`getstatusoutput()`](../library/subprocess.html#subprocess.getstatusoutput "subprocess.getstatusoutput") now
work on Windows. This change was actually inadvertently made in 3.3.4.
(Contributed by Tim Golden in [bpo-10197](https://bugs.python.org/issue?@action=redirect&bpo=10197).)

### sunau

The `getparams()` method now returns a namedtuple rather than a
plain tuple. (Contributed by Claudiu Popa in [bpo-18901](https://bugs.python.org/issue?@action=redirect&bpo=18901).)

`sunau.open()` now supports the context management protocol: when used in a
[`with`](../reference/compound_stmts.html#with) block, the `close` method of the returned object will be
called automatically at the end of the block. (Contributed by Serhiy Storchaka
in [bpo-18878](https://bugs.python.org/issue?@action=redirect&bpo=18878).)

`AU_write.setsampwidth()` now supports 24 bit samples, thus adding
support for writing 24 sample using the module. (Contributed by
Serhiy Storchaka in [bpo-19261](https://bugs.python.org/issue?@action=redirect&bpo=19261).)

The `writeframesraw()` and
`writeframes()` methods now accept any [bytes-like
object](../glossary.html#term-bytes-like-object). (Contributed by Serhiy Storchaka in [bpo-8311](https://bugs.python.org/issue?@action=redirect&bpo=8311).)

### sys

New function [`sys.getallocatedblocks()`](../library/sys.html#sys.getallocatedblocks "sys.getallocatedblocks") returns the current number of
blocks allocated by the interpreter. (In CPython with the default
`--with-pymalloc` setting, this is allocations made through the
[`PyObject_Malloc()`](../c-api/memory.html#c.PyObject_Malloc "PyObject_Malloc") API.) This can be useful for tracking memory leaks,
especially if automated via a test suite. (Contributed by Antoine Pitrou
in [bpo-13390](https://bugs.python.org/issue?@action=redirect&bpo=13390).)

When the Python interpreter starts in [interactive mode](../tutorial/interpreter.html#tut-interactive), it checks for an [`__interactivehook__`](../library/sys.html#sys.__interactivehook__ "sys.__interactivehook__") attribute
on the [`sys`](../library/sys.html#module-sys "sys: Access system-specific parameters and functions.") module. If the attribute exists, its value is called with no
arguments just before interactive mode is started. The check is made after the
[`PYTHONSTARTUP`](../using/cmdline.html#envvar-PYTHONSTARTUP) file is read, so it can be set there. The [`site`](../library/site.html#module-site "site: Module responsible for site-specific configuration.")
module [sets it](../library/site.html#rlcompleter-config) to a function that enables tab
completion and history saving (in `~/.python-history`) if the platform
supports [`readline`](../library/readline.html#module-readline "readline: GNU readline support for Python. (Unix)"). If you do not want this (new) behavior, you can
override it in [`PYTHONSTARTUP`](../using/cmdline.html#envvar-PYTHONSTARTUP), [`sitecustomize`](../library/site.html#module-sitecustomize "sitecustomize"), or
[`usercustomize`](../library/site.html#module-usercustomize "usercustomize") by deleting this attribute from [`sys`](../library/sys.html#module-sys "sys: Access system-specific parameters and functions.") (or setting it
to some other callable). (Contributed by Éric Araujo and Antoine Pitrou in
[bpo-5845](https://bugs.python.org/issue?@action=redirect&bpo=5845).)

### tarfile

The [`tarfile`](../library/tarfile.html#module-tarfile "tarfile: Read and write tar-format archive files.") module now supports a simple [Command-Line Interface](../library/tarfile.html#tarfile-commandline) when
called as a script directly or via `-m`. This can be used to create and
extract tarfile archives. (Contributed by Berker Peksag in [bpo-13477](https://bugs.python.org/issue?@action=redirect&bpo=13477).)

### textwrap

The [`TextWrapper`](../library/textwrap.html#textwrap.TextWrapper "textwrap.TextWrapper") class has two new attributes/constructor
arguments: [`max_lines`](../library/textwrap.html#textwrap.TextWrapper.max_lines "textwrap.TextWrapper.max_lines"), which limits the number of
lines in the output, and [`placeholder`](../library/textwrap.html#textwrap.TextWrapper.placeholder "textwrap.TextWrapper.placeholder"), which is a
string that will appear at the end of the output if it has been truncated
because of *max\_lines*. Building on these capabilities, a new convenience
function [`shorten()`](../library/textwrap.html#textwrap.shorten "textwrap.shorten") collapses all of the whitespace in the input
to single spaces and produces a single line of a given *width* that ends with
the *placeholder* (by default, `[...]`). (Contributed by Antoine Pitrou and
Serhiy Storchaka in [bpo-18585](https://bugs.python.org/issue?@action=redirect&bpo=18585) and [bpo-18725](https://bugs.python.org/issue?@action=redirect&bpo=18725).)

### threading

The [`Thread`](../library/threading.html#threading.Thread "threading.Thread") object representing the main thread can be
obtained from the new [`main_thread()`](../library/threading.html#threading.main_thread "threading.main_thread") function. In normal
conditions this will be the thread from which the Python interpreter was
started. (Contributed by Andrew Svetlov in [bpo-18882](https://bugs.python.org/issue?@action=redirect&bpo=18882).)

### traceback

A new [`traceback.clear_frames()`](../library/traceback.html#traceback.clear_frames "traceback.clear_frames") function takes a traceback object
and clears the local variables in all of the frames it references,
reducing the amount of memory consumed. (Contributed by Andrew Kuchling in
[bpo-1565525](https://bugs.python.org/issue?@action=redirect&bpo=1565525).)

### types

A new [`DynamicClassAttribute()`](../library/types.html#types.DynamicClassAttribute "types.DynamicClassAttribute") descriptor provides a way to define
an attribute that acts normally when looked up through an instance object, but
which is routed to the *class* `__getattr__` when looked up through the
class. This allows one to have properties active on a class, and have virtual
attributes on the class with the same name (see `Enum` for an example).
(Contributed by Ethan Furman in [bpo-19030](https://bugs.python.org/issue?@action=redirect&bpo=19030).)

### urllib

[`urllib.request`](../library/urllib.request.html#module-urllib.request "urllib.request: Extensible library for opening URLs.") now supports `data:` URLs via the
[`DataHandler`](../library/urllib.request.html#urllib.request.DataHandler "urllib.request.DataHandler") class. (Contributed by Mathias Panzenböck
in [bpo-16423](https://bugs.python.org/issue?@action=redirect&bpo=16423).)

The http method that will be used by a [`Request`](../library/urllib.request.html#urllib.request.Request "urllib.request.Request") class
can now be specified by setting a [`method`](../library/urllib.request.html#urllib.request.Request.method "urllib.request.Request.method")
class attribute on the subclass. (Contributed by Jason R Coombs in
[bpo-18978](https://bugs.python.org/issue?@action=redirect&bpo=18978).)

[`Request`](../library/urllib.request.html#urllib.request.Request "urllib.request.Request") objects are now reusable: if the
[`full_url`](../library/urllib.request.html#urllib.request.Request.full_url "urllib.request.Request.full_url") or [`data`](../library/urllib.request.html#urllib.request.Request.data "urllib.request.Request.data")
attributes are modified, all relevant internal properties are updated. This
means, for example, that it is now possible to use the same
[`Request`](../library/urllib.request.html#urllib.request.Request "urllib.request.Request") object in more than one
[`OpenerDirector.open()`](../library/urllib.request.html#urllib.request.OpenerDirector.open "urllib.request.OpenerDirector.open") call with different *data* arguments, or to
modify a [`Request`](../library/urllib.request.html#urllib.request.Request "urllib.request.Request")‘s `url` rather than recomputing it
from scratch. There is also a new
[`remove_header()`](../library/urllib.request.html#urllib.request.Request.remove_header "urllib.request.Request.remove_header") method that can be used to remove
headers from a [`Request`](../library/urllib.request.html#urllib.request.Request "urllib.request.Request"). (Contributed by Alexey
Kachayev in [bpo-16464](https://bugs.python.org/issue?@action=redirect&bpo=16464), Daniel Wozniak in [bpo-17485](https://bugs.python.org/issue?@action=redirect&bpo=17485), and Damien Brecht
and Senthil Kumaran in [bpo-17272](https://bugs.python.org/issue?@action=redirect&bpo=17272).)

[`HTTPError`](../library/urllib.error.html#urllib.error.HTTPError "urllib.error.HTTPError") objects now have a
[`headers`](../library/urllib.error.html#urllib.error.HTTPError.headers "urllib.error.HTTPError.headers") attribute that provides access to the
HTTP response headers associated with the error. (Contributed by
Berker Peksag in [bpo-15701](https://bugs.python.org/issue?@action=redirect&bpo=15701).)

### unittest

The [`TestCase`](../library/unittest.html#unittest.TestCase "unittest.TestCase") class has a new method,
[`subTest()`](../library/unittest.html#unittest.TestCase.subTest "unittest.TestCase.subTest"), that produces a context manager whose
[`with`](../reference/compound_stmts.html#with) block becomes a “sub-test”. This context manager allows a test
method to dynamically generate subtests by, say, calling the `subTest`
context manager inside a loop. A single test method can thereby produce an
indefinite number of separately identified and separately counted tests, all of
which will run even if one or more of them fail. For example:

Copy

```
class NumbersTest(unittest.TestCase):
    def test_even(self):
        for i in range(6):
            with self.subTest(i=i):
                self.assertEqual(i % 2, 0)

```

will result in six subtests, each identified in the unittest verbose output
with a label consisting of the variable name `i` and a particular value for
that variable (`i=0`, `i=1`, etc). See [Distinguishing test iterations using subtests](../library/unittest.html#subtests) for the full
version of this example. (Contributed by Antoine Pitrou in [bpo-16997](https://bugs.python.org/issue?@action=redirect&bpo=16997).)

[`unittest.main()`](../library/unittest.html#unittest.main "unittest.main") now accepts an iterable of test names for
*defaultTest*, where previously it only accepted a single test name as a
string. (Contributed by Jyrki Pulliainen in [bpo-15132](https://bugs.python.org/issue?@action=redirect&bpo=15132).)

If [`SkipTest`](../library/unittest.html#unittest.SkipTest "unittest.SkipTest") is raised during test discovery (that is, at the
module level in the test file), it is now reported as a skip instead of an
error. (Contributed by Zach Ware in [bpo-16935](https://bugs.python.org/issue?@action=redirect&bpo=16935).)

[`discover()`](../library/unittest.html#unittest.TestLoader.discover "unittest.TestLoader.discover") now sorts the discovered files to provide
consistent test ordering. (Contributed by Martin Melin and Jeff Ramnani in
[bpo-16709](https://bugs.python.org/issue?@action=redirect&bpo=16709).)

[`TestSuite`](../library/unittest.html#unittest.TestSuite "unittest.TestSuite") now drops references to tests as soon as the test
has been run, if the test is successful. On Python interpreters that do
garbage collection, this allows the tests to be garbage collected if nothing
else is holding a reference to the test. It is possible to override this
behavior by creating a [`TestSuite`](../library/unittest.html#unittest.TestSuite "unittest.TestSuite") subclass that defines a
custom `_removeTestAtIndex` method. (Contributed by Tom Wardill, Matt
McClure, and Andrew Svetlov in [bpo-11798](https://bugs.python.org/issue?@action=redirect&bpo=11798).)

A new test assertion context-manager, [`assertLogs()`](../library/unittest.html#unittest.TestCase.assertLogs "unittest.TestCase.assertLogs"),
will ensure that a given block of code emits a log message using the
[`logging`](../library/logging.html#module-logging "logging: Flexible event logging system for applications.") module. By default the message can come from any logger and
have a priority of `INFO` or higher, but both the logger name and an
alternative minimum logging level may be specified. The object returned by the
context manager can be queried for the [`LogRecord`](../library/logging.html#logging.LogRecord "logging.LogRecord")s and/or
formatted messages that were logged. (Contributed by Antoine Pitrou in
[bpo-18937](https://bugs.python.org/issue?@action=redirect&bpo=18937).)

Test discovery now works with namespace packages (Contributed by Claudiu Popa
in [bpo-17457](https://bugs.python.org/issue?@action=redirect&bpo=17457).)

[`unittest.mock`](../library/unittest.mock.html#module-unittest.mock "unittest.mock: Mock object library.") objects now inspect their specification signatures when
matching calls, which means an argument can now be matched by either position
or name, instead of only by position. (Contributed by Antoine Pitrou in
[bpo-17015](https://bugs.python.org/issue?@action=redirect&bpo=17015).)

`mock_open()` objects now have `readline` and `readlines`
methods. (Contributed by Toshio Kuratomi in [bpo-17467](https://bugs.python.org/issue?@action=redirect&bpo=17467).)

### venv

[`venv`](../library/venv.html#module-venv "venv: Creation of virtual environments.") now includes activation scripts for the `csh` and `fish`
shells. (Contributed by Andrew Svetlov in [bpo-15417](https://bugs.python.org/issue?@action=redirect&bpo=15417).)

[`EnvBuilder`](../library/venv.html#venv.EnvBuilder "venv.EnvBuilder") and the [`create()`](../library/venv.html#venv.create "venv.create") convenience function
take a new keyword argument *with\_pip*, which defaults to `False`, that
controls whether or not [`EnvBuilder`](../library/venv.html#venv.EnvBuilder "venv.EnvBuilder") ensures that `pip` is
installed in the virtual environment. (Contributed by Nick Coghlan in
[bpo-19552](https://bugs.python.org/issue?@action=redirect&bpo=19552) as part of the [**PEP 453**](https://peps.python.org/pep-0453/) implementation.)

### weakref

New [`WeakMethod`](../library/weakref.html#weakref.WeakMethod "weakref.WeakMethod") class simulates weak references to bound
methods. (Contributed by Antoine Pitrou in [bpo-14631](https://bugs.python.org/issue?@action=redirect&bpo=14631).)

New [`finalize`](../library/weakref.html#weakref.finalize "weakref.finalize") class makes it possible to register a callback
to be invoked when an object is garbage collected, without needing to
carefully manage the lifecycle of the weak reference itself. (Contributed by
Richard Oudkerk in [bpo-15528](https://bugs.python.org/issue?@action=redirect&bpo=15528).)

The callback, if any, associated with a [`ref`](../library/weakref.html#weakref.ref "weakref.ref") is now
exposed via the [`__callback__`](../library/weakref.html#weakref.ref.__callback__ "weakref.ref.__callback__") attribute. (Contributed
by Mark Dickinson in [bpo-17643](https://bugs.python.org/issue?@action=redirect&bpo=17643).)

### zipfile

The [`writepy()`](../library/zipfile.html#zipfile.PyZipFile.writepy "zipfile.PyZipFile.writepy") method of the
[`PyZipFile`](../library/zipfile.html#zipfile.PyZipFile "zipfile.PyZipFile") class has a new *filterfunc* option that can be
used to control which directories and files are added to the archive. For
example, this could be used to exclude test files from the archive.
(Contributed by Christian Tismer in [bpo-19274](https://bugs.python.org/issue?@action=redirect&bpo=19274).)

The *allowZip64* parameter to [`ZipFile`](../library/zipfile.html#zipfile.ZipFile "zipfile.ZipFile") and
`PyZipfile` is now `True` by default. (Contributed by
William Mallard in [bpo-17201](https://bugs.python.org/issue?@action=redirect&bpo=17201).)