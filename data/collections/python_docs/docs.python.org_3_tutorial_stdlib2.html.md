11. Brief Tour of the Standard Library — Part II
================================================

This second tour covers more advanced modules that support professional
programming needs. These modules rarely occur in small scripts.

11.1. Output Formatting
-----------------------

The [`reprlib`](../library/reprlib.html#module-reprlib "reprlib: Alternate repr() implementation with size limits.") module provides a version of [`repr()`](../library/functions.html#repr "repr") customized for
abbreviated displays of large or deeply nested containers:

Copy

```
>>> import reprlib
>>> reprlib.repr(set('supercalifragilisticexpialidocious'))
"{'a', 'c', 'd', 'e', 'f', 'g', ...}"

```

The [`pprint`](../library/pprint.html#module-pprint "pprint: Data pretty printer.") module offers more sophisticated control over printing both
built-in and user defined objects in a way that is readable by the interpreter.
When the result is longer than one line, the “pretty printer” adds line breaks
and indentation to more clearly reveal data structure:

Copy

```
>>> import pprint
>>> t = [[[['black', 'cyan'], 'white', ['green', 'red']], [['magenta',
...     'yellow'], 'blue']]]
...
>>> pprint.pprint(t, width=30)
[[[['black', 'cyan'],
   'white',
   ['green', 'red']],
  [['magenta', 'yellow'],
   'blue']]]

```

The [`textwrap`](../library/textwrap.html#module-textwrap "textwrap: Text wrapping and filling") module formats paragraphs of text to fit a given screen
width:

Copy

```
>>> import textwrap
>>> doc = """The wrap() method is just like fill() except that it returns
... a list of strings instead of one big string with newlines to separate
... the wrapped lines."""
...
>>> print(textwrap.fill(doc, width=40))
The wrap() method is just like fill()
except that it returns a list of strings
instead of one big string with newlines
to separate the wrapped lines.

```

The [`locale`](../library/locale.html#module-locale "locale: Internationalization services.") module accesses a database of culture specific data formats.
The grouping attribute of locale’s format function provides a direct way of
formatting numbers with group separators:

Copy

```
>>> import locale
>>> locale.setlocale(locale.LC_ALL, 'English_United States.1252')
'English_United States.1252'
>>> conv = locale.localeconv()          # get a mapping of conventions
>>> x = 1234567.8
>>> locale.format_string("%d", x, grouping=True)
'1,234,567'
>>> locale.format_string("%s%.*f", (conv['currency_symbol'],
...                      conv['frac_digits'], x), grouping=True)
'$1,234,567.80'

```

11.2. Templating
----------------

The [`string`](../library/string.html#module-string "string: Common string operations.") module includes a versatile [`Template`](../library/string.html#string.Template "string.Template") class
with a simplified syntax suitable for editing by end-users. This allows users
to customize their applications without having to alter the application.

The format uses placeholder names formed by `$` with valid Python identifiers
(alphanumeric characters and underscores). Surrounding the placeholder with
braces allows it to be followed by more alphanumeric letters with no intervening
spaces. Writing `$$` creates a single escaped `$`:

Copy

```
>>> from string import Template
>>> t = Template('${village}folk send $$10 to $cause.')
>>> t.substitute(village='Nottingham', cause='the ditch fund')
'Nottinghamfolk send $10 to the ditch fund.'

```

The [`substitute()`](../library/string.html#string.Template.substitute "string.Template.substitute") method raises a [`KeyError`](../library/exceptions.html#KeyError "KeyError") when a
placeholder is not supplied in a dictionary or a keyword argument. For
mail-merge style applications, user supplied data may be incomplete and the
[`safe_substitute()`](../library/string.html#string.Template.safe_substitute "string.Template.safe_substitute") method may be more appropriate —
it will leave placeholders unchanged if data is missing:

Copy

```
>>> t = Template('Return the $item to $owner.')
>>> d = dict(item='unladen swallow')
>>> t.substitute(d)
Traceback (most recent call last):
  ...
KeyError: 'owner'
>>> t.safe_substitute(d)
'Return the unladen swallow to $owner.'

```

Template subclasses can specify a custom delimiter. For example, a batch
renaming utility for a photo browser may elect to use percent signs for
placeholders such as the current date, image sequence number, or file format:

Copy

```
>>> import time, os.path
>>> photofiles = ['img_1074.jpg', 'img_1076.jpg', 'img_1077.jpg']
>>> class BatchRename(Template):
...     delimiter = '%'
...
>>> fmt = input('Enter rename style (%d-date %n-seqnum %f-format):  ')
Enter rename style (%d-date %n-seqnum %f-format):  Ashley_%n%f

>>> t = BatchRename(fmt)
>>> date = time.strftime('%d%b%y')
>>> for i, filename in enumerate(photofiles):
...     base, ext = os.path.splitext(filename)
...     newname = t.substitute(d=date, n=i, f=ext)
...     print('{0} --> {1}'.format(filename, newname))

img_1074.jpg --> Ashley_0.jpg
img_1076.jpg --> Ashley_1.jpg
img_1077.jpg --> Ashley_2.jpg

```

Another application for templating is separating program logic from the details
of multiple output formats. This makes it possible to substitute custom
templates for XML files, plain text reports, and HTML web reports.

11.3. Working with Binary Data Record Layouts
---------------------------------------------

The [`struct`](../library/struct.html#module-struct "struct: Interpret bytes as packed binary data.") module provides [`pack()`](../library/struct.html#struct.pack "struct.pack") and
[`unpack()`](../library/struct.html#struct.unpack "struct.unpack") functions for working with variable length binary
record formats. The following example shows
how to loop through header information in a ZIP file without using the
[`zipfile`](../library/zipfile.html#module-zipfile "zipfile: Read and write ZIP-format archive files.") module. Pack codes `"H"` and `"I"` represent two and four
byte unsigned numbers respectively. The `"<"` indicates that they are
standard size and in little-endian byte order:

Copy

```
import struct

with open('myfile.zip', 'rb') as f:
    data = f.read()

start = 0
for i in range(3):                      # show the first 3 file headers
    start += 14
    fields = struct.unpack('<IIIHH', data[start:start+16])
    crc32, comp_size, uncomp_size, filenamesize, extra_size = fields

    start += 16
    filename = data[start:start+filenamesize]
    start += filenamesize
    extra = data[start:start+extra_size]
    print(filename, hex(crc32), comp_size, uncomp_size)

    start += extra_size + comp_size     # skip to the next header

```

11.4. Multi-threading
---------------------

Threading is a technique for decoupling tasks which are not sequentially
dependent. Threads can be used to improve the responsiveness of applications
that accept user input while other tasks run in the background. A related use
case is running I/O in parallel with computations in another thread.

The following code shows how the high level [`threading`](../library/threading.html#module-threading "threading: Thread-based parallelism.") module can run
tasks in background while the main program continues to run:

Copy

```
import threading, zipfile

class AsyncZip(threading.Thread):
    def __init__(self, infile, outfile):
        threading.Thread.__init__(self)
        self.infile = infile
        self.outfile = outfile

    def run(self):
        f = zipfile.ZipFile(self.outfile, 'w', zipfile.ZIP_DEFLATED)
        f.write(self.infile)
        f.close()
        print('Finished background zip of:', self.infile)

background = AsyncZip('mydata.txt', 'myarchive.zip')
background.start()
print('The main program continues to run in foreground.')

background.join()    # Wait for the background task to finish
print('Main program waited until background was done.')

```

The principal challenge of multi-threaded applications is coordinating threads
that share data or other resources. To that end, the threading module provides
a number of synchronization primitives including locks, events, condition
variables, and semaphores.

While those tools are powerful, minor design errors can result in problems that
are difficult to reproduce. So, the preferred approach to task coordination is
to concentrate all access to a resource in a single thread and then use the
[`queue`](../library/queue.html#module-queue "queue: A synchronized queue class.") module to feed that thread with requests from other threads.
Applications using [`Queue`](../library/queue.html#queue.Queue "queue.Queue") objects for inter-thread communication and
coordination are easier to design, more readable, and more reliable.

11.5. Logging
-------------

The [`logging`](../library/logging.html#module-logging "logging: Flexible event logging system for applications.") module offers a full featured and flexible logging system.
At its simplest, log messages are sent to a file or to `sys.stderr`:

Copy

```
import logging
logging.debug('Debugging information')
logging.info('Informational message')
logging.warning('Warning:config file %s not found', 'server.conf')
logging.error('Error occurred')
logging.critical('Critical error -- shutting down')

```

This produces the following output:

```
WARNING:root:Warning:config file server.conf not found
ERROR:root:Error occurred
CRITICAL:root:Critical error -- shutting down

```

By default, informational and debugging messages are suppressed and the output
is sent to standard error. Other output options include routing messages
through email, datagrams, sockets, or to an HTTP Server. New filters can select
different routing based on message priority: [`DEBUG`](../library/logging.html#logging.DEBUG "logging.DEBUG"),
[`INFO`](../library/logging.html#logging.INFO "logging.INFO"), [`WARNING`](../library/logging.html#logging.WARNING "logging.WARNING"), [`ERROR`](../library/logging.html#logging.ERROR "logging.ERROR"),
and [`CRITICAL`](../library/logging.html#logging.CRITICAL "logging.CRITICAL").

The logging system can be configured directly from Python or can be loaded from
a user editable configuration file for customized logging without altering the
application.

11.6. Weak References
---------------------

Python does automatic memory management (reference counting for most objects and
[garbage collection](../glossary.html#term-garbage-collection) to eliminate cycles). The memory is freed shortly
after the last reference to it has been eliminated.

This approach works fine for most applications but occasionally there is a need
to track objects only as long as they are being used by something else.
Unfortunately, just tracking them creates a reference that makes them permanent.
The [`weakref`](../library/weakref.html#module-weakref "weakref: Support for weak references and weak dictionaries.") module provides tools for tracking objects without creating a
reference. When the object is no longer needed, it is automatically removed
from a weakref table and a callback is triggered for weakref objects. Typical
applications include caching objects that are expensive to create:

Copy

```
>>> import weakref, gc
>>> class A:
...     def __init__(self, value):
...         self.value = value
...     def __repr__(self):
...         return str(self.value)
...
>>> a = A(10)                   # create a reference
>>> d = weakref.WeakValueDictionary()
>>> d['primary'] = a            # does not create a reference
>>> d['primary']                # fetch the object if it is still alive
10
>>> del a                       # remove the one reference
>>> gc.collect()                # run garbage collection right away
0
>>> d['primary']                # entry was automatically removed
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
    d['primary']                # entry was automatically removed
  File "C:/python313/lib/weakref.py", line 46, in __getitem__
    o = self.data[key]()
KeyError: 'primary'

```

11.8. Decimal Floating-Point Arithmetic
---------------------------------------

The [`decimal`](../library/decimal.html#module-decimal "decimal: Implementation of the General Decimal Arithmetic Specification.") module offers a [`Decimal`](../library/decimal.html#decimal.Decimal "decimal.Decimal") datatype for
decimal floating-point arithmetic. Compared to the built-in [`float`](../library/functions.html#float "float")
implementation of binary floating point, the class is especially helpful for

* financial applications and other uses which require exact decimal
  representation,
* control over precision,
* control over rounding to meet legal or regulatory requirements,
* tracking of significant decimal places, or
* applications where the user expects the results to match calculations done by
  hand.

For example, calculating a 5% tax on a 70 cent phone charge gives different
results in decimal floating point and binary floating point. The difference
becomes significant if the results are rounded to the nearest cent:

Copy

```
>>> from decimal import *
>>> round(Decimal('0.70') * Decimal('1.05'), 2)
Decimal('0.74')
>>> round(.70 * 1.05, 2)
0.73

```

The [`Decimal`](../library/decimal.html#decimal.Decimal "decimal.Decimal") result keeps a trailing zero, automatically
inferring four place significance from multiplicands with two place
significance. Decimal reproduces mathematics as done by hand and avoids
issues that can arise when binary floating point cannot exactly represent
decimal quantities.

Exact representation enables the [`Decimal`](../library/decimal.html#decimal.Decimal "decimal.Decimal") class to perform
modulo calculations and equality tests that are unsuitable for binary floating
point:

Copy

```
>>> Decimal('1.00') % Decimal('.10')
Decimal('0.00')
>>> 1.00 % 0.10
0.09999999999999995

>>> sum([Decimal('0.1')]*10) == Decimal('1.0')
True
>>> 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 == 1.0
False

```

The [`decimal`](../library/decimal.html#module-decimal "decimal: Implementation of the General Decimal Arithmetic Specification.") module provides arithmetic with as much precision as needed:

Copy

```
>>> getcontext().prec = 36
>>> Decimal(1) / Decimal(7)
Decimal('0.142857142857142857142857142857142857')

```