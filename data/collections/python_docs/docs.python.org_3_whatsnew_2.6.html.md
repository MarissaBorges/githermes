As in every release, Python’s standard library received a number of
enhancements and bug fixes. Here’s a partial list of the most notable
changes, sorted alphabetically by module name. Consult the
`Misc/NEWS` file in the source tree for a more complete list of
changes, or look through the Subversion logs for all the details.

* The `asyncore` and `asynchat` modules are
  being actively maintained again, and a number of patches and bugfixes
  were applied. (Maintained by Josiah Carlson; see [bpo-1736190](https://bugs.python.org/issue?@action=redirect&bpo=1736190) for
  one patch.)
* The `bsddb` module also has a new maintainer, Jesús Cea Avión, and the package
  is now available as a standalone package. The web page for the package is
  [www.jcea.es/programacion/pybsddb.htm](https://www.jcea.es/programacion/pybsddb.htm).
  The plan is to remove the package from the standard library
  in Python 3.0, because its pace of releases is much more frequent than
  Python’s.

  The `bsddb.dbshelve` module now uses the highest pickling protocol
  available, instead of restricting itself to protocol 1.
  (Contributed by W. Barnes.)
* The `cgi` module will now read variables from the query string
  of an HTTP POST request. This makes it possible to use form actions
  with URLs that include query strings such as
  “/cgi-bin/add.py?category=1”. (Contributed by Alexandre Fiori and
  Nubis; [bpo-1817](https://bugs.python.org/issue?@action=redirect&bpo=1817).)

  The `parse_qs()` and `parse_qsl()` functions have been
  relocated from the `cgi` module to the [`urlparse`](../library/urllib.parse.html#module-urllib.parse "urllib.parse: Parse URLs into or assemble them from components.") module.
  The versions still available in the `cgi` module will
  trigger [`PendingDeprecationWarning`](../library/exceptions.html#PendingDeprecationWarning "PendingDeprecationWarning") messages in 2.6
  ([bpo-600362](https://bugs.python.org/issue?@action=redirect&bpo=600362)).
* The [`cmath`](../library/cmath.html#module-cmath "cmath: Mathematical functions for complex numbers.") module underwent extensive revision,
  contributed by Mark Dickinson and Christian Heimes.
  Five new functions were added:

  + `polar()` converts a complex number to polar form, returning
    the modulus and argument of the complex number.
  + `rect()` does the opposite, turning a modulus, argument pair
    back into the corresponding complex number.
  + `phase()` returns the argument (also called the angle) of a complex
    number.
  + `isnan()` returns True if either
    the real or imaginary part of its argument is a NaN.
  + `isinf()` returns True if either the real or imaginary part of
    its argument is infinite.

  The revisions also improved the numerical soundness of the
  [`cmath`](../library/cmath.html#module-cmath "cmath: Mathematical functions for complex numbers.") module. For all functions, the real and imaginary
  parts of the results are accurate to within a few units of least
  precision (ulps) whenever possible. See [bpo-1381](https://bugs.python.org/issue?@action=redirect&bpo=1381) for the
  details. The branch cuts for `asinh()`, `atanh()`: and
  `atan()` have also been corrected.

  The tests for the module have been greatly expanded; nearly 2000 new
  test cases exercise the algebraic functions.

  On IEEE 754 platforms, the [`cmath`](../library/cmath.html#module-cmath "cmath: Mathematical functions for complex numbers.") module now handles IEEE 754
  special values and floating-point exceptions in a manner consistent
  with Annex ‘G’ of the C99 standard.
* A new data type in the [`collections`](../library/collections.html#module-collections "collections: Container datatypes") module: `namedtuple(typename, fieldnames)`
  is a factory function that creates subclasses of the standard tuple
  whose fields are accessible by name as well as index. For example:

  Copy

  ```
  >>> var_type = collections.namedtuple('variable',
  ...             'id name type size')
  >>> # Names are separated by spaces or commas.
  >>> # 'id, name, type, size' would also work.
  >>> var_type._fields
  ('id', 'name', 'type', 'size')

  >>> var = var_type(1, 'frequency', 'int', 4)
  >>> print var[0], var.id    # Equivalent
  1 1
  >>> print var[2], var.type  # Equivalent
  int int
  >>> var._asdict()
  {'size': 4, 'type': 'int', 'id': 1, 'name': 'frequency'}
  >>> v2 = var._replace(name='amplitude')
  >>> v2
  variable(id=1, name='amplitude', type='int', size=4)

  ```

  Several places in the standard library that returned tuples have
  been modified to return `namedtuple()` instances. For example,
  the `Decimal.as_tuple()` method now returns a named tuple with
  `sign`, `digits`, and `exponent` fields.

  (Contributed by Raymond Hettinger.)
* Another change to the [`collections`](../library/collections.html#module-collections "collections: Container datatypes") module is that the
  `deque` type now supports an optional *maxlen* parameter;
  if supplied, the deque’s size will be restricted to no more
  than *maxlen* items. Adding more items to a full deque causes
  old items to be discarded.

  Copy

  ```
  >>> from collections import deque
  >>> dq=deque(maxlen=3)
  >>> dq
  deque([], maxlen=3)
  >>> dq.append(1); dq.append(2); dq.append(3)
  >>> dq
  deque([1, 2, 3], maxlen=3)
  >>> dq.append(4)
  >>> dq
  deque([2, 3, 4], maxlen=3)

  ```

  (Contributed by Raymond Hettinger.)
* The [`Cookie`](../library/http.cookies.html#module-http.cookies "http.cookies: Support for HTTP state management (cookies).") module’s [`Morsel`](../library/http.cookies.html#http.cookies.Morsel "http.cookies.Morsel") objects now support an
  [`httponly`](../library/http.cookies.html#http.cookies.Morsel.httponly "http.cookies.Morsel.httponly") attribute. In some browsers. cookies with this attribute
  set cannot be accessed or manipulated by JavaScript code.
  (Contributed by Arvin Schnell; [bpo-1638033](https://bugs.python.org/issue?@action=redirect&bpo=1638033).)
* A new window method in the [`curses`](../library/curses.html#module-curses "curses: An interface to the curses library, providing portable terminal handling. (Unix)") module,
  `chgat()`, changes the display attributes for a certain number of
  characters on a single line. (Contributed by Fabian Kreutz.)

  Copy

  ```
  # Boldface text starting at y=0,x=21
  # and affecting the rest of the line.
  stdscr.chgat(0, 21, curses.A_BOLD)

  ```

  The `Textbox` class in the [`curses.textpad`](../library/curses.html#module-curses.textpad "curses.textpad: Emacs-like input editing in a curses window.") module
  now supports editing in insert mode as well as overwrite mode.
  Insert mode is enabled by supplying a true value for the *insert\_mode*
  parameter when creating the `Textbox` instance.
* The [`datetime`](../library/datetime.html#module-datetime "datetime: Basic date and time types.") module’s `strftime()` methods now support a
  `%f` format code that expands to the number of microseconds in the
  object, zero-padded on
  the left to six places. (Contributed by Skip Montanaro; [bpo-1158](https://bugs.python.org/issue?@action=redirect&bpo=1158).)
* The [`decimal`](../library/decimal.html#module-decimal "decimal: Implementation of the General Decimal Arithmetic Specification.") module was updated to version 1.66 of
  [the General Decimal Specification](https://speleotrove.com/decimal/decarith.html). New features
  include some methods for some basic mathematical functions such as
  `exp()` and `log10()`:

  Copy

  ```
  >>> Decimal(1).exp()
  Decimal("2.718281828459045235360287471")
  >>> Decimal("2.7182818").ln()
  Decimal("0.9999999895305022877376682436")
  >>> Decimal(1000).log10()
  Decimal("3")

  ```

  The `as_tuple()` method of `Decimal` objects now returns a
  named tuple with `sign`, `digits`, and `exponent` fields.

  (Implemented by Facundo Batista and Mark Dickinson. Named tuple
  support added by Raymond Hettinger.)
* The [`difflib`](../library/difflib.html#module-difflib "difflib: Helpers for computing differences between objects.") module’s `SequenceMatcher` class
  now returns named tuples representing matches,
  with `a`, `b`, and `size` attributes.
  (Contributed by Raymond Hettinger.)
* An optional `timeout` parameter, specifying a timeout measured in
  seconds, was added to the [`ftplib.FTP`](../library/ftplib.html#ftplib.FTP "ftplib.FTP") class constructor as
  well as the `connect()` method. (Added by Facundo Batista.)
  Also, the `FTP` class’s `storbinary()` and
  `storlines()` now take an optional *callback* parameter that
  will be called with each block of data after the data has been sent.
  (Contributed by Phil Schwartz; [bpo-1221598](https://bugs.python.org/issue?@action=redirect&bpo=1221598).)
* The `reduce()` built-in function is also available in the
  [`functools`](../library/functools.html#module-functools "functools: Higher-order functions and operations on callable objects.") module. In Python 3.0, the builtin has been
  dropped and `reduce()` is only available from [`functools`](../library/functools.html#module-functools "functools: Higher-order functions and operations on callable objects.");
  currently there are no plans to drop the builtin in the 2.x series.
  (Patched by Christian Heimes; [bpo-1739906](https://bugs.python.org/issue?@action=redirect&bpo=1739906).)
* When possible, the [`getpass`](../library/getpass.html#module-getpass "getpass: Portable reading of passwords and retrieval of the userid.") module will now use
  `/dev/tty` to print a prompt message and read the password,
  falling back to standard error and standard input. If the
  password may be echoed to the terminal, a warning is printed before
  the prompt is displayed. (Contributed by Gregory P. Smith.)
* The [`glob.glob()`](../library/glob.html#glob.glob "glob.glob") function can now return Unicode filenames if
  a Unicode path was used and Unicode filenames are matched within the
  directory. ([bpo-1001604](https://bugs.python.org/issue?@action=redirect&bpo=1001604))
* A new function in the [`heapq`](../library/heapq.html#module-heapq "heapq: Heap queue algorithm (a.k.a. priority queue).") module, `merge(iter1, iter2, ...)`,
  takes any number of iterables returning data in sorted
  order, and returns a new generator that returns the contents of all
  the iterators, also in sorted order. For example:

  Copy

  ```
  >>> list(heapq.merge([1, 3, 5, 9], [2, 8, 16]))
  [1, 2, 3, 5, 8, 9, 16]

  ```

  Another new function, `heappushpop(heap, item)`,
  pushes *item* onto *heap*, then pops off and returns the smallest item.
  This is more efficient than making a call to `heappush()` and then
  `heappop()`.

  [`heapq`](../library/heapq.html#module-heapq "heapq: Heap queue algorithm (a.k.a. priority queue).") is now implemented to only use less-than comparison,
  instead of the less-than-or-equal comparison it previously used.
  This makes [`heapq`](../library/heapq.html#module-heapq "heapq: Heap queue algorithm (a.k.a. priority queue).")’s usage of a type match the
  [`list.sort()`](../library/stdtypes.html#list.sort "list.sort") method.
  (Contributed by Raymond Hettinger.)
* An optional `timeout` parameter, specifying a timeout measured in
  seconds, was added to the [`httplib.HTTPConnection`](../library/http.client.html#http.client.HTTPConnection "http.client.HTTPConnection") and
  [`HTTPSConnection`](../library/http.client.html#http.client.HTTPSConnection "http.client.HTTPSConnection") class constructors. (Added by Facundo
  Batista.)
* Most of the [`inspect`](../library/inspect.html#module-inspect "inspect: Extract information and source code from live objects.") module’s functions, such as
  `getmoduleinfo()` and `getargs()`, now return named tuples.
  In addition to behaving like tuples, the elements of the return value
  can also be accessed as attributes.
  (Contributed by Raymond Hettinger.)

  Some new functions in the module include
  `isgenerator()`, `isgeneratorfunction()`,
  and `isabstract()`.
* The [`itertools`](../library/itertools.html#module-itertools "itertools: Functions creating iterators for efficient looping.") module gained several new functions.

  `izip_longest(iter1, iter2, ...[, fillvalue])` makes tuples from
  each of the elements; if some of the iterables are shorter than
  others, the missing values are set to *fillvalue*. For example:

  Copy

  ```
  >>> tuple(itertools.izip_longest([1,2,3], [1,2,3,4,5]))
  ((1, 1), (2, 2), (3, 3), (None, 4), (None, 5))

  ```

  `product(iter1, iter2, ..., [repeat=N])` returns the Cartesian product
  of the supplied iterables, a set of tuples containing
  every possible combination of the elements returned from each iterable.

  Copy

  ```
  >>> list(itertools.product([1,2,3], [4,5,6]))
  [(1, 4), (1, 5), (1, 6),
   (2, 4), (2, 5), (2, 6),
   (3, 4), (3, 5), (3, 6)]

  ```

  The optional *repeat* keyword argument is used for taking the
  product of an iterable or a set of iterables with themselves,
  repeated *N* times. With a single iterable argument, *N*-tuples
  are returned:

  Copy

  ```
  >>> list(itertools.product([1,2], repeat=3))
  [(1, 1, 1), (1, 1, 2), (1, 2, 1), (1, 2, 2),
   (2, 1, 1), (2, 1, 2), (2, 2, 1), (2, 2, 2)]

  ```

  With two iterables, *2N*-tuples are returned.

  Copy

  ```
  >>> list(itertools.product([1,2], [3,4], repeat=2))
  [(1, 3, 1, 3), (1, 3, 1, 4), (1, 3, 2, 3), (1, 3, 2, 4),
   (1, 4, 1, 3), (1, 4, 1, 4), (1, 4, 2, 3), (1, 4, 2, 4),
   (2, 3, 1, 3), (2, 3, 1, 4), (2, 3, 2, 3), (2, 3, 2, 4),
   (2, 4, 1, 3), (2, 4, 1, 4), (2, 4, 2, 3), (2, 4, 2, 4)]

  ```

  `combinations(iterable, r)` returns sub-sequences of length *r* from
  the elements of *iterable*.

  Copy

  ```
  >>> list(itertools.combinations('123', 2))
  [('1', '2'), ('1', '3'), ('2', '3')]
  >>> list(itertools.combinations('123', 3))
  [('1', '2', '3')]
  >>> list(itertools.combinations('1234', 3))
  [('1', '2', '3'), ('1', '2', '4'),
   ('1', '3', '4'), ('2', '3', '4')]

  ```

  `permutations(iter[, r])` returns all the permutations of length *r* of
  the iterable’s elements. If *r* is not specified, it will default to the
  number of elements produced by the iterable.

  Copy

  ```
  >>> list(itertools.permutations([1,2,3,4], 2))
  [(1, 2), (1, 3), (1, 4),
   (2, 1), (2, 3), (2, 4),
   (3, 1), (3, 2), (3, 4),
   (4, 1), (4, 2), (4, 3)]

  ```

  `itertools.chain(*iterables)` is an existing function in
  [`itertools`](../library/itertools.html#module-itertools "itertools: Functions creating iterators for efficient looping.") that gained a new constructor in Python 2.6.
  `itertools.chain.from_iterable(iterable)` takes a single
  iterable that should return other iterables. `chain()` will
  then return all the elements of the first iterable, then
  all the elements of the second, and so on.

  Copy

  ```
  >>> list(itertools.chain.from_iterable([[1,2,3], [4,5,6]]))
  [1, 2, 3, 4, 5, 6]

  ```

  (All contributed by Raymond Hettinger.)
* The [`logging`](../library/logging.html#module-logging "logging: Flexible event logging system for applications.") module’s `FileHandler` class
  and its subclasses `WatchedFileHandler`, `RotatingFileHandler`,
  and `TimedRotatingFileHandler` now
  have an optional *delay* parameter to their constructors. If *delay*
  is true, opening of the log file is deferred until the first
  `emit()` call is made. (Contributed by Vinay Sajip.)

  `TimedRotatingFileHandler` also has a *utc* constructor
  parameter. If the argument is true, UTC time will be used
  in determining when midnight occurs and in generating filenames;
  otherwise local time will be used.
* Several new functions were added to the [`math`](../library/math.html#module-math "math: Mathematical functions (sin() etc.).") module:

  + [`isinf()`](../library/math.html#math.isinf "math.isinf") and [`isnan()`](../library/math.html#math.isnan "math.isnan") determine whether a given float
    is a (positive or negative) infinity or a NaN (Not a Number), respectively.
  + [`copysign()`](../library/math.html#math.copysign "math.copysign") copies the sign bit of an IEEE 754 number,
    returning the absolute value of *x* combined with the sign bit of
    *y*. For example, `math.copysign(1, -0.0)` returns -1.0.
    (Contributed by Christian Heimes.)
  + [`factorial()`](../library/math.html#math.factorial "math.factorial") computes the factorial of a number.
    (Contributed by Raymond Hettinger; [bpo-2138](https://bugs.python.org/issue?@action=redirect&bpo=2138).)
  + [`fsum()`](../library/math.html#math.fsum "math.fsum") adds up the stream of numbers from an iterable,
    and is careful to avoid loss of precision through using partial sums.
    (Contributed by Jean Brouwers, Raymond Hettinger, and Mark Dickinson;
    [bpo-2819](https://bugs.python.org/issue?@action=redirect&bpo=2819).)
  + [`acosh()`](../library/math.html#math.acosh "math.acosh"), [`asinh()`](../library/math.html#math.asinh "math.asinh")
    and [`atanh()`](../library/math.html#math.atanh "math.atanh") compute the inverse hyperbolic functions.
  + [`log1p()`](../library/math.html#math.log1p "math.log1p") returns the natural logarithm of *1+x*
    (base *e*).
  + `trunc()` rounds a number toward zero, returning the closest
    `Integral` that’s between the function’s argument and zero.
    Added as part of the backport of
    [PEP 3141’s type hierarchy for numbers](#pep-3141).
* The [`math`](../library/math.html#module-math "math: Mathematical functions (sin() etc.).") module has been improved to give more consistent
  behaviour across platforms, especially with respect to handling of
  floating-point exceptions and IEEE 754 special values.

  Whenever possible, the module follows the recommendations of the C99
  standard about 754’s special values. For example, `sqrt(-1.)`
  should now give a [`ValueError`](../library/exceptions.html#ValueError "ValueError") across almost all platforms,
  while `sqrt(float('NaN'))` should return a NaN on all IEEE 754
  platforms. Where Annex ‘F’ of the C99 standard recommends signaling
  ‘divide-by-zero’ or ‘invalid’, Python will raise [`ValueError`](../library/exceptions.html#ValueError "ValueError").
  Where Annex ‘F’ of the C99 standard recommends signaling ‘overflow’,
  Python will raise [`OverflowError`](../library/exceptions.html#OverflowError "OverflowError"). (See [bpo-711019](https://bugs.python.org/issue?@action=redirect&bpo=711019) and
  [bpo-1640](https://bugs.python.org/issue?@action=redirect&bpo=1640).)

  (Contributed by Christian Heimes and Mark Dickinson.)
* [`mmap`](../library/mmap.html#mmap.mmap "mmap.mmap") objects now have a `rfind()` method that searches for a
  substring beginning at the end of the string and searching
  backwards. The `find()` method also gained an *end* parameter
  giving an index at which to stop searching.
  (Contributed by John Lenton.)
* The [`operator`](../library/operator.html#module-operator "operator: Functions corresponding to the standard operators.") module gained a
  `methodcaller()` function that takes a name and an optional
  set of arguments, returning a callable that will call
  the named function on any arguments passed to it. For example:

  Copy

  ```
  >>> # Equivalent to lambda s: s.replace('old', 'new')
  >>> replacer = operator.methodcaller('replace', 'old', 'new')
  >>> replacer('old wine in old bottles')
  'new wine in new bottles'

  ```

  (Contributed by Georg Brandl, after a suggestion by Gregory Petrosyan.)

  The `attrgetter()` function now accepts dotted names and performs
  the corresponding attribute lookups:

  Copy

  ```
  >>> inst_name = operator.attrgetter(
  ...        '__class__.__name__')
  >>> inst_name('')
  'str'
  >>> inst_name(help)
  '_Helper'

  ```

  (Contributed by Georg Brandl, after a suggestion by Barry Warsaw.)
* The [`os`](../library/os.html#module-os "os: Miscellaneous operating system interfaces.") module now wraps several new system calls.
  `fchmod(fd, mode)` and `fchown(fd, uid, gid)` change the mode
  and ownership of an opened file, and `lchmod(path, mode)` changes
  the mode of a symlink. (Contributed by Georg Brandl and Christian
  Heimes.)

  `chflags()` and `lchflags()` are wrappers for the
  corresponding system calls (where they’re available), changing the
  flags set on a file. Constants for the flag values are defined in
  the [`stat`](../library/stat.html#module-stat "stat: Utilities for interpreting the results of os.stat(), os.lstat() and os.fstat().") module; some possible values include
  `UF_IMMUTABLE` to signal the file may not be changed and
  `UF_APPEND` to indicate that data can only be appended to the
  file. (Contributed by M. Levinson.)

  `os.closerange(low, high)` efficiently closes all file descriptors
  from *low* to *high*, ignoring any errors and not including *high* itself.
  This function is now used by the [`subprocess`](../library/subprocess.html#module-subprocess "subprocess: Subprocess management.") module to make starting
  processes faster. (Contributed by Georg Brandl; [bpo-1663329](https://bugs.python.org/issue?@action=redirect&bpo=1663329).)
* The `os.environ` object’s `clear()` method will now unset the
  environment variables using [`os.unsetenv()`](../library/os.html#os.unsetenv "os.unsetenv") in addition to clearing
  the object’s keys. (Contributed by Martin Horcicka; [bpo-1181](https://bugs.python.org/issue?@action=redirect&bpo=1181).)
* The [`os.walk()`](../library/os.html#os.walk "os.walk") function now has a `followlinks` parameter. If
  set to True, it will follow symlinks pointing to directories and
  visit the directory’s contents. For backward compatibility, the
  parameter’s default value is false. Note that the function can fall
  into an infinite recursion if there’s a symlink that points to a
  parent directory. ([bpo-1273829](https://bugs.python.org/issue?@action=redirect&bpo=1273829))
* In the [`os.path`](../library/os.path.html#module-os.path "os.path: Operations on pathnames.") module, the `splitext()` function
  has been changed to not split on leading period characters.
  This produces better results when operating on Unix’s dot-files.
  For example, `os.path.splitext('.ipython')`
  now returns `('.ipython', '')` instead of `('', '.ipython')`.
  ([bpo-1115886](https://bugs.python.org/issue?@action=redirect&bpo=1115886))

  A new function, `os.path.relpath(path, start='.')`, returns a relative path
  from the `start` path, if it’s supplied, or from the current
  working directory to the destination `path`. (Contributed by
  Richard Barran; [bpo-1339796](https://bugs.python.org/issue?@action=redirect&bpo=1339796).)

  On Windows, [`os.path.expandvars()`](../library/os.path.html#os.path.expandvars "os.path.expandvars") will now expand environment variables
  given in the form “%var%”, and “~user” will be expanded into the
  user’s home directory path. (Contributed by Josiah Carlson;
  [bpo-957650](https://bugs.python.org/issue?@action=redirect&bpo=957650).)
* The Python debugger provided by the [`pdb`](../library/pdb.html#module-pdb "pdb: The Python debugger for interactive interpreters.") module
  gained a new command: “run” restarts the Python program being debugged
  and can optionally take new command-line arguments for the program.
  (Contributed by Rocky Bernstein; [bpo-1393667](https://bugs.python.org/issue?@action=redirect&bpo=1393667).)
* The [`pdb.post_mortem()`](../library/pdb.html#pdb.post_mortem "pdb.post_mortem") function, used to begin debugging a
  traceback, will now use the traceback returned by [`sys.exc_info()`](../library/sys.html#sys.exc_info "sys.exc_info")
  if no traceback is supplied. (Contributed by Facundo Batista;
  [bpo-1106316](https://bugs.python.org/issue?@action=redirect&bpo=1106316).)
* The [`pickletools`](../library/pickletools.html#module-pickletools "pickletools: Contains extensive comments about the pickle protocols and pickle-machine opcodes, as well as some useful functions.") module now has an `optimize()` function
  that takes a string containing a pickle and removes some unused
  opcodes, returning a shorter pickle that contains the same data structure.
  (Contributed by Raymond Hettinger.)
* A `get_data()` function was added to the [`pkgutil`](../library/pkgutil.html#module-pkgutil "pkgutil: Utilities for the import system.")
  module that returns the contents of resource files included
  with an installed Python package. For example:

  Copy

  ```
  >>> import pkgutil
  >>> print pkgutil.get_data('test', 'exception_hierarchy.txt')
  BaseException
   +-- SystemExit
   +-- KeyboardInterrupt
   +-- GeneratorExit
   +-- Exception
        +-- StopIteration
        +-- StandardError
   ...

  ```

  (Contributed by Paul Moore; [bpo-2439](https://bugs.python.org/issue?@action=redirect&bpo=2439).)
* The `pyexpat` module’s `Parser` objects now allow setting
  their `buffer_size` attribute to change the size of the buffer
  used to hold character data.
  (Contributed by Achim Gaedke; [bpo-1137](https://bugs.python.org/issue?@action=redirect&bpo=1137).)
* The `Queue` module now provides queue variants that retrieve entries
  in different orders. The `PriorityQueue` class stores
  queued items in a heap and retrieves them in priority order,
  and `LifoQueue` retrieves the most recently added entries first,
  meaning that it behaves like a stack.
  (Contributed by Raymond Hettinger.)
* The [`random`](../library/random.html#module-random "random: Generate pseudo-random numbers with various common distributions.") module’s `Random` objects can
  now be pickled on a 32-bit system and unpickled on a 64-bit
  system, and vice versa. Unfortunately, this change also means
  that Python 2.6’s `Random` objects can’t be unpickled correctly
  on earlier versions of Python.
  (Contributed by Shawn Ligocki; [bpo-1727780](https://bugs.python.org/issue?@action=redirect&bpo=1727780).)

  The new `triangular(low, high, mode)` function returns random
  numbers following a triangular distribution. The returned values
  are between *low* and *high*, not including *high* itself, and
  with *mode* as the most frequently occurring value
  in the distribution. (Contributed by Wladmir van der Laan and
  Raymond Hettinger; [bpo-1681432](https://bugs.python.org/issue?@action=redirect&bpo=1681432).)
* Long regular expression searches carried out by the [`re`](../library/re.html#module-re "re: Regular expression operations.")
  module will check for signals being delivered, so
  time-consuming searches can now be interrupted.
  (Contributed by Josh Hoyt and Ralf Schmitt; [bpo-846388](https://bugs.python.org/issue?@action=redirect&bpo=846388).)

  The regular expression module is implemented by compiling bytecodes
  for a tiny regex-specific virtual machine. Untrusted code
  could create malicious strings of bytecode directly and cause crashes,
  so Python 2.6 includes a verifier for the regex bytecode.
  (Contributed by Guido van Rossum from work for Google App Engine;
  [bpo-3487](https://bugs.python.org/issue?@action=redirect&bpo=3487).)
* The [`rlcompleter`](../library/rlcompleter.html#module-rlcompleter "rlcompleter: Python identifier completion, suitable for the GNU readline library.") module’s `Completer.complete()` method
  will now ignore exceptions triggered while evaluating a name.
  (Fixed by Lorenz Quack; [bpo-2250](https://bugs.python.org/issue?@action=redirect&bpo=2250).)
* The [`sched`](../library/sched.html#module-sched "sched: General purpose event scheduler.") module’s `scheduler` instances now
  have a read-only [`queue`](../library/queue.html#module-queue "queue: A synchronized queue class.") attribute that returns the
  contents of the scheduler’s queue, represented as a list of
  named tuples with the fields `(time, priority, action, argument)`.
  (Contributed by Raymond Hettinger; [bpo-1861](https://bugs.python.org/issue?@action=redirect&bpo=1861).)
* The [`select`](../library/select.html#module-select "select: Wait for I/O completion on multiple streams.") module now has wrapper functions
  for the Linux `epoll()` and BSD `kqueue()` system calls.
  `modify()` method was added to the existing `poll`
  objects; `pollobj.modify(fd, eventmask)` takes a file descriptor
  or file object and an event mask, modifying the recorded event mask
  for that file.
  (Contributed by Christian Heimes; [bpo-1657](https://bugs.python.org/issue?@action=redirect&bpo=1657).)
* The [`shutil.copytree()`](../library/shutil.html#shutil.copytree "shutil.copytree") function now has an optional *ignore* argument
  that takes a callable object. This callable will receive each directory path
  and a list of the directory’s contents, and returns a list of names that
  will be ignored, not copied.

  The [`shutil`](../library/shutil.html#module-shutil "shutil: High-level file operations, including copying.") module also provides an `ignore_patterns()`
  function for use with this new parameter. `ignore_patterns()`
  takes an arbitrary number of glob-style patterns and returns a
  callable that will ignore any files and directories that match any
  of these patterns. The following example copies a directory tree,
  but skips both `.svn` directories and Emacs backup files,
  which have names ending with ‘~’:

  Copy

  ```
  shutil.copytree('Doc/library', '/tmp/library',
                  ignore=shutil.ignore_patterns('*~', '.svn'))

  ```

  (Contributed by Tarek Ziadé; [bpo-2663](https://bugs.python.org/issue?@action=redirect&bpo=2663).)
* Integrating signal handling with GUI handling event loops
  like those used by Tkinter or GTk+ has long been a problem; most
  software ends up polling, waking up every fraction of a second to check
  if any GUI events have occurred.
  The [`signal`](../library/signal.html#module-signal "signal: Set handlers for asynchronous events.") module can now make this more efficient.
  Calling `signal.set_wakeup_fd(fd)` sets a file descriptor
  to be used; when a signal is received, a byte is written to that
  file descriptor. There’s also a C-level function,
  [`PySignal_SetWakeupFd()`](../c-api/exceptions.html#c.PySignal_SetWakeupFd "PySignal_SetWakeupFd"), for setting the descriptor.

  Event loops will use this by opening a pipe to create two descriptors,
  one for reading and one for writing. The writable descriptor
  will be passed to `set_wakeup_fd()`, and the readable descriptor
  will be added to the list of descriptors monitored by the event loop via
  `select()` or `poll()`.
  On receiving a signal, a byte will be written and the main event loop
  will be woken up, avoiding the need to poll.

  (Contributed by Adam Olsen; [bpo-1583](https://bugs.python.org/issue?@action=redirect&bpo=1583).)

  The `siginterrupt()` function is now available from Python code,
  and allows changing whether signals can interrupt system calls or not.
  (Contributed by Ralf Schmitt.)

  The `setitimer()` and `getitimer()` functions have also been
  added (where they’re available). `setitimer()`
  allows setting interval timers that will cause a signal to be
  delivered to the process after a specified time, measured in
  wall-clock time, consumed process time, or combined process+system
  time. (Contributed by Guilherme Polo; [bpo-2240](https://bugs.python.org/issue?@action=redirect&bpo=2240).)
* The [`smtplib`](../library/smtplib.html#module-smtplib "smtplib: SMTP protocol client (requires sockets).") module now supports SMTP over SSL thanks to the
  addition of the `SMTP_SSL` class. This class supports an
  interface identical to the existing `SMTP` class.
  (Contributed by Monty Taylor.) Both class constructors also have an
  optional `timeout` parameter that specifies a timeout for the
  initial connection attempt, measured in seconds. (Contributed by
  Facundo Batista.)

  An implementation of the LMTP protocol ([**RFC 2033**](https://datatracker.ietf.org/doc/html/rfc2033.html)) was also added
  to the module. LMTP is used in place of SMTP when transferring
  e-mail between agents that don’t manage a mail queue. (LMTP
  implemented by Leif Hedstrom; [bpo-957003](https://bugs.python.org/issue?@action=redirect&bpo=957003).)

  `SMTP.starttls()` now complies with [**RFC 3207**](https://datatracker.ietf.org/doc/html/rfc3207.html) and forgets any
  knowledge obtained from the server not obtained from the TLS
  negotiation itself. (Patch contributed by Bill Fenner;
  [bpo-829951](https://bugs.python.org/issue?@action=redirect&bpo=829951).)
* The [`socket`](../library/socket.html#module-socket "socket: Low-level networking interface.") module now supports TIPC (<https://tipc.sourceforge.net/>),
  a high-performance non-IP-based protocol designed for use in clustered
  environments. TIPC addresses are 4- or 5-tuples.
  (Contributed by Alberto Bertogli; [bpo-1646](https://bugs.python.org/issue?@action=redirect&bpo=1646).)

  A new function, `create_connection()`, takes an address and
  connects to it using an optional timeout value, returning the
  connected socket object. This function also looks up the address’s
  type and connects to it using IPv4 or IPv6 as appropriate. Changing
  your code to use `create_connection()` instead of
  `socket(socket.AF_INET, ...)` may be all that’s required to make
  your code work with IPv6.
* The base classes in the [`SocketServer`](../library/socketserver.html#module-socketserver "socketserver: A framework for network servers.") module now support
  calling a [`handle_timeout()`](../library/socketserver.html#socketserver.BaseServer.handle_timeout "socketserver.BaseServer.handle_timeout") method after a span of inactivity
  specified by the server’s [`timeout`](../library/socketserver.html#socketserver.BaseServer.timeout "socketserver.BaseServer.timeout") attribute. (Contributed
  by Michael Pomraning.) The [`serve_forever()`](../library/socketserver.html#socketserver.BaseServer.serve_forever "socketserver.BaseServer.serve_forever") method
  now takes an optional poll interval measured in seconds,
  controlling how often the server will check for a shutdown request.
  (Contributed by Pedro Werneck and Jeffrey Yasskin;
  [bpo-742598](https://bugs.python.org/issue?@action=redirect&bpo=742598), [bpo-1193577](https://bugs.python.org/issue?@action=redirect&bpo=1193577).)
* The [`sqlite3`](../library/sqlite3.html#module-sqlite3 "sqlite3: A DB-API 2.0 implementation using SQLite 3.x.") module, maintained by Gerhard Häring,
  has been updated from version 2.3.2 in Python 2.5 to
  version 2.4.1.
* The [`struct`](../library/struct.html#module-struct "struct: Interpret bytes as packed binary data.") module now supports the C99 \_Bool type,
  using the format character `'?'`.
  (Contributed by David Remahl.)
* The [`Popen`](../library/subprocess.html#subprocess.Popen "subprocess.Popen") objects provided by the [`subprocess`](../library/subprocess.html#module-subprocess "subprocess: Subprocess management.") module
  now have [`terminate()`](../library/subprocess.html#subprocess.Popen.terminate "subprocess.Popen.terminate"), [`kill()`](../library/subprocess.html#subprocess.Popen.kill "subprocess.Popen.kill"), and [`send_signal()`](../library/subprocess.html#subprocess.Popen.send_signal "subprocess.Popen.send_signal") methods.
  On Windows, `send_signal()` only supports the [`SIGTERM`](../library/signal.html#signal.SIGTERM "signal.SIGTERM")
  signal, and all these methods are aliases for the Win32 API function
  `TerminateProcess()`.
  (Contributed by Christian Heimes.)
* A new variable in the [`sys`](../library/sys.html#module-sys "sys: Access system-specific parameters and functions.") module, `float_info`, is an
  object containing information derived from the `float.h` file
  about the platform’s floating-point support. Attributes of this
  object include `mant_dig` (number of digits in the mantissa),
  `epsilon` (smallest difference between 1.0 and the next
  largest value representable), and several others. (Contributed by
  Christian Heimes; [bpo-1534](https://bugs.python.org/issue?@action=redirect&bpo=1534).)

  Another new variable, `dont_write_bytecode`, controls whether Python
  writes any `.pyc` or `.pyo` files on importing a module.
  If this variable is true, the compiled files are not written. The
  variable is initially set on start-up by supplying the [`-B`](../using/cmdline.html#cmdoption-B)
  switch to the Python interpreter, or by setting the
  [`PYTHONDONTWRITEBYTECODE`](../using/cmdline.html#envvar-PYTHONDONTWRITEBYTECODE) environment variable before
  running the interpreter. Python code can subsequently
  change the value of this variable to control whether bytecode files
  are written or not.
  (Contributed by Neal Norwitz and Georg Brandl.)

  Information about the command-line arguments supplied to the Python
  interpreter is available by reading attributes of a named
  tuple available as `sys.flags`. For example, the `verbose`
  attribute is true if Python
  was executed in verbose mode, `debug` is true in debugging mode, etc.
  These attributes are all read-only.
  (Contributed by Christian Heimes.)

  A new function, `getsizeof()`, takes a Python object and returns
  the amount of memory used by the object, measured in bytes. Built-in
  objects return correct results; third-party extensions may not,
  but can define a `__sizeof__()` method to return the
  object’s size.
  (Contributed by Robert Schuppenies; [bpo-2898](https://bugs.python.org/issue?@action=redirect&bpo=2898).)

  It’s now possible to determine the current profiler and tracer functions
  by calling [`sys.getprofile()`](../library/sys.html#sys.getprofile "sys.getprofile") and [`sys.gettrace()`](../library/sys.html#sys.gettrace "sys.gettrace").
  (Contributed by Georg Brandl; [bpo-1648](https://bugs.python.org/issue?@action=redirect&bpo=1648).)
* The [`tarfile`](../library/tarfile.html#module-tarfile "tarfile: Read and write tar-format archive files.") module now supports POSIX.1-2001 (pax) tarfiles in
  addition to the POSIX.1-1988 (ustar) and GNU tar formats that were
  already supported. The default format is GNU tar; specify the
  `format` parameter to open a file using a different format:

  Copy

  ```
  tar = tarfile.open("output.tar", "w",
                     format=tarfile.PAX_FORMAT)

  ```

  The new `encoding` and `errors` parameters specify an encoding and
  an error handling scheme for character conversions. `'strict'`,
  `'ignore'`, and `'replace'` are the three standard ways Python can
  handle errors,;
  `'utf-8'` is a special value that replaces bad characters with
  their UTF-8 representation. (Character conversions occur because the
  PAX format supports Unicode filenames, defaulting to UTF-8 encoding.)

  The `TarFile.add()` method now accepts an `exclude` argument that’s
  a function that can be used to exclude certain filenames from
  an archive.
  The function must take a filename and return true if the file
  should be excluded or false if it should be archived.
  The function is applied to both the name initially passed to `add()`
  and to the names of files in recursively added directories.

  (All changes contributed by Lars Gustäbel).
* An optional `timeout` parameter was added to the
  `telnetlib.Telnet` class constructor, specifying a timeout
  measured in seconds. (Added by Facundo Batista.)
* The [`tempfile.NamedTemporaryFile`](../library/tempfile.html#tempfile.NamedTemporaryFile "tempfile.NamedTemporaryFile") class usually deletes
  the temporary file it created when the file is closed. This
  behaviour can now be changed by passing `delete=False` to the
  constructor. (Contributed by Damien Miller; [bpo-1537850](https://bugs.python.org/issue?@action=redirect&bpo=1537850).)

  A new class, `SpooledTemporaryFile`, behaves like
  a temporary file but stores its data in memory until a maximum size is
  exceeded. On reaching that limit, the contents will be written to
  an on-disk temporary file. (Contributed by Dustin J. Mitchell.)

  The `NamedTemporaryFile` and `SpooledTemporaryFile` classes
  both work as context managers, so you can write
  `with tempfile.NamedTemporaryFile() as tmp: ...`.
  (Contributed by Alexander Belopolsky; [bpo-2021](https://bugs.python.org/issue?@action=redirect&bpo=2021).)
* The [`test.test_support`](../library/test.html#module-test.support "test.support: Support for Python's regression test suite.") module gained a number
  of context managers useful for writing tests.
  [`EnvironmentVarGuard()`](../library/test.html#test.support.os_helper.EnvironmentVarGuard "test.support.os_helper.EnvironmentVarGuard") is a
  context manager that temporarily changes environment variables and
  automatically restores them to their old values.

  Another context manager, `TransientResource`, can surround calls
  to resources that may or may not be available; it will catch and
  ignore a specified list of exceptions. For example,
  a network test may ignore certain failures when connecting to an
  external web site:

  Copy

  ```
  with test_support.TransientResource(IOError,
                                  errno=errno.ETIMEDOUT):
      f = urllib.urlopen('https://sf.net')
      ...

  ```

  Finally, `check_warnings()` resets the `warning` module’s
  warning filters and returns an object that will record all warning
  messages triggered ([bpo-3781](https://bugs.python.org/issue?@action=redirect&bpo=3781)):

  Copy

  ```
  with test_support.check_warnings() as wrec:
      warnings.simplefilter("always")
      # ... code that triggers a warning ...
      assert str(wrec.message) == "function is outdated"
      assert len(wrec.warnings) == 1, "Multiple warnings raised"

  ```

  (Contributed by Brett Cannon.)
* The [`textwrap`](../library/textwrap.html#module-textwrap "textwrap: Text wrapping and filling") module can now preserve existing whitespace
  at the beginnings and ends of the newly created lines
  by specifying `drop_whitespace=False`
  as an argument:

  Copy

  ```
  >>> S = """This  sentence  has a bunch   of
  ...   extra   whitespace."""
  >>> print textwrap.fill(S, width=15)
  This  sentence
  has a bunch
  of    extra
  whitespace.
  >>> print textwrap.fill(S, drop_whitespace=False, width=15)
  This  sentence
    has a bunch
     of    extra
     whitespace.
  >>>

  ```

  (Contributed by Dwayne Bailey; [bpo-1581073](https://bugs.python.org/issue?@action=redirect&bpo=1581073).)
* The [`threading`](../library/threading.html#module-threading "threading: Thread-based parallelism.") module API is being changed to use properties
  such as `daemon` instead of `setDaemon()` and
  `isDaemon()` methods, and some methods have been renamed to use
  underscores instead of camel-case; for example, the
  `activeCount()` method is renamed to `active_count()`. Both
  the 2.6 and 3.0 versions of the module support the same properties
  and renamed methods, but don’t remove the old methods. No date has been set
  for the deprecation of the old APIs in Python 3.x; the old APIs won’t
  be removed in any 2.x version.
  (Carried out by several people, most notably Benjamin Peterson.)

  The [`threading`](../library/threading.html#module-threading "threading: Thread-based parallelism.") module’s `Thread` objects
  gained an `ident` property that returns the thread’s
  identifier, a nonzero integer. (Contributed by Gregory P. Smith;
  [bpo-2871](https://bugs.python.org/issue?@action=redirect&bpo=2871).)
* The [`timeit`](../library/timeit.html#module-timeit "timeit: Measure the execution time of small code snippets.") module now accepts callables as well as strings
  for the statement being timed and for the setup code.
  Two convenience functions were added for creating
  `Timer` instances:
  `repeat(stmt, setup, time, repeat, number)` and
  `timeit(stmt, setup, time, number)` create an instance and call
  the corresponding method. (Contributed by Erik Demaine;
  [bpo-1533909](https://bugs.python.org/issue?@action=redirect&bpo=1533909).)
* The `Tkinter` module now accepts lists and tuples for options,
  separating the elements by spaces before passing the resulting value to
  Tcl/Tk.
  (Contributed by Guilherme Polo; [bpo-2906](https://bugs.python.org/issue?@action=redirect&bpo=2906).)
* The [`turtle`](../library/turtle.html#module-turtle "turtle: An educational framework for simple graphics applications") module for turtle graphics was greatly enhanced by
  Gregor Lingl. New features in the module include:

  + Better animation of turtle movement and rotation.
  + Control over turtle movement using the new `delay()`,
    `tracer()`, and `speed()` methods.
  + The ability to set new shapes for the turtle, and to
    define a new coordinate system.
  + Turtles now have an `undo()` method that can roll back actions.
  + Simple support for reacting to input events such as mouse and keyboard
    activity, making it possible to write simple games.
  + A `turtle.cfg` file can be used to customize the starting appearance
    of the turtle’s screen.
  + The module’s docstrings can be replaced by new docstrings that have been
    translated into another language.

  ([bpo-1513695](https://bugs.python.org/issue?@action=redirect&bpo=1513695))
* An optional `timeout` parameter was added to the
  [`urllib.urlopen`](../library/urllib.request.html#urllib.request.urlopen "urllib.request.urlopen") function and the
  `urllib.ftpwrapper` class constructor, as well as the
  [`urllib2.urlopen`](../library/urllib.request.html#urllib.request.urlopen "urllib.request.urlopen") function. The parameter specifies a timeout
  measured in seconds. For example:

  Copy

  ```
  >>> u = urllib2.urlopen("http://slow.example.com",
                          timeout=3)
  Traceback (most recent call last):
    ...
  urllib2.URLError: <urlopen error timed out>
  >>>

  ```

  (Added by Facundo Batista.)
* The Unicode database provided by the [`unicodedata`](../library/unicodedata.html#module-unicodedata "unicodedata: Access the Unicode Database.") module
  has been updated to version 5.1.0. (Updated by
  Martin von Löwis; [bpo-3811](https://bugs.python.org/issue?@action=redirect&bpo=3811).)
* The [`warnings`](../library/warnings.html#module-warnings "warnings: Issue warning messages and control their disposition.") module’s `formatwarning()` and `showwarning()`
  gained an optional *line* argument that can be used to supply the
  line of source code. (Added as part of [bpo-1631171](https://bugs.python.org/issue?@action=redirect&bpo=1631171), which re-implemented
  part of the [`warnings`](../library/warnings.html#module-warnings "warnings: Issue warning messages and control their disposition.") module in C code.)

  A new function, `catch_warnings()`, is a context manager
  intended for testing purposes that lets you temporarily modify the
  warning filters and then restore their original values ([bpo-3781](https://bugs.python.org/issue?@action=redirect&bpo=3781)).
* The XML-RPC [`SimpleXMLRPCServer`](../library/xmlrpc.server.html#module-xmlrpc.server "xmlrpc.server: Basic XML-RPC server implementations.") and [`DocXMLRPCServer`](../library/xmlrpc.server.html#module-xmlrpc.server "xmlrpc.server: Basic XML-RPC server implementations.")
  classes can now be prevented from immediately opening and binding to
  their socket by passing `False` as the *bind\_and\_activate*
  constructor parameter. This can be used to modify the instance’s
  `allow_reuse_address` attribute before calling the
  `server_bind()` and `server_activate()` methods to
  open the socket and begin listening for connections.
  (Contributed by Peter Parente; [bpo-1599845](https://bugs.python.org/issue?@action=redirect&bpo=1599845).)

  `SimpleXMLRPCServer` also has a `_send_traceback_header`
  attribute; if true, the exception and formatted traceback are returned
  as HTTP headers “X-Exception” and “X-Traceback”. This feature is
  for debugging purposes only and should not be used on production servers
  because the tracebacks might reveal passwords or other sensitive
  information. (Contributed by Alan McIntyre as part of his
  project for Google’s Summer of Code 2007.)
* The [`xmlrpclib`](../library/xmlrpc.client.html#module-xmlrpc.client "xmlrpc.client: XML-RPC client access.") module no longer automatically converts
  [`datetime.date`](../library/datetime.html#datetime.date "datetime.date") and [`datetime.time`](../library/datetime.html#datetime.time "datetime.time") to the
  [`xmlrpclib.DateTime`](../library/xmlrpc.client.html#xmlrpc.client.DateTime "xmlrpc.client.DateTime") type; the conversion semantics were
  not necessarily correct for all applications. Code using
  `xmlrpclib` should convert `date` and [`time`](../library/datetime.html#datetime.time "datetime.time")
  instances. ([bpo-1330538](https://bugs.python.org/issue?@action=redirect&bpo=1330538)) The code can also handle
  dates before 1900 (contributed by Ralf Schmitt; [bpo-2014](https://bugs.python.org/issue?@action=redirect&bpo=2014))
  and 64-bit integers represented by using `<i8>` in XML-RPC responses
  (contributed by Riku Lindblad; [bpo-2985](https://bugs.python.org/issue?@action=redirect&bpo=2985)).
* The [`zipfile`](../library/zipfile.html#module-zipfile "zipfile: Read and write ZIP-format archive files.") module’s `ZipFile` class now has
  `extract()` and `extractall()` methods that will unpack
  a single file or all the files in the archive to the current directory, or
  to a specified directory:

  Copy

  ```
  z = zipfile.ZipFile('python-251.zip')

  # Unpack a single file, writing it relative
  # to the /tmp directory.
  z.extract('Python/sysmodule.c', '/tmp')

  # Unpack all the files in the archive.
  z.extractall()

  ```

  (Contributed by Alan McIntyre; [bpo-467924](https://bugs.python.org/issue?@action=redirect&bpo=467924).)

  The [`open()`](../library/functions.html#open "open"), `read()` and `extract()` methods can now
  take either a filename or a `ZipInfo` object. This is useful when an
  archive accidentally contains a duplicated filename.
  (Contributed by Graham Horler; [bpo-1775025](https://bugs.python.org/issue?@action=redirect&bpo=1775025).)

  Finally, [`zipfile`](../library/zipfile.html#module-zipfile "zipfile: Read and write ZIP-format archive files.") now supports using Unicode filenames
  for archived files. (Contributed by Alexey Borzenkov; [bpo-1734346](https://bugs.python.org/issue?@action=redirect&bpo=1734346).)