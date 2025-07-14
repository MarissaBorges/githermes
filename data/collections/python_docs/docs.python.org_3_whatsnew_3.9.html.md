This article explains the new features in Python 3.9, compared to 3.8.
Python 3.9 was released on October 5, 2020.
For full details, see the [changelog](changelog.html#changelog).

You should check for DeprecationWarning in your code
----------------------------------------------------

When Python 2.7 was still supported, a lot of functionality in Python 3
was kept for backward compatibility with Python 2.7. With the end of Python
2 support, these backward compatibility layers have been removed, or will
be removed soon. Most of them emitted a [`DeprecationWarning`](../library/exceptions.html#DeprecationWarning "DeprecationWarning") warning for
several years. For example, using `collections.Mapping` instead of
`collections.abc.Mapping` emits a [`DeprecationWarning`](../library/exceptions.html#DeprecationWarning "DeprecationWarning") since Python
3.3, released in 2012.

Test your application with the [`-W`](../using/cmdline.html#cmdoption-W) `default` command-line option to see
[`DeprecationWarning`](../library/exceptions.html#DeprecationWarning "DeprecationWarning") and [`PendingDeprecationWarning`](../library/exceptions.html#PendingDeprecationWarning "PendingDeprecationWarning"), or even with
[`-W`](../using/cmdline.html#cmdoption-W) `error` to treat them as errors. [Warnings Filter](../library/warnings.html#warning-filter) can be used to ignore warnings from third-party code.

Python 3.9 is the last version providing those Python 2 backward compatibility
layers, to give more time to Python projects maintainers to organize the
removal of the Python 2 support and add support for Python 3.9.

Aliases to [Abstract Base Classes](../library/collections.abc.html#collections-abstract-base-classes) in
the [`collections`](../library/collections.html#module-collections "collections: Container datatypes") module, like `collections.Mapping` alias to
[`collections.abc.Mapping`](../library/collections.abc.html#collections.abc.Mapping "collections.abc.Mapping"), are kept for one last release for backward
compatibility. They will be removed from Python 3.10.

More generally, try to run your tests in the [Python Development Mode](../library/devmode.html#devmode) which helps to prepare your code to make it compatible with the
next Python version.

Note: a number of pre-existing deprecations were removed in this version of
Python as well. Consult the [Removed](#removed-in-python-39) section.

Improved Modules
----------------

### ast

Added the *indent* option to [`dump()`](../library/ast.html#ast.dump "ast.dump") which allows it to produce a
multiline indented output.
(Contributed by Serhiy Storchaka in [bpo-37995](https://bugs.python.org/issue?@action=redirect&bpo=37995).)

Added [`ast.unparse()`](../library/ast.html#ast.unparse "ast.unparse") as a function in the [`ast`](../library/ast.html#module-ast "ast: Abstract Syntax Tree classes and manipulation.") module that can
be used to unparse an [`ast.AST`](../library/ast.html#ast.AST "ast.AST") object and produce a string with code
that would produce an equivalent [`ast.AST`](../library/ast.html#ast.AST "ast.AST") object when parsed.
(Contributed by Pablo Galindo and Batuhan Taskaya in [bpo-38870](https://bugs.python.org/issue?@action=redirect&bpo=38870).)

Added docstrings to AST nodes that contains the ASDL signature used to
construct that node. (Contributed by Batuhan Taskaya in [bpo-39638](https://bugs.python.org/issue?@action=redirect&bpo=39638).)

### asyncio

Due to significant security concerns, the *reuse\_address* parameter of
[`asyncio.loop.create_datagram_endpoint()`](../library/asyncio-eventloop.html#asyncio.loop.create_datagram_endpoint "asyncio.loop.create_datagram_endpoint") is no longer supported. This is
because of the behavior of the socket option `SO_REUSEADDR` in UDP. For more
details, see the documentation for `loop.create_datagram_endpoint()`.
(Contributed by Kyle Stanley, Antoine Pitrou, and Yury Selivanov in
[bpo-37228](https://bugs.python.org/issue?@action=redirect&bpo=37228).)

Added a new [coroutine](../glossary.html#term-coroutine) [`shutdown_default_executor()`](../library/asyncio-eventloop.html#asyncio.loop.shutdown_default_executor "asyncio.loop.shutdown_default_executor")
that schedules a shutdown for the default executor that waits on the
[`ThreadPoolExecutor`](../library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor "concurrent.futures.ThreadPoolExecutor") to finish closing. Also,
[`asyncio.run()`](../library/asyncio-runner.html#asyncio.run "asyncio.run") has been updated to use the new [coroutine](../glossary.html#term-coroutine).
(Contributed by Kyle Stanley in [bpo-34037](https://bugs.python.org/issue?@action=redirect&bpo=34037).)

Added [`asyncio.PidfdChildWatcher`](../library/asyncio-policy.html#asyncio.PidfdChildWatcher "asyncio.PidfdChildWatcher"), a Linux-specific child watcher
implementation that polls process file descriptors. ([bpo-38692](https://bugs.python.org/issue?@action=redirect&bpo=38692))

Added a new [coroutine](../glossary.html#term-coroutine) [`asyncio.to_thread()`](../library/asyncio-task.html#asyncio.to_thread "asyncio.to_thread"). It is mainly used for
running IO-bound functions in a separate thread to avoid blocking the event
loop, and essentially works as a high-level version of
[`run_in_executor()`](../library/asyncio-eventloop.html#asyncio.loop.run_in_executor "asyncio.loop.run_in_executor") that can directly take keyword arguments.
(Contributed by Kyle Stanley and Yury Selivanov in [bpo-32309](https://bugs.python.org/issue?@action=redirect&bpo=32309).)

When cancelling the task due to a timeout, [`asyncio.wait_for()`](../library/asyncio-task.html#asyncio.wait_for "asyncio.wait_for") will now
wait until the cancellation is complete also in the case when *timeout* is
<= 0, like it does with positive timeouts.
(Contributed by Elvis Pranskevichus in [bpo-32751](https://bugs.python.org/issue?@action=redirect&bpo=32751).)

[`asyncio`](../library/asyncio.html#module-asyncio "asyncio: Asynchronous I/O.") now raises [`TypeError`](../library/exceptions.html#TypeError "TypeError") when calling incompatible
methods with an [`ssl.SSLSocket`](../library/ssl.html#ssl.SSLSocket "ssl.SSLSocket") socket.
(Contributed by Ido Michael in [bpo-37404](https://bugs.python.org/issue?@action=redirect&bpo=37404).)

### compileall

Added new possibility to use hardlinks for duplicated `.pyc` files: *hardlink\_dupes* parameter and –hardlink-dupes command line option.
(Contributed by Lumír ‘Frenzy’ Balhar in [bpo-40495](https://bugs.python.org/issue?@action=redirect&bpo=40495).)

Added new options for path manipulation in resulting `.pyc` files: *stripdir*, *prependdir*, *limit\_sl\_dest* parameters and -s, -p, -e command line options.
Added the possibility to specify the option for an optimization level multiple times.
(Contributed by Lumír ‘Frenzy’ Balhar in [bpo-38112](https://bugs.python.org/issue?@action=redirect&bpo=38112).)

### concurrent.futures

Added a new *cancel\_futures* parameter to
[`concurrent.futures.Executor.shutdown()`](../library/concurrent.futures.html#concurrent.futures.Executor.shutdown "concurrent.futures.Executor.shutdown") that cancels all pending futures
which have not started running, instead of waiting for them to complete before
shutting down the executor.
(Contributed by Kyle Stanley in [bpo-39349](https://bugs.python.org/issue?@action=redirect&bpo=39349).)

Removed daemon threads from [`ThreadPoolExecutor`](../library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor "concurrent.futures.ThreadPoolExecutor")
and [`ProcessPoolExecutor`](../library/concurrent.futures.html#concurrent.futures.ProcessPoolExecutor "concurrent.futures.ProcessPoolExecutor"). This improves
compatibility with subinterpreters and predictability in their shutdown
processes. (Contributed by Kyle Stanley in [bpo-39812](https://bugs.python.org/issue?@action=redirect&bpo=39812).)

Workers in [`ProcessPoolExecutor`](../library/concurrent.futures.html#concurrent.futures.ProcessPoolExecutor "concurrent.futures.ProcessPoolExecutor") are now spawned on
demand, only when there are no available idle workers to reuse. This optimizes
startup overhead and reduces the amount of lost CPU time to idle workers.
(Contributed by Kyle Stanley in [bpo-39207](https://bugs.python.org/issue?@action=redirect&bpo=39207).)

### distutils

The **upload** command now creates SHA2-256 and Blake2b-256 hash
digests. It skips MD5 on platforms that block MD5 digest.
(Contributed by Christian Heimes in [bpo-40698](https://bugs.python.org/issue?@action=redirect&bpo=40698).)

### fcntl

Added constants `fcntl.F_OFD_GETLK`, `fcntl.F_OFD_SETLK`
and `fcntl.F_OFD_SETLKW`.
(Contributed by Donghee Na in [bpo-38602](https://bugs.python.org/issue?@action=redirect&bpo=38602).)

### ftplib

[`FTP`](../library/ftplib.html#ftplib.FTP "ftplib.FTP") and [`FTP_TLS`](../library/ftplib.html#ftplib.FTP_TLS "ftplib.FTP_TLS") now raise a [`ValueError`](../library/exceptions.html#ValueError "ValueError")
if the given timeout for their constructor is zero to prevent the creation of
a non-blocking socket. (Contributed by Donghee Na in [bpo-39259](https://bugs.python.org/issue?@action=redirect&bpo=39259).)

### gc

When the garbage collector makes a collection in which some objects resurrect
(they are reachable from outside the isolated cycles after the finalizers have
been executed), do not block the collection of all objects that are still
unreachable. (Contributed by Pablo Galindo and Tim Peters in [bpo-38379](https://bugs.python.org/issue?@action=redirect&bpo=38379).)

Added a new function [`gc.is_finalized()`](../library/gc.html#gc.is_finalized "gc.is_finalized") to check if an object has been
finalized by the garbage collector. (Contributed by Pablo Galindo in
[bpo-39322](https://bugs.python.org/issue?@action=redirect&bpo=39322).)

### hashlib

The [`hashlib`](../library/hashlib.html#module-hashlib "hashlib: Secure hash and message digest algorithms.") module can now use SHA3 hashes and SHAKE XOF from OpenSSL
when available.
(Contributed by Christian Heimes in [bpo-37630](https://bugs.python.org/issue?@action=redirect&bpo=37630).)

Builtin hash modules can now be disabled with
`./configure --without-builtin-hashlib-hashes` or selectively enabled with
e.g. `./configure --with-builtin-hashlib-hashes=sha3,blake2` to force use
of OpenSSL based implementation.
(Contributed by Christian Heimes in [bpo-40479](https://bugs.python.org/issue?@action=redirect&bpo=40479))

### http

HTTP status codes `103 EARLY_HINTS`, `418 IM_A_TEAPOT` and `425 TOO_EARLY` are added to
[`http.HTTPStatus`](../library/http.html#http.HTTPStatus "http.HTTPStatus"). (Contributed by Donghee Na in [bpo-39509](https://bugs.python.org/issue?@action=redirect&bpo=39509) and Ross Rhodes in [bpo-39507](https://bugs.python.org/issue?@action=redirect&bpo=39507).)

### IDLE and idlelib

Added option to toggle cursor blink off. (Contributed by Zackery Spytz
in [bpo-4603](https://bugs.python.org/issue?@action=redirect&bpo=4603).)

Escape key now closes IDLE completion windows. (Contributed by Johnny
Najera in [bpo-38944](https://bugs.python.org/issue?@action=redirect&bpo=38944).)

Added keywords to module name completion list. (Contributed by Terry J.
Reedy in [bpo-37765](https://bugs.python.org/issue?@action=redirect&bpo=37765).)

New in 3.9 maintenance releases

Make IDLE invoke [`sys.excepthook()`](../library/sys.html#sys.excepthook "sys.excepthook") (when started without ‘-n’).
User hooks were previously ignored. (Contributed by Ken Hilton in
[bpo-43008](https://bugs.python.org/issue?@action=redirect&bpo=43008).)

The changes above have been backported to 3.8 maintenance releases.

Rearrange the settings dialog. Split the General tab into Windows
and Shell/Ed tabs. Move help sources, which extend the Help menu, to the
Extensions tab. Make space for new options and shorten the dialog. The
latter makes the dialog better fit small screens. (Contributed by Terry Jan
Reedy in [bpo-40468](https://bugs.python.org/issue?@action=redirect&bpo=40468).) Move the indent space setting from the Font tab to
the new Windows tab. (Contributed by Mark Roseman and Terry Jan Reedy in
[bpo-33962](https://bugs.python.org/issue?@action=redirect&bpo=33962).)

Apply syntax highlighting to `.pyi` files. (Contributed by Alex
Waygood and Terry Jan Reedy in [bpo-45447](https://bugs.python.org/issue?@action=redirect&bpo=45447).)

### imaplib

[`IMAP4`](../library/imaplib.html#imaplib.IMAP4 "imaplib.IMAP4") and [`IMAP4_SSL`](../library/imaplib.html#imaplib.IMAP4_SSL "imaplib.IMAP4_SSL") now have
an optional *timeout* parameter for their constructors.
Also, the [`open()`](../library/imaplib.html#imaplib.IMAP4.open "imaplib.IMAP4.open") method now has an optional *timeout* parameter
with this change. The overridden methods of [`IMAP4_SSL`](../library/imaplib.html#imaplib.IMAP4_SSL "imaplib.IMAP4_SSL") and
[`IMAP4_stream`](../library/imaplib.html#imaplib.IMAP4_stream "imaplib.IMAP4_stream") were applied to this change.
(Contributed by Donghee Na in [bpo-38615](https://bugs.python.org/issue?@action=redirect&bpo=38615).)

[`imaplib.IMAP4.unselect()`](../library/imaplib.html#imaplib.IMAP4.unselect "imaplib.IMAP4.unselect") is added.
[`imaplib.IMAP4.unselect()`](../library/imaplib.html#imaplib.IMAP4.unselect "imaplib.IMAP4.unselect") frees server’s resources associated with the
selected mailbox and returns the server to the authenticated
state. This command performs the same actions as [`imaplib.IMAP4.close()`](../library/imaplib.html#imaplib.IMAP4.close "imaplib.IMAP4.close"), except
that no messages are permanently removed from the currently
selected mailbox. (Contributed by Donghee Na in [bpo-40375](https://bugs.python.org/issue?@action=redirect&bpo=40375).)

### importlib

To improve consistency with import statements, [`importlib.util.resolve_name()`](../library/importlib.html#importlib.util.resolve_name "importlib.util.resolve_name")
now raises [`ImportError`](../library/exceptions.html#ImportError "ImportError") instead of [`ValueError`](../library/exceptions.html#ValueError "ValueError") for invalid relative
import attempts.
(Contributed by Ngalim Siregar in [bpo-37444](https://bugs.python.org/issue?@action=redirect&bpo=37444).)

Import loaders which publish immutable module objects can now publish
immutable packages in addition to individual modules.
(Contributed by Dino Viehland in [bpo-39336](https://bugs.python.org/issue?@action=redirect&bpo=39336).)

Added [`importlib.resources.files()`](../library/importlib.resources.html#importlib.resources.files "importlib.resources.files") function with support for
subdirectories in package data, matching backport in `importlib_resources`
version 1.5.
(Contributed by Jason R. Coombs in [bpo-39791](https://bugs.python.org/issue?@action=redirect&bpo=39791).)

Refreshed `importlib.metadata` from `importlib_metadata` version 1.6.1.

### ipaddress

[`ipaddress`](../library/ipaddress.html#module-ipaddress "ipaddress: IPv4/IPv6 manipulation library.") now supports IPv6 Scoped Addresses (IPv6 address with suffix `%<scope_id>`).

Scoped IPv6 addresses can be parsed using [`ipaddress.IPv6Address`](../library/ipaddress.html#ipaddress.IPv6Address "ipaddress.IPv6Address").
If present, scope zone ID is available through the [`scope_id`](../library/ipaddress.html#ipaddress.IPv6Address.scope_id "ipaddress.IPv6Address.scope_id") attribute.
(Contributed by Oleksandr Pavliuk in [bpo-34788](https://bugs.python.org/issue?@action=redirect&bpo=34788).)

Starting with Python 3.9.5 the [`ipaddress`](../library/ipaddress.html#module-ipaddress "ipaddress: IPv4/IPv6 manipulation library.") module no longer
accepts any leading zeros in IPv4 address strings.
(Contributed by Christian Heimes in [bpo-36384](https://bugs.python.org/issue?@action=redirect&bpo=36384)).

### math

Expanded the [`math.gcd()`](../library/math.html#math.gcd "math.gcd") function to handle multiple arguments.
Formerly, it only supported two arguments.
(Contributed by Serhiy Storchaka in [bpo-39648](https://bugs.python.org/issue?@action=redirect&bpo=39648).)

Added [`math.lcm()`](../library/math.html#math.lcm "math.lcm"): return the least common multiple of specified arguments.
(Contributed by Mark Dickinson, Ananthakrishnan and Serhiy Storchaka in
[bpo-39479](https://bugs.python.org/issue?@action=redirect&bpo=39479) and [bpo-39648](https://bugs.python.org/issue?@action=redirect&bpo=39648).)

Added [`math.nextafter()`](../library/math.html#math.nextafter "math.nextafter"): return the next floating-point value after *x*
towards *y*.
(Contributed by Victor Stinner in [bpo-39288](https://bugs.python.org/issue?@action=redirect&bpo=39288).)

Added [`math.ulp()`](../library/math.html#math.ulp "math.ulp"): return the value of the least significant bit
of a float.
(Contributed by Victor Stinner in [bpo-39310](https://bugs.python.org/issue?@action=redirect&bpo=39310).)

### nntplib

`NNTP` and `NNTP_SSL` now raise a [`ValueError`](../library/exceptions.html#ValueError "ValueError")
if the given timeout for their constructor is zero to prevent the creation of
a non-blocking socket. (Contributed by Donghee Na in [bpo-39259](https://bugs.python.org/issue?@action=redirect&bpo=39259).)

### pdb

On Windows now [`Pdb`](../library/pdb.html#pdb.Pdb "pdb.Pdb") supports `~/.pdbrc`.
(Contributed by Tim Hopper and Dan Lidral-Porter in [bpo-20523](https://bugs.python.org/issue?@action=redirect&bpo=20523).)

### poplib

[`POP3`](../library/poplib.html#poplib.POP3 "poplib.POP3") and [`POP3_SSL`](../library/poplib.html#poplib.POP3_SSL "poplib.POP3_SSL") now raise a [`ValueError`](../library/exceptions.html#ValueError "ValueError")
if the given timeout for their constructor is zero to prevent the creation of
a non-blocking socket. (Contributed by Donghee Na in [bpo-39259](https://bugs.python.org/issue?@action=redirect&bpo=39259).)

### pydoc

The documentation string is now shown not only for class, function,
method etc, but for any object that has its own [`__doc__`](../library/stdtypes.html#definition.__doc__ "definition.__doc__")
attribute.
(Contributed by Serhiy Storchaka in [bpo-40257](https://bugs.python.org/issue?@action=redirect&bpo=40257).)

### smtplib

[`SMTP`](../library/smtplib.html#smtplib.SMTP "smtplib.SMTP") and [`SMTP_SSL`](../library/smtplib.html#smtplib.SMTP_SSL "smtplib.SMTP_SSL") now raise a [`ValueError`](../library/exceptions.html#ValueError "ValueError")
if the given timeout for their constructor is zero to prevent the creation of
a non-blocking socket. (Contributed by Donghee Na in [bpo-39259](https://bugs.python.org/issue?@action=redirect&bpo=39259).)

[`LMTP`](../library/smtplib.html#smtplib.LMTP "smtplib.LMTP") constructor now has an optional *timeout* parameter.
(Contributed by Donghee Na in [bpo-39329](https://bugs.python.org/issue?@action=redirect&bpo=39329).)

### time

On AIX, [`thread_time()`](../library/time.html#time.thread_time "time.thread_time") is now implemented with `thread_cputime()`
which has nanosecond resolution, rather than
`clock_gettime(CLOCK_THREAD_CPUTIME_ID)` which has a resolution of 10 milliseconds.
(Contributed by Batuhan Taskaya in [bpo-40192](https://bugs.python.org/issue?@action=redirect&bpo=40192))

### sys

Added a new [`sys.platlibdir`](../library/sys.html#sys.platlibdir "sys.platlibdir") attribute: name of the platform-specific
library directory. It is used to build the path of standard library and the
paths of installed extension modules. It is equal to `"lib"` on most
platforms. On Fedora and SuSE, it is equal to `"lib64"` on 64-bit platforms.
(Contributed by Jan Matějek, Matěj Cepl, Charalampos Stratakis and Victor Stinner in [bpo-1294959](https://bugs.python.org/issue?@action=redirect&bpo=1294959).)

Previously, [`sys.stderr`](../library/sys.html#sys.stderr "sys.stderr") was block-buffered when non-interactive. Now
`stderr` defaults to always being line-buffered.
(Contributed by Jendrik Seipp in [bpo-13601](https://bugs.python.org/issue?@action=redirect&bpo=13601).)

### tracemalloc

Added [`tracemalloc.reset_peak()`](../library/tracemalloc.html#tracemalloc.reset_peak "tracemalloc.reset_peak") to set the peak size of traced memory
blocks to the current size, to measure the peak of specific pieces of code.
(Contributed by Huon Wilson in [bpo-40630](https://bugs.python.org/issue?@action=redirect&bpo=40630).)

### typing

[**PEP 593**](https://peps.python.org/pep-0593/) introduced an [`typing.Annotated`](../library/typing.html#typing.Annotated "typing.Annotated") type to decorate existing
types with context-specific metadata and new `include_extras` parameter to
[`typing.get_type_hints()`](../library/typing.html#typing.get_type_hints "typing.get_type_hints") to access the metadata at runtime. (Contributed
by Till Varoquaux and Konstantin Kashin.)

### unicodedata

The Unicode database has been updated to version 13.0.0. ([bpo-39926](https://bugs.python.org/issue?@action=redirect&bpo=39926)).

### venv

The activation scripts provided by [`venv`](../library/venv.html#module-venv "venv: Creation of virtual environments.") now all specify their prompt
customization consistently by always using the value specified by
`__VENV_PROMPT__`. Previously some scripts unconditionally used
`__VENV_PROMPT__`, others only if it happened to be set (which was the default
case), and one used `__VENV_NAME__` instead.
(Contributed by Brett Cannon in [bpo-37663](https://bugs.python.org/issue?@action=redirect&bpo=37663).)

### xml

White space characters within attributes are now preserved when serializing
[`xml.etree.ElementTree`](../library/xml.etree.elementtree.html#module-xml.etree.ElementTree "xml.etree.ElementTree: Implementation of the ElementTree API.") to XML file. EOLNs are no longer normalized
to “n”. This is the result of discussion about how to interpret
section 2.11 of XML spec.
(Contributed by Mefistotelis in [bpo-39011](https://bugs.python.org/issue?@action=redirect&bpo=39011).)